import 'package:flutter/material.dart';

class ResultScreen extends StatelessWidget {
  final double result;
  final String? interpretation;

  const ResultScreen({super.key, required this.result, this.interpretation});

  String _getDelayMessage(double delay) {
    if (delay <= 0) {
      return "Flight is on time or early!";
    } else if (delay <= 15) {
      return "Minor delay";
    } else if (delay <= 60) {
      return "Moderate delay";
    } else {
      return "Significant delay";
    }
  }

  Color _getDelayColor(double delay) {
    if (delay <= 0) {
      return Colors.green;
    } else if (delay <= 15) {
      return Colors.blue;
    } else if (delay <= 60) {
      return Colors.orange;
    } else {
      return Colors.red;
    }
  }

  @override
  Widget build(BuildContext context) {
    final delayMessage = _getDelayMessage(result);
    final delayColor = _getDelayColor(result);

    return Scaffold(
      appBar: AppBar(
        title: const Text("Prediction Result"),
        backgroundColor: Colors.indigo[900],
        foregroundColor: Colors.white,
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.access_time, size: 80, color: delayColor),
              const SizedBox(height: 20),
              Text(
                "Estimated Arrival Delay:",
                style: TextStyle(fontSize: 20, color: Colors.grey[600]),
              ),
              const SizedBox(height: 10),
              Text(
                "${result.toStringAsFixed(0)} minutes",
                style: TextStyle(
                  fontSize: 36,
                  fontWeight: FontWeight.bold,
                  color: delayColor,
                ),
              ),
              const SizedBox(height: 16),
              Text(
                delayMessage,
                style: TextStyle(
                  fontSize: 18,
                  color: delayColor,
                  fontWeight: FontWeight.w500,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 40),
              ElevatedButton(
                onPressed: () => Navigator.pop(context),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.indigo[900],
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(
                    horizontal: 40,
                    vertical: 16,
                  ),
                ),
                child: const Text("Back to Form"),
              ),
              const SizedBox(height: 16),
              TextButton(
                onPressed: () {
                  Navigator.popUntil(context, (route) => route.isFirst);
                },
                child: const Text(
                  "Back to Home",
                  style: TextStyle(color: Colors.indigo),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}