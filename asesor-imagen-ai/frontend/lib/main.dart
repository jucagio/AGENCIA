import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

import 'package:asesor_imagen_ai/core/routing/router.dart';
import 'package:asesor_imagen_ai/core/theme/app_theme.dart';
import 'package:asesor_imagen_ai/core/config/supabase_config.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Load .env file for local development (dotenv values are lowest priority).
  // In production APK builds (--dart-define-from-file), this file may not
  // exist — silently skip loading if missing.
  try {
    await dotenv.load(fileName: '.env');
  } catch (_) {
    // .env not present in the assets bundle — expected in production builds
    // where values come from --dart-define-from-file instead.
  }

  // Initialize Supabase via SupabaseConfig.
  // Priority: dart-define > dotenv > demo mode fallback.
  await SupabaseConfig.initialize();

  runApp(
    const ProviderScope(
      child: AsesorImagenApp(),
    ),
  );
}

/// Root widget. Reads [routerProvider] and applies [AppTheme].
class AsesorImagenApp extends ConsumerWidget {
  const AsesorImagenApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider);

    return MaterialApp.router(
      title: 'Asesor de Imagen AI',
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
      themeMode: ThemeMode.system,
      routerConfig: router,
      debugShowCheckedModeBanner: false,
    );
  }
}
