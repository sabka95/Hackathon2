# Importation des modules nécessaires
import streamlit as st                          # Pour créer une application web interactive
from PIL import Image                           # Pour ouvrir et afficher des images
from generate import generate_image_from_prompt # Fonction personnalisée pour générer une image à partir d’un prompt
from carousel import show_carousel              # Fonction personnalisée pour afficher un carrousel d’images générées

# Configuration de la page Streamlit (titre et disposition centrée)
st.set_page_config(page_title="Text-to-Image Generator", layout="centered")

# Affichage du titre et d'une description explicative
st.title("🖼️ Générateur d'Images à partir d’un Prompt")
st.markdown("Entrez un **prompt textuel** décrivant une image à générer. Exemple : *a red bird with long tail*")

# Affichage du carrousel des images précédemment générées
st.subheader("🎞️ Carrousel des images générées précédemment")
show_carousel()

# Champ de saisie du prompt utilisateur
prompt = st.text_input("Votre prompt ici :", placeholder="Ex: a small green bird with a yellow beak")

# Bouton de génération d’image
if st.button("🎨 Générer une image"):
    if prompt.strip() == "":
        st.warning("Veuillez entrer un prompt.")  # Avertissement si le champ est vide
    else:
        with st.spinner("Génération de l'image en cours..."):  # Indicateur de chargement
            try:
                # Appel de la fonction de génération : retourne le chemin de l’image et le prompt enrichi
                image_path, enriched_prompt = generate_image_from_prompt(prompt)

                # Affichage des résultats
                st.success("✅ Image générée avec succès !")
                st.image(Image.open(image_path), caption="🖼️ Image générée", use_container_width=True)
                st.markdown(f"**Prompt enrichi utilisé :** {enriched_prompt}")
                st.markdown(f"📁 *Image enregistrée dans : `{image_path}`*")

            except ValueError as e:
                st.error(str(e))  # Gestion des erreurs liées à un mauvais prompt ou autres erreurs métier
            except Exception as e:
                st.error(f"❌ Une erreur est survenue : {str(e)}")  # Gestion des erreurs inattendues




