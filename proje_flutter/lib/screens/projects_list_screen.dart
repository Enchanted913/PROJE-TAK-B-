import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/auth_provider.dart';
import '../services/api_service.dart';
import 'project_form_screen.dart';
import 'project_detail_screen.dart';

class ProjectsListScreen extends StatefulWidget {
  const ProjectsListScreen({super.key});

  @override
  State<ProjectsListScreen> createState() => _ProjectsListScreenState();
}

class _ProjectsListScreenState extends State<ProjectsListScreen> {
  late ApiService api;
  late Future<List<Map<String, dynamic>>> _projects;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final token = Provider.of<AuthProvider>(context, listen: false).token;
    api = ApiService(authToken: token);
    _projects = api.fetchProjects();
  }

  void _refresh() {
    setState(() {
      _projects = api.fetchProjects();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Projeler')),
      body: FutureBuilder<List<Map<String, dynamic>>>(
        future: _projects,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) return const Center(child: CircularProgressIndicator());
          if (snapshot.hasError) return Center(child: Text('Hata: ${snapshot.error}'));
          final projects = snapshot.data ?? [];
          return RefreshIndicator(
            onRefresh: () async => _refresh(),
            child: ListView.builder(
              itemCount: projects.length,
              itemBuilder: (context, index) {
                final p = projects[index];
                return ListTile(
                  title: Text(p['title'] ?? ''),
                  subtitle: Text(p['description'] ?? ''),
                  trailing: Text(p['status'] ?? ''),
                  onTap: () async {
                    await Navigator.of(context).push(MaterialPageRoute(builder: (_) => ProjectDetailScreen(project: p)));
                    _refresh();
                  },
                );
              },
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        child: const Icon(Icons.add),
        onPressed: () async {
          await Navigator.of(context).push(MaterialPageRoute(builder: (_) => const ProjectFormScreen()));
          _refresh();
        },
      ),
    );
  }
}
