import requests
import json

# Test the updated API with new field names
url = "http://127.0.0.1:8001/predict"

# Sample data using the new field names
test_data = {
    "scheduled_time": 14,
    "actual_time": 14, 
    "departure_delay_minutes": 15,
    "Airline_Kenya_Airways": 1,
    "Origin_NBO": 1,
    "Destination_JNB": 1
}

print("Testing API with new field names:")
print("Request data:", json.dumps(test_data, indent=2))

try:
    response = requests.post(url, json=test_data)
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Success!")
        print("Response:", json.dumps(result, indent=2))
    else:
        print(f"❌ Error: {response.status_code}")
        print("Response:", response.text)
except requests.exceptions.ConnectionError:
    print("⚠️  API server not running. Start it with: python start_prediction_server.py")
except Exception as e:
    print(f"❌ Error: {e}")
