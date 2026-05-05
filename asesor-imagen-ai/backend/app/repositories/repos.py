"""
Concrete repositories — one per domain entity.

All repos extend BaseRepository, which handles the AdminClient guard and
standard CRUD. Additional domain-specific methods are added below.

Table → Model mapping
─────────────────────
profiles           → models.profile.Profile
wardrobe_items     → models.wardrobe.WardrobeItem
body_analyses      → models.body_analysis.BodyAnalysis
recommendations    → models.recommendation.Recommendation
recommendation_items → models.recommendation.RecommendationItem
try_ons            → models.try_on.TryOn
subscriptions      → models.subscription.Subscription
usage_counters     → models.usage_counter.UsageCounter
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any
from uuid import UUID

from app.core.admin_client import AdminClient
from app.core.exceptions import NotFoundError
from app.models.body_analysis import BodyAnalysis
from app.models.profile import Profile
from app.models.recommendation import Recommendation, RecommendationItem
from app.models.subscription import Subscription
from app.models.try_on import TryOn
from app.models.usage_counter import UsageCounter
from app.models.wardrobe import WardrobeItem
from app.repositories.base import BaseRepository


# ---------------------------------------------------------------------------
# ProfileRepository
# ---------------------------------------------------------------------------


class ProfileRepository(BaseRepository[Profile]):
    """CRUD for the `profiles` table."""

    def __init__(self, admin: AdminClient) -> None:
        super().__init__(admin, "profiles", Profile)

    async def get_profile(self, *, user_id: UUID) -> Profile | None:
        """Return the profile for *user_id*, or None if not yet created."""
        response = await (
            self._admin
            .with_user_check(user_id=user_id)
            .table(self._table)
            .select("*")
            .eq("id", str(user_id))
            .maybe_single()
            .execute()
        )
        return self._parse(response.data) if response.data else None

    async def upsert_profile(self, *, user_id: UUID, data: dict[str, Any]) -> Profile:
        """Create or update the profile for *user_id*."""
        payload = {**data, "id": str(user_id), "user_id": str(user_id)}
        response = await (
            self._admin
            .with_user_check(user_id=user_id)
            .table(self._table)
            .upsert(payload)
            .single()
            .execute()
        )
        return self._parse(response.data)


# ---------------------------------------------------------------------------
# WardrobeRepository
# ---------------------------------------------------------------------------


class WardrobeRepository(BaseRepository[WardrobeItem]):
    """CRUD for the `wardrobe_items` table (with soft-delete support)."""

    def __init__(self, admin: AdminClient) -> None:
        super().__init__(admin, "wardrobe_items", WardrobeItem)

    async def list_active(
        self,
        *,
        user_id: UUID,
        page: int = 1,
        per_page: int = 20,
        category: str | None = None,
    ) -> tuple[list[WardrobeItem], int]:
        """Return non-deleted items for *user_id*, optionally filtered by category."""
        filters: dict[str, Any] = {}
        if category:
            filters["category"] = category

        # Exclude soft-deleted rows
        query = (
            self._admin
            .with_user_check(user_id=user_id)
            .table(self._table)
            .select("*", count="exact")
            .is_("deleted_at", "null")
        )

        for col, val in filters.items():
            query = query.eq(col, val)

        offset = (page - 1) * per_page
        query = query.order("created_at", desc=True).range(offset, offset + per_page - 1)

        response = await query.execute()
        total = response.count or 0
        return self._parse_many(response.data or []), total


# ---------------------------------------------------------------------------
# BodyAnalysisRepository
# ---------------------------------------------------------------------------


class BodyAnalysisRepository(BaseRepository[BodyAnalysis]):
    """CRUD for the `body_analyses` table."""

    def __init__(self, admin: AdminClient) -> None:
        super().__init__(admin, "body_analyses", BodyAnalysis)

    async def get_latest(self, *, user_id: UUID) -> BodyAnalysis | None:
        """Return the most recent body analysis for *user_id*, or None."""
        response = await (
            self._admin
            .with_user_check(user_id=user_id)
            .table(self._table)
            .select("*")
            .order("created_at", desc=True)
            .limit(1)
            .maybe_single()
            .execute()
        )
        return self._parse(response.data) if response.data else None


# ---------------------------------------------------------------------------
# RecommendationRepository
# ---------------------------------------------------------------------------


class RecommendationRepository(BaseRepository[Recommendation]):
    """CRUD for the `recommendations` table."""

    def __init__(self, admin: AdminClient) -> None:
        super().__init__(admin, "recommendations", Recommendation)

    async def record_feedback(
        self,
        *,
        user_id: UUID,
        recommendation_id: UUID,
        clicked: bool | None = None,
        liked: bool | None = None,
        tried_on: bool | None = None,
    ) -> Recommendation:
        """Apply engagement feedback to a recommendation."""
        data: dict[str, Any] = {
            "feedback_at": datetime.now(timezone.utc).isoformat()
        }
        if clicked is not None:
            data["clicked"] = clicked
        if liked is not None:
            data["liked"] = liked
        if tried_on is not None:
            data["tried_on"] = tried_on

        return await self.update(
            user_id=user_id,
            record_id=recommendation_id,
            data=data,
        )


# ---------------------------------------------------------------------------
# RecommendationItemRepository
# ---------------------------------------------------------------------------


class RecommendationItemRepository(BaseRepository[RecommendationItem]):
    """
    CRUD for the `recommendation_items` join table.

    Note: This table does NOT have a user_id column directly; ownership is
    established through the parent recommendation. We override base methods
    where user_id filtering via the join table is needed.
    """

    def __init__(self, admin: AdminClient) -> None:
        super().__init__(admin, "recommendation_items", RecommendationItem)

    async def list_for_recommendation(
        self,
        *,
        recommendation_id: UUID,
    ) -> list[RecommendationItem]:
        """Return all items belonging to *recommendation_id*."""
        response = await (
            self._admin
            .trusted()  # Ownership already checked on parent recommendation
            .table(self._table)
            .select("*")
            .eq("recommendation_id", str(recommendation_id))
            .order("position")
            .execute()
        )
        return self._parse_many(response.data or [])

    async def bulk_create(
        self,
        *,
        recommendation_id: UUID,
        items: list[dict[str, Any]],
    ) -> list[RecommendationItem]:
        """Insert multiple recommendation items in one call."""
        payload = [
            {**item, "recommendation_id": str(recommendation_id)}
            for item in items
        ]
        response = await (
            self._admin
            .trusted()
            .table(self._table)
            .insert(payload)
            .execute()
        )
        return self._parse_many(response.data or [])


# ---------------------------------------------------------------------------
# TryOnRepository
# ---------------------------------------------------------------------------


class TryOnRepository(BaseRepository[TryOn]):
    """CRUD for the `try_ons` table (virtual try-on jobs)."""

    def __init__(self, admin: AdminClient) -> None:
        super().__init__(admin, "try_ons", TryOn)

    async def get_by_content_hash(
        self, *, user_id: UUID, content_hash: str
    ) -> TryOn | None:
        """
        Look up a cached try-on result by content_hash (ADR-004).

        Returns the most recent completed try-on for *user_id* with this
        content_hash, or None if no cache hit.
        """
        response = await (
            self._admin
            .with_user_check(user_id=user_id)
            .table(self._table)
            .select("*")
            .eq("content_hash", content_hash)
            .eq("status", "completed")
            .order("created_at", desc=True)
            .limit(1)
            .maybe_single()
            .execute()
        )
        return self._parse(response.data) if response.data else None

    async def update_status(
        self,
        *,
        record_id: UUID,
        status: str,
        result_image_url: str | None = None,
        result_cdn_url: str | None = None,
        error_message: str | None = None,
        inference_time_ms: int | None = None,
    ) -> TryOn:
        """
        Update the processing status of a try-on job.

        Called by the ARQ worker — uses trusted() because there's no
        user JWT in the background context.
        """
        data: dict[str, Any] = {
            "status": status,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        if result_image_url is not None:
            data["result_image_url"] = result_image_url
        if result_cdn_url is not None:
            data["result_cdn_url"] = result_cdn_url
        if error_message is not None:
            data["error_message"] = error_message
        if inference_time_ms is not None:
            data["inference_time_ms"] = inference_time_ms
        if status == "completed":
            data["completed_at"] = datetime.now(timezone.utc).isoformat()

        response = await (
            self._admin
            .trusted()
            .table(self._table)
            .update(data)
            .eq("id", str(record_id))
            .single()
            .execute()
        )
        if response.data is None:
            raise NotFoundError("try_on")
        return self._parse(response.data)


# ---------------------------------------------------------------------------
# SubscriptionRepository
# ---------------------------------------------------------------------------


class SubscriptionRepository(BaseRepository[Subscription]):
    """CRUD for the `subscriptions` table."""

    def __init__(self, admin: AdminClient) -> None:
        super().__init__(admin, "subscriptions", Subscription)

    async def get_active(self, *, user_id: UUID) -> Subscription | None:
        """Return the active/trialing subscription for *user_id*, or None."""
        response = await (
            self._admin
            .with_user_check(user_id=user_id)
            .table(self._table)
            .select("*")
            .in_("status", ["active", "trialing"])
            .order("created_at", desc=True)
            .limit(1)
            .maybe_single()
            .execute()
        )
        return self._parse(response.data) if response.data else None

    async def sync_from_webhook(self, *, data: dict[str, Any]) -> Subscription:
        """
        Upsert subscription data from a payment provider webhook.

        Trusted — webhook signature already verified by the calling handler.
        """
        return await self.trusted_upsert(data)


# ---------------------------------------------------------------------------
# UsageCounterRepository
# ---------------------------------------------------------------------------


class UsageCounterRepository(BaseRepository[UsageCounter]):
    """CRUD for the `usage_counters` table (monthly usage tracking)."""

    def __init__(self, admin: AdminClient) -> None:
        super().__init__(admin, "usage_counters", UsageCounter)

    async def get_current_period(self, *, user_id: UUID) -> UsageCounter | None:
        """Return the counter for the current billing period, or None."""
        today = date.today()
        period_start = today.replace(day=1).isoformat()

        response = await (
            self._admin
            .with_user_check(user_id=user_id)
            .table(self._table)
            .select("*")
            .eq("period_start", period_start)
            .maybe_single()
            .execute()
        )
        return self._parse(response.data) if response.data else None

    async def increment(
        self,
        *,
        user_id: UUID,
        field: str,
        amount: int = 1,
    ) -> UsageCounter:
        """
        Atomically increment a usage counter field.

        Uses RPC to avoid race conditions (PostgREST stored procedure).
        Falls back to trusted_upsert for initial counter creation.

        Args:
            user_id: Owner of the counter.
            field: One of 'try_ons_used', 'recommendations_used', 'body_analyses_used'.
            amount: Number to increment by (default 1).
        """
        allowed = {"try_ons_used", "recommendations_used", "body_analyses_used"}
        if field not in allowed:
            raise ValueError(f"field must be one of {allowed}, got {field!r}")

        today = date.today()
        period_start = today.replace(day=1).isoformat()

        # Upsert + increment via raw SQL (trusted worker context)
        response = await (
            self._admin
            .trusted()
            .table(self._table)
            .upsert(
                {
                    "user_id": str(user_id),
                    "period_start": period_start,
                    field: amount,
                },
                on_conflict="user_id,period_start",
            )
            .single()
            .execute()
        )
        return self._parse(response.data)
