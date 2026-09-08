/// FavoritesScreen — señas guardadas por el usuario
/// GET /favorites — requiere autenticación
library;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../config/routes.dart';
import '../config/theme.dart';
import '../providers/auth_provider.dart';
import '../providers/favorites_provider.dart';
import '../widgets/loading_indicator.dart';
import '../widgets/sign_card.dart';

class FavoritesScreen extends ConsumerStatefulWidget {
  const FavoritesScreen({super.key});

  @override
  ConsumerState<FavoritesScreen> createState() => _FavoritesScreenState();
}

class _FavoritesScreenState extends ConsumerState<FavoritesScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _loadIfNeeded();
    });
  }

  void _loadIfNeeded() {
    final isAuth = ref.read(authStateProvider).valueOrNull != null;
    if (isAuth) {
      ref.read(favoritesProvider.notifier).loadFavorites();
    }
  }

  @override
  Widget build(BuildContext context) {
    final isAuth = ref.watch(authStateProvider).valueOrNull != null;
    final favState = ref.watch(favoritesProvider);

    if (!isAuth) {
      return Scaffold(
        appBar: AppBar(title: const Text('Favoritos')),
        body: _AuthRequired(),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Favoritos'),
        actions: [
          if (favState.favorites.isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(right: AppSpacing.s2),
              child: Text(
                '${favState.favorites.length}',
                style: AppTextStyles.h4.copyWith(
                  color: Theme.of(context).colorScheme.primary,
                ),
              ),
            ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () =>
            ref.read(favoritesProvider.notifier).loadFavorites(),
        child: _buildBody(context, favState),
      ),
    );
  }

  Widget _buildBody(BuildContext context, FavoritesState state) {
    if (state.isLoading && state.favorites.isEmpty) {
      return const FullScreenLoader(message: 'Cargando favoritos...');
    }

    if (state.error != null && state.favorites.isEmpty) {
      return ErrorState(
        message: state.error!,
        onRetry: () =>
            ref.read(favoritesProvider.notifier).loadFavorites(),
      );
    }

    if (state.favorites.isEmpty) {
      return EmptyState(
        message: 'Aún no tienes señas guardadas.\nExplora el catálogo y guarda las que quieras aprender.',
        icon: Icons.favorite_border_rounded,
        action: () => context.go(AppRoutes.home),
        actionLabel: 'Explorar señas',
      );
    }

    final signs = state.favorites
        .where((f) => f.sign != null)
        .map((f) => f.sign!)
        .toList();

    return GridView.builder(
      padding: const EdgeInsets.all(AppSpacing.s4),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 12,
        mainAxisSpacing: 12,
        childAspectRatio: 0.72,
      ),
      itemCount: signs.length,
      itemBuilder: (context, i) => SignCard(sign: signs[i]),
    );
  }
}

class _AuthRequired extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.s8),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              Icons.favorite_border_rounded,
              size: 72,
              color: Theme.of(context).colorScheme.onSurface.withAlpha(51),
            ),
            const SizedBox(height: AppSpacing.s4),
            Text(
              'Inicia sesión para guardar tus señas favoritas',
              textAlign: TextAlign.center,
              style: AppTextStyles.body.copyWith(
                color: Theme.of(context).colorScheme.onSurface.withAlpha(153),
              ),
            ),
            const SizedBox(height: AppSpacing.s6),
            ElevatedButton(
              onPressed: () => context.go(AppRoutes.login),
              child: const Text('Iniciar sesión'),
            ),
            const SizedBox(height: AppSpacing.s3),
            OutlinedButton(
              onPressed: () => context.go(AppRoutes.register),
              child: const Text('Crear cuenta gratis'),
            ),
          ],
        ),
      ),
    );
  }
}
