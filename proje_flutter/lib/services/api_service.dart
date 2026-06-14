import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config.dart';
import '../models/product.dart';

class ApiService {
  final String baseUrl;
  String? _authToken;
  ApiService({this.baseUrl = API_BASE_URL, String? authToken}) {
    _authToken = authToken;
  }

  void setAuthToken(String? token) {
    _authToken = token;
  }

  Map<String, String> get _headers => {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      'Authorization': 'Bearer ${_authToken ?? API_TOKEN}',
      };

  Future<List<Product>> fetchProducts() async {
    final uri = Uri.parse('$baseUrl/api/products');
    final res = await http.get(uri, headers: _headers);
    if (res.statusCode == 200) {
      final data = json.decode(res.body);
      if (data is List) {
        return data.map((e) => Product.fromJson(e)).toList();
      }
      // handle wrapped responses
      if (data['data'] is List) {
        return (data['data'] as List).map((e) => Product.fromJson(e)).toList();
      }
    }
    throw Exception('Failed to load products: ${res.statusCode}');
  }

  // Example: Register user
  Future<Map<String, dynamic>> register(Map<String, dynamic> body) async {
    final uri = Uri.parse('$baseUrl/api/register');
    final res = await http.post(uri, headers: _headers, body: json.encode(body));
    return json.decode(res.body);
  }

  // Example: Login
  Future<Map<String, dynamic>> login(Map<String, dynamic> body) async {
    final uri = Uri.parse('$baseUrl/api/login');
    final res = await http.post(uri, headers: _headers, body: json.encode(body));
    return json.decode(res.body);
  }

  // Students endpoints
  Future<List<Map<String, dynamic>>> fetchStudents() async {
    final uri = Uri.parse('$baseUrl/api/students');
    final res = await http.get(uri, headers: _headers);
    if (res.statusCode == 200) {
      final data = json.decode(res.body);
      if (data is List) return List<Map<String, dynamic>>.from(data);
      if (data['data'] is List) return List<Map<String, dynamic>>.from(data['data']);
      return [];
    }
    throw Exception('Failed to load students: ${res.statusCode}');
  }

  Future<Map<String, dynamic>> createStudent(Map<String, dynamic> body) async {
    final uri = Uri.parse('$baseUrl/api/students');
    final res = await http.post(uri, headers: _headers, body: json.encode(body));
    return json.decode(res.body);
  }

  Future<Map<String, dynamic>> updateStudent(int id, Map<String, dynamic> body) async {
    final uri = Uri.parse('$baseUrl/api/students/$id');
    final res = await http.put(uri, headers: _headers, body: json.encode(body));
    return json.decode(res.body);
  }

  Future<bool> deleteStudent(int id) async {
    final uri = Uri.parse('$baseUrl/api/students/$id');
    final res = await http.delete(uri, headers: _headers);
    return res.statusCode == 200 || res.statusCode == 204;
  }

  // Projects endpoints
  Future<List<Map<String, dynamic>>> fetchProjects() async {
    final uri = Uri.parse('$baseUrl/api/projects');
    final res = await http.get(uri, headers: _headers);
    if (res.statusCode == 200) {
      final data = json.decode(res.body);
      if (data is List) return List<Map<String, dynamic>>.from(data);
      if (data['data'] is List) return List<Map<String, dynamic>>.from(data['data']);
      return [];
    }
    throw Exception('Failed to load projects: ${res.statusCode}');
  }

  Future<Map<String, dynamic>> createProject(Map<String, dynamic> body) async {
    final uri = Uri.parse('$baseUrl/api/projects');
    final res = await http.post(uri, headers: _headers, body: json.encode(body));
    return json.decode(res.body);
  }

  Future<Map<String, dynamic>> updateProject(int id, Map<String, dynamic> body) async {
    final uri = Uri.parse('$baseUrl/api/projects/$id');
    final res = await http.put(uri, headers: _headers, body: json.encode(body));
    return json.decode(res.body);
  }

  Future<bool> deleteProject(int id) async {
    final uri = Uri.parse('$baseUrl/api/projects/$id');
    final res = await http.delete(uri, headers: _headers);
    return res.statusCode == 200 || res.statusCode == 204;
  }

  // Tasks endpoints
  Future<List<Map<String, dynamic>>> fetchTasks(int projectId) async {
    final uri = Uri.parse('$baseUrl/api/projects/$projectId/tasks');
    final res = await http.get(uri, headers: _headers);
    if (res.statusCode == 200) {
      final data = json.decode(res.body);
      if (data is List) return List<Map<String, dynamic>>.from(data);
      if (data['data'] is List) return List<Map<String, dynamic>>.from(data['data']);
      return [];
    }
    throw Exception('Failed to load tasks: ${res.statusCode}');
  }

  Future<Map<String, dynamic>> createTask(int projectId, Map<String, dynamic> body) async {
    final uri = Uri.parse('$baseUrl/api/projects/$projectId/tasks');
    final res = await http.post(uri, headers: _headers, body: json.encode(body));
    return json.decode(res.body);
  }

  Future<Map<String, dynamic>> updateTask(int projectId, int taskId, Map<String, dynamic> body) async {
    final uri = Uri.parse('$baseUrl/api/projects/$projectId/tasks/$taskId');
    final res = await http.put(uri, headers: _headers, body: json.encode(body));
    return json.decode(res.body);
  }

  Future<bool> deleteTask(int projectId, int taskId) async {
    final uri = Uri.parse('$baseUrl/api/projects/$projectId/tasks/$taskId');
    final res = await http.delete(uri, headers: _headers);
    return res.statusCode == 200 || res.statusCode == 204;
  }

  Future<Map<String, dynamic>> updateTaskStatus(int projectId, int taskId, String status) async {
    final uri = Uri.parse('$baseUrl/api/projects/$projectId/tasks/$taskId/status');
    final res = await http.patch(uri, headers: _headers, body: json.encode({'status': status}));
    return json.decode(res.body);
  }
}
