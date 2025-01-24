# DataViz App
DataViz is a Flask-based web application that allows users to upload CSV files, sanitize data, calculate descriptive statistics based on selected fields, and visualize the data using various types of charts. The app provides a user-friendly interface to analyze and understand datasets through graphical representations.

## Deployed Site
You can access the deployed DataViz app here: [DataViz Web App](http://web-02.consultgenius.tech/dataviz/)
![image](https://github.com/user-attachments/assets/96bb1b82-dc3a-494e-8116-bb1f754b1887)


## Blog Post
Read the detailed journey of how DataViz was created: [DataViz Blog Post](https://medium.com/@mwanzaalbert/dataviz-a-python-powered-data-visualization-web-app-5b955600e093)

## Author's LinkedIn
Connect with me on [LinkedIn](https://www.linkedin.com/in/mwanzaalbert/)

## Features

- File Upload: Upload CSV files for analysis.
- Data Sanitization: Clean the dataset by removing missing values.
- Summary Statistics: Calculate descriptive statistics (e.g., mean, median, min, max) for selected fields in the dataset.
- Data Visualization: Visualize the data using various charts based on the selected field:
    - Bar Chart
    - Line Chart
    - Histogram
    - Pie Chart
    - Scatter Plot
- Reset Functionality: Reset the visualizations and summary calculations.

## Installation
Clone the repository:

bash

```
git clone https://github.com/your-username/DataViz.git

cd DataViz
```
Create a virtual environment and activate it:

bash

```
python3 -m venv venv
source venv/bin/activate
```
Install the required dependencies:

bash

```
pip install -r requirements.txt
```
Run the app:

bash

```
python app.py
```
Open your browser and navigate to http://127.0.0.1:5000/ to use the app.

Usage
Upload a CSV File:

On the homepage, click the "Choose File" button to upload a CSV file, then click "Upload."
Sanitize Data:

After uploading the dataset, click the "Sanitize Data" button to remove rows with missing values from the dataset.
Summary Statistics:

Select a field from the dropdown and click "Show Summary" to view descriptive statistics for the selected field.
Visualize Data:

Select a field and choose a chart type (Bar, Line, Histogram, Pie, or Scatter) to generate a visualization.
Reset:

Click the "Reset" button to clear the visualizations and summaries, returning the app to its default state.

## Folder Structure
bash

```
/DataViz
  /static
    - styles.css          # CSS for basic styling
  /templates
    - index.html          # HTML template for the main page
  app.py                  # Main Flask application
  requirements.txt        # List of required Python packages
```

## Dependencies
The following Python packages are required to run the DataViz app:

- Flask: Web framework for Python
- pandas: Library for data manipulation and analysis
- matplotlib: Plotting library for generating visualizations
- seaborn: Statistical data visualization library

You can install all dependencies using the requirements.txt file provided:

bash
```
pip install -r requirements.txt
```

## Screenshots

- [File Upload and Data Display](https://github.com/mwanzaalbert/DataViz/blob/main/screenshots/upload_and_data_display.jpg)

- [Summary Statistics](https://github.com/mwanzaalbert/DataViz/blob/main/screenshots/summary_statistics.jpg)

- [Data Visualization](https://github.com/mwanzaalbert/DataViz/blob/main/screenshots/visualization.jpg)

## Challenges
- Some challenges faced while building this application include:
- Handling large datasets efficiently.
- Providing a clean user interface for easy navigation and data analysis.
- Ensuring the flexibility of visualizations across various data types.


## Future Improvements

- Data Transformations: Add functionality to perform data transformations (e.g., normalization, scaling).
- More Visualizations: Implement additional chart types like boxplots, heatmaps, and more.
- Advanced Filtering: Add filters for more in-depth data analysis, such as sorting and grouping.
- Error Handling: Improve error handling for edge cases like empty fields or improper CSV formats.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
