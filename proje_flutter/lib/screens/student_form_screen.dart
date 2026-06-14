import 'package:flutter/material.dart';
import '../services/api_service.dart';

class StudentFormScreen extends StatefulWidget {
  final Map<String, dynamic>? student;
  const StudentFormScreen({super.key, this.student});

  @override
  State<StudentFormScreen> createState() => _StudentFormScreenState();
}

class _StudentFormScreenState extends State<StudentFormScreen> {
  final _formKey = GlobalKey<FormState>();
  final ApiService api = ApiService();
  String? _username, _name, _surname, _email, _studentNo, _phone, _password;
  bool _loading = false;

  @override
  void initState() {
    super.initState();
    final s = widget.student;
    if (s != null) {
      _username = s['username']?.toString();
      _name = s['name']?.toString();
      _surname = s['surname']?.toString();
      _email = s['email']?.toString();
      _studentNo = s['student_no']?.toString();
      _phone = s['phone']?.toString();
    }
  }

  void _submit() async {
    if (!_formKey.currentState!.validate()) return;
    _formKey.currentState!.save();
    setState(() => _loading = true);
    try {
      final body = {
        'username': _username,
        'name': _name,
        'surname': _surname,
        'email': _email,
        'student_no': _studentNo,
        'phone': _phone,
        'password': _password,
      };
      if (widget.student == null) {
        await api.createStudent(body);
      } else {
        final id = widget.student!['id'];
        await api.updateStudent(int.parse(id.toString()), body);
      }
      Navigator.of(context).pop();
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Hata: $e')));
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.student == null ? 'Öğrenci Ekle' : 'Öğrenci Düzenle')),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Form(
                key: _formKey,
                child: Column(
                  children: [
                    TextFormField(initialValue: _username, decoration: const InputDecoration(labelText: 'Kullanıcı adı'), onSaved: (v) => _username = v, validator: (v) => (v==null||v.isEmpty)?'Gerekli':null),
                    TextFormField(initialValue: _name, decoration: const InputDecoration(labelText: 'Ad'), onSaved: (v) => _name = v),
                    TextFormField(initialValue: _surname, decoration: const InputDecoration(labelText: 'Soyad'), onSaved: (v) => _surname = v),
                    TextFormField(initialValue: _email, decoration: const InputDecoration(labelText: 'E-posta'), onSaved: (v) => _email = v),
                    TextFormField(initialValue: _studentNo, decoration: const InputDecoration(labelText: 'Öğrenci no'), onSaved: (v) => _studentNo = v),
                    TextFormField(initialValue: _phone, decoration: const InputDecoration(labelText: 'Telefon'), onSaved: (v) => _phone = v),
                    TextFormField(decoration: const InputDecoration(labelText: 'Parola (yeni kullanıcı için)'), obscureText: true, onSaved: (v) => _password = v),
                    const SizedBox(height: 16),
                    _loading ? const CircularProgressIndicator() : ElevatedButton(onPressed: _submit, child: const Text('Kaydet')),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
