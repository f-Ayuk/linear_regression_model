from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, Field
import numpy as np
import joblib
import pandas as pd
import os

from fastapi.middleware.cors import CORSMiddleware
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDRegressor

app = FastAPI(title="Flight Delay Prediction API")

# ✅ CORS (allow all for Flutter + Render)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # IMPORTANT FIX
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Debug helper
def safe_load(path, default):
    try:
        if os.path.exists(path):
            return joblib.load(path)
        else:
            print(f"File not found: {path}")
            return default
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return default

# ✅ Load model artifacts safely
model = safe_load("best_flight_delay_model.pkl", None)
scaler = safe_load("scaler.pkl", None)
features = safe_load("features.pkl", [])

# ✅ Load dropdown data safely
airlines = safe_load("data/airlines.pkl", ["AA", "DL", "UA"])
origins = safe_load("data/origins.pkl", ["JFK", "LAX"])
destinations = safe_load("data/destinations.pkl", ["ORD", "ATL"])

# ✅ Root endpoint (for testing API health)
@app.get("/")
def home():
    return {"message": "API is running successfully"}

# ✅ Input schema
class FlightInput(BaseModel):
    CRSDepTime: int = Field(..., ge=0, le=2359)
    DayOfWeek: int = Field(..., ge=1, le=7)
    Airline: str
    Origin: str
    Dest: str

# ✅ Prepare input
def prepare_input(data: FlightInput):
    if not features:
        raise ValueError("Feature list is empty. Model not loaded properly.")

    input_dict = {feature: 0 for feature in features}

    input_dict["CRSDepTime"] = data.CRSDepTime
    input_dict["DayOfWeek"] = data.DayOfWeek
    input_dict["dep_hour"] = data.CRSDepTime // 100

    # One-hot encoding
    if f"Airline_{data.Airline}" in input_dict:
        input_dict[f"Airline_{data.Airline}"] = 1

    if f"Origin_{data.Origin}" in input_dict:
        input_dict[f"Origin_{data.Origin}"] = 1

    if f"Dest_{data.Dest}" in input_dict:
        input_dict[f"Dest_{data.Dest}"] = 1

    return np.array(list(input_dict.values())).reshape(1, -1)

# ✅ Prediction endpoint
@app.post("/predict")
def predict(data: FlightInput):
    try:
        print("Incoming data:", data)

        if model is None or scaler is None:
            return {"error": "Model or scaler not loaded"}

        input_array = prepare_input(data)
        input_scaled = scaler.transform(input_array)
        prediction = model.predict(input_scaled)[0]

        # Status logic
        if prediction < 0:
            status = "Early"
        elif prediction < 15:
            status = "On Time"
        else:
            status = "Delayed"

        print("Prediction:", prediction)

        return {
            "delay_minutes": round(float(prediction), 2),
            "status": status
        }

    except Exception as e:
        print("Prediction error:", e)
        return {"error": str(e)}

# ✅ OPTIONS endpoint (for Flutter dropdowns)
@app.get("/options")
def get_options():
    try:
        print("Sending dropdown data")
        print("Airlines:", airlines)
        print("Origins:", origins)
        print("Destinations:", destinations)

        return {
            "airlines": airlines,
            "origins": origins,
            "destinations": destinations
        }
    except Exception as e:
        print(f"Error in /options endpoint: {e}")
        return {"error": "Failed to load options"}

# ✅ Retrain endpoint
@app.post("/retrain")
def retrain(file: UploadFile = File(...)):
    global model, scaler, features

    try:
        df = pd.read_csv(file.file)

        target = "ArrDelay"
        df = df.dropna(subset=[target])

        # One-hot encode
        df = pd.get_dummies(df, drop_first=True)

        X = df.drop(columns=[target])
        y = df[target]

        # Save new feature list
        features = list(X.columns)

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        model = SGDRegressor(max_iter=1000)
        model.fit(X_scaled, y)

        # Save updated artifacts
        joblib.dump(model, "best_flight_delay_model.pkl")
        joblib.dump(scaler, "scaler.pkl")
        joblib.dump(features, "features.pkl")

        return {"message": "Model retrained successfully"}

    except Exception as e:
        print("Retrain error:", e)
        return {"error": str(e)}