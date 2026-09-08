import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'package:asesor_imagen_ai/features/auth/presentation/providers/auth_provider.dart'
    as auth_prov;
import 'package:asesor_imagen_ai/features/auth/presentation/screens/login_screen.dart';
import 'package:asesor_imagen_ai/features/auth/presentation/screens/register_screen.dart';
import 'package:asesor_imagen_ai/features/wardrobe/presentation/screens/home_screen.dart';
import 'package:asesor_imagen_ai/shared/screens/onboarding_screen.dart';
import 'package:asesor_imagen_ai/shared/screens/splash_screen.dart';

// ---------------------------------------------------------------------------
// Router provider
// Relies on authProvider (Riverpod 3.x) instead of Supabase stream directly.
// This makes the router safe when Supabase is not initialized (demo mode).
// ---------------------------------------------------------------------------

final routerProvider = Provider.autoDispose<GoRouter>((ref) {
  // Rebuild router whenever auth state changes
  ref.watch(auth_prov.authProvider);

  return GoRouter(
    initialLocation: SplashScreen.routeName,
    debugLogDiagnostics: false,
    redirect: (BuildContext context, GoRouterState state) {
      final authState = ref.read(auth_prov.authProvider);

      // Still loading — stay on splash
      if (authState.status == auth_prov.AuthStatus.initial ||
          authState.status == auth_prov.AuthStatus.loading) {
        return SplashScreen.routeName;
      }

      final isAuthenticated =
          authState.status == auth_prov.AuthStatus.authenticated;
      final currentPath = state.matchedLocation;

      final publicRoutes = {
        SplashScreen.routeName,
        OnboardingScreen.routeName,
        LoginScreen.routeName,
        RegisterScreen.routeName,
      };

      final isOnPublicRoute = publicRoutes.contains(currentPath);

      if (!isAuthenticated && !isOnPublicRoute) {
        return LoginScreen.routeName;
      }

      if (isAuthenticated && isOnPublicRoute) {
        return HomeScreen.routeName;
      }

      return null;
    },
    routes: [
      GoRoute(
        path: SplashScreen.routeName,
        builder: (context, state) => const SplashScreen(),
      ),
      GoRoute(
        path: OnboardingScreen.routeName,
        builder: (context, state) => const OnboardingScreen(),
      ),
      GoRoute(
        path: LoginScreen.routeName,
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: RegisterScreen.routeName,
        builder: (context, state) => const RegisterScreen(),
      ),
      GoRoute(
        path: HomeScreen.routeName,
        builder: (context, state) => const HomeScreen(),
      ),
    ],
  );
});
