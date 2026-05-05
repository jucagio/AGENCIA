from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class BodyAnalysisResponse(BaseModel):
    id: str
    user_id: str
    image_url: Optional[str] = None
    body_type: Optional[str] = None
    skin_tone_category: Optional[str] = None
    color_season: Optional[str] = None
    best_colors: Optional[List[str]] = None
    avoid_colors: Optional[List[str]] = None
    created_at: str
    updated_at: str
