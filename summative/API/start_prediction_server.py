import uvicorn
from prediction import app

if __name__ == "__main__":
    print("Starting FastAPI Flight Delay Prediction Server...")
    uvicorn.run(app, host="127.0.0.1", port=8001)
