import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() => runApp(FlightDelayApp());

class FlightDelayApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flight Delay Predictor',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(primarySwatch: Colors.indigo),
      home: HomeScreen(),
    );
  }
}