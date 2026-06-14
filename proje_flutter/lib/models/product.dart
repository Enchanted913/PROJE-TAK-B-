class Product {
  final int id;
  final String title;
  final String description;
  final double price;

  Product({required this.id, required this.title, required this.description, required this.price});

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['id'] is int ? json['id'] : int.parse(json['id'].toString()),
      title: json['title'] ?? json['name'] ?? '',
      description: json['description'] ?? '',
      price: (json['price'] != null) ? double.parse(json['price'].toString()) : 0.0,
    );
  }
}
