-- Rollback for migration 007.
-- Drops the FSM columns, per-tier counters, and lazy-reset function.

BEGIN;

DROP FUNCTION IF EXISTS public.reset_usage_if_stale(UUID);
DROP FUNCTION IF EXISTS public.verify_rls_policies();

DROP INDEX IF EXISTS public.idx_try_ons_fsm_active;
DROP INDEX IF EXISTS public.idx_usage_counters_week;

ALTER TABLE public.try_ons
    DROP COLUMN IF EXISTS fashn_mode,
    DROP COLUMN IF EXISTS fsm_state,
    DROP COLUMN IF EXISTS fsm_history,
    DROP COLUMN IF EXISTS fallback_used,
    DROP COLUMN IF EXISTS cache_tier;

ALTER TABLE public.usage_counters
    DROP COLUMN IF EXISTS try_ons_base_used,
    DROP COLUMN IF EXISTS try_ons_std_used,
    DROP COLUMN IF EXISTS try_ons_pro_used,
    DROP COLUMN IF EXISTS week_start_date;

COMMIT;
