# Garden Plans - Guide de contribution

## Description du projet

Garden Plans est une collection de meubles de jardin DIY modelises en 3D,
avec plans techniques et guides de construction. Chaque projet utilise des
materiaux recycles (palettes, bois de recuperation) et genere des fichiers
STL + PDF a partir de scripts Python.

## Stack technique

- **Python 3.12+** avec `numpy`, `numpy-stl`, `matplotlib`
- **Site statique** : HTML/CSS pur (pas de framework), deploye via GitHub Pages
- **CI/CD** : GitHub Actions (build + deploy Pages), Netlify (PR previews)

## Structure d'un projet

Chaque projet est un repertoire a la racine avec cette structure :

```
nom_du_projet/
├── README.md                    # Documentation du projet
├── NOMENCLATURE.md              # Liste de debit + instructions (source)
├── generate_table.py            # Generateur STL + PDF technique (OBLIGATOIRE)
├── generate_guide.py            # Generateur guide construction PDF
├── generate_nomenclature.py     # Generateur nomenclature PDF
├── index.html                   # Page projet pour le site statique
├── nom_du_projet.stl            # Maillage 3D genere
├── nom_du_projet_plan.pdf       # Plan technique genere
├── nomenclature.pdf             # Nomenclature PDF generee
└── guide_construction.pdf       # Guide illustre genere
```

Le fichier `generate_table.py` est le point d'entree du build. Le workflow
GitHub Actions detecte automatiquement les repertoires contenant ce fichier.

## Conventions

### Scripts Python

- Utiliser `matplotlib.use("Agg")` pour le rendu headless
- Definir les dimensions en mm en constantes en haut du fichier
- Utiliser `_box_faces(x, y, z, dx, dy, dz)` pour generer les faces STL
- Les fichiers de sortie doivent etre dans `OUTPUT_DIR` (meme repertoire)
- Le plan technique PDF doit contenir : vue de face, vue de dessus, vue de cote,
  cartouche avec dimensions et reference Instructables

### Site statique

- Chaque projet a sa page `index.html` avec specs, telechargements, nomenclature
- La page d'accueil `index.html` a la racine liste tous les projets
- Design responsive, palette de couleurs bois (#d2a679, #c49a6c, #b8956a, #a0784e)
- Pas de framework JS, pas de build frontend

### Nomenclature

- Fournir en PDF (genere par `generate_nomenclature.py`) ET en Markdown (`NOMENCLATURE.md`)
- Le PDF contient : couverture, tableau recapitulatif, instructions de debit,
  outillage, et ordre d'assemblage (6 pages minimum)
- Lister toutes les pieces avec ref (A, B, C...), dimensions, quantite, origine
- Expliquer comment obtenir chaque piece a partir du materiau source
- Inclure la liste d'outillage et l'ordre d'assemblage

### Git

- Une branche par feature/projet
- Commits en anglais, description en francais si necessaire
- Squash avant merge
- PR en draft pendant le developpement

## Commandes utiles

```bash
# Installer les dependances
pip install numpy numpy-stl matplotlib

# Generer les fichiers d'un projet
cd nom_du_projet && python generate_table.py

# Generer le guide de construction
cd nom_du_projet && python generate_guide.py
```

## Ajouter un nouveau projet

1. Creer un repertoire `nom_du_projet/` a la racine
2. Creer `generate_table.py` avec les constantes de dimensions et les fonctions
   `generate_stl()` et `generate_pdf()` (plan technique)
3. Creer `generate_guide.py` pour le guide illustre pas a pas
4. Creer `generate_nomenclature.py` pour la nomenclature PDF
5. Creer `NOMENCLATURE.md` avec la liste de debit detaillee
6. Creer `README.md` avec description, dimensions, fichiers, usage
7. Creer `index.html` pour la page projet du site statique
8. Mettre a jour `index.html` a la racine pour ajouter la carte du projet
9. Executer les scripts pour generer STL, PDF technique, nomenclature et guide
10. Commiter tous les fichiers (y compris les generes)
