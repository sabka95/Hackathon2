# 🎨 Text-to-Image Generator

Ce projet est une application **Streamlit** qui génère des images à partir de descriptions textuelles (**prompts**) en utilisant un modèle de génération (comme **Stable Diffusion**). Il inclut des modules d'enrichissement, de filtrage, d'évaluation, et une interface interactive pour améliorer l'expérience utilisateur.

## 🚀 Fonctionnalités principales

- **Génération d'images** à partir de prompts textuels
- **Filtrage des prompts** (modèle BERT pour la détection de contenu toxique)
- **Enrichissement des prompts** (modèle FLAN-T5)
- **Évaluation automatique** via **CLIPScore** et **FID**
- **Carrousel interactif** des images générées avec défilement automatique
- **Feedback utilisateur** (J’aime / Regénérer) pour affiner l'expérience
- **Stockage vectoriel** des images appréciées pour une personnalisation future via un système **RAG**

## 📂 Structure du projet

```
.
├── app.py                   # Application principale Streamlit
├── generate.py             # Génération d'image à partir du prompt
├── attngan_generate.py     # Ou remplacement par Stable Diffusion local
├── prompt_enricher.py      # Enrichissement du prompt avec FLAN-T5
├── filter_prompt.py        # Filtrage des prompts toxiques avec Detoxify
├── quality_control.py      # Boutons de feedback utilisateur
├── evaluate.py             # Évaluation via CLIPScore et FID
├── carousel.py             # Carrousel d'images Streamlit
├── vector_store.py         # (optionnel) Stockage pour RAG futur
├── images/
│   └── generated/          # Images générées
├── test_prompts.txt        # Liste des prompts utilisés
├── requirements.txt        # Dépendances du projet
└── README.md               # Ce fichier
```

## 📦 Installation

1. **Cloner le projet** :
   ```bash
   git clone https://github.com/ton-projet/image-generator.git
   cd image-generator
   ```

2. **Créer un environnement virtuel** :
   ```bash
   conda create -n chatbot python=3.10
   conda activate chatbot
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer l'application** :
   ```bash
   streamlit run app.py
   ```

## 🧠 Modèles utilisés

| Tâche                      | Modèle utilisé                     |
|---------------------------|-------------------------------------|
| Génération d'images       | Stable Diffusion (local)            |
| Enrichissement de prompt  | FLAN-T5 (via Transformers)          |
| Filtrage de contenu       | Detoxify (BERT)                     |
| Similarité texte-image    | OpenCLIP (ViT-B-32)                 |
| Évaluation de qualité     | CLIPScore & FID (torchmetrics)      |
| Affichage interactif      | Streamlit + HTML (carrousel)        |

## 🧪 Exemple de prompt

```
a futuristic city at sunset
a cozy cabin in the snow
a dog with wings and a rainbow tail dancing on the moon
```

## 📘 À venir

- Intégration du système **RAG** pour personnaliser la génération d'images
- Implémentation au carousel d'images généré partir des tendances google
- Export des images préférées

## 👤 Auteurs

Sabri KACI 
Jean-pierre RUGINA 
Projet réalisé dans le cadre du Hackathon Generative AI – Juillet 2025
