# import re

# BANNED_KEYWORDS = [
#     "nude", "naked", "sex", "sexy", "porn", "erotic", "nudes", "fetish", "orgy", "genitals",
#     "boobs", "penis", "vagina", "strip", "kamasutra", "bdsm", "breasts", "nipple", "nips",

#     "gun", "kill", "murder", "blood", "knife", "weapon", "shoot", "bomb", "explosion", "war",
#     "sniper", "bullet", "execute", "stab", "assassinate", "hostage", "terrorist", "violence",

#     "drug", "cocaine", "heroin", "ecstasy", "meth", "overdose", "suicide", "hang", "cut myself",
#     "bleed", "self harm", "inject", "addict", "narcotic", "alcoholic",

#     "nazi", "hitler", "kkk", "slave", "lynch", "racist", "homophobe", "transphobe", "islamophobe",
#     "bigot", "discriminate", "misogynist", "sexist", "rape", "incest", "pedophile",

#     "child porn", "pedo", "bestiality", "abuse", "molest", "torture"
# ]

# def is_prompt_safe(prompt: str) -> bool:
#     prompt = prompt.lower()
#     for word in BANNED_KEYWORDS:
#         if re.search(rf"\b{re.escape(word)}\b", prompt):
#             return False
#     return True

from transformers import pipeline

# Charge une pipeline de classification de toxicité
toxic_classifier = pipeline("text-classification", model="unitary/toxic-bert", top_k=None)

def is_prompt_safe(prompt: str, threshold: float = 0.5) -> bool:
    """Vérifie si le prompt est non toxique selon un modèle sémantique."""
    try:
        results = toxic_classifier(prompt)
        for result in results:
            if result['label'].lower() == 'toxic' and result['score'] >= threshold:
                return False
        return True
    except Exception as e:
        print(f"⚠️ Erreur dans la détection de toxicité : {e}")
        return False 
