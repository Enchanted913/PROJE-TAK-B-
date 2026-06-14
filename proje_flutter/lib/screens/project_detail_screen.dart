import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/auth_provider.dart';
import '../services/api_service.dart';
import 'task_form_screen.dart';

class ProjectDetailScreen extends StatefulWidget {
  final Map<String, dynamic> project;
  const ProjectDetailScreen({super.key, required this.project});

  @override
  State<ProjectDetailScreen> createState() => _ProjectDetailScreenState();
}

class _ProjectDetailScreenState extends State<ProjectDetailScreen> {
  late ApiService api;
  late Future<List<Map<String, dynamic>>> _tasks;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final token = Provider.of<AuthProvider>(context, listen: false).token;
    api = ApiService(authToken: token);
    _tasks = api.fetchTasks(int.parse(widget.project['id'].toString()));
  }

  void _refresh() {
    setState(() {
      _tasks = api.fetchTasks(int.parse(widget.project['id'].toString()));
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.project['title'] ?? 'Proje Detayı')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(widget.project['title'] ?? '', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 8),
                    Text(widget.project['description'] ?? ''),
                    const SizedBox(height: 8),
                    Text('Durum: ${widget.project['status'] ?? ''}'),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            Expanded(
              child: FutureBuilder<List<Map<String, dynamic>>>(
                future: _tasks,
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.waiting) return const Center(child: CircularProgressIndicator());
                  if (snapshot.hasError) return Center(child: Text('Hata: ${snapshot.error}'));
                  final tasks = snapshot.data ?? [];
                  if (tasks.isEmpty) {
                    return const Center(child: Text('Görev bulunamadı'));
                  }
                  return ListView.builder(
                    itemCount: tasks.length,
                    itemBuilder: (context, index) {
                      final t = tasks[index];
                      return Card(
                        child: ListTile(
                          title: Text(t['title'] ?? ''),
                          subtitle: Text('Durum: ${t['status'] ?? ''} - Puan: ${t['points'] ?? 0}'),
                          onTap: () async {
                            await Navigator.of(context).push(MaterialPageRoute(builder: (_) => TaskFormScreen(projectId: int.parse(widget.project['id'].toString()), task: t)));
                            _refresh();
                          },
                        ),
                      );
                    },
                  );
                },
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        child: const Icon(Icons.add),
        onPressed: () async {
          await Navigator.of(context).push(MaterialPageRoute(builder: (_) => TaskFormScreen(projectId: int.parse(widget.project['id'].toString()))));
          _refresh();
        },
      ),
    );
  }
}
