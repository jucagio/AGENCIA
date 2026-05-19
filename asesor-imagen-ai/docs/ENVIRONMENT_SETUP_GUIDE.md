# Environment Setup Guide — Development Workflow

**From:** Jarvis (CEO)  
**To:** Antigravity (Sprint 0.4), Sasha (Backend), Brook (Frontend)  
**Date:** 2026-05-18  
**Status:** 🟢 READY FOR DEVELOPMENT

---

## Quick Start (5 minutes)

### 1. Copy Template to .env (Local Only)
```bash
cp .env.example .env
# .env is git-ignored and stays on your machine
```

### 2. Configure Development Credentials

You have **TWO PATHS** depending on whether you're testing with real APIs or mock workers.

---

## PATH A: Development with Mock Workers (RECOMMENDED FOR SPRINT 0.4)

**Use this path if:**
- Building rate limiting, CI/CD, Docker, tests
- Don't need real Google Vision / Replicate outputs yet
- Want fast iteration without API costs

### Setup
In `.env`, keep most values as placeholders and set:

```bash
# Development mode
ENVIRONMENT=development
DEBUG=true
FEATURE_MOCK_WORKERS=true  # ← KEY: Use mock workers instead of real APIs

# Mock/dummy credentials (don't need to be real)
GOOGLE_CLOUD_VISION_API_KEY_PATH=/path/to/dummy-key.json
REPLICATE_API_TOKEN=r8_dummy_token_for_testing
ANTHROPIC_API_KEY=sk-ant-dummy_key_for_testing

# Real database (connect to Supabase dev project)
DATABASE_URL=postgresql://user:password@localhost:5432/asesor_imagen_dev
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here  # ← Ask Sasha

# Real Redis (for ARQ job queue)
REDIS_URL=redis://localhost:6379
REDIS_DB=0
```

**What happens:**
- ARQ workers will return mock responses (Vision → dummy analysis, Replicate → dummy image URL, Claude → dummy recommendations)
- Rate limiting, error handling, webhook validation all run normally
- Tests pass with 85%+ coverage
- Database operations are real (Supabase)

**When to use:** Sprint 0.4 (DevOps) + Sprint 0.5 Worker scaffolding

---

## PATH B: Development with Real APIs (WHEN JUAN CAMILO PROVIDES CREDENTIALS)

**Use this path when:**
- Testing end-to-end with real API responses
- Building visual features (Erik/Brook need actual try-on images)
- Final integration testing

### Setup
In `.env`, replace placeholder credentials:

```bash
# Real credentials from Juan Camilo
ENVIRONMENT=development
DEBUG=true
FEATURE_MOCK_WORKERS=false  # ← Real API calls

# Google Cloud Vision API (JSON service account key from GCV Console)
GOOGLE_CLOUD_VISION_API_KEY_PATH=/path/to/asesor-imagen-dev-key.json
# OR inline (not recommended for git):
# GOOGLE_CLOUD_VISION_API_KEY={"type": "service_account", "project_id": "...", ...}

# Replicate API (token from replicate.com/account)
REPLICATE_API_TOKEN=r8_your_real_replicate_token_here

# Claude API (key from console.anthropic.com)
ANTHROPIC_API_KEY=sk-ant-your_real_anthropic_key_here

# All other config same as PATH A
```

**What happens:**
- ARQ workers call real Google Vision, Replicate, Claude APIs
- Actual body analysis, try-on generation, AI recommendations
- Real API costs apply
- Slower iteration (API response times) but production-accurate

**When to use:** Sprint 0.5 (Workers integration) + Final testing

---

## Critical Environment Variables

| Variable | Type | Required | Where to Get | For Sprint 0.4 |
|----------|------|----------|--------------|---|
| `DATABASE_URL` | PostgreSQL | ✅ | Supabase project settings | Real (dev project) |
| `SUPABASE_URL` | string | ✅ | Supabase project → API settings | Real (dev project) |
| `SUPABASE_SERVICE_ROLE_KEY` | secret | ✅ | Supabase → Settings → API Keys (SERVICE ROLE) | Real (ask Sasha) |
| `JWT_SECRET` | string | ✅ | `openssl rand -hex 32` | Keep as-is (dev-secret-key-change-in-production) |
| `REDIS_URL` | URL | ✅ | Local: `redis://localhost:6379` | Real (local or Railway) |
| `STRIPE_SECRET_KEY` | secret | ⚠️ (payment only) | stripe.com/dashboard → API Keys (test/live) | Mock (`sk_test_...`) |
| `STRIPE_PUBLISHABLE_KEY` | public | ⚠️ (payment only) | stripe.com/dashboard → API Keys | Mock (`pk_test_...`) |
| `GOOGLE_CLOUD_VISION_API_KEY_PATH` | path | ✅ PATH A only | GCV Console → Service Account → Keys (JSON) | Mock path (doesn't need to exist) |
| `REPLICATE_API_TOKEN` | secret | ✅ PATH A only | replicate.com/account | Mock token (`r8_test_...`) |
| `ANTHROPIC_API_KEY` | secret | ✅ PATH A only | console.anthropic.com → API Keys | Mock key (`sk-ant-test_...`) |
| `RATE_LIMIT_ENABLED` | bool | ✅ | `true` (Sprint 0.4 focus) | `true` |
| `FEATURE_MOCK_WORKERS` | bool | ✅ | Toggle behavior | **`true`** (start here) |

---

## Step-by-Step: First Run (PATH A)

### 1. Clone + Setup
```bash
cd asesor-imagen-ai
cp .env.example .env
```

### 2. Install Python Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### 3. Verify Configuration
```bash
# Check that .env is readable (but not committed)
ls -la .env   # Should exist
git status    # Should NOT list .env (it's in .gitignore)
```

### 4. Test Database Connection
```bash
# FastAPI will validate DATABASE_URL on startup
python -m app.main  # or: uvicorn app.main:app --reload
# Look for: "Application startup complete"
```

### 5. Run Tests with Mock Workers
```bash
pytest tests/ -v --cov=app --cov-report=term-missing
# Expect: ≥85% coverage, all tests pass with mock APIs
```

---

## Switching Between Paths

### From PATH A (Mock) → PATH B (Real APIs)

When Juan Camilo provides credentials:

1. Update `.env` with real credentials:
   ```bash
   # Replace placeholders
   GOOGLE_CLOUD_VISION_API_KEY_PATH=/path/to/real-key.json
   REPLICATE_API_TOKEN=r8_real_token_from_replicate
   ANTHROPIC_API_KEY=sk-ant-real_key_from_anthropic
   ```

2. Set feature flag:
   ```bash
   FEATURE_MOCK_WORKERS=false
   ```

3. Restart server:
   ```bash
   # If running with uvicorn --reload, it auto-restarts
   # Or manually: Ctrl+C and restart
   ```

**No code changes needed.** The workers detect `FEATURE_MOCK_WORKERS` at runtime and switch behavior.

---

## Security Notes

### ⚠️ Never commit .env
```bash
# .env is already in .gitignore, but verify:
git ls-files | grep -E '^\.env$'  # Should return nothing
```

### ⚠️ Service Account Key (Google Cloud Vision)
If storing locally as JSON file:
```bash
# Store in a safe location, NOT in the repo
touch ~/.secrets/asesor-imagen-dev-key.json
chmod 600 ~/.secrets/asesor-imagen-dev-key.json  # Read-only for you

# In .env:
GOOGLE_CLOUD_VISION_API_KEY_PATH=/Users/yourname/.secrets/asesor-imagen-dev-key.json
```

Or keep JSON inline (less secure, but works for dev):
```bash
GOOGLE_CLOUD_VISION_API_KEY={"type": "service_account", ...}
```

### ⚠️ Redis Password
If using Railway or managed Redis (not localhost):
```bash
REDIS_URL=redis://:[password]@host:port/0
```

---

## Troubleshooting

### Error: `No module named 'app'`
```bash
# Make sure you're in the right directory and venv is activated
ls app/main.py  # Should exist
which python    # Should show venv/bin/python (not system python)
```

### Error: `FEATURE_MOCK_WORKERS not set`
```bash
# Set a default in .env or hardcode in app/config.py
FEATURE_MOCK_WORKERS=true
```

### Error: `Redis connection refused`
```bash
# Start Redis if using local:
redis-server  # macOS: brew install redis && redis-server
# Or use Railway Redis: update REDIS_URL in .env
```

### Error: `DATABASE_URL is invalid`
```bash
# Check format:
# postgresql://user:password@host:port/database
# Ask Sasha for the correct Supabase connection string
```

---

## Docker Workflow (Sprint 0.4)

When building Docker image, `.env` is NOT included. Use build args instead:

```dockerfile
# Dockerfile
ARG DATABASE_URL
ARG REDIS_URL
ARG FEATURE_MOCK_WORKERS

ENV DATABASE_URL=$DATABASE_URL
ENV REDIS_URL=$REDIS_URL
ENV FEATURE_MOCK_WORKERS=$FEATURE_MOCK_WORKERS
```

Build with:
```bash
docker build \
  --build-arg DATABASE_URL=postgresql://... \
  --build-arg REDIS_URL=redis://... \
  --build-arg FEATURE_MOCK_WORKERS=true \
  -t asesor-imagen:dev .
```

(Details in `docs/DOCKER_GUIDE.md` once Sprint 0.4 is underway)

---

## Summary Table

| Goal | Path | FEATURE_MOCK_WORKERS | Real Credentials? | Cost | Speed | Use Case |
|------|------|----------------------|-------------------|------|-------|----------|
| Test rate limiting, DevOps | A | `true` | ✗ (mock) | $0 | ⚡ Fast | Sprint 0.4 |
| Build worker scaffolding | A | `true` | ✗ (mock) | $0 | ⚡ Fast | Sprint 0.5 early |
| Integration testing | B | `false` | ✓ (real) | $$$ | 🐢 Slow | Sprint 0.5 final |
| Visual feature testing (Erik/Brook) | B | `false` | ✓ (real) | $$$ | 🐢 Slow | After D1-D5 |
| Production deployment | B | `false` | ✓ (real) | $$$ | 🐢 Slow | Release candidate |

---

## Next Steps

1. ✅ Antigravity: Copy `.env.example` → `.env`, set `FEATURE_MOCK_WORKERS=true`
2. ✅ Antigravity: Start with PATH A for Sprint 0.4 (rate limiting, Docker, CI/CD)
3. ⏳ Juan Camilo: Provide credentials when ready → Jarvis updates team
4. ✅ Sasha: Use real DATABASE_URL for schema/migrations (even in dev)
5. ✅ Brook: Coordinate with Sasha on real database connection for integration tests
6. ⏳ When credentials arrive: Switch to PATH B for Sprint 0.5 worker integration

---

**Status:** 🟢 READY FOR SPRINT 0.4

Questions? Ping Jarvis.

---

**Commit:** 8db4ee7  
**Versión:** 2026-05-18
