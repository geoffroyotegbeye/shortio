# app/utils/elevenlabs_utils.py
from elevenlabs import generate
from app.core.secrets import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID
from typing import Dict, Any

def generate_audio_with_timing(text: str) -> Dict[str, Any]:
    """
    Génère de l'audio avec ElevenLabs et retourne le stream audio.
    Les données de timing ne sont pas fournies par la bibliothèque en streaming.
    """
    audio_stream = generate(
        text=text,
        voice=ELEVENLABS_VOICE_ID,
        api_key=ELEVENLABS_API_KEY,
        model="eleven_multilingual_v2",
        stream=True
    )
    
    return {"audio_stream": audio_stream}