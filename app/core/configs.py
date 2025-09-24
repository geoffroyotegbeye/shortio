import os

# Dossier de sortie
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Paramètres vidéo
WIDTH, HEIGHT = 1080, 1920  # Format TikTok
FPS = 24

# Templates de scripts
SCRIPT_TEMPLATES = {
    "astuce": [
        "🤯 Cette astuce va changer votre vie ! Vous savez ce moment gênant où vous oubliez le nom de quelqu'un ? Voici LA méthode qui marche à tous les coups : Répétez le nom 3 fois dans la conversation. Associez-le à une image mentale forte. Utilisez-le en partant. Résultat : +90% de mémorisation ! Essayez et dites-moi en commentaire si ça marche pour vous ! 🔥",
        "Stop à la procrastination ! 😤 Technique des 2 minutes : Si une tâche prend moins de 2 minutes, faites-la MAINTENANT. Votre cerveau arrête de la reporter. Technique Pomodoro : 25 min de travail intense, 5 min de pause. Récompensez-vous après chaque session ! Qui teste cette semaine ? 💪"
    ],
    "motivation": [
        "💪 La différence entre les gens qui réussissent et les autres ? Ils font ce qu'ils doivent faire même quand ils n'en ont pas envie. Chaque jour, choisissez : soit vous avancez, soit vous reculez. Il n'y a pas de pause dans la vie. Alors, vous choisissez quoi aujourd'hui ? Dites-moi en commentaire votre objectif du jour ! 🎯"
    ],
    "lifestyle": [
        "✨ Matinée parfaite en 3 étapes : Réveil sans snooze (dur mais efficace). 10 minutes de méditation ou étirements. Petit-déj équilibré + hydratation. Votre énergie sera au max toute la journée ! Qui commence demain matin ? Tag un ami qui en a besoin ! 🌅"
    ]
}

# Palettes de couleurs
COLOR_PALETTES = [
    [(135, 206, 235), (255, 182, 193), (255, 255, 224)],  # Bleu ciel, rose, crème
    [(75, 0, 130), (138, 43, 226), (221, 160, 221)],      # Violet gradient
    [(255, 140, 0), (255, 69, 0), (255, 215, 0)],         # Orange/doré
]