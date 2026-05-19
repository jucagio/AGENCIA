"""
Wardrobe service — wardrobe item CRUD with Supabase Storage upload stub.
"""

from __future__ import annotations

import logging
from uuid import UUID

from app.core.admin_client import AdminClient
from app.models.wardrobe import WardrobeItem
from app.repositories.repos import WardrobeRepository
from app.schemas.wardrobe import WardrobeItemCreateRequest, WardrobeItemUpdateRequest

logger = logging.getLogger(__name__)


class WardrobeService:
    """Wardrobe item management."""

    def __init__(self, admin: AdminClient) -> None:
        self._repo = WardrobeRepository(admin)

    async def list_items(
        self,
        *,
        user_id: UUID,
        page: int = 1,
        size: int = 20,
        category: str | None = None,
    ) -> tuple[list[WardrobeItem], int]:
        """Return paginated wardrobe items for user_id."""
        return await self._repo.list_active(
            user_id=user_id,
            page=page,
            per_page=size,
            category=category,
        )

    async def get_item(self, *, user_id: UUID, item_id: UUID) -> WardrobeItem:
        """Return a single wardrobe item owned by user_id."""
        return await self._repo.get_by_id(user_id=user_id, record_id=item_id)

    async def create_item(
        self,
        *,
        user_id: UUID,
        data: WardrobeItemCreateRequest,
        image_bytes: bytes | None = None,
    ) -> WardrobeItem:
        """
        Create a wardrobe item and optionally upload image to Supabase Storage.

        Image upload is a stub in Sprint 0.3 — stores the URL directly.
        Sprint 0.5: replace with real Supabase Storage + R2 CDN pipeline.
        """
        payload = data.model_dump(exclude_unset=True)

        # TODO(Sprint 0.5): upload image_bytes to Supabase Storage → set storage_path + image_url
        if image_bytes:
            logger.debug("Image upload stub: %d bytes (Sprint 0.5 will implement)", len(image_bytes))

        item = await self._repo.create(user_id=user_id, data=payload)

        # Enqueue vision_worker for auto-tagging
        from arq import create_pool  # noqa: PLC0415
        from arq.connections import RedisSettings  # noqa: PLC0415

        from app.config import get_settings  # noqa: PLC0415

        settings = get_settings()
        pool = await create_pool(RedisSettings.from_dsn(settings.REDIS_URL))
        await pool.enqueue_job("vision_tag_wardrobe", str(item.id), item.image_url)

        return item

    async def update_item(
        self,
        *,
        user_id: UUID,
        item_id: UUID,
        update: WardrobeItemUpdateRequest,
    ) -> WardrobeItem:
        """Update wardrobe item fields."""
        data = update.model_dump(exclude_unset=True)
        return await self._repo.update(user_id=user_id, record_id=item_id, data=data)

    async def delete_item(self, *, user_id: UUID, item_id: UUID) -> None:
        """Soft-delete a wardrobe item (sets deleted_at)."""
        from datetime import datetime, timezone  # noqa: PLC0415

        await self._repo.update(
            user_id=user_id,
            record_id=item_id,
            data={"deleted_at": datetime.now(timezone.utc).isoformat()},
        )
