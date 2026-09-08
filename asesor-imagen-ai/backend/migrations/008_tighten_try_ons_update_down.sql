-- =============================================================
-- Migration 008 DOWN: Revert RLS tightening on try_ons UPDATE
-- =============================================================
-- WARNING: this rollback restores the permissive policy from 005.
-- Only use if 008 broke production and a hotfix is not yet ready.
-- Re-introduces FIX 1 vulnerability (users can spoof fsm_state).
-- =============================================================

BEGIN;

DROP FUNCTION IF EXISTS public.update_try_on_user_fields(UUID, JSONB);

DROP POLICY IF EXISTS "try_ons_update_service_role_only" ON public.try_ons;

CREATE POLICY "try_ons_update"
    ON public.try_ons
    FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Note: we deliberately keep the `notes` and `archived` columns —
-- dropping them would lose user data. They are safe to retain.

COMMIT;
