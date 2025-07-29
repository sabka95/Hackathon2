# Importation des bibliothèques nécessaires
import streamlit as st      # Pour créer l’interface utilisateur web
import os                   # Pour la gestion des fichiers et répertoires
import time                 # Pour gérer les délais entre affichages automatiques
import base64               # Pour encoder les images en base64 et les intégrer dans du HTML

# Constantes de configuration
GENERATED_DIR = "images/generated"     # Dossier où sont stockées les images générées
PROMPT_FILE = "test_prompts.txt"       # Fichier contenant les prompts texte associés aux images
IMAGES_PER_PAGE = 3                    # Nombre d’images affichées simultanément dans le carrousel
AUTOPLAY_INTERVAL = 3                  # Intervalle d'autoplay en secondes (non utilisé ici directement)

# Fonction principale pour afficher le carrousel
def show_carousel():
    # Vérifie si le fichier de prompts existe, sinon affiche un message d’avertissement
    if not os.path.exists(PROMPT_FILE):
        st.warning("Aucun fichier de prompts trouvé.")
        return

    # Lit tous les prompts texte dans une liste (en retirant les lignes vides)
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        prompts = [line.strip() for line in f.readlines() if line.strip()]

    # Liste les fichiers d’images valides (fichiers .png ou .jpg dont le nom est un nombre)
    image_files = sorted([
        f for f in os.listdir(GENERATED_DIR)
        if f.endswith((".png", ".jpg")) and os.path.splitext(f)[0].isdigit()
    ], key=lambda x: int(os.path.splitext(x)[0]))  # Trie par numéro croissant

    total_images = len(image_files)
    if total_images == 0:
        st.warning("Aucune image générée à afficher.")
        return

    # Initialisation de l’état de session Streamlit pour le carrousel
    if "carousel_index" not in st.session_state:
        st.session_state.carousel_index = 0  # Index de départ
    if "carousel_autoplay" not in st.session_state:
        st.session_state.carousel_autoplay = True  # Mode autoplay activé par défaut
    if "last_autoplay_time" not in st.session_state:
        st.session_state.last_autoplay_time = time.time()  # Timestamp pour autoplay (non utilisé ici)

    # Création des boutons de navigation (précédent/suivant)
    col1, col2, col3 = st.columns([1, 8, 1])  # Mise en page avec 3 colonnes (gauche-centre-droite)
    with col1:
        if st.button("⬅️"):
            # Revenir à l’image précédente (avec boucle circulaire)
            st.session_state.carousel_index = (st.session_state.carousel_index - 1) % total_images
            st.session_state.carousel_autoplay = False  # Désactive l’autoplay si action manuelle
    with col3:
        if st.button("➡️"):
            # Passer à l’image suivante
            st.session_state.carousel_index = (st.session_state.carousel_index + 1) % total_images
            st.session_state.carousel_autoplay = False

    # Sélectionne les images à afficher (IMAGES_PER_PAGE successives à partir de l’index courant)
    current_images = [
        image_files[(st.session_state.carousel_index + i) % total_images]
        for i in range(IMAGES_PER_PAGE)
    ]

    # Affiche les images dans des colonnes Streamlit
    cols = st.columns(IMAGES_PER_PAGE)
    for i, (col, img_file) in enumerate(zip(cols, current_images)):
        img_path = os.path.join(GENERATED_DIR, img_file)
        index = int(os.path.splitext(img_file)[0])  # Extrait l’indice numérique depuis le nom du fichier
        caption = prompts[index] if index < len(prompts) else f"Image {index}"  # Récupère le prompt correspondant

        # Lecture de l’image et encodage en base64 (nécessaire pour affichage HTML)
        with open(img_path, "rb") as f:
            img_bytes = f.read()
        img_base64 = base64.b64encode(img_bytes).decode()

        # Génère du HTML pour afficher l’image avec un style (bord arrondi, infobulle avec le prompt)
        html_img = f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{img_base64}" title="{caption}" style="width: 100%; border-radius: 10px;">
            </div>
        """
        with col:
            # Affiche l’image encodée en HTML dans Streamlit
            st.markdown(html_img, unsafe_allow_html=True)
