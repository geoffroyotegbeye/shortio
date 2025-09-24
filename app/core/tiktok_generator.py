# app/core/tiktok_generator.py
import time
import os
from app.core.configs import OUTPUT_DIR, FPS
from app.utils.llm_utils import generate_script_with_openai
from app.utils.elevenlabs_utils import generate_audio_with_timing
from app.utils.video_search_utils import search_pexels_video
from app.utils.video_utils import make_video_from_assets
import random
import re

def make_tiktok_from_prompt(prompt, n_images=3, category="astuce", lang="fr", tone="percutant"):
    timestamp = int(time.time())
    base_name = f"tiktok_{timestamp}"
    
    # 1. Générer le script avec l'IA
    script = generate_script_with_openai(prompt=prompt, tone=tone)
    
    # 2. Chercher une vidéo de fond illustrant le script
    video_query = re.sub(r'[^\w\s]', '', script).split()[:5]
    video_query = " ".join(video_query)
    background_video_url = search_pexels_video(query=video_query)
    
    if not background_video_url:
        raise Exception("Impossible de trouver une vidéo de fond.")
    
    # 3. Générer l'audio avec ElevenLabs
    audio_data = generate_audio_with_timing(text=script)
    audio_path = os.path.join(OUTPUT_DIR, f"{base_name}.mp3")
    # Sauvegarde du fichier audio
    with open(audio_path, 'wb') as f:
        for chunk in audio_data['audio_stream']:
            f.write(chunk)
    
    # 4. Monter la vidéo
    out_video = os.path.join(OUTPUT_DIR, f"{base_name}.mp4")
    # Note: Il faut modifier make_video_from_assets pour gérer la vidéo de fond et les sous-titres
    make_video_from_assets(
        background_video_url=background_video_url,
        audio_path=audio_path,
        timing_data={}, # Nous n'avons pas encore cette data, nous pouvons la simuler
        out_video=out_video
    )
    
    return out_video