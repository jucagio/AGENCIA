import 'package:flutter_dotenv/flutter_dotenv.dart';

/// Centraliza el acceso a variables de entorno cargadas desde .env
/// Lanza [StateError] si una variable requerida no está configurada.
class Env {
  Env._();

  static String get supabaseUrl => _required('SUPABASE_URL');
  static String get supabaseAnonKey => _required('SUPABASE_ANON_KEY');
  static String get apiBaseUrl => _required('API_BASE_URL');

  static String _required(String key) {
    final value = dotenv.env[key];
    if (value == null || value.isEmpty) {
      throw StateError('Variable de entorno requerida no encontrada: $key');
    }
    return value;
  }
}
