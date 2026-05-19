import 'package:flutter/material.dart';

// TODO(Brook): Implementar formulario de login con validación.
// TODO(Erik): Aplicar diseño visual — ver Figma frame: Auth/Login.
class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  static const routeName = '/login';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Iniciar sesión')),
      body: const Center(child: Text('LoginScreen — placeholder')),
    );
  }
}
