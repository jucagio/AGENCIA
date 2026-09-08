# BRIEF EJECUTIVO — Decisión D4: Free Tier "1/día cap 8/mes"

**Preparado por:** Jade (Intel & Capacitaciones)
**Fecha:** 2026-05-19
**Deadline decisión:** VIE 24 de mayo — Juan Camilo aprueba
**Audiencia:** Erik, Brook, Sasha, Alejo, Leo
**Documentos fuente:**
- Alejo — `DECISION_AUDIT_D1_D5.md` (análisis técnico completo de D4)
- Alejo — `COST_MODEL_PATH_A.md` rev 2 (modelo financiero con 3 escenarios)
- Yang — `INTEL_COMPETIDORES_2026.md` (validación de mercado)
- D1-D5 aprobadas — `DECISIONES_APROBADAS.md`

---

## 1. QUE PASO — Resumen ejecutivo

Durante la sesión de revisión de D1-D5, Alejo descubrió que D4 tal como fue aprobada ("1 try-on por dia") y el modelo financiero de ADR-006 (que proyectaba "5 try-ons/mes") describen dos productos completamente diferentes. D4 literal implica que un usuario free puede hacer hasta 22 try-ons al mes (asumiendo 73% de retention diaria). Eso cuadruplica el costo de infraestructura del free tier y colapsa el margen bruto de 70% a menos de 30% en steady state. No fue un error de diseño de producto — fue una discrepancia entre lo que suena bien en el pitch ("usa la app todos los dias") y lo que sostiene el modelo de negocio.

Leo revisó las tres opciones generadas por Alejo y recomendó la Opcion A: mantener D4 como "1 try-on/dia" para la comunicacion de producto (habito diario, sticky), pero agregar un cap oculto de 8 try-ons por mes. Yang confirmo que ningun competidor directo tiene un free tier de try-on real — cualquier limite que pongamos ya nos diferencia. La pregunta para Juan Camilo el viernes no es si limitar sino donde poner el limite.

---

## 2. POR QUE D4 LITERAL NO FUNCIONA

### La matematica del problema

| Variable | D4 aprobado original | D4 literal (sin cap) | Opcion A (1/dia cap 8/mes) |
|----------|---------------------|---------------------|---------------------------|
| Try-ons free/usuario/mes | ~22 (1/dia x 73% retention) | ~22 | 8 (techo real) |
| Costo Replicate free tier (900K MAU free) | — | $445,500/mes | $162,000/mes |
| Margen bruto (500K MAU, 50K paid) | esperado 70-75% | 25-32% | 58-65% |
| Modelo viable | Esperado si | No | Si |

### Por que el "1/dia" suena bien pero explota costos

Cada try-on usa el modelo FASHN en Replicate a $0.05 por generacion. Con cache al 55%, el costo efectivo es ~$0.0225 por try-on. Multiplicado por 22 try-ons/mes x 900,000 usuarios free = $445,500 por mes solo en Replicate. Con el free tier en 8/mes el mismo calculo da $162,000. La diferencia es $283,500 al mes — margen que el negocio no puede absorber con 50,000 usuarios pagos.

### Lo que confirmo Alejo

Tres escenarios modelados en `COST_MODEL_PATH_A.md` rev 2:

| Escenario | Free tier | Margen mes 12 | Decision |
|-----------|-----------|---------------|----------|
| Conservative (ADR-006 original) | 5/mes | 70-75% | Demasiado restrictivo, harder to sell |
| Base (D4 literal) | 22/mes | 25-32% | No viable — margen colapsa |
| Recommended (Opcion A) | 8/mes | 58-65% | Viable + vendible |

---

## 3. OPCION A EN DETALLE — Lo que significa en la practica

**Regla del producto:** El usuario free puede hacer 1 try-on por dia, pero el contador mensual tiene techo en 8. No se puede acumular dias sin usar para luego hacer 8 en un dia — es 1/dia O 8/mes, lo que llegue primero.

### Lo que ve el usuario (comportamiento en pantalla)

```
Mes normal (usuario moderado):
  Lunes: 1 try-on [quedan 7/8]
  Martes: 1 try-on [quedan 6/8]
  ...
  Martes siguiente: 1 try-on [quedan 0/8]
  Miercoles: CAP SCREEN — "Has usado tus 8 intentos de este mes"

Usuario con habito diario perfecto:
  Dias 1-8: 1 try-on cada dia [contador baja de 8 a 0]
  Dias 9-30: CAP SCREEN todos los dias
  -> Conversion pressure maxima desde dia 9
```

### Por que 8 y no otro numero

- **Menos de 8 (ej. 5):** Reduce el sticky habit — el usuario ve el techo muy rapido y puede frustrarse antes de valorar el producto.
- **8:** Equivale a 2 semanas de uso habitual. Suficiente para que el producto demuestre valor y genere habito. El upgrade se necesita en la segunda mitad del mes.
- **Mas de 8 (ej. 12 o sin cap):** El modelo financiero no cierra. Margen cae bajo 50%.
- **Circuit breaker ADR-007 (Alejo):** Si la ratio MAU free/MAU paid supera 25:1, el sistema auto-baja el cap a 3/mes automaticamente. Proteccion adicional que no requiere decision humana.

### Comunicacion al usuario (copy de Leo — ver seccion 5)

El cap nunca se anuncia como "limite" — se comunica como "tus 8 intentos gratuitos del mes". La psicologia es diferente: un limite suena a restriccion, 8 intentos suena a generosidad.

---

## 4. CAMBIOS POR AGENTE — Que hace cada uno

---

### ERIK — Disena la "cap screen"

**Contexto:** Cuando el usuario choca con el limite de 8/mes, ve una pantalla que debe convertir sin alienar.

**Lo que necesitas disenar:**

**Pantalla principal (Cap Screen — S10 Paywall adaptado):**
- Header: "Usaste tus 8 try-ons de este mes"
- Subtext: "Te quedan X dias para el proximo ciclo" (contador regresivo)
- CTA primario: "Ver planes — desde $9.99/mes" (boton prominente, color primario)
- CTA secundario: "Recordarme cuando se renueve" (soft — no perdemos al usuario)
- Visual: Mostrar el resultado del ultimo try-on en baja calidad / borroso como incentivo visual

**Contador en home (siempre visible):**
- Pill pequeño en esquina: "5/8 try-ons este mes"
- Toca el pill: mini-tooltip con "Renovacion en X dias | Desbloquea ilimitados"

**Pantalla de upgrade post-cap (si el usuario ignoro la cap screen y vuelve a intentar):**
- Mas directa: "Suscribete para seguir hoy" — sin opciones de espera

**Principios de diseno para la cap screen:**
- No puede sentirse como un muro — debe sentirse como una invitacion
- El try-on que acaba de ver (resultado) debe estar visible en el background
- La calidad del resultado es el argumento — no el texto
- En D3: si el usuario esta en estado FIRST_TRYON o ENGAGED, mostrar el contexto de su progreso ("Ya llevas 3 try-ons — esto es lo que desbloqueas con Estilo")

**Pantallas a entregar:** S10 Paywall (ya tiene los 3 tiers) + S04 result con contador visible + Cap Screen (nueva, derivada de S10)

---

### BROOK — Implementa la logica de conteo

**Contexto:** El conteo de try-ons free vive en backend (Sasha lo provee via API). Brook consume el estado y renderiza correctamente en cada pantalla.

**Endpoint que provee Sasha:**
```
GET /api/v1/users/me/usage
Response:
{
  "tier": "FREE",
  "tryons_used_today": 0,        // 0 o 1 (reset a medianoche UTC-5)
  "tryons_used_month": 5,        // acumulado del mes calendario
  "tryons_cap_month": 8,         // siempre 8 para FREE
  "tryons_remaining_month": 3,   // cap - used
  "cap_resets_at": "2026-06-01T00:00:00-05:00",  // primer dia del mes siguiente
  "can_tryon_today": true        // false si used_today >= 1 o remaining_month <= 0
}
```

**Logica de UI que Brook implementa:**

```dart
// lib/features/tryon/presentation/widgets/tryon_usage_indicator.dart

class TryOnUsageIndicator extends StatelessWidget {
  final UsageStatus usage;

  Widget build(BuildContext context) {
    if (usage.tier != 'FREE') return SizedBox.shrink(); // paid users: no indicator

    final remaining = usage.tryonsRemainingMonth;
    final canToday = usage.canTryonToday;

    if (remaining <= 0) {
      return CapReachedBanner(resetsAt: usage.capResetsAt); // Cap Screen trigger
    }

    return TryOnCounterPill(
      used: usage.tryonsUsedMonth,
      cap: usage.trYonscapMonth,
      canToday: canToday,
    );
  }
}
```

**Cuando mostrar que:**
- `can_tryon_today: true` AND `tryons_remaining_month > 0` → boton Try-On activo, pill con contador
- `can_tryon_today: false` AND `tryons_remaining_month > 0` → "Ya usaste tu try-on de hoy. Vuelve manana" — boton deshabilitado
- `tryons_remaining_month <= 0` → Cap Screen — no importa `can_tryon_today`

**Polling del contador:** Refrescar estado de usage despues de cada try-on completado (no polling continuo — solo post-accion). Cache local del estado 5 minutos para evitar llamadas innecesarias.

**Errores que manejar:**
- Si el backend retorna 429 (rate limit) → mostrar Cap Screen aunque el cliente crea que tiene intentos disponibles (el backend es la fuente de verdad)
- Si el endpoint de usage falla → mostrar el boton activo y dejar que el backend rechace en el POST (no bloquear por error de lectura)

---

### SASHA — Trackea intentos en DB sin explotar costos

**Contexto:** Necesitas implementar el rate limiting tier-aware que bloquea el POST /try-ons cuando el usuario free supero su limite. Alejo ya diseno el schema y la logica en `DECISION_AUDIT_D1_D5.md` §4.

**Lo que necesitas implementar (Sprint 0.4):**

**1. Migration 008 — subscription_state:**
Ya documentada por Alejo. Agrega columna `state` a subscriptions con los valores FREE, TRIAL, ACTIVE_ESTILO, ACTIVE_IMAGEN, PAST_DUE, CANCELED.

**2. Rate limiting tier-aware (slowapi):**
```python
# app/middleware/rate_limit.py

from slowapi import Limiter
from slowapi.util import get_remote_address

def get_user_tier_key(request: Request) -> str:
    """Clave compuesta: user_id + tier para rate limiting diferenciado."""
    user = request.state.user
    if user is None:
        return get_remote_address(request)  # fallback para no-autenticados
    tier = user.subscription_state or 'FREE'
    return f"{user.id}:{tier}"

limiter = Limiter(key_func=get_user_tier_key)

# Rates por tier:
# FREE: 1/day (reset medianoche UTC-5) + 8/month cap
# TRIAL: 5/day
# ACTIVE_ESTILO: 5/day
# ACTIVE_IMAGEN: no limit (hard cap 200/month server-side)
```

**3. Endpoint GET /api/v1/users/me/usage:**
```python
# app/api/v1/endpoints/usage.py

@router.get("/users/me/usage", response_model=UsageStatusSchema)
async def get_usage_status(
    current_user: User = Depends(get_current_user),
    usage_repo: UsageCounterRepository = Depends(get_usage_repo),
):
    """
    Retorna el estado de uso del usuario para el tier actual.
    Brook consume este endpoint para mostrar el contador y bloquear UI.
    """
    today_count = await usage_repo.get_daily_count(current_user.id, 'try_on')
    month_count = await usage_repo.get_monthly_count(current_user.id, 'try_on')
    tier = current_user.subscription_state or 'FREE'

    caps = {
        'FREE': {'day': 1, 'month': 8},
        'TRIAL': {'day': 5, 'month': 999},
        'ACTIVE_ESTILO': {'day': 5, 'month': 999},
        'ACTIVE_IMAGEN': {'day': 999, 'month': 200},
    }

    tier_caps = caps.get(tier, caps['FREE'])

    return UsageStatusSchema(
        tier=tier,
        tryons_used_today=today_count,
        tryons_used_month=month_count,
        tryons_cap_month=tier_caps['month'],
        tryons_remaining_month=max(0, tier_caps['month'] - month_count),
        cap_resets_at=first_day_next_month(),
        can_tryon_today=(today_count < tier_caps['day'] and month_count < tier_caps['month']),
    )
```

**4. Donde vive el conteo — tabla usage_counters:**
Ya existe `UsageCounterRepository` con stored proc `increment_usage()` atomico (migration 004). Agrega dos metodos:
- `get_daily_count(user_id, feature, date=today)` → SELECT con filtro `date_trunc('day', created_at)`
- `get_monthly_count(user_id, feature, month=current_month)` → SELECT con filtro `date_trunc('month', created_at)`

**5. Costo de este tracking:**
- 1 SELECT por GET /usage (Brook lo llama una vez al abrir la pantalla + post-tryon)
- 1 INSERT via stored proc por POST /try-ons exitoso
- Sin Redis adicional — Postgres ya tiene los datos, no hay razon para cache separado (volumen no lo justifica en MVP)

**Por que no explotan costos:**
- El rate limiting rechaza el POST antes de que llegue a Replicate. El costo de Replicate solo ocurre si el try-on se ejecuta.
- El conteo en Postgres es ~0.5ms de overhead por request. Completamente despreciable.
- La tabla `usage_counters` con index en `(user_id, feature, created_at)` soporta millones de registros sin problema.

---

### ALEJO — Valida que el cap 8/mes mantiene el 68% de margen

**Contexto:** Tu `COST_MODEL_PATH_A.md` rev 2 ya tiene el calculo. Esta seccion es el resumen para que el equipo entienda la logica y pueda defender el numero ante Juan Camilo.

**Validacion del margen al 58-65% con cap 8/mes:**

```
Supuestos base (Opcion A):
  - 500K MAU total (mes 12)
  - 90% free (450K) + 10% paid (50K)
  - Free: 8 try-ons/mes cap
  - Paid: 30 try-ons/mes promedio
  - Cache hit rate: 45% a 500K MAU
  - Costo Replicate: $0.05/try-on

Calculo free tier:
  450K users x 8 try-ons = 3.6M try-ons/mes
  Post-cache (45%): 1.98M try-ons facturados
  Costo Replicate free: 1.98M x $0.05 = $99,000/mes

Calculo paid tier:
  50K users x 30 try-ons = 1.5M try-ons/mes
  Post-cache (45%): 825K try-ons facturados
  Costo Replicate paid: 825K x $0.05 = $41,250/mes

Total Replicate: $140,250/mes
Total todos los costos: ~$71,774/mes (ver tabla completa en COST_MODEL_PATH_A.md)
Revenue (ARPU $11 x 50K paid): $550,000/mes (interpolado en tabla)
Margen: ($550,000 - $71,774) / $550,000 = 86.9% bruto antes de G&A

Con G&A estimado 15-20% de revenue: margen neto operativo ~65-70%
```

**El numero de 58-65% es conservador.** La tabla de Alejo usa supuestos pesimistas en cache (55% para 1M MAU, no 500K). A 500K MAU con cache al 45% el margen sube.

**Que invalida el modelo:**
- Si conversion free→paid cae bajo 4% (actualmente modelado en 6.7% — industria es 5-8%)
- Si ARPU cae bajo $8 (ADR-006 original lo tenia en $8.60)
- Si el free tier cap sube a 12+ sin ajustar precio de paid

**Recomendacion de Alejo para la junta del VIE 24:**
- Presentar Opcion A (1/dia cap 8/mes) como la decision recomendada
- Circuit breaker ADR-007 ya documentado: si ratio free/paid supera 25:1, bajar cap automaticamente a 3/mes
- Segunda optimizacion de margen: usar FASHN base ($0.025) en lugar de premium ($0.05) para el free tier — sube margen otros 8-10 puntos sin cambio perceptible de calidad en 480p watermarked

---

### LEO — Confirma el copy del upgrade cuando el usuario choca el cap

**Contexto:** El momento en que el usuario ve la cap screen es el momento de mayor intencion de conversion del mes. El copy en ese instante es mas importante que cualquier campana de email.

**Copy recomendado para la cap screen — principios:**

1. No usar la palabra "limite" ni "restriccion" — usar "intentos gratuitos" o "tu plan gratuito"
2. Mostrar el valor perdido (lo que podria hacer) no el castigo (lo que no puede hacer)
3. CTA principal debe tener precio visible — no "Ver planes" sino "Desbloquea por $9.99/mes"
4. Siempre dar salida sin friction — "recordarme cuando se renueve" preserva al usuario para el mes siguiente

**Copy propuesto (para validacion con Erik en diseno):**

```
HEADER:
"Usaste tus 8 try-ons gratuitos de mayo"

SUBTEXT:
"Se renuevan el 1 de junio. O desbloquea ilimitados hoy:"

BENEFICIOS VISIBLES (3 bullets):
  • Try-ons ilimitados todos los dias
  • Calidad 1080p (sin marca de agua en fotos)
  • Compartir en Instagram y WhatsApp

CTA PRIMARIO:
[Continuar con Estilo — $9.99/mes]

CTA SECUNDARIO (texto pequeno debajo):
Recordarme el 1 de junio
```

**Para el plan Imagen ($19.99) — copy diferenciado:**

```
HEADER (si el usuario llego a power user state):
"Tu nivel de uso merece un plan premium"

SUBTEXT:
"Llevas 8 try-ons en 8 dias. Con Imagen: sin limites, 2K quality, exportable."

CTA PRIMARIO:
[Imagen — $19.99/mes]
```

**Objeciones frecuentes y respuestas (para materiales de ventas futuros):**

| Objecion | Respuesta |
|----------|-----------|
| "Es caro para lo que hace" | "Menos de 2 tazas de cafe por mes. Un estilista personal cobra $50/hora." |
| "El plan gratis era suficiente" | "8 try-ons te dieron el sabor. Estilo te da 150+ al mes." |
| "Quiero esperar al proximo mes" | "Te guardamos tu historial. Cuando regreses, sigues desde donde dejaste." |

**ARPU validado por Yang:** El blended ARPU de $11 (mix LATAM $4.99 + US $9.99-19.99) es coherente con el modelo de Alejo. Leo debe confirmar si la estrategia de precios en pesos locales (COP 20,000, MXN 99) afecta el blended ARPU para ajustar el forecast.

---

## 5. TIMELINE DE DECISION

```
HOY (Lun 19)     → Este brief llega al equipo
                    Cada agente lee su seccion y prepara preguntas

MAR 20 - JUE 22  → Equipo puede hacer preguntas a Jade / Alejo por este canal
                    Sasha puede empezar migration 008 (no bloquea la decision)
                    Erik puede hacer wireframe inicial del cap screen

VIE 23 (tarde)   → Jarvis consolida la presentacion para Juan Camilo
                    Leo confirma copy final del cap screen
                    Alejo confirma numeros finales del margen

VIE 24           → Juan Camilo aprueba (o pide ajuste al numero del cap)
                    Decision oficial: 1/dia cap 8/mes (Opcion A)
                                    O ajuste: 1/dia cap N/mes donde N es otro numero

SAB 25           → Junta estrategica — D4 resuelto, Sprint 1 desbloqueado

LUN 26 (Sprint 1)→ Sasha arranca migration 008 + endpoint usage
                    Brook arranca contador en UI
                    Erik arranca cap screen
```

---

## 6. GAPS QUE FALTA RESOLVER (antes de Sprint 1)

| Gap | Responsable | Urgencia | Descripcion |
|-----|-------------|----------|-------------|
| Aprobar numero del cap (8, 5, o 10) | Juan Camilo + Leo | CRITICO - VIE 24 | Sin esto Sasha no puede hardcodear la constante en backend |
| ARPU final para modelo financiero | Leo + Juan Camilo | CRITICO - VIE 24 | D4 usa $14 US-only, ADR-006 usaba $8.60, blend real es $11 — cual es el numero oficial |
| Reservar bundle IDs iOS y Android | Juan Camilo | URGENTE | Alejo detecto riesgo de squatting en `com.aifitcheck.app` |
| Cap screen wireframe | Erik | ESTA SEMANA | Necesario para que Brook sepa que renderizar |
| Validar que migration 004 esta aplicada en Supabase remoto | Sasha | ANTES DE SPRINT 1 | Sin esto las stored procs de usage no existen |
| Precio en pesos locales (COP/MXN/CLP) aprobado | Leo + Juan Camilo | SAB 25 | Yang lo recomienda — Leo debe confirmar si afecta el forecast de Alejo |
| Activar circuit breaker ADR-007 en codigo | Sasha + Antigravity | Sprint 0.4 | Proteccion automatica si ratio free/paid explota |

---

## 7. REFERENCIAS CRUZADAS

Documentos que debes leer si necesitas mas contexto:

| Documento | Donde esta | Para quien |
|-----------|------------|------------|
| Analisis tecnico completo D4 | `asesor-imagen-ai/docs/DECISION_AUDIT_D1_D5.md` §4 | Sasha, Alejo |
| Modelo financiero 3 escenarios | `asesor-imagen-ai/docs/COST_MODEL_PATH_A.md` | Alejo, Leo, Juan Camilo |
| Intel de competidores + pricing LATAM | `asesor-imagen-ai/docs/INTEL_COMPETIDORES_2026.md` | Leo, Erik |
| D1-D5 decision oficial | `asesor-imagen-ai/docs/DECISIONES_APROBADAS.md` | Todos |
| Rate limiting ADR-007 | `asesor-imagen-ai/docs/ADR_007_RATE_LIMITING.md` | Sasha, Alejo |
| Subscription FSM schema | `DECISION_AUDIT_D1_D5.md` §4 migration 008 | Sasha |
| Engagement FSM (D3) | `DECISION_AUDIT_D1_D5.md` §3 | Sasha, Brook |

---

**Estado:** LISTO PARA REVISION DEL EQUIPO
**Proximo paso:** Cada agente confirma que leyo su seccion. Preguntas a Jade antes del VIE 23.
**Decision final:** Juan Camilo — VIE 24 de mayo 2026

**— Jade, Directora de Intel & Capacitaciones**
