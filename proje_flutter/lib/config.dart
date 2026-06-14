// Configuration for API access and theming
const String API_BASE_URL = 'https://python01.turkticaret.net';
const String API_TOKEN = 'F7CW2ZQ06WHR567MG8P8GELR1BJ23VLA';

// Theme colors - adjust to match the website theme
import 'package:flutter/material.dart';

final ThemeData appTheme = ThemeData(
  primaryColor: Color(0xFF0D47A1),
  colorScheme: ColorScheme.fromSwatch(primarySwatch: Colors.blue),
  visualDensity: VisualDensity.adaptivePlatformDensity,
);
