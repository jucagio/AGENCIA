"""FastAPI application for agent orchestration."""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from collections import defaultdict
import time

from api.config import settings
from api.security.jwt import JWTHandler
from api.security.permissions import PermissionChecker
from api.dependencies import get_current_user, require_permission

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Orquestación de agentes IA locales con Obsidian vault",
    version="0.1.0",
    debug=settings.debug
)

# CORS Middleware — solo localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["*"],
)


# === RATE LIMITING MIDDLEWARE ===
class RateLimitMiddleware(BaseHTTPMiddleware):
    """In-memory rate limiting (30 requests per minute per IP)."""

    def __init__(self, app, requests_per_minute: int = 30):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.request_log = defaultdict(list)

    async def dispatch(self, request, call_next):
        client_ip = request.client.host
        now = time.time()

        # Clean old requests (older than 1 minute)
        self.request_log[client_ip] = [
            req_time for req_time in self.request_log[client_ip]
            if now - req_time < 60
        ]

        # Check rate limit
        if len(self.request_log[client_ip]) >= self.requests_per_minute:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Max 30 requests per minute."}
            )

        self.request_log[client_ip].append(now)
        response = await call_next(request)
        return response


# === AUDIT MIDDLEWARE ===
class AuditMiddleware(BaseHTTPMiddleware):
    """Log all API requests for auditing."""

    def __init__(self, app):
        super().__init__(app)
        self.audit_log_path = Path(settings.agent_logs_path) / "api_audit.jsonl"
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)

    async def dispatch(self, request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path
        timestamp = datetime.now().isoformat()

        response = await call_next(request)

        # Log to audit file
        audit_entry = {
            "timestamp": timestamp,
            "client_ip": client_ip,
            "method": method,
            "path": path,
            "status_code": response.status_code,
        }

        try:
            with open(self.audit_log_path, "a") as f:
                f.write(json.dumps(audit_entry) + "\n")
        except Exception:
            pass  # Don't fail request if audit logging fails

        return response


app.add_middleware(AuditMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=30)


# === HEALTH CHECK ===
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "environment": settings.environment,
        "vault": f"{settings.vault_path} (exists: {os.path.exists(settings.vault_path)})".format(),
    }


# === AUTHENTICATION ===
@app.post("/auth/login", tags=["auth"])
async def login(username: str, password: str):
    """
    Login endpoint to get JWT token.

    For local development, hardcoded credentials:
    - username: "jarvis", password: "agencia" (admin)
    - username: "sasha", password: "agencia" (agent)

    In production, replace with database lookup.
    """
    # Hardcoded credentials for development (replace with DB in production)
    credentials = {
        "jarvis": {"password": "agencia", "role": "admin"},
        "sasha": {"password": "agencia", "role": "agent"},
        "brook": {"password": "agencia", "role": "agent"},
        "erik": {"password": "agencia", "role": "agent"},
        "cinthya": {"password": "agencia", "role": "agent"},
        "jade": {"password": "agencia", "role": "agent"},
        "alejo": {"password": "agencia", "role": "agent"},
        "ego": {"password": "agencia", "role": "admin"},
        "leo": {"password": "agencia", "role": "agent"},
        "yang": {"password": "agencia", "role": "agent"},
    }

    user = credentials.get(username)
    if not user or user["password"] != password:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token with 24-hour expiration
    token_data = {
        "sub": username,
        "role": user["role"],
        "permissions": PermissionChecker.get_permissions(user["role"]),
    }
    access_token = JWTHandler.create_token(
        token_data,
        expires_delta=timedelta(hours=24)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": username,
        "role": user["role"],
    }


# === AGENT STATE MANAGEMENT ===
def get_agent_state_path(agent_name: str) -> Path:
    """Get path to agent state file."""
    return Path(settings.agent_state_path) / f"{agent_name}.json"


def read_agent_state(agent_name: str) -> dict:
    """Read agent state from vault."""
    state_file = get_agent_state_path(agent_name)
    if state_file.exists():
        try:
            with open(state_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return {"status": "idle", "last_updated": None}
    return {"status": "idle", "last_updated": None}


def write_agent_state(agent_name: str, state: dict) -> None:
    """Write agent state to vault."""
    state_file = get_agent_state_path(agent_name)
    state["last_updated"] = datetime.now().isoformat()
    state_file.parent.mkdir(parents=True, exist_ok=True)
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2)


# === AGENT ENDPOINTS ===
@app.get("/agents/{agent_id}/state", tags=["agents"])
async def get_agent_state_endpoint(agent_id: str, current_user: dict = Depends(get_current_user)):
    """Get current state of an agent. Requires authentication."""
    try:
        state = read_agent_state(agent_id)
        return {
            "agent_id": agent_id,
            "state": state,
            "requested_by": current_user["user_id"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/agents/{agent_id}/execute", tags=["agents"])
async def execute_agent(
    agent_id: str,
    prompt: str,
    current_user: dict = Depends(get_current_user),
    _: dict = Depends(require_permission("agents:execute"))
):
    """
    Execute an agent with a prompt. Requires authentication and agents:execute permission.
    """
    try:
        # Update state: executing
        write_agent_state(agent_id, {
            "status": "executing",
            "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
            "started_at": datetime.now().isoformat(),
            "executed_by": current_user["user_id"],
        })

        # TODO: Call agent-runner.py in FASE 2
        # For now, return acknowledgment

        return {
            "agent_id": agent_id,
            "status": "queued",
            "message": "Agent execution queued. Integration with agent-runner.py in FASE 2.",
            "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
            "executed_by": current_user["user_id"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/agents", tags=["agents"])
async def list_agents(current_user: dict = Depends(get_current_user)):
    """List all agents and their states. Requires authentication."""
    state_dir = Path(settings.agent_state_path)
    agents = {}

    if state_dir.exists():
        for state_file in state_dir.glob("*.json"):
            agent_name = state_file.stem
            try:
                with open(state_file, "r") as f:
                    agents[agent_name] = json.load(f)
            except:
                pass

    return {
        "agents": agents,
        "total": len(agents),
        "requested_by": current_user["user_id"],
    }


# === INFO ENDPOINTS ===
@app.get("/config", tags=["info"])
async def get_config():
    """Get application configuration (non-sensitive)."""
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "vault_path": settings.vault_path,
        "debug": settings.debug,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
