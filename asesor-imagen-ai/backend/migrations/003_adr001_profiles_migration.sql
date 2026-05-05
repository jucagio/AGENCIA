-- =============================================================
-- Migration 003: ADR-001 Compliance (Supabase Auth)
-- =============================================================
-- This migration transitions the legacy 'users' table into a
-- 'profiles' table that extends Supabase's native auth.users.
-- =============================================================

-- 1. Rename table from users to profiles
ALTER TABLE public.users RENAME TO profiles;

-- 2. Remove legacy authentication columns (handled by Supabase Auth now)
ALTER TABLE public.profiles 
    DROP COLUMN hashed_password,
    DROP COLUMN google_oauth_id;

-- 3. Modify ID column to link directly to auth.users
-- Drop the default UUID generation since the ID will come from auth.users on signup
ALTER TABLE public.profiles ALTER COLUMN id DROP DEFAULT;

-- Add foreign key constraint to Supabase auth.users
ALTER TABLE public.profiles 
    ADD CONSTRAINT fk_profiles_auth_users 
    FOREIGN KEY (id) 
    REFERENCES auth.users(id) 
    ON DELETE CASCADE;

-- 4. Rename RLS policies for clarity
ALTER POLICY "users_select_own" ON public.profiles RENAME TO "profiles_select_own";
ALTER POLICY "users_update_own" ON public.profiles RENAME TO "profiles_update_own";

-- 5. Rename updated_at trigger
ALTER TRIGGER users_updated_at ON public.profiles RENAME TO profiles_updated_at;

-- NOTE: Foreign key constraints on child tables (wardrobe_items, body_analysis, etc.)
-- that referenced public.users(id) are automatically updated by PostgreSQL 
-- to reference public.profiles(id) when the table is renamed.
