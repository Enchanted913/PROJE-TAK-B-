class Project {
  final int id;
  final String title;
  final String description;
  final String status;
  final List<dynamic> students;

  Project({required this.id, required this.title, required this.description, required this.status, required this.students});

  factory Project.fromJson(Map<String, dynamic> json) {
    return Project(
      id: json['id'] is int ? json['id'] : int.parse(json['id'].toString()),
      title: json['title'] ?? '',
      description: json['description'] ?? '',
      status: json['status'] ?? 'new',
      students: json['students'] is List ? json['students'] : [],
    );
  }
}
