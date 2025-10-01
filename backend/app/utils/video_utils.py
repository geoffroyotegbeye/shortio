# app/utils/video_utils.py
# Importer config_loader en premier pour configurer ImageMagick avant d'importer moviepy
from app.core import config_loader
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
from app.core.configs import FPS, WIDTH, HEIGHT, TEMP_DIR, BACKEND_DIR
import uuid
import os
import numpy as np
from typing import List, Dict, Any
import requests # Importer la bibliothèque requests

def download_file(url: str, local_path: str):
    """
    Télécharge un fichier depuis une URL et l'enregistre localement.
    """
    print(f"LOG: Téléchargement du fichier depuis {url}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status() # Lève une exception pour les codes d'erreur HTTP
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("LOG: Téléchargement terminé.")
    except requests.exceptions.RequestException as e:
        print(f"LOG: Erreur lors du téléchargement: {e}")
        raise
    
# Construire le chemin absolu vers la police en utilisant la racine du projet
FONT_PATH = os.path.join(BACKEND_DIR, 'assets', 'fonts', 'Montserrat', 'static', 'Montserrat-Bold.ttf')

def create_karaoke_subtitle_clip(text: str, start: float, end: float, font_path: str = FONT_PATH, size: tuple = (WIDTH, HEIGHT)) -> ImageClip:
    """
    Crée un clip de sous-titre en utilisant Pillow pour dessiner le texte.
    Cette méthode ne dépend pas d'ImageMagick.
    """
    try:
        # Définir la police et la taille
        try:
            font = ImageFont.truetype(font_path, 130)
        except IOError:
            print(f"LOG: Police '{font_path}' non trouvée, utilisation de la police par défaut.")
            font = ImageFont.load_default()

        # Créer une image transparente
        img = Image.new('RGBA', size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Obtenir la taille du texte pour le centrer
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Positionner le texte au centre, mais avec un décalage vers le bas
        text_x = (size[0] - text_width) / 2
        
        # Décalage vertical depuis le centre. Augmentez cette valeur pour descendre le texte.
        vertical_offset = 300 
        text_y = ((size[1] - text_height) / 2) + vertical_offset

        # Ajouter un arrière-plan semi-transparent
        bg_padding = 15
        bg_box = [
            text_x - bg_padding,
            text_y - bg_padding,
            text_x + text_width + bg_padding,
            text_y + text_height + bg_padding
        ]
        # Utiliser un rectangle avec des coins arrondis
        draw.rounded_rectangle(bg_box, radius=10, fill=(0, 0, 0, 150)) # Noir avec ~60% d'opacité

        # Dessiner le texte principal (jaune vif pour un bon contraste)
        draw.text((text_x, text_y), text, font=font, fill=(255, 255, 0))

        # Convertir l'image Pillow en tableau NumPy que MoviePy peut utiliser
        image_array = np.array(img)
        return ImageClip(image_array).set_start(start).set_duration(end - start).set_pos(('center', 'center'))

    except Exception as e:
        print(f"LOG: Erreur lors de la création du sous-titre avec Pillow: {e}")
        return None

def make_video_from_assets(background_video_url: str, audio_path: str, words_timing: List[Dict[str, Any]], out_video: str, use_original_audio: bool = False):
    """
    Monte une vidéo à partir d'une vidéo de fond, d'un fichier audio et de données de timing.
    """
    temp_files = []
    video_clip = None
    audio_clip = None
    final_clip = None
    subtitle_clips = []

    try:
        # 1. Préparer la vidéo de fond
        if background_video_url.startswith('http'):
            print("LOG: Téléchargement de la vidéo de fond depuis une URL...")
            background_video_path = os.path.join(TEMP_DIR, f"background_{uuid.uuid4().hex}.mp4")
            download_file(background_video_url, background_video_path)
            temp_files.append(background_video_path)
        else:
            print("LOG: Utilisation de la vidéo locale comme fond...")
            background_video_path = background_video_url # C'est déjà un chemin local

        # 2. Charger et normaliser le clip vidéo
        print("LOG: Chargement et normalisation du clip vidéo...")
        video_clip = VideoFileClip(background_video_path)
        # Redimensionner à la taille standard pour assurer la cohérence des sous-titres
        if video_clip.size != [WIDTH, HEIGHT]:
            print(f"LOG: Redimensionnement de la vidéo de {video_clip.size} à {[WIDTH, HEIGHT]}")
            video_clip = video_clip.resize(newsize=(WIDTH, HEIGHT))

        if use_original_audio:
            audio_clip = video_clip.audio
        else:
            audio_clip = AudioFileClip(audio_path)

        if not audio_clip:
            raise Exception("Impossible de charger le clip audio.")

        # Adapter la vidéo à la durée de l'audio
        if video_clip.duration < audio_clip.duration:
            video_clip = video_clip.loop(duration=audio_clip.duration)
        else:
            video_clip = video_clip.subclip(0, audio_clip.duration)

        # 3. Créer les sous-titres dynamiques
        if words_timing:
            print(f"LOG: Création de {len(words_timing)} clips de sous-titres...")
            for item in words_timing:
                word = item.get('word') or item.get('punctuated_word')
                start = item.get('start')
                end = item.get('end')
                if word and start is not None and end is not None:
                    clip = create_karaoke_subtitle_clip(word, start, end)
                    if clip:
                        subtitle_clips.append(clip)

        # 4. Combiner tous les clips
        print("LOG: Combinaison des clips...")
        final_clip = CompositeVideoClip([video_clip] + subtitle_clips)
        final_clip.audio = audio_clip

        # 5. Écrire la vidéo finale
        print("LOG: Écriture de la vidéo finale...")
        final_clip.write_videofile(out_video, codec="libx264", audio_codec="aac", fps=FPS)

        return out_video

    finally:
        # 6. Nettoyage
        print("LOG: Fermeture des clips MoviePy...")
        clips_to_close = [video_clip, audio_clip, final_clip] + subtitle_clips
        for clip in clips_to_close:
            if clip:
                try:
                    clip.close()
                except Exception:
                    pass # Ignorer les erreurs de fermeture

        print("LOG: Nettoyage des fichiers temporaires...")
        for file_path in temp_files:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"LOG: Erreur lors de la suppression du fichier {file_path}: {e}")
    return out_video