"""
Premier objet 3D FreeCAD - Pot de fleurs pour le jardin

Ce script cree un pot de fleurs parametrique en 3D avec FreeCAD.
Il peut etre execute dans la console Python de FreeCAD ou en ligne de commande:
    freecad -c first_3d_object.py
"""

import FreeCAD
import Part

# --- Parametres du pot de fleurs ---
POT_HEIGHT = 120.0        # mm
POT_TOP_RADIUS = 80.0     # mm
POT_BOTTOM_RADIUS = 50.0  # mm
POT_WALL_THICKNESS = 5.0  # mm
POT_BOTTOM_THICKNESS = 5.0  # mm
DRAIN_HOLE_RADIUS = 8.0   # mm
DRAIN_HOLE_COUNT = 3
DRAIN_HOLE_DISTANCE = 25.0  # mm from center


def create_flower_pot():
    """Cree un pot de fleurs parametrique avec trous de drainage."""

    doc = FreeCAD.newDocument("PotDeFleurs")

    # Coque exterieure - cone tronque
    outer_cone = Part.makeCone(
        POT_BOTTOM_RADIUS, POT_TOP_RADIUS, POT_HEIGHT
    )

    # Coque interieure (pour creuser le pot)
    inner_cone = Part.makeCone(
        POT_BOTTOM_RADIUS - POT_WALL_THICKNESS,
        POT_TOP_RADIUS - POT_WALL_THICKNESS,
        POT_HEIGHT - POT_BOTTOM_THICKNESS,
    )
    inner_cone.translate(FreeCAD.Vector(0, 0, POT_BOTTOM_THICKNESS))

    # Soustraction pour obtenir le pot creux
    pot = outer_cone.cut(inner_cone)

    # Trous de drainage
    import math

    for i in range(DRAIN_HOLE_COUNT):
        angle = (2 * math.pi / DRAIN_HOLE_COUNT) * i
        x = DRAIN_HOLE_DISTANCE * math.cos(angle)
        y = DRAIN_HOLE_DISTANCE * math.sin(angle)
        hole = Part.makeCylinder(DRAIN_HOLE_RADIUS, POT_BOTTOM_THICKNESS)
        hole.translate(FreeCAD.Vector(x, y, 0))
        pot = pot.cut(hole)

    # Ajouter au document
    pot_feature = doc.addObject("Part::Feature", "PotDeFleurs")
    pot_feature.Shape = pot

    doc.recompute()

    # Sauvegarder
    output_path = "pot_de_fleurs.FCStd"
    doc.saveAs(output_path)
    print(f"Objet 3D sauvegarde dans: {output_path}")

    return doc


if __name__ == "__main__":
    create_flower_pot()
