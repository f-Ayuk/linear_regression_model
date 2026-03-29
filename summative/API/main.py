from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import numpy as np
import joblib

app = FastAPI(title="Flight Delay API")

# ✅ CORS Middleware
try:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
except Exception as e:
    print(f"Warning: CORS middleware setup failed: {e}")

# ✅ Load model files
try:
    model = joblib.load("best_flight_delay_model.pkl")
    scaler = joblib.load("scaler.pkl")
    features = joblib.load("features.pkl")
    print("Model, scaler, and features loaded successfully.")
except Exception as e:
    print(f"Error loading model files: {e}")

# ✅ Input schema (ONLY 5 FEATURES)
class FlightInput(BaseModel):
    CRSDepTime: int = Field(..., ge=0, le=2359)  # Departure time (HHMM)
    DayOfWeek: int = Field(..., ge=1, le=7)  # Day of the week (1-7)
    Airline: str  # Airline code
    Origin: str  # Origin airport code
    Dest: str  # Destination airport code

# ✅ Helper function to prepare input data for prediction
def prepare_input(data: FlightInput):
    input_dict = {feature: 0 for feature in features}

    input_dict["CRSDepTime"] = data.CRSDepTime
    input_dict["DayOfWeek"] = data.DayOfWeek
    input_dict["dep_hour"] = data.CRSDepTime // 100  # Extract hour from CRSDepTime

    # One-hot encoding for categorical variables
    airline_col = f"Airline_{data.Airline}"
    origin_col = f"Origin_{data.Origin}"
    dest_col = f"Dest_{data.Dest}"

    if airline_col in input_dict:
        input_dict[airline_col] = 1

    if origin_col in input_dict:
        input_dict[origin_col] = 1

    if dest_col in input_dict:
        input_dict[dest_col] = 1

    return np.array(list(input_dict.values())).reshape(1, -1)

# ✅ Prediction endpoint (POST /predict)
@app.post("/predict")
def predict(data: FlightInput):
    try:
        input_array = prepare_input(data)
        input_scaled = scaler.transform(input_array)
        prediction = model.predict(input_scaled)[0]

        # Optional interpretation based on prediction
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
    except Exception as e:
        return {"error": str(e)}

# ✅ Retrain endpoint (just as a placeholder for now)
@app.post("/retrain")
def retrain():
    return {"message": "Retraining endpoint ready (connect to training script)"}