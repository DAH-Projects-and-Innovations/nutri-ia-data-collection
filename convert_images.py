"""
Script de conversion d'images en JPEG
Convertit tous les fichiers .png, .webp, .jpeg d'un dossier en .jpg
et supprime les fichiers originaux après conversion.
"""
import os
import sys
from pathlib import Path
from PIL import Image

def convert_to_jpg(folder_path):
    folder = Path(folder_path)
    if not folder.exists():
        print(f"Erreur : le dossier {folder_path} n'existe pas.")
        sys.exit(1)

    extensions_a_convertir = [".png", ".webp", ".jpeg", ".PNG", ".WEBP", ".JPEG"]
    converted_count = 0
    error_count = 0

    for file in folder.iterdir():
        if file.is_file() and file.suffix in extensions_a_convertir:
            new_path = file.with_suffix(".jpg")
            try:
                with Image.open(file) as img:
                    # Convertir en RGB (nécessaire pour les PNG/WEBP avec transparence)
                    rgb_img = img.convert("RGB")
                    rgb_img.save(new_path, "JPEG", quality=95)
                print(f"Converti : {file.name} -> {new_path.name}")
                converted_count += 1
                # Supprimer l'original (sauf si c'était déjà un .jpg)
                file.unlink()
            except Exception as e:
                print(f"Erreur avec {file.name} : {e}")
                error_count += 1

    print(f"\n--- Resume ---")
    print(f"Images converties : {converted_count}")
    print(f"Erreurs : {error_count}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python convert_images.py <chemin_du_dossier>")
        sys.exit(1)
    convert_to_jpg(sys.argv[1])
