
# 🧠 Generative AI Pipeline – Texte & Image (CPU-Friendly)

Ce projet propose un pipeline d'intelligence artificielle automatisé permettant de :

- Générer du **texte ou des images** à partir de prompts utilisateurs
- Vérifier automatiquement la **qualité du contenu généré**
- Appliquer un **filtre éthique** pour exclure les contenus sensibles
- Fonctionner efficacement sur des machines **sans GPU**, optimisé pour le CPU

---

## 🔧 Architecture du pipeline

```
Prompt → Modèle de génération → Contrôle qualité → (Optionnel) Générateur d’image → Filtre éthique → Résultat final
```

---

## 📦 Technologies utilisées

| Module            | Modèles / Librairies                             |
|-------------------|--------------------------------------------------|
| Génération Texte  | `distilGPT2`, `T5-small`, `OPT-125M`, `transformers` |
| Résumé Texte      | `facebook/bart-base`, `distilBERT`               |
| Génération Image  | `VAE`, `DCGAN`, `DALL·E mini`, `AttnGAN`         |
| Filtrage Éthique  | Règles, classifieur simple                       |
| Automatisation    | `schedule`, `cron`, `Airflow`                    |
| Interface         | `ipywidgets`, `matplotlib`, `notebook`           |

---

## ⚙️ Installation

```bash
pip install torch torchvision transformers ipywidgets matplotlib nltk
```

---

## 🚀 Exemples d'utilisation

- Générer une image à partir d’une description : `"A futuristic African jungle city"`
- Générer un texte créatif ou un résumé contrôlé
- Créer un contenu illustré avec validation éthique

---

## 🛡️ Filtrage Éthique

Le pipeline inclut un module simple pour détecter les mots-clés interdits (violence, haine, racisme, etc.) et empêcher leur propagation.

---

## 📁 Arborescence du projet

```
📦 ia-generative-pipeline/
├── notebooks/
│   ├── texte_to_image_pipeline.ipynb
│   └── pipeline_gan_cifar10.ipynb
├── scripts/
│   └── image_generation.py
├── data/
│   └── prompts.txt
├── README.md
```

---

## 📌 Auteurs & Contributeurs

- Jean Pierre Rugina (Concepteur & développeur du pipeline)
- Basé sur des modèles open-source de Hugging Face, Microsoft, et la communauté IA

---

## 🧪 Prochaines étapes

- Intégration de CLIP pour image-text alignment
- Interface Web via Gradio ou Streamlit
- Export des résultats au format PDF/JSON

---

## 📄 Licence

Projet open-source sous licence MIT.
