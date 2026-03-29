import 'package:flutter/material.dart';
import 'result_screen.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class PredictionFormScreen extends StatefulWidget {
  const PredictionFormScreen({super.key});

  @override
  _PredictionFormScreenState createState() => _PredictionFormScreenState();
}

class _PredictionFormScreenState extends State<PredictionFormScreen> {
  final TextEditingController dayController = TextEditingController();
  final TextEditingController timeController =
      TextEditingController(); // CRSDepTime input
  String? selectedAirline;
  String? selectedOrigin;
  String? selectedDest;

  List airlines = [];
  List origins = [];
  List destinations = [];

  String result = "";

  final String baseUrl = "https://flight-delay-predict-vyo2.onrender.com";

  @override
  void initState() {
    super.initState();
    fetchOptions();
  }

  Future<void> fetchOptions() async {
    final response = await http.get(Uri.parse("$baseUrl/options"));

    if (response.statusCode == 200) {
      final data = json.decode(response.body);

      setState(() {
        airlines = data["airlines"];
        origins = data["origins"];
        destinations = data["destinations"];
      });
    }
  }

  Future<void> predict() async {
    try {
      int crsDepTime = int.parse(timeController.text.replaceAll(":", ""));

      final response = await http.post(
        Uri.parse("$baseUrl/predict"),
        headers: {"Content-Type": "application/json"},
        body: json.encode({
          "CRSDepTime": crsDepTime,
          "DayOfWeek": int.parse(dayController.text),
          "Airline": selectedAirline,
          "Origin": selectedOrigin,
          "Dest": selectedDest,
        }),
      );

      final data = json.decode(response.body);

      setState(() {
        result =
            "Delay: ${data['delay_minutes']} min\nStatus: ${data['status']}";
      });

      Navigator.push(
        context,
        MaterialPageRoute(
          builder:
              (context) => ResultScreen(
                result: data['delay_minutes'],
                interpretation: data['status'],
              ),
        ),
      );
    } catch (e) {
      setState(() {
        result = "Error: Invalid input";
      });
    }
  }

  Widget dropdown(
    String label,
    List items,
    String? value,
    Function(String?) onChanged,
  ) {
    return DropdownButtonFormField<String>(
      value: value,
      hint: Text(label),
      items:
          items.map<DropdownMenuItem<String>>((item) {
            return DropdownMenuItem(value: item, child: Text(item));
          }).toList(),
      onChanged: onChanged,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Prediction Form")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: timeController,
              decoration: InputDecoration(
                labelText: "CRS Departure Time (input as HH:MM)",
                hintText: "e.g., 15:30",
              ),
              keyboardType: TextInputType.datetime,
            ),

            TextField(
              controller: dayController,
              decoration: InputDecoration(labelText: "DayOfWeek (1-7)"),
              keyboardType: TextInputType.number,
            ),

            SizedBox(height: 10),

            dropdown("Select Airline", airlines, selectedAirline, (val) {
              setState(() => selectedAirline = val);
            }),

            dropdown("Select Origin", origins, selectedOrigin, (val) {
              setState(() => selectedOrigin = val);
            }),

            dropdown("Select Destination", destinations, selectedDest, (val) {
              setState(() => selectedDest = val);
            }),

            SizedBox(height: 20),

            ElevatedButton(onPressed: predict, child: const Text("Predict")),

            SizedBox(height: 20),

            Text(result, style: TextStyle(fontSize: 18)),
          ],
        ),
      ),
    );
  }
}
