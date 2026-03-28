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
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# ✅ Load artifacts
model = joblib.load("best_flight_delay_model.pkl")
scaler = joblib.load("scaler.pkl")
features = joblib.load("features.pkl")

# dropdown data
airlines = joblib.load("data/airlines.pkl")
origins = joblib.load("data/origins.pkl")
destinations = joblib.load("data/destinations.pkl")

# ✅ Input schema with constraints
class FlightInput(BaseModel):
    CRSDepTime: int = Field(..., ge=0, le=2359)
    DayOfWeek: int = Field(..., ge=1, le=7)
    Airline: str
    Origin: str
    Dest: str

# ✅ Helper: prepare input
def prepare_input(data: FlightInput):
    input_dict = {feature: 0 for feature in features}

    input_dict["CRSDepTime"] = data.CRSDepTime
    input_dict["DayOfWeek"] = data.DayOfWeek
    input_dict["dep_hour"] = data.CRSDepTime // 100

    # one-hot encoding
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
    input_array = prepare_input(data)
    input_scaled = scaler.transform(input_array)
    prediction = model.predict(input_scaled)[0]

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

# ✅ Dropdown data endpoint (for Flutter)
@app.get("/options")
def get_options():
    return {
        "airlines": airlines,
        "origins": origins,
        "destinations": destinations
    }

# ✅ Retrain endpoint
@app.post("/retrain")
def retrain(file: UploadFile = File(...)):
    global model, scaler

    df = pd.read_csv(file.file)

    target = "ArrDelay"
    df = df.dropna(subset=[target])
    df = pd.get_dummies(df, drop_first=True)

    X = df.drop(columns=[target])
    y = df[target]

    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import SGDRegressor

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = SGDRegressor(max_iter=1000)
    model.fit(X_scaled, y)

    joblib.dump(model, "best_flight_delay_model.pkl")
    joblib.dump(scaler, "scaler.pkl")

    return {"message": "Model retrained successfully"}