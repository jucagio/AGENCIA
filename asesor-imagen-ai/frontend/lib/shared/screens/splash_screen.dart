import 'package:flutter/material.dart';

// TODO(Erik): Aplicar splash con logo y animación de entrada.
// El router redirige desde /splash automáticamente según estado de auth.
class SplashScreen extends StatelessWidget {
  const SplashScreen({super.key});

  static const routeName = '/splash';

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: CircularProgressIndicator(),
      ),
    );
  }
}
