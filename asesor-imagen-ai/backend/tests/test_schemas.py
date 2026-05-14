"""
Schema validation tests — Sprint 0.2.

Tests all 7 schema modules to ensure Pydantic v2 validation rules work correctly.
Also covers common response patterns and error schemas.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.body_analysis import BodyAnalysisResponse
from app.schemas.common import ErrorDetail, ErrorResponse, PaginationMeta, SuccessResponse
from app.schemas.profile import ProfileResponse, ProfileUpdateRequest
from app.schemas.recommendation import (
    RecommendationCreateRequest,
    RecommendationFeedbackRequest,
    RecommendationItemResponse,
    RecommendationListResponse,
    RecommendationResponse,
)
from app.schemas.subscription import (
    SubscriptionCreateRequest,
    SubscriptionResponse,
    SubscriptionStatusResponse,
    SubscriptionUpdateRequest,
)
from app.schemas.try_on import (
    TryOnCreateRequest,
    TryOnFeedbackRequest,
    TryOnListResponse,
    TryOnResponse,
)
from app.schemas.wardrobe import (
    WardrobeItemCreateRequest,
    WardrobeItemResponse,
    WardrobeItemUpdateRequest,
)

NOW = datetime.now(timezone.utc)
UID = uuid4()
RID = uuid4()


# ---------------------------------------------------------------------------
# Auth schemas
# ---------------------------------------------------------------------------


class TestAuthSchemas:
    def test_register_request_valid(self):
        r = RegisterRequest(email="test@example.com", password="secret1234")  # 10 chars, 1 digit
        assert r.email == "test@example.com"

    def test_register_request_invalid_email(self):
        with pytest.raises(ValidationError):
            RegisterRequest(email="not-an-email", password="secret")

    def test_login_request_valid(self):
        r = LoginRequest(email="user@mail.com", password="pass")
        assert r.password == "pass"

    def test_token_response_defaults(self):
        r = TokenResponse(
            access_token="abc",
            refresh_token="xyz",
            expires_in=3600,
            user_id=str(UID),
        )
        assert r.token_type == "bearer"

    def test_token_response_custom_type(self):
        r = TokenResponse(
            access_token="a",
            token_type="custom",
            refresh_token="b",
            expires_in=900,
            user_id=str(UID),
        )
        assert r.token_type == "custom"


# ---------------------------------------------------------------------------
# Common schemas
# ---------------------------------------------------------------------------


class TestCommonSchemas:
    def test_pagination_meta_defaults(self):
        p = PaginationMeta()
        assert p.page == 1
        assert p.per_page == 20
        assert p.total == 0

    def test_success_response_with_data(self):
        r = SuccessResponse(data={"key": "value"})
        assert r.success is True
        assert r.data == {"key": "value"}

    def test_success_response_with_pagination(self):
        r = SuccessResponse(
            data=[],
            pagination=PaginationMeta(page=2, per_page=10, total=55, total_pages=6),
        )
        assert r.pagination.page == 2

    def test_error_detail(self):
        e = ErrorDetail(code="NOT_FOUND", message="Not found", fields={"id": "invalid"})
        assert e.code == "NOT_FOUND"
        assert e.fields == {"id": "invalid"}

    def test_error_response(self):
        e = ErrorResponse(error=ErrorDetail(code="ERR", message="oops"))
        assert e.success is False


# ---------------------------------------------------------------------------
# Profile schemas
# ---------------------------------------------------------------------------


class TestProfileSchemas:
    def test_profile_update_all_optional(self):
        r = ProfileUpdateRequest()
        assert r.first_name is None

    def test_profile_update_country_code_max_length(self):
        r = ProfileUpdateRequest(country_code="CO")
        assert r.country_code == "CO"

    def test_profile_update_country_code_too_long(self):
        with pytest.raises(ValidationError):
            ProfileUpdateRequest(country_code="COL")

    def test_profile_response_valid(self):
        r = ProfileResponse(
            id=str(UID),
            preferred_language="es",
            notification_preferences={"push": True, "email": False},
            created_at=NOW.isoformat(),
            updated_at=NOW.isoformat(),
        )
        assert str(r.id) == str(UID)


# ---------------------------------------------------------------------------
# Wardrobe schemas
# ---------------------------------------------------------------------------


class TestWardrobeSchemas:
    def test_create_request_minimal(self):
        r = WardrobeItemCreateRequest(image_url="https://example.com/img.jpg")
        assert str(r.image_url).startswith("https://")

    def test_create_request_with_tags(self):
        r = WardrobeItemCreateRequest(
            image_url="https://img.com/a.jpg",
            user_tags=["casual", "summer"],
        )
        assert len(r.user_tags) == 2

    def test_update_request_all_optional(self):
        r = WardrobeItemUpdateRequest()
        assert r.category is None

    def test_response_valid(self):
        r = WardrobeItemResponse(
            id=str(UID),
            user_id=str(UID),
            image_url="https://img.com/a.jpg",
            created_at=NOW.isoformat(),
            updated_at=NOW.isoformat(),
        )
        assert str(r.user_id) == str(UID)


# ---------------------------------------------------------------------------
# Body Analysis schemas
# ---------------------------------------------------------------------------


class TestBodyAnalysisSchemas:
    def test_response_minimal(self):
        r = BodyAnalysisResponse(
            id=str(UID),
            user_id=str(UID),
            created_at=NOW.isoformat(),
            updated_at=NOW.isoformat(),
        )
        assert r.body_type is None

    def test_response_with_colors(self):
        r = BodyAnalysisResponse(
            id=str(UID),
            user_id=str(UID),
            best_colors=["navy", "burgundy"],
            avoid_colors=["neon"],
            created_at=NOW.isoformat(),
            updated_at=NOW.isoformat(),
        )
        assert "navy" in r.best_colors


# ---------------------------------------------------------------------------
# Recommendation schemas
# ---------------------------------------------------------------------------


class TestRecommendationSchemas:
    def test_create_request_valid(self):
        r = RecommendationCreateRequest(occasion="casual friday")
        assert r.occasion == "casual friday"
        assert r.season is None

    def test_create_request_valid_season(self):
        r = RecommendationCreateRequest(occasion="beach", season="summer")
        assert r.season == "summer"

    def test_create_request_invalid_season(self):
        with pytest.raises(ValidationError):
            RecommendationCreateRequest(occasion="x", season="monsoon")

    def test_create_request_empty_occasion(self):
        with pytest.raises(ValidationError):
            RecommendationCreateRequest(occasion="")

    def test_feedback_request_all_optional(self):
        r = RecommendationFeedbackRequest()
        assert r.liked is None

    def test_feedback_with_values(self):
        r = RecommendationFeedbackRequest(clicked=True, liked=True, tried_on=False)
        assert r.clicked is True

    def test_item_response(self):
        r = RecommendationItemResponse(
            wardrobe_item_id=RID,
            position=1,
            role="top",
        )
        assert r.role == "top"

    def test_item_response_invalid_role(self):
        with pytest.raises(ValidationError):
            RecommendationItemResponse(wardrobe_item_id=RID, role="hat")

    def test_response_valid(self):
        r = RecommendationResponse(
            id=RID,
            user_id=UID,
            occasion="formal",
            clicked=False,
            liked=False,
            tried_on=False,
            created_at=NOW,
        )
        assert r.items == []

    def test_list_response(self):
        item = RecommendationResponse(
            id=RID, user_id=UID, occasion="x",
            clicked=False, liked=False, tried_on=False, created_at=NOW,
        )
        r = RecommendationListResponse(items=[item], total=1, page=1, per_page=20)
        assert r.total == 1


# ---------------------------------------------------------------------------
# TryOn schemas
# ---------------------------------------------------------------------------


class TestTryOnSchemas:
    def test_create_request_valid(self):
        r = TryOnCreateRequest(content_hash="a" * 16)
        assert r.wardrobe_item_id is None

    def test_create_request_hash_too_short(self):
        with pytest.raises(ValidationError):
            TryOnCreateRequest(content_hash="short")

    def test_create_request_with_ids(self):
        r = TryOnCreateRequest(
            wardrobe_item_id=RID,
            body_analysis_id=UID,
            content_hash="a" * 64,
        )
        assert r.wardrobe_item_id == RID

    def test_feedback_request_rating_range(self):
        r = TryOnFeedbackRequest(user_rating=5)
        assert r.user_rating == 5

    def test_feedback_request_rating_out_of_range(self):
        with pytest.raises(ValidationError):
            TryOnFeedbackRequest(user_rating=6)

    def test_feedback_request_invalid_fit_feedback(self):
        with pytest.raises(ValidationError):
            TryOnFeedbackRequest(fit_feedback="bad_fit")

    def test_feedback_valid_enums(self):
        r = TryOnFeedbackRequest(
            fit_feedback="perfect",
            color_feedback="harmonious",
            occasion_fit="just_right",
            would_buy=True,
        )
        assert r.fit_feedback == "perfect"

    def test_response_valid(self):
        r = TryOnResponse(
            id=RID,
            user_id=UID,
            content_hash="a" * 64,
            cache_hit=False,
            status="pending",
            liked=False,
            shared=False,
            created_at=NOW,
            updated_at=NOW,
        )
        assert r.status == "pending"

    def test_list_response(self):
        item = TryOnResponse(
            id=RID, user_id=UID, content_hash="a" * 64,
            cache_hit=False, status="completed", liked=True, shared=False,
            created_at=NOW, updated_at=NOW,
        )
        r = TryOnListResponse(items=[item], total=1, page=1, per_page=20)
        assert r.total == 1


# ---------------------------------------------------------------------------
# Subscription schemas
# ---------------------------------------------------------------------------


class TestSubscriptionSchemas:
    def test_create_request_valid(self):
        r = SubscriptionCreateRequest(
            plan_type="free",
            status="active",
        )
        assert r.plan_type == "free"
        assert r.billing_provider is None

    def test_create_request_invalid_plan(self):
        with pytest.raises(ValidationError):
            SubscriptionCreateRequest(plan_type="premium", status="active")

    def test_create_request_invalid_status(self):
        with pytest.raises(ValidationError):
            SubscriptionCreateRequest(plan_type="free", status="inactive")

    def test_create_request_valid_provider(self):
        r = SubscriptionCreateRequest(
            plan_type="estilo",
            status="trialing",
            billing_provider="stripe",
            amount_cents=999,
            currency="USD",
        )
        assert r.amount_cents == 999

    def test_update_request_all_optional(self):
        r = SubscriptionUpdateRequest()
        assert r.status is None

    def test_update_request_cancel(self):
        r = SubscriptionUpdateRequest(
            status="canceled",
            cancel_at_period_end=True,
            canceled_at=NOW,
        )
        assert r.cancel_at_period_end is True

    def test_response_valid(self):
        r = SubscriptionResponse(
            id=RID,
            user_id=UID,
            plan_type="imagen",
            status="active",
            cancel_at_period_end=False,
            created_at=NOW,
            updated_at=NOW,
        )
        assert r.plan_type == "imagen"

    def test_status_response(self):
        r = SubscriptionStatusResponse(
            plan="free",  # field renamed from plan_type in SubscriptionStatusResponse
            status="active",
            is_active=True,
        )
        assert r.is_active is True

    def test_amount_cents_non_negative(self):
        with pytest.raises(ValidationError):
            SubscriptionCreateRequest(
                plan_type="free",
                status="active",
                amount_cents=-1,
            )
