import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:logger/logger.dart';

import 'package:asesor_imagen_ai/core/network/dio_client.dart';

// ---------------------------------------------------------------------------
// Model
// ---------------------------------------------------------------------------

class WardrobeItem {
  const WardrobeItem({
    required this.id,
    required this.name,
    required this.type,
    this.color,
    this.imageUrl,
    this.createdAt,
  });

  final String id;
  final String name;
  final String type;
  final String? color;
  final String? imageUrl;
  final DateTime? createdAt;

  factory WardrobeItem.fromJson(Map<String, dynamic> json) {
    return WardrobeItem(
      id: json['id']?.toString() ?? '',
      name: json['name']?.toString() ?? '',
      type: json['type']?.toString() ?? '',
      color: json['color']?.toString(),
      imageUrl: json['image_url']?.toString(),
      createdAt: json['created_at'] != null
          ? DateTime.tryParse(json['created_at'].toString())
          : null,
    );
  }

  static List<WardrobeItem> demoItems() => [
        const WardrobeItem(id: 'demo-1', name: 'Camisa Blanca', type: 'shirt', color: '#E8E8E8'),
        const WardrobeItem(id: 'demo-2', name: 'Pantalon Azul', type: 'pants', color: '#1E3A5F'),
        const WardrobeItem(id: 'demo-3', name: 'Vestido Negro', type: 'dress', color: '#121212'),
        const WardrobeItem(id: 'demo-4', name: 'Blazer Gris', type: 'jacket', color: '#6B7280'),
        const WardrobeItem(id: 'demo-5', name: 'Falda Floral', type: 'skirt', color: '#EC4899'),
      ];
}

// ---------------------------------------------------------------------------
// Repository
// ---------------------------------------------------------------------------

class WardrobeRepository {
  WardrobeRepository({DioClient? dioClient})
      : _dioClient = dioClient ?? DioClient();

  final DioClient _dioClient;
  final _logger = Logger();

  Future<List<WardrobeItem>> getItems() async {
    try {
      final response = await _dioClient.dio.get('/api/v1/wardrobe');
      final data = response.data as List<dynamic>? ?? [];
      return data
          .map((e) => WardrobeItem.fromJson(e as Map<String, dynamic>))
          .toList();
    } on DioException catch (e) {
      _logger.w('[WardrobeRepo] API unavailable, using demo items: ${e.message}');
      return WardrobeItem.demoItems();
    } catch (e) {
      _logger.e('[WardrobeRepo] Unexpected error', error: e);
      return WardrobeItem.demoItems();
    }
  }

  Future<WardrobeItem> createItem({
    required String name,
    required String type,
    String? color,
    String? imageUrl,
  }) async {
    try {
      final response = await _dioClient.dio.post(
        '/api/v1/wardrobe',
        data: {
          'name': name,
          'type': type,
          if (color != null) 'color': color,
          if (imageUrl != null) 'image_url': imageUrl,
        },
      );
      return WardrobeItem.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      _logger.w('[WardrobeRepo] Create failed, using local item: ${e.message}');
      return WardrobeItem(
        id: 'local-${DateTime.now().millisecondsSinceEpoch}',
        name: name,
        type: type,
        color: color,
        imageUrl: imageUrl,
      );
    }
  }

  Future<void> deleteItem(String id) async {
    try {
      await _dioClient.dio.delete('/api/v1/wardrobe/$id');
    } on DioException catch (e) {
      _logger.w('[WardrobeRepo] Delete skipped: ${e.message}');
    }
  }
}

// ---------------------------------------------------------------------------
// Riverpod 3.x — AsyncNotifier
// ---------------------------------------------------------------------------

final wardrobeRepositoryProvider = Provider<WardrobeRepository>((ref) {
  return WardrobeRepository();
});

class WardrobeNotifier extends AsyncNotifier<List<WardrobeItem>> {
  @override
  Future<List<WardrobeItem>> build() async {
    return ref.read(wardrobeRepositoryProvider).getItems();
  }

  Future<void> fetchItems() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(
      () => ref.read(wardrobeRepositoryProvider).getItems(),
    );
  }

  Future<void> addItem({
    required String name,
    required String type,
    String? color,
    String? imageUrl,
  }) async {
    final newItem = await ref.read(wardrobeRepositoryProvider).createItem(
          name: name,
          type: type,
          color: color,
          imageUrl: imageUrl,
        );
    state.whenData((items) {
      state = AsyncValue.data([...items, newItem]);
    });
  }

  Future<void> deleteItem(String id) async {
    await ref.read(wardrobeRepositoryProvider).deleteItem(id);
    state.whenData((items) {
      state = AsyncValue.data(items.where((i) => i.id != id).toList());
    });
  }
}

final wardrobeProvider =
    AsyncNotifierProvider<WardrobeNotifier, List<WardrobeItem>>(
  WardrobeNotifier.new,
);
