# app/utils/llm_utils.py
import openai
from app.core.secrets import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_script_with_openai(prompt: str, tone: str) -> str:
    """Génère un script vidéo à partir d'un prompt et d'un ton."""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Tu es un créateur de contenu pour TikTok. Ton but est d'écrire un script court et percutant de moins de 100 mots, avec un ton {tone}."},
            {"role": "user", "content": f"Génère un script vidéo sur le concept suivant : '{prompt}'."}
        ],
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()