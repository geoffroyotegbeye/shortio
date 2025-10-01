# app/utils/deepgram_utils.py
import os
from deepgram import DeepgramClient, SpeakOptions, PrerecordedOptions
from typing import List, Dict, Any

# Initialiser le client Deepgram une seule fois
# Le SDK lira automatiquement la variable d'environnement DEEPGRAM_API_KEY
try:
    deepgram_client = DeepgramClient()
except Exception as e:
    print(f"LOG: Avertissement - Impossible d'initialiser le client Deepgram: {e}")
    deepgram_client = None

def generate_audio_with_deepgram(text: str, lang: str = 'en') -> Dict[str, Any]:
    """
    Génère de l'audio avec le service Text-to-Speech de Deepgram.
    """
    if not deepgram_client:
        raise Exception("Le client Deepgram n'est pas initialisé. Vérifiez votre clé API.")

    print("LOG: Appel à l'API Deepgram pour la génération audio (TTS)...")
    try:
        # Choisir le modèle en fonction de la langue
        model_name = "aura-2-asteria-fr" if lang == 'fr' else "aura-2-zeus-en"
        print(f"LOG: Utilisation du modèle Deepgram TTS : {model_name}")

        options = SpeakOptions(
            model=model_name,
            encoding="linear16",  # Encodage standard pour WAV
            container="wav"
        )
        
        # L'API retourne directement les bytes de l'audio
        response = deepgram_client.speak.rest.v("1").stream(
            {"text": text},
            options
        )
        
        # 'stream' contient les données binaires directement
        audio_data = response.stream.read()

        print("LOG: Audio généré avec succès par Deepgram.")
        return {"audio_data": audio_data}

    except Exception as e:
        print(f"LOG: Erreur lors de la génération audio avec Deepgram: {e}")
        raise

def transcribe_audio_with_deepgram(audio_path: str, lang: str = None) -> Dict[str, Any]:
    """
    Transcrire un fichier audio en utilisant le service Speech-to-Text de Deepgram.
    """
    if not deepgram_client:
        raise Exception("Le client Deepgram n'est pas initialisé. Vérifiez votre clé API.")

    print(f"LOG: Appel à l'API Deepgram pour la transcription audio (STT) de {audio_path}...")
    try:
        with open(audio_path, 'rb') as audio_file:
            buffer_data = audio_file.read()

        payload = {
            'buffer': buffer_data
        }

        options = PrerecordedOptions(
            model="nova-2",
            detect_language=True, # Détection automatique de la langue
            smart_format=True,
            utterances=True,
            diarize=True, # Activer la diarisation pour avoir les timings par mot
            punctuate=True
        )

        response = deepgram_client.listen.prerecorded.v("1").transcribe_file(
            payload,
            options,
            timeout=600 # Timeout de 10 minutes pour les fichiers longs
        )

        response_dict = response.to_dict()
        
        # Extraire les informations utiles
        words = []
        detected_language = ""
        if response_dict.get('results'):
            channels = response_dict['results'].get('channels', [])
            if channels:
                alternatives = channels[0].get('alternatives', [])
                if alternatives:
                    detected_language = alternatives[0].get('detected_language', '')
                    transcript_words = alternatives[0].get('words', [])
                    for word in transcript_words:
                        words.append({
                            'word': word.get('punctuated_word', word.get('word')),
                            'start': word.get('start'),
                            'end': word.get('end')
                        })

        print(f"LOG: Transcription Deepgram réussie, {len(words)} mots trouvés. Langue détectée: {detected_language}")
        return {
            "words": words,
            "detected_language": detected_language
        }

    except Exception as e:
        print(f"LOG: Erreur lors de la transcription avec Deepgram: {e}")
        raise
