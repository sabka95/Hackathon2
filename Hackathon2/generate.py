import os
from datetime import datetime
from filter_prompt import is_prompt_safe
from prompt_enricher import enrich_prompt
from AttnGAN.attngan_generate import generate_image_from_text
from quality_control import is_image_acceptable

def generate_image_from_prompt(prompt: str, max_retries: int = 3) -> tuple[str, str]:
    """
    Génère une image à partir d'un prompt utilisateur avec :
    - Filtrage éthique
    - Enrichissement par LLM
    - Génération AttnGAN
    - Contrôle qualité avec relance automatique

    Args:
        prompt (str): prompt brut (ex : "a red bird")
        max_retries (int): nombre maximum de tentatives en cas d’échec qualité

    Returns:
        (image_path, enriched_prompt) : chemin image valide et prompt enrichi
    """
    # 1. Filtrage éthique
    if not is_prompt_safe(prompt):
        raise ValueError("⛔ Prompt refusé : contenu inapproprié détecté.")

    # 2. Enrichissement avec LLM
    enriched_prompt = enrich_prompt(prompt)

    # 3. Dossiers de sauvegarde
    output_dir = "images/generated"
    rejected_dir = "images/rejected"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(rejected_dir, exist_ok=True)

    # 4. Tentatives de génération et validation qualité
    for attempt in range(1, max_retries + 1):
        # Génération image
        image = generate_image_from_text(enriched_prompt)

        # Sauvegarde temporaire
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gen_{timestamp}_try{attempt}.png"
        image_path = os.path.join(output_dir, filename)
        image.save(image_path)

        # Contrôle qualité
        if is_image_acceptable(image_path):
            return image_path, enriched_prompt

        # Sinon : déplacer vers dossier "rejected"
        rejected_path = os.path.join(rejected_dir, filename)
        os.rename(image_path, rejected_path)
        print(f"❌ Image rejetée (qualité insuffisante) - tentative {attempt}/{max_retries}")

    raise RuntimeError("❌ Aucune image générée n’a passé le contrôle qualité.")

