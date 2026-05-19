# BLOCKERS TÉCNICOS FLUTTER — Brook

**Owner:** Brook (Frontend Flutter)  
**Assigned by:** Jarvis (CEO)  
**Deadline:** 2026-05-19 (48 horas)  
**Impact:** CRITICAL — Bloquea ALL screens (S01-S11)  
**Status:** 🔴 BLOCKING

---

## 🚨 RESUMEN

4 issues técnicos están bloqueando la implementación completa del proyecto.  
**Resolverlos es prerequisito para cualquier pantalla nueva.**

Sin esto, no hay Flutter app. Con esto, 5 screens listos en 3 días.

---

## ISSUE #1: Dependency Conflict

**Problema:**  
Conflicto de versiones en pubspec.yaml. App no compila.

**Stack trace esperado:**  
```
ERROR: Incompatible version constraints
  riverpod ^2.x requires "flutter_hooks: ^0.18.0"
  pero go_router ^8.x requires "flutter_hooks: ^0.20.0"
```

**Solución:**
- Upgrade Riverpod a ^2.5.0 (compatible con flutter_hooks ^0.20.0)
- O downgrade go_router a ^6.0.0
- Recomendación: **Upgrade Riverpod** (última version es mejor)

**Files:**
- `pubspec.yaml`
- `pubspec.lock` (regenerate post-fix)

**Tests:**
```bash
flutter pub get
flutter pub outdated  # verificar upgrades disponibles
```

---

## ISSUE #2: Import Paths (Clean Architecture)

**Problema:**  
Imports circulares o rutas relativas rotas en estructura Clean Architecture.

**Síntomas:**
```
ERROR: The import of '../../services/auth_service.dart' 
is not found at 'package:asesor_imagen_ai/services/auth_service.dart'
```

**Estructura esperada:**
```
lib/
├── core/              → exceptions, constants, theme
├── data/
│   ├── datasources/   → local, remote
│   ├── models/
│   └── repositories/
├── domain/
│   ├── entities/
│   ├── repositories/
│   └── usecases/
├── presentation/
│   ├── screens/
│   ├── widgets/
│   └── providers/    → Riverpod consumers
└── main.dart
```

**Solución:**
- Convertir todos los imports a imports `package:` en lugar de relativos
- Ejemplo: cambiar `import '../../services/auth.dart'` a `import 'package:asesor_imagen_ai/services/auth.dart'`
- Verificar que TODOS los files en `lib/` usan `package:` imports

**Files:**
- Todos los `.dart` en `lib/` (audit + fix)

**Tests:**
```bash
flutter analyze  # debería estar limpio
```

---

## ISSUE #3: build_runner & Code Generation

**Problema:**  
`riverpod_generator` y `freezed` requieren code generation, pero output no está generado o `.g.dart` files están stale.

**Síntomas:**
```
ERROR: Could not find 'auth_provider.g.dart' 
generated from 'lib/presentation/providers/auth_provider.dart'
```

**Solución:**
```bash
# Limpiar generados viejos
flutter pub run build_runner clean

# Generar código fresco
flutter pub run build_runner build --delete-conflicting-outputs

# (Opcional) Watch mode durante desarrollo
flutter pub run build_runner watch --delete-conflicting-outputs
```

**Files que requieren generation:**
- Cualquier archivo con `@riverpod` annotation (Riverpod generator)
- Cualquier clase con `@freezed` annotation (Freezed serialization)

**Verificar:**
```bash
# Todos estos archivos deben existir post-generation
ls lib/presentation/providers/*.g.dart
ls lib/domain/entities/*.g.dart
```

**pubspec.yaml debe tener:**
```yaml
dev_dependencies:
  build_runner: ^2.4.0
  riverpod_generator: ^2.5.0
  freezed_annotation: ^2.4.0
  freezed: ^2.4.0
```

---

## ISSUE #4: Theme Integration — Aether Luxe Tokens

**Problema:**  
Aether Luxe design system tokens (AppColors, AppTypography, AppSpacing) no están integrados en Flutter ThemeData.

**Síntomas:**
```
ERROR: 'AppColors' is not defined
ERROR: primaryGradient not available in theme context
```

**Solución:**

Crear `lib/core/theme/app_theme.dart`:

```dart
import 'package:flutter/material.dart';

class AppColors {
  static const Color black = Color(0xFF000000);
  static const Color secondary = Color(0xFF0058BE);  // Electric blue
  static const Color tertiary = Color(0xFF9466FF);   // Violet
  static const Color surface = Color(0xFFFAFAFA);
  static const Color outline = Color(0xFF76777D);
  
  // ... resto de 40+ tokens de DESIGN_SYSTEM.md
}

class AppTypography {
  static const h1 = TextStyle(
    fontSize: 48,
    fontWeight: FontWeight.w600,
    height: 1.1,
    letterSpacing: -0.02,
  );
  
  static const h2 = TextStyle(
    fontSize: 32,
    fontWeight: FontWeight.w600,
    height: 1.2,
    letterSpacing: -0.01,
  );
  
  // ... resto de estilos
}

class AppSpacing {
  static const xs = 8.0;
  static const sm = 16.0;
  static const md = 24.0;
  static const lg = 32.0;
  // ...
}

class AppTheme {
  static ThemeData lightTheme() {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.light(
        primary: AppColors.secondary,
        secondary: AppColors.tertiary,
        surface: AppColors.surface,
      ),
      textTheme: TextTheme(
        displayLarge: AppTypography.h1,
        displayMedium: AppTypography.h2,
        displaySmall: AppTypography.h3,
        bodyLarge: AppTypography.bodyLg,
        // ...
      ),
    );
  }
}
```

**En `main.dart`:**
```dart
MaterialApp(
  theme: AppTheme.lightTheme(),
  home: MainScreen(),
)
```

**Reference:** `docs/design-system/DESIGN_SYSTEM.md` sección 9 (Flutter equivalences)

---

## 📋 ACCIÓN REQUERIDA (BROOK)

### Orden de resolución (dependencias):
1. **Issue #1** (deps) → `flutter pub get` funcione
2. **Issue #2** (imports) → análisis limpio
3. **Issue #3** (build_runner) → `.g.dart` generados
4. **Issue #4** (theme) → AppTheme disponible en toda la app

### Checklist de validación:
```bash
# Pre-fixes
[ ] flutter pub get              # falla por deps
[ ] flutter analyze              # falla por imports

# Post-fixes (en orden)
[ ] flutter pub get              # ✅ debe pasar
[ ] flutter analyze              # ✅ debe estar limpio (0 errors)
[ ] flutter pub run build_runner build --delete-conflicting-outputs
[ ] ls lib/presentation/providers/*.g.dart  # ✅ archivos existen
[ ] flutter pub run build_runner watch      # ✅ corre sin errores
```

### Testing:
```bash
# Hot reload debe funcionar
flutter run
  # En el emulator: navegar entre screens sin crashes
  # AppTheme (AppColors, AppTypography, AppSpacing) debe ser accesible en widgets
```

---

## 🎯 IMPACTO POST-FIX

Una vez resolvertos estos 4 issues:

✅ App compila limpiamente  
✅ Hot reload funciona  
✅ Imports limpios (no relativos)  
✅ Code generation automático  
✅ Theme tokens listos para UI  

**Entonces Brook puede implementar (en paralelo con Erik diseñando):**
- S01 Splash/Onboarding (uses AppTheme)
- S02 Login (uses GradientButton, AppColors)
- S03 Register (uses AppTheme)
- S04 Virtual Try-On (estructura lista para cargar resultado)
- Post-Erik S05-S11 (mockups ready)

---

## 📞 SOPORTE

Si necesitas help:
- Sasha: arquitectura backend + integración API
- Erik: tokens exactos de DESIGN_SYSTEM.md
- Jarvis: estrategia de resolución + priorización

**Timeline:** 48 horas. Si no, sprint está completamente bloqueado.

