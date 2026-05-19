import 'package:flutter/material.dart';

// TODO(Brook): Implementar perfil con datos del usuario, medidas corporales y suscripción.
// TODO(Erik): Aplicar diseño visual — ver Figma frame: Profile.
class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  static const routeName = '/profile';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Mi Perfil')),
      body: const Center(child: Text('ProfileScreen — placeholder')),
    );
  }
}
