from pathlib import Path

# ==========================
# Racine du projet
# ==========================
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ==========================
# Dossiers des données
# ==========================
RAW_IMAGES_DIR = PROJECT_ROOT / "data" / "raw" / "images"
AUGMENTED_IMAGES_DIR = PROJECT_ROOT / "data" / "interim" / "augmented_images"
PROCESSED_IMAGES_DIR = PROJECT_ROOT / "data" / "processed" / "images"

# ==========================
# Répertoires générés
# ==========================
TRAIN_DIR = PROCESSED_IMAGES_DIR / "train"
VALIDATION_DIR = PROCESSED_IMAGES_DIR / "validation"

# ==========================
# Paramètres du dataset
# ==========================
TRAIN_SPLIT = 0.8
RANDOM_SEED = 42

# ==========================
# Extensions autorisées
# ==========================
IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png",
    ".JPG", ".JPEG", ".PNG"
}

# ==========================
# Classes
# ==========================
CLASSES = [
    "alloco",
    "foutou",
    "kedjenou",
    "mafe",
    "thieboudiene",
    "yassa-poulet",
]