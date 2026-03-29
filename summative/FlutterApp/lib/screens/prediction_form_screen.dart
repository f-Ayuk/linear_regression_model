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
  final TextEditingController timeController = TextEditingController();

  String? selectedAirline;
  String? selectedOrigin;
  String? selectedDest;

  List<String> airlines = [];
  List<String> origins = [];
  List<String> destinations = [];

  String result = "";
  bool isLoading = true;

  final String baseUrl = "https://flight-delay-predict-vyo2.onrender.com";

  @override
  void initState() {
    super.initState();

    // Simulate dropdown options to test the UI (for now without API call)
    setState(() {
      airlines = ["AA", "DL", "UA"]; // Simulated data
      origins = ["JFK", "LAX"]; // Simulated data
      destinations = ["ORD", "ATL"]; // Simulated data
      isLoading = false; // Stop showing loading spinner
    });

    // Uncomment below code to fetch data from the API once ready:
    // fetchOptions();
  }

  // Future method to fetch API options (you can uncomment it when you're ready)
  Future<void> fetchOptions() async {
    final response = await http.get(Uri.parse("$baseUrl/options"));

    if (response.statusCode == 200) {
      final data = json.decode(response.body);

      setState(() {
        airlines = List<String>.from(data["airlines"]);
        origins = List<String>.from(data["origins"]);
        destinations = List<String>.from(data["destinations"]);
        isLoading = false; // Stop showing loading spinner after data is fetched
      });
    }
  }

  // Prediction function that makes API request
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

  // Dropdown widget for selecting options
  Widget dropdown(
    String label,
    List<String> items,
    String? value,
    Function(String?) onChanged,
  ) {
    return DropdownButtonFormField<String>(
      value: value,
      hint: Text(label),
      isExpanded: true,
      items:
          items.map((item) {
            return DropdownMenuItem<String>(value: item, child: Text(item));
          }).toList(),
      onChanged: onChanged,
    );
  }

  @override
  Widget build(BuildContext context) {
    // If the data is still loading, show a loading spinner
    if (isLoading) {
      return Scaffold(
        appBar: AppBar(title: const Text("Prediction Form")),
        body: const Center(child: CircularProgressIndicator()),
      );
    }

    return Scaffold(
      appBar: AppBar(title: const Text("Prediction Form")),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              TextField(
                controller: timeController,
                decoration: InputDecoration(
                  labelText: "CRS Departure Time (HH:MM)",
                  hintText: "e.g., 15:30",
                ),
                keyboardType: TextInputType.datetime,
              ),
              const SizedBox(height: 10),
              TextField(
                controller: dayController,
                decoration: const InputDecoration(labelText: "DayOfWeek (1-7)"),
                keyboardType: TextInputType.number,
              ),
              const SizedBox(height: 10),
              // Dropdown for Airline
              dropdown("Select Airline", airlines, selectedAirline, (val) {
                setState(() => selectedAirline = val);
              }),
              const SizedBox(height: 10),
              // Dropdown for Origin
              dropdown("Select Origin", origins, selectedOrigin, (val) {
                setState(() => selectedOrigin = val);
              }),
              const SizedBox(height: 10),
              // Dropdown for Destination
              dropdown("Select Destination", destinations, selectedDest, (val) {
                setState(() => selectedDest = val);
              }),
              const SizedBox(height: 20),
              ElevatedButton(onPressed: predict, child: const Text("Predict")),
              const SizedBox(height: 20),
              Text(result, style: const TextStyle(fontSize: 18)),
            ],
          ),
        ),
      ),
    );
  }
}
