import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';

import 'package:asesor_imagen_ai/core/theme/design_tokens.dart';
import 'package:asesor_imagen_ai/features/wardrobe/data/wardrobe_repository.dart';

// ---------------------------------------------------------------------------
// WardrobeGrid — diseño Stitch validado por Erik
// Label "Tu Ropa" + badge "Max 5" en esquina superior derecha
// GridView de items con imagen/color + botón "+"
// Slot vacío → solo botón "+" gris
// ---------------------------------------------------------------------------

class WardrobeGrid extends StatelessWidget {
  const WardrobeGrid({
    super.key,
    required this.items,
    required this.selectedIds,
    required this.onToggle,
    this.maxItems = 5,
  });

  final List<WardrobeItem> items;
  final List<String> selectedIds;
  final ValueChanged<String> onToggle;
  final int maxItems;

  @override
  Widget build(BuildContext context) {
    final selectedItems =
        items.where((i) => selectedIds.contains(i.id)).toList();
    final unselectedItems =
        items.where((i) => !selectedIds.contains(i.id)).toList();

    // Mostrar los seleccionados primero, luego los slots vacíos hasta maxItems
    final displayItems = <WardrobeItem?>[
      ...selectedItems,
      ...unselectedItems.take((maxItems - selectedItems.length).clamp(0, maxItems)),
    ];

    // Rellenar hasta maxItems con nulls (slots vacíos)
    while (displayItems.length < maxItems) {
      displayItems.add(null);
    }
    final gridItems = displayItems.take(maxItems).toList();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Header con label y badge Max 5
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text(
              'Tu Ropa',
              style: TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w600,
                color: Color(0xFF374151),
              ),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
              decoration: BoxDecoration(
                color: const Color(0xFFF3F4F6),
                borderRadius: BorderRadius.circular(DesignTokens.radiusFull),
              ),
              child: Text(
                'Max $maxItems',
                style: const TextStyle(
                  fontSize: 11,
                  fontWeight: FontWeight.w500,
                  color: Color(0xFF6B7280),
                ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 10),

        // Grid
        GridView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 5,
            mainAxisSpacing: 8,
            crossAxisSpacing: 8,
            childAspectRatio: 0.75,
          ),
          itemCount: gridItems.length,
          itemBuilder: (context, index) {
            final item = gridItems[index];
            final isSelected = item != null && selectedIds.contains(item.id);
            return _WardrobeSlot(
              item: item,
              isSelected: isSelected,
              onTap: item != null ? () => onToggle(item.id) : null,
            );
          },
        ),

        // Subtexto de selección
        if (selectedIds.isNotEmpty) ...[
          const SizedBox(height: 8),
          Text(
            '${selectedIds.length} de $maxItems prendas seleccionadas',
            style: const TextStyle(
              fontSize: 11,
              color: Color(0xFF9CA3AF),
            ),
          ),
        ],
      ],
    );
  }
}

class _WardrobeSlot extends StatelessWidget {
  const _WardrobeSlot({
    required this.item,
    required this.isSelected,
    this.onTap,
  });

  final WardrobeItem? item;
  final bool isSelected;
  final VoidCallback? onTap;

  static const _primaryBlue = Color(0xFF0058BE);

  Color _parseColor(String? hex) {
    if (hex == null) return const Color(0xFFE5E7EB);
    try {
      final clean = hex.replaceAll('#', '');
      return Color(int.parse('FF$clean', radix: 16));
    } catch (_) {
      return const Color(0xFFE5E7EB);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (item == null) {
      // Slot vacío — solo "+" gris
      return Container(
        decoration: BoxDecoration(
          color: const Color(0xFFF9FAFB),
          borderRadius: BorderRadius.circular(DesignTokens.radiusMedium),
          border: Border.all(
            color: const Color(0xFFE5E7EB),
            width: 1.5,
          ),
        ),
        child: const Center(
          child: Icon(Icons.add, size: 20, color: Color(0xFFD1D5DB)),
        ),
      );
    }

    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(DesignTokens.radiusMedium),
          border: Border.all(
            color: isSelected ? _primaryBlue : const Color(0xFFE5E7EB),
            width: isSelected ? 2 : 1.5,
          ),
        ),
        child: ClipRRect(
          borderRadius: BorderRadius.circular(DesignTokens.radiusMedium - 2),
          child: Stack(
            fit: StackFit.expand,
            children: [
              // Imagen o color swatch
              item!.imageUrl != null && item!.imageUrl!.isNotEmpty
                  ? CachedNetworkImage(
                      imageUrl: item!.imageUrl!,
                      fit: BoxFit.cover,
                      placeholder: (_, __) => Container(
                        color: _parseColor(item!.color),
                      ),
                      errorWidget: (_, __, ___) => Container(
                        color: _parseColor(item!.color),
                        child: const Icon(Icons.checkroom_outlined,
                            size: 20, color: Colors.white),
                      ),
                    )
                  : Container(
                      color: _parseColor(item!.color),
                      child: Center(
                        child: Text(
                          _typeEmoji(item!.type),
                          style: const TextStyle(fontSize: 22),
                        ),
                      ),
                    ),

              // Overlay seleccionado
              if (isSelected)
                Positioned(
                  top: 4,
                  right: 4,
                  child: Container(
                    width: 18,
                    height: 18,
                    decoration: const BoxDecoration(
                      color: _primaryBlue,
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(Icons.check,
                        size: 12, color: Colors.white),
                  ),
                ),

              // Botón "+" si no está seleccionado
              if (!isSelected)
                Positioned(
                  bottom: 0,
                  left: 0,
                  right: 0,
                  child: Container(
                    color: Colors.black.withOpacity(0.35),
                    padding: const EdgeInsets.symmetric(vertical: 4),
                    child: const Icon(Icons.add, size: 14, color: Colors.white),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }

  String _typeEmoji(String type) {
    const map = {
      'shirt': '👕',
      'pants': '👖',
      'dress': '👗',
      'jacket': '🧥',
      'skirt': '👗',
      'shoes': '👟',
      'accessory': '👜',
    };
    return map[type] ?? '👔';
  }
}
