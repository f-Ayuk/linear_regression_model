# test_api.py - Test version without model files

from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

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
    DepartureDelta: int

    Airline_AA: int = Field(0, ge=0, le=1)
    Airline_DL: int = Field(0, ge=0, le=1)
    Airline_UA: int = Field(0, ge=0, le=1)

    Origin_JFK: int = Field(0, ge=0, le=1)
    Origin_LAX: int = Field(0, ge=0, le=1)
    Origin_ORD: int = Field(0, ge=0, le=1)

    Destination_DEN: int = Field(0, ge=0, le=1)
    Destination_ATL: int = Field(0, ge=0, le=1)
    Destination_MIA: int = Field(0, ge=0, le=1)

@app.post("/predict")
def predict_delay(data: FlightInput):
    try:
        # Dummy prediction for testing (replace with actual model later)
        base_delay = data.DepartureDelta * 0.5
        hour_factor = abs(data.ActualHour - data.ScheduledHour) * 2
        
        # Simple dummy calculation
        prediction = base_delay + hour_factor + 10  # Base delay of 10 minutes
        
        return {"predicted_delay_minutes": round(float(prediction), 2)}

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "Flight Delay Prediction API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
