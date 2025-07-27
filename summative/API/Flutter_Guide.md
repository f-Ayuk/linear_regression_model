# Flutter Integration Guide for African Flight Delay Prediction API

## API Overview
**Endpoint**: `http://127.0.0.1:8001/predict`
**Method**: POST
**Content-Type**: application/json

## User-Friendly Field Names

The API now uses intuitive field names instead of technical terms:

### Required Fields:
- `scheduled_time` (0-23): What hour was the flight scheduled to depart?
- `actual_time` (0-23): What hour did the flight actually depart?
- `departure_delay_minutes` (-30 to 90): How many minutes late/early was departure?
  - **Positive numbers** = Late (e.g., 15 = 15 minutes late)
  - **Negative numbers** = Early (e.g., -5 = 5 minutes early)  
  - **Zero** = Exactly on time

### Optional Fields (Set ONE to 1, others to 0):

#### Airlines:
- `Airline_Airlink`
- `Airline_EgyptAir`
- `Airline_Ethiopian_Airlines`
- `Airline_FlySafair`
- `Airline_Kenya_Airways`
- `Airline_Royal_Air_Maroc`
- `Airline_RwandAir`
- `Airline_South_African_Airways`
- `Airline_Tunisair`

#### Origin/Destination Airports:
- `CAI` (Cairo), `CMN` (Casablanca), `CPT` (Cape Town)
- `DSS` (Dakar), `JNB` (Johannesburg), `KGL` (Kigali)
- `LOS` (Lagos), `NBO` (Nairobi), `TUN` (Tunis)

## Flutter Dart Example

```dart
class FlightDelayService {
  static const String baseUrl = 'http://127.0.0.1:8001';
  
  Future<Map<String, dynamic>> predictDelay({
    required int scheduledTime,
    required int actualTime,
    required double departureDelayMinutes,
    String? airline,
    String? origin,
    String? destination,
  }) async {
    
    Map<String, dynamic> requestBody = {
      'scheduled_time': scheduledTime,
      'actual_time': actualTime,
      'departure_delay_minutes': departureDelayMinutes,
    };
    
    if (airline != null) requestBody['Airline_$airline'] = 1;
    if (origin != null) requestBody['Origin_$origin'] = 1;
    if (destination != null) requestBody['Destination_$destination'] = 1;
    
    final response = await http.post(
      Uri.parse('$baseUrl/predict'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(requestBody),
    );
    
    return json.decode(response.body);
  }
}
```

## Sample API Test

### Request:
```json
{
  "scheduled_time": 14,
  "actual_time": 14,
  "departure_delay_minutes": 15,
  "Airline_Kenya_Airways": 1,
  "Origin_NBO": 1,
  "Destination_JNB": 1
}
```

### Response:
```json
{
  "predicted_delay_minutes": 25.67,
  "interpretation": "Flight predicted to have moderate delay of 26 minutes"
}
```
