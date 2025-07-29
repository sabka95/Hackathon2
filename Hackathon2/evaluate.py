import os
from PIL import Image
import torch
import torchvision.transforms as T
from torchmetrics.image.fid import FrechetInceptionDistance
from torchvision.transforms.functional import pil_to_tensor
import open_clip

# === CONFIGURATION ===
GENERATED_DIR = "images/generated"
REAL_DIR = "images/real"  # Dossier avec images réelles
PROMPT_FILE = "test_prompts.txt"

# === PRÉTRAITEMENTS ===
transform_fid = T.Compose([
    T.Resize((299, 299)),
    T.ToTensor()
])

# FID
fid = FrechetInceptionDistance(feature=64)

# CLIP
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, _, preprocess_clip = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
tokenizer = open_clip.get_tokenizer('ViT-B-32')
clip_model = clip_model.to(device)

# === AJOUT DES IMAGES RÉELLES POUR LE FID ===
real_images = sorted([
    f for f in os.listdir(REAL_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg"))
])

for fname in real_images:
    img_path = os.path.join(REAL_DIR, fname)
    try:
        img = Image.open(img_path).convert("RGB").resize((299, 299))
        tensor = pil_to_tensor(img)  # dtype: uint8
        fid.update(tensor.unsqueeze(0), real=True)
    except Exception as e:
        print(f"❌ Erreur image réelle '{fname}' : {e}")

# === CHARGEMENT DES PROMPTS ===
with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    prompts = [line.strip() for line in f.readlines() if line.strip()]

# === ÉVALUATION DES IMAGES GÉNÉRÉES ===
clip_scores = []
total = len(prompts)

print(f"\n🔍 Évaluation sur {total} prompts...")

for i, prompt in enumerate(prompts):
    img_path = os.path.join(GENERATED_DIR, f"{i}.png")

    if not os.path.exists(img_path):
        print(f"❌ Image manquante : {img_path}")
        continue

    try:
        # FID
        image_pil = Image.open(img_path).convert("RGB").resize((299, 299))
        img_fid = pil_to_tensor(image_pil)
        fid.update(img_fid.unsqueeze(0), real=False)

        # CLIP
        image = preprocess_clip(image_pil).unsqueeze(0).to(device)
        text = tokenizer([prompt]).to(device)

        with torch.no_grad():
            image_feat = clip_model.encode_image(image)
            text_feat = clip_model.encode_text(text)
            score = torch.nn.functional.cosine_similarity(image_feat, text_feat)
            clip_scores.append(score.item())

        print(f"[{i+1}/{total}] ✅ {img_path} | CLIPScore: {score.item():.4f}")

    except Exception as e:
        print(f"[{i+1}/{total}] ❌ Erreur sur '{img_path}' : {e}")

# === RÉSULTATS ===
mean_clip = sum(clip_scores) / len(clip_scores) if clip_scores else 0
fid_score = fid.compute().item()

print("\n=== 🔚 RÉSULTATS FINAUX ===")
print(f"🎯 CLIPScore moyen : {mean_clip:.4f}")
print(f"🎯 FID Score       : {fid_score:.4f}")

