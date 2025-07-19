from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pickle
import os
from datetime import datetime
import pandas as pd
import numpy as np
from extensions import db, bcrypt, login_manager  
from models import User, Prediction

# weather
import requests
from flask import Flask, jsonify

#Enter API key here for Weather api Intergration
API_KEY = ""          
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"



app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Admin/OneDrive/Desktop/Project/instance/site.db'

db.init_app(app) 
bcrypt.init_app(app) 
login_manager.init_app(app)  

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes here (signup, login, etc.)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists!", "danger")
            return redirect(url_for('signup'))

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials!", "danger")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/how-it-works')
def how_it_works():
    return render_template('how-it-works.html')

class Inference:
    def __init__(self, model_path, sc_path):
        self.model_path = model_path
        self.sc_path = sc_path

        if os.path.exists(self.model_path) and os.path.exists(self.sc_path):
            self.model = pickle.load(open(self.model_path, "rb"))
            self.sc = pickle.load(open(self.sc_path, "rb"))
        else:
            print("Model or Standard Scaler path is not correct!")

    def get_string_to_datetime(self, date):
        try:
            dt = datetime.strptime(date, "%d/%m/%Y")
            return {"day": dt.day, "month": dt.month, "year": dt.year, "week_day": dt.strftime("%A")}
        except ValueError:
            raise ValueError("Incorrect date format. Please use dd/mm/yyyy.")

    def seasons_to_df(self, seasons):
        seasons_cols = ["Spring", "Summer", "Winter"]
        seasons_data = np.zeros((1, len(seasons_cols)), dtype="int")
        df_seasons = pd.DataFrame(seasons_data, columns=seasons_cols)
        if seasons in seasons_cols:
            df_seasons[seasons] = 1
        return df_seasons

    def days_df(self, week_day):
        days_names = ['Monday', 'Saturday', 'Sunday', 'Thursday', 'Tuesday', 'Wednesday']
        days_name_data = np.zeros((1, len(days_names)), dtype="int")
        df_days = pd.DataFrame(days_name_data, columns=days_names)
        if week_day in days_names:
            df_days[week_day] = 1
        return df_days

    def users_input(self, form_data):
        # Get input from form data
        date = form_data['date']
        hour = int(form_data['hour'])
        temperature = float(form_data['temperature'])
        humidity = float(form_data['humidity'])
        wind_speed = float(form_data['wind_speed'])
        visibility = float(form_data['visibility'])
        solar_radiation = float(form_data['solar_radiation'])
        rainfall = float(form_data['rainfall'])
        snowfall = float(form_data['snowfall'])
        seasons = form_data['seasons']
        holiday = form_data['holiday']
        functioning_day = form_data['functioning_day']

        str_to_date = self.get_string_to_datetime(date)

        holiday_dict = {"No Holiday": 0, "Holiday": 1}
        functioning_day_dict = {"No": 0, "Yes": 1}

        holiday = holiday_dict.get(holiday, 0)
        functioning_day = functioning_day_dict.get(functioning_day, 0)

        u_input_list = [hour, temperature, humidity, wind_speed, visibility, solar_radiation, rainfall, snowfall, holiday, functioning_day, str_to_date["day"], str_to_date["month"], str_to_date["year"]]

        features_name = ["Hour", 'Temperature (°C)', 'Humidity (%)', 'Wind speed (m/s)', 'Visibility (10m)', 'Solar Radiation (M3/m2)', 'Rainfall(mm)', 'Snowfall (cm)', 'Holiday', 'Functioning Day', 'Day', 'Month', 'Year']

        df_u_input = pd.DataFrame([u_input_list], columns=features_name)
        df_season = self.seasons_to_df(seasons)
        df_days = self.days_df(str_to_date["week_day"])

        df_for_pred = pd.concat([df_u_input, df_season, df_days], axis=1)
        return df_for_pred

    def prediction(self, form_data):
        df = self.users_input(form_data)

        df.rename(columns={
            'Humidity (%)': 'Humidity(%)',
            'Solar Radiation (M3/m2)': 'Solar Radiation (MJ/m2)',
            'Temperature (°C)': 'Temperature(°C)'
        }, inplace=True)

        df = df[['Hour', 'Temperature(°C)', 'Humidity(%)', 'Wind speed (m/s)', 'Visibility (10m)', 
                 'Solar Radiation (MJ/m2)', 'Rainfall(mm)', 'Snowfall (cm)', 'Holiday', 'Functioning Day', 
                 'Day', 'Month', 'Year', 'Spring', 'Summer', 'Winter', 'Monday', 'Saturday', 'Sunday', 
                 'Thursday', 'Tuesday', 'Wednesday']]

        scaled_data = self.sc.transform(df)
        prediction = self.model.predict(scaled_data)
        return prediction


@app.route('/predict', methods=['POST'])
@login_required
def predict():
    form_data = request.form.to_dict()

    try:
        prediction = inference.prediction(form_data)

        new_prediction = Prediction(
            user_id=current_user.id,
            date=form_data['date'],
            hour=int(form_data['hour']),
            temperature=float(form_data['temperature']),
            humidity=float(form_data['humidity']),
            wind_speed=float(form_data['wind_speed']),
            visibility=float(form_data['visibility']),
            solar_radiation=float(form_data['solar_radiation']),
            rainfall=float(form_data['rainfall']),
            snowfall=float(form_data['snowfall']),
            seasons=form_data['seasons'],
            holiday=form_data['holiday'],
            functioning_day=form_data['functioning_day'],
            prediction=round(prediction[0])
        )
        db.session.add(new_prediction)
        db.session.commit()

        return jsonify({'prediction': round(prediction[0]), 'message': 'Prediction successfully saved!'})

    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/prediction-history')
@login_required
def prediction_history():
    predictions = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.date, Prediction.hour).all()

    # Extract hours and processed prediction values
    hours = [p.hour for p in predictions]
    values = [round(abs(p.prediction), 2) for p in predictions]  # For JSON or chart use

    # Also update the prediction values for the table
    for p in predictions:
        p.prediction = round(abs(p.prediction), 2)

    return render_template('prediction_history.html', predictions=predictions, hours=hours, values=values)


# weather
@app.route('/weather')
def weather_page():
    return render_template('weather.html')

@app.route('/get_weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City name is required"}), 400

    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_info = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"],
            "city": city.capitalize()
        }
        return jsonify(weather_info)
    else:
        return jsonify({"error": "City not found"}), 404


if __name__ == '__main__':
    ml_model_path = r"C:\Users\Admin\OneDrive\Desktop\Project\models\xgboost_regressor_r2_0_928_v1.pkl"
    standard_scaler_path = r"C:\Users\Admin\OneDrive\Desktop\Project\models\sc.pkl"
    inference = Inference(ml_model_path, standard_scaler_path)

    app.run(debug=True)

