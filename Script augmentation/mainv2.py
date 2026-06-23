# =========================
# IMPORT DES BIBLIOTHÈQUES
# =========================

from pathlib import Path   # pour gérer les chemins de fichiers/dossiers proprement
import pandas as pd        # pour créer et sauvegarder le fichier Excel
import cv2                 # pour lire et écrire les images
import albumentations as A # pour faire les augmentations d’images
from tqdm import tqdm      # pour afficher une barre de progression
import random              # pour générer des valeurs aléatoires (annotations)


# =========================
# CONFIGURATION DU PROJET
# =========================

# dossier contenant les images originales
INPUT_IMAGES = Path("foutou/")

# dossier où seront stockées les images augmentées
OUTPUT_IMAGES = Path("foutouaugmented/")

# fichier Excel de sortie contenant les annotations
OUTPUT_ANNOTATIONS = "foutou_site_augmented.xlsx"

# nombre d’images augmentées à générer par image originale
N_AUGMENTATIONS = 10

# création automatique du dossier de sortie s’il n’existe pas
OUTPUT_IMAGES.mkdir(parents=True, exist_ok=True)


# =========================
# PIPELINE D'AUGMENTATION D’IMAGES
# =========================

# Ce bloc définit toutes les transformations appliquées aux images

transform = A.Compose([

    # rotation de l’image jusqu’à ±20°
    A.Rotate(limit=20, border_mode=cv2.BORDER_REFLECT, p=0.8),

    # zoom / déplacement léger de l’image
    A.Affine(
        scale=(0.85, 1.15),              # zoom in / zoom out
        translate_percent=(-0.05, 0.05), # déplacement horizontal/vertical
        p=0.8
    ),

    # modification de la luminosité et du contraste
    A.RandomBrightnessContrast(
        brightness_limit=0.3,
        contrast_limit=0.3,
        p=0.8
    ),

    # modification des couleurs (teinte, saturation, etc.)
    A.HueSaturationValue(
        hue_shift_limit=5,
        sat_shift_limit=25,
        val_shift_limit=15,
        p=0.7
    ),

    # changement de perspective (simule un autre angle de prise de vue)
    A.Perspective(scale=(0.03, 0.08), p=0.6),

    # flou léger (simule mauvaise mise au point)
    A.GaussianBlur(blur_limit=(3, 5), p=0.3),

    # ajout de bruit (simule caméra de mauvaise qualité)
    A.GaussNoise(std_range=(0.05, 0.15), p=0.3)

])


# =========================
# FONCTION POUR CRÉER LES ANNOTATIONS
# =========================

def generate_annotation(image_id, original=True):

    # si image originale → vue "Dessus"
    # sinon → angle aléatoire
    angle = "Dessus" if original else random.choice(
        ["Dessus", "Leger_angle", "45_degres"]
    )

    # création d’un dictionnaire représentant une ligne du dataset
    return {
        "image_id": image_id,

        # informations fixes sur le plat
        "nom_plat": "foutou",
        "pays": "Cote_d'Ivoire",
        "categorie": "plat_principal",

        # caractéristiques visuelles
        "angle_vue": angle,
        "luminosite": "Bonne",      # simplifié (non calculé ici)
        "qualite_image": "Bonne",   # simplifié (non calculé ici)
        "portion": "Normale",

        # informations sémantiques
        "ingredients_visibles": "Sauce, viande, accompagnement",
        "source": "unknown",

        # niveau de confiance de l’annotation
        "confiance_annotation": 90
    }


# =========================
# LISTE DES IMAGES
# =========================

# récupère toutes les images dans le dossier foutou/
image_files = list(INPUT_IMAGES.glob("*.*"))

# liste qui contiendra toutes les annotations finales
all_annotations = []

print(f"{len(image_files)} images trouvées")


# =========================
# PIPELINE PRINCIPAL
# =========================

# boucle sur toutes les images originales
for img_path in tqdm(image_files):

    # lecture de l’image
    image = cv2.imread(str(img_path))

    # si l’image est invalide → on passe à la suivante
    if image is None:
        continue

    # nom de l’image sans extension (ex: IMG_001)
    image_id = img_path.stem


    # =========================
    # AJOUT DE L’IMAGE ORIGINALE
    # =========================

    all_annotations.append(
        generate_annotation(image_id, original=True)
    )

    # sauvegarde de l’image originale dans le dossier de sortie
    cv2.imwrite(
        str(OUTPUT_IMAGES / f"{image_id}.jpg"),
        image
    )


    # =========================
    # GÉNÉRATION DES IMAGES AUGMENTÉES
    # =========================

    for i in range(N_AUGMENTATIONS):

        # application des transformations sur l’image
        aug = transform(image=image)["image"]

        # création d’un nouvel ID pour l’image augmentée
        new_id = f"{image_id}_aug_{i+1:02d}"

        # sauvegarde de l’image augmentée
        cv2.imwrite(
            str(OUTPUT_IMAGES / f"{new_id}.jpg"),
            aug
        )

        # création de l’annotation correspondante
        all_annotations.append(
            generate_annotation(new_id, original=False)
        )


# =========================
# EXPORT DU FICHIER EXCEL
# =========================

# conversion de toutes les annotations en tableau
df = pd.DataFrame(all_annotations)

# sauvegarde dans un fichier Excel
df.to_excel(OUTPUT_ANNOTATIONS, index=False)


# =========================
# FIN DU PROGRAMME
# =========================

print("\n=== TERMINÉ ===")
print(f"Images générées : {len(all_annotations)}")
print(f"Excel : {OUTPUT_ANNOTATIONS}")
print(f"Dossier images : {OUTPUT_IMAGES}")