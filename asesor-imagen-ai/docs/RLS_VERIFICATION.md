# RLS Verification — Sprint 0.5 T5

Owner: Sasha. Last verified against migration `005_rls_policies.sql` + `007_optionf_fsm_cache_tier.sql`.

## Policies that must exist

| Table | Policy | USING expression |
|-------|--------|------------------|
| `try_ons` | try_ons_select | `auth.uid() = user_id` |
| `try_ons` | try_ons_insert | `auth.uid() = user_id` (WITH CHECK) |
| `try_ons` | try_ons_update | `auth.uid() = user_id` (USING + WITH CHECK) |
| `try_ons` | try_ons_delete | `auth.uid() = user_id` |
| `usage_counters` | usage_counters_select | `auth.uid() = user_id` |
| `wardrobe_items` | wardrobe_items_* | `auth.uid() = user_id` (all 4 verbs) |
| `body_analysis` | body_analysis_* | `auth.uid() = user_id` (all 4 verbs) |

`usage_counters` deliberately has NO insert/update/delete policy — only the service-role RPC `increment_usage` writes there, which is the correct least-privilege model.

## Verification steps (run on staging before release)

### 1. Confirm policies are present (as service_role)

```sql
SELECT schemaname, tablename, policyname, cmd
FROM pg_policies
WHERE schemaname = 'public'
  AND tablename IN ('try_ons', 'usage_counters', 'wardrobe_items', 'body_analysis')
ORDER BY tablename, policyname;
```

Or use the helper added in 007:

```sql
SELECT * FROM public.verify_rls_policies();
```

Expected: at least 13 rows (4 verbs × 3 user-scoped tables + 1 select on usage_counters).

### 2. Confirm cross-tenant isolation (as a real user JWT)

Open the Supabase SQL editor with a user JWT (or use the REST API with the user's anon token):

```sql
-- Substitute <USER_A_UUID> with a known seeded user.
SET LOCAL "request.jwt.claims" = '{"sub":"<USER_A_UUID>","role":"authenticated"}';

SELECT COUNT(*) FROM public.try_ons         WHERE user_id != '<USER_A_UUID>'::uuid;
SELECT COUNT(*) FROM public.usage_counters  WHERE user_id != '<USER_A_UUID>'::uuid;
SELECT COUNT(*) FROM public.wardrobe_items  WHERE user_id != '<USER_A_UUID>'::uuid;
SELECT COUNT(*) FROM public.body_analysis   WHERE user_id != '<USER_A_UUID>'::uuid;
```

Expected: every query returns 0. If any returns > 0, RLS is broken — block release and page Sasha.

### 3. Confirm INSERT is rejected for cross-tenant writes

```sql
SET LOCAL "request.jwt.claims" = '{"sub":"<USER_A_UUID>","role":"authenticated"}';

INSERT INTO public.try_ons (user_id, content_hash, status)
VALUES ('<USER_B_UUID>'::uuid, 'test', 'pending');
-- Expected: ERROR — new row violates row-level security policy.
```

### 4. Confirm service-role bypass still works (admin context only)

```sql
-- As service_role:
SELECT COUNT(*) FROM public.try_ons;  -- should return total across all users
```

This is the path used by workers via `admin.trusted()`.

## Automated test

`tests/test_rls_enforcement.py` covers the application-layer guard (`AdminClient.with_user_check`) which is the FIRST line of defense. RLS is the SECOND line. Both must hold.
