import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/api_service.dart';

class AuthProvider extends ChangeNotifier {
  final ApiService api;
  String? _token;
  Map<String, dynamic>? _user;

  AuthProvider({ApiService? apiService}) : api = apiService ?? ApiService();

  String? get token => _token;
  Map<String, dynamic>? get user => _user;

  Future<void> loadFromStorage() async {
    final sp = await SharedPreferences.getInstance();
    _token = sp.getString('auth_token');
    if (_token != null) api.setAuthToken(_token);
    notifyListeners();
  }

  Future<bool> login(String username, String password) async {
    final res = await api.login({'username': username, 'password': password});
    if (res.containsKey('token')) {
      _token = res['token'];
      api.setAuthToken(_token);
      final sp = await SharedPreferences.getInstance();
      await sp.setString('auth_token', _token!);
      if (res.containsKey('user')) _user = res['user'];
      notifyListeners();
      return true;
    }
    return false;
  }

  Future<bool> register(Map<String, dynamic> body) async {
    final res = await api.register(body);
    if (res.containsKey('token')) {
      _token = res['token'];
      api.setAuthToken(_token);
      final sp = await SharedPreferences.getInstance();
      await sp.setString('auth_token', _token!);
      if (res.containsKey('user')) _user = res['user'];
      notifyListeners();
      return true;
    }
    return false;
  }

  Future<void> logout() async {
    _token = null;
    _user = null;
    api.setAuthToken(null);
    final sp = await SharedPreferences.getInstance();
    await sp.remove('auth_token');
    notifyListeners();
  }
}
