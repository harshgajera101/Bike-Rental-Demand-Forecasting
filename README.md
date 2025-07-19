# Bike-Rental-Demand-Forecasting
This machine learning web app predicts daily bike rental demand using the Seoul Bike Sharing dataset. After training multiple models, XGBoost was selected for its high accuracy. The app, built with Flask, includes user login, real-time weather via API, and MySQL-based prediction tracking with visualizations.


Follow these steps to run the project:

1. Open and run the e-bike.ipynb notebook step-by-step to train and save the bike demand forecasting model.

2. Next, run the inference.ipynb notebook to test the model and verify its prediction performance.

3. In the terminal, navigate to the project directory and execute the following commands:
python create_table.py (to create necessary database tables)
python my_inspect.py (to inspect or initialize database structure)

4. Finally, start the Flask web app by running python app.py and open the local server address shown in the terminal (e.g., http://127.0.0.1:5000/) in your browser.
