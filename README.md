# Bike Rental Demand Forecasting 🚴‍♂️

A web-based application that predicts bike rental demand based on weather conditions and environmental factors. Users can register, login, and get accurate predictions for bike rental demand using machine learning algorithms.

![Homepage Screenshot]()
<!-- Add homepage screenshot here -->

## 🌟 Features

### 🔐 User Authentication
- 📝 **User Registration**: Secure signup with encrypted password storage
- 🔑 **User Login**: Session-based authentication system
- 🔒 **Password Security**: Implemented using bcrypt hashing

### 📊 Bike Demand Prediction
- ⚡ **Real-time Predictions**: Enter weather parameters to get instant bike demand forecasts
- 🎯 **High Accuracy**: XGBoost model with 93% accuracy
- 🧾 **Input Parameters**:
  - Temperature (°C)
  - Humidity (%)
  - Wind Speed (m/s)
  - Rainfall (mm)
  - Season selection
  - And more environmental factors

![Prediction Form Screenshot]()
<!-- Add prediction form screenshot here -->

### 📈 Prediction History
- 📋 **Table View**: Comprehensive history of all predictions made
- 📉 **Graphical Analysis**: Interactive charts and graphs for data visualization
- 👤 **User-specific Data**: Each user can view their own prediction history

![Prediction History Screenshot]()
<!-- Add prediction history table screenshot here -->

![Prediction Graph Screenshot]()
<!-- Add prediction graph screenshot here -->

### 🌤️ Weather Integration
- ⛅ **Real-time Weather Data**: Get current weather information for any location
- 🔗 **API Integration**: Fetch live weather data without leaving the application
- 🧠 **Convenient Input**: Auto-populate prediction form with current weather conditions

![Weather Page Screenshot]()
<!-- Add weather page screenshot here -->

## 🛠️ Technology Stack

### 💻 Frontend
- **HTML5**: Structure and semantic markup
- **CSS3**: Styling and responsive design
- **JavaScript**: Interactive functionality and API calls

### 🧠 Backend
- **Python**: Core programming language
- **Flask**: Web framework with SQLAlchemy ORM
- **XGBoost**: Machine learning model for bike demand predictions
- **Pandas & NumPy**: Data processing and manipulation
- **Scikit-learn**: Data preprocessing (StandardScaler)

### 🗄️ Database
- **SQLite**: Lightweight database for user data and prediction history
- **Flask-SQLAlchemy**: ORM for database operations
- **Flask-Login**: Session management and user authentication

### 🛡️ Security & Authentication
- **Flask-Bcrypt**: Password hashing and encryption
- **Flask-Login**: User session management and login handling
- **Session-based Authentication**: Secure user login system

### 🌍 APIs & External Services
- **OpenWeatherMap API**: Real-time weather data integration

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Git
- OpenWeatherMap API Key (free registration at openweathermap.org)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/bike-rental-demand-forecasting.git
cd bike-rental-demand-forecasting
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install flask flask-sqlalchemy flask-bcrypt flask-login
pip install pandas numpy scikit-learn xgboost
pip install requests pickle
```

### Step 4: Setup Required Files
Make sure you have the following model files in your `models/` directory:
- `xgboost_regressor_r2_0_928_v1.pkl` - Trained XGBoost model
- `sc.pkl` - StandardScaler for data preprocessing

### Step 5: Environment Configuration
Update the `API_KEY` in `app.py` with your OpenWeatherMap API key:
```python
API_KEY = "your-openweathermap-api-key-here"
```

Update the database path in `app.py` if needed:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
```

### Step 6: Initialize Database
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### Step 7: Run the Application
```bash
python app.py
```

## 🎯 Model Performance

- **Algorithm**: XGBoost Regressor
- **Model File**: `xgboost_regressor_r2_0_928_v1.pkl`
- **R² Score**: 0.928 (92.8% accuracy)
- **Data Preprocessing**: StandardScaler for feature normalization
- **Features Used**: 22 features including temporal, weather, and categorical variables
- **Training Data**: Seoul Bike Sharing dataset from Kaggle
- **Date Processing**: Automatic extraction of day, month, year, and weekday
- **Categorical Encoding**: One-hot encoding for seasons and days of week


![Model Performance Screenshot]()
<!-- Add model performance metrics screenshot here -->


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- **Kaggle** for providing the Seoul Bike Sharing Demand dataset
- **XGBoost** team for the excellent machine learning library
- **Flask** community for the robust web framework
- **OpenWeatherMap** for providing free weather API access
- **Scikit-learn** for data preprocessing tools

## 👨‍💻 Author

**Harsh Gajera**
- GitHub: [@harshgajera101](https://github.com/harshgajera101)
- LinkedIn: [Harsh Gajera](https://linkedin.com/in/gajera-harsh)

