# === IMPORTS ===
import os
from PIL import Image                           # Pour charger les images
import torch                                    # Pour le calcul avec GPU/CPU
import torchvision.transforms as T              # Pour redimensionnement et conversion en tenseur
from torchmetrics.image.fid import FrechetInceptionDistance  # Pour calculer le FID
from torchvision.transforms.functional import pil_to_tensor  # Pour transformer une image PIL en tenseur
import open_clip                                # Pour évaluer la similarité image/texte avec CLIP

# === CONFIGURATION DES DOSSIERS ===
GENERATED_DIR = "images/generated"              # Dossier contenant les images générées
REAL_DIR = "images/real"                        # Dossier contenant les images réelles de référence
PROMPT_FILE = "test_prompts.txt"                # Fichier contenant les prompts textuels

# === PRÉTRAITEMENT POUR FID ===
transform_fid = T.Compose([
    T.Resize((299, 299)),                       # Redimensionne à la taille attendue par Inception
    T.ToTensor()                                # Convertit l’image en tenseur PyTorch
])

# === INITIALISATION DU CALCUL DU FID ===
fid = FrechetInceptionDistance(feature=64)      # Plus feature est bas, plus c’est rapide (moins précis que 2048)

# === INITIALISATION DE CLIP ===
device = "cuda" if torch.cuda.is_available() else "cpu"   # Utilise le GPU si dispo
clip_model, _, preprocess_clip = open_clip.create_model_and_transforms(
    'ViT-B-32', pretrained='laion2b_s34b_b79k')            # Chargement du modèle CLIP et de ses transforms
tokenizer = open_clip.get_tokenizer('ViT-B-32')            # Tokeniseur pour transformer le texte en vecteurs
clip_model = clip_model.to(device)                         # Envoie le modèle sur le bon périphérique

# === AJOUT DES IMAGES RÉELLES POUR FID (base de comparaison) ===
real_images = sorted([
    f for f in os.listdir(REAL_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg"))
])

for fname in real_images:
    img_path = os.path.join(REAL_DIR, fname)
    try:
        img = Image.open(img_path).convert("RGB").resize((299, 299))   # Prétraitement image réelle
        tensor = pil_to_tensor(img)                                    # Conversion en tenseur (uint8)
        fid.update(tensor.unsqueeze(0), real=True)                     # Ajout à la référence FID
    except Exception as e:
        print(f"❌ Erreur image réelle '{fname}' : {e}")

# === CHARGEMENT DES PROMPTS ASSOCIÉS AUX IMAGES GÉNÉRÉES ===
with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    prompts = [line.strip() for line in f.readlines() if line.strip()]  # Nettoyage des lignes vides

# === ÉVALUATION DES IMAGES GÉNÉRÉES ===
clip_scores = []                          # Stocke les scores CLIP pour calculer la moyenne
total = len(prompts)                      # Nombre total d’évaluations attendues

print(f"\n🔍 Évaluation sur {total} prompts...")

for i, prompt in enumerate(prompts):
    img_path = os.path.join(GENERATED_DIR, f"{i}.png")     # Chemin de l’image générée correspondante

    if not os.path.exists(img_path):
        print(f"❌ Image manquante : {img_path}")
        continue

    try:
        # === FID ===
        image_pil = Image.open(img_path).convert("RGB").resize((299, 299))
        img_fid = pil_to_tensor(image_pil)
        fid.update(img_fid.unsqueeze(0), real=False)       # Ajout à l’échantillon FID à comparer

        # === CLIPScore ===
        image = preprocess_clip(image_pil).unsqueeze(0).to(device)   # Prétraitement image
        text = tokenizer([prompt]).to(device)                        # Tokenisation du prompt

        with torch.no_grad():                                       # Pas besoin de gradients
            image_feat = clip_model.encode_image(image)             # Embedding image
            text_feat = clip_model.encode_text(text)                # Embedding texte
            score = torch.nn.functional.cosine_similarity(image_feat, text_feat)  # Similarité
            clip_scores.append(score.item())                        # Sauvegarde du score

        print(f"[{i+1}/{total}] ✅ {img_path} | CLIPScore: {score.item():.4f}")

    except Exception as e:
        print(f"[{i+1}/{total}] ❌ Erreur sur '{img_path}' : {e}")

# === AFFICHAGE DES RÉSULTATS FINAUX ===
mean_clip = sum(clip_scores) / len(clip_scores) if clip_scores else 0
fid_score = fid.compute().item()  # Calcul final du FID

print("\n=== 🔚 RÉSULTATS FINAUX ===")
print(f"🎯 CLIPScore moyen : {mean_clip:.4f}")   # Score de similarité moyen entre image et prompt
print(f"🎯 FID Score       : {fid_score:.4f}")   # Score de distance entre vraies et fausses images
