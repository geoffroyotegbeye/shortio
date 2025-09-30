# app/utils/whisper_utils.py
import whisper
from typing import List, Dict, Any

def transcribe_audio_with_whisper(audio_path: str) -> List[Dict[str, Any]]:
    """
    Transcrire un fichier audio en utilisant Whisper et retourner les segments de mots avec leurs timings.
    """
    print("LOG: Chargement du modèle Whisper...")
    # Utiliser le modèle 'base' qui est un bon compromis entre vitesse et précision.
    # Pour une meilleure précision (mais plus lent), on pourrait utiliser 'medium'.
    model = whisper.load_model("base")
    
    print(f"LOG: Transcription de l'audio : {audio_path}")
    try:
        # Lancer la transcription avec l'option word_timestamps=True
        result = model.transcribe(audio_path, word_timestamps=True)
        
        # Extraire les segments de mots
        word_segments = result.get('segments', [])
        
        # Aplatir la liste de mots
        all_words = []
        for segment in word_segments:
            all_words.extend(segment['words'])
            
        print(f"LOG: Transcription Whisper terminée. {len(all_words)} mots trouvés.")
        return all_words
        
    except Exception as e:
        print(f"LOG: Erreur lors de la transcription avec Whisper: {e}")
        return []
