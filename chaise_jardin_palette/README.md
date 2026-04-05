# Deck Chair de Jardin en Palettes Recyclees

Chaise de jardin type deck chair / Adirondack, 100% bois de palette.
Design classique avec assise basse, dossier recline et accoudoirs larges.

Inspiree du projet [A Deck Chair Made From Pallet Wood Leftovers](https://www.instructables.com/A-Deck-Chair-Made-From-Pallet-Wood-Leftovers/)
sur Instructables, adaptee pour accompagner la table basse palette (450 mm).

## Design

- Assise basse et legerement inclinee (350 mm)
- Dossier recline a ~110 degres
- Accoudoirs larges (95 mm) pour poser un verre
- Pieds arriere d'une seule piece (sol → haut du dossier, 900 mm)
- Empilable grace au retrecissement des pieds arriere

## Dimensions

| Element | Dimensions |
|---------|-----------|
| Chaise (L x P x H) | 600 x 480 x 900 mm |
| Hauteur assise | 350 mm |
| Angle dossier | ~110 degres |
| Assise | 6 lattes de 70 x 22 mm |
| Dossier | 5 lattes de 70 x 22 mm |
| Accoudoirs | 550 x 95 x 22 mm |
| Pieds avant | 44 x 70 x 350 mm |
| Pieds arriere | 44 x 70 x 900 mm |

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
