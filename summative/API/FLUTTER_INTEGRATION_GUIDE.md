# Flutter App Integration Guide

## API Field Names (User-Friendly)

### Required Fields:
1. **scheduled_hour** (int, 0-23)
   - Label: "Scheduled Departure Hour"
   - Help: "Enter hour in 24-hour format (e.g., 14 for 2 PM)"

2. **actual_hour** (int, 0-23)
   - Label: "Actual Departure Hour" 
   - Help: "Enter hour in 24-hour format (e.g., 15 for 3 PM)"

3. **departure_delay_minutes** (float, -30 to 90)
   - Label: "Departure Delay (minutes)"
   - Help: "Enter + for late, - for early, 0 for on-time"
   - Examples: "15 (15 min late)", "-5 (5 min early)", "0 (on time)"

### Optional Fields (Airline Selection - only one should be 1):
- Airlink, EgyptAir, Ethiopian Airlines, FlySafair, Kenya Airways, 
- Royal Air Maroc, RwandAir, South African Airways, Tunisair

### Optional Fields (Airport Selection - only one should be 1):
**Origins**: CAI, CMN, CPT, DSS, JNB, KGL, LOS, NBO, TUN
**Destinations**: CAI, CMN, CPT, DSS, JNB, KGL, LOS, NBO, TUN

## Airport Codes:
- **CAI**: Cairo International Airport
- **CMN**: Mohammed V International Airport (Casablanca)
- **CPT**: Cape Town International Airport
- **DSS**: Dakar Airport
- **JNB**: OR Tambo International Airport (Johannesburg)
- **KGL**: Kigali International Airport
- **LOS**: Murtala Muhammed International Airport (Lagos)
- **NBO**: Jomo Kenyatta International Airport (Nairobi)
- **TUN**: Tunis Airport

## Sample Flutter HTTP Request:

```dart
final response = await http.post(
  Uri.parse('http://127.0.0.1:8001/predict'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'scheduled_hour': 14,           // 2 PM scheduled
    'actual_hour': 14,              // 2 PM actual  
    'departure_delay_minutes': 15,  // 15 minutes late
    'Airline_Kenya Airways': 1,     // Kenya Airways flight
    'Origin_NBO': 1,               // From Nairobi
    'Destination_JNB': 1,          // To Johannesburg
    // All other airline/airport fields default to 0
  }),
);
```

## Expected Response:
```json
{
  "predicted_delay_minutes": 18.45,
  "interpretation": "Flight predicted to have minor delay of 18 minutes"
}
```

## UI Suggestions:

### Input Form:
1. **Time Pickers**: For scheduled_hour and actual_hour
2. **Number Input**: For departure_delay_minutes with +/- buttons
3. **Dropdown**: For airline selection
4. **Dropdown**: For origin and destination airports
5. **Helper Text**: Show examples and explanations

### Results Display:
- Show predicted delay in large, colored text
- Green: Early/On-time (≤ 0 minutes)
- Yellow: Minor delay (1-15 minutes) 
- Orange: Moderate delay (16-30 minutes)
- Red: Significant delay (> 30 minutes)
- Include interpretation text for user clarity
