import 'package:flutter/material.dart';

// TODO(Brook): Implementar grid de prendas con filtros por categoría.
// TODO(Erik): Aplicar diseño visual — ver Figma frame: Wardrobe.
class WardrobeScreen extends StatelessWidget {
  const WardrobeScreen({super.key});

  static const routeName = '/wardrobe';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Mi Armario')),
      body: const Center(child: Text('WardrobeScreen — placeholder')),
    );
  }
}
