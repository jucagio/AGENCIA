import 'package:flutter/material.dart';

// TODO(Brook): Implementar selector de prenda + cámara + visualización del try-on.
// TODO(Sasha): Integrar con endpoint POST /try-on/generate — requiere multipart form.
// TODO(Erik): Aplicar diseño visual — ver Figma frame: TryOn.
class TryOnScreen extends StatelessWidget {
  const TryOnScreen({super.key});

  static const routeName = '/try-on';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Pruébatelo')),
      body: const Center(child: Text('TryOnScreen — placeholder')),
    );
  }
}
