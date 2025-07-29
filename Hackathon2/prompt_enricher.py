# Importation de la bibliothèque Hugging Face Transformers
from transformers import pipeline

# Chargement d’une pipeline de génération de texte à partir de texte
# Le modèle utilisé ici est 'google/flan-t5-base', un LLM polyvalent optimisé pour suivre des instructions
generator = pipeline("text2text-generation", model="google/flan-t5-base")

# Fonction d’enrichissement de prompt : elle rend le prompt plus descriptif pour générer une image plus détaillée
def enrich_prompt(prompt: str) -> str:
    """
    Utilise un LLM pour enrichir le prompt utilisateur en ajoutant des détails visuels.
    
    Args:
        prompt (str): prompt de base saisi par l'utilisateur (ex : "a red bird")

    Returns:
        str: prompt enrichi (ex : "a vivid red bird with long feathers flying over a misty forest")
    """
    
    # Création d’une instruction claire pour guider le LLM (en anglais car les modèles Flan-T5 sont anglophones)
    instruction = f"Make this prompt much more detailed and visual for an image generator: '{prompt}'"
    
    # Appel de la pipeline de génération de texte
    result = generator(
        instruction,
        max_new_tokens=30,              # Longueur maximale de la réponse générée
        do_sample=False,             # Désactivation du sampling pour une réponse plus déterministe
        num_return_sequences=1,      # On ne garde qu’une seule version du prompt enrichi
    )[0]['generated_text']
    print("🔍 Résultat généré :", result)
    # Nettoyage et retour du texte enrichi
    return result.strip()
