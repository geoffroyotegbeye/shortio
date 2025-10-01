# app/utils/cartesia_utils.py
import requests
import os
import time
from typing import Dict, Any, Optional
from app.core.config_loader import CARTESIA_ACCESS_TOKEN, CARTESIA_VOICE_ID

def generate_audio_with_cartesia(text: str, lang: str = 'fr') -> Dict[str, Any]:
    """
    Génère de l'audio à partir de texte en utilisant l'API Cartesia TTS.
    """
    print(f"LOG: Génération audio avec Cartesia TTS pour le texte: {text[:50]}...")

    if not CARTESIA_ACCESS_TOKEN or not CARTESIA_VOICE_ID:
        raise Exception("Token d'accès ou ID de voix Cartesia non configuré.")

    url = "https://api.cartesia.ai/tts/bytes"

    headers = {
        "Cartesia-Version": "2024-05-10", # Utiliser une version récente de l'API
        "Authorization": f"Bearer {CARTESIA_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model_id": "sonic-english", # Modèle par défaut, la langue le surchargera
        "transcript": text,
        "voice": {
            "mode": "id",
            "id": CARTESIA_VOICE_ID
        },
        "output_format": {
            "container": "wav", # Utiliser WAV pour une meilleure compatibilité
            "encoding": "pcm_s16le",
            "sample_rate": 24000
        },
        "language": lang
    }

    max_retries = 3
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            print(f"LOG: Tentative {attempt + 1}/{max_retries} d'appel à l'API Cartesia...")
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            print("LOG: Audio généré avec succès via Cartesia TTS")
            # Retourner les données dans un format compatible avec les autres services
            return {"audio_data": response.content}

        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                print(f"LOG: Timeout lors de l'appel à l'API Cartesia. Nouvelle tentative dans {retry_delay} secondes...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                print("LOG: Échec après plusieurs tentatives - Timeout persistant.")
                raise Exception("L'API Cartesia ne répond pas dans le délai imparti.")
        except requests.exceptions.HTTPError as e:
            print(f"LOG: Erreur HTTP lors de l'appel à l'API Cartesia: {e}")
            if e.response.status_code == 401:
                raise Exception("Erreur d'authentification avec l'API Cartesia. Vérifiez votre token.")
            raise
        except Exception as e:
            print(f"LOG: Erreur inattendue lors de l'appel à l'API Cartesia: {e}")
            raise
