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
    print("LOG: Étape 1 - Génération du script par OpenAI...")
    script = generate_script_with_openai(prompt=prompt, tone=tone)
    print(f"LOG: Script généré : {script}")

    # 2. Chercher une vidéo de fond illustrant le script
    print("LOG: Étape 2 - Recherche d'une vidéo de fond sur Pexels...")
    video_query = re.sub(r'[^\w\s]', '', script).split()[:5]
    video_query = " ".join(video_query)
    background_video_url = search_pexels_video(query=video_query)

    if not background_video_url:
        print("LOG: Impossible de trouver une vidéo de fond.")
        raise Exception("Impossible de trouver une vidéo de fond.")
    print(f"LOG: Vidéo de fond trouvée : {background_video_url}")

    # 3. Générer l'audio avec ElevenLabs
    print("LOG: Étape 3 - Génération de l'audio avec ElevenLabs...")
    audio_data = generate_audio_with_timing(text=script)
    audio_path = os.path.join(OUTPUT_DIR, f"{base_name}.mp3")
    # Sauvegarde du fichier audio
    with open(audio_path, 'wb') as f:
        for chunk in audio_data['audio_stream']:
            f.write(chunk)
    print(f"LOG: Audio généré et sauvegardé : {audio_path}")

    # 4. Monter la vidéo
    print("LOG: Étape 4 - Montage de la vidéo...")
    out_video = os.path.join(OUTPUT_DIR, f"{base_name}.mp4")
    make_video_from_assets(
        background_video_url=background_video_url,
        audio_path=audio_path,
        timing_data={},
        out_video=out_video
    )
    print("LOG: Montage terminé.")

    return out_video