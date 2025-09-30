# app/utils/elevenlabs_utils.py
import requests
import time
import base64
from app.core.config_loader import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID
from typing import Dict, Any

def generate_audio_with_timing(text: str) -> Dict[str, Any]:
    """
    Génère de l'audio avec ElevenLabs et retourne l'audio ainsi que les données de synchronisation.
    """
    print("LOG: Appel de l'API ElevenLabs pour la génération audio avec synchronisation...")
    
    api_key = ELEVENLABS_API_KEY.strip()
    voice_id = ELEVENLABS_VOICE_ID.strip()
    
    # Nouvel endpoint pour obtenir les timestamps
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"

    headers = {
        "xi-api-key": api_key,
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

    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            print(f"LOG: Tentative {attempt + 1}/{max_retries} d'appel à l'API ElevenLabs...")
            # Pas de streaming ici, on attend la réponse complète
            response = requests.post(
                url,
                headers=headers,
                json=json_data,
                timeout=60  # Timeout augmenté car la réponse peut être plus longue
            )
            
            response.raise_for_status()
            print("LOG: Réponse JSON reçue avec succès.")
            
            response_json = response.json()
            audio_base64 = response_json.get("audio_base64")
            alignment_data = response_json.get("alignment")

            if not audio_base64 or not alignment_data:
                raise Exception("La réponse de l'API est incomplète (audio ou alignment manquant).")

            # Décoder l'audio depuis le Base64
            audio_data = base64.b64decode(audio_base64)
            
            return {
                "audio_data": audio_data,
                "timing_data": alignment_data
            }
            
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                print(f"LOG: Timeout lors de l'appel à l'API ElevenLabs. Nouvelle tentative dans {retry_delay} secondes...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Backoff exponentiel
            else:
                print("LOG: Échec après plusieurs tentatives - Timeout persistant.")
                raise Exception("L'API ElevenLabs ne répond pas dans le délai imparti après plusieurs tentatives.")
        except requests.exceptions.HTTPError as e:
            print(f"LOG: Erreur HTTP lors de l'appel à l'API ElevenLabs: {str(e)}")
            if e.response.status_code == 401:
                raise Exception("Erreur d'authentification avec l'API ElevenLabs. Vérifiez votre clé API.")
            # Essayer de lire le corps de la réponse pour plus de détails
            try:
                error_details = e.response.json()
                print(f"LOG: Détails de l'erreur : {error_details}")
            except:
                pass
            raise
        except Exception as e:
            print(f"LOG: Erreur inattendue lors de l'appel à l'API ElevenLabs: {str(e)}")
            raise