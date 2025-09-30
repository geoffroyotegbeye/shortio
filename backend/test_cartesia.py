"""
Script de test pour l'API Cartesia TTS - Version simplifiée
"""
import requests

# Token d'accès Cartesia (directement dans le code pour simplifier le test)
token = "sk_car_ytausfC8xbbob2pmot358s"

# URL de l'API
url = "https://api.cartesia.ai/tts/bytes"

# Texte à convertir en audio
text = "Bonjour, ceci est un test de l'API Cartesia."

# Paramètres de la requête (version simplifiée)
payload = {
    "text": text,
}

# En-têtes de la requête
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

print(f"Envoi de la requête à l'API Cartesia...")
try:
    # Envoyer la requête
    response = requests.post(url, json=payload, headers=headers)

    # Afficher le code de statut et la réponse
    print(f"Code de statut: {response.status_code}")
    print(f"Réponse: {response.text[:500]}")  # Afficher les 500 premiers caractères de la réponse

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Enregistrer l'audio dans un fichier
        with open("test_cartesia.mp3", "wb") as f:
            f.write(response.content)
        print(f"Audio généré avec succès et enregistré dans test_cartesia.mp3")
except Exception as e:
    print(f"Erreur: {e}")
