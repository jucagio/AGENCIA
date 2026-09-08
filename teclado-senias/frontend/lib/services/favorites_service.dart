/// Servicio de favoritos — wrappea /api/v1/favorites/*
/// Todos los endpoints requieren autenticación.
library;

import '../models/favorite.dart';
import 'api_service.dart';

class FavoritesService {
  FavoritesService({required ApiService apiService}) : _api = apiService;

  final ApiService _api;

  // ---------------------------------------------------------------------------
  // GET /favorites
  // ---------------------------------------------------------------------------

  Future<List<Favorite>> listFavorites() async {
    final data = await _api.get('/favorites', requiresAuth: true);
    final list = data as List<dynamic>;
    return list
        .map((f) => Favorite.fromJson(f as Map<String, dynamic>))
        .toList();
  }

  // ---------------------------------------------------------------------------
  // POST /favorites/:sign_id
  // ---------------------------------------------------------------------------

  Future<void> addFavorite(String signId) async {
    await _api.post('/favorites/$signId', requiresAuth: true);
  }

  // ---------------------------------------------------------------------------
  // DELETE /favorites/:sign_id
  // ---------------------------------------------------------------------------

  Future<void> removeFavorite(String signId) async {
    await _api.delete('/favorites/$signId', requiresAuth: true);
  }
}
