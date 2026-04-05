# Deck Chair de Jardin en Palettes Recyclees

Chaise de jardin type deck chair, 100% bois de palette.
Design minimaliste : assise tres basse, dossier tres incline, sans accoudoirs.
Panneaux lateraux style palette (planche + blocs + planche).

Fidellement inspire du projet [A Deck Chair Made From Pallet Wood Leftovers](https://www.instructables.com/A-Deck-Chair-Made-From-Pallet-Wood-Leftovers/)
par Well Done Tips sur Instructables. Adaptee pour accompagner la table basse palette (450 mm).

## Design

- Panneaux lateraux style palette : planche basse + 3 blocs + planche haute (122 mm)
- Assise tres basse (144 mm) - position transat, genoux au-dessus des hanches
- Dossier incline a ~125 degres - position tres detendue
- Pas d'accoudoirs - design epure et minimaliste
- Lattes pleine largeur (95 mm) avec ecarts de 15 mm
- Assise courte (4 lattes) couvrant toute la largeur (600 mm)
- Longerons depassant de 350 mm a l'arriere pour la stabilite
- Supports dossier inclines a 35 degres de la verticale

## Dimensions

| Element | Dimensions |
|---------|-----------|
| Chaise (L x P x H) | 600 x 775 x 677 mm |
| Hauteur assise | 144 mm |
| Angle dossier | ~125 degres |
| Panneaux lateraux | 775 x 95 x 122 mm |
| Assise | 4 lattes de 600 x 95 x 22 mm |
| Dossier | 5 lattes de 410 x 95 x 22 mm |
| Supports dossier | 650 x 70 x 44 mm |
| Blocs lateraux | 44 x 44 x 78 mm |
| Montants ancrage | 144 x 70 x 44 mm |
| Pieces totales | 24 (8 references) |

## Fichiers

| Fichier | Description |
|---------|-------------|
| `generate_table.py` | Generateur STL + PDF technique |
| `generate_guide.py` | Generateur guide construction PDF |
| `generate_nomenclature.py` | Generateur nomenclature PDF |
| `chaise_jardin_palette.stl` | Maillage 3D |
| `chaise_jardin_palette_plan.pdf` | Plan technique |
| `guide_construction.pdf` | Guide illustre |
| `nomenclature.pdf` | Nomenclature PDF |
| `NOMENCLATURE.md` | Nomenclature source |

## Usage

```bash
pip install numpy numpy-stl matplotlib
python3 generate_table.py
python3 generate_guide.py
python3 generate_nomenclature.py
```
