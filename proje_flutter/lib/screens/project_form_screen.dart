import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/auth_provider.dart';
import '../services/api_service.dart';

class ProjectFormScreen extends StatefulWidget {
  final Map<String, dynamic>? project;
  const ProjectFormScreen({super.key, this.project});

  @override
  State<ProjectFormScreen> createState() => _ProjectFormScreenState();
}

class _ProjectFormScreenState extends State<ProjectFormScreen> {
  final _formKey = GlobalKey<FormState>();
  late ApiService api;
  String? _title;
  String? _description;
  String? _status;
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
    final p = widget.project;
    if (p != null) {
      _title = p['title']?.toString();
      _description = p['description']?.toString();
      _status = p['status']?.toString();
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
      };
      if (widget.project == null) {
        await api.createProject(body);
      } else {
        final id = int.parse(widget.project!['id'].toString());
        await api.updateProject(id, body);
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
      appBar: AppBar(title: Text(widget.project == null ? 'Proje Ekle' : 'Proje Düzenle')),
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
                    TextFormField(initialValue: _title, decoration: const InputDecoration(labelText: 'Proje adı'), onSaved: (v) => _title = v, validator: (v) => (v == null || v.isEmpty) ? 'Gerekli' : null),
                    const SizedBox(height: 8),
                    TextFormField(initialValue: _description, decoration: const InputDecoration(labelText: 'Açıklama'), minLines: 2, maxLines: 4, onSaved: (v) => _description = v),
                    const SizedBox(height: 8),
                    DropdownButtonFormField<String>(
                      decoration: const InputDecoration(labelText: 'Durum'),
                      value: _status ?? 'devam',
                      items: const [
                        DropdownMenuItem(value: 'devam', child: Text('Devam Eden')),
                        DropdownMenuItem(value: 'yarim', child: Text('Yarım')),
                        DropdownMenuItem(value: 'tamam', child: Text('Tamamlanan')),
                      ],
                      onChanged: (v) => _status = v,
                      onSaved: (v) => _status = v,
                    ),
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
