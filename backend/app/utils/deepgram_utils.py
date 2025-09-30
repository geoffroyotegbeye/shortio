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

def generate_audio_with_deepgram(text: str) -> Dict[str, Any]:
    """
    Génère de l'audio avec le service Text-to-Speech de Deepgram.
    """
    if not deepgram_client:
        raise Exception("Le client Deepgram n'est pas initialisé. Vérifiez votre clé API.")

    print("LOG: Appel à l'API Deepgram pour la génération audio (TTS)...")
    try:
        options = SpeakOptions(
            model="aura-2-zeus-en",  # Un modèle performant, à adapter si besoin
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

def transcribe_audio_with_deepgram(audio_path: str) -> List[Dict[str, Any]]:
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
            smart_format=True,
            utterances=True,
            diarize=True, # Activer la diarisation pour avoir les timings par mot
            punctuate=True
        )

        response = deepgram_client.listen.prerecorded.v("1").transcribe_file(payload, options)
        
        # Extraire les mots et leurs timings
        words = response.results.channels[0].alternatives[0].words
        # Transformer les objets Word en dictionnaires simples
        word_list = [
            {"word": word.word, "start": word.start, "end": word.end}
            for word in words
        ]
        
        print(f"LOG: Transcription Deepgram terminée. {len(word_list)} mots trouvés.")
        return word_list

    except Exception as e:
        print(f"LOG: Erreur lors de la transcription avec Deepgram: {e}")
        raise
