# app/api/endpoints.py
from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import VideoRequest, VideoResponse
from app.core.tiktok_generator import make_tiktok_from_prompt
import os

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "API is running"}

@router.post("/generate-video", response_model=VideoResponse)
async def generate_video(request: VideoRequest, http_request: Request):
    print("LOG: Début du processus de génération de vidéo.")
    try:
        video_path = make_tiktok_from_prompt(
            prompt=request.prompt,
            n_images=request.n_images,
            category=request.category,
            lang=request.lang,
            tone=request.tone,
            tts_service=request.tts_service
        )
        print("LOG: Vidéo générée avec succès.")

        # Construire l'URL complète de la vidéo
        base_url = str(http_request.base_url)
        video_filename = os.path.basename(video_path)
        # Assurez-vous que l'URL est correctement formée
        video_url = f"{base_url.rstrip('/')}/videos/{video_filename}"
        
        print(f"LOG: URL de la vidéo retournée au frontend : {video_url}")
        return VideoResponse(video_url=video_url)
    except Exception as e:
        print(f"LOG: Erreur critique - {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de la vidéo : {str(e)}")