"""
Finite-State Machine for try-on job lifecycle (Sprint 0.5 T2).

State diagram
─────────────

                ┌────────────────────────────┐
                │                            ▼
    queued ──► cache_lookup ──► cache_hit ──► completed
                  │
                  └──► inference_running ──► uploading ──► completed
                                │
                                └──► fallback_triggered ──► inference_running
                                                                │
                                                                └──► failed

Persistence
───────────
Stored on `try_ons` in two columns (see migration 007):
    - fsm_state    TEXT          — current state
    - fsm_history  JSONB         — array of {state, at, meta} entries

Why FSM (and not just `status`)?
    `status` (pending|processing|completed|failed) is the public-facing
    contract for the mobile app. FSM is internal — it tells us WHY a try-on
    is in `processing`: is it waiting for cache, doing inference, uploading?
    This unlocks better metrics (`fashn_inference_latency_seconds` only
    measures the inference state, not the whole job).
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


class FSMState(str, enum.Enum):
    """All valid states for the try-on job FSM.

    Mirror of the CHECK constraint in migration 007. Keep in sync.
    """

    QUEUED = "queued"
    CACHE_LOOKUP = "cache_lookup"
    CACHE_HIT = "cache_hit"
    INFERENCE_RUNNING = "inference_running"
    UPLOADING = "uploading"
    COMPLETED = "completed"
    FAILED = "failed"
    FALLBACK_TRIGGERED = "fallback_triggered"


# Allowed transitions. Keys = from-state, values = set of allowed next states.
ALLOWED_TRANSITIONS: dict[FSMState, set[FSMState]] = {
    FSMState.QUEUED: {FSMState.CACHE_LOOKUP, FSMState.FAILED},
    FSMState.CACHE_LOOKUP: {
        FSMState.CACHE_HIT,
        FSMState.INFERENCE_RUNNING,
        FSMState.FAILED,
    },
    FSMState.CACHE_HIT: {FSMState.UPLOADING, FSMState.COMPLETED, FSMState.FAILED},
    FSMState.INFERENCE_RUNNING: {
        FSMState.UPLOADING,
        FSMState.FALLBACK_TRIGGERED,
        FSMState.FAILED,
    },
    FSMState.UPLOADING: {FSMState.COMPLETED, FSMState.FAILED},
    FSMState.FALLBACK_TRIGGERED: {FSMState.INFERENCE_RUNNING, FSMState.FAILED},
    FSMState.COMPLETED: set(),  # terminal
    FSMState.FAILED: set(),     # terminal
}


class InvalidTransitionError(RuntimeError):
    """Raised when a transition is not allowed by ALLOWED_TRANSITIONS."""


@dataclass
class HistoryEntry:
    """One row of the fsm_history JSONB array."""

    state: FSMState
    at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    meta: dict[str, Any] = field(default_factory=dict)

    def to_jsonable(self) -> dict[str, Any]:
        return {
            "state": self.state.value,
            "at": self.at.isoformat(),
            "meta": self.meta,
        }


def can_transition(current: FSMState | str, target: FSMState | str) -> bool:
    """Return True if `current → target` is allowed."""
    current_e = FSMState(current) if not isinstance(current, FSMState) else current
    target_e = FSMState(target) if not isinstance(target, FSMState) else target
    return target_e in ALLOWED_TRANSITIONS.get(current_e, set())


def transition(
    current: FSMState | str,
    target: FSMState | str,
    *,
    meta: dict[str, Any] | None = None,
) -> HistoryEntry:
    """Validate transition + return a HistoryEntry to append to fsm_history.

    Raises:
        InvalidTransitionError: when the transition is not allowed.
    """
    current_e = FSMState(current) if not isinstance(current, FSMState) else current
    target_e = FSMState(target) if not isinstance(target, FSMState) else target
    if not can_transition(current_e, target_e):
        raise InvalidTransitionError(
            f"Invalid FSM transition: {current_e.value} -> {target_e.value}"
        )
    return HistoryEntry(state=target_e, meta=meta or {})


def is_terminal(state: FSMState | str) -> bool:
    """True for `completed` / `failed`."""
    state_e = FSMState(state) if not isinstance(state, FSMState) else state
    return state_e in (FSMState.COMPLETED, FSMState.FAILED)


# ─────────────────────────────────────────────────────────────
# FASHN tier mapping (Sprint 0.5 T4)
# ─────────────────────────────────────────────────────────────
# Free plan      → BASE  → FASHN "performance" mode (cheapest, fastest)
# Estilo plan    → STD   → FASHN "balanced"
# Imagen plan    → PRO   → FASHN "quality"
#
# Fallback rule (T4): if PRO times out (>15s), retry with STD.

PLAN_TO_TIER: dict[str, str] = {
    "free": "BASE",
    "estilo": "STD",
    "imagen": "PRO",
}

TIER_TO_FASHN_MODE: dict[str, str] = {
    "BASE": "performance",
    "STD": "balanced",
    "PRO": "quality",
}


def plan_to_fashn_mode(plan: str | None) -> str:
    """Return the FASHN mode string for a given subscription plan.

    Defaults to "performance" for unknown / None plans.
    """
    if not plan:
        return TIER_TO_FASHN_MODE["BASE"]
    tier = PLAN_TO_TIER.get(plan, "BASE")
    return TIER_TO_FASHN_MODE[tier]


def plan_to_tier(plan: str | None) -> str:
    """Return BASE / STD / PRO for a plan name. Defaults to BASE."""
    return PLAN_TO_TIER.get(plan or "", "BASE")
