import 'package:flutter/material.dart';
import 'prediction_form_screen.dart';

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.indigo[900],
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(32.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.flight_takeoff, size: 100, color: Colors.white),
              SizedBox(height: 20),
              Text(
                'Flight Delay Predictor',
                style: TextStyle(fontSize: 28, color: Colors.white),
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 30),
              ElevatedButton(
                style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.white, foregroundColor: Colors.indigo),
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => PredictionFormScreen()),
                  );
                },
                child: Text('Get Started'),
              )
            ],
          ),
        ),
      ),
    );
  }
}