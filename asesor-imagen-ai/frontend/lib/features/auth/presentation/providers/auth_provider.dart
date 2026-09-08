import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

// ---------------------------------------------------------------------------
// Demo credentials — allows running the app without a Supabase project
// ---------------------------------------------------------------------------

const _demoEmail = 'demo@example.com';
const _demoPassword = 'demo123';

// ---------------------------------------------------------------------------
// Auth state
// ---------------------------------------------------------------------------

enum AuthStatus { initial, loading, authenticated, unauthenticated, error }

class AuthState {
  const AuthState({
    this.status = AuthStatus.initial,
    this.errorMessage,
    this.user,
    this.isDemoUser = false,
  });

  final AuthStatus status;
  final String? errorMessage;
  final User? user;
  final bool isDemoUser;

  AuthState copyWith({
    AuthStatus? status,
    String? errorMessage,
    User? user,
    bool? isDemoUser,
  }) {
    return AuthState(
      status: status ?? this.status,
      errorMessage: errorMessage,
      user: user ?? this.user,
      isDemoUser: isDemoUser ?? this.isDemoUser,
    );
  }
}

// ---------------------------------------------------------------------------
// AuthNotifier — Riverpod 3.x Notifier
// ---------------------------------------------------------------------------

class AuthNotifier extends Notifier<AuthState> {
  @override
  AuthState build() {
    // Check existing Supabase session
    try {
      final session = Supabase.instance.client.auth.currentSession;
      if (session != null) {
        return AuthState(
          status: AuthStatus.authenticated,
          user: Supabase.instance.client.auth.currentUser,
        );
      }
    } catch (_) {
      // Supabase not initialized (demo mode)
    }
    return const AuthState(status: AuthStatus.unauthenticated);
  }

  Future<bool> login({
    required String email,
    required String password,
  }) async {
    state = state.copyWith(status: AuthStatus.loading);

    // Demo mode — bypass Supabase for demo credentials
    if (email.trim().toLowerCase() == _demoEmail && password == _demoPassword) {
      await Future.delayed(const Duration(milliseconds: 800)); // simulate
      state = const AuthState(
        status: AuthStatus.authenticated,
        isDemoUser: true,
      );
      return true;
    }

    // Real login via Supabase
    try {
      final response =
          await Supabase.instance.client.auth.signInWithPassword(
        email: email.trim(),
        password: password,
      );
      if (response.session != null) {
        state = AuthState(
          status: AuthStatus.authenticated,
          user: response.user,
        );
        return true;
      } else {
        state = state.copyWith(
          status: AuthStatus.unauthenticated,
          errorMessage: 'Credenciales incorrectas.',
        );
        return false;
      }
    } on AuthException catch (e) {
      state = state.copyWith(
        status: AuthStatus.error,
        errorMessage: e.message,
      );
      return false;
    } catch (_) {
      state = state.copyWith(
        status: AuthStatus.error,
        errorMessage: 'Error de conexion. Intenta de nuevo.',
      );
      return false;
    }
  }

  Future<void> logout() async {
    if (!state.isDemoUser) {
      try {
        await Supabase.instance.client.auth.signOut();
      } catch (_) {
        // Supabase might not be initialized
      }
    }
    state = const AuthState(status: AuthStatus.unauthenticated);
  }
}

// ---------------------------------------------------------------------------
// Providers
// ---------------------------------------------------------------------------

final authProvider = NotifierProvider<AuthNotifier, AuthState>(
  AuthNotifier.new,
);

final isAuthenticatedProvider = Provider<bool>((ref) {
  return ref.watch(authProvider).status == AuthStatus.authenticated;
});
