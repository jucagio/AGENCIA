from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from pydantic import BaseModel
from backend.app.security import verify_token
from backend.app.database import create_analysis, get_body_analysis, SupabaseDB
from backend.app.config import settings
import logging
import json
from datetime import datetime
import httpx

router = APIRouter(prefix="/api/v1/body-analysis", tags=["body-analysis"])
logger = logging.getLogger(__name__)

class AnalysisResponse(BaseModel):
    id: str
    user_id: str
    analysis_json: dict
    created_at: str

@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    user_id: str = Depends(verify_token)
):
    """Upload and analyze body image using Supabase AI"""
    try:
        # Validate file type
        if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image format. Use JPEG, PNG, or WebP"
            )

        # Read file content
        content = await file.read()

        # Store image in Supabase Storage
        db = SupabaseDB.get_client()
        timestamp = datetime.now().isoformat()
        file_path = f"{user_id}/{timestamp}_{file.filename}"

        # Upload to Supabase bucket
        response = db.storage.from_("body-images").upload(
            path=file_path,
            file=content
        )

        # Get public URL
        image_url = db.storage.from_("body-images").get_public_url(file_path)

        # Call Supabase AI API (via Edge Function or direct API)
        # This placeholder will be replaced with actual Supabase AI integration
        analysis_result = await call_supabase_ai(image_url, content)

        # Store analysis in database
        analysis_data = {
            "image_url": image_url,
            "analysis": analysis_result,
            "uploaded_at": timestamp
        }

        analysis = await create_analysis(user_id, analysis_data)

        return {
            "status": "success",
            "analysis_id": analysis[0].get("id") if analysis else None,
            "image_url": image_url,
            "analysis": analysis_result
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Body analysis error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze image: {str(e)}"
        )

@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: str,
    user_id: str = Depends(verify_token)
):
    """Get specific body analysis"""
    try:
        db = SupabaseDB.get_client()
        response = db.table("body_analysis").select("*").eq("id", analysis_id).eq("user_id", user_id).single().execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not found"
            )

        return response.data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get analysis error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve analysis"
        )

@router.get("")
async def list_analyses(user_id: str = Depends(verify_token)):
    """List all body analyses for user"""
    try:
        db = SupabaseDB.get_client()
        response = db.table("body_analysis").select("*").eq("user_id", user_id).execute()

        return {
            "analyses": response.data,
            "count": len(response.data) if response.data else 0
        }
    except Exception as e:
        logger.error(f"List analyses error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve analyses"
        )

async def call_supabase_ai(image_url: str, image_content: bytes) -> dict:
    """
    Call Supabase AI API to analyze body image.
    Placeholder for Supabase AI integration.
    Replace with actual API endpoint and credentials from env vars.
    """
    try:
        # This is a placeholder - replace with actual Supabase AI API endpoint
        # SUPABASE_AI_ENDPOINT = os.getenv("SUPABASE_AI_ENDPOINT")
        # The endpoint should analyze:
        # - Body shape/type
        # - Proportions
        # - Skin tone
        # - Style recommendations

        analysis_result = {
            "body_shape": "waiting_for_ai_analysis",
            "proportions": {},
            "skin_tone": "waiting_for_ai_analysis",
            "recommendations": [],
            "confidence": 0
        }

        logger.info(f"AI analysis pending for image: {image_url}")
        return analysis_result

    except Exception as e:
        logger.error(f"Supabase AI call error: {str(e)}")
        raise
