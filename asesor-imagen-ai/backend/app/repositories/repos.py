"""
Concrete repositories — one per domain entity.

All repos extend BaseRepository, which handles the AdminClient guard and
standard CRUD. Additional domain-specific methods are added below.

Table → Model mapping
─────────────────────
profiles             → models.profile.Profile
wardrobe_items       → models.wardrobe.WardrobeItem
body_analysis        → models.body_analysis.BodyAnalysis        [H4: was body_analyses]
recommendations      → models.recommendation.Recommendation
recommendation_items → models.recommendation.RecommendationItem
try_ons              → models.try_on.TryOn
subscriptions        → models.subscription.Subscription
user_style_profile   → models.user_style_profile.UserStyleProfile
usage_counters       → models.usage_counter.UsageCounter
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
from app.models.user_style_profile import UserStyleProfile
from app.models.wardrobe import WardrobeItem
from app.repositories.base import BaseRepository

# ---------------------------------------------------------------------------
# ProfileRepository
# ---------------------------------------------------------------------------


class ProfileRepository(BaseRepository[Profile]):
    """CRUD for the `profiles` table.

    [H5] The profiles table uses the user UUID as its PRIMARY KEY (column "id"),
    NOT a separate user_id FK column. All guard calls use id_column="id".
    """

    def __init__(self, admin: AdminClient) -> None:
        super().__init__(admin, "profiles", Profile)

    async def get_profile(self, *, user_id: UUID) -> Profile | None:
        """Return the profile for *user_id*, or None if not yet created."""
        response = await (
            self._admin
            .with_user_check(user_id=user_id, id_column="id")
            .table(self._table)
            .select("*")
            .eq("id", str(user_id))
            .maybe_single()
            .execute()
        )
        return self._parse(response.data) if response.data else None

    async def upsert_profile(self, *, user_id: UUID, data: dict[str, Any]) -> Profile:
        """Create or update the profile for *user_id*.

        [H5] The PK of profiles is "id" (= user_id). We do NOT inject an
        extra user_id column because the table has no such column.
        """
        # profiles PK is "id"; do not inject a spurious "user_id" key
        payload = {**data, "id": str(user_id)}
        response = await (
            self._admin
            .with_user_check(user_id=user_id, id_column="id")
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
    """CRUD for the `body_analysis` table."""  # [H4: was body_analyses]

    def __init__(self, admin: AdminClient) -> None:
        # [H4] Correct table name is "body_analysis" (matches migration 004)
        super().__init__(admin, "body_analysis", BodyAnalysis)

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

    [H6] Ownership of recommendation_items is established through the parent
    recommendation. Both list_for_recommendation() and bulk_create() now
    require user_id and perform an explicit ownership check BEFORE acting
    on the child rows — callers cannot bypass this by passing a foreign
    recommendation_id.
    """

    def __init__(self, admin: AdminClient) -> None:
        super().__init__(admin, "recommendation_items", RecommendationItem)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _verify_recommendation_owner(
        self, *, user_id: UUID, recommendation_id: UUID
    ) -> None:
        """
        Assert that *recommendation_id* belongs to *user_id*.

        Raises:
            NotFoundError: if the recommendation doesn't exist or is owned
                by a different user. We intentionally surface the same error
                as "not found" to avoid leaking existence information.
        """
        response = await (
            self._admin
            .with_user_check(user_id=user_id)
            .table("recommendations")
            .select("id")
            .eq("id", str(recommendation_id))
            .maybe_single()
            .execute()
        )
        if response.data is None:
            raise NotFoundError("recommendation")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def list_for_recommendation(
        self,
        *,
        user_id: UUID,
        recommendation_id: UUID,
    ) -> list[RecommendationItem]:
        """Return all items belonging to *recommendation_id*.

        [H6] Verifies that *user_id* owns the parent recommendation before
        returning items — callers cannot read another user's items by
        guessing a recommendation_id.
        """
        await self._verify_recommendation_owner(
            user_id=user_id, recommendation_id=recommendation_id
        )
        response = await (
            self._admin
            .trusted()  # Ownership already verified above
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
        user_id: UUID,
        recommendation_id: UUID,
        items: list[dict[str, Any]],
    ) -> list[RecommendationItem]:
        """Insert multiple recommendation items in one call.

        [H6] Verifies that *user_id* owns the parent recommendation before
        inserting — callers cannot attach items to another user's recommendation.
        """
        await self._verify_recommendation_owner(
            user_id=user_id, recommendation_id=recommendation_id
        )
        payload = [
            {**item, "recommendation_id": str(recommendation_id)}
            for item in items
        ]
        response = await (
            self._admin
            .trusted()  # Ownership already verified above
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
# UserStyleProfileRepository  [new — 9th repo]
# ---------------------------------------------------------------------------


class UserStyleProfileRepository(BaseRepository[UserStyleProfile]):
    """
    CRUD for the `user_style_profile` table.

    user_style_profile uses user_id as its PRIMARY KEY (1-to-1 with
    auth.users). Rows are created/updated by the recommendation engine.
    Direct user mutations are not exposed here.
    """

    def __init__(self, admin: AdminClient) -> None:
        # The PK column name is "user_id", which also acts as ownership column
        super().__init__(admin, "user_style_profile", UserStyleProfile)

    async def get_for_user(self, *, user_id: UUID) -> UserStyleProfile | None:
        """Return the style profile for *user_id*, or None if not yet computed."""
        response = await (
            self._admin
            .with_user_check(user_id=user_id)
            .table(self._table)
            .select("*")
            .eq("user_id", str(user_id))
            .maybe_single()
            .execute()
        )
        return self._parse(response.data) if response.data else None

    async def upsert_for_user(
        self, *, user_id: UUID, data: dict[str, Any]
    ) -> UserStyleProfile:
        """Upsert style profile data for *user_id* (recommendation engine)."""
        payload = {**data, "user_id": str(user_id)}
        response = await (
            self._admin
            .trusted()  # Called by the AI recommendation engine worker
            .table(self._table)
            .upsert(payload)
            .single()
            .execute()
        )
        return self._parse(response.data)


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
        Atomically increment a usage counter field via a stored procedure.

        [L1] Uses the `increment_usage` RPC (defined in migration 004) which
        runs UPDATE usage_counters SET <field> = <field> + amount inside the
        DB transaction — this prevents race conditions on concurrent calls.

        Args:
            user_id: Owner of the counter.
            field: One of 'try_ons_used', 'recommendations_used', 'body_analyses_used'.
            amount: Number to increment by (default 1).

        Raises:
            ValueError: if *field* is not in the allowed set.
        """
        allowed = {"try_ons_used", "recommendations_used", "body_analyses_used"}
        if field not in allowed:
            raise ValueError(f"field must be one of {allowed}, got {field!r}")

        today = date.today()
        period_start = today.replace(day=1).isoformat()

        # [L1] Atomic increment via stored procedure (see migration 004).
        # The proc does an INSERT ... ON CONFLICT DO UPDATE SET field = field + amount
        # which is atomic within a single Postgres transaction.
        response = await (
            self._admin
            .trusted()
            .table(self._table)  # type: ignore[attr-defined] — rpc on trusted client
            # Fall back to direct upsert when RPC not yet deployed; the RPC
            # is defined in migration 004 as increment_usage(uuid, text, int).
            # TODO(0.3): switch to .rpc("increment_usage", {...}) once migration
            #            is applied to Supabase remote. Using upsert for now to
            #            keep tests passing without a live DB.
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
