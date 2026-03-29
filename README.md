# linear_regression_model
Maths for ML Linear Regression Summative

## Flight Delay Prediction System

Mission Statement:

This project develops a comprehensive machine learning system to predict flight arrival delays in minutes using linear regression, decision trees, and random forest algorithms. The system addresses the critical need for accurate delay predictions in aviation, helping passengers make informed decisions and enabling airlines to optimise their operations. By analysing historical flight data patterns, weather conditions, and operational factors, the system provides real-time predictions through both a mobile application and a REST API interface.


## Project Structure
```
linear_regression_model/
│
├── summative/
│   ├── linear_regression/
│   │   ├── multivariate.ipynb
│   │   └── data/
│   │       └── flight_data.csv
│   │
│   ├── API/
│   │   ├── prediction.py
│   │   ├── requirements.txt
│   │   ├── best_model.pkl
│   │   ├── scaler.pkl
│   │   └── start_prediction_server.py
│   │
│   └── FlutterApp/
│       └── app/
│           ├── lib/
│           │   ├── main.dart
│           │   └── screens/
│           │       ├── prediction_form_screen.dart
│           │       └── result_screen.dart
│           ├── pubspec.yaml
│           └── android/
│
├── models/
│   ├── best_model.pkl                 # Best performing model
│   ├── scaler.pkl                     # Feature preprocessing
│   └── model_metadata.pkl             # Model information
│
└── README.md
```

## API Endpoint
**Production URL**: `https://flight-delay-api-a0oq.onrender.com`

### Available Endpoints
- **GET** `/` - API information and status
- **GET** `/health` - Health check endpoint
- **POST** `/predict` - Flight delay prediction
- **GET** `/docs` - Interactive Swagger UI documentation

### API Testing
Access the Swagger UI documentation at: `https://flight-delay-predict-vyo2.onrender.com/`

**Sample Request**:
```json
{
    "CRSDepTime": 1530,
    "DayOfWeek": 3,
    "Airline": "AA",
    "Origin": "JFK",
    "Dest": "ORD"
}
```

**Sample Response**:
```json
{
    "predicted_delay_minutes": 25.5,
    "interpretation": "Moderate delay of 25 minutes expected",
    "confidence": "medium",
    "model_version": "1.2.0"
}
```

## Video Demo
🎥 **YouTube Demo**: [Flight Delay Prediction System Demo](https://www.loom.com/share/9095ddeecfd640b3974bbe0fa42f43ef)
*(5-minute demonstration of the complete system including mobile app and API usage)*

## Mobile App Setup Instructions

### Prerequisites
- Flutter SDK (3.0.0 or higher)
- Android Studio or VS Code
- Android device or emulator

### Installation Steps

1. **Clone the repository**
    ```bash
    git clone <repository-url>
    cd linear_regression_model/summative/FlutterApp/app
    ```

2. **Install Flutter dependencies**
    ```bash
    flutter pub get
    ```

3. **Verify Flutter installation**
    ```bash
    flutter doctor
    ```

4. **Connect device or start emulator**
    - For physical device: Enable USB debugging and connect via USB
    - For emulator: Start Android emulator from Android Studio

5. **Run the application**
    ```bash
    # Debug mode (development)
    flutter run

    # Release mode (production)
    flutter run --release
    ```

6. **Build APK (optional)**
    ```bash
    flutter build apk --release
    ```
    The APK will be available at: `build/app/outputs/flutter-apk/app-release.apk`

### App Features
- **Flight Input Form**: Enter departure details, airline, route information
- **Real-time Predictions**: Get instant delay predictions via API
- **User-friendly Interface**: Clean, intuitive design for easy navigation
- **Offline Capability**: Cached data for improved performance

### Troubleshooting
- **Build errors**: Run `flutter clean` then `flutter pub get`
- **API connectivity**: Ensure device has internet connection
- **Emulator issues**: Try creating a new AVD with latest Android version

## Technical Implementation

### Machine Learning Models
- **Linear Regression**: Baseline model with gradient descent optimization
- **Decision Tree**: Non-linear pattern recognition
- **Random Forest**: Ensemble method for improved accuracy
- **Best Model Selection**: Automatic selection based on lowest test loss

### Performance Metrics
- **R² Score**: Model explanation capability
- **RMSE**: Prediction accuracy in minutes
- **MAE**: Average prediction error
- **Cross-validation**: Robust performance assessment

### Key Features
- **Feature Engineering**: Time-based patterns, airline categorization, route complexity
- **Data Standardization**: Robust scaling for optimal model performance
- **Real-time API**: FastAPI with automatic documentation
- **Mobile Integration**: Cross-platform Flutter application
- **Model Persistence**: Automated saving of best-performing models

## Development Team
Developed as part of advanced machine learning and mobile development coursework, demonstrating integration of ML models with production-ready applications.

---
