import 'package:flutter/material.dart';

// TODO(Brook): Implementar shell con BottomNavigationBar para las secciones principales.
// TODO(Erik): Aplicar diseño visual — ver Figma frame: Home/Shell.
class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  static const routeName = '/home';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Asesor de Imagen')),
      body: const Center(child: Text('HomeScreen — placeholder')),
    );
  }
}
