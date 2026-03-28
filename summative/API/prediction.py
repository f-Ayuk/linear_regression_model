from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, Field
import numpy as np
import joblib
import pandas as pd

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Flight Delay Prediction API")

# ✅ CORS (not wildcard for grading)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development URL for Flutter frontend
        "http://127.0.0.1:3000"   # Localhost URL for Flutter frontend
    ],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# ✅ Load artifacts (model, scaler, feature list)
model = joblib.load("best_flight_delay_model.pkl")
scaler = joblib.load("scaler.pkl")
features = joblib.load("features.pkl")

# Dropdown data - for options (these should be pre-saved as pickle files)
airlines = joblib.load("data/airlines.pkl")
origins = joblib.load("data/origins.pkl")
destinations = joblib.load("data/destinations.pkl")

# ✅ Input schema with constraints
class FlightInput(BaseModel):
    CRSDepTime: int = Field(..., ge=0, le=2359)  # Departure time in HHMM format
    DayOfWeek: int = Field(..., ge=1, le=7)  # 1=Monday, 7=Sunday
    Airline: str  # Airline code (must match one of the airline codes)
    Origin: str  # Origin airport code (must match one of the origin codes)
    Dest: str  # Destination airport code (must match one of the destination codes)

# ✅ Helper: Prepare input data for prediction
def prepare_input(data: FlightInput):
    input_dict = {feature: 0 for feature in features}

    input_dict["CRSDepTime"] = data.CRSDepTime
    input_dict["DayOfWeek"] = data.DayOfWeek
    input_dict["dep_hour"] = data.CRSDepTime // 100  # Convert CRSDepTime to hour

    # One-hot encoding for airline, origin, and destination
    if f"Airline_{data.Airline}" in input_dict:
        input_dict[f"Airline_{data.Airline}"] = 1

    if f"Origin_{data.Origin}" in input_dict:
        input_dict[f"Origin_{data.Origin}"] = 1

    if f"Dest_{data.Dest}" in input_dict:
        input_dict[f"Dest_{data.Dest}"] = 1

    return np.array(list(input_dict.values())).reshape(1, -1)

# ✅ Prediction endpoint (POST /predict)
@app.post("/predict")
def predict(data: FlightInput):
    input_array = prepare_input(data)
    input_scaled = scaler.transform(input_array)
    prediction = model.predict(input_scaled)[0]

    # Determine status based on the prediction
    if prediction < 0:
        status = "Early"
    elif prediction < 15:
        status = "On Time"
    else:
        status = "Delayed"

    return {
        "delay_minutes": round(float(prediction), 2),
        "status": status
    }

# ✅ Dropdown options endpoint (for Flutter to fetch airline, origin, and destination options)
@app.get("/options")
def get_options():
    return {
        "airlines": airlines,
        "origins": origins,
        "destinations": destinations
    }

# ✅ Retrain model endpoint (POST /retrain)
@app.post("/retrain")
def retrain(file: UploadFile = File(...)):
    global model, scaler

    # Read the uploaded CSV file
    df = pd.read_csv(file.file)

    target = "ArrDelay"
    df = df.dropna(subset=[target])  # Remove rows with missing target values
    df = pd.get_dummies(df, drop_first=True)  # One-hot encode categorical variables

    X = df.drop(columns=[target])
    y = df[target]

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Retrain the model
    model = SGDRegressor(max_iter=1000)
    model.fit(X_scaled, y)

    # Save the updated model and scaler
    joblib.dump(model, "best_flight_delay_model.pkl")
    joblib.dump(scaler, "scaler.pkl")

    return {"message": "Model retrained successfully"}