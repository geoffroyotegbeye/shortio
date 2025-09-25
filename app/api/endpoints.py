# app/api/endpoints.py
from fastapi import APIRouter, HTTPException
from app.models.schemas import VideoRequest, VideoResponse
from app.core.tiktok_generator import make_tiktok_from_prompt
import os

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "API is running"}

@router.post("/generate-video", response_model=VideoResponse)
async def generate_video(request: VideoRequest):
    print("LOG: Début du processus de génération de vidéo.")
    try:
        video_path = make_tiktok_from_prompt(
            prompt=request.prompt,
            n_images=request.n_images,
            category=request.category,
            lang=request.lang,
            tone=request.tone
        )
        print("LOG: Vidéo générée avec succès.")
        return VideoResponse(video_path=video_path)
    except Exception as e:
        print(f"LOG: Erreur critique - {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de la vidéo : {str(e)}")