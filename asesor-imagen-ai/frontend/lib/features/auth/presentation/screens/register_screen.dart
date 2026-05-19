import 'package:flutter/material.dart';

// TODO(Brook): Implementar formulario de registro con validación.
// TODO(Erik): Aplicar diseño visual — ver Figma frame: Auth/Register.
class RegisterScreen extends StatelessWidget {
  const RegisterScreen({super.key});

  static const routeName = '/register';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Crear cuenta')),
      body: const Center(child: Text('RegisterScreen — placeholder')),
    );
  }
}
