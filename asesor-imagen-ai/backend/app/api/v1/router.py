"""
API v1 Router — aggregates all endpoint routers.

New endpoint modules are added here as the project grows.
Sprint 0: no feature endpoints, just the router shell.
"""

from fastapi import APIRouter

api_v1_router = APIRouter()


# ---------------------------------------------------------------------------
# Future sprint routers will be included here:
#
# from app.api.v1.endpoints import auth, users, wardrobe, analysis,
#                                   tryons, recommendations, subscriptions
#
# api_v1_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
# api_v1_router.include_router(users.router, prefix="/users", tags=["Users"])
# api_v1_router.include_router(wardrobe.router, prefix="/wardrobe", tags=["Wardrobe"])
# api_v1_router.include_router(analysis.router, prefix="/analysis", tags=["Body Analysis"])
# api_v1_router.include_router(tryons.router, prefix="/tryons", tags=["Virtual Try-On"])
# api_v1_router.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
# api_v1_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"])
# ---------------------------------------------------------------------------
