import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AuthService {
  final _supabase = Supabase.instance.client;

  Future<void> register(String email, String password, String name) async {
    try {
      final response = await _supabase.auth.signUp(
        email: email,
        password: password,
        data: {'name': name},
      );
      if (response.user == null) {
        throw Exception('Registro fallido');
      }
    } catch (e) {
      rethrow;
    }
  }

  Future<void> login(String email, String password) async {
    try {
      final response = await _supabase.auth.signInWithPassword(
        email: email,
        password: password,
      );
      if (response.user == null) {
        throw Exception('Credenciales inválidas');
      }
      // Save token locally
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('auth_token', response.session?.accessToken ?? '');
    } catch (e) {
      rethrow;
    }
  }

  Future<void> logout() async {
    try {
      await _supabase.auth.signOut();
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove('auth_token');
    } catch (e) {
      rethrow;
    }
  }

  Future<bool> isLoggedIn() async {
    final session = _supabase.auth.currentSession;
    return session != null;
  }

  User? getCurrentUser() {
    return _supabase.auth.currentUser;
  }
}
