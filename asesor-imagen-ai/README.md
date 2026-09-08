# Asesor de Imagen AI

**Asesor de Imagen AI** — asistente de moda con IA que analiza el cuerpo del usuario, prueba outfits virtualmente y recomienda vestuario personalizado.

**Status:** 🔨 Sprint 0 (Infrastructure)

## Project Overview

- **MVP Duration:** 14 weeks
- **Team:** Sasha (Backend), Brook (Frontend), Erik (Design)
- **Launch Target:** Week 14 (50K users)
- **Financials:** $24K/month profit @ 50K users

## Stack

| Layer | Tech | Version |
|-------|------|---------|
| Backend | FastAPI | 0.104+ |
| Database | Supabase/PostgreSQL | Latest |
| Frontend | Flutter | 3.41+ |
| Auth | JWT HS256 | - |
| Vision | Google Vision API | - |
| Try-On | Replicate | - |
| Recommendations | Claude (Anthropic) | - |
| Payments | Stripe + Mercado Pago | - |
| Infra | Railway + Supabase | - |

## Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Fill with credentials
uvicorn app.main:app --reload
```

### Database

Credentials needed:
- Supabase URL
- Supabase Key
- Google Vision API (JSON)
- Replicate API token
- Anthropic API key
- Stripe keys (test)
- Mercado Pago token

## Sprint 0 Checklist

- [ ] Week 1: Infrastructure (Sasha)
  - [ ] Supabase schema + RLS
  - [ ] FastAPI scaffold
  - [ ] Docker + Railway
  - [ ] CI/CD pipeline

## Documentation

- `ASESOR_IMAGEN_AI_RESUMEN_EJECUTIVO.md` - Overview & viability
- `ASESOR_IMAGEN_AI_ARQUITECTURA.md` - Technical architecture
- `ASESOR_IMAGEN_AI_SCHEMAS_Y_SERVICIOS.md` - Code templates
- `ASESOR_IMAGEN_AI_CHECKLIST_EJECUCION.md` - Execution plan

## MVP Deployment (Sprint 0.5)

### Backend — Local

```bash
cd asesor-imagen-ai/backend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # fill in SUPABASE_*, REDIS_URL, AI keys
uvicorn app.main:app --reload
```

Smoke check: `curl http://127.0.0.1:8000/health` → `{"success": true, "data": {"status":"ok",...}}`

### Backend — Railway Deploy

`railway.toml` and `backend/Dockerfile` are committed. To deploy:

```bash
railway login
railway link            # link to project (interactive)
railway up              # builds Dockerfile + deploys
```

Required env vars in Railway dashboard:
- `ENVIRONMENT=production`
- `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`
- `SUPABASE_AVATARS_BUCKET=avatars`, `SUPABASE_WARDROBE_BUCKET=wardrobe`, `SUPABASE_TRYONS_BUCKET=tryons`
- `REDIS_URL` (Upstash recommended, TLS: `rediss://...`)
- `ALLOWED_ORIGINS` (no wildcards in prod)
- `SECRET_KEY` (≥ 32 chars, NOT the dev placeholder)
- `REPLICATE_API_TOKEN`, `ANTHROPIC_API_KEY`, `GOOGLE_CLOUD_VISION_API_KEY`

### Migrations

Apply M007 (Option F: FSM + cache tier) and M008 (RLS tighten on `try_ons`) to Supabase staging:

```bash
npx supabase link --project-ref <YOUR_PROJECT_REF>
npx supabase db push --linked
```

Smoke SQL to verify (run in Supabase SQL editor):

```sql
-- M007: FSM columns
SELECT column_name FROM information_schema.columns
WHERE table_name='try_ons' AND column_name IN ('fsm_state','fashn_mode','cache_tier');
-- expect 3 rows

-- M008: service-role-only UPDATE policy
SELECT policyname FROM pg_policies
WHERE tablename='try_ons' AND policyname LIKE '%service_role%';
-- expect ≥ 1 row

-- M007: per-tier usage counters
SELECT column_name FROM information_schema.columns
WHERE table_name='usage_counters' AND column_name IN ('try_ons_base_used','try_ons_std_used','try_ons_pro_used');
-- expect 3 rows
```

### Frontend (APK)

Demo APK is in `asesor-imagen-ai/frontend/build/app/outputs/flutter-apk/app-release.apk`.
Demo credentials: `demo@example.com` / `demo123` (only valid once Supabase has a seeded `demo@example.com` user).

To repoint Flutter at the deployed backend:
1. Wait for Railway URL (e.g. `https://asesor-imagen-xxx.up.railway.app`).
2. Edit `frontend/.env` → set `API_BASE_URL`.
3. Rebuild APK: `flutter build apk --release`.

## Team

- **Sasha** - Backend/Security (FastAPI, PostgreSQL, APIs)
- **Brook** - Frontend (Flutter, Dart)
- **Erik** - Design (UI/UX, Figma)
- **Jarvis** - Architecture & Ops

## License

Internal - Agencia de Agentes Claude
