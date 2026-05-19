import 'package:flutter/material.dart';

// TODO(Brook): Implementar feed de recomendaciones con filtros de ocasión/estilo.
// TODO(Sasha): Integrar con endpoint GET /recommendations.
// TODO(Erik): Aplicar diseño visual — ver Figma frame: Recommendations.
class RecommendationsScreen extends StatelessWidget {
  const RecommendationsScreen({super.key});

  static const routeName = '/recommendations';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Recomendaciones')),
      body: const Center(child: Text('RecommendationsScreen — placeholder')),
    );
  }
}
