import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'result_screen.dart';

class PredictionFormScreen extends StatefulWidget {
  @override
  _PredictionFormScreenState createState() => _PredictionFormScreenState();
}

class _PredictionFormScreenState extends State<PredictionFormScreen> {
  final _formKey = GlobalKey<FormState>();
  int scheduledHour = 12;
  int actualHour = 12;
  int delta = 0;

  String airline = 'Kenya Airways';
  String origin = 'JNB';
  String destination = 'LOS';

  List<String> airlines = ['Kenya Airways', 'South African Airways'];
  List<String> origins = ['JNB', 'NBO'];
  List<String> destinations = ['LOS', 'CPT'];

  Future<void> _predictDelay() async {
    final uri = Uri.parse(
      'https://your-api-url.onrender.com/predict',
    ); // Replace this with your Render URL

    // One-hot encoding
    Map<String, int> airlineMap = {
      'Airline_Kenya': airline == 'Kenya Airways' ? 1 : 0,
      'Airline_SAA': airline == 'South African Airways' ? 1 : 0,
    };

    Map<String, int> originMap = {
      'Origin_JNB': origin == 'JNB' ? 1 : 0,
      'Origin_NBO': origin == 'NBO' ? 1 : 0,
    };

    Map<String, int> destMap = {
      'Destination_LOS': destination == 'LOS' ? 1 : 0,
      'Destination_CPT': destination == 'CPT' ? 1 : 0,
    };

    final body = {
      'ScheduledHour': scheduledHour,
      'ActualHour': actualHour,
      'DepartureDelta': delta,
      ...airlineMap,
      ...originMap,
      ...destMap,
    };

    try {
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      );

      if (response.statusCode == 200) {
        final result = jsonDecode(response.body);
        Navigator.push(
          context,
          MaterialPageRoute(
            builder:
                (context) =>
                    ResultScreen(result: result['PredictedDelayMinutes']),
          ),
        );
      } else {
        _showError("Invalid response: ${response.body}");
      }
    } catch (e) {
      _showError("Error occurred: $e");
    }
  }

  void _showError(String message) {
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(SnackBar(content: Text(message)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Enter Flight Details')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              DropdownButtonFormField(
                value: airline,
                items:
                    airlines
                        .map((a) => DropdownMenuItem(value: a, child: Text(a)))
                        .toList(),
                onChanged: (val) => setState(() => airline = val as String),
                decoration: InputDecoration(labelText: 'Airline'),
              ),
              DropdownButtonFormField(
                value: origin,
                items:
                    origins
                        .map((o) => DropdownMenuItem(value: o, child: Text(o)))
                        .toList(),
                onChanged: (val) => setState(() => origin = val as String),
                decoration: InputDecoration(labelText: 'Origin'),
              ),
              DropdownButtonFormField(
                value: destination,
                items:
                    destinations
                        .map((d) => DropdownMenuItem(value: d, child: Text(d)))
                        .toList(),
                onChanged: (val) => setState(() => destination = val as String),
                decoration: InputDecoration(labelText: 'Destination'),
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Scheduled Hour (0-23)'),
                keyboardType: TextInputType.number,
                onChanged: (val) => scheduledHour = int.parse(val),
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Actual Hour (0-23)'),
                keyboardType: TextInputType.number,
                onChanged: (val) => actualHour = int.parse(val),
              ),
              TextFormField(
                decoration: InputDecoration(
                  labelText: 'Departure Delta (-3 to 3)',
                ),
                keyboardType: TextInputType.number,
                onChanged: (val) => delta = int.parse(val),
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: _predictDelay,
                child: Text("Predict Delay"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}