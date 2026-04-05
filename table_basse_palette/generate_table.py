"""
Table basse en palettes recyclees - Modele 3D

Inspiree du projet Instructables "DIY Pallet Table 100% Pallet Wood".
Dimensions basees sur des euro-palettes standard (1200x800mm, lattes 22mm).

Design :
  - Plateau superieur en lattes de palette alignees
  - Etagere inferieure (rangement)
  - 4 pieds en blocs de palette (cubes empiles)
  - Entretoises laterales pour la rigidite

Usage :
    python3 generate_table.py
"""

import math
import os

import numpy as np
from stl import mesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib.backends.backend_pdf import PdfPages

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Dimensions (mm) - inspirees euro-palette ---
# Plateau
TABLE_LENGTH = 1200.0       # longueur totale
TABLE_WIDTH = 600.0         # largeur totale
TABLE_HEIGHT = 450.0        # hauteur totale

# Lattes du plateau et de l'etagere
PLANK_THICKNESS = 22.0      # epaisseur d'une latte de palette
PLANK_WIDTH = 95.0          # largeur d'une latte
PLANK_GAP = 3.0             # espacement entre lattes
N_PLANKS_TOP = 6            # nombre de lattes sur le plateau

# Pieds (blocs de palette empiles)
LEG_WIDTH = 95.0            # largeur du pied (= largeur latte)
LEG_DEPTH = 95.0            # profondeur du pied
LEG_HEIGHT = TABLE_HEIGHT - 2 * PLANK_THICKNESS  # hauteur pieds (sans plateau ni etagere)

# Etagere inferieure
SHELF_HEIGHT = 100.0        # hauteur du bas de l'etagere depuis le sol
SHELF_INSET = 50.0          # retrait de l'etagere par rapport aux bords

# Entretoises (traverses laterales)
BRACE_WIDTH = 70.0
BRACE_THICKNESS = 22.0

N_MESH = 1  # simplification du maillage


def _box_faces(x, y, z, dx, dy, dz):
    """Genere les 12 triangles (6 faces) d'un parallelipede."""
    v = np.array([
        [x, y, z],
        [x + dx, y, z],
        [x + dx, y + dy, z],
        [x, y + dy, z],
        [x, y, z + dz],
        [x + dx, y, z + dz],
        [x + dx, y + dy, z + dz],
        [x, y + dy, z + dz],
    ])
    # 6 faces x 2 triangles = 12 triangles
    faces = [
        # Bas
        [v[0], v[2], v[1]], [v[0], v[3], v[2]],
        # Haut
        [v[4], v[5], v[6]], [v[4], v[6], v[7]],
        # Avant
        [v[0], v[1], v[5]], [v[0], v[5], v[4]],
        # Arriere
        [v[2], v[3], v[7]], [v[2], v[7], v[6]],
        # Gauche
        [v[0], v[4], v[7]], [v[0], v[7], v[3]],
        # Droite
        [v[1], v[2], v[6]], [v[1], v[6], v[5]],
    ]
    return faces


def generate_stl():
    """Genere le fichier STL de la table basse en palettes."""
    all_faces = []

    # --- Plateau superieur (lattes) ---
    top_z = TABLE_HEIGHT - PLANK_THICKNESS
    total_planks_width = N_PLANKS_TOP * PLANK_WIDTH + (N_PLANKS_TOP - 1) * PLANK_GAP
    start_y = (TABLE_WIDTH - total_planks_width) / 2.0

    for i in range(N_PLANKS_TOP):
        py = start_y + i * (PLANK_WIDTH + PLANK_GAP)
        all_faces.extend(_box_faces(0, py, top_z, TABLE_LENGTH, PLANK_WIDTH, PLANK_THICKNESS))

    # --- Traverses du plateau (2 traverses perpendiculaires sous le plateau) ---
    brace_z = top_z - BRACE_THICKNESS
    brace_positions = [LEG_WIDTH, TABLE_LENGTH - LEG_WIDTH - BRACE_THICKNESS]
    for bx in brace_positions:
        all_faces.extend(_box_faces(bx, 0, brace_z, BRACE_THICKNESS, TABLE_WIDTH, BRACE_THICKNESS))

    # Traverse centrale
    center_brace_x = (TABLE_LENGTH - BRACE_THICKNESS) / 2.0
    all_faces.extend(_box_faces(center_brace_x, 0, brace_z, BRACE_THICKNESS, TABLE_WIDTH, BRACE_THICKNESS))

    # --- 4 Pieds ---
    leg_positions = [
        (0, 0),                                          # avant-gauche
        (TABLE_LENGTH - LEG_WIDTH, 0),                   # avant-droit
        (0, TABLE_WIDTH - LEG_DEPTH),                    # arriere-gauche
        (TABLE_LENGTH - LEG_WIDTH, TABLE_WIDTH - LEG_DEPTH),  # arriere-droit
    ]
    for lx, ly in leg_positions:
        all_faces.extend(_box_faces(lx, ly, 0, LEG_WIDTH, LEG_DEPTH, brace_z))

    # --- Etagere inferieure ---
    shelf_z = SHELF_HEIGHT
    shelf_x0 = SHELF_INSET
    shelf_length = TABLE_LENGTH - 2 * SHELF_INSET
    n_shelf_planks = 4
    shelf_total_w = n_shelf_planks * PLANK_WIDTH + (n_shelf_planks - 1) * PLANK_GAP
    shelf_start_y = (TABLE_WIDTH - shelf_total_w) / 2.0

    for i in range(n_shelf_planks):
        sy = shelf_start_y + i * (PLANK_WIDTH + PLANK_GAP)
        all_faces.extend(_box_faces(shelf_x0, sy, shelf_z, shelf_length, PLANK_WIDTH, PLANK_THICKNESS))

    # Traverses de l'etagere (sous l'etagere)
    shelf_brace_z = shelf_z - BRACE_THICKNESS
    for bx in [shelf_x0, shelf_x0 + shelf_length - BRACE_THICKNESS]:
        all_faces.extend(_box_faces(bx, 0, shelf_brace_z, BRACE_THICKNESS, TABLE_WIDTH, BRACE_THICKNESS))

    # --- Entretoises laterales (longerons bas reliant les pieds) ---
    longeron_z = SHELF_HEIGHT + PLANK_THICKNESS
    longeron_length = TABLE_LENGTH - 2 * LEG_WIDTH
    # Cote avant
    all_faces.extend(_box_faces(LEG_WIDTH, 0, longeron_z,
                                longeron_length, BRACE_THICKNESS, BRACE_WIDTH))
    # Cote arriere
    all_faces.extend(_box_faces(LEG_WIDTH, TABLE_WIDTH - BRACE_THICKNESS, longeron_z,
                                longeron_length, BRACE_THICKNESS, BRACE_WIDTH))

    # --- Construire le mesh ---
    faces_array = np.array(all_faces)
    table_mesh = mesh.Mesh(np.zeros(faces_array.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces_array):
        table_mesh.vectors[i] = f

    stl_path = os.path.join(OUTPUT_DIR, "table_basse_palette.stl")
    table_mesh.save(stl_path)
    print(f"STL genere: {stl_path}")
    return stl_path


def _add_dim_h(ax, x1, x2, y, label, offset=8):
    """Cote horizontale."""
    yo = y + offset
    ax.annotate("", xy=(x2, yo), xytext=(x1, yo),
                arrowprops=dict(arrowstyle="<->", color="blue", lw=0.8))
    ax.plot([x1, x1], [y, yo], "b-", lw=0.4)
    ax.plot([x2, x2], [y, yo], "b-", lw=0.4)
    ax.text((x1 + x2) / 2, yo + 3, label, ha="center", fontsize=7, color="blue")


def _add_dim_v(ax, x, y1, y2, label, offset=8):
    """Cote verticale."""
    xo = x + offset
    ax.annotate("", xy=(xo, y2), xytext=(xo, y1),
                arrowprops=dict(arrowstyle="<->", color="blue", lw=0.8))
    ax.plot([x, xo], [y1, y1], "b-", lw=0.4)
    ax.plot([x, xo], [y2, y2], "b-", lw=0.4)
    ax.text(xo + 3, (y1 + y2) / 2, label, ha="left", va="center", fontsize=7,
            color="blue", rotation=90)


def generate_pdf():
    """Genere le plan technique PDF de la table basse."""
    pdf_path = os.path.join(OUTPUT_DIR, "table_basse_palette_plan.pdf")

    fig = plt.figure(figsize=(11.69, 8.27))  # A4 paysage
    fig.suptitle("Plan Technique - Table Basse en Palettes Recyclees", fontsize=13, fontweight="bold")

    # ===================== VUE DE FACE =====================
    ax1 = fig.add_axes([0.04, 0.38, 0.30, 0.52])
    ax1.set_title("Vue de face", fontsize=10)
    ax1.set_aspect("equal")

    # Pieds gauche et droit
    ax1.add_patch(Rectangle((0, 0), LEG_WIDTH, TABLE_HEIGHT - PLANK_THICKNESS,
                            facecolor="#d2a679", edgecolor="black", lw=1.2))
    ax1.add_patch(Rectangle((TABLE_LENGTH - LEG_WIDTH, 0), LEG_WIDTH,
                            TABLE_HEIGHT - PLANK_THICKNESS,
                            facecolor="#d2a679", edgecolor="black", lw=1.2))

    # Plateau (lattes vues de profil = une bande)
    ax1.add_patch(Rectangle((0, TABLE_HEIGHT - PLANK_THICKNESS), TABLE_LENGTH, PLANK_THICKNESS,
                            facecolor="#c49a6c", edgecolor="black", lw=1.5))

    # Etagere
    ax1.add_patch(Rectangle((SHELF_INSET, SHELF_HEIGHT), TABLE_LENGTH - 2 * SHELF_INSET, PLANK_THICKNESS,
                            facecolor="#c49a6c", edgecolor="black", lw=1.0))

    # Entretoises laterales
    longeron_z = SHELF_HEIGHT + PLANK_THICKNESS
    ax1.add_patch(Rectangle((LEG_WIDTH, longeron_z),
                            TABLE_LENGTH - 2 * LEG_WIDTH, BRACE_WIDTH,
                            facecolor="#b8956a", edgecolor="black", lw=0.8, linestyle="--"))

    # Cotes
    _add_dim_h(ax1, 0, TABLE_LENGTH, TABLE_HEIGHT, f"{TABLE_LENGTH:.0f} mm", offset=12)
    _add_dim_v(ax1, TABLE_LENGTH, 0, TABLE_HEIGHT, f"{TABLE_HEIGHT:.0f} mm", offset=15)
    _add_dim_v(ax1, -15, 0, SHELF_HEIGHT, f"{SHELF_HEIGHT:.0f}", offset=0)

    ax1.set_xlim(-40, TABLE_LENGTH + 50)
    ax1.set_ylim(-20, TABLE_HEIGHT + 40)
    ax1.grid(True, alpha=0.2)
    ax1.set_xlabel("mm")
    ax1.set_ylabel("mm")

    # ===================== VUE DE DESSUS =====================
    ax2 = fig.add_axes([0.38, 0.38, 0.28, 0.52])
    ax2.set_title("Vue de dessus", fontsize=10)
    ax2.set_aspect("equal")

    # Lattes du plateau
    total_pw = N_PLANKS_TOP * PLANK_WIDTH + (N_PLANKS_TOP - 1) * PLANK_GAP
    start_y = (TABLE_WIDTH - total_pw) / 2.0
    colors_top = ["#c49a6c", "#b8956a", "#d2a679", "#c49a6c", "#b8956a", "#d2a679"]
    for i in range(N_PLANKS_TOP):
        py = start_y + i * (PLANK_WIDTH + PLANK_GAP)
        ax2.add_patch(Rectangle((0, py), TABLE_LENGTH, PLANK_WIDTH,
                                facecolor=colors_top[i % len(colors_top)],
                                edgecolor="black", lw=0.8))

    # Contour pieds (pointilles)
    for lx, ly in [(0, 0), (TABLE_LENGTH - LEG_WIDTH, 0),
                   (0, TABLE_WIDTH - LEG_DEPTH), (TABLE_LENGTH - LEG_WIDTH, TABLE_WIDTH - LEG_DEPTH)]:
        ax2.add_patch(Rectangle((lx, ly), LEG_WIDTH, LEG_DEPTH,
                                facecolor="none", edgecolor="red", lw=0.6, linestyle="--"))

    _add_dim_h(ax2, 0, TABLE_LENGTH, TABLE_WIDTH, f"{TABLE_LENGTH:.0f} mm", offset=15)
    _add_dim_v(ax2, TABLE_LENGTH, 0, TABLE_WIDTH, f"{TABLE_WIDTH:.0f} mm", offset=15)

    ax2.set_xlim(-20, TABLE_LENGTH + 50)
    ax2.set_ylim(-20, TABLE_WIDTH + 40)
    ax2.grid(True, alpha=0.2)
    ax2.set_xlabel("mm")
    ax2.set_ylabel("mm")

    # ===================== VUE DE COTE =====================
    ax3 = fig.add_axes([0.72, 0.38, 0.25, 0.52])
    ax3.set_title("Vue de cote", fontsize=10)
    ax3.set_aspect("equal")

    # Pieds
    ax3.add_patch(Rectangle((0, 0), LEG_DEPTH, TABLE_HEIGHT - PLANK_THICKNESS,
                            facecolor="#d2a679", edgecolor="black", lw=1.2))
    ax3.add_patch(Rectangle((TABLE_WIDTH - LEG_DEPTH, 0), LEG_DEPTH,
                            TABLE_HEIGHT - PLANK_THICKNESS,
                            facecolor="#d2a679", edgecolor="black", lw=1.2))

    # Plateau
    ax3.add_patch(Rectangle((0, TABLE_HEIGHT - PLANK_THICKNESS), TABLE_WIDTH, PLANK_THICKNESS,
                            facecolor="#c49a6c", edgecolor="black", lw=1.5))

    # Etagere
    ax3.add_patch(Rectangle((SHELF_INSET, SHELF_HEIGHT), TABLE_WIDTH - 2 * SHELF_INSET, PLANK_THICKNESS,
                            facecolor="#c49a6c", edgecolor="black", lw=1.0))

    # Longeron
    ax3.add_patch(Rectangle((0, SHELF_HEIGHT + PLANK_THICKNESS),
                            BRACE_THICKNESS, BRACE_WIDTH,
                            facecolor="#b8956a", edgecolor="black", lw=0.8))
    ax3.add_patch(Rectangle((TABLE_WIDTH - BRACE_THICKNESS, SHELF_HEIGHT + PLANK_THICKNESS),
                            BRACE_THICKNESS, BRACE_WIDTH,
                            facecolor="#b8956a", edgecolor="black", lw=0.8))

    _add_dim_h(ax3, 0, TABLE_WIDTH, TABLE_HEIGHT, f"{TABLE_WIDTH:.0f} mm", offset=12)
    _add_dim_v(ax3, TABLE_WIDTH, 0, TABLE_HEIGHT, f"{TABLE_HEIGHT:.0f} mm", offset=15)

    ax3.set_xlim(-20, TABLE_WIDTH + 50)
    ax3.set_ylim(-20, TABLE_HEIGHT + 40)
    ax3.grid(True, alpha=0.2)
    ax3.set_xlabel("mm")
    ax3.set_ylabel("mm")

    # ===================== CARTOUCHE =====================
    ax_info = fig.add_axes([0.04, 0.04, 0.92, 0.26])
    ax_info.axis("off")
    info = (
        "Objet : Table Basse en Palettes Recyclees (100% bois de palette)\n"
        f"Dimensions : {TABLE_LENGTH:.0f} x {TABLE_WIDTH:.0f} x {TABLE_HEIGHT:.0f} mm "
        f"(L x l x H)\n"
        f"Plateau : {N_PLANKS_TOP} lattes de {PLANK_WIDTH:.0f} x {PLANK_THICKNESS:.0f} mm  |  "
        f"Pieds : {LEG_WIDTH:.0f} x {LEG_DEPTH:.0f} x {LEG_HEIGHT:.0f} mm\n"
        f"Etagere inferieure a {SHELF_HEIGHT:.0f} mm du sol  |  "
        f"Entretoises : {BRACE_WIDTH:.0f} x {BRACE_THICKNESS:.0f} mm\n"
        "Materiau : Euro-palette recyclee (lattes 22 mm)  |  "
        "Echelle : 1:1 (mm)\n"
        "Inspire de : instructables.com/DIY-PALLET-TABLE-100-PALLET-WOOD"
    )
    ax_info.text(0.5, 0.5, info, transform=ax_info.transAxes,
                 fontsize=8.5, va="center", ha="center",
                 bbox=dict(boxstyle="round,pad=0.5", facecolor="#f5e6d3", edgecolor="black"),
                 family="monospace")

    plt.savefig(pdf_path, format="pdf", dpi=150)
    plt.close()
    print(f"PDF technique genere: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    generate_stl()
    generate_pdf()
    print("\nGeneration terminee!")
