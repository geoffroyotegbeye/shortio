from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router

app = FastAPI(
    title="TikTok Video Generator API",
    description="API pour générer des vidéos TikTok à partir d'un concept",
    version="1.0.0"
)

# Configuration CORS
origins = [
    "http://localhost:5173",  # Autoriser le frontend React en développement
    # Ajoutez ici d'autres origines si nécessaire (ex: l'URL de votre site en production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les en-têtes
)

app.include_router(router, prefix="/api/v1")

# Monter le dossier 'output' pour servir les fichiers statiques (vidéos)
# Les vidéos seront accessibles via http://localhost:8000/videos/nom_du_fichier.mp4
app.mount("/videos", StaticFiles(directory="output"), name="videos")