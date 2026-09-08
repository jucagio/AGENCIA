import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'package:asesor_imagen_ai/core/theme/design_tokens.dart';
import 'package:asesor_imagen_ai/features/auth/presentation/providers/auth_provider.dart';
import 'package:asesor_imagen_ai/features/wardrobe/presentation/screens/home_screen.dart';
import 'package:asesor_imagen_ai/features/auth/presentation/screens/login_screen.dart';

// ---------------------------------------------------------------------------
// SplashScreen — auto-navigates once auth state is resolved
// ---------------------------------------------------------------------------

class SplashScreen extends ConsumerStatefulWidget {
  const SplashScreen({super.key});

  static const routeName = '/splash';

  @override
  ConsumerState<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends ConsumerState<SplashScreen> {
  @override
  void initState() {
    super.initState();
    // Short delay so Supabase has time to check existing session
    Future.delayed(const Duration(milliseconds: 500), _navigate);
  }

  void _navigate() {
    if (!mounted) return;
    final status = ref.read(authProvider).status;
    if (status == AuthStatus.authenticated) {
      context.go(HomeScreen.routeName);
    } else {
      context.go(LoginScreen.routeName);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 88,
              height: 88,
              decoration: BoxDecoration(
                gradient: AppColors.primaryGradient,
                borderRadius: BorderRadius.circular(DesignTokens.radiusXLarge),
                boxShadow: [
                  BoxShadow(
                    color: AppColors.primary.withValues(alpha: 0.3),
                    blurRadius: 20,
                    offset: const Offset(0, 6),
                  ),
                ],
              ),
              child: const Icon(
                Icons.style_rounded,
                color: Colors.white,
                size: 44,
              ),
            ),
            const SizedBox(height: 24),
            Text(
              'Asesor de Imagen',
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.w700,
                  ),
            ),
            const SizedBox(height: 4),
            Text(
              'Tu estilo, potenciado con IA',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: Colors.grey[500],
                  ),
            ),
            const SizedBox(height: 48),
            SizedBox(
              width: 28,
              height: 28,
              child: CircularProgressIndicator(
                strokeWidth: 2,
                color: AppColors.primary,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
