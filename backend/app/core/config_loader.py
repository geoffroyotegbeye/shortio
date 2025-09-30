"""
Module pour charger les configurations à partir des variables d'environnement.
Ce fichier remplace l'utilisation directe de secrets.py.
"""
import os
from dotenv import load_dotenv
import moviepy.config as moviepy_conf

import sys

# Tenter de charger les variables d'environnement
try:
    # Charger les variables d'environnement depuis le fichier .env
    load_dotenv()
    print("LOG: Variables d'environnement chargées depuis le fichier .env")
except ImportError:
    print("LOG: Avertissement - python-dotenv n'est pas installé. Les variables d'environnement ne seront pas chargées depuis .env")

# Charger les clés API depuis les variables d'environnement
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")

# Configuration Cartesia
CARTESIA_ACCESS_TOKEN = os.environ.get("CARTESIA_ACCESS_TOKEN", "")
CARTESIA_VOICE_ID = os.environ.get("CARTESIA_VOICE_ID", "")

# Vérifier que les clés sont présentes
if not OPENAI_API_KEY:
    print("ATTENTION: Clé API OpenAI non configurée")

if not ELEVENLABS_API_KEY:
    print("ATTENTION: Clé API ElevenLabs non configurée")

if not ELEVENLABS_VOICE_ID:
    print("ATTENTION: ID de voix ElevenLabs non configuré")

if not PEXELS_API_KEY:
    print("ATTENTION: Clé API Pexels non configurée")

# Configuration de MoviePy pour ImageMagick
IMAGEMAGICK_BINARY = os.environ.get("IMAGEMAGICK_BINARY", "")
if not IMAGEMAGICK_BINARY:
    # Essayer de trouver ImageMagick automatiquement
    import platform
    if platform.system().lower() == "windows":
        possible_paths = [
            r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe",
            r"C:\Program Files\ImageMagick-7.1.1-Q16\magick.exe",
            r"C:\Program Files\ImageMagick-7.0.10-Q16\magick.exe"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                IMAGEMAGICK_BINARY = path
                break

# Configurer MoviePy
if IMAGEMAGICK_BINARY and os.path.exists(IMAGEMAGICK_BINARY):
    print(f"LOG: Configuration d'ImageMagick avec le chemin: {IMAGEMAGICK_BINARY}")
    moviepy_conf.change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_BINARY})
else:
    print("LOG: Chemin d'ImageMagick non trouvé. Les sous-titres peuvent ne pas fonctionner correctement.")
