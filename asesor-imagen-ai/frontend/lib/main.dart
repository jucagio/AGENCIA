import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

import 'package:asesor_imagen_ai/core/routing/router.dart';
import 'package:asesor_imagen_ai/core/theme/app_theme.dart';
import 'package:asesor_imagen_ai/core/config/env.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Load environment variables
  await dotenv.load(fileName: '.env');

  // Initialize Supabase
  await Supabase.initialize(
    url: Env.supabaseUrl,
    anonKey: Env.supabaseAnonKey,
  );

  runApp(
    // ProviderScope wraps the entire app — required for Riverpod
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
