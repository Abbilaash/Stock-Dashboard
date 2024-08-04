# Stock-Dashboard

## Overview
This project is an interactive dashboard for stock market trends. It uses regression techniques for predicting stock prices. The website provides a user-friendly interface for viewing stock data, predictions, and additional features to enhance the user experience.

## Features
- **Responsive Design:** The website is fully responsive, ensuring a seamless experience on mobile, laptop, and desktop devices.
- **Stock Predictions:** Using LSTM for accurate stock price predictions.
- **Data Visualization:** Interactive charts and graphs for visualizing stock trends and predictions.
- **Additional Features:** Extra functionalities to provide a comprehensive stock market analysis experience.

## Technologies Used
- **Backend:** Flask
- **Frontend:** HTML, CSS, Bootstrap
- **Machine Learning:** LSTM Neural Networks
- **Data Visualization:** Plotly, Matplotlib
- **Web Scraping:** BeautifulSoup, Requests

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Abbilaash/Stock-Dashboard.git
    cd stock-market-prediction
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application:**
    ```bash
    flask run
    ```

## Usage
1. Open your web browser and go to `http://127.0.0.1:5000`.
2. Navigate through the various sections to view stock data, predictions, and additional features.

## Project Structure
- `app.py`: The main Flask application file.
- `func.py`: The main stock price prediction function.
- `templates/`: Contains HTML templates for rendering web pages.
- `static/`: Contains static files (CSS, JavaScript, images).
- `models/`: Contains the LSTM model and related scripts.
- `data/`: Contains scripts for data collection and processing.
- `requirements.txt`: List of Python packages required for the project.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes. Make sure to follow the coding guidelines and write appropriate tests.

## Acknowledgements
- Special thanks to the open-source community for providing the tools and libraries that made this project possible.

## Contact
For any questions or feedback, please contact Abbilaash at abbilaashat@gmail.com
