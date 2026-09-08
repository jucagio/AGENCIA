from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from backend.app.security import verify_token
from backend.app.database import SupabaseDB
from datetime import datetime
import logging
import json

router = APIRouter(prefix="/api/v1/outfits", tags=["outfits"])
logger = logging.getLogger(__name__)

class OutfitCreateRequest(BaseModel):
    clothes_ids: List[str]
    occasion: str = "casual"
    notes: str = None

class OutfitResponse(BaseModel):
    id: str
    user_id: str
    clothes_count: int
    occasion: str
    created_at: str

@router.post("")
async def create_outfit(
    request: OutfitCreateRequest,
    user_id: str = Depends(verify_token)
):
    """Create a new outfit from clothing items"""
    try:
        db = SupabaseDB.get_client()

        outfit_data = {
            "user_id": user_id,
            "clothes_ids_json": request.clothes_ids,
            "occasion": request.occasion,
            "notes": request.notes
        }

        response = db.table("outfits").insert(outfit_data).execute()

        if response.data:
            return {
                "status": "created",
                "outfit_id": response.data[0].get("id"),
                "clothes_count": len(request.clothes_ids)
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create outfit"
            )

    except Exception as e:
        logger.error(f"Create outfit error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create outfit"
        )

@router.get("/{outfit_id}")
async def get_outfit(
    outfit_id: str,
    user_id: str = Depends(verify_token)
):
    """Get outfit details"""
    try:
        db = SupabaseDB.get_client()

        response = db.table("outfits").select("*").eq("id", outfit_id).eq("user_id", user_id).single().execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Outfit not found"
            )

        outfit = response.data
        clothes_ids = outfit.get("clothes_ids_json", [])

        # Get clothing details
        clothes = []
        if clothes_ids:
            clothes_response = db.table("clothes").select("*").in_("id", clothes_ids).execute()
            clothes = clothes_response.data if clothes_response.data else []

        return {
            "outfit": outfit,
            "clothes": clothes,
            "clothes_count": len(clothes_ids)
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get outfit error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve outfit"
        )

@router.get("")
async def list_outfits(user_id: str = Depends(verify_token)):
    """List all outfits for user"""
    try:
        db = SupabaseDB.get_client()

        response = db.table("outfits").select("*").eq("user_id", user_id).execute()

        return {
            "outfits": response.data,
            "count": len(response.data) if response.data else 0
        }

    except Exception as e:
        logger.error(f"List outfits error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve outfits"
        )

@router.put("/{outfit_id}")
async def update_outfit(
    outfit_id: str,
    request: OutfitCreateRequest,
    user_id: str = Depends(verify_token)
):
    """Update an outfit"""
    try:
        db = SupabaseDB.get_client()

        update_data = {
            "clothes_ids_json": request.clothes_ids,
            "occasion": request.occasion,
            "notes": request.notes
        }

        response = db.table("outfits").update(update_data).eq("id", outfit_id).eq("user_id", user_id).execute()

        return {
            "status": "updated",
            "outfit_id": outfit_id
        }

    except Exception as e:
        logger.error(f"Update outfit error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update outfit"
        )

@router.delete("/{outfit_id}")
async def delete_outfit(
    outfit_id: str,
    user_id: str = Depends(verify_token)
):
    """Delete an outfit"""
    try:
        db = SupabaseDB.get_client()

        response = db.table("outfits").delete().eq("id", outfit_id).eq("user_id", user_id).execute()

        return {"status": "deleted"}

    except Exception as e:
        logger.error(f"Delete outfit error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete outfit"
        )
