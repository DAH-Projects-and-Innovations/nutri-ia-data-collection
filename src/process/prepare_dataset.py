import re
import shutil
from pathlib import Path

from sklearn.model_selection import train_test_split

from src.config.dataset import (
    RAW_IMAGES_DIR,
    AUGMENTED_IMAGES_DIR,
    TRAIN_DIR,
    VALIDATION_DIR,
    TRAIN_SPLIT,
    RANDOM_SEED,
    IMAGE_EXTENSIONS,
    CLASSES,
)


# ==========================================================
# Création de la structure train / validation
# ==========================================================

def create_output_directories():

    if TRAIN_DIR.exists():
        shutil.rmtree(TRAIN_DIR)

    if VALIDATION_DIR.exists():
        shutil.rmtree(VALIDATION_DIR)

    TRAIN_DIR.mkdir(parents=True, exist_ok=True)
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)

    for class_name in CLASSES:
        (TRAIN_DIR / class_name).mkdir(parents=True, exist_ok=True)
        (VALIDATION_DIR / class_name).mkdir(parents=True, exist_ok=True)

    print("✓ Structure train/validation recréée")


# ==========================================================
# Lecture des images
# ==========================================================

def get_images(folder: Path):

    return sorted(
        [
            img
            for img in folder.iterdir()
            if img.is_file()
            and img.suffix.lower() in IMAGE_EXTENSIONS
        ]
    )


# ==========================================================
# Affichage dataset original
# ==========================================================

def scan_original_dataset():

    print("\n========== DATASET ORIGINAL ==========\n")

    total = 0

    for class_name in CLASSES:

        images = get_images(RAW_IMAGES_DIR / class_name)

        print(f"{class_name:<15}: {len(images)} images")

        total += len(images)

    print("---------------------------------------")
    print(f"Total : {total} images\n")


# ==========================================================
# Split Train / Validation
# ==========================================================

def split_original_dataset():

    print("========== SPLIT ORIGINAL ==========\n")

    train_mapping = {}

    train_total = 0
    validation_total = 0

    for class_name in CLASSES:

        original_images = get_images(RAW_IMAGES_DIR / class_name)

        train_images, validation_images = train_test_split(
            original_images,
            train_size=TRAIN_SPLIT,
            random_state=RANDOM_SEED,
            shuffle=True,
        )

        train_mapping[class_name] = train_images

        train_folder = TRAIN_DIR / class_name
        validation_folder = VALIDATION_DIR / class_name

        for image in train_images:
            shutil.copy2(image, train_folder / image.name)

        for image in validation_images:
            shutil.copy2(image, validation_folder / image.name)

        train_total += len(train_images)
        validation_total += len(validation_images)

        print(
            f"{class_name:<15}"
            f"Train : {len(train_images):3d}"
            f"   Validation : {len(validation_images):3d}"
        )

    print("---------------------------------------")
    print(f"Train total      : {train_total}")
    print(f"Validation total : {validation_total}\n")

    return train_mapping


# ==========================================================
# Extraction de l'identifiant d'une image augmentée
# ==========================================================

def get_original_id(image: Path):
    """
    Retourne l'identifiant de l'image originale.

    Exemples

    IMG_CIV03_001.jpg
        -> img_civ03_001

    IMG_CIV03_001_pil_env...
        -> img_civ03_001

    foutou_001.jpg
        -> foutou_001

    foutou_001_sd...
        -> foutou_001
    """

    stem = image.stem.lower()

    match = re.match(
        r"^(img_[a-z0-9]+_\d{3}|[a-z-]+_\d{3})",
        stem,
    )

    if match:
        return match.group(1)

    return stem

# ==========================================================
# Ajout des augmentations
# ==========================================================

def add_augmented_images(train_mapping):

    print("========== AJOUT DES IMAGES AUGMENTÉES ==========\n")

    total_augmented = 0

    for class_name in CLASSES:

        augmented_dir = AUGMENTED_IMAGES_DIR / class_name

        if not augmented_dir.exists():
            print(f"{class_name:<15}: 0 image augmentée")
            continue

        train_folder = TRAIN_DIR / class_name

        # identifiants des images originales présentes dans le train
        train_ids = {
            get_original_id(img)
            for img in train_mapping[class_name]
        }

        copied = 0

        for aug_image in get_images(augmented_dir):

            image_id = get_original_id(aug_image)

            if image_id in train_ids:

                shutil.copy2(
                    aug_image,
                    train_folder / aug_image.name,
                )

                copied += 1

        total_augmented += copied

        print(f"{class_name:<15}: +{copied} images")

    print("---------------------------------------")
    print(f"Total ajouté : {total_augmented}\n")

# ==========================================================
# Résumé final
# ==========================================================

def print_final_summary():

    print("\n========== DATASET FINAL ==========\n")

    train_total = 0
    validation_total = 0

    for class_name in CLASSES:

        train_count = len(get_images(TRAIN_DIR / class_name))
        validation_count = len(get_images(VALIDATION_DIR / class_name))

        train_total += train_count
        validation_total += validation_count

        print(
            f"{class_name:<15}"
            f"Train : {train_count:4d}"
            f"   Validation : {validation_count:3d}"
        )

    print("---------------------------------------")
    print(f"Train final      : {train_total}")
    print(f"Validation final : {validation_total}")


# ==========================================================
# Main
# ==========================================================

def main():

    create_output_directories()

    scan_original_dataset()

    train_mapping = split_original_dataset()

    add_augmented_images(train_mapping)

    print_final_summary()


if __name__ == "__main__":
    main()