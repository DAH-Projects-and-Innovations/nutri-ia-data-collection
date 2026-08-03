from pathlib import Path

from src.config.dataset import (
    RAW_IMAGES_DIR,
    TRAIN_DIR,
    VALIDATION_DIR,
    IMAGE_EXTENSIONS,
    CLASSES,
)

# Création des dossiers train et validation
TRAIN_DIR.mkdir(parents=True, exist_ok=True)
VALIDATION_DIR.mkdir(parents=True, exist_ok=True)

print(f"Train directory created: {TRAIN_DIR}")
print(f"Validation directory created: {VALIDATION_DIR}")

print("\n========== Original Dataset ==========")

total_images = 0

for class_name in CLASSES:
    class_dir = RAW_IMAGES_DIR / class_name

    if not class_dir.exists():
        print(f"[ERREUR] Dossier introuvable : {class_dir}")
        continue

    image_files = [
        img for img in class_dir.iterdir()
        if img.suffix in IMAGE_EXTENSIONS
    ]

    print(f"{class_name:<15}: {len(image_files)} images")

    total_images += len(image_files)

print("--------------------------------------")
print(f"Total : {total_images} images")