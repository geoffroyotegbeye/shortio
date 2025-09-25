# app/utils/elevenlabs_utils.py
import requests
from app.core.secrets import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID
from typing import Dict, Any

def generate_audio_with_timing(text: str) -> Dict[str, Any]:
    """
    Génère de l'audio avec ElevenLabs en utilisant l'API REST via requests.
    Retourne le stream audio de la réponse.
    """
    print("LOG: Appel de l'API ElevenLabs pour la génération audio via requests...")

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    
    json_data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}?output_format=mp3_44100_128",
        headers=headers,
        json=json_data,
        stream=True
    )

    response.raise_for_status()
    print("LOG: Stream audio reçu.")

    # La réponse de requests est déjà un stream, il suffit de la retourner
    return {"audio_stream": response.iter_content(chunk_size=4096)}