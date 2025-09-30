# app/utils/gtts_utils.py
from gtts import gTTS
import io
from typing import Dict, Any

def generate_audio_with_gtts(text: str, lang: str = 'fr') -> Dict[str, Any]:
    """
    Génère de l'audio avec gTTS (Google Text-to-Speech).
    Retourne les données audio mais pas de données de synchronisation.
    """
    print("LOG: Appel à gTTS pour la génération audio...")
    try:
        # Créer un objet BytesIO pour stocker l'audio en mémoire
        audio_fp = io.BytesIO()
        
        # Créer l'objet gTTS
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # Écrire l'audio dans notre buffer en mémoire
        tts.write_to_fp(audio_fp)
        
        # Se positionner au début du buffer pour le lire
        audio_fp.seek(0)
        
        # Lire les données audio
        audio_data = audio_fp.read()
        
        print("LOG: Audio généré avec succès par gTTS.")
        
        # Retourner les données dans un format compatible avec le reste de l'application
        return {
            "audio_data": audio_data,
            "timing_data": {}  # gTTS ne fournit pas de données de synchronisation
        }
    except Exception as e:
        print(f"LOG: Erreur lors de la génération audio avec gTTS: {str(e)}")
        # En cas d'erreur, retourner un dictionnaire vide pour ne pas bloquer le flux
        return {"audio_data": None, "timing_data": {}}
