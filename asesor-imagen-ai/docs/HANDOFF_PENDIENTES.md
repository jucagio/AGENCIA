# Handoff de pendientes — Sprint 0
**Última actualización:** 2026-04-29
**Owner:** Jarvis

---

## Estado al cierre del día (rate limit hit en 3 agentes a la vez)

### ✅ Completado por Brook (Frontend)
- Flutter project en `frontend/` (creado por Jarvis, scaffold por Brook)
- `pubspec.yaml` con dependencias 2026 (Riverpod 3.3, go_router 17.2, supabase 2.12)
- Estructura Clean Architecture completa en `lib/`
- `main.dart` + `app.dart` con bootstrap Supabase + Riverpod
- 9 screens stubbed (splash, onboarding, login, register, home, wardrobe, try_on, recommendations, profile)
- `core/`: env, constants, theme (light/dark), routing, errors, dio_client

### ✅ Completado por Erik (Diseño)
- `docs/design-system/design-system.md`
- `docs/design-system/design-tokens.json` (Brook puede importar)
- 5 mockups: splash/onboarding, auth, home, wardrobe gallery, add wardrobe item

### ✅ Completado por Yang (Intel)
- `docs/INTEL_COMPETIDORES_2026.md`

### ⏸️ Sasha — Pendiente
- Entrega 0.1 (Foundation) bloqueada por rate limit antes de empezar.

---

## 🔧 ISSUES TÉCNICOS PENDIENTES (para Brook al regresar)

### Issue #1 — Conflicto de dependencias riverpod_generator + custom_lint
**Síntoma:** `flutter pub get` falla con conflict entre `analyzer ^8` (custom_lint) y `analyzer ^9/^12` (riverpod_generator).

**Workaround aplicado por Jarvis:** Comentado `riverpod_generator`, `riverpod_lint`, `custom_lint` en `pubspec.yaml`.

**Acción Brook:**
- Opción A: Esperar release que alinee analyzer en custom_lint 0.9+
- Opción B: Refactor `router.dart` y futuros providers a Riverpod sin code generation (Provider/StreamProvider tradicional). Menos elegante pero sin conflicts.

### Issue #2 — Imports incorrectos en `lib/core/routing/router.dart`
**Líneas 13-15:** `'../shared/screens/...'` debería ser `'../../shared/screens/...'` (2 niveles arriba desde `lib/core/routing/`).

```dart
// MAL
import '../shared/screens/onboarding_screen.dart';

// BIEN
import '../../shared/screens/onboarding_screen.dart';
```

### Issue #3 — `failures.dart` redirected constructors mal formados
**Líneas 34, 39, 44:** `NotFoundFailure`, `ValidationFailure`, `UnknownFailure` aparecen como redirects pero no están definidos como classes. Probablemente faltó correr `build_runner` para generar freezed.

**Acción Brook:**
```bash
cd frontend
dart run build_runner build --delete-conflicting-outputs
```
Si freezed no resuelve, declarar las clases manualmente.

### Issue #4 — `router.g.dart` no generado
Sin `riverpod_generator` (ver Issue #1), las anotaciones `@riverpod` no producen el `.g.dart`. Refactor a sintaxis tradicional o reactivar generator cuando se resuelva conflicto.

---

## 📋 Próximos pasos (orden de ejecución)

1. **Sasha (cuando reset)** → Entrega 0.1 (Foundation backend, ya con plan v2 + ADRs)
2. **Brook (cuando reset)** → Resolver Issues #1-#4 arriba
3. **Erik (cuando reset)** → Completar 5 mockups restantes (body analysis, try-on screen, recommendations, profile, paywall)
4. **Cyber Neo** → Audit RLS policies (cuando Sasha entregue migration SQL en 0.2)
5. **Leo** → Pricing strategy con intel de Yang (puede empezar ya, no depende de rate limit)

---

## ⚠️ Lección operacional
3 agentes en paralelo + rate limits = riesgo de bloqueo simultáneo. Para próximos sprints:
- Escalonar lanzamientos (no todos al mismo tiempo)
- Verificar `flutter analyze` / `pytest` ANTES de cerrar sesión del agente
- Mantener doc de handoff actualizado
