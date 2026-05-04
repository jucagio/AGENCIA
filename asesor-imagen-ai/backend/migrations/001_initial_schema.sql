-- =============================================================
-- Asesor de Imagen AI — Initial Database Schema
-- =============================================================
-- Run this SQL in Supabase Dashboard > SQL Editor
-- This creates all tables, RLS policies, and indexes.
-- =============================================================

-- ---------------------------------------------------------------------------
-- 1. TABLES
-- ---------------------------------------------------------------------------

-- Users table
CREATE TABLE public.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    avatar_url TEXT,
    google_oauth_id TEXT UNIQUE,
    subscription_tier TEXT DEFAULT 'free'
        CHECK (subscription_tier IN ('free', 'premium_monthly', 'premium_annual')),
    subscription_status TEXT DEFAULT 'active'
        CHECK (subscription_status IN ('active', 'cancelled', 'past_due')),
    subscription_id TEXT,
    body_shape TEXT
        CHECK (body_shape IS NULL OR body_shape IN ('pear', 'apple', 'hourglass', 'rectangle', 'inverted_triangle')),
    skin_tone TEXT
        CHECK (skin_tone IS NULL OR skin_tone IN ('fair', 'light', 'medium', 'olive', 'tan', 'dark')),
    color_preferences TEXT[],
    budget_range TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Body analysis results
CREATE TABLE public.body_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    height_cm INT,
    weight_kg INT,
    measurements JSONB,
    body_landmarks JSONB,
    color_analysis JSONB,
    style_notes TEXT,
    image_url TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Wardrobe items
CREATE TABLE public.wardrobe_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category TEXT NOT NULL
        CHECK (category IN ('shirt', 'pants', 'dress', 'jacket', 'shoes', 'accessories', 'skirt', 'coat')),
    sub_category TEXT,
    color TEXT NOT NULL,
    size TEXT
        CHECK (size IS NULL OR size IN ('XS', 'S', 'M', 'L', 'XL', 'XXL')),
    brand TEXT,
    price DECIMAL(10, 2),
    purchase_date DATE,
    condition TEXT DEFAULT 'good'
        CHECK (condition IN ('excellent', 'good', 'fair', 'worn')),
    image_url TEXT,
    image_features JSONB,
    is_favorite BOOLEAN DEFAULT false,
    is_archived BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Saved outfits
CREATE TABLE public.outfits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name TEXT,
    occasion TEXT
        CHECK (occasion IS NULL OR occasion IN ('casual', 'work', 'date', 'party', 'outdoor')),
    season TEXT
        CHECK (season IS NULL OR season IN ('spring', 'summer', 'fall', 'winter')),
    description TEXT,
    items JSONB,
    created_outfit_image_url TEXT,
    likes INT DEFAULT 0,
    rating DECIMAL(3, 2),
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Virtual try-on results
CREATE TABLE public.tryons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    wardrobe_item_id UUID REFERENCES wardrobe_items(id),
    outfit_id UUID REFERENCES outfits(id),
    body_image_url TEXT,
    item_image_url TEXT,
    result_image_url TEXT,
    model_used TEXT,
    status TEXT DEFAULT 'pending'
        CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- AI Recommendations
CREATE TABLE public.recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    query TEXT NOT NULL,
    occasion TEXT,
    suggestions JSONB NOT NULL DEFAULT '[]'::jsonb,
    model_used TEXT DEFAULT 'claude',
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Subscriptions history
CREATE TABLE public.subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    provider TEXT NOT NULL
        CHECK (provider IN ('stripe', 'mercadopago')),
    provider_subscription_id TEXT UNIQUE NOT NULL,
    plan TEXT NOT NULL
        CHECK (plan IN ('premium_monthly', 'premium_annual')),
    status TEXT DEFAULT 'active'
        CHECK (status IN ('active', 'cancelled', 'past_due', 'trialing')),
    current_period_start TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ,
    cancel_at_period_end BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- User analytics events
CREATE TABLE public.analytics_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    event_type TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);


-- ---------------------------------------------------------------------------
-- 2. ROW LEVEL SECURITY (RLS)
-- ---------------------------------------------------------------------------

-- Users
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "users_select_own"
    ON users FOR SELECT
    TO authenticated
    USING (id = auth.uid());

CREATE POLICY "users_update_own"
    ON users FOR UPDATE
    TO authenticated
    USING (id = auth.uid())
    WITH CHECK (id = auth.uid());

-- Body Analysis
ALTER TABLE public.body_analysis ENABLE ROW LEVEL SECURITY;

CREATE POLICY "body_analysis_select_own"
    ON body_analysis FOR SELECT
    TO authenticated
    USING (user_id = auth.uid());

CREATE POLICY "body_analysis_insert_own"
    ON body_analysis FOR INSERT
    TO authenticated
    WITH CHECK (user_id = auth.uid());

-- Wardrobe Items
ALTER TABLE public.wardrobe_items ENABLE ROW LEVEL SECURITY;

CREATE POLICY "wardrobe_select_own"
    ON wardrobe_items FOR SELECT
    TO authenticated
    USING (user_id = auth.uid());

CREATE POLICY "wardrobe_insert_own"
    ON wardrobe_items FOR INSERT
    TO authenticated
    WITH CHECK (user_id = auth.uid());

CREATE POLICY "wardrobe_update_own"
    ON wardrobe_items FOR UPDATE
    TO authenticated
    USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

CREATE POLICY "wardrobe_delete_own"
    ON wardrobe_items FOR DELETE
    TO authenticated
    USING (user_id = auth.uid());

-- Outfits
ALTER TABLE public.outfits ENABLE ROW LEVEL SECURITY;

CREATE POLICY "outfits_select_own"
    ON outfits FOR SELECT
    TO authenticated
    USING (user_id = auth.uid());

CREATE POLICY "outfits_insert_own"
    ON outfits FOR INSERT
    TO authenticated
    WITH CHECK (user_id = auth.uid());

CREATE POLICY "outfits_update_own"
    ON outfits FOR UPDATE
    TO authenticated
    USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

CREATE POLICY "outfits_delete_own"
    ON outfits FOR DELETE
    TO authenticated
    USING (user_id = auth.uid());

-- Try-ons
ALTER TABLE public.tryons ENABLE ROW LEVEL SECURITY;

CREATE POLICY "tryons_select_own"
    ON tryons FOR SELECT
    TO authenticated
    USING (user_id = auth.uid());

CREATE POLICY "tryons_insert_own"
    ON tryons FOR INSERT
    TO authenticated
    WITH CHECK (user_id = auth.uid());

-- Recommendations
ALTER TABLE public.recommendations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "recommendations_select_own"
    ON recommendations FOR SELECT
    TO authenticated
    USING (user_id = auth.uid());

CREATE POLICY "recommendations_insert_own"
    ON recommendations FOR INSERT
    TO authenticated
    WITH CHECK (user_id = auth.uid());

-- Subscriptions
ALTER TABLE public.subscriptions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "subscriptions_select_own"
    ON subscriptions FOR SELECT
    TO authenticated
    USING (user_id = auth.uid());

-- Analytics Events (insert only, no read from client)
ALTER TABLE public.analytics_events ENABLE ROW LEVEL SECURITY;

CREATE POLICY "analytics_insert_own"
    ON analytics_events FOR INSERT
    TO authenticated
    WITH CHECK (user_id = auth.uid());


-- ---------------------------------------------------------------------------
-- 3. INDEXES
-- ---------------------------------------------------------------------------

CREATE INDEX idx_wardrobe_user_id ON wardrobe_items(user_id);
CREATE INDEX idx_wardrobe_category ON wardrobe_items(category);
CREATE INDEX idx_wardrobe_user_category ON wardrobe_items(user_id, category);
CREATE INDEX idx_outfits_user_id ON outfits(user_id);
CREATE INDEX idx_tryons_user_id ON tryons(user_id);
CREATE INDEX idx_body_analysis_user_id ON body_analysis(user_id);
CREATE INDEX idx_recommendations_user_id ON recommendations(user_id);
CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_analytics_user_created ON analytics_events(user_id, created_at DESC);


-- ---------------------------------------------------------------------------
-- 4. UPDATED_AT TRIGGER
-- ---------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER wardrobe_items_updated_at
    BEFORE UPDATE ON wardrobe_items
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER subscriptions_updated_at
    BEFORE UPDATE ON subscriptions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
