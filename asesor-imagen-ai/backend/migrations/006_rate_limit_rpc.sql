-- Migration 006: Atomic Rate Limit Fallback (Sprint 0.4 - Task A1)
-- CR-4: Fallback Postgres no atómico bajo concurrencia -> UPDATE ... WHERE usage < 3 RETURNING ... (row lock)

CREATE OR REPLACE FUNCTION increment_weekly_tryon_usage(p_user_id UUID, p_cap INT)
RETURNS INT
LANGUAGE plpgsql
SECURITY DEFINER -- Needs to bypass RLS if called by service_role
AS $$
DECLARE
    v_new_usage INT;
BEGIN
    -- Atomic row lock and update
    -- If usage_this_week < p_cap, increment and return new value.
    -- If already >= p_cap, do not update, and return current value.
    
    UPDATE public.users
    SET usage_this_week = usage_this_week + 1
    WHERE id = p_user_id AND usage_this_week < p_cap
    RETURNING usage_this_week INTO v_new_usage;

    IF v_new_usage IS NULL THEN
        -- It means the WHERE clause failed because usage_this_week >= p_cap
        -- We just SELECT the current usage
        SELECT usage_this_week INTO v_new_usage
        FROM public.users
        WHERE id = p_user_id;
    END IF;

    RETURN v_new_usage;
END;
$$;
