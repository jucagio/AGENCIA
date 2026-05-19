import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

import 'package:asesor_imagen_ai/features/auth/presentation/screens/login_screen.dart';
import 'package:asesor_imagen_ai/features/auth/presentation/screens/register_screen.dart';
import 'package:asesor_imagen_ai/features/recommendations/presentation/screens/recommendations_screen.dart';
import 'package:asesor_imagen_ai/features/try_on/presentation/screens/try_on_screen.dart';
import 'package:asesor_imagen_ai/features/wardrobe/presentation/screens/home_screen.dart';
import 'package:asesor_imagen_ai/features/wardrobe/presentation/screens/wardrobe_screen.dart';
import 'package:asesor_imagen_ai/shared/screens/onboarding_screen.dart';
import 'package:asesor_imagen_ai/shared/screens/profile_screen.dart';
import 'package:asesor_imagen_ai/shared/screens/splash_screen.dart';

// ---------------------------------------------------------------------------
// Auth state provider — escucha cambios de sesión de Supabase en tiempo real
// ---------------------------------------------------------------------------

/// Retorna la sesión activa o null si el usuario no está autenticado.
/// Provider manual — no requiere riverpod_generator ni build_runner.
final authStateProvider = StreamProvider.autoDispose<AuthState>((ref) {
  return Supabase.instance.client.auth.onAuthStateChange;
});

// ---------------------------------------------------------------------------
// Router provider
// ---------------------------------------------------------------------------

final routerProvider = Provider.autoDispose<GoRouter>((ref) {
  final authStateAsync = ref.watch(authStateProvider);

  return GoRouter(
    initialLocation: SplashScreen.routeName,
    debugLogDiagnostics: true,
    redirect: (BuildContext context, GoRouterState state) {
      // Mientras carga el estado de auth → quedarse en splash
      if (authStateAsync.isLoading || authStateAsync.hasError) {
        return SplashScreen.routeName;
      }

      final session = Supabase.instance.client.auth.currentSession;
      final isAuthenticated = session != null;
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

      return null; // Sin redirección
    },
    routes: [
      // -----------------------------------------------------------------------
      // Rutas públicas
      // -----------------------------------------------------------------------
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

      // -----------------------------------------------------------------------
      // Rutas protegidas
      // -----------------------------------------------------------------------
      GoRoute(
        path: HomeScreen.routeName,
        builder: (context, state) => const HomeScreen(),
      ),
      GoRoute(
        path: WardrobeScreen.routeName,
        builder: (context, state) => const WardrobeScreen(),
      ),
      GoRoute(
        path: TryOnScreen.routeName,
        builder: (context, state) => const TryOnScreen(),
      ),
      GoRoute(
        path: RecommendationsScreen.routeName,
        builder: (context, state) => const RecommendationsScreen(),
      ),
      GoRoute(
        path: ProfileScreen.routeName,
        builder: (context, state) => const ProfileScreen(),
      ),
    ],
  );
});
