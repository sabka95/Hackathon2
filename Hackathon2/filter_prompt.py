# Importation de la bibliothèque Hugging Face Transformers
from transformers import pipeline

# Chargement d'une pipeline de classification de toxicité basée sur le modèle 'unitary/toxic-bert'
# Cette pipeline prend un texte et retourne une liste de scores associés à différents types de toxicité
toxic_classifier = pipeline("text-classification", model="unitary/toxic-bert", top_k=None)

# Liste des labels considérés comme inappropriés (à surveiller)
UNSAFE_LABELS = {
    "toxic", "obscene", "insult", "threat",
    "identity_attack", "identity_hate", "severe_toxic", "sexual_explicit"
}

# Fonction qui vérifie si un prompt est sûr en détectant les labels toxiques avec un score élevé
def is_prompt_safe(prompt: str, threshold: float = 0.5) -> bool:
    try:
        # Application de la pipeline de classification sur le prompt
        results = toxic_classifier(prompt)
        print(results)  # Affichage des résultats pour débogage

        # Analyse des résultats retournés pour le premier (et unique) texte
        for result in results[0]:  
            # Si le label est considéré comme dangereux ET dépasse le seuil défini
            if result['label'].lower() in UNSAFE_LABELS and result['score'] >= threshold:
                return False  # Prompt considéré comme dangereux

        return True  # Aucun score toxique détecté au-dessus du seuil, prompt accepté

    except Exception as e:
        # En cas d'erreur dans le modèle (connexion, format, etc.), rejeter le prompt par sécurité
        print(f"⚠️ Erreur dans la détection de toxicité : {e}")
        return False
