"""FastAPI application for agent orchestration."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import os
from datetime import datetime
from pathlib import Path

from api.config import settings

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


# === HEALTH CHECK ===
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "environment": settings.environment,
        "vault": f"{settings.vault_path} (exists: {os.path.exists(settings.vault_path)})".format(),
    }


# === AGENT STATE MANAGEMENT ===
def get_agent_state_path(agent_name: str) -> Path:
    """Get path to agent state file."""
    return Path(settings.agent_state_path) / f"{agent_name}.json"


def read_agent_state(agent_name: str) -> dict:
    """Read agent state from vault."""
    state_file = get_agent_state_path(agent_name)
    if state_file.exists():
        with open(state_file, "r") as f:
            return json.load(f)
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
async def get_agent_state_endpoint(agent_id: str):
    """Get current state of an agent."""
    try:
        state = read_agent_state(agent_id)
        return {
            "agent_id": agent_id,
            "state": state,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agents/{agent_id}/execute", tags=["agents"])
async def execute_agent(agent_id: str, prompt: str):
    """
    Execute an agent with a prompt.
    Note: This is a placeholder. Integration with agent-runner.py happens in FASE 2.
    """
    try:
        # Update state: executing
        write_agent_state(agent_id, {
            "status": "executing",
            "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
            "started_at": datetime.now().isoformat(),
        })

        # TODO: Call agent-runner.py in FASE 2
        # For now, return acknowledgment

        return {
            "agent_id": agent_id,
            "status": "queued",
            "message": "Agent execution queued. Integration with agent-runner.py in FASE 2.",
            "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agents", tags=["agents"])
async def list_agents():
    """List all agents and their states."""
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
