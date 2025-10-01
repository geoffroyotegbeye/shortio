# app/api/endpoints.py
from fastapi import APIRouter, HTTPException, Request, UploadFile, File
import shutil
from app.models.schemas import VideoRequest, VideoResponse
from app.core.tiktok_generator import make_tiktok_from_prompt
from app.core.subtitle_generator import process_video_for_subtitles
from app.core.configs import TEMP_DIR
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
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add-subtitles", response_model=VideoResponse)
async def add_subtitles_to_video(request: Request, video_file: UploadFile = File(...)):
    """
    Accepte une vidéo, extrait l'audio, le transcrit, et incruste les sous-titres.
    """
    temp_video_path = ""
    try:
        # Sauvegarder la vidéo uploadée temporairement
        os.makedirs(TEMP_DIR, exist_ok=True)
        temp_video_path = os.path.join(TEMP_DIR, video_file.filename)
        with open(temp_video_path, "wb") as buffer:
            shutil.copyfileobj(video_file.file, buffer)
        
        print(f"LOG: Vidéo uploadée sauvegardée temporairement à {temp_video_path}")

        # Lancer le processus de sous-titrage
        final_video_path = process_video_for_subtitles(
            video_path=temp_video_path,
            original_filename=video_file.filename
        )

        # Construire l'URL de la vidéo finale
        base_url = str(request.base_url)
        video_url = f"{base_url}videos/{os.path.basename(final_video_path)}"
        print(f"LOG: URL de la vidéo avec sous-titres : {video_url}")

        return VideoResponse(video_url=video_url)

    except Exception as e:
        print(f"LOG: Erreur critique lors de l'ajout de sous-titres: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Nettoyer la vidéo temporaire uploadée
        if temp_video_path and os.path.exists(temp_video_path):
            try:
                os.remove(temp_video_path)
                print(f"LOG: Vidéo temporaire uploadée supprimée : {temp_video_path}")
            except Exception as e:
                print(f"LOG: Erreur lors de la suppression de la vidéo temporaire {temp_video_path}: {e}")