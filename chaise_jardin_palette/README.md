# Deck Chair de Jardin en Palettes Recyclees

Chaise de jardin type deck chair, 100% bois de palette.
Design minimaliste : assise tres basse, dossier incline, sans accoudoirs.

Fidellement inspire du projet [A Deck Chair Made From Pallet Wood Leftovers](https://www.instructables.com/A-Deck-Chair-Made-From-Pallet-Wood-Leftovers/)
par Well Done Tips sur Instructables. Adaptee pour accompagner la table basse palette (450 mm).

## Design

- Assise tres basse (250 mm) - style transat
- Dossier incline a ~115 degres - position detendue
- Pas d'accoudoirs - design epure et minimaliste
- Lattes pleine largeur (95 mm, non refendues)
- Longerons au sol depassant a l'arriere pour la stabilite
- Supports dossier inclines fixes sur les longerons

## Dimensions

| Element | Dimensions |
|---------|-----------|
| Chaise (L x P x H) | 600 x 699 x 703 mm |
| Hauteur assise | 250 mm |
| Angle dossier | ~115 degres |
| Assise | 5 lattes de 95 x 22 mm |
| Dossier | 4 lattes de 95 x 22 mm |
| Longerons | 699 x 70 x 44 mm |
| Pieds avant | 44 x 70 x 250 mm |
| Supports dossier | 500 x 70 x 44 mm |

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
