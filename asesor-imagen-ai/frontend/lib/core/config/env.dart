import 'package:asesor_imagen_ai/core/config/supabase_config.dart';

/// Centraliza el acceso a variables de entorno.
///
/// Delegado a [SupabaseConfig] que resuelve con prioridad:
///   1. --dart-define-from-file (producción, baked en binario)
///   2. flutter_dotenv (.env, desarrollo local)
///   3. Fallback seguro (modo demo)
///
/// Mantener esta clase para retrocompatibilidad con repos existentes.
class Env {
  Env._();

  static String get supabaseUrl => SupabaseConfig.supabaseUrl;
  static String get supabaseAnonKey => SupabaseConfig.supabaseAnonKey;
  static String get apiBaseUrl => SupabaseConfig.apiBaseUrl;
  static bool get isDemoMode => SupabaseConfig.isDemoMode;
}
