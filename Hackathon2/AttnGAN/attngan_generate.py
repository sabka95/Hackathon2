# attngan_generate.py (remplacé par Stable Diffusion via Hugging Face Diffusers)

# Importation des bibliothèques nécessaires
import torch                                         # PyTorch pour le calcul tensoriel
from diffusers import StableDiffusionPipeline       # Pipeline de génération d’image Stable Diffusion

# Chargement du modèle Stable Diffusion préentraîné depuis Hugging Face
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",               # Modèle choisi : Stable Diffusion v1.5
    torch_dtype=torch.float32                       # Type des tenseurs utilisé (ici float32 pour compatibilité CPU)
)

pipe = pipe.to("cpu")  # Envoie le modèle sur le CPU. Pour accélérer, utiliser .to("cuda") si un GPU est disponible.

# Fonction principale pour générer une image à partir d’un prompt texte
def generate_image_from_text(prompt: str):
    """
    Génère une image à partir d’un prompt texte en utilisant Stable Diffusion.

    Args:
        prompt (str): le texte descriptif de l’image à générer

    Returns:
        image (PIL.Image): image générée correspondant au prompt
    """
    with torch.no_grad():                           # Désactive la gestion automatique des gradients (économie mémoire)
        result = pipe(prompt, num_inference_steps=25)  # Génère l’image en 25 étapes d’inférence

    return result.images[0]  # Retourne la première image générée (liste de 1 élément)
