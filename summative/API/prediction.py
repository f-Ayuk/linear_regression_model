# prediction.py

from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd

# Load model and scaler
model = joblib.load("best_model.pkl")
scaler = joblib.load("scaler.pkl")

app = FastAPI(
    title="African Flight Delay Prediction API",
    description="Predict flight delays for African airlines based on departure information",
    version="1.0.0"
)

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
    scheduled_hour: int = Field(..., ge=0, le=23, description="Scheduled departure hour (0-23)", example=14)
    actual_hour: int = Field(..., ge=0, le=23, description="Actual departure hour (0-23)", example=14)
    departure_delay_minutes: float = Field(
        ..., 
        ge=-30, 
        le=90, 
        description="Departure delay in minutes (positive = late, negative = early, 0 = on-time)",
        example=15,
        alias="DepartureDelta"
    )

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

# Feature columns (must match model input order) - using original names for model compatibility
FEATURE_COLUMNS = [
    'ScheduledHour', 'ActualHour', 'DepartureDelta',  # Keep original names for model
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
    """
    Predict flight delay based on departure information and flight details.
    
    - **scheduled_hour**: Hour of scheduled departure (0-23)
    - **actual_hour**: Hour of actual departure (0-23) 
    - **departure_delay_minutes**: How many minutes delayed (+ late, - early, 0 on-time)
    - **Airlines & Airports**: Set appropriate flags to 1, others to 0
    
    Returns predicted delay in minutes.
    """
    try:
        # Convert input to DataFrame with original column names for model compatibility
        input_dict = data.dict(by_alias=True)  # Use alias names (original names)
        
        # Map user-friendly names to original model names
        model_input = {
            'ScheduledHour': input_dict.get('scheduled_hour', data.scheduled_hour),
            'ActualHour': input_dict.get('actual_hour', data.actual_hour),
            'DepartureDelta': input_dict.get('DepartureDelta', data.departure_delay_minutes)
        }
        
        # Add airline/airport flags
        for key, value in input_dict.items():
            if key.startswith(('Airline_', 'Origin_', 'Destination_')):
                model_input[key] = value
        
        input_df = pd.DataFrame([model_input])
        
        # Ensure all columns are present (especially one-hot encoded)
        for col in FEATURE_COLUMNS:
            if col not in input_df.columns:
                input_df[col] = 0
        
        # Reorder columns to match model training
        input_df = input_df[FEATURE_COLUMNS]

        # Scale features
        scaled = scaler.transform(input_df)

        # Predict delay
        prediction = model.predict(scaled)[0]
        return {
            "predicted_delay_minutes": round(float(prediction), 2),
            "interpretation": get_delay_interpretation(prediction)
        }

    except Exception as e:
        return {"error": str(e)}

def get_delay_interpretation(delay_minutes):
    """Provide human-readable interpretation of delay prediction"""
    if delay_minutes <= -5:
        return f"Flight predicted to depart {abs(delay_minutes):.0f} minutes early"
    elif delay_minutes < 0:
        return "Flight predicted to depart slightly early"
    elif delay_minutes == 0:
        return "Flight predicted to depart on time"
    elif delay_minutes <= 15:
        return f"Flight predicted to have minor delay of {delay_minutes:.0f} minutes"
    elif delay_minutes <= 30:
        return f"Flight predicted to have moderate delay of {delay_minutes:.0f} minutes"
    else:
        return f"Flight predicted to have significant delay of {delay_minutes:.0f} minutes"

@app.get("/")
def read_root():
    return {
        "message": "African Flight Delay Prediction API",
        "description": "Use /predict endpoint to predict flight delays",
        "documentation": "/docs",
        "version": "1.0.0"
    }

@app.get("/airlines")
def get_supported_airlines():
    """Get list of supported airlines"""
    airlines = [col.replace('Airline_', '') for col in FEATURE_COLUMNS if col.startswith('Airline_')]
    return {"supported_airlines": airlines}

@app.get("/airports")
def get_supported_airports():
    """Get list of supported airports (origins and destinations)"""
    origins = [col.replace('Origin_', '') for col in FEATURE_COLUMNS if col.startswith('Origin_')]
    destinations = [col.replace('Destination_', '') for col in FEATURE_COLUMNS if col.startswith('Destination_')]
    return {
        "supported_origins": origins,
        "supported_destinations": destinations
    }

# Run the app with: uvicorn prediction:app --reload
# Ensure you have the model and scaler files in the same directory as this script.
# To run the FastAPI app, use the command:
# uvicorn prediction:app --reload
# Make sure to install the required packages:
# pip install fastapi uvicorn joblib pandas scikit-learn
# Note: The model and scaler files should be pre-trained and saved as 'best_model.pkl' and 'scaler.pkl'.
# Ensure you have the model and scaler files in the same directory as this script.