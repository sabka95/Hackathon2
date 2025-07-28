# Génération multiple de textes et d'images avec GPT-2 et Stable Diffusion + Évaluation
from transformers import GPT2LMHeadModel, GPT2Tokenizer, MarianMTModel, MarianTokenizer
from diffusers import StableDiffusionPipeline
from PIL import Image
import torch
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer

# Chargement des modèles
modele_texte_tokenizer = GPT2Tokenizer.from_pretrained("gpt2-medium")
modele_texte = GPT2LMHeadModel.from_pretrained("gpt2-medium").eval()

traducteur_tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-fr-en")
traducteur_model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-fr-en")

pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

# Liste de mots-clés sensibles
mots_interdits = ["haine", "violence", "terrorisme", "discrimination", "sexe", "guerre", "drogue"]

# Fonctions d'évaluation BLEU et ROUGE
smoothie = SmoothingFunction().method4
rouge = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)

def contient_contenu_sensible(texte, mots):
    texte_min = texte.lower()
    return any(mot in texte_min for mot in mots)

# Entrée utilisateur
entree = "Dans le futur, les villes africaines seront"
nombre_textes = 3
images_par_texte = 2

# Boucle de génération
for i in range(nombre_textes):
    print(f"\n--- Génération {i+1} ---")
    tokens_entree = modele_texte_tokenizer.encode(entree, return_tensors="pt")
    with torch.no_grad():
        sortie = modele_texte.generate(
            tokens_entree,
            max_length=70,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            temperature=0.8,
            top_k=50,
            top_p=0.95
        )

    texte_genere = modele_texte_tokenizer.decode(sortie[0], skip_special_tokens=True)
    print("\nTexte généré :\n", texte_genere)

    # Évaluation de la qualité
    reference = entree.split()
    candidate = texte_genere.split()
    bleu_score = sentence_bleu([reference], candidate, smoothing_function=smoothie)
    rouge_score = rouge.score(entree, texte_genere)
    print(f"\n📊 Évaluation : BLEU = {bleu_score:.4f}, ROUGE-1 = {rouge_score['rouge1'].fmeasure:.4f}, ROUGE-L = {rouge_score['rougeL'].fmeasure:.4f}")

    if contient_contenu_sensible(texte_genere, mots_interdits):
        print("⚠️ Contenu sensible détecté. Aucune image ne sera générée.")
        continue

    # Traduction du texte en anglais
    encoded_text = traducteur_tokenizer([texte_genere], return_tensors="pt", padding=True)
    translated = traducteur_model.generate(**encoded_text)
    prompt_en = traducteur_tokenizer.decode(translated[0], skip_special_tokens=True)

    # Génération d’images
    prompts = [prompt_en] * images_par_texte
    images = pipe(prompts).images

    for j, img in enumerate(images):
        img.show(title=f"Texte {i+1} - Image {j+1}")

    print("Prompt utilisé pour les images :", prompt_en)
