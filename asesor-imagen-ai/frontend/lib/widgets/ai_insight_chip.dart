import 'package:flutter/material.dart';
import 'package:asesor_imagen_ai/core/theme/design_tokens.dart';

// ---------------------------------------------------------------------------
// AIInsightChip — diseño Stitch validado por Erik
// Chip con fondo violeta claro #E9DDFF, texto #9466FF, icono auto_awesome
// ---------------------------------------------------------------------------

class AIInsightChip extends StatelessWidget {
  const AIInsightChip({
    super.key,
    this.label = 'AI Insights',
  });

  final String label;

  static const _chipBg = Color(0xFFE9DDFF);
  static const _chipText = Color(0xFF9466FF);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: _chipBg,
        borderRadius: BorderRadius.circular(DesignTokens.radiusFull),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.auto_awesome, size: 14, color: _chipText),
          const SizedBox(width: 5),
          Text(
            label,
            style: const TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w600,
              color: _chipText,
            ),
          ),
        ],
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// AIInsightCard — sección completa "Tu Look"
// Imagen generada + chip + análisis en párrafo + botones Guardar / Compartir
// ---------------------------------------------------------------------------

class AIInsightCard extends StatelessWidget {
  const AIInsightCard({
    super.key,
    required this.imageUrl,
    required this.insightTitle,
    required this.insightExplanation,
    required this.onSave,
    required this.onShare,
    this.isLoading = false,
  });

  final String imageUrl;
  final String insightTitle;
  final String insightExplanation;
  final VoidCallback onSave;
  final VoidCallback onShare;
  final bool isLoading;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Encabezado sección
        const Text(
          'Tu Look',
          style: TextStyle(
            fontSize: 15,
            fontWeight: FontWeight.w700,
            color: Color(0xFF111827),
          ),
        ),
        const SizedBox(height: 12),

        // Imagen generada
        AspectRatio(
          aspectRatio: 3 / 4,
          child: ClipRRect(
            borderRadius: BorderRadius.circular(DesignTokens.radiusLarge),
            child: isLoading
                ? _LoadingImage()
                : imageUrl.isNotEmpty
                    ? Image.network(
                        imageUrl,
                        fit: BoxFit.cover,
                        loadingBuilder: (context, child, progress) {
                          if (progress == null) return child;
                          return _LoadingImage();
                        },
                        errorBuilder: (_, __, ___) => _PlaceholderImage(),
                      )
                    : _PlaceholderImage(),
          ),
        ),

        const SizedBox(height: 16),

        // Chip AI Insights
        const AIInsightChip(),
        const SizedBox(height: 10),

        // Título del análisis
        if (insightTitle.isNotEmpty)
          Text(
            insightTitle,
            style: const TextStyle(
              fontSize: 15,
              fontWeight: FontWeight.w700,
              color: Color(0xFF111827),
            ),
          ),

        if (insightExplanation.isNotEmpty) ...[
          const SizedBox(height: 6),
          Text(
            insightExplanation,
            style: const TextStyle(
              fontSize: 13,
              color: Color(0xFF6B7280),
              height: 1.6,
            ),
          ),
        ],

        const SizedBox(height: 20),

        // Botones Guardar + Compartir
        Row(
          children: [
            // Guardar — outline
            Expanded(
              child: OutlinedButton.icon(
                onPressed: onSave,
                style: OutlinedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 12),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(DesignTokens.radiusLarge),
                  ),
                  side: const BorderSide(color: Color(0xFFD1D5DB), width: 1.5),
                ),
                icon: const Icon(Icons.bookmark_add_outlined,
                    size: 16, color: Color(0xFF374151)),
                label: const Text(
                  'Guardar',
                  style: TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                    color: Color(0xFF374151),
                  ),
                ),
              ),
            ),

            const SizedBox(width: 10),

            // Compartir — sólido negro
            Expanded(
              child: ElevatedButton.icon(
                onPressed: onShare,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF111827),
                  padding: const EdgeInsets.symmetric(vertical: 12),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(DesignTokens.radiusLarge),
                  ),
                  elevation: 0,
                ),
                icon: const Icon(Icons.share_outlined,
                    size: 16, color: Colors.white),
                label: const Text(
                  'Compartir',
                  style: TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                    color: Colors.white,
                  ),
                ),
              ),
            ),
          ],
        ),
      ],
    );
  }
}

class _LoadingImage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          colors: [Color(0xFFF0F4FF), Color(0xFFF5F0FF)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
      ),
      child: const Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          CircularProgressIndicator(
            color: Color(0xFF9466FF),
            strokeWidth: 2,
          ),
          SizedBox(height: 16),
          Text(
            'Generando tu look...',
            style: TextStyle(
              fontSize: 13,
              color: Color(0xFF9466FF),
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }
}

class _PlaceholderImage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          colors: [Color(0xFFF0F4FF), Color(0xFFF5F0FF)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          ShaderMask(
            shaderCallback: (bounds) => const LinearGradient(
              colors: [Color(0xFF0058BE), Color(0xFF9466FF)],
            ).createShader(bounds),
            child: const Icon(
              Icons.checkroom_outlined,
              size: 64,
              color: Colors.white,
            ),
          ),
          const SizedBox(height: 12),
          const Text(
            'Tu look aparecera aqui',
            style: TextStyle(
              fontSize: 13,
              color: Color(0xFF9CA3AF),
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }
}
