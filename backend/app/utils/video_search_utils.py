# app/utils/video_search_utils.py
import requests
import random
import time
from app.core.config_loader import PEXELS_API_KEY

def search_pexels_video(query: str) -> str:
    """Recherche une vidéo sur Pexels et retourne son URL."""
    # Nettoyer la clé API (supprimer les espaces éventuels)
    api_key = PEXELS_API_KEY.strip() if PEXELS_API_KEY else ""
    
    if not api_key:
        print("LOG: Erreur - Clé API Pexels manquante ou vide")
        raise Exception("Clé API Pexels non configurée. Veuillez définir PEXELS_API_KEY dans secrets.py")
    
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": api_key}
    params = {"query": query, "orientation": "portrait", "per_page": 10}
    
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            print(f"LOG: Tentative {attempt + 1}/{max_retries} d'appel à l'API Pexels...")
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('videos'):
                print("LOG: Aucune vidéo trouvée pour la requête. Essai avec une requête plus générique...")
                # Si aucune vidéo n'est trouvée, essayer avec une requête plus générique
                if attempt == max_retries - 1:
                    # Dernière tentative avec un terme très général
                    generic_terms = ["nature", "people", "abstract", "background"]
                    params["query"] = random.choice(generic_terms)
                else:
                    # Simplifier la requête en prenant moins de mots
                    words = query.split()
                    if len(words) > 1:
                        params["query"] = " ".join(words[:1])  # Prendre juste le premier mot
                    continue
            
            # Si nous avons des vidéos, choisir une au hasard
            if data.get('videos'):
                video = random.choice(data['videos'])
                # Chercher une vidéo d'une taille appropriée (par ex. "hd" ou "sd")
                suitable_files = []
                for file in video['video_files']:
                    if file.get('width', 0) >= 1080:
                        suitable_files.append(file)
                
                if suitable_files:
                    print(f"LOG: Vidéo trouvée avec succès: {suitable_files[0]['link']}")
                    return suitable_files[0]['link']
            
            print("LOG: Aucune vidéo de taille appropriée trouvée.")
            return None
            
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                print(f"LOG: Timeout lors de l'appel à l'API Pexels. Nouvelle tentative dans {retry_delay} secondes...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Backoff exponentiel
            else:
                print("LOG: Échec après plusieurs tentatives - Timeout persistant.")
                raise Exception("L'API Pexels ne répond pas dans le délai imparti après plusieurs tentatives.")
        except requests.exceptions.HTTPError as e:
            print(f"LOG: Erreur HTTP lors de l'appel à l'API Pexels: {str(e)}")
            if e.response.status_code == 401:
                raise Exception("Erreur d'authentification avec l'API Pexels. Vérifiez votre clé API.")
            raise
        except Exception as e:
            print(f"LOG: Erreur lors de l'appel à l'API Pexels: {str(e)}")
            raise
    
    return None