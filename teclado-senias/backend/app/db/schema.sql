-- ==========================================================================
-- Teclado de Senas -- Supabase database schema
-- ==========================================================================
-- Run this in the Supabase SQL Editor (Dashboard > SQL Editor > New query)
--
-- Tables:
--   user_profiles  -- extends auth.users with display info
--   signs          -- sign language signs catalog
--   videos         -- multiple video files per sign
--   translations   -- user translation history for analytics
--   favorites      -- user bookmarked signs
--
-- Security:
--   - RLS enabled on ALL tables
--   - Users can only read/write their own data
--   - Signs and videos are publicly readable
--   - Service role bypasses RLS for admin operations
-- ==========================================================================

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ==========================================================================
-- 1. USER PROFILES
-- ==========================================================================

CREATE TABLE IF NOT EXISTS public.user_profiles (
    id              UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    display_name    TEXT NOT NULL DEFAULT '',
    avatar_url      TEXT,
    preferred_language TEXT NOT NULL DEFAULT 'co-csn',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.user_profiles IS 'Extended user profile data. One row per auth.users entry.';
COMMENT ON COLUMN public.user_profiles.preferred_language IS 'ISO code for preferred sign language variant. Default: Colombian Sign Language.';

ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;

-- Users can read their own profile
CREATE POLICY "Users can read own profile"
    ON public.user_profiles
    FOR SELECT
    USING (auth.uid() = id);

-- Users can update their own profile
CREATE POLICY "Users can update own profile"
    ON public.user_profiles
    FOR UPDATE
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);

-- Service role can insert profiles during registration
CREATE POLICY "Service role can insert profiles"
    ON public.user_profiles
    FOR INSERT
    WITH CHECK (true);

-- Auto-update updated_at on changes
CREATE OR REPLACE FUNCTION public.update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER user_profiles_updated_at
    BEFORE UPDATE ON public.user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at();


-- ==========================================================================
-- 2. SIGNS
-- ==========================================================================

CREATE TABLE IF NOT EXISTS public.signs (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    word            TEXT NOT NULL,
    language_code   TEXT NOT NULL DEFAULT 'co-csn',
    video_url       TEXT NOT NULL,
    description     TEXT,
    difficulty      TEXT NOT NULL DEFAULT 'beginner'
                    CHECK (difficulty IN ('beginner', 'intermediate', 'advanced')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.signs IS 'Catalog of sign language signs with primary video URL.';
COMMENT ON COLUMN public.signs.word IS 'The word this sign represents, stored lowercase.';
COMMENT ON COLUMN public.signs.language_code IS 'Sign language variant code (e.g., co-csn for Colombian).';

-- Index for fast search by word
CREATE INDEX IF NOT EXISTS idx_signs_word ON public.signs (word);
CREATE INDEX IF NOT EXISTS idx_signs_language_code ON public.signs (language_code);
-- Composite unique: one sign per word per language
CREATE UNIQUE INDEX IF NOT EXISTS idx_signs_word_language
    ON public.signs (lower(word), language_code);

ALTER TABLE public.signs ENABLE ROW LEVEL SECURITY;

-- Signs are publicly readable (no auth required)
CREATE POLICY "Signs are publicly readable"
    ON public.signs
    FOR SELECT
    USING (true);

-- Only admins (service role) can insert/update/delete signs
-- Service role bypasses RLS, so no explicit policy needed for writes

-- Trigger for updated_at
CREATE TRIGGER signs_updated_at
    BEFORE UPDATE ON public.signs
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at();


-- ==========================================================================
-- 3. VIDEOS
-- ==========================================================================

CREATE TABLE IF NOT EXISTS public.videos (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sign_id         UUID NOT NULL REFERENCES public.signs(id) ON DELETE CASCADE,
    url             TEXT NOT NULL,
    duration_seconds NUMERIC(6,2),
    format          TEXT NOT NULL DEFAULT 'mp4'
                    CHECK (format IN ('mp4', 'webm', 'gif')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.videos IS 'Multiple video files per sign (different formats, angles, speeds).';

CREATE INDEX IF NOT EXISTS idx_videos_sign_id ON public.videos (sign_id);

ALTER TABLE public.videos ENABLE ROW LEVEL SECURITY;

-- Videos are publicly readable
CREATE POLICY "Videos are publicly readable"
    ON public.videos
    FOR SELECT
    USING (true);

-- Writes via service role only (bypasses RLS)


-- ==========================================================================
-- 4. TRANSLATIONS
-- ==========================================================================

CREATE TABLE IF NOT EXISTS public.translations (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    input_text      TEXT NOT NULL,
    signs_matched   TEXT[] NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.translations IS 'Log of user translation requests for analytics.';
COMMENT ON COLUMN public.translations.signs_matched IS 'Array of sign IDs that matched the input text.';

CREATE INDEX IF NOT EXISTS idx_translations_user_id ON public.translations (user_id);
CREATE INDEX IF NOT EXISTS idx_translations_created_at ON public.translations (created_at);

ALTER TABLE public.translations ENABLE ROW LEVEL SECURITY;

-- Users can read their own translations
CREATE POLICY "Users can read own translations"
    ON public.translations
    FOR SELECT
    USING (auth.uid() = user_id);

-- Users can insert their own translations
CREATE POLICY "Users can insert own translations"
    ON public.translations
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);


-- ==========================================================================
-- 5. FAVORITES
-- ==========================================================================

CREATE TABLE IF NOT EXISTS public.favorites (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    sign_id         UUID NOT NULL REFERENCES public.signs(id) ON DELETE CASCADE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.favorites IS 'User-bookmarked signs for quick access.';

-- Each user can favorite a sign only once
CREATE UNIQUE INDEX IF NOT EXISTS idx_favorites_user_sign
    ON public.favorites (user_id, sign_id);

CREATE INDEX IF NOT EXISTS idx_favorites_user_id ON public.favorites (user_id);

ALTER TABLE public.favorites ENABLE ROW LEVEL SECURITY;

-- Users can read their own favorites
CREATE POLICY "Users can read own favorites"
    ON public.favorites
    FOR SELECT
    USING (auth.uid() = user_id);

-- Users can add their own favorites
CREATE POLICY "Users can insert own favorites"
    ON public.favorites
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Users can remove their own favorites
CREATE POLICY "Users can delete own favorites"
    ON public.favorites
    FOR DELETE
    USING (auth.uid() = user_id);


-- ==========================================================================
-- SEED DATA (development only)
-- ==========================================================================
-- Uncomment the block below to insert sample signs for testing.

/*
INSERT INTO public.signs (word, language_code, video_url, description, difficulty) VALUES
    ('hola', 'co-csn', 'https://storage.example.com/signs/hola.mp4', 'Saludo informal', 'beginner'),
    ('gracias', 'co-csn', 'https://storage.example.com/signs/gracias.mp4', 'Expresion de agradecimiento', 'beginner'),
    ('por favor', 'co-csn', 'https://storage.example.com/signs/por-favor.mp4', 'Solicitud educada', 'beginner'),
    ('si', 'co-csn', 'https://storage.example.com/signs/si.mp4', 'Afirmacion', 'beginner'),
    ('no', 'co-csn', 'https://storage.example.com/signs/no.mp4', 'Negacion', 'beginner'),
    ('buenos dias', 'co-csn', 'https://storage.example.com/signs/buenos-dias.mp4', 'Saludo matutino', 'beginner'),
    ('buenas noches', 'co-csn', 'https://storage.example.com/signs/buenas-noches.mp4', 'Saludo nocturno', 'beginner'),
    ('como estas', 'co-csn', 'https://storage.example.com/signs/como-estas.mp4', 'Pregunta de bienestar', 'beginner'),
    ('ayuda', 'co-csn', 'https://storage.example.com/signs/ayuda.mp4', 'Solicitar asistencia', 'beginner'),
    ('agua', 'co-csn', 'https://storage.example.com/signs/agua.mp4', 'Sustantivo: agua', 'beginner'),
    ('familia', 'co-csn', 'https://storage.example.com/signs/familia.mp4', 'Sustantivo: familia', 'intermediate'),
    ('trabajo', 'co-csn', 'https://storage.example.com/signs/trabajo.mp4', 'Sustantivo: trabajo', 'intermediate'),
    ('escuela', 'co-csn', 'https://storage.example.com/signs/escuela.mp4', 'Sustantivo: escuela', 'intermediate'),
    ('doctor', 'co-csn', 'https://storage.example.com/signs/doctor.mp4', 'Sustantivo: doctor', 'intermediate'),
    ('emergencia', 'co-csn', 'https://storage.example.com/signs/emergencia.mp4', 'Situacion de emergencia', 'advanced')
ON CONFLICT DO NOTHING;
*/
