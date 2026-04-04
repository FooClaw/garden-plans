# FreeCAD - Objets 3D pour le jardin

## Premier objet : Pot de fleurs

Script parametrique qui genere un pot de fleurs en 3D avec :
- Forme conique (plus large en haut)
- Parois creuses
- 3 trous de drainage

### Utilisation

Dans la console FreeCAD :
```python
exec(open("first_3d_object.py").read())
```

Ou en ligne de commande :
```bash
freecad -c first_3d_object.py
```

### Parametres modifiables

| Parametre | Valeur par defaut | Description |
|-----------|------------------|-------------|
| `POT_HEIGHT` | 120 mm | Hauteur du pot |
| `POT_TOP_RADIUS` | 80 mm | Rayon du haut |
| `POT_BOTTOM_RADIUS` | 50 mm | Rayon du bas |
| `POT_WALL_THICKNESS` | 5 mm | Epaisseur des parois |
| `DRAIN_HOLE_COUNT` | 3 | Nombre de trous de drainage |
