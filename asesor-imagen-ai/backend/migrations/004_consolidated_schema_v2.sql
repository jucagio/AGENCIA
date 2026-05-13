-- =============================================================
-- Migration 004: Consolidated Schema V2 (ADR-001 Compliant)
-- =============================================================
-- INTENT: Establishes the full 12-table schema from a clean state.
--
-- ⚠️  PRODUCTION GUIDANCE:
--   This migration ASSUMES an empty database or a fully reproducible
--   environment (CI, staging fresh clone, local Docker reset).
--   For production upgrades from an existing Supabase project, use
--   migration 003 (003_adr001_profiles_migration.sql) which is the
--   incremental path.
--
-- DECISION (see docs/DECISIONES_PENDIENTES.md §Sprint 0.2):
--   Migration 004 is the source of truth for schema structure.
--   Migration 003 is the incremental upgrade path for prod.
--
-- ROLLBACK: Run migrations/004_consolidated_schema_v2_down.sql
-- =============================================================
-- Replaces initial schema with full 12-table model.
-- All user FKs point to auth.users(id).
-- =============================================================

-- 1. DROP ALL EXISTING TABLES (idempotent — IF EXISTS prevents errors on clean DBs)
-- NOTE: CASCADE is intentional; FK dependencies are rebuilt below.
DROP TABLE IF EXISTS public.audit_log CASCADE;
DROP TABLE IF EXISTS public.idempotency_keys CASCADE;
DROP TABLE IF EXISTS public.usage_counters CASCADE;
DROP TABLE IF EXISTS public.user_style_profile CASCADE;
DROP TABLE IF EXISTS public.recommendation_items CASCADE;
DROP TABLE IF EXISTS public.recommendations CASCADE;
DROP TABLE IF EXISTS public.try_ons CASCADE;
DROP TABLE IF EXISTS public.try_on_cache CASCADE;
DROP TABLE IF EXISTS public.body_analysis CASCADE;
DROP TABLE IF EXISTS public.wardrobe_items CASCADE;
DROP TABLE IF EXISTS public.subscriptions CASCADE;
DROP TABLE IF EXISTS public.profiles CASCADE;
DROP TABLE IF EXISTS public.users CASCADE; -- legacy table, just in case
DROP TABLE IF EXISTS public.analytics_events CASCADE;
DROP TABLE IF EXISTS public.outfits CASCADE;

-- 2. CREATE TABLES (IF NOT EXISTS provides extra idempotency safety)

-- profiles
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    first_name TEXT,
    last_name TEXT,
    avatar_url TEXT,
    date_of_birth DATE,
    country_code TEXT,
    preferred_language TEXT DEFAULT 'es',
    notification_preferences JSONB DEFAULT '{"push": true, "email": true}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    deleted_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_profiles_country ON profiles(country_code);

-- subscriptions
CREATE TABLE IF NOT EXISTS public.subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    plan_type TEXT NOT NULL CHECK (plan_type IN ('free', 'estilo', 'imagen')),
    billing_provider TEXT CHECK (billing_provider IN ('stripe', 'mercadopago')),
    external_subscription_id TEXT,
    external_customer_id TEXT,
    status TEXT NOT NULL CHECK (status IN ('trialing', 'active', 'past_due', 'canceled', 'expired')),
    trial_ends_at TIMESTAMPTZ,
    current_period_start TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    canceled_at TIMESTAMPTZ,
    currency TEXT,
    amount_cents INT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON subscriptions(status);

-- wardrobe_items
CREATE TABLE IF NOT EXISTS public.wardrobe_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    image_url TEXT NOT NULL,
    storage_path TEXT,
    cdn_url TEXT,
    primary_color TEXT,
    primary_color_hex TEXT,
    secondary_colors JSONB,
    detected_style TEXT,
    detected_occasion TEXT[],
    category TEXT,
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
CREATE INDEX IF NOT EXISTS idx_wardrobe_user ON wardrobe_items(user_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_wardrobe_category ON wardrobe_items(user_id, category) WHERE deleted_at IS NULL;

-- body_analysis
CREATE TABLE IF NOT EXISTS public.body_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    image_url TEXT,
    storage_path TEXT,
    body_type TEXT CHECK (body_type IN ('apple', 'pear', 'hourglass', 'rectangle', 'inverted_triangle')),
    skin_tone_category TEXT CHECK (skin_tone_category IN ('warm', 'cool', 'neutral')),
    color_season TEXT CHECK (color_season IN ('spring', 'summer', 'autumn', 'winter')),
    detected_colors JSONB,
    best_colors JSONB,
    avoid_colors JSONB,
    shoulder_width_cm INT,
    bust_cm INT,
    waist_cm INT,
    hip_cm INT,
    inseam_cm INT,
    notes TEXT,
    vision_api_response JSONB,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_body_analysis_user ON body_analysis(user_id, created_at DESC);

-- try_on_cache
CREATE TABLE IF NOT EXISTS public.try_on_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_hash TEXT NOT NULL UNIQUE,
    result_image_url TEXT NOT NULL,
    result_storage_path TEXT,
    result_cdn_url TEXT,
    replicate_model_version TEXT,
    hit_count INT DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT now(),
    last_hit_at TIMESTAMPTZ DEFAULT now(),
    expires_at TIMESTAMPTZ DEFAULT (now() + INTERVAL '90 days')
);
CREATE INDEX IF NOT EXISTS idx_try_on_cache_hash ON try_on_cache(content_hash);
CREATE INDEX IF NOT EXISTS idx_try_on_cache_expires ON try_on_cache(expires_at);

-- try_ons
CREATE TABLE IF NOT EXISTS public.try_ons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    wardrobe_item_id UUID REFERENCES wardrobe_items(id) ON DELETE SET NULL,
    body_analysis_id UUID REFERENCES body_analysis(id) ON DELETE SET NULL,
    content_hash TEXT NOT NULL,
    cache_hit BOOLEAN DEFAULT FALSE,
    cached_from_id UUID REFERENCES try_on_cache(id),
    replicate_model_version TEXT,
    replicate_prediction_id TEXT,
    inference_time_ms INT,
    status TEXT NOT NULL CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
    result_image_url TEXT,
    result_storage_path TEXT,
    result_cdn_url TEXT,
    error_message TEXT,
    confidence_score DECIMAL(3,2),
    user_rating INT CHECK (user_rating BETWEEN 1 AND 5),
    fit_feedback TEXT CHECK (fit_feedback IN ('too_loose', 'too_tight', 'perfect', 'ok')),
    color_feedback TEXT CHECK (color_feedback IN ('clashes', 'okay', 'harmonious', 'amazing')),
    occasion_fit TEXT CHECK (occasion_fit IN ('too_casual', 'too_formal', 'just_right')),
    would_buy BOOLEAN,
    liked BOOLEAN DEFAULT FALSE,
    view_duration_seconds INT,
    shared BOOLEAN DEFAULT FALSE,
    saved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    completed_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_try_ons_user ON try_ons(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_try_ons_hash ON try_ons(content_hash);
CREATE INDEX IF NOT EXISTS idx_try_ons_status ON try_ons(status) WHERE status IN ('pending', 'processing');

-- recommendations
CREATE TABLE IF NOT EXISTS public.recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    occasion TEXT NOT NULL,
    season TEXT,
    reason TEXT,
    color_harmony_score DECIMAL(3,2),
    body_fit_score DECIMAL(3,2),
    clicked BOOLEAN DEFAULT FALSE,
    liked BOOLEAN DEFAULT FALSE,
    tried_on BOOLEAN DEFAULT FALSE,
    claude_model_version TEXT,
    prompt_version TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    feedback_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_recos_user ON recommendations(user_id, created_at DESC);

-- recommendation_items
CREATE TABLE IF NOT EXISTS public.recommendation_items (
    recommendation_id UUID REFERENCES recommendations(id) ON DELETE CASCADE,
    wardrobe_item_id UUID REFERENCES wardrobe_items(id) ON DELETE CASCADE,
    position INT,
    role TEXT CHECK (role IN ('top', 'bottom', 'shoes', 'accessory', 'outerwear')),
    PRIMARY KEY (recommendation_id, wardrobe_item_id)
);
CREATE INDEX IF NOT EXISTS idx_reco_items_item ON recommendation_items(wardrobe_item_id);

-- user_style_profile
CREATE TABLE IF NOT EXISTS public.user_style_profile (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    preferred_styles JSONB,
    preferred_colors JSONB,
    avoided_colors JSONB,
    occasion_preferences JSONB,
    favorite_brands JSONB,
    avg_price_point DECIMAL(10,2),
    budget_tier TEXT CHECK (budget_tier IN ('budget', 'mid', 'luxury')),
    trend_score DECIMAL(3,2),
    style_summary TEXT,
    calculated_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- usage_counters
CREATE TABLE IF NOT EXISTS public.usage_counters (
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    period_start DATE NOT NULL,
    try_ons_used INT DEFAULT 0,
    recommendations_used INT DEFAULT 0,
    body_analyses_used INT DEFAULT 0,
    PRIMARY KEY (user_id, period_start)
);

-- idempotency_keys
CREATE TABLE IF NOT EXISTS public.idempotency_keys (
    key TEXT PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    endpoint TEXT NOT NULL,
    request_hash TEXT,
    response_status INT,
    response_body JSONB,
    created_at TIMESTAMPTZ DEFAULT now(),
    expires_at TIMESTAMPTZ DEFAULT (now() + INTERVAL '24 hours')
);
CREATE INDEX IF NOT EXISTS idx_idempotency_expires ON idempotency_keys(expires_at);

-- audit_log
CREATE TABLE IF NOT EXISTS public.audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    resource_type TEXT,
    resource_id TEXT,
    ip_address INET,
    user_agent TEXT,
    status TEXT CHECK (status IN ('success', 'failed')),
    error_message TEXT,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_log(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_log(action, created_at DESC);

-- 3. TRIGGERS

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Use DROP TRIGGER IF EXISTS before CREATE TRIGGER for idempotency
DROP TRIGGER IF EXISTS profiles_updated_at ON profiles;
CREATE TRIGGER profiles_updated_at BEFORE UPDATE ON profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS subscriptions_updated_at ON subscriptions;
CREATE TRIGGER subscriptions_updated_at BEFORE UPDATE ON subscriptions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS wardrobe_items_updated_at ON wardrobe_items;
CREATE TRIGGER wardrobe_items_updated_at BEFORE UPDATE ON wardrobe_items FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS body_analysis_updated_at ON body_analysis;
CREATE TRIGGER body_analysis_updated_at BEFORE UPDATE ON body_analysis FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS try_ons_updated_at ON try_ons;
CREATE TRIGGER try_ons_updated_at BEFORE UPDATE ON try_ons FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS user_style_profile_updated_at ON user_style_profile;
CREATE TRIGGER user_style_profile_updated_at BEFORE UPDATE ON user_style_profile FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 4. STORED PROCEDURES

-- [L1] increment_usage: atomic counter increment for UsageCounterRepository.
-- Performs INSERT ... ON CONFLICT DO UPDATE atomically in a single transaction
-- to prevent quota bypass via concurrent requests.
--
-- Usage (PostgREST RPC):
--   POST /rest/v1/rpc/increment_usage
--   {"p_user_id": "<uuid>", "p_field": "try_ons_used", "p_amount": 1}
CREATE OR REPLACE FUNCTION increment_usage(
    p_user_id UUID,
    p_field TEXT,
    p_amount INT DEFAULT 1
)
RETURNS usage_counters
LANGUAGE plpgsql
SECURITY DEFINER  -- runs as owner (service role), bypasses RLS safely
AS $$
DECLARE
    p_period_start DATE := date_trunc('month', CURRENT_DATE)::DATE;
    v_result usage_counters;
BEGIN
    IF p_field NOT IN ('try_ons_used', 'recommendations_used', 'body_analyses_used') THEN
        RAISE EXCEPTION 'Invalid field: %. Must be one of try_ons_used, recommendations_used, body_analyses_used', p_field;
    END IF;

    INSERT INTO usage_counters (user_id, period_start, try_ons_used, recommendations_used, body_analyses_used)
    VALUES (
        p_user_id,
        p_period_start,
        CASE WHEN p_field = 'try_ons_used' THEN p_amount ELSE 0 END,
        CASE WHEN p_field = 'recommendations_used' THEN p_amount ELSE 0 END,
        CASE WHEN p_field = 'body_analyses_used' THEN p_amount ELSE 0 END
    )
    ON CONFLICT (user_id, period_start) DO UPDATE
        SET try_ons_used = CASE WHEN p_field = 'try_ons_used'
                                THEN usage_counters.try_ons_used + p_amount
                                ELSE usage_counters.try_ons_used END,
            recommendations_used = CASE WHEN p_field = 'recommendations_used'
                                        THEN usage_counters.recommendations_used + p_amount
                                        ELSE usage_counters.recommendations_used END,
            body_analyses_used = CASE WHEN p_field = 'body_analyses_used'
                                      THEN usage_counters.body_analyses_used + p_amount
                                      ELSE usage_counters.body_analyses_used END
    RETURNING * INTO v_result;

    RETURN v_result;
END;
$$;
