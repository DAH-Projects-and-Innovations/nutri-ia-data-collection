# Nutri-IA : Collecte et Traitement de Données

Ce dépôt contient le code et l'infrastructure nécessaires pour la collecte, le nettoyage et la préparation des données destinées à l'Assistant IA de Nutrition.

## 📁 Architecture du projet

```text
nutri-ia-data-collection/
├── data
│   ├── external       <- Données provenant de tiers (API, bases publiques).
│   ├── interim        <- Données en cours de traitement/nettoyage.
│   │   ├── images     <- Images en cours de traitement.
│   │   └── tabular    <- Données structurées en cours de nettoyage.
│   ├── processed      <- Données finales, prêtes à être exploitées ou utilisées pour l'entraînement.
│   │   ├── images     <- Images redimensionnées, annotées ou normalisées.
│   │   └── tabular    <- Fichiers structurés nettoyés (CSV, JSON, etc.).
│   └── raw            <- Données brutes, immuables (la source de vérité).
│       ├── images     <- Photos originales brutes (aliments, étiquettes).
│       └── tabular    <- Fichiers structurés bruts originaux (CSV, JSON).
├── docs               <- Documentation du projet (dictionnaire de données, notes méthodologiques).
├── notebooks          <- Notebooks d'exploration de données et de tests rapides.
├── src                <- Code source.
│   ├── collect        <- Scripts de collecte (Scraping, requêtes API).
│   ├── config         <- Configuration du projet (chemins, paramètres).
│   ├── process        <- Scripts de traitement, de fusion et de nettoyage.
│   └── utils          <- Fonctions utilitaires communes.
├── tests              <- Tests unitaires.
├── main.py            <- Point d'entrée principal.
├── pyproject.toml     <- Gestion des dépendances (via uv).
└── .gitignore         <- Fichiers et dossiers ignorés par Git.
```

## 🚀 Installation

Ce projet utilise [uv](https://github.com/astral-sh/uv) pour la gestion rapide des dépendances.

1. **Cloner le dépôt :**

   ```bash
   git clone https://github.com/DAH-Projects-and-Innovations/nutri-ia-data-collection.git
   cd nutri-ia-data-collection
   ```

2. **Installer les dépendances :**

   ```bash
   uv sync
   ```

3. **Activer l'environnement virtuel :**
   ```bash
   source .venv/bin/activate
   ```
