import 'package:flutter/material.dart';

// ---------------------------------------------------------------------------
// Tokens de diseño — Sistema Aether Luxe
// Versión: Sprint 0.5 — aprobados por Erik
// Ref: DESIGN_SYSTEM.md sección 8 — Flutter equivalences
// ---------------------------------------------------------------------------

/// Tokens de diseño del sistema Aether Luxe.
/// Brook los implementa; Erik define los valores finales.
abstract final class DesignTokens {
  // ---------------------------------------------------------------------------
  // Colors — Aether Luxe palette
  // ---------------------------------------------------------------------------

  // Primary brand
  static const Color primary = Color(0xFF1E88E5); // blue-600
  static const Color secondary = Color(0xFF6B5B95); // violet-500

  // Surface / background
  static const Color primaryContainer = Color(0xFF141B2B); // dark navy
  static const Color primaryFixed = Color(0xFFDCE2F7); // light blue-grey

  static const Color surfaceLight = Color(0xFFFAFAFA);
  static const Color surfaceDark = Color(0xFF121218);

  // Semantic
  static const Color errorColor = Color(0xFFDC2626); // red-600
  static const Color successColor = Color(0xFF16A34A); // green-600
  static const Color warningColor = Color(0xFFD97706); // amber-600

  // Legacy — kept for compatibility
  static const Color primarySeed = primary;
  static const Color primaryLight = Color(0xFFEDE9FE);
  static const Color primaryDark = Color(0xFF4C1D95);
  static const Color secondarySeed = Color(0xFFF59E0B);

  // Gradient
  static const LinearGradient primaryGradient = LinearGradient(
    colors: [primary, secondary],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  // ---------------------------------------------------------------------------
  // Typography — Inter / system font
  // ---------------------------------------------------------------------------
  static const String fontFamily = 'Inter';

  // ---------------------------------------------------------------------------
  // Spacing — base 8px system
  // ---------------------------------------------------------------------------
  static const double space2 = 2.0;
  static const double space4 = 4.0;
  static const double space8 = 8.0;
  static const double space12 = 12.0;
  static const double space16 = 16.0;
  static const double space24 = 24.0;
  static const double space32 = 32.0;
  static const double space48 = 48.0;
  static const double space64 = 64.0;

  // ---------------------------------------------------------------------------
  // Border radius
  // ---------------------------------------------------------------------------
  static const double radiusSmall = 4.0;
  static const double radiusMedium = 8.0;
  static const double radiusLarge = 16.0;
  static const double radiusXLarge = 24.0;
  static const double radiusFull = 999.0;
}

// ---------------------------------------------------------------------------
// AppColors — semantic color API for screens and widgets
// ---------------------------------------------------------------------------

abstract final class AppColors {
  // Primary gradient colors
  static const Color primary = DesignTokens.primary;
  static const Color secondary = DesignTokens.secondary;

  // Containers
  static const Color primaryContainer = DesignTokens.primaryContainer;
  static const Color primaryFixed = DesignTokens.primaryFixed;

  // Surfaces
  static const Color surfaceLight = DesignTokens.surfaceLight;
  static const Color surfaceDark = DesignTokens.surfaceDark;

  // Semantic
  static const Color error = DesignTokens.errorColor;
  static const Color success = DesignTokens.successColor;
  static const Color warning = DesignTokens.warningColor;

  // Gradient
  static const LinearGradient primaryGradient = DesignTokens.primaryGradient;
}

// ---------------------------------------------------------------------------
// AppTypography — text styles aligned to Material 3 type scale
// ---------------------------------------------------------------------------

abstract final class AppTypography {
  static const TextStyle h1 = TextStyle(
    fontSize: 48,
    fontWeight: FontWeight.w600,
    height: 1.1,
    letterSpacing: -0.02 * 48,
    fontFamily: DesignTokens.fontFamily,
  );

  static const TextStyle h2 = TextStyle(
    fontSize: 32,
    fontWeight: FontWeight.w600,
    height: 1.2,
    letterSpacing: -0.01 * 32,
    fontFamily: DesignTokens.fontFamily,
  );

  static const TextStyle h3 = TextStyle(
    fontSize: 24,
    fontWeight: FontWeight.w600,
    height: 1.25,
    letterSpacing: -0.005 * 24,
    fontFamily: DesignTokens.fontFamily,
  );

  static const TextStyle bodyLg = TextStyle(
    fontSize: 18,
    fontWeight: FontWeight.w400,
    height: 1.6,
    fontFamily: DesignTokens.fontFamily,
  );

  static const TextStyle bodyMd = TextStyle(
    fontSize: 16,
    fontWeight: FontWeight.w400,
    height: 1.5,
    fontFamily: DesignTokens.fontFamily,
  );

  static const TextStyle bodySm = TextStyle(
    fontSize: 14,
    fontWeight: FontWeight.w400,
    height: 1.5,
    fontFamily: DesignTokens.fontFamily,
  );

  static const TextStyle labelCaps = TextStyle(
    fontSize: 12,
    fontWeight: FontWeight.w600,
    height: 1.4,
    letterSpacing: 0.08 * 12,
    fontFamily: DesignTokens.fontFamily,
  );
}

// ---------------------------------------------------------------------------
// AppSpacing — named spacing constants for consistent layouts
// ---------------------------------------------------------------------------

abstract final class AppSpacing {
  static const double xs = DesignTokens.space8;
  static const double sm = DesignTokens.space16;
  static const double md = DesignTokens.space24;
  static const double lg = DesignTokens.space32;
  static const double xl = DesignTokens.space64;

  // Convenience aliases
  static const double p2 = DesignTokens.space2;
  static const double p4 = DesignTokens.space4;
  static const double p8 = DesignTokens.space8;
  static const double p12 = DesignTokens.space12;
  static const double p16 = DesignTokens.space16;
  static const double p24 = DesignTokens.space24;
  static const double p32 = DesignTokens.space32;
  static const double p48 = DesignTokens.space48;
  static const double p64 = DesignTokens.space64;
}
