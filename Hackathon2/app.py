import streamlit as st
from PIL import Image
from generate import generate_image_from_prompt
from carousel import show_carousel

st.set_page_config(page_title="Text-to-Image Generator", layout="centered")

st.title("🖼️ Générateur d'Images à partir d’un Prompt")
st.markdown("Entrez un **prompt textuel** décrivant une image à générer. Exemple : *a red bird with long tail*")

st.subheader("🎞️ Carrousel des images générées précédemment")
show_carousel()

prompt = st.text_input("Votre prompt ici :", placeholder="Ex: a small green bird with a yellow beak")

if st.button("🎨 Générer une image"):
    if prompt.strip() == "":
        st.warning("Veuillez entrer un prompt.")
    else:
        with st.spinner("Génération de l'image en cours..."):
            try:
                image_path, enriched_prompt = generate_image_from_prompt(prompt)
                st.success("✅ Image générée avec succès !")

                st.image(Image.open(image_path), caption="🖼️ Image générée", use_container_width=True)
                st.markdown(f"**Prompt enrichi utilisé :** {enriched_prompt}")
                st.markdown(f"📁 *Image enregistrée dans : `{image_path}`*")

            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"❌ Une erreur est survenue : {str(e)}")



