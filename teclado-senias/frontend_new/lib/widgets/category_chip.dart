/// CategoryChip — chip seleccionable para filtros de categoría/dificultad
/// Implementa las especificaciones de chips del design system de Erik.
library;

import 'package:flutter/material.dart';
import '../config/theme.dart';

class CategoryChip extends StatelessWidget {
  const CategoryChip({
    super.key,
    required this.label,
    this.isSelected = false,
    this.onTap,
  });

  final String label;
  final bool isSelected;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Semantics(
      label: '$label, ${isSelected ? "seleccionado" : "no seleccionado"}',
      button: true,
      child: GestureDetector(
        onTap: onTap,
        child: AnimatedContainer(
          duration: AppDurations.fast,
          curve: Curves.easeOut,
          height: 32,
          padding: const EdgeInsets.symmetric(
            horizontal: AppSpacing.s3,
            vertical: AppSpacing.s1,
          ),
          decoration: BoxDecoration(
            color: isSelected
                ? AppColors.primary
                : isDark
                    ? AppColors.dark700
                    : AppColors.light200,
            borderRadius: AppRadius.borderFull,
          ),
          child: Center(
            child: Text(
              label,
              style: AppTextStyles.bodySm.copyWith(
                fontWeight: FontWeight.w500,
                color: isSelected
                    ? AppColors.white
                    : isDark
                        ? const Color(0xFF9CA3AF)
                        : AppColors.dark500,
              ),
            ),
          ),
        ),
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Lista horizontal de chips para filtros
// ---------------------------------------------------------------------------

class ChipsRow extends StatelessWidget {
  const ChipsRow({
    super.key,
    required this.chips,
    required this.selectedIndex,
    required this.onSelected,
  });

  final List<String> chips;
  final int selectedIndex;
  final void Function(int index) onSelected;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 40,
      child: ListView.separated(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: AppSpacing.s4),
        itemCount: chips.length,
        separatorBuilder: (_, __) => const SizedBox(width: AppSpacing.s2),
        itemBuilder: (context, index) {
          return CategoryChip(
            label: chips[index],
            isSelected: selectedIndex == index,
            onTap: () => onSelected(index),
          );
        },
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// DifficultyDots — indicador de dificultad (5 dots) del design system de Erik
// ---------------------------------------------------------------------------

class DifficultyDots extends StatelessWidget {
  const DifficultyDots({
    super.key,
    required this.level,
    this.showLabel = true,
    this.dotSize = 10,
  });

  /// Nivel 0-5 (0 = sin dificultad definida, 1-5 = básico a experto)
  final int level;
  final bool showLabel;
  final double dotSize;

  static const _labels = ['', 'Básico', 'Fácil', 'Intermedio', 'Avanzado', 'Experto'];

  Color _dotColor(int dotIndex, BuildContext context) {
    if (dotIndex > level) {
      return Theme.of(context).brightness == Brightness.dark
          ? AppColors.difficultyInactiveDark
          : AppColors.difficultyInactive;
    }
    if (level <= 2) return AppColors.difficultyBeginnerColor;
    if (level == 3) return AppColors.difficultyMediumColor;
    return AppColors.difficultyAdvancedColor;
  }

  @override
  Widget build(BuildContext context) {
    if (level == 0) return const SizedBox.shrink();

    return Semantics(
      label: 'Dificultad: ${level <= 5 ? _labels[level] : ""}',
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          ...List.generate(5, (i) {
            return Container(
              width: dotSize,
              height: dotSize,
              margin: EdgeInsets.only(right: i < 4 ? 4 : 0),
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: _dotColor(i + 1, context),
              ),
            );
          }),
          if (showLabel && level <= 5) ...[
            const SizedBox(width: 6),
            Text(
              _labels[level],
              style: AppTextStyles.caption.copyWith(
                color: Theme.of(context).colorScheme.onSurface.withAlpha(153),
              ),
            ),
          ],
        ],
      ),
    );
  }
}
