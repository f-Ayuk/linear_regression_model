import 'package:flutter/material.dart';

class ResultScreen extends StatelessWidget {
  final double result;
  final String? interpretation;

  const ResultScreen({required this.result, this.interpretation});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Prediction Result")),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.access_time, size: 80, color: Colors.indigo),
              SizedBox(height: 20),
              Text(
                "Estimated Delay: ${result.toStringAsFixed(2)} minutes",
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              if (interpretation != null) ...[
                SizedBox(height: 16),
                Text(
                  interpretation!,
                  style: TextStyle(fontSize: 18, color: Colors.grey[600]),
                  textAlign: TextAlign.center,
                ),
              ],
              SizedBox(height: 40),
              ElevatedButton(
                onPressed: () => Navigator.pop(context),
                child: Text("Back"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
