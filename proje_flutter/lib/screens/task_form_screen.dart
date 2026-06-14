import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/auth_provider.dart';
import '../services/api_service.dart';

class TaskFormScreen extends StatefulWidget {
  final int projectId;
  final Map<String, dynamic>? task;
  const TaskFormScreen({super.key, required this.projectId, this.task});

  @override
  State<TaskFormScreen> createState() => _TaskFormScreenState();
}

class _TaskFormScreenState extends State<TaskFormScreen> {
  final _formKey = GlobalKey<FormState>();
  late ApiService api;
  String? _title;
  String? _description;
  String? _status;
  int? _points;
  bool _loading = false;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final token = Provider.of<AuthProvider>(context, listen: false).token;
    api = ApiService(authToken: token);
  }

  @override
  void initState() {
    super.initState();
    final t = widget.task;
    if (t != null) {
      _title = t['title']?.toString();
      _description = t['description']?.toString();
      _status = t['status']?.toString();
      _points = int.tryParse(t['points']?.toString() ?? '0');
    }
  }

  void _submit() async {
    if (!_formKey.currentState!.validate()) return;
    _formKey.currentState!.save();
    setState(() => _loading = true);
    try {
      final body = {
        'title': _title,
        'description': _description,
        'status': _status,
        'points': _points,
      };
      if (widget.task == null) {
        await api.createTask(widget.projectId, body);
      } else {
        final taskId = int.parse(widget.task!['id'].toString());
        await api.updateTask(widget.projectId, taskId, body);
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
      appBar: AppBar(title: Text(widget.task == null ? 'Görev Ekle' : 'Görev Düzenle')),
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
                    TextFormField(initialValue: _title, decoration: const InputDecoration(labelText: 'Görev başlığı'), onSaved: (v) => _title = v, validator: (v) => (v == null || v.isEmpty) ? 'Gerekli' : null),
                    const SizedBox(height: 8),
                    TextFormField(initialValue: _description, decoration: const InputDecoration(labelText: 'Açıklama'), minLines: 2, maxLines: 4, onSaved: (v) => _description = v),
                    const SizedBox(height: 8),
                    DropdownButtonFormField<String>(
                      decoration: const InputDecoration(labelText: 'Durum'),
                      value: _status ?? 'pending',
                      items: const [
                        DropdownMenuItem(value: 'pending', child: Text('Beklemede')),
                        DropdownMenuItem(value: 'in_progress', child: Text('Devam Ediyor')),
                        DropdownMenuItem(value: 'completed', child: Text('Tamamlandı')),
                      ],
                      onChanged: (v) => _status = v,
                      onSaved: (v) => _status = v,
                    ),
                    const SizedBox(height: 8),
                    TextFormField(initialValue: _points?.toString(), decoration: const InputDecoration(labelText: 'Puan'), keyboardType: TextInputType.number, onSaved: (v) => _points = int.tryParse(v ?? '0')),
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
