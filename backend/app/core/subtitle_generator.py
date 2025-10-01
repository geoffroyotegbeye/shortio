# app/core/subtitle_generator.py
import os
import time
import uuid
from moviepy.editor import VideoFileClip

from app.core.configs import OUTPUT_DIR, TEMP_DIR
from app.utils.deepgram_utils import transcribe_audio_with_deepgram
from app.utils.whisper_utils import transcribe_audio_with_whisper
from app.utils.video_utils import make_video_from_assets

def process_video_for_subtitles(video_path: str, original_filename: str) -> str:
    """
    Orchestre le processus d'ajout de sous-titres à une vidéo.
    """
    base_name = f"subtitled_{uuid.uuid4().hex[:10]}_{os.path.splitext(original_filename)[0]}"
    temp_files = []

    try:
        # 1. Extraire l'audio de la vidéo
        print("LOG: Étape 1 - Extraction de l'audio...")
        audio_path = os.path.join(TEMP_DIR, f"{base_name}.wav")
        temp_files.append(audio_path)

        with VideoFileClip(video_path) as video_clip:
            if video_clip.audio is None:
                raise Exception("La vidéo uploadée ne contient pas de piste audio.")
            video_clip.audio.write_audiofile(audio_path, codec='pcm_s16le')
        
        # DEBUG: Vérifier la taille du fichier audio
        if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
            raise Exception(f"Le fichier audio extrait est vide ou n'a pas été créé à {audio_path}")
        print(f"LOG: Audio extrait avec succès. Taille: {os.path.getsize(audio_path)} bytes.")

        # 2. Transcrire l'audio pour obtenir les timings
        print("LOG: Étape 2 - Transcription de l'audio...")
        timing_data = []
        detected_lang = 'fr' # Langue par défaut si tout échoue
        try:
            print("LOG: Tentative de transcription avec Deepgram (avec détection de langue)...")
            deepgram_result = transcribe_audio_with_deepgram(audio_path)
            timing_data = deepgram_result.get("words", [])
            detected_lang = deepgram_result.get("detected_language", detected_lang)
            print(f"LOG: Langue détectée par Deepgram : {detected_lang}")
            if not timing_data:
                raise Exception("Deepgram n'a retourné aucun mot.")
        except Exception as e_deepgram:
            print(f"LOG DEBUG: La transcription Deepgram a échoué avec l'erreur : {e_deepgram}. Tentative avec Whisper...")
            try:
                # On utilise la langue détectée par Deepgram (ou le défaut) pour aider Whisper
                print(f"LOG: Lancement de Whisper avec la langue : {detected_lang}")
                timing_data = transcribe_audio_with_whisper(audio_path, language=detected_lang)
            except Exception as e_whisper:
                print(f"LOG: Échec de Whisper: {e_whisper}. Impossible d'obtenir les timings.")
                timing_data = []

        # DEBUG: Vérifier le contenu de timing_data avant le montage
        if not timing_data:
            print("LOG DEBUG: La liste de mots 'timing_data' est VIDE. La vidéo sera générée sans sous-titres.")
        else:
            print(f"LOG DEBUG: 'timing_data' contient {len(timing_data)} mots. Premier mot: {timing_data[0]}")

        # 3. Monter la vidéo avec les sous-titres
        print("LOG: Étape 3 - Montage de la vidéo avec sous-titres...")
        output_video_path = os.path.join(OUTPUT_DIR, f"{base_name}.mp4")

        # Réutiliser la fonction de montage existante
        # Note: 'background_video_url' est maintenant le chemin local de la vidéo originale
        # 'audio_path' est le chemin de l'audio extrait
        make_video_from_assets(
            background_video_url=video_path, 
            audio_path=audio_path,
            words_timing=timing_data,
            out_video=output_video_path,
            use_original_audio=True # Nouvelle option pour ne pas ré-encoder l'audio
        )

        print(f"LOG: Vidéo avec sous-titres générée : {output_video_path}")
        return output_video_path

    finally:
        # Nettoyage des fichiers temporaires
        print("LOG: Nettoyage des fichiers temporaires...")
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    print(f"LOG: Fichier temporaire supprimé : {temp_file}")
                except Exception as e:
                    print(f"LOG: Erreur lors de la suppression du fichier temporaire {temp_file}: {e}")
