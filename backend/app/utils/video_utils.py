# app/utils/video_utils.py
# Importer config_loader en premier pour configurer ImageMagick avant d'importer moviepy
from app.core import config_loader
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
from app.core.configs import FPS, WIDTH, HEIGHT
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
    
def create_karaoke_subtitle_clip(text: str, start: float, end: float, font_path: str = "arial.ttf", size: tuple = (WIDTH, HEIGHT)) -> ImageClip:
    """
    Crée un clip de sous-titre en utilisant Pillow pour dessiner le texte.
    Cette méthode ne dépend pas d'ImageMagick.
    """
    try:
        # Définir la police et la taille
        try:
            font = ImageFont.truetype(font_path, 60)
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
        
        # Position en bas au centre
        position = ((size[0] - text_width) / 2, size[1] - text_height - 50) # 50px depuis le bas

        # Dessiner le contour (pour la lisibilité)
        stroke_width = 3
        for x_offset in range(-stroke_width, stroke_width + 1):
            for y_offset in range(-stroke_width, stroke_width + 1):
                if x_offset != 0 or y_offset != 0:
                    draw.text((position[0] + x_offset, position[1] + y_offset), text, font=font, fill='black')

        # Dessiner le texte principal
        draw.text(position, text, font=font, fill='white')

        # Convertir l'image Pillow en tableau NumPy que MoviePy peut utiliser
        image_array = np.array(img)
        return ImageClip(image_array).set_start(start).set_duration(end - start).set_pos(('center', 'center'))

    except Exception as e:
        print(f"LOG: Erreur lors de la création du sous-titre avec Pillow: {e}")
        return None

def make_video_from_assets(background_video_url: str, audio_path: str, words_timing: List[Dict[str, Any]], out_video: str):
    """
    Monte une vidéo à partir d'une vidéo de fond, d'un fichier audio et de données de timing.
    """
    # 1. Télécharger la vidéo de fond
    background_video_path = "temp_background_video.mp4"
    download_file(background_video_url, background_video_path)
    
    # 2. Charger les clips
    print("LOG: Chargement des clips vidéo et audio...")
    video_clip = VideoFileClip(background_video_path)
    audio_clip = AudioFileClip(audio_path)
    
    # Adapter la vidéo à la durée de l'audio
    if video_clip.duration < audio_clip.duration:
        video_clip = video_clip.loop(duration=audio_clip.duration)
    else:
        video_clip = video_clip.subclip(0, audio_clip.duration)
        
    # 3. Créer les sous-titres dynamiques
    subtitle_clips = []
    if words_timing:
        print(f"LOG: Création de {len(words_timing)} clips de sous-titres...")
        for item in words_timing:
            clip = create_karaoke_subtitle_clip(item['word'], item['start'], item['end'])
            if clip:
                subtitle_clips.append(clip)
    else:
        print("LOG: Aucune donnée de synchronisation pour les sous-titres. La vidéo sera générée sans texte.")

    # 4. Superposer les éléments
    # On commence avec le clip vidéo de base
    final_clips = [video_clip]
    # On ajoute tous les clips de sous-titres par-dessus
    if subtitle_clips:
        final_clips.extend(subtitle_clips)

    final_video = CompositeVideoClip(final_clips)
    
    # 5. Définir l'audio et écrire le fichier final
    print("LOG: Écriture du fichier vidéo final...")
    final_video = final_video.set_audio(audio_clip)
    final_video.write_videofile(out_video, fps=FPS, codec="libx264", audio_codec="aac", threads=4, preset="medium")
    print(f"LOG: Vidéo finale sauvegardée à {out_video}")

    # Fermer les clips pour libérer les fichiers (important pour Windows)
    try:
        video_clip.close()
        audio_clip.close()
        final_video.close()
        print("LOG: Clips MoviePy fermés.")
    except Exception as e:
        print(f"LOG: Avertissement - n'a pas pu fermer tous les clips : {e}")
    
    # Nettoyage des fichiers temporaires
    os.remove(background_video_path)
    # Ne pas supprimer audio_path ici car il est géré dans tiktok_generator
    
    return out_video