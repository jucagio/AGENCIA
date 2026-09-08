# Migrations Checklist — Asesor de Imagen AI

**Owner:** Sasha (Backend & Security)
**Last update:** 2026-05-22 (Sprint Fase 1 — Supabase Real)

---

## Ruta de aplicación recomendada para PRODUCCIÓN (fresh start)

Para un proyecto Supabase NUEVO y VACÍO, aplicar EN ESTE ORDEN:

| # | Archivo | Tipo | Idempotente | Obligatoria |
|---|---------|------|-------------|-------------|
| 1 | `004_consolidated_schema_v2.sql` | Schema (12 tablas, ADR-001) | ✅ | ✅ |
| 2 | `002_storage_buckets.sql` | Storage buckets + RLS storage | ✅ | ✅ |
| 3 | `005_rls_policies.sql` | RLS policies user-scoped | ✅ | ✅ |
| 4 | `006_rate_limit_rpc.sql` | RPC atómico para rate limit | ✅ (CREATE OR REPLACE) | ✅ |
| 5 | `007_optionf_fsm_cache_tier.sql` | FSM + cache tier + lazy reset | ✅ | ✅ |
| 6 | `008_tighten_try_ons_update.sql` | Tightening RLS try_ons (FIX 1 Cyber Neo) | ✅ | ✅ |

**NO aplicar en producción nueva:**
- `001_initial_schema.sql` — Legacy (tabla `users` propia, pre-ADR-001)
- `003_adr001_profiles_migration.sql` — Solo para upgrade incremental desde M001

---

## Qué hace cada migración

### `004_consolidated_schema_v2.sql` — Schema base
Crea las 12 tablas oficiales del modelo de datos (ADR-001):
- `profiles` — extiende `auth.users` (FK a `auth.users(id)`)
- `subscriptions` — tier, status, periodo de billing
- `wardrobe_items` — prendas del usuario (categoría, color, talla, URL)
- `body_analysis` — análisis corporal Google Vision (landmarks, measurements)
- `try_ons` — virtual try-ons (input/output URLs, FASHN mode, status)
- `try_on_cache` — cache de resultados (hash → URL) para evitar re-ejecutar FASHN
- `recommendations` + `recommendation_items` — outfits sugeridos por Claude
- `user_style_profile` — perfil de estilo persistente
- `usage_counters` — contadores semanales por tier (base/std/pro)
- `idempotency_keys` — para POST seguros
- `audit_log` — append-only audit trail

DROP CASCADE al inicio + IF NOT EXISTS = idempotente desde estado vacío.

### `002_storage_buckets.sql` — Buckets + storage policies
- Crea buckets `avatars` (private), `wardrobe` (private), `tryons` (public).
- Aplica RLS sobre `storage.objects` con folder-based isolation (`{user_id}/...`).
- **Idempotente:** `INSERT ... ON CONFLICT DO NOTHING` + `DROP POLICY IF EXISTS`.

### `005_rls_policies.sql` — RLS user-scoped
- Habilita RLS en todas las tablas user-scoped.
- Define policies SELECT/INSERT/UPDATE/DELETE con `auth.uid() = user_id` (o `auth.uid() = id` para profiles).
- `usage_counters`: SELECT only para users; writes solo via service_role + RPC.
- `audit_log`, `idempotency_keys`, `try_on_cache`: RLS habilitado, sin policies de user (solo service_role).
- **Idempotente** (parchada Fase 1): cada `CREATE POLICY` precedido por `DROP POLICY IF EXISTS`.

### `006_rate_limit_rpc.sql` — Rate limit atómico
- Función `increment_weekly_tryon_usage(user_id, cap)` con `SECURITY DEFINER`.
- Atomic UPDATE ... WHERE usage < cap RETURNING (row lock) → previene race condition.
- Returna nuevo valor si OK, valor actual si capped.
- **Idempotente:** `CREATE OR REPLACE FUNCTION`.

### `007_optionf_fsm_cache_tier.sql` — FSM + cache tier + lazy reset
- Agrega columnas a `try_ons`: `fsm_state`, `fsm_history`, `cache_tier`, `fallback_used`, `fashn_mode`.
- Agrega columnas a `usage_counters`: contadores por tier (base/std/pro).
- Función `lazy_reset_weekly_counters()` — fallback si no hay cron job.
- **Idempotente:** `ADD COLUMN IF NOT EXISTS`.

### `008_tighten_try_ons_update.sql` — RLS hardening (Cyber Neo FIX 1)
- DROP policy `try_ons_update` (user-scoped, demasiado permisiva).
- CREATE policy `try_ons_update_service_role_only` (solo service_role escribe).
- CREATE función `update_try_on_user_fields(...)` — endpoint controlado para que el user actualice solo campos seguros (rating, notes).
- Cierra vector: user no puede spoofear `fsm_state='completed'` para bypass de billing.

---

## Verificación post-aplicación

Después de correr las 6 migraciones, validar:

```sql
-- 1. Tablas creadas (12)
SELECT count(*) FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN (
    'profiles', 'subscriptions', 'wardrobe_items', 'body_analysis',
    'try_ons', 'try_on_cache', 'recommendations', 'recommendation_items',
    'user_style_profile', 'usage_counters', 'idempotency_keys', 'audit_log'
  );
-- expect: 12

-- 2. RLS activo en todas
SELECT tablename FROM pg_tables
WHERE schemaname = 'public' AND rowsecurity = false;
-- expect: 0 rows

-- 3. Policies activas
SELECT count(*) FROM pg_policies WHERE schemaname = 'public';
-- expect: >=24

-- 4. Buckets
SELECT id FROM storage.buckets WHERE id IN ('avatars', 'wardrobe', 'tryons');
-- expect: 3 rows

-- 5. RPCs disponibles
SELECT proname FROM pg_proc
WHERE pronamespace = 'public'::regnamespace
  AND proname IN ('increment_weekly_tryon_usage', 'update_try_on_user_fields', 'lazy_reset_weekly_counters');
-- expect: 3 rows

-- 6. try_ons UPDATE locked (Cyber Neo FIX 1)
SELECT polname FROM pg_policy
WHERE polrelid = 'public.try_ons'::regclass AND polcmd = 'w';
-- expect: 'try_ons_update_service_role_only' (NOT 'try_ons_update')
```

---

## Cambios Fase 1 (2026-05-22)

- ✅ M005 parchada con `DROP POLICY IF EXISTS` en TODAS las policies (era no-idempotente).
- ✅ M002 parchada con `INSERT ... ON CONFLICT DO NOTHING` para buckets + `DROP POLICY IF EXISTS` para storage policies.
- ✅ M001 + M003 marcadas como legacy (no aplicar en producción nueva).
