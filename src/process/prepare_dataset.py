from src.config.dataset import (
    TRAIN_DIR,
    VALIDATION_DIR,
)

from pathlib import Path
import shutil


def reset_directory(directory: Path) -> None:
    """Supprime et recrée un répertoire."""
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir(parents=True, exist_ok=True)


def create_processed_structure() -> None:
    """Crée la structure train/validation."""
    reset_directory(TRAIN_DIR)
    reset_directory(VALIDATION_DIR)

    print(f"Train directory created: {TRAIN_DIR}")
    print(f"Validation directory created: {VALIDATION_DIR}")


if __name__ == "__main__":
    create_processed_structure()