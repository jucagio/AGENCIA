from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from backend.app.security import verify_token
from backend.app.database import SupabaseDB
from datetime import datetime
import logging

router = APIRouter(prefix="/api/v1/wardrobe", tags=["wardrobe"])
logger = logging.getLogger(__name__)

class ClothingItem(BaseModel):
    image_url: str
    category: str
    color: str
    size: str
    brand: Optional[str] = None
    notes: Optional[str] = None

class WardrobeResponse(BaseModel):
    id: str
    items_count: int
    created_at: str

@router.post("/create")
async def create_wardrobe(user_id: str = Depends(verify_token)):
    """Create a new wardrobe for user"""
    try:
        db = SupabaseDB.get_client()

        wardrobe_data = {
            "user_id": user_id
        }

        response = db.table("wardrobe").insert(wardrobe_data).execute()

        if response.data:
            return {
                "status": "created",
                "wardrobe_id": response.data[0].get("id")
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create wardrobe"
            )

    except Exception as e:
        logger.error(f"Create wardrobe error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create wardrobe"
        )

@router.post("/{wardrobe_id}/add-item")
async def add_clothing_item(
    wardrobe_id: str,
    file: UploadFile = File(...),
    category: str = None,
    color: str = None,
    size: str = None,
    user_id: str = Depends(verify_token)
):
    """Add a clothing item to wardrobe"""
    try:
        # Validate file
        if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image format"
            )

        # Read file
        content = await file.read()

        # Upload to Supabase Storage
        db = SupabaseDB.get_client()
        timestamp = datetime.now().isoformat()
        file_path = f"{user_id}/wardrobe/{timestamp}_{file.filename}"

        db.storage.from_("wardrobe-images").upload(
            path=file_path,
            file=content
        )

        # Get public URL
        image_url = db.storage.from_("wardrobe-images").get_public_url(file_path)

        # Store item metadata
        item_data = {
            "wardrobe_id": wardrobe_id,
            "image_url": image_url,
            "category": category or "other",
            "color": color or "unknown",
            "size": size or "one_size"
        }

        response = db.table("clothes").insert(item_data).execute()

        return {
            "status": "added",
            "item_id": response.data[0].get("id") if response.data else None,
            "image_url": image_url
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Add clothing item error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add clothing item"
        )

@router.get("/{wardrobe_id}/items")
async def get_wardrobe_items(
    wardrobe_id: str,
    user_id: str = Depends(verify_token)
):
    """Get all items in a wardrobe"""
    try:
        db = SupabaseDB.get_client()

        # Verify wardrobe belongs to user
        wardrobe_check = db.table("wardrobe").select("*").eq("id", wardrobe_id).eq("user_id", user_id).single().execute()

        if not wardrobe_check.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wardrobe not found"
            )

        # Get items
        response = db.table("clothes").select("*").eq("wardrobe_id", wardrobe_id).execute()

        return {
            "wardrobe_id": wardrobe_id,
            "items": response.data,
            "count": len(response.data) if response.data else 0
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get wardrobe items error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve wardrobe items"
        )

@router.delete("/items/{item_id}")
async def delete_clothing_item(
    item_id: str,
    user_id: str = Depends(verify_token)
):
    """Delete a clothing item"""
    try:
        db = SupabaseDB.get_client()

        response = db.table("clothes").delete().eq("id", item_id).execute()

        return {"status": "deleted"}

    except Exception as e:
        logger.error(f"Delete item error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item"
        )

@router.get("")
async def list_wardrobes(user_id: str = Depends(verify_token)):
    """List all wardrobes for user"""
    try:
        db = SupabaseDB.get_client()
        response = db.table("wardrobe").select("*").eq("user_id", user_id).execute()

        return {
            "wardrobes": response.data,
            "count": len(response.data) if response.data else 0
        }

    except Exception as e:
        logger.error(f"List wardrobes error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve wardrobes"
        )
