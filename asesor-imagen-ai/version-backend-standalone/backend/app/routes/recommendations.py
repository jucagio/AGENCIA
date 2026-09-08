from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from backend.app.security import verify_token
from backend.app.database import SupabaseDB
import logging

router = APIRouter(prefix="/api/v1/recommendations", tags=["recommendations"])
logger = logging.getLogger(__name__)

class ClothingRecommendation(BaseModel):
    category: str
    color: str
    style: str
    reason: str
    confidence: float

class RecommendationResponse(BaseModel):
    analysis_id: str
    recommendations: List[ClothingRecommendation]
    generated_at: str

@router.get("/{analysis_id}", response_model=RecommendationResponse)
async def get_recommendations(
    analysis_id: str,
    user_id: str = Depends(verify_token)
):
    """Get style recommendations based on body analysis"""
    try:
        db = SupabaseDB.get_client()

        # Get the analysis
        analysis_response = db.table("body_analysis").select("*").eq("id", analysis_id).eq("user_id", user_id).single().execute()

        if not analysis_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not found"
            )

        analysis = analysis_response.data
        analysis_json = analysis.get("analysis_json", {})

        # Generate recommendations based on body analysis
        recommendations = generate_style_recommendations(analysis_json)

        return {
            "analysis_id": analysis_id,
            "recommendations": recommendations,
            "generated_at": analysis.get("created_at")
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get recommendations error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate recommendations"
        )

@router.post("/{analysis_id}/save")
async def save_recommendations(
    analysis_id: str,
    recommendations: List[ClothingRecommendation],
    user_id: str = Depends(verify_token)
):
    """Save recommendations for future reference"""
    try:
        db = SupabaseDB.get_client()

        # Store recommendations
        rec_data = {
            "user_id": user_id,
            "analysis_id": analysis_id,
            "recommendations_json": [rec.dict() for rec in recommendations]
        }

        response = db.table("recommendations").insert(rec_data).execute()

        return {
            "status": "saved",
            "count": len(recommendations)
        }

    except Exception as e:
        logger.error(f"Save recommendations error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save recommendations"
        )

@router.get("")
async def list_recommendations(user_id: str = Depends(verify_token)):
    """List all saved recommendations"""
    try:
        db = SupabaseDB.get_client()
        response = db.table("recommendations").select("*").eq("user_id", user_id).execute()

        return {
            "recommendations": response.data,
            "count": len(response.data) if response.data else 0
        }

    except Exception as e:
        logger.error(f"List recommendations error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve recommendations"
        )

def generate_style_recommendations(analysis: dict) -> List[ClothingRecommendation]:
    """
    Generate clothing recommendations based on body analysis.
    This is a template - replace with actual AI logic.
    """
    recommendations = [
        ClothingRecommendation(
            category="tops",
            color="earth_tones",
            style="fitted",
            reason="Complements body proportions",
            confidence=0.85
        ),
        ClothingRecommendation(
            category="bottoms",
            color="neutral",
            style="high_waist",
            reason="Flattering for body shape",
            confidence=0.82
        ),
        ClothingRecommendation(
            category="dresses",
            color="jewel_tones",
            style="wrap_dress",
            reason="Enhances natural features",
            confidence=0.88
        )
    ]

    return recommendations
