#!/usr/bin/python3
import os
from datetime import datetime
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg for non-GUI environments

import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/dataviz/', strict_slashes=False, methods=['GET'])
def landing():
    return render_template('index.html')


@app.route('/dataviz.app', strict_slashes=False, methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file:
            # Create timestamped filename and save file to uploads folder
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{file.filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)  # Save file to the uploads folder

            # Debug: Print file path for verification
            print(f"File saved at: {file_path}")

            # Read file into DataFrame for further processing
            df = pd.read_csv(file_path)
            df.to_csv('uploaded_dataset.csv', index=False)

            # Redirect to the same route but with the file path in the form data
            return redirect(url_for('index_with_data', file_path=file_path))
    
    return render_template('index_2.html')


@app.route('/dataviz.app/with_data', strict_slashes=False)
def index_with_data():
    file_path = request.args.get('file_path')
    df = pd.read_csv(file_path)

    return render_template(
        'index_2.html',
        df_html=df.head().to_html(classes='table table-striped'),
        fields=df.columns,
        file_path=file_path
    )


# Route to sanitize the data
@app.route('/dataviz.app/sanitize', strict_slashes=False, methods=['POST'])
def sanitize():
    file_path = request.form.get('file_path')  # Get the file path from the form
    df = pd.read_csv(file_path)
    df_cleaned = df.dropna()

    sanitized_path = file_path.replace('.csv', '_sanitized.csv')
    df_cleaned.to_csv(sanitized_path, index=False)

    return render_template(
        'index_2.html',
        df_html=df_cleaned.head().to_html(classes='table table-striped'),
        fields=df_cleaned.columns,
        message='Data sanitized!',
        file_path=sanitized_path
    )


# Route to display summary statistics
@app.route('/dataviz.app/summary', strict_slashes=False, methods=['POST'])
def summary():
    field = request.form.get('field')
    file_path = request.form.get('file_path')  # Get the file path from the form
    df = pd.read_csv(file_path)
    summary = df[field].describe()

    return render_template(
        'index_2.html',
        df_html=df.head().to_html(classes='table table-striped'),
        fields=df.columns,
        summary=summary.to_frame().to_html(classes='table table-striped'),
        file_path=file_path
    )


@app.route('/dataviz.app/visualize', strict_slashes=False, methods=['POST'])
def visualize():
    chart_type = request.form.get('chart_type')
    field = request.form.get('field')
    file_path = request.form.get('file_path')  # Get the file path from the form
    df = pd.read_csv(file_path)

    # Clear previous plots to avoid overlaps
    plt.clf()  # Clear the current figure before plotting

    img = io.BytesIO()

    # Set figure size for better layout management
    plt.figure(figsize=(12, 6))

    if chart_type == 'line' or chart_type == 'scatter':
        field1 = request.form.get('field1')
        field2 = request.form.get('field2')

        if pd.api.types.is_numeric_dtype(df[field1]) and pd.api.types.is_numeric_dtype(df[field2]):
            if chart_type == 'line':
                sns.lineplot(x=field1, y=field2, data=df)
            elif chart_type == 'scatter':
                sns.scatterplot(x=field1, y=field2, data=df)
        else:
            return render_template('index_2.html', df_html=df.head().to_html(classes='table table-striped'), fields=df.columns, message='Please select numeric fields for line chart or scatter plot.', file_path=file_path)

    elif chart_type == 'bar':
        field_y = request.form.get('field_y')

        # If the user selects the same field for both x and y, use the frequency of values for the y-axis
        if field == field_y:
            df_grouped = df[field].value_counts().reset_index()
            df_grouped.columns = [field, 'counts']
            ax = sns.barplot(x=field, y='counts', data=df_grouped, palette='Set2')
            plt.xticks(rotation=45, ha='right')
            plt.legend(title=field, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
        else:
            # If different fields are selected for x and y, plot the bar chart based on the numeric y-axis field
            if pd.api.types.is_numeric_dtype(df[field_y]):
                df_grouped = df.groupby(field)[field_y].sum().reset_index()  # Summing or aggregating the numeric values by group
                ax = sns.barplot(x=field, y=field_y, data=df_grouped, palette='Set2')

                for bar in ax.patches:
                    ax.annotate(format(bar.get_height(), '.2f'),
                                (bar.get_x() + bar.get_width() / 2., bar.get_height()),
                                ha='center', va='center', xytext=(0, 9),
                                textcoords='offset points')
                plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels to avoid overlap
            else:
                return render_template(
                    'index_2.html',
                    df_html=df.head().to_html(classes='table table-striped'),
                    fields=df.columns,
                    message='Please select a numeric field for Y-axis.',
                    file_path=file_path)

    elif chart_type == 'histogram':
        sns.histplot(df[field])

    elif chart_type == 'pie':
        pie_data = df[field].value_counts()
        pie_labels = pie_data.index
        pie_percentages = pie_data / pie_data.sum() * 100

        plt.figure(figsize=(10, 8))  # Adjust size for better appearance
        pie_data.plot.pie(labels=None, autopct=None, colors=sns.color_palette('Set2'), startangle=90)
        legend_labels = [f'{label}: {percentage:.1f}%' for label, percentage in zip(pie_labels, pie_percentages)]
        plt.legend(legend_labels, title=field, loc="center left", bbox_to_anchor=(1, 0.5), fontsize='small')
        plt.ylabel('')  # Remove default ylabel for cleaner plot

    plt.tight_layout()  # Automatically adjust layout to fit elements

    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template(
        'index_2.html',
        df_html=df.head().to_html(classes='table table-striped'),
        fields=df.columns,
        plot_url=plot_url,
        file_path=file_path
    )


# Route to reset visualization and summary
@app.route('/dataviz.app/reset', strict_slashes=False, methods=['POST'])
def reset():
    file_path = request.form.get('file_path')  # Get the file path from the form
    df = pd.read_csv(file_path)

    return render_template(
        'index_2.html',
        df_html=df.head().to_html(classes='table table-striped'),
        fields=df.columns,
        message='Reset successful!',
        file_path=file_path
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5008, debug=True)
