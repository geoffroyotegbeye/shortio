"""
Script pour installer ImageMagick et configurer le chemin dans le fichier .env
"""
import os
import sys
import platform
import subprocess
import re
from dotenv import load_dotenv, set_key

def main():
    print("Installation et configuration d'ImageMagick pour TikTok Video Generator API")
    
    # Déterminer le système d'exploitation
    system = platform.system().lower()
    
    if system == "windows":
        print("\nSur Windows, vous devez installer ImageMagick manuellement:")
        print("1. Téléchargez ImageMagick depuis https://imagemagick.org/script/download.php#windows")
        print("2. Installez-le en cochant l'option 'Add to PATH'")
        print("3. Après l'installation, exécutez ce script à nouveau pour configurer le chemin")
        
        # Vérifier si ImageMagick est déjà installé
        try:
            # Essayer de trouver magick.exe dans le PATH
            result = subprocess.run(["where", "magick"], capture_output=True, text=True)
            if result.returncode == 0:
                magick_path = result.stdout.strip().split("\n")[0]
                print(f"\nImageMagick trouvé à: {magick_path}")
                update_env_file(magick_path)
            else:
                print("\nImageMagick n'a pas été trouvé dans votre PATH.")
                print("Après l'installation, exécutez ce script à nouveau.")
        except Exception as e:
            print(f"Erreur lors de la recherche d'ImageMagick: {str(e)}")
    
    elif system == "linux":
        print("\nInstallation d'ImageMagick sur Linux...")
        try:
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "imagemagick"], check=True)
            
            # Vérifier l'installation
            result = subprocess.run(["which", "convert"], capture_output=True, text=True)
            if result.returncode == 0:
                magick_path = result.stdout.strip()
                print(f"ImageMagick installé avec succès: {magick_path}")
                update_env_file(magick_path)
            else:
                print("Erreur: ImageMagick n'a pas été installé correctement.")
        except Exception as e:
            print(f"Erreur lors de l'installation d'ImageMagick: {str(e)}")
    
    elif system == "darwin":  # macOS
        print("\nInstallation d'ImageMagick sur macOS...")
        try:
            # Vérifier si Homebrew est installé
            result = subprocess.run(["which", "brew"], capture_output=True, text=True)
            if result.returncode != 0:
                print("Homebrew n'est pas installé. Installation de Homebrew...")
                homebrew_install = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
                os.system(homebrew_install)
            
            # Installer ImageMagick
            subprocess.run(["brew", "install", "imagemagick"], check=True)
            
            # Vérifier l'installation
            result = subprocess.run(["which", "convert"], capture_output=True, text=True)
            if result.returncode == 0:
                magick_path = result.stdout.strip()
                print(f"ImageMagick installé avec succès: {magick_path}")
                update_env_file(magick_path)
            else:
                print("Erreur: ImageMagick n'a pas été installé correctement.")
        except Exception as e:
            print(f"Erreur lors de l'installation d'ImageMagick: {str(e)}")
    
    else:
        print(f"Système d'exploitation non pris en charge: {system}")

def update_env_file(magick_path):
    """Met à jour le fichier .env avec le chemin d'ImageMagick"""
    env_file = ".env"
    
    # Charger les variables d'environnement existantes
    load_dotenv(env_file)
    
    # Mettre à jour la variable IMAGEMAGICK_BINARY
    set_key(env_file, "IMAGEMAGICK_BINARY", magick_path)
    print(f"Fichier .env mis à jour avec le chemin d'ImageMagick: {magick_path}")
    
    print("\nConfiguration terminée!")
    print("Vous pouvez maintenant exécuter l'API avec 'python run.py'")

if __name__ == "__main__":
    main()
