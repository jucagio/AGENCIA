"""
API v1 Router — aggregates all endpoint routers.

Sprint 0.3: all 8 endpoint modules wired up.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    body_analysis,
    recommendations,
    subscriptions,
    try_ons,
    users,
    wardrobe,
    webhooks,
)

api_v1_router = APIRouter()

api_v1_router.include_router(auth.router,            prefix="/auth",            tags=["Auth"])
api_v1_router.include_router(users.router,           prefix="/users",           tags=["Users"])
api_v1_router.include_router(wardrobe.router,        prefix="/wardrobe",        tags=["Wardrobe"])
api_v1_router.include_router(body_analysis.router,   prefix="/body-analysis",   tags=["Body Analysis"])
api_v1_router.include_router(try_ons.router,         prefix="/try-ons",         tags=["Try-On"])
api_v1_router.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
api_v1_router.include_router(subscriptions.router,   prefix="/subscriptions",   tags=["Subscriptions"])
api_v1_router.include_router(webhooks.router,        prefix="/webhooks",        tags=["Webhooks"])
