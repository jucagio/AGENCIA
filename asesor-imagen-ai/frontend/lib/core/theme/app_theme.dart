import 'package:flutter/material.dart';

import 'package:asesor_imagen_ai/core/theme/design_tokens.dart';

// ---------------------------------------------------------------------------
// AppTheme — Material 3 theme wired to Aether Luxe design tokens
// Sprint 0.5: AppColors, AppTypography, AppSpacing tokens integrated.
// TODO(Erik): Refine ComponentThemes (ButtonTheme, CardTheme, InputDecoration)
// once Figma component specs are finalized.
// ---------------------------------------------------------------------------

/// Temas de la aplicación.
/// Material 3 habilitado. Tokens del sistema de diseño Aether Luxe.
abstract final class AppTheme {
  static ThemeData get light => ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: AppColors.primary,
          brightness: Brightness.light,
        ).copyWith(
          primary: AppColors.primary,
          secondary: AppColors.secondary,
          surface: AppColors.surfaceLight,
          error: AppColors.error,
        ),
        fontFamily: DesignTokens.fontFamily,
        scaffoldBackgroundColor: AppColors.surfaceLight,
        textTheme: const TextTheme(
          displayLarge: AppTypography.h1,
          displayMedium: AppTypography.h2,
          displaySmall: AppTypography.h3,
          headlineLarge: AppTypography.h1,
          headlineMedium: AppTypography.h2,
          headlineSmall: AppTypography.h3,
          bodyLarge: AppTypography.bodyLg,
          bodyMedium: AppTypography.bodyMd,
          bodySmall: AppTypography.bodySm,
          labelSmall: AppTypography.labelCaps,
        ),
      );

  static ThemeData get dark => ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: AppColors.primary,
          brightness: Brightness.dark,
        ).copyWith(
          primary: AppColors.primary,
          secondary: AppColors.secondary,
          surface: AppColors.surfaceDark,
          error: AppColors.error,
        ),
        fontFamily: DesignTokens.fontFamily,
        scaffoldBackgroundColor: AppColors.surfaceDark,
        textTheme: const TextTheme(
          displayLarge: AppTypography.h1,
          displayMedium: AppTypography.h2,
          displaySmall: AppTypography.h3,
          headlineLarge: AppTypography.h1,
          headlineMedium: AppTypography.h2,
          headlineSmall: AppTypography.h3,
          bodyLarge: AppTypography.bodyLg,
          bodyMedium: AppTypography.bodyMd,
          bodySmall: AppTypography.bodySm,
          labelSmall: AppTypography.labelCaps,
        ),
      );
}
