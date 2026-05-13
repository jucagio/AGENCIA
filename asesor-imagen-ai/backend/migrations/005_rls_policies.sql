-- =============================================================
-- Migration 005: RLS Policies for Consolidated Schema V2
-- =============================================================
-- ARCHITECTURE NOTE:
--   service_role bypasses RLS by design (Supabase default).
--   The guard for user-scoped tables is NOT these policies alone —
--   it is app/core/admin_client.AdminClient.with_user_check() at the
--   application layer. These policies are the last line of defence
--   for direct PostgREST client access (e.g., mobile app using
--   user-scoped JWT directly against the REST API).
-- =============================================================

-- profiles
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "profiles_select" ON public.profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "profiles_insert" ON public.profiles FOR INSERT WITH CHECK (auth.uid() = id);
CREATE POLICY "profiles_update" ON public.profiles FOR UPDATE USING (auth.uid() = id) WITH CHECK (auth.uid() = id);
CREATE POLICY "profiles_delete" ON public.profiles FOR DELETE USING (auth.uid() = id);

-- subscriptions
ALTER TABLE public.subscriptions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "subscriptions_select" ON public.subscriptions FOR SELECT USING (auth.uid() = user_id);
-- Insert/Update/Delete solo por service_role (bypasses RLS automatically, no need to create policies)

-- wardrobe_items
ALTER TABLE public.wardrobe_items ENABLE ROW LEVEL SECURITY;
CREATE POLICY "wardrobe_items_select" ON public.wardrobe_items FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "wardrobe_items_insert" ON public.wardrobe_items FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "wardrobe_items_update" ON public.wardrobe_items FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "wardrobe_items_delete" ON public.wardrobe_items FOR DELETE USING (auth.uid() = user_id);

-- body_analysis
ALTER TABLE public.body_analysis ENABLE ROW LEVEL SECURITY;
CREATE POLICY "body_analysis_select" ON public.body_analysis FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "body_analysis_insert" ON public.body_analysis FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "body_analysis_update" ON public.body_analysis FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "body_analysis_delete" ON public.body_analysis FOR DELETE USING (auth.uid() = user_id);

-- try_ons
ALTER TABLE public.try_ons ENABLE ROW LEVEL SECURITY;
CREATE POLICY "try_ons_select" ON public.try_ons FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "try_ons_insert" ON public.try_ons FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "try_ons_update" ON public.try_ons FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "try_ons_delete" ON public.try_ons FOR DELETE USING (auth.uid() = user_id);

-- recommendations
ALTER TABLE public.recommendations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "recommendations_select" ON public.recommendations FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "recommendations_insert" ON public.recommendations FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "recommendations_update" ON public.recommendations FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "recommendations_delete" ON public.recommendations FOR DELETE USING (auth.uid() = user_id);

-- recommendation_items
ALTER TABLE public.recommendation_items ENABLE ROW LEVEL SECURITY;
CREATE POLICY "recommendation_items_select" ON public.recommendation_items FOR SELECT
USING (EXISTS (SELECT 1 FROM public.recommendations r WHERE r.id = recommendation_id AND r.user_id = auth.uid()));
CREATE POLICY "recommendation_items_insert" ON public.recommendation_items FOR INSERT
WITH CHECK (EXISTS (SELECT 1 FROM public.recommendations r WHERE r.id = recommendation_id AND r.user_id = auth.uid()));
CREATE POLICY "recommendation_items_update" ON public.recommendation_items FOR UPDATE
USING (EXISTS (SELECT 1 FROM public.recommendations r WHERE r.id = recommendation_id AND r.user_id = auth.uid()))
WITH CHECK (EXISTS (SELECT 1 FROM public.recommendations r WHERE r.id = recommendation_id AND r.user_id = auth.uid()));
CREATE POLICY "recommendation_items_delete" ON public.recommendation_items FOR DELETE
USING (EXISTS (SELECT 1 FROM public.recommendations r WHERE r.id = recommendation_id AND r.user_id = auth.uid()));

-- user_style_profile
ALTER TABLE public.user_style_profile ENABLE ROW LEVEL SECURITY;
CREATE POLICY "user_style_profile_select" ON public.user_style_profile FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "user_style_profile_insert" ON public.user_style_profile FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "user_style_profile_update" ON public.user_style_profile FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "user_style_profile_delete" ON public.user_style_profile FOR DELETE USING (auth.uid() = user_id);

-- usage_counters
-- [M6] Users may only SELECT their own counters. INSERT / UPDATE / DELETE are
-- restricted to service_role (ARQ worker via increment_usage() stored proc).
-- This prevents users from zeroing or bypassing their quota limits.
ALTER TABLE public.usage_counters ENABLE ROW LEVEL SECURITY;
CREATE POLICY "usage_counters_select" ON public.usage_counters FOR SELECT USING (auth.uid() = user_id);
-- No INSERT/UPDATE/DELETE policies — only service_role (via increment_usage RPC) writes here.

-- audit_log
-- [M4] audit_log is INSERT-only by service_role. No user policy is needed or safe:
-- allowing auth.uid() IS NULL would permit unauthenticated writes, which is
-- exploitable for log pollution and denial-of-service on the audit trail.
ALTER TABLE public.audit_log ENABLE ROW LEVEL SECURITY;
-- No policies defined: only service_role (which bypasses RLS) may write to audit_log.

-- idempotency_keys
ALTER TABLE public.idempotency_keys ENABLE ROW LEVEL SECURITY;
-- Solo service_role

-- try_on_cache
ALTER TABLE public.try_on_cache ENABLE ROW LEVEL SECURITY;
-- Solo service_role
