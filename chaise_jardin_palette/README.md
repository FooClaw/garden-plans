# Chaise de Jardin Empilable en Palettes Recyclees

Chaise de jardin 100% bois de palette, conçue pour accompagner la
table basse palette (450 mm). Design empilable grace au retrecissement
des pieds arriere.

Inspiree du projet [A Deck Chair Made From Pallet Wood Leftovers](https://www.instructables.com/A-Deck-Chair-Made-From-Pallet-Wood-Leftovers/)
sur Instructables, adaptee en plus compact et empilable.

## Dimensions

| Element | Dimensions |
|---------|-----------|
| Chaise (L x P x H) | 588 x 450 x 770 mm |
| Hauteur assise | 370 mm (adaptee table 450 mm) |
| Assise | 6 lattes de 70 x 22 mm |
| Dossier | 4 lattes de 70 x 22 mm, H = 400 mm |
| Pieds avant | 44 x 44 x 370 mm |
| Pieds arriere | 44 x 44 x 770 mm |

## Empilabilite

Les pieds arriere sont plus rapproches (480 mm) que les pieds avant
(588 mm), ce qui permet d'imbriquer les chaises les unes dans les autres.
On peut empiler 4-5 chaises facilement.

## Fichiers

| Fichier | Description |
|---------|-------------|
| `generate_table.py` | Generateur STL + PDF technique |
| `generate_guide.py` | Generateur guide construction PDF |
| `generate_nomenclature.py` | Generateur nomenclature PDF |
| `chaise_jardin_palette.stl` | Maillage 3D |
| `chaise_jardin_palette_plan.pdf` | Plan technique |
| `guide_construction.pdf` | Guide 10 pages illustre |
| `nomenclature.pdf` | Nomenclature PDF |
| `NOMENCLATURE.md` | Nomenclature source |

## Usage

```bash
pip install numpy numpy-stl matplotlib
python3 generate_table.py
python3 generate_guide.py
python3 generate_nomenclature.py
```
