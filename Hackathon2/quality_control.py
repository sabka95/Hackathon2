from PIL import Image, ImageStat
import numpy as np
import cv2

def is_image_acceptable(image_path: str, blur_threshold=100, brightness_range=(50, 220)) -> bool:
    """
    Évalue la qualité d’une image :
    - Vérifie qu’elle n’est pas floue (via Laplacian)
    - Vérifie que la luminosité est dans un intervalle raisonnable
    
    Args:
        image_path (str): chemin vers l’image générée
        blur_threshold (float): seuil minimal de netteté
        brightness_range (tuple): plage de luminosité moyenne acceptable

    Returns:
        bool: True si l’image est acceptable, False sinon
    """
    try:
        # Chargement image + conversion en niveaux de gris
        img_cv = cv2.imread(image_path)
        if img_cv is None:
            return False

        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        # Test de netteté (flou) via Laplacian
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        if laplacian_var < blur_threshold:
            return False

        # Test de luminosité
        brightness = np.mean(gray)
        if brightness < brightness_range[0] or brightness > brightness_range[1]:
            return False

        return True

    except Exception as e:
        print(f"Erreur lors du contrôle qualité : {e}")
        return False
