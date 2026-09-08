/// Modelo de favorito — mapea el schema Favorite del backend de Sasha
library;

import 'package:equatable/equatable.dart';
import 'sign.dart';

class Favorite extends Equatable {
  const Favorite({
    required this.id,
    this.sign,
    this.createdAt,
  });

  final String id;
  final Sign? sign;
  final DateTime? createdAt;

  factory Favorite.fromJson(Map<String, dynamic> json) {
    return Favorite(
      id: json['id'] as String,
      sign: json['sign'] != null
          ? Sign.fromJson(json['sign'] as Map<String, dynamic>)
          : null,
      createdAt: json['created_at'] != null
          ? DateTime.tryParse(json['created_at'] as String)
          : null,
    );
  }

  Map<String, dynamic> toJson() => {
        'id': id,
        'sign': sign?.toJson(),
        'created_at': createdAt?.toIso8601String(),
      };

  @override
  List<Object?> get props => [id, sign, createdAt];
}
