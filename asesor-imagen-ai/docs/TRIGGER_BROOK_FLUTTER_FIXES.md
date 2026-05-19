# TRIGGER — BROOK FLUTTER FIXES

**From:** Jarvis (CEO)  
**To:** Brook (Frontend Engineer)  
**Date:** 2026-05-18 (SAB)  
**Task:** Fix 4 Critical Issues  
**Deadline:** 2026-05-20 EOD (48 hours)  
**Status:** 🔴 BLOCKING ALL FRONTEND WORK

---

## 🚨 PRIORITY: CRITICAL

**You cannot implement ANY screen (S01-S11) until these 4 issues are fixed.**

This is your ONLY task for 48 hours. Everything else waits.

---

## 📋 THE 4 ISSUES (with fixes)

Full details in: `docs/BLOCKERS_BROOK_FLUTTER.md`

### ISSUE #1: Dependency Conflict

**Problem:** `pubspec.yaml` has conflicting version constraints. App doesn't compile.

**Root cause:** Riverpod ^2.0 incompatible with flutter_hooks version needed by go_router ^8.0

**Fix:**
```bash
cd asesor_imagen_ai/

# Step 1: Update Riverpod to ^2.5.0 (latest compatible)
# Edit pubspec.yaml:
# Change: riverpod: ^2.0
# To:     riverpod: ^2.5.0

# Step 2: Get dependencies
flutter pub get

# Step 3: Verify no conflicts
flutter pub outdated  # Should show green (latest versions OK)
```

**Verify:** `flutter pub get` succeeds without errors

---

### ISSUE #2: Import Paths (Clean Architecture)

**Problem:** Mix of relative imports (`../../services/auth.dart`) and package imports. IDE can't resolve.

**Root cause:** Clean Architecture not properly implemented. Some files use relative, others use package imports.

**Fix:**
```bash
# Step 1: Audit all imports
grep -r "^import '" lib/ | grep -v "package:" | head -20

# Step 2: Convert ALL to package imports
# Example:
# BEFORE: import '../../services/auth_service.dart';
# AFTER:  import 'package:asesor_imagen_ai/services/auth_service.dart';

# Step 3: Run analyzer
flutter analyze

# Step 4: Fix any remaining issues
# Should be 0 errors, 0 warnings
```

**Expected output:** `flutter analyze` returns nothing (all clean)

**Time estimate:** 30-45 min if >100 files

---

### ISSUE #3: build_runner & Code Generation

**Problem:** Riverpod generators and Freezed don't generate `.g.dart` files. Code references non-existent files.

**Root cause:** build_runner never ran, OR old generated files are stale.

**Fix:**
```bash
# Step 1: Clean generated files
flutter pub run build_runner clean

# Step 2: Generate fresh code
flutter pub run build_runner build --delete-conflicting-outputs

# Step 3: Verify files exist
ls lib/presentation/providers/*.g.dart   # Should see files
ls lib/domain/entities/*.g.dart          # Should see files

# Step 4: Optional: Watch mode (for development)
flutter pub run build_runner watch --delete-conflicting-outputs &

# Step 5: Verify analyzer is clean
flutter analyze
```

**Expected output:** 
- `.g.dart` files exist
- `flutter analyze` clean
- No "missing import" errors

**Time estimate:** 5-10 min

---

### ISSUE #4: Theme Integration (Aether Luxe Design Tokens)

**Problem:** AppColors, AppTypography, AppSpacing not defined. Widgets reference non-existent theme constants.

**Root cause:** Design system tokens exist in DESIGN_SYSTEM.md but not wired into Flutter ThemeData.

**Fix:**

**Step 1: Create `lib/core/theme/app_theme.dart`**
```dart
import 'package:flutter/material.dart';

class AppColors {
  // Primary
  static const Color black = Color(0xFF000000);
  static const Color secondary = Color(0xFF0058BE);  // Electric blue
  static const Color tertiary = Color(0xFF9466FF);   // Violet
  
  // Secondary
  static const Color surface = Color(0xFFFAFAFA);
  static const Color outline = Color(0xFF76777D);
  static const Color error = Color(0xFFB3261E);
  
  // Gradient (for GradientButton, hero elements)
  static const Color gradientStart = Color(0xFF0058BE);
  static const Color gradientEnd = Color(0xFF9466FF);
  
  // Copy ALL colors from DESIGN_SYSTEM.md section 1
  // Total: 40+ tokens
}

class AppTypography {
  // Heading 1 (48px, w600, lh1.1, ls-0.02)
  static const h1 = TextStyle(
    fontSize: 48,
    fontWeight: FontWeight.w600,
    height: 1.1,
    letterSpacing: -0.02,
  );
  
  // Heading 2 (32px, w600, lh1.2, ls-0.01)
  static const h2 = TextStyle(
    fontSize: 32,
    fontWeight: FontWeight.w600,
    height: 1.2,
    letterSpacing: -0.01,
  );
  
  // Copy ALL from DESIGN_SYSTEM.md section 2
  // Total: 8 text styles (h1-h3, bodyLg, bodyMd, labelCaps, etc)
}

class AppSpacing {
  static const double xs = 8.0;
  static const double sm = 16.0;
  static const double md = 24.0;
  static const double lg = 32.0;
  static const double xl = 64.0;
  static const double gutter = 24.0;
  static const double margin = 32.0;
}

class AppTheme {
  static ThemeData lightTheme() {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.light(
        primary: AppColors.secondary,
        secondary: AppColors.tertiary,
        surface: AppColors.surface,
        error: AppColors.error,
      ),
      scaffoldBackgroundColor: AppColors.surface,
      textTheme: TextTheme(
        displayLarge: AppTypography.h1,
        displayMedium: AppTypography.h2,
        displaySmall: AppTypography.h3,
        bodyLarge: AppTypography.bodyLg,
        bodyMedium: AppTypography.bodyMd,
        labelLarge: AppTypography.labelCaps,
      ),
      // Material Design 3 default is good for other properties
    );
  }
}
```

**Reference:** `docs/design-system/DESIGN_SYSTEM.md` sections 1-2 (AppColors, AppTypography, AppSpacing)

**Step 2: Wire into `main.dart`**
```dart
import 'package:asesor_imagen_ai/core/theme/app_theme.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Fit Check',
      theme: AppTheme.lightTheme(),  // ← USE THIS
      home: const MainScreen(),
    );
  }
}
```

**Step 3: Use in widgets**
```dart
// Instead of:
//   color: Color(0xFF0058BE)
// Use:
//   color: AppColors.secondary

// Instead of:
//   style: TextStyle(fontSize: 32, fontWeight: FontWeight.w600)
// Use:
//   style: AppTypography.h2

// Instead of:
//   padding: EdgeInsets.all(16)
// Use:
//   padding: EdgeInsets.all(AppSpacing.sm)
```

**Step 4: Verify**
```bash
flutter analyze          # Should be clean
flutter pub get          # Should work
flutter run              # App should launch with correct colors/fonts
```

**Time estimate:** 30 min (create file + wire + verify)

---

## ✅ VALIDATION CHECKLIST

Run this after each fix:

```bash
# Post-Issue #1 (Deps)
flutter pub get
# Expected: "Got dependencies"

# Post-Issue #2 (Imports)
flutter analyze
# Expected: No output (all clean)

# Post-Issue #3 (build_runner)
flutter pub run build_runner build --delete-conflicting-outputs
ls lib/presentation/providers/*.g.dart
# Expected: .g.dart files exist

# Post-Issue #4 (Theme)
flutter analyze
flutter run
# Expected: App launches, colors are blue/purple/violet (Aether Luxe)
```

**Final validation (all 4 done):**
```bash
flutter pub get                  # ✅ Works
flutter analyze                  # ✅ 0 errors, 0 warnings
flutter pub run build_runner ... # ✅ .g.dart files exist
flutter run                      # ✅ App launches, theme correct
```

---

## 🎯 DELIVERABLE

**By EOD 2026-05-20 (48h from now):**

- [ ] Issue #1: Dependency conflict fixed
- [ ] Issue #2: Import paths converted to package imports
- [ ] Issue #3: build_runner generates `.g.dart` files
- [ ] Issue #4: AppTheme integrated, colors/fonts match Aether Luxe
- [ ] Verification: `flutter analyze` clean + app launches

**Expected state:** App compiles, hot reload works, theme correct. Ready to implement S01-S11.

---

## 🚀 WHAT HAPPENS NEXT (once fixed)

**Day 3 onwards (2026-05-20+):**

- [ ] You implement S01-S04 screens (authentication + virtual try-on structure)
- [ ] Erik designs S05-S11 mockups (if D1-D5 decided)
- [ ] By end of week: S01-S04 functional, design mockups ready for implementation

**Without these fixes:**
- ❌ Cannot start ANY screen
- ❌ Cannot integrate theme
- ❌ Cannot hot reload during development
- ❌ Project is completely blocked

---

## 📞 SUPPORT

- Sasha: Code architecture questions
- Erik: Design system tokens (reference DESIGN_SYSTEM.md)
- Jarvis: Strategy + escalation

---

## 🎬 START NOW

48 hours to fix 4 issues. Let's go. 🚀

Each issue should take ~30-45 min if you focus. Total: 2-3 hours of actual work spread over 48h.

Report progress daily to Jarvis.

