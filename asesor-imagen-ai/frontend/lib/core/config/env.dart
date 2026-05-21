import 'package:flutter/foundation.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

/// Centraliza el acceso a variables de entorno cargadas desde .env
/// En modo debug, los valores placeholder son aceptados (modo demo).
/// En modo release, lanza [StateError] si una variable requerida no está configurada.
class Env {
  Env._();

  // Supabase
  static String get supabaseUrl => _get('SUPABASE_URL', 'https://placeholder.supabase.co');
  static String get supabaseAnonKey => _get('SUPABASE_ANON_KEY', 'placeholder-anon-key');

  // API backend — Railway staging o producción
  // Sasha entrega la URL cuando esté disponible en Railway.
  static String get apiBaseUrl => _get('API_BASE_URL', 'http://localhost:8000');

  static bool get isDemoMode {
    final url = dotenv.env['API_BASE_URL'] ?? '';
    return url.isEmpty ||
        url.contains('your-') ||
        url.contains('placeholder') ||
        url == 'http://localhost:8000';
  }

  static String _get(String key, String fallback) {
    final value = dotenv.env[key];
    if (value == null || value.isEmpty) {
      if (kDebugMode) {
        debugPrint('[Env] $key no encontrado — usando fallback: $fallback');
        return fallback;
      }
      throw StateError('Variable de entorno requerida no encontrada: $key');
    }
    // Detect placeholder values
    if (value.contains('your-') || value.contains('placeholder')) {
      if (kDebugMode) {
        debugPrint('[Env] $key tiene valor placeholder — usando fallback: $fallback');
        return fallback;
      }
    }
    return value;
  }
}
