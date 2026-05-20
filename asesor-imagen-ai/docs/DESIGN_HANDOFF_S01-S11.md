# DESIGN HANDOFF — S01-S11
## AI Fit Check — Entrega Completa de Diseño a Brook

**Owner:** Erik (Diseñador Senior)
**Handoff a:** Brook (Frontend Flutter)
**Fecha de entrega:** SAB 25 mayo 2026
**Design system:** Aether Luxe (aprobado por Juan Camilo Gil — 2026-05-18)
**Sprint wave delivery:**
  - Wave 1 (completado): S04B, S06, S07, S11
  - Wave 2 (en curso): S05, S08, S09, S10
  - Wave 3 (completado specs): S01, S02, S03, S04

---

## INDICE DE PANTALLAS

| Screen | Nombre | Wave | Specs | Cap Screen |
|--------|--------|------|-------|-----------|
| S01 | Splash / Onboarding (3 slides) | 3 | ERIK_SPRINT_DESIGN_SPECS.md §S01 | - |
| S02 | Login | 3 | ERIK_SPRINT_DESIGN_SPECS.md §S02 | - |
| S03 | Register | 3 | ERIK_SPRINT_DESIGN_SPECS.md §S03 | - |
| S04 | Virtual Try-On | 3 | ERIK_SPRINT_DESIGN_SPECS.md §S04 | Counter pill |
| S04B | Loading State | 1 | ERIK_SPRINT_DESIGN_SPECS.md §S04B | - |
| S05 | My Wardrobe | 2 | ERIK_SPRINT_DESIGN_SPECS.md §S05 | - |
| S06 | Style Insights + Soft Cap | 1 | S06_SOFT_CAP_UI_DESIGN.md | SoftCapBottomSheet |
| S07 | Body Analysis Upload | 1 | ERIK_SPRINT_DESIGN_SPECS.md §S07 | - |
| S08 | Collections | 2 | ERIK_SPRINT_DESIGN_SPECS.md §S08 | Share gated |
| S09 | Profile / Settings | 2 | ERIK_SPRINT_DESIGN_SPECS.md §S09 | Plan badge |
| S10 | Paywall | 2 | ERIK_SPRINT_DESIGN_SPECS.md §S10 | 3 tiers |
| S11 | Error States (4) | 1 | ERIK_SPRINT_DESIGN_SPECS.md §S11 | - |

**Figma:** [PENDIENTE — link cuando Figma este listo SAB 25]
**Directorio assets:** `asesor-imagen-ai/frontend/assets/illustrations/`
**Tokens dart:** `asesor-imagen-ai/frontend/lib/core/theme/`

---

## 1. FUENTES DE VERDAD — DONDE LEER CADA COSA

| Documento | Ruta | Contiene |
|-----------|------|---------|
| Design System Aether Luxe | `docs/design-system/DESIGN_SYSTEM.md` | Todos los tokens: colores, tipos, spacing, radius, sombras, componentes |
| Specs completas S01-S11 | `docs/mockups/ERIK_SPRINT_DESIGN_SPECS.md` | Layouts ASCII, tokens por pantalla, notas de implementacion |
| Soft Cap UI (S06) | `docs/mockups/S06_SOFT_CAP_UI_DESIGN.md` | Flow completo S06-A/B/C, variants A-D, animaciones, Dart snippets |
| Copy variants cap screen | `docs/COPY_SOFT_CAP_APPROVED.md` | JSON copy por variant, logica de seleccion dia/segmento |
| Decisiones D1-D5 | `docs/DECISIONES_APROBADAS.md` | App name, try-on flow, body analysis, tiers, social sharing |
| UX screens plan | `docs/UX_SCREENS_PLAN.md` | Flujos completos, navegacion, endpoints por pantalla |

---

## 2. TOKENS DE DISENO — IMPLEMENTACION DART

Los tokens ya estan documentados en `docs/design-system/DESIGN_SYSTEM.md` con el codigo Dart exacto.
Archivos que Brook debe crear o verificar:

```
lib/core/theme/
  ├── app_colors.dart      ← AppColors (40+ tokens, Material You)
  ├── app_typography.dart  ← AppTypography (h1-h3, bodyLg, bodyMd, labelCaps)
  ├── app_spacing.dart     ← AppSpacing (unit/xs/sm/md/lg/xl/gutter/margin)
  ├── app_radius.dart      ← AppRadius (sm/DEFAULT/md/lg/xl/full)
  └── app_shadows.dart     ← AppShadows (ambient1, ambient2)
```

**Regla:** NINGUN color hardcodeado fuera de AppColors. NINGUNA fuente hardcodeada fuera de AppTypography. Si un token no existe, pedirlo a Erik — no inventarlo.

### Gradiente primario (uso EXCLUSIVO)

```dart
static const Gradient primaryGradient = LinearGradient(
  begin: Alignment.topLeft,
  end: Alignment.bottomRight,
  colors: [Color(0xFF0058BE), Color(0xFF9466FF)],
);
```

Usar en: GradientButton, GradientLoaderCard, border activo UploadZone, AIInsightChip border hover.
NO usar en: fondos de pantalla completa, texto normal, decoracion gratuita.

---

## 3. COMPONENTES REUTILIZABLES — ATOMS

Crear en `lib/shared/widgets/atoms/`. Todos deben tener:
- tests de widget basicos
- soporte dark mode (Material You tokens)
- comentario de uso en cabecera

### GradientButton

```dart
// lib/shared/widgets/atoms/gradient_button.dart
// USO: CTA primario. Maximo 1 por pantalla visible.

class GradientButton extends StatelessWidget {
  final String label;
  final IconData? icon;
  final VoidCallback? onPressed;
  final bool loading;

  // Especificaciones Aether Luxe:
  // - gradient: primaryGradient (#0058BE → #9466FF, 135deg)
  // - height: 48px (WCAG tap target)
  // - radius: AppRadius.full (pill)
  // - texto: AppTypography.bodyLg.copyWith(fontWeight: w600, color: white)
  // - icono: 20px, white
  // - shadow: AppShadows.ambient2
  // - disabled: opacity 0.4, sin gradient (surfaceContainerHighest)
  // - tap feedback: scale 1.0 → 0.97 → 1.0 (100ms easeOut)
}
```

### OutlineButton

```dart
// lib/shared/widgets/atoms/outline_button.dart
// USO: CTA secundario, acciones secundarias.

// - borde: 1px solid AppColors.primary (#000)
// - texto: AppTypography.labelCaps, color AppColors.onSurface
// - bg: transparent
// - radius: AppRadius.lg (16px)
// - height: 48px
// - hover/focus: bg AppColors.surfaceVariant
```

### AIInsightChip

```dart
// lib/shared/widgets/atoms/ai_insight_chip.dart
// USO: Badge que indica contenido generado por IA.

// - bg: AppColors.tertiaryFixed (#E9DDFF)
// - text: AppColors.onTertiaryContainer (#9466FF)
// - icono: Icons.auto_awesome, 14px, same color
// - padding: 4px top/bottom, 12px left/right
// - radius: AppRadius.full (pill)
// - font: AppTypography.labelCaps
```

### PlanBadge

```dart
// lib/shared/widgets/atoms/plan_badge.dart
// USO: Indica tier del usuario (Free/Estilo/Imagen).

// Props: plan enum {free, estilo, imagen}
//
// free:   bg AppColors.surfaceContainer, text AppColors.onSurfaceVariant
// estilo: bg AppColors.secondaryFixed (#D8E2FF), text AppColors.secondary (#0058BE)
// imagen: bg AppColors.tertiaryFixed (#E9DDFF), text AppColors.onTertiaryContainer (#9466FF)
// todos:  radius full, labelCaps, padding 4px 8px
```

### TryOnCounterPill

```dart
// lib/shared/widgets/atoms/tryon_counter_pill.dart
// USO: Contador de try-ons del free tier. Visible en S04 y S06.
// Props: used int, cap int, resetsAt DateTime

// Estado normal (used < cap - 1):
//   bg: AppColors.surfaceContainerHigh
//   text: AppColors.onSurfaceVariant
//   label: "${used}/${cap} esta semana"
//
// Estado alerta (used == cap - 1):
//   bg: AppColors.errorContainer (#FFDED6)
//   text: AppColors.onErrorContainer (#93000A)
//   icono: Icons.warning_amber_outlined, 14px
//   label: "1/${cap} esta semana"
//
// Estado cap (used >= cap):
//   bg: AppColors.errorContainer
//   text: AppColors.onErrorContainer
//   icono: Icons.lock_outline, 14px
//   label: "0/${cap} (reset domingo 23:59)"
//   → tap: trigger SoftCapBottomSheet si no esta ya abierto

// Animacion cambio de numero: AnimatedSwitcher, 200ms
// Animacion normal → cap: scale pulse 1.0 → 1.1 → 1.0, 400ms
```

---

## 4. COMPONENTES REUTILIZABLES — MOLECULES

Crear en `lib/shared/widgets/molecules/`.

### UploadZone

```dart
// lib/shared/widgets/molecules/upload_zone.dart
// USO: S04 (foto personal), S05 (prenda modal), S07 (body analysis)
// Props:
//   promptIcon: IconData (photo_camera / person)
//   promptTitle: String
//   promptSubtitle: String
//   aspectRatio: double (S04: 3/4, S07: 3/4, S05 modal: 1/1)
//   onImagePicked: Function(File)
//   imageFile: File? (null = estado vacio)

// Estado vacio:
//   border: 2px dashed AppColors.outlineVariant (#C6C6CD)
//   bg: AppColors.surfaceContainerLowest (#FFF)
//   radius: AppRadius.lg (16px)
//   icono: promptIcon, 48px, color AppColors.outline
//   texto: promptTitle (h3) + promptSubtitle (bodyMd)

// Estado filled (imageFile != null):
//   imagen: Image.file, BoxFit.cover, radius lg
//   boton X: circle 32px, top-right, bg surface 80%, onTap → clear image

// Hover/active (drag over):
//   border → AppColors.secondary (#0058BE), animado 200ms AnimatedContainer
//   opcional: border gradient 2px (mas complejo, omitir en MVP)
```

### GradientLoaderCard

```dart
// lib/shared/widgets/molecules/gradient_loader_card.dart
// USO: S04B (try-on loading), S07 loading state
// Props:
//   onCancel: VoidCallback? (null = no mostrar boton cancelar)
//   durationMs: int (default 45000)
//   rotatingTexts: List<String>

// Especificaciones:
//   bg card: AppColors.surfaceContainerLow (#F3F4F6)
//   radius: AppRadius.lg (16px)
//   padding: 32px
//   shadow: AppShadows.ambient2
//
//   Shimmer interno:
//     AnimationController duration 1800ms, repeat(reverse: true)
//     gradient: LinearGradient(
//       colors: [
//         Color(0xFF0058BE).withOpacity(0.15),
//         Color(0xFF9466FF).withOpacity(0.35),
//         Color(0xFF0058BE).withOpacity(0.15),
//       ],
//     )
//     escala: TweenAnimationBuilder 1.00 → 1.015 → 1.00, 2000ms loop
//
//   Progress bar:
//     track: AppColors.outlineVariant (#C6C6CD), height 4px, radius full
//     fill: gradient #0058BE → #9466FF
//     animacion: 0 → 1.0 en durationMs (no linear, use Curves.easeOut)
//
//   Textos rotativos:
//     Timer.periodic(Duration(seconds: 5), ...)
//     CrossFadeTransition 300ms entre textos
//     secuencia: rotatingTexts[index % rotatingTexts.length]
//
//   Boton cancelar:
//     visible solo despues de 20000ms
//     OutlineButton "Cancelar"
//     onPressed: onCancel callback

// NO usar Lottie para este componente — implementacion nativa es mas eficiente.
```

### SoftCapBottomSheet

```dart
// lib/shared/widgets/molecules/soft_cap_bottom_sheet.dart
// USO: S06 (post-analysis cap), S04 (cuando usuario intenta try-on sin cupo)
// Props:
//   variant: SoftCapVariant {A, B, C, D}
//   onCTA: VoidCallback
//   onSecondary: VoidCallback?
//   resetsAt: DateTime
//   usedThisWeek: int
//   capWeek: int

// Mostrar via:
//   showModalBottomSheet(
//     isScrollControlled: true,
//     backgroundColor: Colors.transparent,
//     builder: (_) => DraggableScrollableSheet(
//       initialChildSize: 0.40,
//       minChildSize: 0.0,
//       maxChildSize: 0.50,
//       builder: (_, controller) => SoftCapBottomSheet(...),
//     ),
//   );

// Timing en S06: delay 700ms despues de que ResultsAnalysisCard termina de animar
// Timing en S04: inmediato cuando POST /try-ons retorna 429

// Copy: leer COPY_SOFT_CAP_APPROVED.md para cada variant
// Seleccion de variant: logica en SoftCapVariantSelector (ver abajo)
```

### SoftCapVariantSelector

```dart
// lib/features/tryon/domain/soft_cap_variant_selector.dart
// USO: Determina cual variant mostrar segun dia y segmento del usuario

enum SoftCapVariant { A, B, C, D }

class SoftCapVariantSelector {
  static SoftCapVariant select({
    required int engagementScore,    // de GET /users/me/engagement
    required bool isNewUser,         // primera semana
    required int daysSinceLastSession,
    required DateTime now,
  }) {
    if (engagementScore >= 7) return SoftCapVariant.C;
    if (isNewUser) return SoftCapVariant.B;
    if (daysSinceLastSession > 5) return SoftCapVariant.D;

    // Map dia de semana
    final weekday = now.weekday; // 1=Lun, 7=Dom
    switch (weekday) {
      case 1: return SoftCapVariant.D; // Lunes
      case 2: return SoftCapVariant.A; // Martes
      case 3: return SoftCapVariant.A; // Miercoles
      case 4: return SoftCapVariant.B; // Jueves
      case 5: return SoftCapVariant.B; // Viernes
      case 6: return SoftCapVariant.B; // Sabado
      case 7: return SoftCapVariant.B; // Domingo
      default: return SoftCapVariant.A;
    }
  }
}
```

### WardrobeCard

```dart
// lib/shared/widgets/molecules/wardrobe_card.dart
// USO: S05 grid de prendas
// Props: item WardrobeItem, onTap VoidCallback, onMenu Function(String action)

// - aspect ratio: 1:1 (AspectRatio widget)
// - imagen: BoxFit.cover, radius AppRadius.md (12px)
// - shadow: AppShadows.ambient1
// - badge categoria: labelCaps, bg AppColors.surfaceContainer, bottom-left
// - menu: PopupMenuButton top-right, circle 32px, bg surface/80%
//   acciones: "Editar", "Usar en Try-On", "Eliminar" (error color)
```

### LookCard

```dart
// lib/shared/widgets/molecules/look_card.dart
// USO: S08 grid de collections
// Props: tryOn TryOnResult, onTap VoidCallback, onShare VoidCallback

// - aspect ratio: 3:4 portrait
// - imagen: BoxFit.cover, radius AppRadius.lg (16px)
// - shadow: AppShadows.ambient1
// - overlay bottom: LinearGradient(transparent → Color(0x99000000)), bottom 60%
// - fecha: labelCaps, white, bottom-left sobre overlay
// - boton share: circle 36px, white 80%, icono share, AppColors.secondary
//   si free tier: tap → navegar a S10 Paywall con trigger='share_attempt'
```

### ErrorView

```dart
// lib/shared/widgets/molecules/error_view.dart
// USO: S11 estados de error
// Props:
//   type: ErrorType {notFound, networkError, tryOnFailed, generic}
//   onPrimary: VoidCallback
//   onSecondary: VoidCallback? (null = no mostrar)
//   primaryLabel: String
//   secondaryLabel: String?

// Cada tipo carga su ilustracion SVG desde assets/illustrations/
// notFound      → error_404.svg
// networkError  → error_network.svg
// tryOnFailed   → icono material error_outline 48px (no SVG custom)
// generic       → icono material error_outline 48px
```

---

## 5. SPECS POR PANTALLA — RESUMEN EJECUTIVO

### S01 — Splash / Onboarding

**Flujo:**
1. Splash 500ms → si JWT valido → Home, si no → Onboarding Slide 1
2. 3 slides con PageView horizontal
3. Slide 3 tiene GradientButton "Comenzar gratis" + link "Ya tengo cuenta"

**Componente:** OnboardingSlide (hero SVG + h2 + bodyMd + dots + CTA)

**Animaciones:**
- Slide transition: 300ms easeInOut
- Hero image enter: scale 0.85→1.0 + fade, 400ms easeOut
- Texto enter: slide +16px + fade, delay 150ms, 300ms
- Dot activo: expand 6px→24px pill + gradient, 200ms

**Assets SVG necesarios:**
- `onboarding_slide_1.svg` — figura femenina, overlay IA, trazos azul-violeta
- `onboarding_slide_2.svg` — closet organizado, prendas por colores
- `onboarding_slide_3.svg` — paleta de colores personal, silueta

---

### S02 — Login

**Componentes:** Input (5 estados), GradientButton, GoogleSignInButton (OutlineButton + G logo)

**Input estados:**
```
Default:  border 1px outlineVariant (#C6C6CD)
Focus:    border 2px secondary (#0058BE)
Error:    border 2px error (#BA1A1A) + caption error debajo
Filled:   border 1px outline (#76777D) + check_circle suffix verde
Disabled: bg surfaceContainerHighest, opacity 0.6
```

**Endpoints:**
- POST /api/v1/auth/login → JWT
- POST /api/v1/auth/google → JWT (Google OAuth)

---

### S03 — Register

**Adicional vs S02:**
- Password strength bar: 4 segmentos, colores error/warning/outline/success
- Checkbox terminos: CheckboxListTile, secondary al marcar
- GradientButton disabled hasta que todos los campos esten validos + checkbox marcado

**Validacion live:**
- Email: regex basico, check en onChanged
- Password: min 10 chars, 1 letter, 1 digit — helperText cambia en tiempo real
- Nombre: min 2 chars

**Endpoint:** POST /api/v1/auth/register

---

### S04 — Virtual Try-On (3 sub-estados)

**Estado A — Upload:**
- UploadZone grande (min 280px) para foto personal
- Grid ClothingSlots 2 columnas, aspect 1:1, max 5
- Tap slot vacio → BottomSheet: "Desde Mi Closet" / "Subir nueva foto" (D2 hybrid)
- D3 soft CTA body analysis: card primaryFixed, visible si user sin body_analysis
- Free tier counter: TryOnCounterPill en header
- GradientButton disabled si no hay foto personal

**Estado B — Loading:**
- GradientLoaderCard (ver componente)
- Textos rotativos S04: "Analizando proporciones...", "Combinando colores...", "Aplicando tu look ideal...", "Casi listo..."
- Polling GET /try-ons/{id} cada 3s con jitter (random 2-4s)
- Boton cancelar aparece a los 20s

**Estado C — Resultado:**
- Imagen resultado 2:3 portrait, full width con gutter 24px
- AIInsightCard: "Por que funciona" con texto IA
- Botones: Guardar (GradientButton) + Compartir (OutlineButton)
- Compartir free → Paywall S10 con trigger='share_attempt'
- Compartir paid → SharePlatformSheet (Instagram Stories, WhatsApp, Feed)
- "Nuevo Try-On" TextButton → volver a Estado A

**Endpoint:** POST /api/v1/try-ons → 202 {job_id} → polling GET

---

### S04B — Loading State

Ver GradientLoaderCard en componentes molecules.

**Textos S04B:** "Analizando proporciones...", "Combinando colores y estilos...", "Aplicando tu look ideal...", "Finalizando detalles...", "Casi listo, valio la pena esperar..."
**durationMs:** 45000 (45 segundos max)
**Boton cancelar:** visible a los 20s, onCancel → volver a S04 Estado A

---

### S05 — My Wardrobe

**Estructura:**
- Header: "Mi Closet" + GradientButton circle 40px (+)
- Filtros scrollables: Todos/Tops/Pantalones/Vestidos/Zapatos/Accesorios
- GridView 2 cols, gap 12px, WardrobeCard
- Empty state: empty_wardrobe.svg + GradientButton

**Add prenda:** DraggableScrollableSheet
- UploadZone mini (200px height, icono camera_alt)
- Select categoria (Dropdown), Input talla, Input marca (todos opcionales)
- GradientButton "Guardar prenda" disabled si no hay foto

**Paginacion:** pageSize 20, infinite scroll con SkeletonCard al pie
**Delete:** AlertDialog confirmacion antes de DELETE /wardrobe/items/{id}

**Endpoints:** GET/POST /api/v1/wardrobe/items, PATCH/DELETE /api/v1/wardrobe/items/{id}

---

### S06 — Style Insights + Soft Cap

Ver `docs/mockups/S06_SOFT_CAP_UI_DESIGN.md` para el diseno completo.

**Resumen ejecutivo:**
- Estado A (sin analisis): 2 cards descriptivos + GradientButton "Iniciar analisis"
- Estado B (con analisis): Results card → 300ms delay → SoftCapBottomSheet (si cap reached)
- TryOnCounterPill siempre en header
- Soft cap: 4 variants A-D segun SoftCapVariantSelector

**Endpoints:**
- GET /api/v1/body-analysis → BodyAnalysisResult o null
- GET /api/v1/users/me/usage → UsageStatus (incluye soft_cap_reached, soft_cap_variant)

---

### S07 — Body Analysis Upload

**Identico a S04 upload pero:**
- Instrucciones: card bg primaryFixed (#DCE2F7), lista de tips
- UploadZone: icono person, aspecto 3:4, titulo "Tu foto de cuerpo completo"
- CTA: "Analizar mi figura" → POST /body-analysis → GradientLoaderCard
- Textos loading S07: "Detectando silueta...", "Analizando proporciones...", "Calculando temporada de color...", "Casi listo..."
- Redirige a S06 Estado B con resultados

**durationMs:** 20000 (20 segundos body analysis)

---

### S08 — Collections

**Grid:** 2 columnas, LookCard 3:4 portrait
**Filtros:** Recientes / Favoritos (2 FilterChips)
**LookCard:** overlay gradient bottom + fecha + boton share circle
**Free share:** deshabilitado, tap → S10 Paywall

**Detalle look (tap card):** Full screen o DraggableScrollableSheet
- Imagen grande + AIInsightCard completo
- Guardar (GradientButton) + Compartir (OutlineButton)
- SharePlatformSheet: Instagram Stories / WhatsApp / Feed + referral info

**Empty state:** empty_collections.svg + GradientButton → S04

**Endpoints:** GET /api/v1/try-ons?liked=true

---

### S09 — Profile / Settings

**Header:** CircleAvatar 80px (iniciales o foto), nombre, email, PlanBadge, "Mejorar Plan" si free
**Branding D1:** card sutil con logo "AI Fit Check" + tagline
**Config items (ProfileSettingTile x 6):** Notificaciones (toggle), Idioma, Privacidad, Terminos, Calificar, Cerrar sesion (error color)
**Logout:** AlertDialog → DELETE token → pushAndRemoveUntil(LoginScreen)

**Endpoints:** GET/PATCH /api/v1/users/me

---

### S10 — Paywall

**Header:** Container 200px, primaryGradient, crown icon, "+50K usuarios activos" badge
**Cards:** Free (dim) + Estilo (highlighted, border secondary) + Imagen (dark, primaryContainer)

**Trigger banners (si viene de otra pantalla):**
```dart
if (trigger == 'try_on_limit') {
  // banner arriba: bg errorContainer, texto "Agotaste tu try-on del dia"
}
if (trigger == 'share_attempt') {
  // banner arriba: "Compartir disponible desde el plan Estilo"
}
```

**CTAs:**
- Estilo: GradientButton "Empezar con Estilo" → checkout Stripe
- Imagen: SolidButton (bg white, text primary) "Ir a Imagen" → checkout Stripe

**Post-pago:** GET /users/me para verificar nuevo plan → dismiss paywall + snackbar exito

**Endpoints:** POST /api/v1/subscriptions/stripe/checkout {tierId: 'estilo'|'imagen'}

---

### S11 — Error States

**S11a — Skeleton Loading:**
- SkeletonCard(width, height, radius) con shimmer blanco 30%
- Usar en todas las pantallas mientras carga (reemplaza GridView/ListView)
- Package sugerido: shimmer ^3.0.0

**S11b — 404:** error_404.svg + h1 "404" + h3 + GradientButton "Volver al inicio"

**S11c — Sin conexion:** error_network.svg + h2 + GradientButton "Reintentar" + spinner si retry activo

**S11d — Try-On fallido:** icono error_outline 48px (error color) + h2 + "no fue descontado." + GradientButton "Intentar de nuevo" + OutlineButton "Contactar soporte"

---

## 6. ASSETS SVG NECESARIOS

Crear en `frontend/assets/illustrations/`. Estilo: lineal minimalista, trazos AppColors.onSurfaceVariant (#45464C), no fotorrealistas.

### Prioridad 1 — Antes de Wave 1 Figma (DOM 21)
- [ ] `error_network.svg` — wifi cortado, nube rota, 200x180px
- [ ] `error_404.svg` — personaje con lupa buscando algo, 240x200px

### Prioridad 2 — Wave 2 (MAR-JUE 21-22)
- [ ] `body_type_pear.svg` — silueta pera, trazo negro lineal, 120x160px
- [ ] `body_type_rectangle.svg` — silueta rectangulo
- [ ] `body_type_inverted_triangle.svg` — triangulo invertido
- [ ] `body_type_hourglass.svg` — reloj de arena
- [ ] `body_type_oval.svg` — oval / manzana

### Prioridad 3 — Wave 3 (JUE-SAB 23-25)
- [ ] `empty_wardrobe.svg` — perchas vacias, 200x180px
- [ ] `empty_collections.svg` — camara + estrella, 200x180px
- [ ] `onboarding_slide_1.svg` — figura femenina + overlay IA, 280x320px
- [ ] `onboarding_slide_2.svg` — closet organizado, 280x300px
- [ ] `onboarding_slide_3.svg` — paleta de colores, 280x300px

**Nota de generacion:** Usar Nano Banana 2 + Claude Banana para prompts profesionales de ilustracion SVG. Prompt base para body_type: "lineal flat illustration, minimal strokes, single color #45464C, white background, [body shape] silhouette, fashion-forward, no shading, SVG exportable."

---

## 7. ANIMACIONES — REFERENCIA COMPLETA

### Duraciones estandar

| Tipo | Duracion | Easing |
|------|----------|--------|
| Micro (feedback touch) | 100-150ms | easeOut |
| Transicion estado | 200-300ms | easeInOut |
| Enter page/card | 300-400ms | easeOut |
| Shimmer GradientLoader | 1800ms | easeInOut PingPong |
| Texto rotativo | 5000ms interval / 300ms cross-fade | linear |
| Soft cap slide-up | 300ms | easeOut |
| Counter cambio numero | 200ms | AnimatedSwitcher |

### Page transitions

```dart
// Dentro de la app (NavigationBar tab switch):
// Fade: opacity 0 → 1, 200ms

// Push (ir a pantalla nueva):
// CupertinoPageRoute o MaterialPageRoute con custom SlideTransition
// from: Offset(1.0, 0) → Offset(0, 0), 300ms, Curves.easeOut

// Pop (volver):
// Offset(0, 0) → Offset(1.0, 0), 250ms, Curves.easeIn

// Modal / BottomSheet:
// Offset(0, 1) → Offset(0, 0), 350ms, Curves.easeOut
// DraggableScrollableSheet para dismiss
```

### Micro-interacciones

```dart
// Boton tap (GradientButton, OutlineButton):
// GestureDetector → onTapDown: scale 0.97, onTapUp: scale 1.0, 100ms each
// Implementar con AnimatedScale o Transform.scale

// Heart button save (Collections):
// Scale pulse: 1.0 → 1.2 → 1.0, 300ms, ElasticOutCurve
// Color change: outline → error (#BA1A1A) filled, AnimatedContainer

// ClothingSlot fill:
// FadeTransition opacity 0 → 1, 250ms

// Results card enter (S06):
// opacity 0 + translateY +24px → visible, 400ms easeOut

// Counter cambio:
// AnimatedSwitcher, 200ms, fade + scale 0.8 → 1.0
```

---

## 8. NAVEGACION — ESTRUCTURA FLUTTER

```dart
// lib/core/navigation/app_router.dart

// Auth routes (sin NavigationBar):
// /splash           → SplashScreen
// /onboarding       → OnboardingScreen (PageView)
// /login            → LoginScreen
// /register         → RegisterScreen

// App routes (con NavigationBar bottom):
// /home             → VirtualTryOnScreen (Tab 0 - default)
// /wardrobe         → WardrobeScreen (Tab 1)
// /style-insights   → StyleInsightsScreen (Tab 2)
// /collections      → CollectionsScreen (Tab 3)

// Utilitarias (push sobre cualquier tab):
// /profile          → ProfileScreen
// /paywall          → PaywallScreen (requiere trigger param)
// /body-analysis    → BodyAnalysisUploadScreen

// NavigationBar (mobile < 600dp):
//   Tab 0: Icons.auto_awesome_outlined / auto_awesome (activo) - "Try-On"
//   Tab 1: Icons.checkroom_outlined / checkroom (activo) - "Closet"
//   Tab 2: Icons.person_search_outlined / person_search (activo) - "Estilo"
//   Tab 3: Icons.collections_outlined / collections (activo) - "Looks"

// NavigationRail (tablet >= 600dp): mismo orden, lateral izquierdo
```

---

## 9. QA VISUAL CHECKLIST

Usar al terminar cada pantalla antes del handoff:

### Tokens
- [ ] Todos los colores de AppColors (ningun hardcode #HEX fuera de AppColors)
- [ ] Tipografia de AppTypography (sin fontSize hardcodeado)
- [ ] Spacing de AppSpacing (multiples de 4px o 8px estrictos)
- [ ] Radius de AppRadius (sm/DEFAULT/md/lg/xl/full — sin valores sueltos)
- [ ] Sombras de AppShadows (ambient1/ambient2 — sin box-shadow manual)

### Componentes
- [ ] GradientButton: maximo 1 por pantalla visible simultaneamente
- [ ] Gradiente NO en fondos de pantalla completa
- [ ] AIInsightChip: solo en contenido generado por IA
- [ ] PlanBadge: correcto por tier del usuario actual

### Accesibilidad
- [ ] Touch targets minimo 48x48px en todos los botones (WCAG 2.1 AA)
- [ ] Texto suficiente contraste (usar tokens — todos estan testeados)
- [ ] Safe areas respetadas: top 59px, bottom 34px
- [ ] Inputs con labels visibles (no solo placeholder)

### Estados
- [ ] Empty states disenados (S05 wardrobe vacio, S08 collections vacio)
- [ ] Error states manejados (usa S11 ErrorView con tipo correcto)
- [ ] Loading states: SkeletonCard o GradientLoaderCard segun caso
- [ ] Disabled states: opacity 0.4, no-gradient si aplica

### Decisiones D1-D5
- [ ] D1: "AI Fit Check" visible en header de cada pantalla (labelCaps)
- [ ] D2: S04 muestra UploadZone prominente, wardrobe como opcion secundaria
- [ ] D3: S04 result tiene soft CTA body analysis (card primaryFixed, dismiss available)
- [ ] D4: TryOnCounterPill visible en S04 y S06 si usuario es free tier
- [ ] D5: Boton Compartir en S04C y S08, gateado por tier

---

## 10. PROTOCOLO DE ENTREGA — SAB 25 EOD

Cuando todo este listo, Erik entrega a Brook:

```markdown
## Entrega Erik — Sprint Design — 2026-05-25

### Figma
[link al archivo — por confirmar]
Organizacion de frames:
  - Auth: S01, S02, S03
  - Try-On: S04 (3 estados), S04B
  - Wardrobe: S05
  - Style Insights: S06 (2 estados + soft cap variants)
  - Body Analysis: S07
  - Collections: S08
  - Utilities: S09, S10, S11 (4 estados)

### Assets exportados (disponibles en /frontend/assets/illustrations/)
  [lista de 13 SVG con status de cada uno]

### Tokens
  Sin cambios vs DESIGN_SYSTEM.md — usar ese como fuente de verdad.

### Notas de implementacion
  Ver cada pantalla en DESIGN_HANDOFF_S01-S11.md y ERIK_SPRINT_DESIGN_SPECS.md.

### QA Visual
  Usar checklist seccion 9 de este documento.
  Comparar screenshot simulador vs specs ASCII de ERIK_SPRINT_DESIGN_SPECS.md.
  Discrepancias > 8px de spacing o colores incorrectos → abrir issue en GitHub.
```

---

**Owner:** Erik
**Fecha creacion:** 2026-05-20
**Ultima actualizacion:** 2026-05-20
**Estado:** Wave 1 completado (specs S06 + S07 + S04B + S11) — Figma pendiente
**Proximo update:** LUN 21 (Wave 2 specs S05+S08) / MIE 22 (Wave 3 specs S01-S04 refinado)
**Handoff final:** SAB 25 mayo 2026
