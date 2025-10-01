# app/main.py

# Patch pour la compatibilité avec Pillow >= 10.0.0
# Doit être exécuté avant l'import de moviepy (qui se fait via d'autres modules)
import PIL.Image
if not hasattr(PIL.Image, 'Resampling'):
    PIL.Image.Resampling = PIL.Image # Compatibilité pour les anciennes versions
if not hasattr(PIL.Image, 'ANTIALIAS'):
    setattr(PIL.Image, 'ANTIALIAS', PIL.Image.Resampling.LANCZOS)

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router
import os

app = FastAPI(
    title="AI Video Generator API",
    description="API pour générer des vidéos courtes à partir d'un prompt ou y ajouter des sous-titres.",
    version="1.1.0"
)

# Configurer CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permettre toutes les origines (à ajuster en production)
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Servir les fichiers statiques (vidéos générées)
# Utilise la variable BACKEND_DIR définie dans configs.py pour plus de robustesse
from app.core.configs import BACKEND_DIR
output_dir = os.path.join(BACKEND_DIR, 'output')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

app.mount("/videos", StaticFiles(directory=output_dir), name="videos")

# Inclure les routes de l'API
app.include_router(router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bienvenue sur l'API AI Video Generator"}