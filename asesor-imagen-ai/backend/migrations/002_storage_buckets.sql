-- =============================================================
-- Asesor de Imagen AI — Storage Buckets Setup
-- =============================================================
-- Run this SQL in Supabase Dashboard > SQL Editor
-- Creates 3 storage buckets with appropriate access policies.
--
-- IMPORTANT: Supabase storage buckets are usually created via
-- the Dashboard UI (Storage > New Bucket). This SQL provides
-- the RLS policies for the buckets once created.
--
-- Buckets to create in Dashboard (or via apply_migrations.ps1):
--   1. avatars   (public: false)
--   2. wardrobe  (public: false)
--   3. tryons    (public: true — results can be shared)
--
-- IDEMPOTENCY:
--   This migration creates buckets via INSERT ... ON CONFLICT DO NOTHING
--   and policies via DROP POLICY IF EXISTS + CREATE POLICY.
--   Safe to re-run.
-- =============================================================

-- ---------------------------------------------------------------------------
-- Buckets (idempotent — ON CONFLICT DO NOTHING)
-- ---------------------------------------------------------------------------
INSERT INTO storage.buckets (id, name, public)
VALUES ('avatars', 'avatars', false)
ON CONFLICT (id) DO NOTHING;

INSERT INTO storage.buckets (id, name, public)
VALUES ('wardrobe', 'wardrobe', false)
ON CONFLICT (id) DO NOTHING;

INSERT INTO storage.buckets (id, name, public)
VALUES ('tryons', 'tryons', true)
ON CONFLICT (id) DO NOTHING;

-- ---------------------------------------------------------------------------
-- Storage Bucket Policies
-- ---------------------------------------------------------------------------
-- Note: These policies use the storage schema.
-- Supabase auto-creates the storage.objects table.

-- AVATARS — private, user can only access own
DROP POLICY IF EXISTS "avatars_select_own" ON storage.objects;
CREATE POLICY "avatars_select_own"
    ON storage.objects FOR SELECT
    TO authenticated
    USING (bucket_id = 'avatars' AND (storage.foldername(name))[1] = auth.uid()::text);

DROP POLICY IF EXISTS "avatars_insert_own" ON storage.objects;
CREATE POLICY "avatars_insert_own"
    ON storage.objects FOR INSERT
    TO authenticated
    WITH CHECK (bucket_id = 'avatars' AND (storage.foldername(name))[1] = auth.uid()::text);

DROP POLICY IF EXISTS "avatars_update_own" ON storage.objects;
CREATE POLICY "avatars_update_own"
    ON storage.objects FOR UPDATE
    TO authenticated
    USING (bucket_id = 'avatars' AND (storage.foldername(name))[1] = auth.uid()::text);

DROP POLICY IF EXISTS "avatars_delete_own" ON storage.objects;
CREATE POLICY "avatars_delete_own"
    ON storage.objects FOR DELETE
    TO authenticated
    USING (bucket_id = 'avatars' AND (storage.foldername(name))[1] = auth.uid()::text);

-- WARDROBE — private, user can only access own
DROP POLICY IF EXISTS "wardrobe_storage_select_own" ON storage.objects;
CREATE POLICY "wardrobe_storage_select_own"
    ON storage.objects FOR SELECT
    TO authenticated
    USING (bucket_id = 'wardrobe' AND (storage.foldername(name))[1] = auth.uid()::text);

DROP POLICY IF EXISTS "wardrobe_storage_insert_own" ON storage.objects;
CREATE POLICY "wardrobe_storage_insert_own"
    ON storage.objects FOR INSERT
    TO authenticated
    WITH CHECK (bucket_id = 'wardrobe' AND (storage.foldername(name))[1] = auth.uid()::text);

DROP POLICY IF EXISTS "wardrobe_storage_update_own" ON storage.objects;
CREATE POLICY "wardrobe_storage_update_own"
    ON storage.objects FOR UPDATE
    TO authenticated
    USING (bucket_id = 'wardrobe' AND (storage.foldername(name))[1] = auth.uid()::text);

DROP POLICY IF EXISTS "wardrobe_storage_delete_own" ON storage.objects;
CREATE POLICY "wardrobe_storage_delete_own"
    ON storage.objects FOR DELETE
    TO authenticated
    USING (bucket_id = 'wardrobe' AND (storage.foldername(name))[1] = auth.uid()::text);

-- TRYONS — private by default, public read if explicitly shared, private write
-- NOTE: Uses a conditional check if we add an 'is_public' metadata flag,
-- otherwise user can only read their own. Signed URLs (TTL 1h) recommended for sharing.
DROP POLICY IF EXISTS "tryons_storage_select_own" ON storage.objects;
CREATE POLICY "tryons_storage_select_own"
    ON storage.objects FOR SELECT
    TO authenticated
    USING (bucket_id = 'tryons' AND (storage.foldername(name))[1] = auth.uid()::text);

DROP POLICY IF EXISTS "tryons_storage_insert_own" ON storage.objects;
CREATE POLICY "tryons_storage_insert_own"
    ON storage.objects FOR INSERT
    TO authenticated
    WITH CHECK (bucket_id = 'tryons' AND (storage.foldername(name))[1] = auth.uid()::text);

DROP POLICY IF EXISTS "tryons_storage_delete_own" ON storage.objects;
CREATE POLICY "tryons_storage_delete_own"
    ON storage.objects FOR DELETE
    TO authenticated
    USING (bucket_id = 'tryons' AND (storage.foldername(name))[1] = auth.uid()::text);
