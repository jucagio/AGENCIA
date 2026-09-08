/// Provider de favoritos con Riverpod
///
/// FavoritesNotifier mantiene la lista y el Set de sign_ids favoritos
/// para poder determinar rápidamente si una seña es favorita.
library;

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/favorite.dart';
import '../services/api_service.dart';
import '../services/favorites_service.dart';

// ---------------------------------------------------------------------------
// Servicio
// ---------------------------------------------------------------------------

final favoritesServiceProvider = Provider<FavoritesService>((ref) {
  final apiService = ref.read(apiServiceProvider);
  return FavoritesService(apiService: apiService);
});

// ---------------------------------------------------------------------------
// Estado
// ---------------------------------------------------------------------------

class FavoritesState {
  const FavoritesState({
    this.favorites = const [],
    this.favoriteSignIds = const {},
    this.isLoading = false,
    this.error,
  });

  final List<Favorite> favorites;
  final Set<String> favoriteSignIds;
  final bool isLoading;
  final String? error;

  bool isFavorite(String signId) => favoriteSignIds.contains(signId);

  FavoritesState copyWith({
    List<Favorite>? favorites,
    Set<String>? favoriteSignIds,
    bool? isLoading,
    String? error,
  }) {
    return FavoritesState(
      favorites: favorites ?? this.favorites,
      favoriteSignIds: favoriteSignIds ?? this.favoriteSignIds,
      isLoading: isLoading ?? this.isLoading,
      error: error,
    );
  }
}

// ---------------------------------------------------------------------------
// Notifier
// ---------------------------------------------------------------------------

class FavoritesNotifier extends StateNotifier<FavoritesState> {
  FavoritesNotifier(this._service) : super(const FavoritesState());

  final FavoritesService _service;

  Future<void> loadFavorites() async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final list = await _service.listFavorites();
      final ids = list
          .where((f) => f.sign != null)
          .map((f) => f.sign!.id)
          .toSet();
      state = FavoritesState(
        favorites: list,
        favoriteSignIds: ids,
        isLoading: false,
      );
    } on Exception catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: 'No se pudieron cargar los favoritos.',
      );
    }
  }

  Future<void> addFavorite(String signId) async {
    // Optimistic update
    state = state.copyWith(
      favoriteSignIds: {...state.favoriteSignIds, signId},
    );
    try {
      await _service.addFavorite(signId);
      await loadFavorites(); // recargar para tener los datos completos
    } on Exception catch (e) {
      // Revertir el optimistic update
      final ids = Set<String>.from(state.favoriteSignIds)..remove(signId);
      state = state.copyWith(
        favoriteSignIds: ids,
        error: 'No se pudo agregar a favoritos.',
      );
    }
  }

  Future<void> removeFavorite(String signId) async {
    // Optimistic update
    final ids = Set<String>.from(state.favoriteSignIds)..remove(signId);
    final favs = state.favorites.where((f) => f.sign?.id != signId).toList();
    state = state.copyWith(favoriteSignIds: ids, favorites: favs);
    try {
      await _service.removeFavorite(signId);
    } on Exception catch (e) {
      // Revertir
      await loadFavorites();
      state = state.copyWith(error: 'No se pudo eliminar de favoritos.');
    }
  }

  void clearError() => state = state.copyWith(error: null);
}

final favoritesProvider =
    StateNotifierProvider<FavoritesNotifier, FavoritesState>((ref) {
  final service = ref.read(favoritesServiceProvider);
  return FavoritesNotifier(service);
});
