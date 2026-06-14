class Task {
  final int id;
  final String title;
  final String description;
  final String status;
  final int projectId;
  final int points;

  Task({required this.id, required this.title, required this.description, required this.status, required this.projectId, required this.points});

  factory Task.fromJson(Map<String, dynamic> json) {
    return Task(
      id: json['id'] is int ? json['id'] : int.parse(json['id'].toString()),
      title: json['title'] ?? '',
      description: json['description'] ?? '',
      status: json['status'] ?? 'pending',
      projectId: json['project_id'] is int ? json['project_id'] : int.parse(json['project_id'].toString()),
      points: json['points'] is int ? json['points'] : int.tryParse(json['points']?.toString() ?? '0') ?? 0,
    );
  }
}
