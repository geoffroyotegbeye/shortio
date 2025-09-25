# app/utils/video_utils.py
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from app.core.configs import FPS, WIDTH, HEIGHT
import os
from typing import Dict, Any
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
    
def create_karaoke_subtitle_clip(text: str, start: float, end: float, font_path: str, size: tuple) -> TextClip:
    """
    Crée un clip de sous-titre pour un mot ou un segment, en changeant sa couleur.
    Ceci est un exemple conceptuel. L'implémentation finale sera plus complexe.
    """
    # Ici, la logique de changement de couleur mot par mot devrait être implémentée
    # en utilisant les données de timing. C'est une tâche avancée.
    # Pour le moment, nous allons créer un clip de texte simple.
    
    return TextClip(
        txt=text, 
        fontsize=60, 
        color='white',
        stroke_color='black',
        stroke_width=2,
        font=font_path,
        size=size,
        method='caption'
    ).set_start(start).set_duration(end - start).set_pos(("center", "bottom"))

def make_video_from_assets(background_video_url: str, audio_path: str, timing_data: Dict[str, Any], out_video: str):
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
        # Si la vidéo est plus courte, la boucler
        video_clip = video_clip.loop(duration=audio_clip.duration)
    else:
        # Si la vidéo est plus longue, la couper
        video_clip = video_clip.subclip(0, audio_clip.duration)
        
    # 3. Créer les sous-titres (simplifié)
    subtitle_clips = [
        # Exemple de clip, la vraie logique dépend des données de timing
        create_karaoke_subtitle_clip("Mon super texte", 0, audio_clip.duration, "Arial", (WIDTH, HEIGHT))
    ]
    
    # 4. Superposer les éléments
    final_video = CompositeVideoClip([video_clip] + subtitle_clips)
    
    # 5. Définir l'audio et écrire le fichier final
    print("LOG: Écriture du fichier vidéo final...")
    final_video = final_video.set_audio(audio_clip)
    final_video.write_videofile(out_video, fps=FPS, codec="libx264", audio_codec="aac", threads=4, preset="medium")
    print(f"LOG: Vidéo finale sauvegardée à {out_video}")
    
    # Nettoyage des fichiers temporaires
    os.remove(background_video_path)
    os.remove(audio_path)
    
    return out_video