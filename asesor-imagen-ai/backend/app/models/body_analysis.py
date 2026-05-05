from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class BodyAnalysisBase(BaseModel):
    image_url: Optional[str] = None
    storage_path: Optional[str] = None
    
    body_type: Optional[str] = Field(None, pattern="^(apple|pear|hourglass|rectangle|inverted_triangle)$")
    skin_tone_category: Optional[str] = Field(None, pattern="^(warm|cool|neutral)$")
    color_season: Optional[str] = Field(None, pattern="^(spring|summer|autumn|winter)$")
    
    detected_colors: Optional[Dict[str, Any]] = None
    best_colors: Optional[List[str]] = None
    avoid_colors: Optional[List[str]] = None
    
    shoulder_width_cm: Optional[int] = None
    bust_cm: Optional[int] = None
    waist_cm: Optional[int] = None
    hip_cm: Optional[int] = None
    inseam_cm: Optional[int] = None
    
    notes: Optional[str] = None
    vision_api_response: Optional[Dict[str, Any]] = None

class BodyAnalysisCreate(BodyAnalysisBase):
    pass

class BodyAnalysisUpdate(BaseModel):
    image_url: Optional[str] = None
    storage_path: Optional[str] = None
    body_type: Optional[str] = Field(None, pattern="^(apple|pear|hourglass|rectangle|inverted_triangle)$")
    skin_tone_category: Optional[str] = Field(None, pattern="^(warm|cool|neutral)$")
    color_season: Optional[str] = Field(None, pattern="^(spring|summer|autumn|winter)$")
    detected_colors: Optional[Dict[str, Any]] = None
    best_colors: Optional[List[str]] = None
    avoid_colors: Optional[List[str]] = None
    shoulder_width_cm: Optional[int] = None
    bust_cm: Optional[int] = None
    waist_cm: Optional[int] = None
    hip_cm: Optional[int] = None
    inseam_cm: Optional[int] = None
    notes: Optional[str] = None

class BodyAnalysis(BodyAnalysisBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
