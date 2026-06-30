# README — Augmentation de Dataset Mets Africains

## Objectif

Multiplier un dataset de 1000 photos de mets africains (10 plats × 100 images) en **11 000 images** (1000 originales + 10 000 générées), pour entraîner un modèle de reconnaissance alimentaire robuste.

**Répartition par image originale :** 7 transformations visuelles (PIL) + 3 ajouts d'ingrédients (IA générative) = 10 nouvelles images.

---

## Structure du notebook — bloc par bloc

### Bloc 1 — Installation des dépendances
Installe `diffusers`, `torch`, `Pillow`, etc. Nécessaire une seule fois par session Colab.

### Bloc 2 — Vérification GPU
Confirme que le GPU T4 gratuit de Colab est actif. **Sans GPU, le bloc SD (ajouts IA) ne fonctionnera pas** — il faut activer `Exécution > Modifier le type d'exécution > GPU T4` avant de lancer.

### Bloc 3 — Upload des fichiers
Charge le fichier Excel d'annotations et le dossier d'images depuis ton ordinateur vers l'environnement Colab.

### Bloc 4 — Configuration
Variables centrales : nom du fichier Excel, dossier des images, taille de sortie. C'est le seul bloc à modifier si tu changes de dataset.

### Bloc 5 — Les  transformations PIL
Fonctions de traitement d'image classique (rotation, recadrage, luminosité, contraste, teinte). Rapides (millisecondes), ne nécessitent pas de GPU, et ne changent jamais le contenu du plat — uniquement son apparence photographique.

> **💡 Évolution future (Prochaine étape) :** Pour optimiser le stockage et ne pas figer les transformations en amont, l'objectif à terme est de remplacer ce traitement statique par un pipeline **Albumentations** intégré directement dans le `DataLoader` PyTorch. Cela permettra de générer des variations (luminosité, flous, micro-rotations) à la volée et à l'infini à chaque *epoch*, sans encombrer l'espace disque.

### Bloc 6 — Détection du plat + catalogue des ajouts SD
- `detecter_plat()` : identifie le plat **uniquement à partir du nom du fichier image**, normalisé (accents et séparateurs retirés) pour éviter toute erreur de lecture.
- `SD_AJOUTS` : dictionnaire contenant, pour chacun des 10 plats, 3 prompts décrivant un ingrédient ou élément à ajouter dans l'image.

### Bloc 7 — Chargement du modèle Stable Diffusion Inpainting
Télécharge et charge le modèle d'IA générative (une fois par session). C'est l'étape la plus longue (~2-3 minutes).

### Bloc 8 — Fonctions d'inpainting
Génère le masque (zone où l'IA va dessiner) et applique le prompt correspondant sur cette zone, en laissant le reste de l'image intact.

### Bloc 9 — Boucle principale de génération
Parcourt toutes les images, applique les 7 transformations PIL puis les 3 ajouts SD, sauvegarde les résultats et met à jour le fichier Excel d'annotations avec les nouvelles lignes.

### Bloc 10 — Export final
Sauvegarde le fichier Excel complet (1000 lignes originales + 10 000 lignes générées) avec les colonnes additionnelles (`image_origine`, `type_transformation`, `prompt_utilise`).

---

## Pertinence des modifications choisies

### Pourquoi 7 transformations PIL et pas plus ?

Les transformations géométriques et photométriques (rotation, zoom léger, luminosité, contraste, balance des couleurs) simulent les variations naturelles qu'un modèle rencontrera en conditions réelles : photos prises avec des téléphones différents, des éclairages de restaurant variés, des angles de prise de vue différents. Sept variantes couvrent un espace de variation suffisamment large sans dupliquer l'information utile — au-delà, les transformations deviennent redondantes statistiquement.

### Pourquoi 3 ajouts IA et pas plus ?

Les ajouts génératifs (Stable Diffusion) sont plus coûteux en calcul et risquent d'introduire des artefacts visuels (déformations, incohérences d'éclairage) si on en abuse. Trois ajouts par image suffisent à introduire de la **variabilité de contenu réel** : présence ou absence d'un accompagnement, d'une viande, d'un assaisonnement — ce qui correspond aux variations qu'on observe réellement entre deux assiettes du même plat servies à des moments différents.

### Pourquoi des prompts spécifiques à chaque plat ?

Un ajout générique ("ajoute de la nourriture") produirait des résultats incohérents culturellement et culinairement. Chaque prompt a été choisi pour refléter un **accompagnement ou ingrédient authentique et plausible** pour le plat concerné :

| Plat | Ajout 1 | Ajout 2 | Ajout 3 | Logique |
|---|---|---|---|---|
| Foutou | Poisson fumé | Sauce graine supplémentaire | Morceaux de bœuf | Variations réelles de garniture du foutou en Côte d'Ivoire |
| Garba | Thon frit | Alloco | Oignons/piments | Composition typique du garba de rue |
| Attiéké poisson | Poisson frit | Alloco | Crevettes grillées | Alternatives protéiques courantes |
| Kedjenou | Poulet | Riz blanc | Piments/tomates | Accompagnements classiques du kedjenou |
| Gombo | Crabe/crevettes | Foutou | Peau de bœuf (kanda) | Garnitures traditionnelles de la sauce gombo |
| Thiéboudienne | Poisson farci | Légumes | Crevettes | Variantes de protéines du plat national sénégalais |
| Mafé | Agneau | Riz cassé | Courge/patate douce | Variations de viande et accompagnement |
| Yassa | Oignons caramélisés | Poulet braisé | Citron/olives | Éléments caractéristiques du yassa |
| Thiakry | Glaçons | Mangue fraîche | Coco/raisins | Garnitures du dessert selon la saison/préférence |
| Domoda | Viande | Courge/patate | Riz | Variations standards du plat gambien |

### Pourquoi insister sur "matches existing lighting" et "no duplicate" dans les prompts ?

Ces contraintes empêchent deux défauts fréquents de l'inpainting par IA générative : la création d'incohérences visuelles (un ajout éclairé différemment du reste de la photo, signe immédiat de manipulation) et la duplication accidentelle d'éléments déjà présents dans l'image. Cela garantit que les images générées restent crédibles et utilisables comme données d'entraînement réalistes.

### Pourquoi détecter le plat seulement par le nom du fichier ?

Une détection basée sur le contenu visuel de l'image (classification automatique) introduirait un risque d'erreur en amont de tout le pipeline : si le plat est mal identifié, les 3 ajouts IA seront incohérents culinairement (par exemple, ajouter des glaçons sur un kedjenou). Le nom de fichier, lui, est une information fiable à 100% si la convention de nommage du dataset a été respectée lors de la collecte initiale.