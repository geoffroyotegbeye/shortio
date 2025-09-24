# TikTok Video Generator API

API RESTful pour générer des vidéos TikTok à partir d'un concept, utilisant FastAPI.

## Prérequis
- Python 3.8+
- Dépendances listées dans `requirements.txt`

## Installation
1. Cloner le dépôt :
   ```bash
   git clone <url-du-dépôt>
   cd tiktok_api
   ```
2. Créer un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
4. Lancer le serveur :
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## Utilisation
- Accéder à la documentation interactive : `http://localhost:8000/docs`
- Envoyer une requête POST à `/api/v1/generate-video` avec un JSON comme :
  ```json
  {
    "concept": "Une astuce pour mémoriser des noms",
    "n_images": 3,
    "category": "astuce",
    "lang": "fr"
  }
  ```

## Tester
Exécuter les tests unitaires :
```bash
pytest tests/
```

## Structure
- `app/main.py` : Point d'entrée de l'API.
- `app/api/endpoints.py` : Routes de l'API.
- `app/core/` : Logique métier et configuration.
- `app/models/` : Modèles Pydantic.
- `app/utils/` : Fonctions utilitaires.
- `tests/` : Tests unitaires.
- `output/` : Fichiers générés.

## Dépendances
Voir `requirements.txt` pour la liste complète.