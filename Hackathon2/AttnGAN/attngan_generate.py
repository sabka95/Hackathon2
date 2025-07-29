# attngan_generate.py (remplacé par Stable Diffusion Hugging Face)
import torch
from diffusers import StableDiffusionPipeline

# Chargement du modèle Hugging Face
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32
)
pipe = pipe.to("cpu")  # Si tu as un GPU : .to("cuda")

def generate_image_from_text(prompt: str):
    """
    Génère une image à partir d’un prompt texte en utilisant Stable Diffusion.
    """
    with torch.no_grad():
        result = pipe(prompt, num_inference_steps=25)
    return result.images[0]
