-- =============================================================
-- Migration 008: Tighten try_ons UPDATE RLS (FIX 1)
-- =============================================================
-- Owner: Sasha (Backend & Security)
-- Reviewed by: Alejo (Architecture)
-- Sprint: 0.5 — Worker Integration (post-007)
-- Depends on: 005_rls_policies.sql, 007_optionf_fsm_cache_tier.sql
--
-- INTENT (FIX 1 — Cyber Neo audit finding):
--   The legacy policy `try_ons_update` (005:43) allowed users to UPDATE any
--   column on their own try_ons row — including security-critical fields
--   introduced in 007 (`fsm_state`, `fsm_history`, `cache_tier`,
--   `fallback_used`, `fashn_mode`). A malicious user could spoof
--   `fsm_state='completed'` and bypass worker-side billing / quota logic.
--
--   This migration:
--     1. DROPs the permissive policy.
--     2. Replaces it with a deny-all UPDATE policy. Direct PostgREST
--        UPDATEs from user JWTs are now blocked.
--     3. Service-role (worker, AdminClient.with_user_check) bypasses RLS
--        and continues to write FSM transitions as before.
--     4. Exposes `update_try_on_user_fields(uuid, jsonb)` SECURITY DEFINER
--        RPC for the narrow set of columns users SHOULD be able to mutate
--        (currently: `notes`, `archived`). Whitelist-enforced; any other
--        column raises `insufficient_privilege`.
--
-- ROLLBACK: See 008_tighten_try_ons_update_down.sql
-- =============================================================

BEGIN;

-- ─────────────────────────────────────────────────────────────
-- 0. Pre-flight: ensure user-mutable columns exist
-- ─────────────────────────────────────────────────────────────
-- The RPC whitelist references `notes` and `archived`. If 004 didn't
-- create them, add them here so the RPC is callable from day one.

ALTER TABLE public.try_ons
    ADD COLUMN IF NOT EXISTS notes    TEXT,
    ADD COLUMN IF NOT EXISTS archived BOOLEAN NOT NULL DEFAULT FALSE;

-- ─────────────────────────────────────────────────────────────
-- 1. Drop legacy permissive UPDATE policy
-- ─────────────────────────────────────────────────────────────

DROP POLICY IF EXISTS "try_ons_update" ON public.try_ons;

-- ─────────────────────────────────────────────────────────────
-- 2. Replace with deny-all UPDATE policy
-- ─────────────────────────────────────────────────────────────
-- USING (false) + WITH CHECK (false) → no row visible for UPDATE,
-- no row passes the post-update check. Effectively, all UPDATEs
-- coming through a non-service-role JWT return "UPDATE 0".
--
-- service_role bypasses RLS entirely (Supabase default), so workers
-- using AdminClient continue to function unchanged.

CREATE POLICY "try_ons_update_service_role_only"
    ON public.try_ons
    FOR UPDATE
    USING (false)
    WITH CHECK (false);

COMMENT ON POLICY "try_ons_update_service_role_only" ON public.try_ons IS
'FIX 1 (Cyber Neo): direct user UPDATEs are denied. Use RPC update_try_on_user_fields() for user-mutable columns; service_role (worker) bypasses RLS for FSM transitions.';

-- ─────────────────────────────────────────────────────────────
-- 3. Whitelist-enforced RPC for user-mutable columns
-- ─────────────────────────────────────────────────────────────
-- Accepts a JSONB patch object. Only keys present in the whitelist
-- are applied; any other key raises insufficient_privilege.
-- Returns the updated row so the caller can refresh client state
-- without a second SELECT roundtrip.
--
-- Security notes:
--   * SECURITY DEFINER → runs as table owner, bypassing RLS.
--   * search_path pinned to (public, pg_temp). auth.uid() is invoked
--     with explicit schema-qualified call to prevent search_path
--     hijacking (Supabase hardening guideline).
--   * auth.uid() IS NULL check rejects anon JWTs.
--   * format('%I', col) safely quotes identifiers from the whitelist
--     (whitelist is checked BEFORE format() is called).
--   * Values are bound via USING ($1) — not string-interpolated —
--     so JSON values cannot inject SQL.

CREATE OR REPLACE FUNCTION public.update_try_on_user_fields(
    p_try_on_id UUID,
    p_updates   JSONB
)
RETURNS public.try_ons
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
DECLARE
    -- Whitelist of columns users may mutate via this RPC.
    -- Add to this set only after a security review.
    v_allowed   CONSTANT TEXT[] := ARRAY['notes', 'archived'];
    v_caller    UUID := auth.uid();
    v_key       TEXT;
    v_set_parts TEXT[] := ARRAY[]::TEXT[];
    v_sql       TEXT;
    v_row       public.try_ons;
BEGIN
    -- 1. Reject anonymous callers.
    IF v_caller IS NULL THEN
        RAISE EXCEPTION 'authentication required'
            USING ERRCODE = '28000';  -- invalid_authorization_specification
    END IF;

    -- 2. Reject empty / non-object patches.
    IF p_updates IS NULL
       OR jsonb_typeof(p_updates) <> 'object'
       OR p_updates = '{}'::jsonb THEN
        RAISE EXCEPTION 'p_updates must be a non-empty JSON object'
            USING ERRCODE = '22023';  -- invalid_parameter_value
    END IF;

    -- 3. Validate every key against the whitelist BEFORE building SQL.
    FOR v_key IN SELECT jsonb_object_keys(p_updates) LOOP
        IF NOT (v_key = ANY (v_allowed)) THEN
            RAISE EXCEPTION 'field % not allowed for user update', v_key
                USING ERRCODE = '42501';  -- insufficient_privilege
        END IF;

        -- Build "col = (p_updates ->> 'col')::<type>" fragments.
        -- Identifier is whitelisted; cast is hardcoded per column.
        IF v_key = 'notes' THEN
            v_set_parts := v_set_parts ||
                format('%I = ($1 ->> %L)::TEXT', v_key, v_key);
        ELSIF v_key = 'archived' THEN
            v_set_parts := v_set_parts ||
                format('%I = ($1 ->> %L)::BOOLEAN', v_key, v_key);
        END IF;
    END LOOP;

    -- 4. Execute the UPDATE scoped to the caller's own row.
    --    Note: this function runs as DEFINER, so RLS is bypassed —
    --    the WHERE clause is the ONLY tenant guard. Do not remove it.
    v_sql := format(
        'UPDATE public.try_ons SET %s, updated_at = NOW() '
        'WHERE id = $2 AND user_id = $3 RETURNING *',
        array_to_string(v_set_parts, ', ')
    );

    EXECUTE v_sql
        INTO v_row
        USING p_updates, p_try_on_id, v_caller;

    -- 5. No row → either not found OR belongs to another user.
    --    Return same error in both cases (no enumeration).
    IF v_row.id IS NULL THEN
        RAISE EXCEPTION 'try_on % not found', p_try_on_id
            USING ERRCODE = 'P0002';  -- no_data_found
    END IF;

    RETURN v_row;
END;
$$;

REVOKE ALL ON FUNCTION public.update_try_on_user_fields(UUID, JSONB) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.update_try_on_user_fields(UUID, JSONB) TO authenticated;

COMMENT ON FUNCTION public.update_try_on_user_fields(UUID, JSONB) IS
'FIX 1 (Cyber Neo): user-side UPDATE proxy for try_ons. Whitelisted columns only (notes, archived). FSM / cache / fashn_mode are service_role-only.';

COMMIT;

-- =============================================================
-- POST-DEPLOY VERIFICATION (staging — DO NOT run on prod data)
-- =============================================================
-- A. Confirm policy was replaced:
--    SELECT policyname, cmd, qual, with_check
--    FROM pg_policies
--    WHERE schemaname='public' AND tablename='try_ons' AND cmd='UPDATE';
--    -- Expected: 1 row, policyname='try_ons_update_service_role_only',
--    --           qual='false', with_check='false'.
--
-- B. As authenticated user (RLS active) — must FAIL / 0 rows:
--    SELECT set_config('request.jwt.claims',
--           json_build_object('sub','<user-uuid>')::text, false);
--    UPDATE public.try_ons SET fsm_state='completed'
--        WHERE id='<own-try-on-id>';
--    -- Expected: UPDATE 0
--
-- C. As authenticated user via RPC — must SUCCEED:
--    SELECT (public.update_try_on_user_fields(
--                '<own-try-on-id>'::uuid,
--                '{"notes":"Great fit","archived":false}'::jsonb
--           )).id;
--    -- Expected: returns the try_on uuid.
--
-- D. As authenticated user, RPC with disallowed key — must RAISE 42501:
--    SELECT public.update_try_on_user_fields(
--               '<own-try-on-id>'::uuid,
--               '{"fsm_state":"completed"}'::jsonb);
--    -- Expected: ERROR 42501 field fsm_state not allowed for user update
--
-- E. As authenticated user, RPC against another user's row — must RAISE P0002:
--    SELECT public.update_try_on_user_fields(
--               '<other-user-try-on-id>'::uuid,
--               '{"notes":"hijack"}'::jsonb);
--    -- Expected: ERROR P0002 try_on ... not found
--
-- F. As service_role (worker) — must SUCCEED:
--    UPDATE public.try_ons SET fsm_state='completed', cache_tier='hot'
--        WHERE id='<any-try-on-id>';
--    -- Expected: UPDATE 1
-- =============================================================
