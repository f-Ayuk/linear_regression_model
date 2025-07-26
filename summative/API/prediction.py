# prediction.py

from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd

# Load model and scaler
model = joblib.load("best_model.pkl")
scaler = joblib.load("scaler.pkl")

app = FastAPI()

# Allow CORS (for Flutter app access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model with data types and range constraints
class FlightInput(BaseModel):
    ScheduledHour: int = Field(..., ge=0, le=23)
    ActualHour: int = Field(..., ge=0, le=23)
    DepartureDelta: float

    # African Airlines (optional, defaults to 0)
    Airline_Airlink: int = Field(0, ge=0, le=1)
    Airline_EgyptAir: int = Field(0, ge=0, le=1)
    Airline_Ethiopian_Airlines: int = Field(0, ge=0, le=1, alias="Airline_Ethiopian Airlines")
    Airline_FlySafair: int = Field(0, ge=0, le=1)
    Airline_Kenya_Airways: int = Field(0, ge=0, le=1, alias="Airline_Kenya Airways")
    Airline_Royal_Air_Maroc: int = Field(0, ge=0, le=1, alias="Airline_Royal Air Maroc")
    Airline_RwandAir: int = Field(0, ge=0, le=1)
    Airline_South_African_Airways: int = Field(0, ge=0, le=1, alias="Airline_South African Airways")
    Airline_Tunisair: int = Field(0, ge=0, le=1)

    # Origin airports (optional, defaults to 0)
    Origin_CAI: int = Field(0, ge=0, le=1)  # Cairo
    Origin_CMN: int = Field(0, ge=0, le=1)  # Casablanca
    Origin_CPT: int = Field(0, ge=0, le=1)  # Cape Town
    Origin_DSS: int = Field(0, ge=0, le=1)  # Dakar
    Origin_JNB: int = Field(0, ge=0, le=1)  # Johannesburg
    Origin_KGL: int = Field(0, ge=0, le=1)  # Kigali
    Origin_LOS: int = Field(0, ge=0, le=1)  # Lagos
    Origin_NBO: int = Field(0, ge=0, le=1)  # Nairobi
    Origin_TUN: int = Field(0, ge=0, le=1)  # Tunis

    # Destination airports (optional, defaults to 0)
    Destination_CAI: int = Field(0, ge=0, le=1)  # Cairo
    Destination_CMN: int = Field(0, ge=0, le=1)  # Casablanca
    Destination_CPT: int = Field(0, ge=0, le=1)  # Cape Town
    Destination_DSS: int = Field(0, ge=0, le=1)  # Dakar
    Destination_JNB: int = Field(0, ge=0, le=1)  # Johannesburg
    Destination_KGL: int = Field(0, ge=0, le=1)  # Kigali
    Destination_LOS: int = Field(0, ge=0, le=1)  # Lagos
    Destination_NBO: int = Field(0, ge=0, le=1)  # Nairobi
    Destination_TUN: int = Field(0, ge=0, le=1)  # Tunis

    class Config:
        validate_by_name = True

# Feature columns (must match model input order)
FEATURE_COLUMNS = [
    'ScheduledHour', 'ActualHour', 'DepartureDelta',
    'Airline_Airlink', 'Airline_EgyptAir', 'Airline_Ethiopian Airlines', 'Airline_FlySafair', 
    'Airline_Kenya Airways', 'Airline_Royal Air Maroc', 'Airline_RwandAir', 
    'Airline_South African Airways', 'Airline_Tunisair',
    'Origin_CAI', 'Origin_CMN', 'Origin_CPT', 'Origin_DSS', 'Origin_JNB', 
    'Origin_KGL', 'Origin_LOS', 'Origin_NBO', 'Origin_TUN',
    'Destination_CAI', 'Destination_CMN', 'Destination_CPT', 'Destination_DSS', 
    'Destination_JNB', 'Destination_KGL', 'Destination_LOS', 'Destination_NBO', 'Destination_TUN'
]

@app.post("/predict")
def predict_delay(data: FlightInput):
    try:
        # Convert input to DataFrame
        input_df = pd.DataFrame([data.dict()])
        input_df = input_df[FEATURE_COLUMNS]

        # Scale features
        scaled = scaler.transform(input_df)

        # Predict delay
        prediction = model.predict(scaled)[0]
        return {"predicted_delay_minutes": round(float(prediction), 2)}

    except Exception as e:
        return {"error": str(e)}
# Run the app with: uvicorn prediction:app --reload
# Ensure you have the model and scaler files in the same directory as this script.
# To run the FastAPI app, use the command:
# uvicorn prediction:app --reload
# Make sure to install the required packages:
# pip install fastapi uvicorn joblib pandas scikit-learn
# Note: The model and scaler files should be pre-trained and saved as 'best_model.pkl' and 'scaler.pkl'.
# Ensure you have the model and scaler files in the same directory as this script.