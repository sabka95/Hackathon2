import streamlit as st
import os
import time
import base64

GENERATED_DIR = "images/generated"
PROMPT_FILE = "test_prompts.txt"
IMAGES_PER_PAGE = 3
AUTOPLAY_INTERVAL = 3  # secondes

def show_carousel():
    # Charger les prompts
    if not os.path.exists(PROMPT_FILE):
        st.warning("Aucun fichier de prompts trouvé.")
        return

    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        prompts = [line.strip() for line in f.readlines() if line.strip()]

    # Lister les fichiers d’images
    image_files = sorted([
        f for f in os.listdir(GENERATED_DIR)
        if f.endswith((".png", ".jpg")) and os.path.splitext(f)[0].isdigit()
    ], key=lambda x: int(os.path.splitext(x)[0]))

    total_images = len(image_files)
    if total_images == 0:
        st.warning("Aucune image générée à afficher.")
        return

    # Initialiser l'état
    if "carousel_index" not in st.session_state:
        st.session_state.carousel_index = 0
    if "carousel_autoplay" not in st.session_state:
        st.session_state.carousel_autoplay = True
    if "last_autoplay_time" not in st.session_state:
        st.session_state.last_autoplay_time = time.time()

    # Navigation manuelle
    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        if st.button("⬅️"):
            st.session_state.carousel_index = (st.session_state.carousel_index - 1) % total_images
            st.session_state.carousel_autoplay = False
    with col3:
        if st.button("➡️"):
            st.session_state.carousel_index = (st.session_state.carousel_index + 1) % total_images
            st.session_state.carousel_autoplay = False

    # Sélection des images à afficher
    current_images = [
        image_files[(st.session_state.carousel_index + i) % total_images]
        for i in range(IMAGES_PER_PAGE)
    ]

    cols = st.columns(IMAGES_PER_PAGE)
    for i, (col, img_file) in enumerate(zip(cols, current_images)):
        img_path = os.path.join(GENERATED_DIR, img_file)
        index = int(os.path.splitext(img_file)[0])
        caption = prompts[index] if index < len(prompts) else f"Image {index}"

        # Lire et encoder l’image en base64
        with open(img_path, "rb") as f:
            img_bytes = f.read()
        img_base64 = base64.b64encode(img_bytes).decode()

        # Affichage de l’image avec infobulle (attribut title)
        html_img = f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{img_base64}" title="{caption}" style="width: 100%; border-radius: 10px;">
            </div>
        """
        with col:
            st.markdown(html_img, unsafe_allow_html=True)

    # Autoplay
    if st.session_state.carousel_autoplay:
        if time.time() - st.session_state.last_autoplay_time > AUTOPLAY_INTERVAL:
            st.session_state.carousel_index = (st.session_state.carousel_index + 1) % total_images
            st.session_state.last_autoplay_time = time.time()
            st.experimental_rerun()
