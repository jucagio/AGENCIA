-- =============================================================
-- Migration 007: Option F — FSM, Cache Tier, Lazy Reset (Sprint 0.5 T2)
-- =============================================================
-- Owner: Sasha (Backend & Security)
-- Reviewed by: Alejo (Architecture)
-- Sprint: 0.5 — Worker Integration
--
-- INTENT:
--   1. Add FSM (Finite State Machine) state tracking to try_ons.
--   2. Add fashn_mode (performance/balanced/quality) per try-on.
--   3. Add cache_tier column for cache hit observability.
--   4. Add per-tier weekly counters to usage_counters (base/std/pro).
--   5. Add lazy reset PostgreSQL function (fallback for Antigravity cron — Q5).
--
-- ROLLBACK: See 007_optionf_fsm_cache_tier_down.sql
-- =============================================================

BEGIN;

-- ─────────────────────────────────────────────────────────────
-- 1. ALTER try_ons — FSM + fashn_mode + fallback tracking
-- ─────────────────────────────────────────────────────────────

ALTER TABLE public.try_ons
    ADD COLUMN IF NOT EXISTS fashn_mode TEXT
        CHECK (fashn_mode IN ('performance', 'balanced', 'quality')),
    ADD COLUMN IF NOT EXISTS fsm_state TEXT NOT NULL DEFAULT 'queued'
        CHECK (fsm_state IN (
            'queued',
            'cache_lookup',
            'cache_hit',
            'inference_running',
            'uploading',
            'completed',
            'failed',
            'fallback_triggered'
        )),
    ADD COLUMN IF NOT EXISTS fsm_history JSONB NOT NULL DEFAULT '[]'::jsonb,
    ADD COLUMN IF NOT EXISTS fallback_used BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS cache_tier TEXT
        CHECK (cache_tier IN ('hot', 'warm', 'cold', 'miss'));

-- Partial index for queries that look for in-flight try-ons.
-- WHERE clause is IMMUTABLE — values are constants.
DROP INDEX IF EXISTS idx_try_ons_fsm_active;
CREATE INDEX idx_try_ons_fsm_active
    ON public.try_ons (fsm_state, created_at DESC)
    WHERE fsm_state NOT IN ('completed', 'failed');

-- ─────────────────────────────────────────────────────────────
-- 2. ALTER usage_counters — per-tier weekly buckets
-- ─────────────────────────────────────────────────────────────
-- Free/Estilo/Imagen tiers have different caps. We track each independently
-- so analytics can answer "how much did paid tier consume this week?".

ALTER TABLE public.usage_counters
    ADD COLUMN IF NOT EXISTS try_ons_base_used INT NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS try_ons_std_used  INT NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS try_ons_pro_used  INT NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS week_start_date   DATE;

-- Backfill week_start_date from period_start (Monday of period_start's ISO week).
UPDATE public.usage_counters
SET week_start_date = date_trunc('week', period_start)::DATE
WHERE week_start_date IS NULL;

CREATE INDEX IF NOT EXISTS idx_usage_counters_week
    ON public.usage_counters (user_id, week_start_date DESC);

-- ─────────────────────────────────────────────────────────────
-- 3. FUNCTION: reset_usage_if_stale (Q5 — Lazy Reset Fallback)
-- ─────────────────────────────────────────────────────────────
-- Called on every GET /users/me/usage and POST /try-ons (before cap check).
-- If the user's row is from a previous ISO week, zero counters & advance
-- week_start_date. This is the safety net in case the Antigravity weekly
-- cron job fails or runs late.
--
-- Atomic: uses row lock via SELECT ... FOR UPDATE.

CREATE OR REPLACE FUNCTION public.reset_usage_if_stale(p_user_id UUID)
RETURNS TABLE (
    user_id            UUID,
    week_start_date    DATE,
    try_ons_used       INT,
    try_ons_base_used  INT,
    try_ons_std_used   INT,
    try_ons_pro_used   INT,
    was_reset          BOOLEAN
)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
    v_current_week DATE := date_trunc('week', CURRENT_DATE)::DATE;
    v_row          public.usage_counters;
    v_was_reset    BOOLEAN := FALSE;
BEGIN
    -- Acquire row lock (or NULL if no row exists yet).
    SELECT * INTO v_row
    FROM public.usage_counters
    WHERE public.usage_counters.user_id = p_user_id
    ORDER BY week_start_date DESC NULLS LAST
    LIMIT 1
    FOR UPDATE;

    IF v_row.user_id IS NULL THEN
        -- No counter row yet — caller will create on first increment.
        RETURN QUERY SELECT
            p_user_id, v_current_week, 0, 0, 0, 0, FALSE;
        RETURN;
    END IF;

    -- Stale? Reset.
    IF v_row.week_start_date IS NULL OR v_row.week_start_date < v_current_week THEN
        UPDATE public.usage_counters
        SET try_ons_used        = 0,
            try_ons_base_used   = 0,
            try_ons_std_used    = 0,
            try_ons_pro_used    = 0,
            week_start_date     = v_current_week,
            period_start        = v_current_week
        WHERE public.usage_counters.user_id = p_user_id
          AND public.usage_counters.period_start = v_row.period_start;
        v_was_reset := TRUE;

        SELECT * INTO v_row
        FROM public.usage_counters
        WHERE public.usage_counters.user_id = p_user_id
          AND public.usage_counters.week_start_date = v_current_week;
    END IF;

    RETURN QUERY SELECT
        v_row.user_id,
        v_row.week_start_date,
        v_row.try_ons_used,
        v_row.try_ons_base_used,
        v_row.try_ons_std_used,
        v_row.try_ons_pro_used,
        v_was_reset;
END;
$$;

REVOKE ALL ON FUNCTION public.reset_usage_if_stale(UUID) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.reset_usage_if_stale(UUID) TO service_role;

COMMENT ON FUNCTION public.reset_usage_if_stale IS
'Lazy reset fallback (Sprint 0.5 Q5). Resets weekly try-on counters if user row is from a previous ISO week. Service-role only.';

-- ─────────────────────────────────────────────────────────────
-- 4. RLS Verification helper (read-only)
-- ─────────────────────────────────────────────────────────────
-- Returns 1 row per policy that protects try_ons / usage_counters.
-- Used by T5 verification step. Service-role only.

CREATE OR REPLACE FUNCTION public.verify_rls_policies()
RETURNS TABLE (
    schemaname  TEXT,
    tablename   TEXT,
    policyname  TEXT,
    cmd         TEXT,
    qual        TEXT
)
LANGUAGE sql
SECURITY DEFINER
SET search_path = public, pg_catalog
AS $$
    SELECT
        p.schemaname::TEXT,
        p.tablename::TEXT,
        p.policyname::TEXT,
        p.cmd::TEXT,
        p.qual::TEXT
    FROM pg_policies p
    WHERE p.schemaname = 'public'
      AND p.tablename IN ('try_ons', 'usage_counters', 'wardrobe_items', 'body_analysis')
    ORDER BY p.tablename, p.policyname;
$$;

REVOKE ALL ON FUNCTION public.verify_rls_policies() FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.verify_rls_policies() TO service_role;

COMMIT;

-- =============================================================
-- POST-DEPLOY VERIFICATION (run manually, do not commit results)
-- =============================================================
-- 1. RLS policies present:
--    SELECT * FROM public.verify_rls_policies();
--
-- 2. Cross-tenant isolation (run as a known user JWT, should return 0 rows):
--    SELECT COUNT(*) FROM public.try_ons
--    WHERE user_id != auth.uid();
--
-- 3. FSM state distribution:
--    SELECT fsm_state, COUNT(*) FROM public.try_ons GROUP BY fsm_state;
--
-- 4. Lazy reset smoke test (as service_role):
--    SELECT * FROM public.reset_usage_if_stale('<some-uuid>'::uuid);
-- =============================================================
