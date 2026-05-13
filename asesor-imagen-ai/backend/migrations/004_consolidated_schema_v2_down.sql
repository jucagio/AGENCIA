-- =============================================================
-- Migration 004 DOWN: Rollback for Consolidated Schema V2
-- =============================================================
-- Symmetric inverse of 004_consolidated_schema_v2.sql.
-- Tables are dropped in reverse FK dependency order to avoid
-- constraint violations.
--
-- Verify symmetry:
--   1. Apply 004_consolidated_schema_v2.sql
--   2. Apply this file (004_down)
--   3. Re-apply 004_consolidated_schema_v2.sql
--   → Should succeed without errors.
--
-- WARNING: THIS DESTROYS ALL DATA. Only run in dev/CI/staging.
-- =============================================================

-- Drop stored procedures first
DROP FUNCTION IF EXISTS increment_usage(UUID, TEXT, INT);
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

-- Drop tables in reverse FK dependency order
-- (leaf tables before parent tables)
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
