# Importation des bibliothèques nécessaires
import os                                  # Pour la gestion des fichiers et dossiers
from datetime import datetime              # Pour nommer les fichiers avec horodatage
from filter_prompt import is_prompt_safe   # Fonction personnalisée de filtrage éthique du prompt
from prompt_enricher import enrich_prompt  # Fonction personnalisée d’enrichissement du prompt via LLM
from AttnGAN.attngan_generate import generate_image_from_text  # Fonction GAN de génération d’image
from quality_control import is_image_acceptable               # Fonction personnalisée de contrôle qualité

# Fonction principale qui orchestre la génération d’image à partir d’un prompt utilisateur
def generate_image_from_prompt(prompt: str, max_retries: int = 3) -> tuple[str, str]:
    """
    Génère une image à partir d'un prompt utilisateur, avec :
    - Filtrage éthique
    - Enrichissement du prompt
    - Génération via AttnGAN
    - Contrôle qualité (et éventuellement plusieurs tentatives)

    Args:
        prompt (str): prompt utilisateur (ex: "a red bird")
        max_retries (int): nombre de tentatives autorisées si l’image générée est rejetée

    Returns:
        (image_path, enriched_prompt): chemin vers l’image acceptée et prompt enrichi utilisé
    """

    # Étape 1 : filtrage éthique du prompt
    if not is_prompt_safe(prompt):
        raise ValueError("⛔ Prompt refusé : contenu inapproprié détecté.")

    # Étape 2 : enrichissement du prompt via LLM (ex: ajout de détails pour meilleure image)
    enriched_prompt = enrich_prompt(prompt)

    # Étape 3 : préparation des dossiers de sauvegarde
    output_dir = "images/generated"    # Répertoire pour les images acceptées
    rejected_dir = "images/rejected"   # Répertoire pour les images rejetées
    os.makedirs(output_dir, exist_ok=True)    # Création si non existant
    os.makedirs(rejected_dir, exist_ok=True)

    # Étape 4 : boucle de génération et validation qualité (avec relance possible)
    for attempt in range(1, max_retries + 1):
        # Génération d'une image à partir du prompt enrichi
        image = generate_image_from_text(enriched_prompt)

        # Création d’un nom de fichier unique avec timestamp et numéro de tentative
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gen_{timestamp}_try{attempt}.png"
        image_path = os.path.join(output_dir, filename)

        # Sauvegarde temporaire de l’image
        image.save(image_path)

        # Vérification de la qualité de l’image générée
        if is_image_acceptable(image_path):
            # Si l’image passe le contrôle qualité, retour du chemin + prompt enrichi
            return image_path, enriched_prompt

        # Sinon : déplacer l’image dans le dossier "rejected"
        rejected_path = os.path.join(rejected_dir, filename)
        os.rename(image_path, rejected_path)
        print(f"❌ Image rejetée (qualité insuffisante) - tentative {attempt}/{max_retries}")

    # Si aucune des images générées ne passe le contrôle qualité
    raise RuntimeError("❌ Aucune image générée n’a passé le contrôle qualité.")
