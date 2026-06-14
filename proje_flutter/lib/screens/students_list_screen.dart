import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/auth_provider.dart';
import '../services/api_service.dart';
import 'student_form_screen.dart';

class StudentsListScreen extends StatefulWidget {
  const StudentsListScreen({super.key});

  @override
  State<StudentsListScreen> createState() => _StudentsListScreenState();
}

class _StudentsListScreenState extends State<StudentsListScreen> {
  late ApiService api;
  late Future<List<Map<String, dynamic>>> _students;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final token = Provider.of<AuthProvider>(context, listen: false).token;
    api = ApiService(authToken: token);
    _students = api.fetchStudents();
  }

  void _refresh() {
    setState(() {
      _students = api.fetchStudents();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Öğrenciler')),
      body: FutureBuilder<List<Map<String, dynamic>>>(
        future: _students,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) return const Center(child: CircularProgressIndicator());
          if (snapshot.hasError) return Center(child: Text('Hata: ${snapshot.error}'));
          final students = snapshot.data ?? [];
          return RefreshIndicator(
            onRefresh: () async => _refresh(),
            child: ListView.builder(
              itemCount: students.length,
              itemBuilder: (context, index) {
                final s = students[index];
                return ListTile(
                  title: Text('${s['name'] ?? ''} ${s['surname'] ?? ''}'),
                  subtitle: Text(s['email'] ?? ''),
                  trailing: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      IconButton(
                        icon: const Icon(Icons.edit),
                        onPressed: () async {
                          await Navigator.of(context).push(MaterialPageRoute(builder: (_) => StudentFormScreen(student: s)));
                          _refresh();
                        },
                      ),
                      IconButton(
                        icon: const Icon(Icons.delete),
                        onPressed: () async {
                          final ok = await showDialog<bool>(
                            context: context,
                            builder: (_) => AlertDialog(
                              title: const Text('Sil'),
                              content: const Text('Bu öğrenciyi silmek istediğinizden emin misiniz?'),
                              actions: [
                                TextButton(onPressed: () => Navigator.of(context).pop(false), child: const Text('İptal')),
                                TextButton(onPressed: () => Navigator.of(context).pop(true), child: const Text('Sil')),
                              ],
                            ),
                          );
                          if (ok == true) {
                            final id = int.tryParse(students[index]['id'].toString());
                            if (id != null) {
                              await api.deleteStudent(id);
                              _refresh();
                            }
                          }
                        },
                      ),
                    ],
                  ),
                );
              },
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        child: const Icon(Icons.add),
        onPressed: () async {
          await Navigator.of(context).push(MaterialPageRoute(builder: (_) => const StudentFormScreen()));
          _refresh();
        },
      ),
    );
  }
}
