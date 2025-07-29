# Importation de la fonction de génération d’image depuis le module principal
from generate import generate_image_from_prompt

# Lecture du fichier contenant les prompts à traiter
with open("test_prompts.txt", "r") as f:
    # Nettoie les lignes vides et les espaces
    prompts = [line.strip() for line in f.readlines() if line.strip()]

# Boucle principale : génère une image pour chaque prompt
for i, prompt in enumerate(prompts):
    try:
        # Appel à la fonction qui effectue le filtrage, enrichissement, génération et contrôle qualité
        path, enriched = generate_image_from_prompt(prompt)

        # Affiche le chemin de l’image générée avec succès
        print(f"[{i+1}/{len(prompts)}] ✅ Image générée : {path}")

    except Exception as e:
        # En cas d’erreur (prompt rejeté, image invalide, etc.), affiche un message d’échec
        print(f"[{i+1}/{len(prompts)}] ❌ Échec pour le prompt '{prompt}': {e}")
