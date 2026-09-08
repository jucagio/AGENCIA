import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

final router = GoRouter(
  initialLocation: '/login',
  routes: [
    GoRoute(
      path: '/login',
      name: 'login',
      pageBuilder: (context, state) => MaterialPage(
        child: Placeholder(), // LoginScreen (import when created)
      ),
    ),
    GoRoute(
      path: '/register',
      name: 'register',
      pageBuilder: (context, state) => MaterialPage(
        child: Placeholder(), // RegisterScreen
      ),
    ),
    GoRoute(
      path: '/home',
      name: 'home',
      pageBuilder: (context, state) => MaterialPage(
        child: Placeholder(), // HomeScreen
      ),
    ),
    GoRoute(
      path: '/search',
      name: 'search',
      pageBuilder: (context, state) => MaterialPage(
        child: Placeholder(), // SearchScreen
      ),
    ),
    GoRoute(
      path: '/sign/:id',
      name: 'sign_detail',
      pageBuilder: (context, state) {
        final id = state.pathParameters['id']!;
        return MaterialPage(
          child: Placeholder(), // SignDetailScreen(signId: id)
        );
      },
    ),
    GoRoute(
      path: '/favorites',
      name: 'favorites',
      pageBuilder: (context, state) => MaterialPage(
        child: Placeholder(), // FavoritesScreen
      ),
    ),
    GoRoute(
      path: '/settings',
      name: 'settings',
      pageBuilder: (context, state) => MaterialPage(
        child: Placeholder(), // SettingsScreen
      ),
    ),
  ],
  redirect: (context, state) {
    // TODO: Check auth state and redirect accordingly
    return null;
  },
);
