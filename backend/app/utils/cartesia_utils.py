# app/utils/cartesia_utils.py
import requests
import os
import time
from typing import Dict, Any, Optional
from app.core.config_loader import CARTESIA_ACCESS_TOKEN, CARTESIA_VOICE_ID

class CartesiaTTS:
    """Classe pour interagir avec l'API Cartesia TTS."""
    
    def __init__(self, access_token: str = None, voice_id: str = None):
        """
        Initialise le client Cartesia TTS.
        
        Args:
            access_token: Token d'accès Cartesia. Si non fourni, tentera de le récupérer depuis les variables d'environnement.
            voice_id: ID de la voix Cartesia. Si non fourni, tentera de le récupérer depuis les variables d'environnement.
        """
        self.access_token = access_token or CARTESIA_ACCESS_TOKEN
        self.voice_id = voice_id or CARTESIA_VOICE_ID
        self.api_url = "https://api.cartesia.ai/tts/bytes"
        
        if not self.access_token:
            print("ATTENTION: Token d'accès Cartesia non configuré")
    
    def generate_audio(self, text: str, voice_id: str = None, language: str = "fr-FR") -> Dict[str, Any]:
        """
        Génère de l'audio à partir de texte en utilisant l'API Cartesia TTS.
        
        Args:
            text: Le texte à convertir en audio
            voice_id: L'ID de la voix à utiliser (optionnel)
            language: Le code de langue (par défaut: fr-FR)
            
        Returns:
            Un dictionnaire contenant le flux audio et les métadonnées
        """
        print(f"LOG: Génération audio avec Cartesia TTS pour le texte: {text[:50]}...")
        
        # Utiliser la voix spécifiée ou celle par défaut
        voice_id = voice_id or self.voice_id
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # Utiliser un format de requête simplifié
        payload = {
            "text": text,
            "language": language
        }
        
        # Ajouter la voix si spécifiée
        if voice_id:
            payload["voice_id"] = voice_id
        
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                print(f"LOG: Tentative {attempt + 1}/{max_retries} d'appel à l'API Cartesia...")
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                response.raise_for_status()
                print("LOG: Audio généré avec succès via Cartesia TTS")
                
                # Retourner le contenu audio directement
                return {"audio_stream": [response.content]}
                
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    print(f"LOG: Timeout lors de l'appel à l'API Cartesia. Nouvelle tentative dans {retry_delay} secondes...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Backoff exponentiel
                else:
                    print("LOG: Échec après plusieurs tentatives - Timeout persistant.")
                    raise Exception("L'API Cartesia ne répond pas dans le délai imparti après plusieurs tentatives.")
            except requests.exceptions.HTTPError as e:
                print(f"LOG: Erreur HTTP lors de l'appel à l'API Cartesia: {str(e)}")
                if e.response.status_code == 401:
                    raise Exception("Erreur d'authentification avec l'API Cartesia. Vérifiez votre token d'accès.")
                raise
            except Exception as e:
                print(f"LOG: Erreur lors de l'appel à l'API Cartesia: {str(e)}")
                raise

def generate_audio_with_cartesia(text: str, voice_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Fonction utilitaire pour générer de l'audio avec Cartesia.
    Cette fonction est compatible avec l'interface existante pour ElevenLabs.
    """
    cartesia_client = CartesiaTTS()
    return cartesia_client.generate_audio(text=text, voice_id=voice_id)
