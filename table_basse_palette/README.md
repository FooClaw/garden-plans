# Table Basse en Palettes Recyclees

Modele 3D d'une table basse 100% bois de palette, inspire du projet
[DIY Pallet Table](https://www.instructables.com/DIY-PALLET-TABLE-100-PALLET-WOOD/)
sur Instructables.

## Design

- Plateau 6 lattes de palette alignees
- Etagere inferieure pour le rangement
- 4 pieds en blocs de palette
- Entretoises laterales pour la rigidite
- Materiau : euro-palette recyclee (lattes 22 mm)

## Dimensions

| Element | Dimensions |
|---------|-----------|
| Table (L x l x H) | 1200 x 600 x 450 mm |
| Lattes plateau | 95 x 22 mm (x6) |
| Pieds | 95 x 95 x 406 mm |
| Etagere | a 100 mm du sol |
| Entretoises | 70 x 22 mm |

## Fichiers

| Fichier | Description |
|---------|-------------|
| `generate_table.py` | Script Python (numpy-stl + matplotlib) |
| `table_basse_palette.stl` | Maillage 3D pour visualisation / impression |
| `table_basse_palette_plan.pdf` | Plan technique avec vues de face, dessus et cote |

## Usage

```bash
python3 generate_table.py
```

Genere le STL et le PDF. Necessite `numpy`, `numpy-stl` et `matplotlib`.
