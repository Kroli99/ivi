# Used Car Interactive Dashboard

## Project Overview
This project is an interactive dashboard for exploring used car data. It allows users to filter and analyze used car sales data based on various attributes such as brand, price, and mileage. The dashboard is built using Dash by Plotly and incorporates elements like interactive graphs and user inputs to provide a dynamic and insightful user experience.

## Features
- **Brand Selection**: Users can select one or multiple car brands to view specific data.
- **Price Filtering**: Interactive sliders allow users to filter cars based on price ranges.
- **Data Visualization**: Multiple charts display various aspects of the data, such as price distribution and mileage, which update dynamically based on user interactions.
- **Responsive Design**: The dashboard is responsive and can be used on various devices, ensuring a wide accessibility.

## Technologies Used
- **Dash**: A Python framework for building analytical web applications.
- **Plotly**: For creating interactive plots.
- **Pandas**: For data manipulation and analysis.
- **Requests**: To handle HTTP requests (if data is fetched dynamically).

## Installation
To run this project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/used-car-dashboard.git
   cd used-car-dashboard

2.	**Set up a Python virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3.	**Install required packages:**
    ```bash
    pip install -r requirements.txt

4.	**Run the application:**
    ```bash
    python app.py

## Usage

After starting the app, navigate to http://127.0.0.1:8050/ in your web browser to view the dashboard. Use the interactive elements like dropdowns and sliders to filter the data and explore different aspects of the used car market.