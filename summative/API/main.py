from fastapi import FastAPI
from pydantic import BaseModel, Field
import numpy as np
import joblib

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Flight Delay API")

# ✅ CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load model files
model = joblib.load("best_flight_delay_model.pkl")
scaler = joblib.load("scaler.pkl")
features = joblib.load("features.pkl")

# ✅ Input schema (ONLY 5 FEATURES)
class FlightInput(BaseModel):
    CRSDepTime: int = Field(..., ge=0, le=2359)
    DayOfWeek: int = Field(..., ge=1, le=7)
    Airline: str
    Origin: str
    Dest: str

# ✅ Convert user input → model format
def prepare_input(data: FlightInput):
    input_dict = {feature: 0 for feature in features}

    # Core features
    input_dict["CRSDepTime"] = data.CRSDepTime
    input_dict["DayOfWeek"] = data.DayOfWeek

    # Derived feature
    input_dict["dep_hour"] = data.CRSDepTime // 100

    # One-hot encoding
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

# ✅ Prediction endpoint
@app.post("/predict")
def predict(data: FlightInput):
    try:
        input_array = prepare_input(data)
        input_scaled = scaler.transform(input_array)
        prediction = model.predict(input_scaled)[0]

        # Optional interpretation
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

# ✅ Retrain endpoint (simple placeholder)
@app.post("/retrain")
def retrain():
    return {"message": "Retraining endpoint ready (connect to training script)"}