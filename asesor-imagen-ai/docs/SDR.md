# SDR — Software Design Record
## Asesor de Imagen AI — MVP v1.0

**Documento técnico formal para implementación**
**Versión:** 1.0
**Fecha:** 2026-04-30
**Status:** Approved for implementation
**Owner:** Jarvis (CEO) + Alejo (Solutions Architect)
**Stakeholder:** Juan Camilo Gil (Accionista)

---

## TABLA DE CONTENIDOS

1. [Visión y alcance](#1-visión-y-alcance)
2. [Requirements funcionales](#2-requirements-funcionales)
3. [Requirements no funcionales](#3-requirements-no-funcionales)
4. [Modelo de datos](#4-modelo-de-datos)
5. [Arquitectura del sistema](#5-arquitectura-del-sistema)
6. [API contracts](#6-api-contracts)
7. [Security model](#7-security-model)
8. [Performance targets](#8-performance-targets)
9. [Integraciones externas](#9-integraciones-externas)
10. [Constraints y assumptions](#10-constraints-y-assumptions)
11. [Glosario](#11-glosario)

---

## 1. VISIÓN Y ALCANCE

### 1.1 Producto

App móvil iOS+Android que permite a usuarias:
- Subir fotos de su cuerpo y prendas
- Probarse virtualmente combinaciones de outfits (Virtual Try-On)
- Recibir recomendaciones IA personalizadas según body type, color season y preferencias aprendidas
- Aprovechar al máximo el guardarropa que ya tienen

### 1.2 Audiencia

- **Geografía primaria:** LATAM (Colombia, México, Argentina, Chile)
- **Geografía secundaria:** US Hispanic + España
- **Demografía:** Mujeres 22-40 años, ingreso medio-alto, smartphone-native, fashion-conscious

### 1.3 Modelo de negocio

Freemium subscription:
- **Free:** $0 (5 try-ons/mes, watermark, 30 prendas máx)
- **Estilo (Pro):** $4.99 LATAM / $9.99 US (try-ons ilimitados, recomendaciones premium)
- **Imagen (Premium):** $9.99 LATAM / $19.99 US (todo + stylist humano + analytics)

### 1.4 Plataformas objetivo

- **iOS:** ≥ iOS 16
- **Android:** ≥ Android 9 (API 28)
- **Web:** Out of scope MVP

### 1.5 Idiomas

- **MVP:** Español (LATAM neutro) + Inglés (US)
- **Post-launch:** Portugués (Brasil)

---

## 2. REQUIREMENTS FUNCIONALES

### 2.1 Autenticación (RF-AUTH)

| ID | Requirement | Prioridad |
|----|-------------|-----------|
| RF-AUTH-001 | Usuaria puede registrarse con email + password | P0 |
| RF-AUTH-002 | Usuaria puede registrarse con Google OAuth | P0 |
| RF-AUTH-003 | Usuaria puede registrarse con Apple Sign In (iOS) | P0 |
| RF-AUTH-004 | Usuaria puede recuperar password (magic link) | P0 |
| RF-AUTH-005 | Sesión persiste entre app launches | P0 |
| RF-AUTH-006 | JWT con refresh token rotation | P0 |
| RF-AUTH-007 | Logout limpia todos los tokens locales | P0 |
| RF-AUTH-008 | Usuaria puede eliminar cuenta (GDPR right-to-be-forgotten) | P0 |
| RF-AUTH-009 | MFA opcional (post-launch) | P2 |

### 2.2 Profile (RF-PROF)

| ID | Requirement | Prioridad |
|----|-------------|-----------|
| RF-PROF-001 | Usuaria puede ver/editar nombre, avatar, fecha nacimiento | P0 |
| RF-PROF-002 | Usuaria puede configurar idioma + país | P0 |
| RF-PROF-003 | Usuaria puede ver historial de body analyses | P1 |
| RF-PROF-004 | Usuaria puede ver style profile aprendido | P1 |
| RF-PROF-005 | Usuaria puede ver subscription status + history | P0 |
| RF-PROF-006 | Usuaria puede gestionar notificaciones (push + email) | P1 |

### 2.3 Wardrobe Management (RF-WARD)

| ID | Requirement | Prioridad |
|----|-------------|-----------|
| RF-WARD-001 | Usuaria puede subir foto de prenda (cámara o galería) | P0 |
| RF-WARD-002 | Sistema auto-tagea prenda con Vision API (color, style, occasion) | P0 |
| RF-WARD-003 | Usuaria puede editar tags manualmente | P0 |
| RF-WARD-004 | Usuaria puede ver wardrobe en grid paginado | P0 |
| RF-WARD-005 | Usuaria puede filtrar por color, style, occasion, brand | P1 |
| RF-WARD-006 | Usuaria puede buscar prendas por keyword | P1 |
| RF-WARD-007 | Usuaria puede eliminar prendas (soft delete) | P0 |
| RF-WARD-008 | Usuaria puede agregar metadata (precio, fecha compra, marca) | P1 |
| RF-WARD-009 | Free tier: máximo 30 prendas | P0 |
| RF-WARD-010 | Pro/Premium: prendas ilimitadas | P0 |

### 2.4 Body Analysis (RF-BODY)

| ID | Requirement | Prioridad |
|----|-------------|-----------|
| RF-BODY-001 | Usuaria puede subir foto cuerpo entero | P0 |
| RF-BODY-002 | Sistema detecta body type (apple/pear/hourglass/rectangle/inverted_triangle) | P0 |
| RF-BODY-003 | Sistema detecta skin tone category (warm/cool/neutral) | P0 |
| RF-BODY-004 | Sistema calcula color season (spring/summer/autumn/winter) | P0 |
| RF-BODY-005 | Sistema sugiere best/avoid colors (array hex) | P0 |
| RF-BODY-006 | Privacy: imágenes encriptadas en R2 | P0 |
| RF-BODY-007 | Privacy: signed URLs con expiración 1h | P0 |
| RF-BODY-008 | Usuaria puede eliminar body analysis (cascade delete imágenes) | P0 |
| RF-BODY-009 | Free tier: 1 analysis/mes | P0 |
| RF-BODY-010 | Pro/Premium: analysis ilimitados | P0 |

### 2.5 Virtual Try-On (RF-TRYON)

| ID | Requirement | Prioridad |
|----|-------------|-----------|
| RF-TRYON-001 | Usuaria selecciona prenda + body image base | P0 |
| RF-TRYON-002 | Sistema verifica cache hit (hash match) → return cached | P0 |
| RF-TRYON-003 | Si miss: sistema enqueue task ARQ → llama Replicate | P0 |
| RF-TRYON-004 | Cliente recibe resultado vía Supabase Realtime | P0 |
| RF-TRYON-005 | Cliente puede polling fallback `/try-ons/{id}` | P0 |
| RF-TRYON-006 | Tiempo total p95 < 5s (cache hit) / < 15s (miss) | P0 |
| RF-TRYON-007 | Usuaria puede dar feedback (5 stars, fit, color, would_buy) | P0 |
| RF-TRYON-008 | Usuaria puede compartir resultado (Stories format watermark) | P1 |
| RF-TRYON-009 | Usuaria puede guardar try-on como favorito | P0 |
| RF-TRYON-010 | Free tier: 5 try-ons/mes hard cap | P0 |
| RF-TRYON-011 | Pro tier: 50 try-ons/mes (cap suave) | P0 |
| RF-TRYON-012 | Premium tier: ilimitado | P0 |
| RF-TRYON-013 | Idempotency-Key obligatoria en POST | P0 |
| RF-TRYON-014 | Cuando cuota agotada: paywall modal upgrade | P0 |

### 2.6 AI Recommendations (RF-RECO)

| ID | Requirement | Prioridad |
|----|-------------|-----------|
| RF-RECO-001 | Usuaria puede pedir recos por ocasión (office/casual/date/gym) | P0 |
| RF-RECO-002 | Sistema construye prompt Claude con: body_analysis + recent try-ons + wardrobe + occasion | P0 |
| RF-RECO-003 | Tiempo respuesta p95 < 2s | P0 |
| RF-RECO-004 | Cada outfit muestra reasoning (por qué se recomienda) | P0 |
| RF-RECO-005 | Usuaria puede like/dislike outfit (training signal) | P0 |
| RF-RECO-006 | Sistema actualiza user_style_profile diariamente | P0 |
| RF-RECO-007 | Free tier: 10 recos/día | P0 |
| RF-RECO-008 | Pro tier: 50 recos/día | P0 |
| RF-RECO-009 | Premium: ilimitado | P0 |
| RF-RECO-010 | A/B testing prompts (claude_model_version field) | P1 |

### 2.7 Subscriptions (RF-SUB)

| ID | Requirement | Prioridad |
|----|-------------|-----------|
| RF-SUB-001 | Usuaria puede iniciar trial 7 días Pro sin tarjeta | P0 |
| RF-SUB-002 | Usuaria paga vía Stripe (US) o Mercado Pago (LATAM) | P0 |
| RF-SUB-003 | Cobros automáticos mensuales | P0 |
| RF-SUB-004 | Yearly discount -33% | P0 |
| RF-SUB-005 | Usuaria puede cancelar (efecto fin de período) | P0 |
| RF-SUB-006 | Failed payment: dunning flow 7 días, luego downgrade | P0 |
| RF-SUB-007 | Tax handling LATAM (IVA Colombia 19%, México 16%) | P0 |
| RF-SUB-008 | Receipts emitidos por email | P0 |
| RF-SUB-009 | Webhooks idempotentes Stripe + MP | P0 |
| RF-SUB-010 | Quota enforcement: usage_counters incrementa por feature | P0 |

### 2.8 Notifications (RF-NOTIF)

| ID | Requirement | Prioridad |
|----|-------------|-----------|
| RF-NOTIF-001 | Welcome push + email post-registro | P0 |
| RF-NOTIF-002 | Onboarding nudge T+1h, T+24h, T+72h | P0 |
| RF-NOTIF-003 | Try-on completed push (cuando ARQ termina) | P0 |
| RF-NOTIF-004 | Quota warning push (4/5 usados) | P0 |
| RF-NOTIF-005 | Trial expiration nudge T-3, T-1, T-0 | P0 |
| RF-NOTIF-006 | Failed payment dunning email + push | P0 |
| RF-NOTIF-007 | Weekly digest email (lunes 8 AM) — usuarios activos | P1 |
| RF-NOTIF-008 | Win-back email 30/60/90 días sin login | P1 |
| RF-NOTIF-009 | Usuaria puede opt-out de cualquier notif (compliance) | P0 |

### 2.9 Referral & Sharing (RF-VIRAL)

| ID | Requirement | Prioridad |
|----|-------------|-----------|
| RF-VIRAL-001 | Usuaria recibe código referido único | P1 |
| RF-VIRAL-002 | Si amiga se suscribe con código → ambas reciben 1 mes Estilo gratis | P1 |
| RF-VIRAL-003 | Share try-on a Instagram Stories (con watermark) | P1 |
| RF-VIRAL-004 | Share try-on a TikTok (con watermark) | P1 |

---

## 3. REQUIREMENTS NO FUNCIONALES

### 3.1 Performance (RNF-PERF)

| ID | Requirement | Target |
|----|-------------|--------|
| RNF-PERF-001 | API latency p95 (excluyendo IA externa) | < 500ms |
| RNF-PERF-002 | API latency p99 | < 1s |
| RNF-PERF-003 | Try-on completed time p95 (cache hit) | < 5s |
| RNF-PERF-004 | Try-on completed time p95 (cache miss) | < 15s |
| RNF-PERF-005 | Recommendations response p95 | < 2s |
| RNF-PERF-006 | App cold start time (Flutter) | < 3s |
| RNF-PERF-007 | Image load time global (R2 CDN) | < 500ms |

### 3.2 Scalability (RNF-SCALE)

| ID | Requirement | Target |
|----|-------------|--------|
| RNF-SCALE-001 | Soportar 1K req/min sustained | Sprint 9 |
| RNF-SCALE-002 | Soportar 10K req/min con auto-scale | Mes 6 |
| RNF-SCALE-003 | Database max connections | 100 (con pooling) |
| RNF-SCALE-004 | Concurrent users (DAU peak) | 50K (mes 12) |

### 3.3 Reliability (RNF-REL)

| ID | Requirement | Target |
|----|-------------|--------|
| RNF-REL-001 | Uptime SLA | 99.5% |
| RNF-REL-002 | Backup frequency | Diaria automatizada |
| RNF-REL-003 | Point-in-time recovery | 7 días |
| RNF-REL-004 | Crash-free rate (Flutter) | >99.5% |
| RNF-REL-005 | Replicate downtime → graceful degradation | "Queued for later" |

### 3.4 Security (RNF-SEC)

| ID | Requirement | Detalle |
|----|-------------|---------|
| RNF-SEC-001 | OWASP Top 10 2025 compliance | All categories |
| RNF-SEC-002 | HTTPS only | HSTS habilitado |
| RNF-SEC-003 | RLS habilitado | Todas las tablas user-specific |
| RNF-SEC-004 | Passwords hashing | Supabase Auth (bcrypt 12) |
| RNF-SEC-005 | JWT lifetime | Access 30min, Refresh 7 días |
| RNF-SEC-006 | Rate limiting | 60 req/min/user |
| RNF-SEC-007 | CORS restrictivo prod | Whitelist dominios |
| RNF-SEC-008 | Secrets management | Railway env vars |
| RNF-SEC-009 | PII encryption at rest | R2 server-side encryption |
| RNF-SEC-010 | Audit log retención | 12 meses |

### 3.5 Privacy & Compliance (RNF-PRIV)

| ID | Requirement | Detalle |
|----|-------------|---------|
| RNF-PRIV-001 | GDPR compliance | Right-to-be-forgotten, data export |
| RNF-PRIV-002 | LGPD (Brasil) compliance | Post-launch sem 18+ |
| RNF-PRIV-003 | Ley 1581 Colombia (Habeas Data) | Compliance |
| RNF-PRIV-004 | Body images: encrypted at rest + transit | Always |
| RNF-PRIV-005 | Body images: delete on user request | <24h |
| RNF-PRIV-006 | No selling user data | Política explícita |
| RNF-PRIV-007 | Cookie consent (web post-launch) | EU + Brasil |

### 3.6 Accessibility (RNF-A11Y)

| ID | Requirement | Standard |
|----|-------------|----------|
| RNF-A11Y-001 | WCAG 2.2 AA compliance | All screens |
| RNF-A11Y-002 | Screen reader support | iOS VoiceOver + Android TalkBack |
| RNF-A11Y-003 | Touch targets | Min 44x44 pt |
| RNF-A11Y-004 | Color contrast | 4.5:1 mínimo |
| RNF-A11Y-005 | Dynamic type support | iOS + Android |

### 3.7 Observability (RNF-OBS)

| ID | Requirement | Tool |
|----|-------------|------|
| RNF-OBS-001 | Error tracking | Sentry |
| RNF-OBS-002 | Product analytics | PostHog |
| RNF-OBS-003 | Structured logs JSON | Railway logs |
| RNF-OBS-004 | Uptime monitoring | Better Uptime / Pingdom |
| RNF-OBS-005 | Performance monitoring | Sentry Performance |
| RNF-OBS-006 | Distributed tracing | OpenTelemetry (post-launch) |

---

## 4. MODELO DE DATOS

### 4.1 Diagrama ER (alto nivel)

```
auth.users (Supabase managed)
    │
    │ 1:1
    ▼
profiles  ──────────────────────────────────┐
    │                                        │
    │ 1:N                                    │ 1:N
    ▼                                        ▼
wardrobe_items                          body_analysis
    │                                        │
    │ 1:N                                    │
    ▼                                        │
try_ons ─────────────────────────────────────┤
    │                                        │
    │ N:1 (cache)                            │
    ▼                                        │
try_on_cache                                 │
                                             │
recommendations ─────┬───────────────────────┤
    │                │                       │
    │ N:M            │                       │
    ▼                ▼                       │
recommendation_items └─→ wardrobe_items     │
                                             │
subscriptions ───────────────────────────────┤
    │                                        │
    │ 1:N                                    │
    ▼                                        │
usage_counters                               │
                                             │
user_style_profile ──────────────────────────┤
                                             │
audit_log ───────────────────────────────────┘

idempotency_keys (independiente)
```

### 4.2 Schemas SQL (PostgreSQL 16)

#### `profiles`
```sql
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  first_name TEXT,
  last_name TEXT,
  avatar_url TEXT,
  date_of_birth DATE,
  country_code TEXT, -- ISO 3166-1 alpha-2
  preferred_language TEXT DEFAULT 'es',
  notification_preferences JSONB DEFAULT '{"push": true, "email": true}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  deleted_at TIMESTAMPTZ
);
CREATE INDEX idx_profiles_country ON profiles(country_code);
```

#### `subscriptions`
```sql
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  plan_type TEXT NOT NULL CHECK (plan_type IN ('free', 'estilo', 'imagen')),
  billing_provider TEXT CHECK (billing_provider IN ('stripe', 'mercadopago')),
  external_subscription_id TEXT, -- Stripe sub_id or MP id
  external_customer_id TEXT,
  status TEXT NOT NULL CHECK (status IN ('trialing', 'active', 'past_due', 'canceled', 'expired')),
  trial_ends_at TIMESTAMPTZ,
  current_period_start TIMESTAMPTZ,
  current_period_end TIMESTAMPTZ,
  cancel_at_period_end BOOLEAN DEFAULT FALSE,
  canceled_at TIMESTAMPTZ,
  currency TEXT, -- 'USD', 'COP', 'MXN', etc
  amount_cents INT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
```

#### `wardrobe_items`
```sql
CREATE TABLE wardrobe_items (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  image_url TEXT NOT NULL,
  storage_path TEXT, -- Supabase storage path
  cdn_url TEXT, -- R2 URL
  
  -- Auto-tagged
  primary_color TEXT,
  primary_color_hex TEXT,
  secondary_colors JSONB,
  detected_style TEXT, -- 'casual', 'formal', 'sportwear', 'bohemian', etc
  detected_occasion TEXT[], -- ['office', 'casual']
  category TEXT, -- 'top', 'bottom', 'dress', 'shoes', 'accessory', 'outerwear'
  
  -- User-provided
  size TEXT,
  brand TEXT,
  price_paid DECIMAL(10,2),
  currency TEXT,
  purchase_date DATE,
  condition TEXT CHECK (condition IN ('new', 'like_new', 'good', 'fair')),
  user_tags TEXT[],
  user_notes TEXT,
  
  metadata JSONB DEFAULT '{}'::jsonb,
  
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  deleted_at TIMESTAMPTZ
);
CREATE INDEX idx_wardrobe_user ON wardrobe_items(user_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_wardrobe_category ON wardrobe_items(user_id, category) WHERE deleted_at IS NULL;
```

#### `body_analysis`
```sql
CREATE TABLE body_analysis (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  
  image_url TEXT, -- encrypted in R2
  storage_path TEXT,
  
  -- Body
  body_type TEXT CHECK (body_type IN ('apple', 'pear', 'hourglass', 'rectangle', 'inverted_triangle')),
  
  -- Color
  skin_tone_category TEXT CHECK (skin_tone_category IN ('warm', 'cool', 'neutral')),
  color_season TEXT CHECK (color_season IN ('spring', 'summer', 'autumn', 'winter')),
  detected_colors JSONB, -- {dominant_hex, secondary_hex, ...}
  best_colors JSONB, -- ['#hex1', '#hex2', ...]
  avoid_colors JSONB,
  
  -- Optional measurements
  shoulder_width_cm INT,
  bust_cm INT,
  waist_cm INT,
  hip_cm INT,
  inseam_cm INT,
  
  -- Notes
  notes TEXT,
  
  vision_api_response JSONB, -- raw response (debug)
  
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_body_analysis_user ON body_analysis(user_id, created_at DESC);
```

#### `try_ons`
```sql
CREATE TABLE try_ons (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  wardrobe_item_id UUID REFERENCES wardrobe_items(id) ON DELETE SET NULL,
  body_analysis_id UUID REFERENCES body_analysis(id) ON DELETE SET NULL,
  
  -- Cache lookup
  content_hash TEXT NOT NULL, -- SHA256(body_image + wardrobe_item + replicate_model_version)
  cache_hit BOOLEAN DEFAULT FALSE,
  cached_from_id UUID REFERENCES try_on_cache(id),
  
  -- Replicate
  replicate_model_version TEXT,
  replicate_prediction_id TEXT,
  inference_time_ms INT,
  
  -- Result
  status TEXT NOT NULL CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
  result_image_url TEXT,
  result_storage_path TEXT,
  result_cdn_url TEXT,
  error_message TEXT,
  
  -- Quality scores
  confidence_score DECIMAL(3,2), -- 0-1
  
  -- User feedback
  user_rating INT CHECK (user_rating BETWEEN 1 AND 5),
  fit_feedback TEXT CHECK (fit_feedback IN ('too_loose', 'too_tight', 'perfect', 'ok')),
  color_feedback TEXT CHECK (color_feedback IN ('clashes', 'okay', 'harmonious', 'amazing')),
  occasion_fit TEXT CHECK (occasion_fit IN ('too_casual', 'too_formal', 'just_right')),
  would_buy BOOLEAN,
  liked BOOLEAN DEFAULT FALSE,
  
  -- Engagement
  view_duration_seconds INT,
  shared BOOLEAN DEFAULT FALSE,
  saved_at TIMESTAMPTZ,
  
  created_at TIMESTAMPTZ DEFAULT now(),
  completed_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_try_ons_user ON try_ons(user_id, created_at DESC);
CREATE INDEX idx_try_ons_hash ON try_ons(content_hash);
CREATE INDEX idx_try_ons_status ON try_ons(status) WHERE status IN ('pending', 'processing');
```

#### `try_on_cache`
```sql
CREATE TABLE try_on_cache (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  content_hash TEXT NOT NULL UNIQUE, -- SHA256
  result_image_url TEXT NOT NULL,
  result_storage_path TEXT,
  result_cdn_url TEXT,
  replicate_model_version TEXT,
  hit_count INT DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT now(),
  last_hit_at TIMESTAMPTZ DEFAULT now(),
  expires_at TIMESTAMPTZ DEFAULT (now() + INTERVAL '90 days')
);
CREATE INDEX idx_try_on_cache_hash ON try_on_cache(content_hash);
CREATE INDEX idx_try_on_cache_expires ON try_on_cache(expires_at);
```

#### `recommendations`
```sql
CREATE TABLE recommendations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  occasion TEXT NOT NULL,
  season TEXT,
  
  -- Reasoning
  reason TEXT, -- por qué Claude recomendó
  color_harmony_score DECIMAL(3,2),
  body_fit_score DECIMAL(3,2),
  
  -- Engagement
  clicked BOOLEAN DEFAULT FALSE,
  liked BOOLEAN DEFAULT FALSE,
  tried_on BOOLEAN DEFAULT FALSE,
  
  -- A/B
  claude_model_version TEXT,
  prompt_version TEXT,
  
  created_at TIMESTAMPTZ DEFAULT now(),
  feedback_at TIMESTAMPTZ
);
CREATE INDEX idx_recos_user ON recommendations(user_id, created_at DESC);
```

#### `recommendation_items`
```sql
CREATE TABLE recommendation_items (
  recommendation_id UUID REFERENCES recommendations(id) ON DELETE CASCADE,
  wardrobe_item_id UUID REFERENCES wardrobe_items(id) ON DELETE CASCADE,
  position INT, -- orden visual
  role TEXT CHECK (role IN ('top', 'bottom', 'shoes', 'accessory', 'outerwear')),
  PRIMARY KEY (recommendation_id, wardrobe_item_id)
);
CREATE INDEX idx_reco_items_item ON recommendation_items(wardrobe_item_id);
```

#### `user_style_profile`
```sql
CREATE TABLE user_style_profile (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  
  -- Learned preferences
  preferred_styles JSONB, -- [{style, confidence, count}]
  preferred_colors JSONB,
  avoided_colors JSONB,
  occasion_preferences JSONB,
  favorite_brands JSONB,
  
  -- Demographics
  avg_price_point DECIMAL(10,2),
  budget_tier TEXT CHECK (budget_tier IN ('budget', 'mid', 'luxury')),
  trend_score DECIMAL(3,2), -- 0-1, follows trends?
  
  -- For Claude
  style_summary TEXT,
  
  calculated_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

#### `usage_counters`
```sql
CREATE TABLE usage_counters (
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  period_start DATE NOT NULL,
  try_ons_used INT DEFAULT 0,
  recommendations_used INT DEFAULT 0,
  body_analyses_used INT DEFAULT 0,
  PRIMARY KEY (user_id, period_start)
);
```

#### `idempotency_keys`
```sql
CREATE TABLE idempotency_keys (
  key TEXT PRIMARY KEY, -- UUID v4 from client
  user_id UUID REFERENCES auth.users(id),
  endpoint TEXT NOT NULL,
  request_hash TEXT, -- to detect different request with same key
  response_status INT,
  response_body JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  expires_at TIMESTAMPTZ DEFAULT (now() + INTERVAL '24 hours')
);
CREATE INDEX idx_idempotency_expires ON idempotency_keys(expires_at);
```

#### `audit_log`
```sql
CREATE TABLE audit_log (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID,
  action TEXT NOT NULL, -- 'login', 'upload_body', 'payment', 'delete_account'
  resource_type TEXT,
  resource_id TEXT,
  ip_address INET,
  user_agent TEXT,
  status TEXT CHECK (status IN ('success', 'failed')),
  error_message TEXT,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_audit_user ON audit_log(user_id, created_at DESC);
CREATE INDEX idx_audit_action ON audit_log(action, created_at DESC);
```

### 4.3 Row-Level Security (RLS)

**Patrón base:** Cada tabla user-specific habilita RLS y restringe acceso a `auth.uid() = user_id`.

```sql
-- Ejemplo profiles
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile" ON profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON profiles
  FOR UPDATE USING (auth.uid() = id) WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can insert own profile" ON profiles
  FOR INSERT WITH CHECK (auth.uid() = id);

-- service_role bypass para webhooks
-- (Supabase service_role automáticamente bypassa RLS)
```

**Total:** 32 policies (8 tablas user-specific × 4 ops: SELECT, INSERT, UPDATE, DELETE).

### 4.4 Triggers

```sql
-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_profiles_updated_at
  BEFORE UPDATE ON profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- (Repetir para todas las tablas con updated_at)
```

---

## 5. ARQUITECTURA DEL SISTEMA

### 5.1 Diagrama de componentes

```
┌──────────────────────────────────────────────────┐
│              FLUTTER MOBILE APP                  │
│  ├─ Riverpod (state management)                  │
│  ├─ go_router (navigation)                       │
│  ├─ supabase_flutter (auth + realtime + storage) │
│  └─ dio (HTTP client to FastAPI)                 │
└──────────────────────────────────────────────────┘
              │ HTTPS
              ▼
┌──────────────────────────────────────────────────┐
│            FASTAPI BACKEND (Railway)              │
│  ├─ Middleware:                                   │
│  │   ├─ Auth (JWT validation via JWKS)           │
│  │   ├─ Rate limiting (Redis)                    │
│  │   ├─ Idempotency-Key                          │
│  │   ├─ Request logging (JSON structured)        │
│  │   └─ CORS                                     │
│  ├─ Endpoints v1:                                │
│  │   ├─ /auth/*                                  │
│  │   ├─ /users/*                                 │
│  │   ├─ /wardrobe/*                              │
│  │   ├─ /body-analysis/*                         │
│  │   ├─ /try-ons/*                               │
│  │   ├─ /recommendations/*                       │
│  │   ├─ /subscriptions/*                         │
│  │   └─ /webhooks/* (stripe, mercadopago)        │
│  └─ Async:                                        │
│      └─ enqueue → ARQ                            │
└──┬──────────────────────┬────────────────────────┘
   │                      │
   ▼                      ▼
┌─────────┐         ┌──────────────────┐
│ ARQ     │         │ SUPABASE         │
│ Worker  │         │ ├─ Auth          │
│ (Redis) │         │ ├─ PostgreSQL    │
│         │         │ ├─ Realtime (WS) │
│ Tasks:  │         │ └─ Storage       │
│ ├─ Vision│        └────┬─────────────┘
│ ├─ Replicate│          │
│ ├─ Claude   │          │ async replication
│ ├─ R2 sync  │          ▼
│ └─ Cron     │     ┌──────────────────┐
└─────────────┘     │ CLOUDFLARE R2    │
                    │ (CDN, $0 egress) │
                    └──────────────────┘

External:
- Stripe + Mercado Pago (webhooks → /webhooks/*)
- Sentry (errors)
- PostHog (analytics)
- n8n (workflows)
- Resend (emails)
- OneSignal (push)
```

### 5.2 Flujo crítico: Virtual Try-On

```
1. Cliente Flutter: POST /try-ons
   Headers: Authorization, Idempotency-Key
   Body: { wardrobe_item_id, body_analysis_id }

2. FastAPI Backend:
   a. Validate JWT
   b. Check idempotency (return cached response if key exists)
   c. Check user quota (free 5/mes)
   d. Compute content_hash = SHA256(body_url + item_url + model_version)
   e. Lookup try_on_cache by hash
   f. IF cache hit:
      - INSERT try_ons (cache_hit=true, status='completed', result_url=cached.result_url)
      - Return 202 + try_on_id
   g. IF miss:
      - INSERT try_ons (status='pending')
      - Enqueue ARQ task
      - Return 202 + try_on_id

3. ARQ Worker:
   a. Fetch body_image + item_image URLs
   b. Call Replicate API
   c. Wait result (5-15s)
   d. Upload result to Supabase Storage
   e. UPDATE try_ons (status='completed', result_url, inference_time)
   f. INSERT try_on_cache (hash, result_url)
   g. Trigger Supabase Realtime publish

4. Cliente Flutter:
   - Subscribed to Realtime channel
   - Receives push notif on try_on_id update
   - Fetch result via GET /try-ons/{id}
   - Display result + feedback widget

5. Async: R2 replication
   - Cron worker copies new images from Supabase → R2
   - Updates cdn_url field
```

### 5.3 Estructura de directorios

```
asesor-imagen-ai/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── core/
│   │   │   ├── database.py
│   │   │   ├── security.py        (JWT validation Supabase)
│   │   │   ├── middleware.py
│   │   │   ├── exceptions.py
│   │   │   └── rate_limit.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── api/v1/
│   │   │   ├── router.py
│   │   │   └── endpoints/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── workers/                (ARQ tasks)
│   │   └── utils/
│   ├── migrations/
│   │   └── versions/
│   │       └── 001_initial_schema.sql
│   ├── tests/
│   ├── Dockerfile
│   ├── railway.json
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── lib/
│   │   ├── main.dart
│   │   ├── app.dart
│   │   ├── core/
│   │   │   ├── config/
│   │   │   ├── theme/
│   │   │   ├── routing/
│   │   │   ├── network/
│   │   │   └── errors/
│   │   ├── features/
│   │   │   ├── auth/{data,domain,presentation}/
│   │   │   ├── wardrobe/{...}/
│   │   │   ├── body_analysis/{...}/
│   │   │   ├── try_on/{...}/
│   │   │   ├── recommendations/{...}/
│   │   │   └── subscription/{...}/
│   │   └── shared/
│   ├── test/
│   ├── ios/, android/
│   ├── pubspec.yaml
│   └── .env.example
│
├── docs/
│   ├── MASTER_PLAN.md
│   ├── MASTER_PROMPT.md
│   ├── SDR.md
│   ├── ADR-001..006.md
│   ├── PRICING_STRATEGY.md
│   ├── INTEL_COMPETIDORES_2026.md
│   ├── design-system/
│   ├── mockups/
│   └── HANDOFF_PENDIENTES.md
│
├── .github/
│   └── workflows/
│       ├── backend-test.yml
│       ├── backend-deploy.yml
│       ├── flutter-test.yml
│       └── flutter-build.yml
│
└── README.md
```

---

## 6. API CONTRACTS

### 6.1 Convenciones

- Base URL: `https://api.asesor-imagen-ai.com/v1`
- Auth: `Authorization: Bearer <jwt>`
- Idempotency (POST críticos): `Idempotency-Key: <uuid v4>`
- Content-Type: `application/json`
- Errors: RFC 7807 Problem Details

### 6.2 Endpoints principales

#### Auth

```
POST /auth/register
Body: { email, password, country_code, preferred_language }
201: { user_id, access_token, refresh_token }

POST /auth/login
Body: { email, password }
200: { user_id, access_token, refresh_token }

POST /auth/refresh
Body: { refresh_token }
200: { access_token, refresh_token }

GET /auth/me
200: { id, email, profile: {...} }
```

#### Profile

```
GET /users/profile
200: { id, first_name, ..., notification_preferences }

PUT /users/profile
Body: { first_name?, last_name?, ... }
200: { ...updated profile }

DELETE /users/account
204 (soft delete + cascade)
```

#### Wardrobe

```
POST /wardrobe/items
multipart/form-data: { image, brand?, price?, ... }
202: { id, status: 'tagging' }
[ARQ Vision tagging async]

GET /wardrobe/items?cursor=...&limit=20&category=top&color=blue
200: { items: [...], next_cursor }

GET /wardrobe/items/{id}
200: { ...item }

PUT /wardrobe/items/{id}
Body: { user_tags?, user_notes?, ... }
200: { ...updated }

DELETE /wardrobe/items/{id}
204 (soft delete)
```

#### Body Analysis

```
POST /users/body-analysis
multipart/form-data: { image }
Headers: Idempotency-Key
202: { id, status: 'processing' }

GET /users/body-analysis/{id}
200: { id, status, body_type?, color_season?, best_colors?, ... }

GET /users/body-analysis/history
200: { analyses: [...] }
```

#### Try-On

```
POST /try-ons
Headers: Idempotency-Key
Body: { wardrobe_item_id, body_analysis_id? }
202: { id, status, cache_hit, estimated_time_seconds }

GET /try-ons/{id}
200: { id, status, result_url?, error?, feedback? }

GET /try-ons?cursor=...&limit=20
200: { try_ons: [...], next_cursor }

POST /try-ons/{id}/feedback
Body: { rating, fit_feedback?, color_feedback?, would_buy? }
200: { ...updated }
```

#### Recommendations

```
GET /recommendations?occasion=office&count=5
200: { recommendations: [{ id, items: [...], reason }] }

POST /recommendations/{id}/feedback
Body: { liked }
200: { ok }

GET /users/style-profile
200: { preferred_styles, preferred_colors, ... }
```

#### Subscriptions

```
POST /subscriptions/checkout-session
Body: { plan_type, billing_provider, currency }
200: { checkout_url }

GET /subscriptions/me
200: { plan_type, status, current_period_end, ... }

POST /subscriptions/cancel
200: { ...updated, cancel_at_period_end: true }

POST /webhooks/stripe
Headers: Stripe-Signature
200: { ok }

POST /webhooks/mercadopago
Headers: x-signature
200: { ok }
```

### 6.3 Error format

```json
{
  "type": "https://api.asesor-imagen-ai.com/errors/quota-exceeded",
  "title": "Quota exceeded",
  "status": 429,
  "detail": "You have used 5/5 free try-ons this month. Upgrade to Estilo for unlimited.",
  "instance": "/v1/try-ons",
  "code": "QUOTA_EXCEEDED",
  "upgrade_url": "https://api.../subscriptions/checkout-session"
}
```

---

## 7. SECURITY MODEL

### 7.1 Authentication & Authorization

- **Auth provider:** Supabase Auth (GoTrue)
- **Token type:** JWT HS256 (Supabase signs)
- **Validation:** FastAPI valida con JWKS endpoint Supabase
- **Authorization:** RLS en DB + middleware role check en endpoints admin

### 7.2 Threat model

| Amenaza | Mitigación |
|---------|-----------|
| SQL Injection | Prepared statements (asyncpg/SQLAlchemy) |
| XSS | Content-Type strict, no inline HTML |
| CSRF | Token-based auth (no cookies) |
| Brute force login | Supabase Auth + rate limit |
| Token theft | HTTPS only, short-lived JWT, refresh rotation |
| PII leak en logs | Filter middleware, no logear emails/URLs imágenes |
| Replay attacks | Idempotency-Key + timestamp validation |
| DDoS | Cloudflare + rate limit per IP |
| Quota bypass | Backend enforced, no trust client |
| Webhooks spoofing | Verify Stripe/MP signatures |

### 7.3 Encryption

- **Transit:** TLS 1.3 only
- **At rest (DB):** Supabase default encryption
- **At rest (R2):** Server-side encryption AES-256
- **At rest (PII corporal):** Adicionalmente, image encrypted con app-level key antes de upload

### 7.4 Compliance roadmap

- **MVP (sem 14):** GDPR + Ley 1581 Colombia
- **Sem 18:** LGPD Brasil
- **Sem 24:** SOC 2 Type I (post-funding)
- **Año 2:** SOC 2 Type II + ISO 27001

---

## 8. PERFORMANCE TARGETS

### 8.1 Backend

| Endpoint | p50 | p95 | p99 |
|----------|-----|-----|-----|
| GET /auth/me | <50ms | <150ms | <300ms |
| GET /wardrobe/items | <100ms | <300ms | <600ms |
| POST /wardrobe/items | <500ms | <1.5s | <3s |
| POST /try-ons (cache hit) | <100ms | <300ms | <500ms |
| POST /try-ons (cache miss) | <200ms | <500ms | <1s |
| Try-on completed e2e (cache hit) | <2s | <5s | <8s |
| Try-on completed e2e (cache miss) | <8s | <15s | <25s |
| GET /recommendations | <800ms | <2s | <4s |

### 8.2 Frontend

| Metric | Target |
|--------|--------|
| App size (download) | <30MB |
| Cold start | <3s |
| Hot start | <500ms |
| Screen transition | <200ms |
| Image load (CDN) | <500ms |
| Crash-free rate | >99.5% |

### 8.3 Caching strategy

- **Try-ons cache:** Postgres `try_on_cache` table, TTL 90 días
- **Claude prompt cache:** Anthropic native (4 min cache)
- **CDN cache:** Cloudflare R2, edge cache 1h
- **Client cache:** `cached_network_image` (Flutter), LRU 500MB

### 8.4 Cost optimization targets

| Item | Cost @ 50K paid | Optimization |
|------|-----------------|--------------|
| Replicate | $15K-22K/mo | ADR-004 caching (-35%) |
| Claude | $1.6K-4K/mo | Prompt cache (-60%) |
| Vision | $1.5K/mo | Resize before call |
| Storage | $80-150/mo | R2 vs Supabase Storage egress |
| Total mensual | ~$17K-20K/mo | Margen >85% |

---

## 9. INTEGRACIONES EXTERNAS

### 9.1 Google Vision API

- **Uso:** Body analysis, wardrobe auto-tagging
- **Endpoints usados:** `IMAGE_PROPERTIES`, `LABEL_DETECTION`, `DOMINANT_COLORS`
- **Pricing:** $1.50/1K calls
- **Fallback:** Manual tagging si API down
- **Auth:** Service account JSON

### 9.2 Replicate

- **Uso:** Virtual try-on
- **Modelo MVP:** IDM-VTON v2 o equivalente 2026 best-in-class
- **Pricing:** ~$0.05/inference
- **Fallback:** Queue + retry, notificar usuaria si >2min
- **Auth:** API token

### 9.3 Anthropic Claude

- **Uso:** Recommendations + style profile updates
- **Modelo MVP:** Claude Sonnet 4.6 (rec) o Haiku (style profile cron)
- **Pricing:** $3/$15 per 1M tokens (Sonnet)
- **Optimización:** Prompt caching (60% reducción)
- **Auth:** API key

### 9.4 Stripe

- **Uso:** Pagos US + global
- **Productos:** Subscription Estilo + Imagen
- **Pricing API:** % comisión
- **Webhooks:** invoice.payment_succeeded, customer.subscription.updated, etc

### 9.5 Mercado Pago

- **Uso:** Pagos LATAM (Colombia, México, Chile)
- **Productos:** Pagos recurrentes
- **Webhooks:** payment.created, payment.updated

### 9.6 Resend

- **Uso:** Emails transaccionales
- **Pricing:** $20/mes (50K emails)

### 9.7 OneSignal

- **Uso:** Push notifications
- **Pricing:** Free tier <10K subscribers

### 9.8 n8n

- **Uso:** Workflows automation
- **Hosting:** Self-hosted Railway

### 9.9 Sentry

- **Uso:** Error tracking + performance
- **Pricing:** Free tier 5K errors/mes

### 9.10 PostHog

- **Uso:** Product analytics + funnels + feature flags
- **Pricing:** Free tier 1M events/mes

---

## 10. CONSTRAINTS Y ASSUMPTIONS

### 10.1 Constraints técnicos

- **Flutter 3.41.5** fixed (Brook lo levantó). Upgrade solo en releases majores
- **Python 3.11** fixed (asyncio mature)
- **PostgreSQL 16** (Supabase managed)
- **Railway free tier no soporta workers persistentes** → Pro tier desde sem 5
- **Stripe no opera en Argentina + Venezuela** → solo Mercado Pago

### 10.2 Constraints comerciales

- **MVP launch sem 14** (Jul 31, 2026)
- **Free tier obligatorio** para acquisition (decidido por Leo)
- **Privacy LATAM** debe ser de clase mundial (objeción #1 Yang)

### 10.3 Constraints regulatorios

- **GDPR** desde launch (incluso para LATAM users por imagen corporal)
- **Habeas Data Colombia** (Ley 1581)
- **Consumer protection LATAM** (right to refund 7 días)

### 10.4 Assumptions críticas

- **Replicate calidad superior a Acloset** validable sem 4 (línea roja)
- **Cache hit rate >35%** alcanzable a 50K paid (Alejo TBD validar)
- **Conversión free→paid 5-8%** alcanzable con paywall agresivo
- **MAU free no supera 1M** en mes 12 (si supera, ADR-007 activa)
- **Influencers LATAM convertibles a 2-3% de su audiencia** (industry benchmark)

---

## 11. GLOSARIO

| Término | Definición |
|---------|-----------|
| **ADR** | Architecture Decision Record |
| **ARPU** | Average Revenue Per User |
| **ARQ** | Async Redis Queue (Python) |
| **CAC** | Customer Acquisition Cost |
| **CDN** | Content Delivery Network (Cloudflare R2) |
| **DAU** | Daily Active Users |
| **GDPR** | General Data Protection Regulation (EU) |
| **JWKS** | JSON Web Key Set (endpoint Supabase) |
| **JWT** | JSON Web Token |
| **LGPD** | Lei Geral de Proteção de Dados (Brasil) |
| **LTV** | Lifetime Value |
| **MAU** | Monthly Active Users |
| **MRR** | Monthly Recurring Revenue |
| **MVP** | Minimum Viable Product |
| **Path A** | Modelo financiero 50K paid puros (ADR-006) |
| **PII** | Personally Identifiable Information |
| **RLS** | Row-Level Security (PostgreSQL) |
| **SDR** | Software Design Record |
| **TTV** | Time To Value |
| **WCAG** | Web Content Accessibility Guidelines |

---

## 📎 ANEXOS

- **ADRs detallados:** `docs/ADR-001..006.md`
- **Plan de ejecución:** `docs/MASTER_PLAN.md`
- **Pricing strategy:** `docs/PRICING_STRATEGY.md`
- **Inteligencia competidores:** `docs/INTEL_COMPETIDORES_2026.md`
- **Design system:** `docs/design-system/`
- **Mockups:** `docs/mockups/`

---

**SDR aprobado para implementación.**

**Owner técnico:** Alejo (Solutions Architect)
**Owner producto:** Jarvis (CEO)
**Sponsor:** Juan Camilo Gil (Accionista)

**Próximo paso:** Sprint 0 ejecución según `MASTER_PROMPT.md`.
