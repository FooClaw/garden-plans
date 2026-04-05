# Deck Chair de Jardin en Palettes Recyclees

Chaise de jardin type deck chair, 100% bois de palette.
Design minimaliste : assise tres basse, dossier tres incline, sans accoudoirs.

Fidellement inspire du projet [A Deck Chair Made From Pallet Wood Leftovers](https://www.instructables.com/A-Deck-Chair-Made-From-Pallet-Wood-Leftovers/)
par Well Done Tips sur Instructables. Adaptee pour accompagner la table basse palette (450 mm).

## Design

- Assise tres basse (180 mm) - style transat, genoux au-dessus des hanches
- Dossier incline a ~120 degres - position tres detendue
- Pas d'accoudoirs - design epure et minimaliste
- Lattes pleine largeur (95 mm, non refendues) avec ecarts visibles (10 mm)
- Assise courte (4 lattes) - les jambes depassent devant
- Longerons au sol depassant de 300 mm a l'arriere pour la stabilite
- Supports dossier inclines (600 mm) fixes sur les longerons

## Dimensions

| Element | Dimensions |
|---------|-----------|
| Chaise (L x P x H) | 600 x 710 x 700 mm |
| Hauteur assise | 180 mm |
| Angle dossier | ~120 degres |
| Assise | 4 lattes de 95 x 22 mm |
| Dossier | 5 lattes de 95 x 22 mm |
| Longerons | 710 x 70 x 44 mm |
| Pieds avant | 44 x 70 x 180 mm |
| Supports dossier | 600 x 70 x 44 mm |

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
