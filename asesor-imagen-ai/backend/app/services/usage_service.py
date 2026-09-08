"""
Usage service — weekly counters with lazy reset (Sprint 0.5 T5).

Q5 approved: Lazy reset is the FALLBACK in case the Antigravity weekly cron
job doesn't fire on time. Called on:
    - GET /users/me/usage
    - POST /try-ons (before cap check)

Source of truth is Postgres (function `public.reset_usage_if_stale` from
migration 007). Redis counters remain for fast cap enforcement, and are
reconciled by `reconcile_worker` (ARQ cron).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any
from uuid import UUID

logger = logging.getLogger(__name__)


@dataclass
class UsageSnapshot:
    """In-memory representation of a user's current weekly usage."""

    user_id: UUID
    week_start_date: Any
    try_ons_used: int
    try_ons_base_used: int
    try_ons_std_used: int
    try_ons_pro_used: int
    was_reset: bool


class UsageService:
    """Read + reset weekly usage. Cap enforcement remains in rate_limiter."""

    def __init__(self, admin: Any) -> None:
        self._admin = admin

    async def get_or_reset(self, *, user_id: UUID) -> UsageSnapshot:
        """Call `reset_usage_if_stale(user_id)` via RPC and return snapshot.

        Safe to call on every request — the RPC short-circuits when the row
        is already current (Postgres CURRENT_DATE check, no UPDATE).
        """
        try:
            res = await (
                self._admin.trusted()
                .schema("public")
                .rpc("reset_usage_if_stale", {"p_user_id": str(user_id)})
                .execute()
            )
        except Exception as exc:  # noqa: BLE001 — fail-open to avoid breaking traffic
            logger.error("reset_usage_if_stale RPC failed: %s", exc)
            return UsageSnapshot(
                user_id=user_id,
                week_start_date=None,
                try_ons_used=0,
                try_ons_base_used=0,
                try_ons_std_used=0,
                try_ons_pro_used=0,
                was_reset=False,
            )

        rows = res.data or []
        row = rows[0] if rows else {}
        snapshot = UsageSnapshot(
            user_id=user_id,
            week_start_date=row.get("week_start_date"),
            try_ons_used=int(row.get("try_ons_used") or 0),
            try_ons_base_used=int(row.get("try_ons_base_used") or 0),
            try_ons_std_used=int(row.get("try_ons_std_used") or 0),
            try_ons_pro_used=int(row.get("try_ons_pro_used") or 0),
            was_reset=bool(row.get("was_reset")),
        )
        if snapshot.was_reset:
            logger.info("Lazy reset triggered for user %s", user_id)
        return snapshot
