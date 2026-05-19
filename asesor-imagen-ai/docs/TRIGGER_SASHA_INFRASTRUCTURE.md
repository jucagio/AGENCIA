# 🔌 TRIGGER SASHA — Infrastructure Prep & Worker Scaffolding

**From:** Jarvis (CEO)  
**To:** Sasha (Backend Senior)  
**Date:** 2026-05-18 (SAB)  
**Priority:** 🔴 CRITICAL  
**Timeline:** 3 days (MAR-MIÉ 18-20)  
**Blocker:** Antigravity Sprint 0.4 (rate limiting) — can prep meanwhile

---

## Mission

While Antigravity handles Sprint 0.4 DevOps (delayed), you prepare the infrastructure foundation for Sprint 0.5 workers. **Zero code changes to existing endpoints. Pure infrastructure + scaffolding.**

---

## T1: Create Supabase `/try-ons/` Storage Bucket (TODAY)

**Owner:** Sasha  
**Duration:** 30 min  
**Blocker:** None  

### Instructions

1. **Go to:** Supabase dashboard (ask Juan Camilo for URL)
2. **Navigate:** Storage → Buckets
3. **Create bucket:**
   - Name: `try-ons`
   - Public: No (private, access via signed URLs)
   - File size limit: 100 MB (try-on images)
4. **Create folder structure:**
   ```
   try-ons/
   ├── 2026-05/
   │   └── user_id/
   │       └── job_id.png (or .jpg)
   └── 2026-06/
       └── ...
   ```
5. **Test signed URL generation:**
   ```python
   # Quick test script
   from supabase import create_client
   url = supabase.storage.from_("try-ons").get_signed_url(
       "test/image.png", expires_in=86400
   )
   print(url)  # Should return 24h signed URL
   ```
6. **Document:**
   - SUPABASE_BUCKET_NAME = "try-ons"
   - STORAGE_SIGNED_URL_EXPIRY_HOURS = 24
   - Update `.env` for team

**Definition of Done:**
- [ ] Bucket created and tested
- [ ] Signed URLs working (24h expiry)
- [ ] Folder structure documented
- [ ] Team knows bucket name + access pattern

---

## T2: ARQ Worker Pool Real Setup (Days 1-2)

**Owner:** Sasha + Antigravity (once available)  
**Duration:** 4 hours (can start immediately, full integration waits for Sprint 0.4)  
**Blocker:** Antigravity rate limiting (defer full integration)  

### Instructions

**Create `app/core/queue.py`:**

```python
from arq import create_pool, ArqRedis
from arq.connections import RedisSettings
from typing import Optional
import os

# ARQ Redis settings
REDIS_SETTINGS = RedisSettings(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    database=int(os.getenv("REDIS_DB", 0)),
)

async def create_arq_pool() -> ArqRedis:
    """Create real ARQ pool for job queue."""
    return await create_pool(REDIS_SETTINGS)

async def get_arq_pool(request) -> ArqRedis:
    """Dependency for injecting ARQ pool into FastAPI."""
    return request.app.state.arq_pool

class ArqPoolDep:
    """Dependency class for ARQ pool."""
    pass
```

**Update `app/main.py` lifespan:**

```python
from contextlib import asynccontextmanager
from app.core.queue import create_arq_pool

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.arq_pool = await create_arq_pool()
    app.state.db = get_db_session()
    print("✅ ARQ pool initialized")
    
    yield
    
    # Shutdown
    await app.state.arq_pool.close()
    print("🛑 ARQ pool closed")

app = FastAPI(lifespan=lifespan)
```

**Create `app/workers/base.py`:**

```python
from arq import func
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

@func
async def vision_worker(
    image_url: str,
    user_id: str,
    job_id: str,
) -> Dict[str, Any]:
    """
    Vision API worker (T1, Sprint 0.5).
    Currently stub — returns mock response.
    Will integrate Google Cloud Vision API when credentials arrive.
    """
    return {
        "status": "completed",
        "job_id": job_id,
        "user_id": user_id,
        "body_analysis": {
            "body_type": "pear",
            "skin_tone": "warm",
            "color_season": "autumn",
            "best_colors": ["rust", "gold", "olive"],
            "avoid_colors": ["cool_pink", "bright_blue"],
        },
        "cached": False,
    }

@func
async def replicate_worker(
    person_image_url: str,
    garment_image_urls: list[str],
    user_id: str,
    job_id: str,
) -> Dict[str, Any]:
    """
    Replicate API worker (T2, Sprint 0.5).
    Currently stub — returns mock response.
    Will integrate Replicate API when credentials arrive.
    """
    return {
        "status": "completed",
        "job_id": job_id,
        "user_id": user_id,
        "result_image_url": "https://supabase.../try-ons/.../result.png",
        "ai_insight": "This rust-colored sweater complements your warm skin tone and brings out your eyes.",
        "cached": False,
    }

@func
async def claude_worker(
    body_analysis: Dict[str, Any],
    wardrobe_items: list[Dict[str, Any]],
    user_id: str,
    job_id: str,
) -> Dict[str, Any]:
    """
    Claude API worker (T3, Sprint 0.5).
    Currently stub — returns mock response.
    Will integrate Claude API when credentials arrive.
    """
    return {
        "status": "completed",
        "job_id": job_id,
        "user_id": user_id,
        "recommendations": [
            {
                "outfit_id": "rec_001",
                "items": ["item_1", "item_2", "item_3"],
                "why_it_works": "This combination plays to your strengths...",
            },
            {
                "outfit_id": "rec_002",
                "items": ["item_4", "item_5", "item_6"],
                "why_it_works": "For a more casual vibe...",
            },
            {
                "outfit_id": "rec_003",
                "items": ["item_7", "item_8", "item_9"],
                "why_it_works": "Perfect for evening events...",
            },
        ],
    }
```

**Wire into services (no-op for now):**

```python
# app/services/try_on.py
async def create_try_on(
    user_id: str,
    person_image_url: str,
    wardrobe_items: list[str],
    arq_pool,  # Injected from FastAPI dependency
) -> TryOnResponse:
    """Create try-on job (enqueue ARQ task)."""
    job = await arq_pool.enqueue_job(
        "replicate_worker",
        person_image_url,
        wardrobe_items,
        user_id,
    )
    # Save job_id to DB
    return TryOnResponse(
        id=job.job_id,
        status="processing",
        ...
    )
```

**Definition of Done:**
- [ ] `app/core/queue.py` created
- [ ] `app/workers/base.py` created with 3 stub workers
- [ ] ARQ pool initialized in lifespan
- [ ] Services can enqueue jobs (no actual processing yet)
- [ ] Tests verify job enqueueing works
- [ ] Documented: `docs/WORKERS_SETUP.md`

**Why wait?** Sprint 0.4 rate limiting must be in place before workers start (to prevent abuse). But we scaffold it now.

---

## T3: Readiness Probe + Health Check (Day 1)

**Owner:** Sasha  
**Duration:** 1 hour  
**Blocker:** None  

### Instructions

**Update `app/health.py`:**

```python
from fastapi import APIRouter, HTTPException
from app.core.database import get_db
from app.core.queue import get_arq_pool
import redis

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/ready")
async def readiness_probe(
    db = Depends(get_db),
    arq = Depends(get_arq_pool),
) -> dict:
    """
    Kubernetes readiness probe.
    Returns 200 if all dependencies healthy, 503 otherwise.
    """
    checks = {}
    
    # Database
    try:
        await db.execute("SELECT 1")
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error: {str(e)}"
        raise HTTPException(status_code=503, detail="Database unavailable")
    
    # Redis (ARQ pool)
    try:
        ping = await arq.ping()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {str(e)}"
        raise HTTPException(status_code=503, detail="Redis unavailable")
    
    return {
        "status": "ready",
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat(),
    }

@router.get("/live")
async def liveness_probe() -> dict:
    """
    Kubernetes liveness probe.
    Returns 200 if app is running (not hung).
    """
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}
```

**Update `app/main.py`:**

```python
from app.health import router as health_router

app.include_router(health_router)
```

**Test:**
```bash
curl http://localhost:8000/health/ready
# Expected: 200 {"status": "ready", "checks": {...}}

curl http://localhost:8000/health/live
# Expected: 200 {"status": "alive", ...}
```

**Definition of Done:**
- [ ] Readiness probe returns 503 if any dependency down
- [ ] Liveness probe always returns 200 (if app running)
- [ ] Docker healthcheck configured
- [ ] Railway health check wired to `/health/ready`

---

## T4: Worker Monitoring & Observability (Day 2)

**Owner:** Sasha + Alejo (architecture review)  
**Duration:** 3 hours  
**Blocker:** None (Sentry setup waits for Sprint 0.4, but can scaffold)  

### Instructions

**Create `app/core/observability.py`:**

```python
import logging
import json
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)

class WorkerLogger:
    """Log worker job events for debugging + monitoring."""
    
    @staticmethod
    def log_job_start(job_id: str, worker_name: str, params: Dict[str, Any]):
        logger.info(
            "job_start",
            extra={
                "job_id": job_id,
                "worker": worker_name,
                "params_keys": list(params.keys()),
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
    
    @staticmethod
    def log_job_success(job_id: str, worker_name: str, result: Dict[str, Any]):
        logger.info(
            "job_success",
            extra={
                "job_id": job_id,
                "worker": worker_name,
                "result_keys": list(result.keys()),
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
    
    @staticmethod
    def log_job_failure(job_id: str, worker_name: str, error: str, retry_count: int = 0):
        logger.error(
            "job_failure",
            extra={
                "job_id": job_id,
                "worker": worker_name,
                "error": error,
                "retry_count": retry_count,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

# Example usage in workers:
# WorkerLogger.log_job_start(job_id, "vision_worker", {"image_url": "..."})
# try:
#     result = call_vision_api(...)
#     WorkerLogger.log_job_success(job_id, "vision_worker", result)
# except Exception as e:
#     WorkerLogger.log_job_failure(job_id, "vision_worker", str(e))
```

**Create `app/workers/monitoring.py`:**

```python
from typing import Dict, Any
import asyncio

class WorkerMetrics:
    """Collect worker performance metrics."""
    
    def __init__(self):
        self.jobs_completed = 0
        self.jobs_failed = 0
        self.total_duration_ms = 0
    
    async def track_job(self, job_id: str, worker_func, *args, **kwargs):
        """Decorator-style job tracking."""
        import time
        start = time.time()
        try:
            result = await worker_func(*args, **kwargs)
            self.jobs_completed += 1
            duration_ms = (time.time() - start) * 1000
            self.total_duration_ms += duration_ms
            return result
        except Exception as e:
            self.jobs_failed += 1
            raise
    
    def get_metrics(self) -> Dict[str, Any]:
        total = self.jobs_completed + self.jobs_failed
        return {
            "jobs_completed": self.jobs_completed,
            "jobs_failed": self.jobs_failed,
            "total_jobs": total,
            "success_rate": (self.jobs_completed / total * 100) if total > 0 else 0,
            "avg_duration_ms": (self.total_duration_ms / self.jobs_completed) if self.jobs_completed > 0 else 0,
        }
```

**Wire into metrics endpoint:**

```python
# app/health.py
@router.get("/metrics")
async def metrics() -> dict:
    """Worker performance metrics."""
    return {
        "worker_metrics": app.state.worker_metrics.get_metrics(),
        "timestamp": datetime.utcnow().isoformat(),
    }
```

**Definition of Done:**
- [ ] WorkerLogger captures job start/success/failure
- [ ] WorkerMetrics tracks completion rates + duration
- [ ] `/health/metrics` endpoint returns worker stats
- [ ] Logs structured (JSON-compatible for Sentry later)
- [ ] Documented in `docs/WORKERS_MONITORING.md`

---

## T5: Supabase RLS Policy for Try-Ons (Day 2)

**Owner:** Sasha  
**Duration:** 1 hour  
**Blocker:** None  

### Instructions

**Create `migrations/007_try_on_rls.sql`:**

```sql
-- Enable RLS on try_ons table
ALTER TABLE try_ons ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own try-ons
CREATE POLICY "try_ons_user_isolation" ON try_ons
  FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "try_ons_user_create" ON try_ons
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "try_ons_user_update" ON try_ons
  FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Policy: Workers (service role) can update job status
-- (Don't restrict to auth.uid() — workers use service_role_key)
CREATE POLICY "try_ons_worker_update" ON try_ons
  FOR UPDATE
  USING (true)  -- Service role bypasses RLS
  WITH CHECK (true);

-- Create index for faster queries
CREATE INDEX idx_try_ons_user_id ON try_ons(user_id);
CREATE INDEX idx_try_ons_status ON try_ons(status);
```

**Apply migration:**

```bash
# Option A: If using supabase CLI
supabase db push

# Option B: Manual in Supabase dashboard
# Copy SQL into SQL editor and run
```

**Test RLS:**

```python
# As authenticated user (should see their try-ons)
user_try_ons = supabase.table("try_ons").select("*").eq("user_id", user_id).execute()

# As service role (for workers)
service_role_try_ons = admin_client.table("try_ons").select("*").execute()
```

**Definition of Done:**
- [ ] RLS policies created for try_ons table
- [ ] Indexes created for performance
- [ ] Tested: users see only their data
- [ ] Tested: workers can update via service role
- [ ] Migration documented

---

## T6: Documentation — Workers Integration Guide (Day 3)

**Owner:** Sasha  
**Duration:** 2 hours  
**Blocker:** None  

### Instructions

**Create `docs/WORKERS_INTEGRATION_GUIDE.md`:**

Include sections:
1. **Architecture overview** — ARQ pool, workers, job flow
2. **Setting up workers** — Queue creation, pool initialization
3. **Enqueuing jobs** — How to call workers from services
4. **Worker stubs** — Mock responses vs real APIs
5. **Monitoring** — Health checks, metrics, logging
6. **Error handling** — Retries, DLQ, fallback
7. **Debugging** — How to check job status, logs
8. **Switching mock → real** — When credentials arrive, what changes
9. **Local development** — Running Redis locally, testing jobs
10. **Production deployment** — Railway Redis, monitoring

Example structure:

```markdown
# Workers Integration Guide

## Quick Start
1. ARQ pool created in lifespan
2. 3 workers available: vision, replicate, claude (stubs)
3. Services can enqueue jobs
4. Results stored in DB
5. Poll GET /try-ons/{id} for status

## When are workers real?
- Day 1-2 (now): Stubs return mock responses
- Day 3 (Sprint 0.5 start): Swap to real APIs when:
  - Juan Camilo provides credentials
  - Sprint 0.4 rate limiting approved
  - ARQ pool test passes

## How to test a worker
\`\`\`python
from app.workers.base import vision_worker
result = await vision_worker(
    image_url="https://example.com/image.jpg",
    user_id="user_123",
    job_id="job_456",
)
print(result)  # Mock response
\`\`\`

## Error scenarios
- Image URL invalid (SSRF check) → 400
- Worker timeout (>60s) → retry 3x then fail
- Worker fails (API error) → logged, user sees "try again"
```

**Definition of Done:**
- [ ] Comprehensive guide written
- [ ] Examples provided for each worker
- [ ] Debugging steps documented
- [ ] Ready for Antigravity to extend when they take Sprint 0.5

---

## Summary: What Sasha Delivers (3 Days)

| Task | Duration | Deliverable | Status |
|------|----------|-------------|--------|
| T1: Supabase bucket | 30 min | `/try-ons/` bucket ready | ✅ |
| T2: ARQ workers scaffold | 4 hours | 3 worker stubs + pool setup | ✅ |
| T3: Health checks | 1 hour | Readiness + liveness probes | ✅ |
| T4: Observability | 3 hours | Job logging + metrics | ✅ |
| T5: RLS policies | 1 hour | Row-level security on try_ons | ✅ |
| T6: Documentation | 2 hours | `WORKERS_INTEGRATION_GUIDE.md` | ✅ |

**Total: ~11.5 hours over 3 days**

---

## Definition of Done

- [ ] All 6 tasks completed
- [ ] Tests: `test_arq_pool.py`, `test_health_checks.py`, `test_rls_policies.py`
- [ ] Coverage ≥85%
- [ ] Ruff clean
- [ ] Documented + ready for Antigravity Sprint 0.5

---

## Success Criteria

**By EOD Wednesday (2026-05-20):**
- ARQ pool real and tested
- Supabase bucket ready for try-on storage
- Health checks reporting correctly
- Worker stubs ready to swap with real APIs
- Documentation complete
- **Ready for Spring 0.5 when Juan Camilo provides credentials**

---

## Dependencies

- ✅ Database migration 006 applied (idempotency)
- ✅ Supabase credentials (SUPABASE_URL, SERVICE_ROLE_KEY)
- ⏳ Real worker credentials (waiting on Juan Camilo)
- ⏳ Sprint 0.4 rate limiting (Antigravity, for full Sprint 0.5)

---

## Notes

- No breaking changes to existing endpoints
- All work is scaffolding + infrastructure
- Workers remain stubs until credentials arrive
- Full Sprint 0.5 integration waits for rate limiting + credentials
- You're unblocked — can start today

---

**Trigger Status:** 🟢 **READY — Start immediately**

Questions? → Jarvis

Let's go 🚀
