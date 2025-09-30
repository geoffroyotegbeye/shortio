# app/core/tiktok_generator.py
import time
import os
from app.core.configs import OUTPUT_DIR, FPS
from app.utils.llm_utils import generate_script_with_openai
# Import both audio generation options
from app.utils.elevenlabs_utils import generate_audio_with_timing
from app.utils.cartesia_utils import generate_audio_with_cartesia
from app.utils.deepgram_utils import generate_audio_with_deepgram, transcribe_audio_with_deepgram
from app.utils.gtts_utils import generate_audio_with_gtts
from app.utils.whisper_utils import transcribe_audio_with_whisper
from app.utils.video_search_utils import search_pexels_video
from app.utils.video_utils import make_video_from_assets
import random
import re
from app.core.config_loader import CARTESIA_ACCESS_TOKEN

def make_tiktok_from_prompt(prompt, n_images=3, category="astuce", lang="fr", tone="percutant", tts_service="auto"):
    """
    Génère une vidéo TikTok à partir d'un prompt.
    
    Args:
        prompt: Le concept de la vidéo
        n_images: Nombre d'images à utiliser
        category: Catégorie de la vidéo (astuce, motivation, lifestyle)
        lang: Langue du contenu
        tone: Ton du script
        tts_service: Service TTS à utiliser ('auto', 'cartesia', 'elevenlabs')
    """
    
    timestamp = int(time.time())
    base_name = f"tiktok_{timestamp}"
    temp_files = []  # Liste pour suivre les fichiers temporaires à nettoyer en cas d'erreur
    
    try:
        # 1. Générer le script avec l'IA
        print("LOG: Étape 1 - Génération du script par OpenAI...")
        script = generate_script_with_openai(prompt=prompt, tone=tone)
        if not script or len(script.strip()) < 10:
            raise Exception("Le script généré est trop court ou vide.")
        print(f"LOG: Script généré : {script}")

        # 2. Chercher une vidéo de fond illustrant le script
        print("LOG: Étape 2 - Recherche d'une vidéo de fond sur Pexels...")
        # Nettoyer le texte pour la recherche de vidéo
        video_query = re.sub(r'[^\w\s]', '', script).split()[:5]
        video_query = " ".join(video_query)
        if not video_query or len(video_query.strip()) < 3:
            video_query = prompt  # Utiliser le prompt original si le script nettoyé est trop court
        
        background_video_url = search_pexels_video(query=video_query)

        if not background_video_url:
            print("LOG: Impossible de trouver une vidéo de fond. Tentative avec des termes génériques...")
            # Essayer avec des termes génériques liés à la catégorie
            generic_terms = {
                "astuce": "tips advice",
                "motivation": "motivation success",
                "lifestyle": "lifestyle daily routine"
            }
            background_video_url = search_pexels_video(query=generic_terms.get(category, "background"))
            
            if not background_video_url:
                raise Exception("Impossible de trouver une vidéo de fond après plusieurs tentatives.")
        
        print(f"LOG: Vidéo de fond trouvée : {background_video_url}")

        # 3. Générer l'audio avec Cartesia ou ElevenLabs
        audio_path = os.path.join(OUTPUT_DIR, f"{base_name}.mp3")
        
        # Déterminer quelle API utiliser pour la génération audio
        audio_response = None

        # Logique de génération audio avec fallback
        print("LOG: Étape 3 - Tentative de génération audio...")
        try:
            print("LOG: Tentative avec Deepgram (prioritaire)...")
            audio_response = generate_audio_with_deepgram(text=script)
        except Exception as e_deepgram:
            print(f"LOG: Échec de Deepgram TTS: {e_deepgram}. Tentative avec ElevenLabs...")
            try:
                audio_response = generate_audio_with_timing(text=script)
            except Exception as e_elevenlabs:
                print(f"LOG: Échec d'ElevenLabs: {e_elevenlabs}. Tentative avec gTTS...")
                try:
                    audio_response = generate_audio_with_gtts(text=script, lang=lang)
                except Exception as e_gtts:
                    print(f"LOG: Échec de gTTS: {e_gtts}. La génération audio a échoué.")
                    raise Exception("Tous les services de génération audio ont échoué.")
        
        if not audio_response or not audio_response.get("audio_data"):
            raise Exception("La génération audio a échoué ou n'a retourné aucune donnée.")

        # Extraire les données audio
        audio_data = audio_response["audio_data"]

        # Sauvegarde du fichier audio
        try:
            with open(audio_path, 'wb') as f:
                f.write(audio_data)
            temp_files.append(audio_path)  # Ajouter à la liste des fichiers temporaires
            print(f"LOG: Audio généré et sauvegardé : {audio_path}")
        except Exception as e:
            print(f"LOG: Erreur lors de la sauvegarde de l'audio : {str(e)}")
            raise Exception(f"Erreur lors de la sauvegarde de l'audio : {str(e)}")

        # NOUVELLE ÉTAPE : Transcription pour obtenir les timings
        print("LOG: Étape 3.5 - Tentative de transcription pour la synchronisation...")
        try:
            print("LOG: Tentative avec Deepgram (prioritaire)...")
            timing_data = transcribe_audio_with_deepgram(audio_path)
        except Exception as e_deepgram_stt:
            print(f"LOG: Échec de Deepgram STT: {e_deepgram_stt}. Tentative avec Whisper...")
            try:
                timing_data = transcribe_audio_with_whisper(audio_path)
            except Exception as e_whisper:
                print(f"LOG: Échec de Whisper: {e_whisper}. Impossible d'obtenir les timings.")
                timing_data = [] # Continuer sans sous-titres

        # 4. Monter la vidéo
        print("LOG: Étape 4 - Montage de la vidéo...")
        out_video = os.path.join(OUTPUT_DIR, f"{base_name}.mp4")
        make_video_from_assets(
            background_video_url=background_video_url,
            audio_path=audio_path,
            words_timing=timing_data, # Passer les timings de Whisper
            out_video=out_video
        )
        print("LOG: Montage terminé.")

        # Vérifier que le fichier vidéo existe et a une taille non nulle
        if not os.path.exists(out_video) or os.path.getsize(out_video) == 0:
            raise Exception("La vidéo générée est vide ou n'a pas été créée correctement.")

        return out_video
        
    except Exception as e:
        print(f"LOG: Erreur dans le processus de génération de vidéo : {str(e)}")
        
        # Nettoyer les fichiers temporaires en cas d'erreur
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    print(f"LOG: Fichier temporaire supprimé : {temp_file}")
                except:
                    pass
        
        # Relancer l'exception pour la gestion d'erreur en amont
        raise