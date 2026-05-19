import 'package:flutter/material.dart';

// TODO(Brook): Implementar flujo de onboarding con PageView.
// TODO(Erik): Aplicar diseño visual — ver Figma frame: Onboarding.
class OnboardingScreen extends StatelessWidget {
  const OnboardingScreen({super.key});

  static const routeName = '/onboarding';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Bienvenido')),
      body: const Center(child: Text('OnboardingScreen — placeholder')),
    );
  }
}
