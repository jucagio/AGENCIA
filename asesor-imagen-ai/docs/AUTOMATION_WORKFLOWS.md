# Asesor de Imagen AI — Automation Workflows
**Diseñado por:** Cinthya (Especialista en Automatización)
**Fecha:** 2026-04-25
**Estado:** DISEÑO — listo para implementar cuando Sasha tenga endpoints Sprint 1-2
**Herramienta principal:** n8n self-hosted (Railway)

---

## Indice

1. [Stack de Integraciones](#1-stack-de-integraciones)
2. [Webhook Architecture](#2-webhook-architecture)
3. [Workflow 1 — Welcome Onboarding](#workflow-1-welcome-onboarding)
4. [Workflow 2 — Activation Milestones](#workflow-2-activation-milestones)
5. [Workflow 3 — Free Tier Limit Warning + Upgrade Nudge](#workflow-3-free-tier-limit-warning--upgrade-nudge)
6. [Workflow 4 — Trial Expiration Nudge](#workflow-4-trial-expiration-nudge)
7. [Workflow 5 — Failed Payment / Dunning](#workflow-5-failed-payment--dunning)
8. [Workflow 6 — Weekly Digest](#workflow-6-weekly-digest)
9. [Workflow 7 — Win-Back (Churned Users)](#workflow-7-win-back-churned-users)
10. [Workflow 8 — Referral Program](#workflow-8-referral-program)
11. [KPIs por Workflow](#kpis-por-workflow)
12. [Compliance](#compliance)
13. [Variables de Entorno Globales](#variables-de-entorno-globales)

---

## 1. Stack de Integraciones

### Decision Matrix

| Servicio | Opcion Elegida | Alternativa | Justificacion | Costo inicial |
|----------|---------------|-------------|---------------|---------------|
| **Email transaccional** | **Resend** | Postmark, SendGrid | API moderna, DX excelente, 100 emails/dia gratis, SDK oficial para FastAPI, mejor deliverability en LATAM que SendGrid Free | Free: 3k/mes. Pro: $20/mes (50k emails) |
| **Push notifications** | **OneSignal** | Firebase FCM | FCM es gratis pero requiere implementacion manual en Flutter; OneSignal tiene SDK Flutter oficial, segmentacion avanzada, A/B testing de push incluido, dashboard analitico. Para <10k MAU es completamente gratis | Free hasta 10k subs |
| **CRM** | **Brevo (ex-Sendinblue)** | HubSpot Free, Customer.io | HubSpot Free no tiene automation flows; Customer.io es $100+/mes minimo. Brevo tiene automation flows, CRM basico, y 300 emails/dia gratis. Cuando escale a $5k MRR migrar a Customer.io | Free hasta 300 emails/dia |
| **Workflows** | **n8n self-hosted (Railway)** | n8n Cloud | Control total, datos sensibles no salen del entorno, Railway starter $5/mes. n8n Cloud seria $20-50/mes sin la flexibilidad de self-hosted | $5/mes Railway |
| **Analytics events** | **PostHog** | Mixpanel, Amplitude | Open source, self-hosteable, tiene feature flags que usaremos para rollout gradual, sessions recording, funnels. Free cloud hasta 1M eventos/mes. Mixpanel es mas costoso y Amplitude no tiene tier tan generoso | Free hasta 1M eventos |

### Resumen de costos Mes 1 (pre-revenue)

```
n8n Railway:        $5/mes
Resend Free:        $0 (hasta 3k emails/mes)
OneSignal Free:     $0 (hasta 10k subs)
Brevo Free:         $0 (hasta 300 emails/dia)
PostHog Cloud:      $0 (hasta 1M eventos)
Stripe:             2.9% + $0.30 por transaccion (cero fijo)
MercadoPago:        3.49% + $0.49 (LATAM)
--------------------------------------------------
TOTAL FIJO:         $5/mes
```

Cuando el MRR supere $2k/mes escalar a Resend Pro ($20) y evaluar Customer.io.

---

## 2. Webhook Architecture

### Diagrama de flujo completo

```
+-----------------+     +-----------------+     +------------------+
| Flutter App     |     | FastAPI Backend |     | Supabase         |
| (eventos UI)    |---->| /webhooks/      |     | (database hooks) |
+-----------------+     | internal        |     +--------+---------+
                        +--------+--------+              |
                                 |                       | pg_net / supabase
                                 |                       | webhooks
                                 v                       v
                        +--------+------------------------+
                        |           n8n (Railway)         |
                        |    Webhook Receiver Central     |
                        |    URL: https://n8n.railway/    |
                        |         webhook/{tipo}          |
                        +---+---+---+---+---+-------------+
                            |   |   |   |   |
              +-------------+   |   |   |   +------------------+
              |                 |   |   |                       |
              v                 v   |   v                       v
    +---------+-----+   +-------+-+ | +-+-------+    +---------+-----+
    | Resend Email  |   | OneSignal | | | Brevo   |    | PostHog       |
    | (transac)     |   | (push)    | | | (CRM)   |    | (analytics)   |
    +---------------+   +-----------+ | +---------+    +---------------+
                                      |
                                      v
                            +---------+-----+
                            | Slack/Telegram |
                            | (ops alerts)   |
                            +---------------+

Stripe/MercadoPago webhooks → FastAPI → n8n interno
```

### Idempotencia

Cada evento que llega a n8n incluye un `event_id` unico generado por la fuente.

**Patron de idempotencia en n8n:**

```
Webhook recibe payload
    |
    v
[Code node] Extraer event_id
    |
    v
[Supabase node] SELECT FROM webhook_processed WHERE event_id = $1
    |
    +-- Si YA existe → Stop (return 200, no action)
    |
    +-- Si NO existe → INSERT webhook_processed (event_id, processed_at)
                    → Continuar con el workflow
```

**Tabla requerida en Supabase** (agregar a migration 003):

```sql
CREATE TABLE public.webhook_processed (
    event_id TEXT PRIMARY KEY,
    workflow_name TEXT NOT NULL,
    processed_at TIMESTAMPTZ DEFAULT now()
);

-- Auto-delete despues de 30 dias (no necesitamos historico largo)
CREATE INDEX idx_webhook_processed_at ON webhook_processed(processed_at);
```

### Retry Logic (Exponential Backoff)

n8n tiene retry nativo en nodos HTTP Request. Configuracion estandar para todos los workflows:

```
Max retries: 3
Retry intervals: 1s → 4s → 16s (exponential)
On final failure: → Dead Letter Queue
```

En nodos criticos (email, push) agregar un nodo `Error Trigger` que capture el fallo y lo enrute al DLQ.

### Dead Letter Queue (DLQ)

**Implementacion:** Tabla Supabase + notificacion Slack

```sql
CREATE TABLE public.workflow_dlq (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_name TEXT NOT NULL,
    event_id TEXT,
    payload JSONB,
    error_message TEXT,
    retry_count INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now(),
    resolved_at TIMESTAMPTZ,
    resolved_by TEXT
);
```

Cuando un nodo falla despues de 3 reintentos:
1. n8n escribe a `workflow_dlq` via Supabase node
2. n8n envia alerta a Slack #ops-alerts con el error y payload
3. Jarvis/Cinthya revisa manualmente o re-dispara el workflow

### Monitoring

Metricas que n8n expone + alertas que configuramos:

| Metrica | Umbral de alerta | Canal |
|---------|-----------------|-------|
| Workflow execution failed | Cualquier fallo | Slack #ops-alerts |
| DLQ > 5 items en 1h | > 5 | Slack #ops-alerts + email Jarvis |
| Email delivery rate < 90% | < 90% | Slack #ops-alerts |
| Push delivery rate < 80% | < 80% | Slack #ops-alerts |
| Workflow latency > 30s | > 30s | Log (no alerta inmediata) |

---

## Workflow 1 — Welcome Onboarding

**Descripcion:** Secuencia de bienvenida de 72h para activar al usuario recien registrado.

**Trigger:** Supabase webhook `auth.users INSERT` (nuevo usuario en tabla `users`)

**Herramienta:** n8n

### Diagrama

```
[Supabase Webhook]
user.id, user.email, user.full_name, subscription_tier
    |
    v
[Idempotency Check] event_id = "onboard_" + user.id
    |
    v
[Split en paralelo]
    |---> [Resend] Welcome email (template "welcome_v1")
    |---> [OneSignal] Push: "Bienvenida a tu asesor de imagen personal"
    |---> [Brevo CRM] Crear contacto + asignar lista "free_users"
    |---> [PostHog] Event: user_registered {tier: "free"}
    |
    v
[Wait 1h]
    |
    v
[Supabase] SELECT body_analysis WHERE user_id = $1
    |
    +-- Si body_analysis existe → Skip
    |
    +-- Si NO existe →
            [OneSignal] Push: "Sube tu primera prenda y prueba el try-on gratis"
    |
    v
[Wait 23h] (total T+24h desde registro)
    |
    v
[Resend] Email "5 outfits que arrasan este mes" (template "outfits_trending_v1")
    |
    v
[Wait 48h] (total T+72h desde registro)
    |
    v
[Supabase] SELECT body_analysis WHERE user_id = $1
    |
    +-- Si body_analysis existe → [PostHog] Event: onboarding_completed → Stop
    |
    +-- Si NO existe →
            [OneSignal] Push: "Tu analisis de cuerpo tarda solo 2 minutos"
            [PostHog] Event: onboarding_reminder_sent
```

### Integraciones requeridas

- Supabase webhook en tabla `users` (evento: INSERT)
- Resend API key + plantillas `welcome_v1`, `outfits_trending_v1`
- OneSignal App ID + REST API key
- Brevo API key
- PostHog Project API key

### Error Handling

- Si Resend falla → retry x3 → DLQ → Slack alert
- Si OneSignal falla → retry x3 → log (no critico)
- Si Brevo falla → retry x2 → log (CRM no es critico en onboarding)

### KPIs

- Email welcome open rate objetivo: > 45%
- Push T+1h click rate objetivo: > 15%
- Body analysis completion en 72h: > 30% de nuevos usuarios
- TTV (primer try-on) en 7 dias: > 25%

---

## Workflow 2 — Activation Milestones

**Descripcion:** Felicitaciones progresivas cuando el usuario completa hitos clave. Crea momentum y reduce churn temprano.

**Trigger:** FastAPI POST `/webhooks/internal/milestone` (llamado desde los endpoints de body analysis, try-on y outfits)

Payload esperado:
```json
{
  "event_id": "milestone_{user_id}_{milestone_type}_{timestamp}",
  "user_id": "uuid",
  "milestone": "body_analysis_completed | first_try_on_done | first_outfit_saved | fifth_try_on | wardrobe_10_items",
  "metadata": {}
}
```

**Herramienta:** n8n

### Diagrama

```
[Webhook POST /milestone]
    |
    v
[Idempotency Check]
    |
    v
[Switch node — milestone type]
    |
    +-- "body_analysis_completed" ──────────────────────────────────+
    |       [OneSignal] Push: "Perfil completado. Tu IA ya te conoce"    |
    |       [Resend] Email: "Tu analisis revela esto sobre tu estilo"     |
    |       [PostHog] Event: milestone_body_analysis                     |
    |                                                                    |
    +-- "first_try_on_done" ────────────────────────────────────────+
    |       [OneSignal] Push: "Primer try-on completado! Como te quedo?"  |
    |       [PostHog] Event: milestone_first_tryon                       |
    |                                                                    |
    +-- "first_outfit_saved" ───────────────────────────────────────+
    |       [OneSignal] Push: "Guardaste tu primer outfit. Estilo en marcha"|
    |       [PostHog] Event: milestone_first_outfit                      |
    |                                                                    |
    +-- "fifth_try_on" ─────────────────────────────────────────────+
    |       [Supabase] SELECT subscription_tier WHERE user_id = $1       |
    |       +-- free tier:                                               |
    |       |   [OneSignal] Push: "5 try-ons completados! Pasa a PRO"    |
    |       |   [Resend] Email upgrade (template "upgrade_from_milestone")|
    |       +-- premium: [PostHog] Event: power_user_detected            |
    |                                                                    |
    +-- "wardrobe_10_items" ────────────────────────────────────────+
            [OneSignal] Push: "10 prendas en tu armario. La IA ya puede                 
                              sugerirte outfits completos"
            [PostHog] Event: milestone_wardrobe_10
```

### Dependencia con Sasha

Sasha debe llamar `POST /webhooks/internal/milestone` desde:
- `POST /analysis/body` al completar
- `POST /tryons` al completar el primer try-on
- `POST /outfits` al guardar el primero
- Logica de conteo en `usage_counters` al llegar a 5 try-ons

### KPIs

- Milestone completion rate por tipo (meta: body_analysis > 40% en 7 dias)
- Conversion milestone fifth_try_on → upgrade: > 8%
- Push open rate en milestone messages: > 25% (contextuales = mas apertura)

---

## Workflow 3 — Free Tier Limit Warning + Upgrade Nudge

**Descripcion:** Secuencia de conversion cuando el usuario free llega a 4/5 try-ons usados. Momento de maximo intent.

**Trigger:** FastAPI POST `/webhooks/internal/usage-warning` cuando `usage_counters.tryon_count` llega a 4

Payload:
```json
{
  "event_id": "usage_warn_{user_id}_{month_year}",
  "user_id": "uuid",
  "email": "string",
  "usage_count": 4,
  "limit": 5,
  "region": "LATAM | US"
}
```

**Herramienta:** n8n

### Diagrama

```
[Webhook POST /usage-warning]
    |
    v
[Idempotency Check] — CRITICO: event_id incluye mes/año para no re-triggear
    |
    v
[Split paralelo]
    |---> [OneSignal] Push: "Te queda 1 try-on este mes. Haztelo contar"
    |---> [PostHog] Event: free_limit_warning {usage: 4}
    |
    v
[Wait 24h]
    |
    v
[Supabase] SELECT subscription_tier WHERE user_id = $1
    |
    +-- Si subscription_tier != 'free' → [PostHog] conversion_from_warning → Stop
    |
    +-- Si sigue free →
            [Code node] Calcular precio segun region
                LATAM: "Estilo $3.99/mes (20% off tu primer mes)"
                US: "Estilo $7.99/mes (20% off tu primer mes)"
            [Resend] Email: template "upgrade_nudge_discount"
                           {discount_code: "PRIMERAMIGA20", precio_con_desc, region}
            [PostHog] Event: upgrade_email_sent {discount: "20%"}
    |
    v
[Wait 48h] (total T+72h)
    |
    v
[Supabase] SELECT subscription_tier WHERE user_id = $1
    |
    +-- Si subscription_tier != 'free' → Stop (convirtio)
    |
    +-- Si sigue free →
            [OneSignal] Push: "Ultima oportunidad: 20% off Estilo PRO"
            [PostHog] Event: upgrade_final_nudge
    |
    v
[Wait 7 dias]
    |
    v
[Supabase] SELECT subscription_tier WHERE user_id = $1
    |
    +-- Si sigue free → [PostHog] Event: upgrade_nudge_failed → Stop
```

### Workflow hermano: Welcome PRO

Se dispara cuando el usuario hace upgrade desde este flow:

```
Trigger: Supabase webhook users.subscription_tier UPDATE (free → premium_*)
    |
    [OneSignal] Push: "Bienvenida a PRO! Try-ons ilimitados desbloqueados"
    [Resend] Email: "Tu plan PRO esta activo. Esto es lo que puedes hacer ahora"
    [Brevo] Mover contacto de lista "free_users" a "pro_users"
    [PostHog] Event: upgrade_completed {from: "free", plan: tier}
```

### KPIs

- Open rate email de descuento: > 35%
- Click-to-upgrade desde email: > 12%
- Conversion total del flow (T+0 a T+72h): > 6%
- Discount code redemption rate: trackear con Stripe coupon

---

## Workflow 4 — Trial Expiration Nudge (PRO)

**Descripcion:** Secuencia de conversion para usuarios en trial de 7 dias sin tarjeta guardada.

**Trigger:** Cron diario 9:00 AM — consulta Supabase para trials que expiran en 3, 1, 0 dias

Logica de deteccion en n8n:
```sql
-- Trials expirando en 3 dias
SELECT u.id, u.email, u.full_name, s.current_period_end
FROM users u
JOIN subscriptions s ON s.user_id = u.id
WHERE s.status = 'trialing'
AND s.current_period_end BETWEEN now() + INTERVAL '2 days 20 hours'
                              AND now() + INTERVAL '3 days 4 hours'
AND u.id NOT IN (SELECT user_id FROM webhook_processed 
                 WHERE workflow_name = 'trial_exp_3d' 
                 AND processed_at > now() - INTERVAL '1 day')
```

(Query similar para 1 dia y 0 dias)

**Herramienta:** n8n

### Diagrama

```
[Cron 9:00 AM diario]
    |
    v
[Supabase] 3 queries en paralelo:
    +-- Trials expirando en T-3 dias
    +-- Trials expirando en T-1 dia
    +-- Trials expirados hoy (T-0)
    |
    v
[Split por lista]
    |
    +-- Para cada user en T-3:
    |       [Resend] Email: "Tu prueba gratuita termina en 3 dias"
    |                      template: "trial_exp_3d"
    |       [OneSignal] Push: "3 dias restantes de PRO"
    |       [webhook_processed] INSERT trial_exp_3d + user_id
    |
    +-- Para cada user en T-1:
    |       [OneSignal] Push: "Ultimo dia de tu prueba PRO"
    |       [Resend] Email: "Manana pierde acceso a try-ons ilimitados"
    |                      template: "trial_exp_1d"
    |       [webhook_processed] INSERT trial_exp_1d + user_id
    |
    +-- Para cada user en T-0 (expirado hoy):
            [Supabase] Verificar si aun en trialing (puede haber convertido)
            +-- Si convirtio → Skip
            +-- Si no convirtio →
                    [Resend] Email: "Tu prueba termino. Oferta rescue: 1 mes $2.99"
                             template: "trial_expired_rescue"
                             {rescue_price_latam: "$2.99", rescue_price_us: "$5.99"}
                    [OneSignal] Push: "Oferta especial: 1 mes Estilo a mitad de precio"
                    [PostHog] Event: trial_expired_rescue_sent
```

### KPIs

- Trial-to-paid conversion rate objetivo: > 20%
- Open rate T-3 email: > 50% (alta relevancia)
- Rescue offer acceptance rate: > 8%
- Revenue rescued (MRR salvado por rescue offer)

---

## Workflow 5 — Failed Payment / Dunning

**Descripcion:** Recuperacion de pagos fallidos. Secuencia escalada de 14 dias antes de downgrade.

**Trigger:** Stripe webhook `invoice.payment_failed` / MercadoPago webhook equivalente

Payload Stripe (simplificado):
```json
{
  "type": "invoice.payment_failed",
  "data": {
    "object": {
      "customer": "cus_xxx",
      "subscription": "sub_xxx",
      "amount_due": 999,
      "next_payment_attempt": 1714080000
    }
  }
}
```

**Herramienta:** n8n

### Diagrama

```
[Stripe Webhook POST /webhooks/stripe]
    |
    v
[FastAPI] Verificar Stripe signature (HMAC) → n8n recibe evento verificado
    |
    v
[Idempotency] event_id = stripe_event_id
    |
    v
[Supabase] SELECT user by subscription_id → obtener user.id, user.email
    |
    v
[Supabase] UPDATE users SET subscription_status = 'past_due'
    |
    v
[Resend] Email Dia 1: "Hubo un problema con tu pago"
         template: "payment_failed_d1"
         {update_payment_url, amount, last_4_digits}
[PostHog] Event: payment_failed {day: 1}
    |
    v
[Wait 2 dias] (Dia 3)
    |
    v
[Supabase] SELECT subscription_status WHERE user_id = $1
    |
    +-- Si 'active' → [PostHog] payment_recovered_d3 → Stop
    |
    +-- Si sigue 'past_due' →
            [Resend] Email Dia 3: "Segundo intento de cobro fallido"
                     template: "payment_failed_d3"
            [OneSignal] Push: "Actualiza tu metodo de pago para mantener PRO"
            [PostHog] Event: payment_failed {day: 3}
    |
    v
[Wait 4 dias] (Dia 7)
    |
    v
[Supabase] SELECT subscription_status WHERE user_id = $1
    |
    +-- Si 'active' → Stop
    |
    +-- Si sigue 'past_due' →
            [Resend] Email Dia 7: "Ultimo aviso antes de pausar tu cuenta"
                     template: "payment_failed_d7"
            [PostHog] Event: payment_failed {day: 7}
    |
    v
[Wait 1 dia] (Dia 8)
    |
    v
[Supabase] SELECT subscription_status WHERE user_id = $1
    |
    +-- Si 'active' → Stop
    |
    +-- Si sigue 'past_due' →
            [Supabase] UPDATE users SET subscription_tier = 'free'
                                        subscription_status = 'cancelled'
            [OneSignal] Push: "Tu cuenta paso a plan gratuito. Wardrobe conservado"
            [Resend] Email Dia 8: "Tu cuenta fue pausada. Tu wardrobe esta guardado"
                     template: "downgrade_notice"
            [Brevo] Mover a lista "churned_paid"
            [PostHog] Event: involuntary_churn {reason: "payment_failed"}
    |
    v
[Wait 7 dias] (Dia 15 desde fallo inicial)
    |
    v
[Supabase] SELECT subscription_tier WHERE user_id = $1
    |
    +-- Si subscription_tier != 'free' → Stop (recontrató)
    |
    +-- Si sigue free →
            [Resend] Email: "Tus datos se eliminaran en 30 dias"
                     template: "deletion_notice_30d"
            [PostHog] Event: deletion_notice_sent
```

### Importante — Wardrobe Retention Policy

En el downgrade se conserva el wardrobe pero se limita a 20 items visibles (el resto archivado). 
Esto es incentivo para reactivar. Sasha debe implementar esta logica en el endpoint de downgrade.

### KPIs

- Payment recovery rate (dias 1-7): objetivo > 35%
- Churn por pago fallido (involuntary churn): objetivo < 15% de payment_failed
- MRR recovered por dunning sequence

---

## Workflow 6 — Weekly Digest (Engagement)

**Descripcion:** Email semanal personalizado para mantener el habito de uso de la app.

**Trigger:** Cron lunes 8:00 AM (hora local del usuario — usar timezone del perfil)

Para MVP: cron lunes 8:00 AM UTC-5 (hora Colombia/LATAM principal)

**Herramienta:** n8n

### Diagrama

```
[Cron lunes 8:00 AM]
    |
    v
[Supabase] Query usuarios activos (login en ultimos 14 dias, subscription activa)
    SELECT u.id, u.email, u.full_name, u.body_shape, u.color_preferences,
           u.subscription_tier,
           COUNT(DISTINCT o.id) as outfits_this_week,
           COUNT(DISTINCT t.id) as tryons_this_week,
           COUNT(DISTINCT w.id) as wardrobe_items
    FROM users u
    LEFT JOIN outfits o ON o.user_id = u.id 
                        AND o.created_at > now() - INTERVAL '7 days'
    LEFT JOIN tryons t ON t.user_id = u.id 
                       AND t.created_at > now() - INTERVAL '7 days'
    LEFT JOIN wardrobe_items w ON w.user_id = u.id
    WHERE u.updated_at > now() - INTERVAL '14 days'
    AND u.subscription_status = 'active'
    |
    v
[Split por usuario]
    |
    v
[Para cada usuario]
    |
    +-- [Code node] Determinar tipo de digest:
    |       outfits_this_week > 0: "power_user"
    |       tryons_this_week > 0: "engaged"
    |       else: "dormant" (no enviar digest, ir a win-back en su momento)
    |
    +-- Si power_user o engaged:
            [HTTP Request] Claude API (Haiku) — generar recomendaciones
                Prompt (minimalista para reducir tokens):
                "Usuario: cuerpo={body_shape}, colores={color_preferences}.
                 Esta semana: {outfits_this_week} outfits, {tryons_this_week} try-ons.
                 Sugiere 3 combinaciones de colores en tendencia para su perfil.
                 Responde en JSON: [{titulo, descripcion_corta}]"
            |
            v
            [Resend] Email template "weekly_digest_v1"
                     {nombre, outfits_count, tryons_count,
                      recomendaciones_ia, wardrobe_count}
            [PostHog] Event: weekly_digest_sent {tier: subscription_tier}
```

### Optimizacion de costos IA

- Usar Claude Haiku (no Sonnet) para generacion de recomendaciones del digest
- Batch: procesar todos los usuarios antes de llamar Claude (una llamada por usuario, no por lote — cada perfil es diferente)
- Cache: si el body_shape y color_preferences no cambiaron en 30 dias, reusar recomendaciones del digest anterior (guardar en `analytics_events` con event_type = 'digest_recommendations_cache')

Estimado: ~200 tokens por usuario × $0.00025/1k tokens = $0.00005 por usuario/semana = $0.50 para 10k usuarios activos/semana.

### KPIs

- Weekly digest open rate: > 30%
- Click-to-app desde digest: > 20%
- DAU/WAU ratio (activos semana vs mes)
- Retention semana 4 (usuarios que abren digest 4 semanas seguidas)

---

## Workflow 7 — Win-Back (Churned Users)

**Descripcion:** Reactivacion de usuarios que dejaron de usar la app. Tres olas en 30/60/90 dias.

**Trigger:** Cron diario 10:00 AM — detecta usuarios inactivos por dias exactos

**Herramienta:** n8n

### Diagrama

```
[Cron diario 10:00 AM]
    |
    v
[Supabase] 3 queries en paralelo:
    +-- Inactivos exactamente 30 dias (last_login BETWEEN 30d y 31d atras)
    +-- Inactivos exactamente 60 dias
    +-- Inactivos exactamente 90 dias
    (usar analytics_events o users.updated_at como proxy de actividad)
    |
    v
[Para cada ola]

OLA 30 DIAS:
    [Resend] Email "Lo que te perdiste este mes en Asesor de Imagen"
             template: "winback_30d"
             {nuevas_features, outfits_tendencia_mes}
    [PostHog] Event: winback_email_sent {day: 30}

OLA 60 DIAS:
    [Supabase] CHECK si abrio email de 30 dias (via Resend webhook o PostHog)
    +-- Si abrio pero no reactivó:
    |       [OneSignal] Push: "Vuelve y prueba las nuevas recomendaciones"
    |       [Resend] Email con descuento 25% primer mes
    |                template: "winback_60d_discount"
    +-- Si no abrio email 30d:
            [Resend] Email con oferta directa
            [PostHog] Event: winback_email_sent {day: 60}

OLA 90 DIAS:
    [Supabase] SELECT subscription_tier WHERE user_id = $1
    +-- Si es paid y no reactivó:
    |       [Resend] Email: "Ultima oferta: 1 mes gratis al reactivar"
    |                template: "winback_90d_final"
    |       [PostHog] Event: winback_final_attempt {day: 90}
    +-- Si es free:
            [Resend] Email: "Tu cuenta sigue ahi. Tus prendas te esperan"
            Nota: sin descuento (no hay que recuperar revenue, solo DAU)

Post-90 dias sin reactivacion:
    [Brevo] Mover a lista "inactive_90d_plus" (baja frecuencia de contacto: 1x trimestre)
    [PostHog] Event: user_churned_confirmed
```

### KPIs

- Winback rate D30: objetivo > 8%
- Winback rate D60: objetivo > 4%
- Winback rate D90: objetivo > 2%
- CAC winback vs CAC nuevo usuario (eficiencia)

---

## Workflow 8 — Referral Program

**Descripcion:** Sistema de atribucion y reward para el programa de referidos.

**Modelo:** Quien refiere recibe 1 mes de Estilo gratis cuando la amiga se suscribe a plan pago.

**Trigger:** Dos eventos que trabajan juntos:
1. Usuario genera codigo de referido: FastAPI POST `/webhooks/internal/referral-created`
2. Nueva suscripcion con codigo de referido: Stripe webhook `checkout.session.completed` con metadata `referral_code`

**Herramienta:** n8n

### Tabla requerida (migration 003)

```sql
CREATE TABLE public.referrals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    referrer_user_id UUID NOT NULL REFERENCES users(id),
    referral_code TEXT UNIQUE NOT NULL,
    referred_user_id UUID REFERENCES users(id),
    status TEXT DEFAULT 'pending'
        CHECK (status IN ('pending', 'converted', 'rewarded', 'expired')),
    reward_issued_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_referrals_code ON referrals(referral_code);
CREATE INDEX idx_referrals_referrer ON referrals(referrer_user_id);
```

### Diagrama

```
FASE 1 — Generacion de codigo (en app)
[FastAPI] POST /referral/generate → INSERT referrals (referrer_user_id, referral_code)
    |
    v
[Webhook] → n8n
    |
    v
[OneSignal] Push: "Tu codigo de referido esta listo: {codigo}"
[PostHog] Event: referral_code_generated

----

FASE 2 — Nueva amiga se registra con codigo
[Stripe webhook] checkout.session.completed
    {
      metadata: { referral_code: "ABC123", user_id: "uuid_nueva" }
    }
    |
    v
[FastAPI] Verifica firma Stripe → pasa evento a n8n
    |
    v
[Idempotency] event_id = stripe_checkout_session_id
    |
    v
[Supabase] SELECT referrals WHERE referral_code = $1 AND status = 'pending'
    |
    +-- No existe o status != pending → [PostHog] referral_invalid → Stop
    |
    +-- Existe y pending →
            [Supabase] UPDATE referrals SET
                referred_user_id = $nueva_user_id,
                status = 'converted'
            |
            v
            [Split paralelo]
            |
            +-- Para quien REFIRIÓ:
            |       [Stripe] Apply coupon "1_month_free_estilo" a customer referrer
            |               (via Stripe API: POST /v1/customers/{id}/discount)
            |       [OneSignal] Push: "Tu amiga se unio! 1 mes PRO gratis aplicado"
            |       [Resend] Email: "Gracias por recomendar Asesor de Imagen"
            |                       template: "referral_reward_v1"
            |       [Supabase] UPDATE referrals SET status = 'rewarded',
            |                  reward_issued_at = now()
            |       [PostHog] Event: referral_rewarded {referrer_user_id}
            |
            +-- Para la NUEVA USUARIA:
                    [OneSignal] Push: "Bienvenida! Tu amiga ya te dio la mejor intro"
                    [PostHog] Event: user_registered_via_referral
                    → Disparar Workflow 1 (Welcome Onboarding) para nueva usuaria
```

### Prevencion de fraude

- Un codigo de referido solo puede convertirse una vez (status 'pending' → 'converted')
- No se puede referir una cuenta existente (check por email antes de crear cuenta)
- Rate limit: maximo 10 codigos activos por usuario
- Reward solo se emite cuando el pago es exitoso (no en trial)

### KPIs

- Referral participation rate (% usuarios que generan codigo): objetivo > 15%
- Referral conversion rate (codigo generado → amiga suscrita): objetivo > 10%
- Viral coefficient K (referidos por usuario activo): objetivo > 0.3
- CAC via referral vs paid acquisition

---

## KPIs por Workflow

### Dashboard de metricas (PostHog)

Crear los siguientes funnels en PostHog al configurar:

```
Funnel 1 — Onboarding Activation
user_registered → body_analysis_completed → first_try_on_done → first_outfit_saved

Funnel 2 — Free to Paid Conversion
free_limit_warning → upgrade_email_sent → upgrade_completed

Funnel 3 — Trial Conversion
trial_started → trial_exp_3d → trial_exp_1d → trial_converted

Funnel 4 — Dunning Recovery
payment_failed → payment_recovered (vs) → involuntary_churn

Funnel 5 — Winback
user_churned_confirmed → winback_email_sent → user_reactivated
```

### Tabla resumen de KPIs

| Workflow | KPI Principal | Objetivo MVP | Objetivo 6 meses |
|----------|-------------|--------------|-----------------|
| WF1 Welcome | Body analysis completion 72h | 30% | 40% |
| WF2 Milestones | TTV (primer try-on < 7 dias) | 25% | 35% |
| WF3 Upgrade Nudge | Free → Paid conversion | 6% | 10% |
| WF4 Trial | Trial → Paid conversion | 20% | 30% |
| WF5 Dunning | Payment recovery rate | 35% | 45% |
| WF6 Digest | Weekly retention (abre 4 sem seguidas) | 20% | 35% |
| WF7 Winback | D30 reactivation rate | 8% | 12% |
| WF8 Referral | Viral coefficient K | 0.3 | 0.5 |

---

## Compliance

### GDPR (aplica para usuarios EU y como buena practica global)

**Unsubscribe links:**
- Todos los emails transaccionales incluyen `{unsubscribe_link}` en footer
- Resend maneja la mecanica de unsubscribe automaticamente
- n8n verifica `unsubscribe_status` en Brevo antes de enviar cualquier email de marketing

**Flujo de opt-out en n8n:**
```
Antes de enviar email de marketing (WF3, WF6, WF7):
    [Brevo] GET contact by email → check unsubscribed flag
    +-- unsubscribed: true → Skip email → continuar con push si corresponde
    +-- unsubscribed: false → enviar email
```

**Data retention en n8n:**
- n8n self-hosted NO almacena PII en sus logs de ejecucion
- Configurar en n8n: `EXECUTIONS_DATA_SAVE_ON_SUCCESS=none` (no guardar payload de execuciones exitosas)
- `EXECUTIONS_DATA_SAVE_ON_ERROR=all` (guardar solo errores, para debugging)
- Rotation de logs de error: 30 dias

**Tabla `webhook_processed`:** solo guarda `event_id` (no PII), retener 30 dias.

### CAN-SPAM (aplica para usuarios US)

- [x] Identificacion clara del remitente: `Asesor de Imagen <hola@asesor-imagen.app>`
- [x] Subject lines no engañosos
- [x] Direccion postal fisica en footer (usar direccion legal de la empresa)
- [x] Unsubscribe honrado en <= 10 dias (Resend lo hace en tiempo real)

### Leyes LATAM (Colombia, Mexico, Argentina — principales mercados)

**Colombia (Ley 1581/2012 — Habeas Data):**
- Consentimiento explicito en registro para comunicaciones de marketing
- Campo `marketing_consent: boolean` en tabla `users` (agregar en migration 003)
- n8n verifica `marketing_consent = true` antes de emails de marketing

**Mexico (LFPDPPP):**
- Aviso de privacidad claro en onboarding
- Mecanismo de cancelacion (equivalente a GDPR opt-out)

**Regla practica para MVP:** checkbox en registro "Acepto recibir comunicaciones sobre tendencias de moda y ofertas especiales". Datos de marketing no se procesan si `marketing_consent = false`.

### PII en n8n

**Datos que n8n maneja (temporalmente en memoria durante ejecucion):**
- email, nombre, user_id → OK, datos operacionales necesarios
- imagenes corporales, resultados de try-on → NUNCA pasan por n8n
  - n8n solo recibe URLs de Supabase Storage, nunca el binario
  - Las imagenes se procesan directamente en el backend de FastAPI

**Datos que n8n NO almacena permanentemente:**
- Configurar n8n Railway con variables de entorno de seguridad (ver seccion siguiente)

---

## Variables de Entorno Globales

Variables que deben configurarse en n8n (Railway environment variables):

```bash
# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=xxx   # service role para writes desde n8n

# Email
RESEND_API_KEY=re_xxx
FROM_EMAIL=hola@asesor-imagen.app
FROM_NAME=Asesor de Imagen

# Push
ONESIGNAL_APP_ID=xxx
ONESIGNAL_REST_API_KEY=xxx

# CRM
BREVO_API_KEY=xxx

# Analytics
POSTHOG_PROJECT_API_KEY=phc_xxx
POSTHOG_HOST=https://app.posthog.com

# Payments
STRIPE_WEBHOOK_SECRET=whsec_xxx
STRIPE_SECRET_KEY=sk_xxx

# IA (para WF6 digest)
ANTHROPIC_API_KEY=sk-ant-xxx

# n8n Security (no guardar PII en logs)
EXECUTIONS_DATA_SAVE_ON_SUCCESS=none
EXECUTIONS_DATA_SAVE_ON_ERROR=all
EXECUTIONS_DATA_MAX_AGE=168  # 7 dias en horas
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=xxx  # cambiar por contraseña fuerte

# Internal webhook security
N8N_WEBHOOK_SECRET=xxx  # FastAPI la usa para firmar llamadas internas
```

---

## Endpoints que Sasha debe implementar (para activar los workflows)

Lista de endpoints internos que n8n necesita y que no existen aun en el router:

```
POST /webhooks/internal/milestone
  Body: {event_id, user_id, milestone, metadata}
  Llamar desde: body_analysis, tryons, outfits endpoints

POST /webhooks/internal/usage-warning
  Body: {event_id, user_id, email, usage_count, limit, region}
  Llamar desde: tryons endpoint cuando usage_counters.tryon_count == 4

POST /webhooks/internal/referral-created
  Body: {event_id, user_id, referral_code}
  Llamar desde: POST /referral/generate

GET /users/{user_id}/usage-counters
  Response: {tryon_count, month, limit}
  Necesario para: WF3 trigger logic
```

Todos estos endpoints son internos (solo llamados por n8n o logica interna), deben requerir autenticacion por `N8N_WEBHOOK_SECRET` en header `X-Webhook-Secret`.

---

## Orden de Implementacion Recomendado

Cuando Sasha tenga endpoints listos (Sprint 1-2):

```
Semana 1 (criticos para revenue):
  1. WF1 Welcome Onboarding — base del funnel
  2. WF5 Failed Payment / Dunning — protege revenue

Semana 2 (conversion):
  3. WF3 Free Tier Limit Warning — driver de upgrade
  4. WF4 Trial Expiration — conversion de trials

Semana 3 (engagement y retencion):
  5. WF2 Activation Milestones — gamificacion
  6. WF6 Weekly Digest — retention habito

Semana 4 (crecimiento):
  7. WF7 Win-Back — reactivacion
  8. WF8 Referral Program — viral loop
```

---

**Cinthya — Especialista en Automatizacion de Procesos**
**Estado:** DISENIO COMPLETO — pendiente implementacion post Sprint 1-2 de Sasha
**Proxima accion:** Cuando Sasha entregue endpoints internos, implementar WF1 y WF5 en n8n Railway como prioridad.
