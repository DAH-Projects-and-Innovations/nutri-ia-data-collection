# scripts/merge_augmented.py

import shutil
from pathlib import Path

dossier_reel = Path("data/raw/images")
dossier_augmente = Path("data/raw/augmented_images")

mapping = {
    "Alloco": "alloco",
    "Foutou": "foutou",
    "Kedjenou": "kedjenou",
    "Mafe": "mafe",
    "Thieboudienne": "thieboudiene",
    "Yassa Poulet": "yassa-poulet",
}

for plat_aug in dossier_augmente.iterdir():

    if not plat_aug.is_dir():
        continue

    nom_destination = mapping.get(plat_aug.name)

    if not nom_destination:
        print(f"Dossier non reconnu : {plat_aug.name}")
        continue

    destination = dossier_reel / nom_destination
    destination.mkdir(parents=True, exist_ok=True)

    images = (
        list(plat_aug.glob("*.jpg"))
        + list(plat_aug.glob("*.jpeg"))
        + list(plat_aug.glob("*.png"))
    )

    for img in images:

        dest_fichier = destination / img.name

        if not dest_fichier.exists():
            shutil.copy2(img, dest_fichier)
            print(f"Copié : {img.name} -> {nom_destination}")

print("Fusion terminée.")