# Importation des bibliothèques nécessaires
from PIL import Image, ImageStat         # Pour des analyses plus poussées avec Pillow (non utilisée ici finalement)
import numpy as np                       # Pour les calculs statistiques (moyenne)
import cv2                               # OpenCV pour le traitement d’image (niveaux de gris, flou, etc.)

# Fonction qui évalue si une image est "acceptable" selon des critères de netteté et de luminosité
def is_image_acceptable(image_path: str, blur_threshold=100, brightness_range=(50, 220)) -> bool:
    """
    Évalue la qualité d’une image :
    - Vérifie qu’elle n’est pas floue (via variance du Laplacien)
    - Vérifie que la luminosité est dans un intervalle raisonnable

    Args:
        image_path (str): chemin vers l’image générée
        blur_threshold (float): seuil minimal de netteté (plus haut = plus strict)
        brightness_range (tuple): plage acceptable pour la luminosité moyenne (0 à 255)

    Returns:
        bool: True si l’image passe les contrôles qualité, False sinon
    """
    try:
        # Lecture de l’image avec OpenCV
        img_cv = cv2.imread(image_path)
        if img_cv is None:
            return False  # Échec de chargement

        # Conversion en niveaux de gris
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        # Mesure de la netteté via la variance du Laplacien (plus elle est élevée, plus l’image est nette)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        if laplacian_var < blur_threshold:
            return False  # Image trop floue

        # Mesure de la luminosité moyenne de l’image
        brightness = np.mean(gray)
        if brightness < brightness_range[0] or brightness > brightness_range[1]:
            return False  # Image trop sombre ou trop lumineuse

        return True  # Image considérée comme acceptable

    except Exception as e:
        # En cas d’erreur (fichier corrompu, image non lisible, etc.)
        print(f"Erreur lors du contrôle qualité : {e}")
        return False
