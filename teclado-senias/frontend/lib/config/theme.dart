import 'package:flutter/material.dart';

class AppColors {
  // Brand
  static const primary = Color(0xFF0066FF);
  static const secondary = Color(0xFF7C3AED);
  static const accent = Color(0xFF06B6D4);

  // Neutral
  static const dark900 = Color(0xFF111827);
  static const dark800 = Color(0xFF1F2937);
  static const dark700 = Color(0xFF374151);
  static const dark600 = Color(0xFF4B5563);
  static const dark500 = Color(0xFF6B7280);

  static const light100 = Color(0xFFF3F4F6);
  static const light200 = Color(0xFFE5E7EB);
  static const light300 = Color(0xFFD1D5DB);
  static const white = Color(0xFFFFFFFF);

  // Semantic
  static const success = Color(0xFF22C55E);
  static const successBg = Color(0xFFF0FDF4);
  static const warning = Color(0xFFF59E0B);
  static const warningBg = Color(0xFFFFFBEB);
  static const error = Color(0xFFEF4444);
  static const errorBg = Color(0xFFFEF2F2);
  static const info = Color(0xFF3B82F6);
  static const infoBg = Color(0xFFEFF6FF);

  // Dark mode
  static const darkPrimary = Color(0xFF3B82F6);
  static const darkSecondary = Color(0xFFA78BFA);
  static const darkAccent = Color(0xFF22D3EE);
}

class AppSpacing {
  static const s1 = 4.0;
  static const s2 = 8.0;
  static const s3 = 12.0;
  static const s4 = 16.0;
  static const s5 = 20.0;
  static const s6 = 24.0;
  static const s8 = 32.0;
  static const s10 = 40.0;
  static const s12 = 48.0;
  static const s16 = 64.0;
  static const s20 = 80.0;
  static const s24 = 96.0;
}

class AppRadius {
  static const sm = 4.0;
  static const md = 8.0;
  static const lg = 12.0;
  static const xl = 16.0;
  static const xxl = 24.0;
  static const full = 9999.0;
}

class AppTypography {
  static const String fontFamily = 'OpenSans';

  static const display = TextStyle(
    fontSize: 48,
    fontWeight: FontWeight.bold,
    height: 56 / 48,
    letterSpacing: -0.02,
  );

  static const h1 = TextStyle(
    fontSize: 32,
    fontWeight: FontWeight.w600,
    height: 40 / 32,
    letterSpacing: -0.01,
  );

  static const h2 = TextStyle(
    fontSize: 24,
    fontWeight: FontWeight.w600,
    height: 32 / 24,
    letterSpacing: -0.01,
  );

  static const h3 = TextStyle(
    fontSize: 20,
    fontWeight: FontWeight.w600,
    height: 28 / 20,
  );

  static const h4 = TextStyle(
    fontSize: 18,
    fontWeight: FontWeight.w600,
    height: 24 / 18,
  );

  static const bodyLg = TextStyle(
    fontSize: 18,
    fontWeight: FontWeight.normal,
    height: 28 / 18,
  );

  static const body = TextStyle(
    fontSize: 16,
    fontWeight: FontWeight.normal,
    height: 24 / 16,
  );

  static const bodySm = TextStyle(
    fontSize: 14,
    fontWeight: FontWeight.normal,
    height: 20 / 14,
  );

  static const caption = TextStyle(
    fontSize: 12,
    fontWeight: FontWeight.normal,
    height: 16 / 12,
    letterSpacing: 0.02,
  );

  static const buttonLg = TextStyle(
    fontSize: 18,
    fontWeight: FontWeight.w600,
    height: 24 / 18,
    letterSpacing: 0.01,
  );

  static const button = TextStyle(
    fontSize: 16,
    fontWeight: FontWeight.w600,
    height: 20 / 16,
    letterSpacing: 0.01,
  );

  static const buttonSm = TextStyle(
    fontSize: 14,
    fontWeight: FontWeight.w600,
    height: 18 / 14,
    letterSpacing: 0.01,
  );

  static const label = TextStyle(
    fontSize: 12,
    fontWeight: FontWeight.w500,
    height: 16 / 12,
    letterSpacing: 0.05,
  );

  static const overline = TextStyle(
    fontSize: 11,
    fontWeight: FontWeight.w600,
    height: 16 / 11,
    letterSpacing: 0.1,
  );
}

ThemeData lightTheme() {
  return ThemeData(
    useMaterial3: true,
    brightness: Brightness.light,
    primaryColor: AppColors.primary,
    scaffoldBackgroundColor: AppColors.light100,
    fontFamily: AppTypography.fontFamily,
    colorScheme: ColorScheme.light(
      primary: AppColors.primary,
      secondary: AppColors.secondary,
      tertiary: AppColors.accent,
      error: AppColors.error,
      surface: AppColors.white,
      onSurface: AppColors.dark900,
    ),
    appBarTheme: AppBarTheme(
      backgroundColor: AppColors.white,
      foregroundColor: AppColors.dark900,
      elevation: 0,
      centerTitle: false,
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: AppColors.white,
      contentPadding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.s4,
        vertical: AppSpacing.s4,
      ),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(AppRadius.md),
        borderSide: const BorderSide(color: AppColors.light200),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(AppRadius.md),
        borderSide: const BorderSide(color: AppColors.light200),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(AppRadius.md),
        borderSide: const BorderSide(color: AppColors.primary, width: 1.5),
      ),
      errorBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(AppRadius.md),
        borderSide: const BorderSide(color: AppColors.error, width: 1.5),
      ),
      labelStyle: AppTypography.label.copyWith(color: AppColors.dark500),
      hintStyle: AppTypography.body.copyWith(color: AppColors.light300),
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: AppColors.primary,
        foregroundColor: AppColors.white,
        minimumSize: const Size.fromHeight(56),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadius.lg),
        ),
        textStyle: AppTypography.buttonLg,
      ),
    ),
  );
}

ThemeData darkTheme() {
  return ThemeData(
    useMaterial3: true,
    brightness: Brightness.dark,
    primaryColor: AppColors.darkPrimary,
    scaffoldBackgroundColor: AppColors.dark900,
    fontFamily: AppTypography.fontFamily,
    colorScheme: ColorScheme.dark(
      primary: AppColors.darkPrimary,
      secondary: AppColors.darkSecondary,
      tertiary: AppColors.darkAccent,
      error: AppColors.error,
      surface: AppColors.dark800,
      onSurface: Color(0xFFF9FAFB),
    ),
  );
}
