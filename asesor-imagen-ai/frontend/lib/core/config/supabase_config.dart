import 'package:flutter/foundation.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

/// Centralized Supabase initialization and configuration.
///
/// Priority order for env values:
///   1. --dart-define-from-file (baked into binary at build time — production)
///   2. flutter_dotenv (.env file — development/debug)
///   3. defaultValue fallback (demo mode)
///
/// Build commands:
///   Dev (demo):   flutter run
///   Dev (local):  flutter run --dart-define-from-file=.env.development.json
///   Production:   flutter build apk --dart-define-from-file=.env.production.json --release
class SupabaseConfig {
  SupabaseConfig._();

  // ---------------------------------------------------------------------------
  // Env resolution — dart-define > dotenv > fallback
  // ---------------------------------------------------------------------------

  static String get supabaseUrl {
    // dart-define takes priority (baked in at build time)
    const dartDefine = String.fromEnvironment(
      'SUPABASE_URL',
      defaultValue: '',
    );
    if (dartDefine.isNotEmpty && !_isPlaceholder(dartDefine)) return dartDefine;

    // dotenv fallback (local dev)
    final dotenvValue = _dotenvGet('SUPABASE_URL');
    if (dotenvValue != null) return dotenvValue;

    return 'https://placeholder.supabase.co';
  }

  static String get supabaseAnonKey {
    const dartDefine = String.fromEnvironment(
      'SUPABASE_ANON_KEY',
      defaultValue: '',
    );
    if (dartDefine.isNotEmpty && !_isPlaceholder(dartDefine)) return dartDefine;

    final dotenvValue = _dotenvGet('SUPABASE_ANON_KEY');
    if (dotenvValue != null) return dotenvValue;

    return '';
  }

  static String get apiBaseUrl {
    const dartDefine = String.fromEnvironment(
      'API_BASE_URL',
      defaultValue: '',
    );
    if (dartDefine.isNotEmpty && !_isPlaceholder(dartDefine)) return dartDefine;

    final dotenvValue = _dotenvGet('API_BASE_URL');
    if (dotenvValue != null) return dotenvValue;

    // Android emulator localhost — safe default for local dev
    return 'http://10.0.2.2:8000';
  }

  /// True when Supabase credentials are placeholder / not configured.
  static bool get isDemoMode {
    return _isPlaceholder(supabaseUrl) ||
        supabaseUrl.isEmpty ||
        supabaseAnonKey.isEmpty;
  }

  // ---------------------------------------------------------------------------
  // Supabase initialization
  // ---------------------------------------------------------------------------

  /// Call once in [main] before [runApp].
  ///
  /// Uses PKCE flow — the recommended and default auth flow for mobile apps.
  /// Falls back to demo mode silently when credentials are missing.
  static Future<void> initialize() async {
    if (isDemoMode) {
      debugPrint(
        '[SupabaseConfig] Credentials missing or placeholder — running in demo mode.',
      );
      return;
    }

    try {
      await Supabase.initialize(
        url: supabaseUrl,
        anonKey: supabaseAnonKey,
        authOptions: const FlutterAuthClientOptions(
          authFlowType: AuthFlowType.pkce,
        ),
        // Realtime is enabled by default — no need to opt in
        // Storage is available via Supabase.instance.client.storage
      );
      debugPrint('[SupabaseConfig] Supabase initialized — url: $supabaseUrl');
    } catch (e, st) {
      debugPrint('[SupabaseConfig] Supabase init failed: $e\n$st');
      // Non-fatal: app continues in demo mode
    }
  }

  // ---------------------------------------------------------------------------
  // Supabase Storage helpers
  // ---------------------------------------------------------------------------

  /// Public URL for a file in the [wardrobe] bucket.
  /// Works with both Supabase Cloud and self-hosted (local dev).
  static String wardrobePublicUrl(String path) {
    if (isDemoMode) return '';
    return Supabase.instance.client.storage
        .from('wardrobe')
        .getPublicUrl(path);
  }

  /// Public URL for a file in the [try-ons] bucket.
  static String tryOnPublicUrl(String path) {
    if (isDemoMode) return '';
    return Supabase.instance.client.storage
        .from('try-ons')
        .getPublicUrl(path);
  }

  // ---------------------------------------------------------------------------
  // Private helpers
  // ---------------------------------------------------------------------------

  static bool _isPlaceholder(String value) {
    return value.contains('placeholder') || value.contains('your-');
  }

  /// Safe dotenv access — returns null if dotenv is not loaded or key missing.
  static String? _dotenvGet(String key) {
    try {
      final value = dotenv.env[key];
      if (value == null || value.isEmpty || _isPlaceholder(value)) return null;
      return value;
    } catch (_) {
      return null;
    }
  }
}
