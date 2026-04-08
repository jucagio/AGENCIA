"""Supabase client initialization and helper functions.

Provides a singleton client and typed helper functions so that
routers never construct raw queries -- all DB access goes through here.
"""

from functools import lru_cache
from typing import Any

from supabase import create_client, Client

from app.config import settings


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    """Return a cached Supabase client instance.

    Uses the anon key by default, which respects RLS policies.
    For admin operations, use get_supabase_admin_client().
    """
    if not settings.supabase_url or not settings.supabase_key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_KEY must be set in environment variables"
        )
    return create_client(settings.supabase_url, settings.supabase_key)


@lru_cache(maxsize=1)
def get_supabase_admin_client() -> Client:
    """Return a cached Supabase client with service role key.

    Bypasses RLS -- use only for admin operations like user profile
    creation during registration.
    """
    if not settings.supabase_url or not settings.supabase_service_role_key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set"
        )
    return create_client(settings.supabase_url, settings.supabase_service_role_key)


# ---------------------------------------------------------------------------
# Query helpers -- thin wrappers to keep routers clean
# ---------------------------------------------------------------------------

def fetch_signs_paginated(
    page: int = 1,
    page_size: int = 20,
    language_code: str = "co-csn",
) -> dict[str, Any]:
    """Fetch a paginated list of signs.

    Returns dict with 'data' list and 'count' total.
    """
    client = get_supabase_client()
    offset = (page - 1) * page_size

    # Get total count
    count_response = (
        client.table("signs")
        .select("id", count="exact")
        .eq("language_code", language_code)
        .execute()
    )
    total = count_response.count or 0

    # Get page
    data_response = (
        client.table("signs")
        .select("id, word, video_url, description, difficulty, language_code, created_at")
        .eq("language_code", language_code)
        .order("word")
        .range(offset, offset + page_size - 1)
        .execute()
    )

    return {"data": data_response.data, "count": total}


def search_signs(query: str, language_code: str = "co-csn") -> list[dict]:
    """Search signs by word using case-insensitive partial match."""
    client = get_supabase_client()
    response = (
        client.table("signs")
        .select("id, word, video_url, description, difficulty, language_code")
        .eq("language_code", language_code)
        .ilike("word", f"%{query}%")
        .order("word")
        .limit(50)
        .execute()
    )
    return response.data


def fetch_sign_by_id(sign_id: str) -> dict | None:
    """Fetch a single sign by its UUID, including related videos."""
    client = get_supabase_client()
    response = (
        client.table("signs")
        .select("id, word, video_url, description, difficulty, language_code, created_at, videos(id, url, duration_seconds, format)")
        .eq("id", sign_id)
        .maybe_single()
        .execute()
    )
    return response.data


def fetch_signs_by_words(words: list[str], language_code: str = "co-csn") -> list[dict]:
    """Fetch signs matching a list of words (for translation)."""
    if not words:
        return []
    client = get_supabase_client()
    # Supabase .in_() expects the column and a list of values
    lower_words = [w.lower() for w in words]
    response = (
        client.table("signs")
        .select("id, word, video_url, description, difficulty")
        .eq("language_code", language_code)
        .in_("word", lower_words)
        .execute()
    )
    return response.data


def fetch_user_favorites(user_id: str) -> list[dict]:
    """Fetch all favorites for a user, joining sign data."""
    client = get_supabase_client()
    response = (
        client.table("favorites")
        .select("id, created_at, signs(id, word, video_url, description, difficulty)")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return response.data


def add_favorite(user_id: str, sign_id: str) -> dict:
    """Add a sign to user favorites. Returns the created record."""
    client = get_supabase_client()
    response = (
        client.table("favorites")
        .insert({"user_id": user_id, "sign_id": sign_id})
        .execute()
    )
    return response.data[0] if response.data else {}


def remove_favorite(user_id: str, sign_id: str) -> bool:
    """Remove a sign from user favorites. Returns True if deleted."""
    client = get_supabase_client()
    response = (
        client.table("favorites")
        .delete()
        .eq("user_id", user_id)
        .eq("sign_id", sign_id)
        .execute()
    )
    return len(response.data) > 0


def fetch_user_profile(user_id: str) -> dict | None:
    """Fetch user profile by auth user ID."""
    client = get_supabase_client()
    response = (
        client.table("user_profiles")
        .select("id, display_name, avatar_url, preferred_language, created_at, updated_at")
        .eq("id", user_id)
        .maybe_single()
        .execute()
    )
    return response.data


def create_user_profile(user_id: str, display_name: str) -> dict:
    """Create a user profile after registration."""
    admin = get_supabase_admin_client()
    response = (
        admin.table("user_profiles")
        .insert({
            "id": user_id,
            "display_name": display_name,
            "preferred_language": "co-csn",
        })
        .execute()
    )
    return response.data[0] if response.data else {}


def log_translation(user_id: str, input_text: str, signs_matched: list[str]) -> dict:
    """Log a translation request for analytics."""
    client = get_supabase_client()
    response = (
        client.table("translations")
        .insert({
            "user_id": user_id,
            "input_text": input_text,
            "signs_matched": signs_matched,
        })
        .execute()
    )
    return response.data[0] if response.data else {}
