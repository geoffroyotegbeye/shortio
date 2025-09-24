# app/models/schemas.py
from pydantic import BaseModel, Field
from typing import Optional

class VideoRequest(BaseModel):
    prompt: str = Field(..., example="Une astuce pour mémoriser des noms")
    tone: str = Field("percutant", example="percutant")
    n_images: int = Field(3, ge=1, le=5, example=3)
    category: str = Field("astuce", example="astuce")
    lang: str = Field("fr", example="fr")

class VideoResponse(BaseModel):
    video_path: str = Field(..., example="/output/tiktok_1234567890.mp4")