import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import 'package:asesor_imagen_ai/core/theme/design_tokens.dart';

// ---------------------------------------------------------------------------
// UploadZone — diseño Stitch validado por Erik
// Área rectangular con borde punteado (2px dashed #C6C6CD)
// Icono cámara centrado + texto descriptivo
// Click → bottom sheet para elegir cámara o galería
// ---------------------------------------------------------------------------

class UploadZone extends StatelessWidget {
  const UploadZone({
    super.key,
    required this.photoPath,
    required this.onPhotoSelected,
    this.label = 'Tu Foto',
    this.hint = 'Sube tu foto (de frente y buena luz)',
  });

  final String? photoPath;
  final ValueChanged<String> onPhotoSelected;
  final String label;
  final String hint;

  static const _dashedColor = Color(0xFFC6C6CD);
  static const _primaryBlue = Color(0xFF0058BE);

  Future<void> _pickImage(BuildContext context, ImageSource source) async {
    final picker = ImagePicker();
    final picked = await picker.pickImage(source: source, imageQuality: 85);
    if (picked != null) onPhotoSelected(picked.path);
  }

  void _showSourcePicker(BuildContext context) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(
          top: Radius.circular(DesignTokens.radiusXLarge),
        ),
      ),
      builder: (ctx) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const SizedBox(height: 12),
            Container(
              width: 40,
              height: 4,
              decoration: BoxDecoration(
                color: Colors.grey[300],
                borderRadius: BorderRadius.circular(2),
              ),
            ),
            const SizedBox(height: 16),
            ListTile(
              leading: const Icon(Icons.camera_alt_outlined),
              title: const Text('Camara'),
              onTap: () {
                Navigator.pop(ctx);
                _pickImage(context, ImageSource.camera);
              },
            ),
            ListTile(
              leading: const Icon(Icons.photo_library_outlined),
              title: const Text('Galeria'),
              onTap: () {
                Navigator.pop(ctx);
                _pickImage(context, ImageSource.gallery);
              },
            ),
            const SizedBox(height: 12),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Label
        Text(
          label,
          style: const TextStyle(
            fontSize: 13,
            fontWeight: FontWeight.w600,
            color: Color(0xFF374151),
          ),
        ),
        const SizedBox(height: 8),

        // Drop zone
        GestureDetector(
          onTap: () => _showSourcePicker(context),
          child: Container(
            height: 180,
            width: double.infinity,
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(DesignTokens.radiusMedium),
            ),
            child: CustomPaint(
              painter: _DashedBorderPainter(
                color: _dashedColor,
                radius: DesignTokens.radiusMedium,
                strokeWidth: 2,
                dashWidth: 6,
                dashSpace: 4,
              ),
              child: photoPath != null
                  ? _buildPhotoPreview(context)
                  : _buildEmptyState(context),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildEmptyState(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Container(
          width: 48,
          height: 48,
          decoration: BoxDecoration(
            color: const Color(0xFFF0F4FF),
            borderRadius: BorderRadius.circular(DesignTokens.radiusMedium),
          ),
          child: const Icon(
            Icons.camera_alt_outlined,
            color: _primaryBlue,
            size: 22,
          ),
        ),
        const SizedBox(height: 12),
        Text(
          hint,
          textAlign: TextAlign.center,
          style: const TextStyle(
            fontSize: 12,
            color: Color(0xFF9CA3AF),
            height: 1.4,
          ),
        ),
      ],
    );
  }

  Widget _buildPhotoPreview(BuildContext context) {
    return Stack(
      fit: StackFit.expand,
      children: [
        ClipRRect(
          borderRadius: BorderRadius.circular(DesignTokens.radiusMedium),
          child: Image.file(
            File(photoPath!),
            fit: BoxFit.cover,
          ),
        ),
        // Edit overlay
        Positioned(
          bottom: 8,
          right: 8,
          child: Material(
            color: Colors.white,
            borderRadius: BorderRadius.circular(DesignTokens.radiusFull),
            elevation: 2,
            child: InkWell(
              onTap: () => _showSourcePicker(context),
              borderRadius: BorderRadius.circular(DesignTokens.radiusFull),
              child: const Padding(
                padding: EdgeInsets.all(8),
                child: Icon(Icons.edit_outlined, size: 16, color: _primaryBlue),
              ),
            ),
          ),
        ),
      ],
    );
  }
}

// ---------------------------------------------------------------------------
// Painter para borde punteado — sin dependencias externas
// ---------------------------------------------------------------------------

class _DashedBorderPainter extends CustomPainter {
  const _DashedBorderPainter({
    required this.color,
    required this.radius,
    required this.strokeWidth,
    required this.dashWidth,
    required this.dashSpace,
  });

  final Color color;
  final double radius;
  final double strokeWidth;
  final double dashWidth;
  final double dashSpace;

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..strokeWidth = strokeWidth
      ..style = PaintingStyle.stroke;

    final path = Path()
      ..addRRect(RRect.fromRectAndRadius(
        Rect.fromLTWH(strokeWidth / 2, strokeWidth / 2,
            size.width - strokeWidth, size.height - strokeWidth),
        Radius.circular(radius),
      ));

    final dashPath = _createDashPath(path, dashWidth, dashSpace);
    canvas.drawPath(dashPath, paint);
  }

  Path _createDashPath(Path source, double dashWidth, double dashSpace) {
    final dashPath = Path();
    final metrics = source.computeMetrics();
    for (final metric in metrics) {
      double distance = 0;
      while (distance < metric.length) {
        final start = distance;
        final end = (distance + dashWidth).clamp(0.0, metric.length);
        dashPath.addPath(
          metric.extractPath(start, end),
          Offset.zero,
        );
        distance += dashWidth + dashSpace;
      }
    }
    return dashPath;
  }

  @override
  bool shouldRepaint(covariant _DashedBorderPainter old) =>
      old.color != color ||
      old.strokeWidth != strokeWidth ||
      old.dashWidth != dashWidth;
}
