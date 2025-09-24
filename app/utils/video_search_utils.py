# app/utils/video_search_utils.py
import requests
import random
from app.core.secrets import PEXELS_API_KEY

def search_pexels_video(query: str) -> str:
    """Recherche une vidéo sur Pexels et retourne son URL."""
    url = f"https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "orientation": "portrait", "per_page": 10}
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    
    if data['videos']:
        video = random.choice(data['videos'])
        # Chercher une vidéo d'une taille appropriée (par ex. "hd" ou "sd")
        for file in video['video_files']:
            if file['width'] >= 1080:
                return file['link']
    return None