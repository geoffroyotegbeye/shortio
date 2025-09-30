# app/utils/llm_utils.py
import openai
import time
from app.core.config_loader import OPENAI_API_KEY

# Initialiser le client OpenAI avec la clé API
client = openai.OpenAI(api_key=OPENAI_API_KEY.strip())

def generate_script_with_openai(prompt: str, tone: str) -> str:
    """Génère un script vidéo à partir d'un prompt et d'un ton."""
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            print(f"LOG: Tentative {attempt + 1}/{max_retries} d'appel à l'API OpenAI...")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Tu es un créateur de contenu pour TikTok. Ton but est d'écrire un script court et percutant de moins de 100 mots, avec un ton {tone}."},
                    {"role": "user", "content": f"Génère un script vidéo sur le concept suivant : '{prompt}'."}
                ],
                max_tokens=150,
                temperature=0.7,
                timeout=30,  # Timeout explicite de 30 secondes
            )
            return response.choices[0].message.content.strip()
        except openai.Timeout:
            if attempt < max_retries - 1:
                print(f"LOG: Timeout lors de l'appel à l'API OpenAI. Nouvelle tentative dans {retry_delay} secondes...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Backoff exponentiel
            else:
                print("LOG: Échec après plusieurs tentatives - Timeout persistant.")
                raise Exception("L'API OpenAI ne répond pas dans le délai imparti après plusieurs tentatives.")
        except Exception as e:
            print(f"LOG: Erreur lors de l'appel à l'API OpenAI: {str(e)}")
            raise