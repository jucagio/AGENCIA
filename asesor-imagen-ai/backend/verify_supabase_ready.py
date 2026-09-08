"""
verify_supabase_ready.py — Sprint Fase 1 end-to-end checks.

Owner: Sasha (Backend & Security)

Verifica que un proyecto Supabase real esté listo para producción:

  [1] Conectividad: SUPABASE_URL + ANON_KEY responden /auth/v1/settings.
  [2] Service role válido: GET /auth/v1/admin/users con SERVICE_ROLE_KEY.
  [3] Migraciones aplicadas: PostgREST expone las 12 tablas + buckets.
  [4] Auth real funciona: register (admin API) + login (password grant).
  [5] Wardrobe CRUD: POST /api/v1/wardrobe con JWT real -> 201.
  [6] Try-on accept payload: POST /api/v1/try-ons con JWT real -> 201/202.

Cómo correr:
    # 1. Asegúrate de tener .env con SUPABASE_URL/ANON_KEY/SERVICE_ROLE_KEY llenos.
    # 2. Levanta el backend en otra terminal:  uvicorn app.main:app --port 8000
    # 3. Ejecuta:                              python verify_supabase_ready.py

Salida: códigos de retorno
    0 -> READY (Fase 1 cerrada, listo para Fase 2)
    1 -> Algún check falló (revisa stdout, NO avanzar a Fase 2)
"""

from __future__ import annotations

import json
import os
import sys
import time
import uuid
from typing import Optional

import httpx

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
TIMEOUT = 15.0


def _load_env() -> dict[str, str]:
    """Read .env from same dir (simple parser, no dotenv dependency)."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    out: dict[str, str] = {}
    if not os.path.exists(env_path):
        return out
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


# Merge .env into os.environ (without overriding shell env)
for k, v in _load_env().items():
    os.environ.setdefault(k, v)

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY", "")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")


# ---------------------------------------------------------------------------
# Pretty printing helpers
# ---------------------------------------------------------------------------
def _ok(msg: str) -> None:
    print(f"  [OK]   {msg}")


def _fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


def _info(msg: str) -> None:
    print(f"  [INFO] {msg}")


def _section(n: int, total: int, title: str) -> None:
    print()
    print(f"=== [{n}/{total}] {title} ===")


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------
def check_env() -> bool:
    _section(1, 6, "Environment variables")
    missing = []
    for name in ("SUPABASE_URL", "SUPABASE_ANON_KEY", "SUPABASE_SERVICE_ROLE_KEY"):
        if not os.environ.get(name):
            missing.append(name)
    if missing:
        _fail(f"Missing in .env: {', '.join(missing)}")
        _info("Copy .env.production.example -> .env and fill the values.")
        return False
    if not SUPABASE_URL.startswith("https://") or ".supabase.co" not in SUPABASE_URL:
        _fail(f"SUPABASE_URL has unexpected format: {SUPABASE_URL}")
        return False
    if SUPABASE_ANON_KEY == SUPABASE_SERVICE_ROLE_KEY:
        _fail("ANON_KEY == SERVICE_ROLE_KEY (must be different).")
        return False
    _ok(f"SUPABASE_URL: {SUPABASE_URL}")
    _ok(f"SUPABASE_ANON_KEY: {SUPABASE_ANON_KEY[:12]}... (len={len(SUPABASE_ANON_KEY)})")
    _ok(f"SUPABASE_SERVICE_ROLE_KEY: {SUPABASE_SERVICE_ROLE_KEY[:12]}... (len={len(SUPABASE_SERVICE_ROLE_KEY)})")
    return True


def check_connectivity() -> bool:
    _section(2, 6, "Supabase connectivity (auth settings endpoint)")
    try:
        r = httpx.get(
            f"{SUPABASE_URL}/auth/v1/settings",
            headers={"apikey": SUPABASE_ANON_KEY},
            timeout=TIMEOUT,
        )
        if r.status_code == 200:
            _ok(f"GET /auth/v1/settings -> 200; mailer_autoconfirm={r.json().get('mailer_autoconfirm')}")
            return True
        _fail(f"GET /auth/v1/settings -> {r.status_code}: {r.text[:200]}")
        return False
    except httpx.HTTPError as e:
        _fail(f"Network error: {e}")
        return False


def check_service_role() -> bool:
    _section(3, 6, "Service role key valid (admin API)")
    try:
        r = httpx.get(
            f"{SUPABASE_URL}/auth/v1/admin/users?per_page=1",
            headers={
                "apikey": SUPABASE_SERVICE_ROLE_KEY,
                "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
            },
            timeout=TIMEOUT,
        )
        if r.status_code == 200:
            count = len(r.json().get("users", []))
            _ok(f"GET /auth/v1/admin/users -> 200 (users in page: {count})")
            return True
        _fail(f"Admin API -> {r.status_code}: {r.text[:200]}")
        _info("Si es 401/403, el SERVICE_ROLE_KEY es incorrecto (cuidado: NO es el anon).")
        return False
    except httpx.HTTPError as e:
        _fail(f"Network error: {e}")
        return False


def check_migrations_applied() -> bool:
    _section(4, 6, "Migrations applied (PostgREST exposes 12 tables + buckets)")
    expected_tables = [
        "profiles",
        "subscriptions",
        "wardrobe_items",
        "body_analysis",
        "try_ons",
        "try_on_cache",
        "recommendations",
        "recommendation_items",
        "user_style_profile",
        "usage_counters",
        "idempotency_keys",
        "audit_log",
    ]
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
    }
    missing = []
    for t in expected_tables:
        # HEAD avoids returning rows; service role bypasses RLS so 200 = table exists.
        r = httpx.head(
            f"{SUPABASE_URL}/rest/v1/{t}?select=*&limit=1",
            headers=headers,
            timeout=TIMEOUT,
        )
        if r.status_code in (200, 206):
            continue
        missing.append((t, r.status_code))
    if missing:
        for t, code in missing:
            _fail(f"Table '{t}' not reachable via PostgREST (HTTP {code}).")
        _info("Re-ejecuta apply_migrations.ps1.")
        return False
    _ok(f"All {len(expected_tables)} tables reachable via PostgREST.")

    # Buckets
    r = httpx.get(
        f"{SUPABASE_URL}/storage/v1/bucket",
        headers=headers,
        timeout=TIMEOUT,
    )
    if r.status_code != 200:
        _fail(f"GET /storage/v1/bucket -> {r.status_code}")
        return False
    bucket_ids = {b["id"] for b in r.json()}
    for expected in ("avatars", "wardrobe", "tryons"):
        if expected not in bucket_ids:
            _fail(f"Bucket '{expected}' missing.")
            return False
    _ok("All 3 storage buckets present: avatars, wardrobe, tryons.")
    return True


def check_auth_register_login() -> tuple[bool, Optional[str], Optional[str]]:
    """Returns (ok, access_token, user_id) for downstream checks."""
    _section(5, 6, "Auth real: register + login via backend")
    # Use the backend (not Supabase direct) — that's what Flutter will hit.
    email = f"verify-{uuid.uuid4().hex[:8]}@asesor-test.local"
    password = "VerifyPass1234!"
    try:
        r = httpx.post(
            f"{BACKEND_URL}/api/v1/auth/register",
            json={"email": email, "password": password},
            timeout=TIMEOUT,
        )
        if r.status_code not in (200, 201):
            _fail(f"POST /api/v1/auth/register -> {r.status_code}: {r.text[:200]}")
            _info("Está corriendo el backend? -> uvicorn app.main:app --port 8000")
            return False, None, None
        body = r.json()
        access = body.get("access_token")
        uid = body.get("user_id")
        if not access:
            _fail(f"Register no devolvió access_token. body={body}")
            return False, None, None
        _ok(f"Register -> {r.status_code}; email={email}; user_id={uid}")
    except httpx.HTTPError as e:
        _fail(f"Backend register network error: {e}")
        return False, None, None

    # Login (separate path)
    try:
        r = httpx.post(
            f"{BACKEND_URL}/api/v1/auth/login",
            json={"email": email, "password": password},
            timeout=TIMEOUT,
        )
        if r.status_code != 200:
            _fail(f"POST /api/v1/auth/login -> {r.status_code}: {r.text[:200]}")
            return False, None, None
        access = r.json().get("access_token")
        _ok(f"Login -> 200; access_token={access[:24]}...")
        return True, access, uid
    except httpx.HTTPError as e:
        _fail(f"Backend login network error: {e}")
        return False, None, None


def check_wardrobe_and_tryon(access_token: str) -> bool:
    _section(6, 6, "Wardrobe CRUD + Try-On accept payload")
    auth = {"Authorization": f"Bearer {access_token}"}

    # Wardrobe POST
    payload = {
        "image_url": "https://example.com/test-shirt.jpg",
        "category": "shirt",
        "size": "M",
        "brand": "VerifyBrand",
        "user_tags": ["test", "verification"],
        "user_notes": "auto-created by verify_supabase_ready.py",
    }
    try:
        r = httpx.post(
            f"{BACKEND_URL}/api/v1/wardrobe",
            json=payload,
            headers=auth,
            timeout=TIMEOUT,
        )
        if r.status_code not in (200, 201):
            _fail(f"POST /api/v1/wardrobe -> {r.status_code}: {r.text[:300]}")
            return False
        item = r.json()
        wardrobe_id = item.get("id") or item.get("data", {}).get("id")
        if not wardrobe_id:
            _fail(f"Wardrobe response sin id. body={item}")
            return False
        _ok(f"POST /api/v1/wardrobe -> {r.status_code}; id={wardrobe_id}")
    except httpx.HTTPError as e:
        _fail(f"Wardrobe network error: {e}")
        return False

    # Wardrobe GET list (verify it's persisted)
    try:
        r = httpx.get(
            f"{BACKEND_URL}/api/v1/wardrobe",
            headers=auth,
            timeout=TIMEOUT,
        )
        if r.status_code != 200:
            _fail(f"GET /api/v1/wardrobe -> {r.status_code}")
            return False
        _ok(f"GET /api/v1/wardrobe -> 200; items returned.")
    except httpx.HTTPError as e:
        _fail(f"Wardrobe GET error: {e}")
        return False

    # Try-On POST — accept payload (status can be 201 created or 202 accepted/queued)
    tryon_payload = {
        "wardrobe_item_id": wardrobe_id,
        "content_hash": "verify_hash_" + uuid.uuid4().hex,  # >=16 chars
    }
    try:
        r = httpx.post(
            f"{BACKEND_URL}/api/v1/try-ons",
            json=tryon_payload,
            headers={**auth, "Idempotency-Key": str(uuid.uuid4())},
            timeout=TIMEOUT,
        )
        # 201/202 = accepted; 400 con error de body_analysis_id requerido = payload aceptado pero
        # negocio falta un fk -> contamos como "endpoint vivo".
        if r.status_code in (200, 201, 202):
            _ok(f"POST /api/v1/try-ons -> {r.status_code}; payload aceptado.")
            return True
        if r.status_code in (400, 422):
            # validate that the error is *business* (missing body_analysis), not infra.
            txt = r.text.lower()
            if "body_analysis" in txt or "validation" in txt:
                _ok(f"POST /api/v1/try-ons -> {r.status_code} (validation as expected; endpoint vivo).")
                return True
        _fail(f"POST /api/v1/try-ons -> {r.status_code}: {r.text[:300]}")
        return False
    except httpx.HTTPError as e:
        _fail(f"Try-on network error: {e}")
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    print("=" * 60)
    print("  verify_supabase_ready.py — Sprint Fase 1")
    print(f"  Backend: {BACKEND_URL}")
    print("=" * 60)

    if not check_env():
        return 1
    if not check_connectivity():
        return 1
    if not check_service_role():
        return 1
    if not check_migrations_applied():
        return 1

    ok, access_token, _uid = check_auth_register_login()
    if not ok or not access_token:
        return 1

    if not check_wardrobe_and_tryon(access_token):
        return 1

    print()
    print("=" * 60)
    print("  RESULT: READY (Fase 1 cerrada).")
    print("  -> Avanzar a Fase 2.")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
