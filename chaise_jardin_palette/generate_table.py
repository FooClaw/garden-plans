"""
Chaise de jardin empilable en palettes recyclees - Modele 3D

Inspiree du projet Instructables "A Deck Chair Made From Pallet Wood Leftovers".
Dimensions adaptees pour accompagner la table basse palette (450 mm de haut).
Design empilable : pieds avant elargi et arriere retreci pour imbrication.

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
from matplotlib.patches import Rectangle, FancyArrowPatch, Polygon
from matplotlib.backends.backend_pdf import PdfPages

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Dimensions (mm) - adaptees table basse 450mm ---
# Assise
SEAT_WIDTH = 500.0          # largeur assise (interieur accoudoirs)
SEAT_DEPTH = 450.0          # profondeur assise
SEAT_HEIGHT = 370.0         # hauteur assise (table = 450, confort = table - 80)

# Dossier
BACKREST_HEIGHT = 400.0     # hauteur du dossier au-dessus de l'assise
BACKREST_ANGLE = 10.0       # inclinaison en degres vers l'arriere

# Lattes de palette
PLANK_THICKNESS = 22.0
PLANK_WIDTH = 70.0          # largeur lattes (refendues pour chaise plus legere)
PLANK_GAP = 5.0

# Assise : nombre de lattes
N_SEAT_PLANKS = 6
# Dossier : nombre de lattes
N_BACK_PLANKS = 4

# Pieds (section carree, depuis lattes epaisses collees)
LEG_SECTION = 44.0          # 2 x 22mm colles
# Pieds avant
FRONT_LEG_HEIGHT = SEAT_HEIGHT
# Pieds arriere (montent jusqu'au dossier)
BACK_LEG_HEIGHT = SEAT_HEIGHT + BACKREST_HEIGHT

# Traverses
BRACE_SECTION = 22.0        # epaisseur traverse
BRACE_WIDTH_B = 44.0        # largeur traverse

# Empilabilite : ecart lateral entre pieds avant et arriere
# Les pieds arriere sont plus rapproches que les pieds avant
FRONT_LEG_SPREAD = SEAT_WIDTH + 2 * LEG_SECTION  # largeur totale ext. avant
BACK_LEG_SPREAD = SEAT_WIDTH - 20.0              # largeur int. arriere (retrecissement)
STACK_CLEARANCE = 10.0      # jeu pour empiler


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
    faces = [
        [v[0], v[2], v[1]], [v[0], v[3], v[2]],
        [v[4], v[5], v[6]], [v[4], v[6], v[7]],
        [v[0], v[1], v[5]], [v[0], v[5], v[4]],
        [v[2], v[3], v[7]], [v[2], v[7], v[6]],
        [v[0], v[4], v[7]], [v[0], v[7], v[3]],
        [v[1], v[2], v[6]], [v[1], v[6], v[5]],
    ]
    return faces


def generate_stl():
    """Genere le fichier STL de la chaise de jardin empilable."""
    all_faces = []

    # Offsets pieds
    front_left_x = 0
    front_right_x = FRONT_LEG_SPREAD - LEG_SECTION
    back_offset = (FRONT_LEG_SPREAD - BACK_LEG_SPREAD) / 2.0
    back_left_x = back_offset
    back_right_x = back_offset + BACK_LEG_SPREAD - LEG_SECTION

    # --- 4 Pieds ---
    # Avant gauche
    all_faces.extend(_box_faces(front_left_x, 0, 0,
                                LEG_SECTION, LEG_SECTION, FRONT_LEG_HEIGHT))
    # Avant droit
    all_faces.extend(_box_faces(front_right_x, 0, 0,
                                LEG_SECTION, LEG_SECTION, FRONT_LEG_HEIGHT))
    # Arriere gauche (pleine hauteur)
    all_faces.extend(_box_faces(back_left_x, SEAT_DEPTH - LEG_SECTION, 0,
                                LEG_SECTION, LEG_SECTION, BACK_LEG_HEIGHT))
    # Arriere droit (pleine hauteur)
    all_faces.extend(_box_faces(back_right_x, SEAT_DEPTH - LEG_SECTION, 0,
                                LEG_SECTION, LEG_SECTION, BACK_LEG_HEIGHT))

    # --- Traverses de structure ---
    # Traverse avant (sous assise)
    all_faces.extend(_box_faces(front_left_x, 0,
                                SEAT_HEIGHT - PLANK_THICKNESS - BRACE_SECTION,
                                FRONT_LEG_SPREAD, BRACE_SECTION, BRACE_SECTION))
    # Traverse arriere (sous assise)
    all_faces.extend(_box_faces(back_left_x, SEAT_DEPTH - LEG_SECTION,
                                SEAT_HEIGHT - PLANK_THICKNESS - BRACE_SECTION,
                                BACK_LEG_SPREAD, BRACE_SECTION, BRACE_SECTION))
    # Traverses laterales (sous assise, reliant avant-arriere)
    for lx_front, lx_back in [(front_left_x, back_left_x),
                                (front_right_x, back_right_x)]:
        cx = min(lx_front, lx_back)
        all_faces.extend(_box_faces(cx, LEG_SECTION,
                                    SEAT_HEIGHT - PLANK_THICKNESS - BRACE_SECTION,
                                    LEG_SECTION, SEAT_DEPTH - 2 * LEG_SECTION,
                                    BRACE_SECTION))

    # --- Assise (lattes) ---
    seat_z = SEAT_HEIGHT - PLANK_THICKNESS
    total_seat_w = N_SEAT_PLANKS * PLANK_WIDTH + (N_SEAT_PLANKS - 1) * PLANK_GAP
    seat_start_x = (FRONT_LEG_SPREAD - total_seat_w) / 2.0
    for i in range(N_SEAT_PLANKS):
        px = seat_start_x + i * (PLANK_WIDTH + PLANK_GAP)
        all_faces.extend(_box_faces(px, 0, seat_z,
                                    PLANK_WIDTH, SEAT_DEPTH, PLANK_THICKNESS))

    # --- Dossier (lattes) ---
    back_z_base = SEAT_HEIGHT
    total_back_h = N_BACK_PLANKS * PLANK_WIDTH + (N_BACK_PLANKS - 1) * PLANK_GAP
    back_start_x = (FRONT_LEG_SPREAD - (BACK_LEG_SPREAD - 2 * LEG_SECTION)) / 2.0
    back_plank_width = BACK_LEG_SPREAD - 2 * LEG_SECTION
    for i in range(N_BACK_PLANKS):
        pz = back_z_base + i * (PLANK_WIDTH + PLANK_GAP)
        all_faces.extend(_box_faces(back_start_x, SEAT_DEPTH - LEG_SECTION,
                                    pz,
                                    back_plank_width, PLANK_THICKNESS, PLANK_WIDTH))

    # --- Traverse basse (entre pieds avant, renfort) ---
    rung_z = 120.0
    all_faces.extend(_box_faces(front_left_x + LEG_SECTION, 0, rung_z,
                                FRONT_LEG_SPREAD - 2 * LEG_SECTION,
                                BRACE_SECTION, BRACE_SECTION))
    # Traverse basse arriere
    all_faces.extend(_box_faces(back_left_x + LEG_SECTION,
                                SEAT_DEPTH - LEG_SECTION, rung_z,
                                BACK_LEG_SPREAD - 2 * LEG_SECTION,
                                BRACE_SECTION, BRACE_SECTION))

    # --- Construire le mesh ---
    faces_array = np.array(all_faces)
    chair_mesh = mesh.Mesh(np.zeros(faces_array.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces_array):
        chair_mesh.vectors[i] = f

    stl_path = os.path.join(OUTPUT_DIR, "chaise_jardin_palette.stl")
    chair_mesh.save(stl_path)
    print(f"STL genere: {stl_path}")
    return stl_path


def _add_dim_h(ax, x1, x2, y, label, offset=8):
    yo = y + offset
    ax.annotate("", xy=(x2, yo), xytext=(x1, yo),
                arrowprops=dict(arrowstyle="<->", color="blue", lw=0.8))
    ax.plot([x1, x1], [y, yo], "b-", lw=0.4)
    ax.plot([x2, x2], [y, yo], "b-", lw=0.4)
    ax.text((x1 + x2) / 2, yo + 3, label, ha="center", fontsize=7, color="blue")


def _add_dim_v(ax, x, y1, y2, label, offset=8):
    xo = x + offset
    ax.annotate("", xy=(xo, y2), xytext=(xo, y1),
                arrowprops=dict(arrowstyle="<->", color="blue", lw=0.8))
    ax.plot([x, xo], [y1, y1], "b-", lw=0.4)
    ax.plot([x, xo], [y2, y2], "b-", lw=0.4)
    ax.text(xo + 3, (y1 + y2) / 2, label, ha="left", va="center", fontsize=7,
            color="blue", rotation=90)


def generate_pdf():
    """Genere le plan technique PDF de la chaise."""
    pdf_path = os.path.join(OUTPUT_DIR, "chaise_jardin_palette_plan.pdf")
    WOOD1, WOOD2, WOOD3, WOOD4 = "#d2a679", "#c49a6c", "#b8956a", "#a0784e"

    fig = plt.figure(figsize=(11.69, 8.27))
    fig.suptitle("Plan Technique - Chaise de Jardin Empilable en Palettes",
                 fontsize=13, fontweight="bold")

    # ===================== VUE DE FACE =====================
    ax1 = fig.add_axes([0.04, 0.38, 0.28, 0.52])
    ax1.set_title("Vue de face", fontsize=10)
    ax1.set_aspect("equal")

    s = 0.5
    total_h = BACK_LEG_HEIGHT
    # Pieds avant
    ax1.add_patch(Rectangle((0, 0), LEG_SECTION * s, FRONT_LEG_HEIGHT * s,
                            fc=WOOD1, ec="black", lw=1))
    ax1.add_patch(Rectangle(((FRONT_LEG_SPREAD - LEG_SECTION) * s, 0),
                            LEG_SECTION * s, FRONT_LEG_HEIGHT * s,
                            fc=WOOD1, ec="black", lw=1))
    # Pieds arriere (plus hauts, en retrait)
    bo = (FRONT_LEG_SPREAD - BACK_LEG_SPREAD) / 2.0
    ax1.add_patch(Rectangle((bo * s, 0), LEG_SECTION * s, BACK_LEG_HEIGHT * s,
                            fc=WOOD1, ec="black", lw=0.8, ls="--"))
    ax1.add_patch(Rectangle(((bo + BACK_LEG_SPREAD - LEG_SECTION) * s, 0),
                            LEG_SECTION * s, BACK_LEG_HEIGHT * s,
                            fc=WOOD1, ec="black", lw=0.8, ls="--"))
    # Assise
    ax1.add_patch(Rectangle((0, (SEAT_HEIGHT - PLANK_THICKNESS) * s),
                            FRONT_LEG_SPREAD * s, PLANK_THICKNESS * s,
                            fc=WOOD2, ec="black", lw=1.2))
    # Dossier lattes
    for i in range(N_BACK_PLANKS):
        pz = SEAT_HEIGHT + i * (PLANK_WIDTH + PLANK_GAP)
        ax1.add_patch(Rectangle((bo * s + LEG_SECTION * s, pz * s),
                                (BACK_LEG_SPREAD - 2 * LEG_SECTION) * s,
                                PLANK_WIDTH * s,
                                fc=WOOD3, ec="black", lw=0.6))
    # Traverse basse
    ax1.add_patch(Rectangle((LEG_SECTION * s, 120 * s),
                            (FRONT_LEG_SPREAD - 2 * LEG_SECTION) * s,
                            BRACE_SECTION * s,
                            fc=WOOD3, ec="black", lw=0.5))
    # Cotes
    _add_dim_h(ax1, 0, FRONT_LEG_SPREAD * s, total_h * s,
               f"{FRONT_LEG_SPREAD:.0f} mm", offset=8)
    _add_dim_v(ax1, FRONT_LEG_SPREAD * s, 0, SEAT_HEIGHT * s,
               f"{SEAT_HEIGHT:.0f}", offset=10)
    _add_dim_v(ax1, FRONT_LEG_SPREAD * s + 25, 0, BACK_LEG_HEIGHT * s,
               f"{BACK_LEG_HEIGHT:.0f}", offset=0)

    ax1.set_xlim(-20, FRONT_LEG_SPREAD * s + 55)
    ax1.set_ylim(-15, total_h * s + 30)
    ax1.grid(True, alpha=0.2)
    ax1.set_xlabel("mm")
    ax1.set_ylabel("mm")

    # ===================== VUE DE COTE =====================
    ax2 = fig.add_axes([0.36, 0.38, 0.28, 0.52])
    ax2.set_title("Vue de cote", fontsize=10)
    ax2.set_aspect("equal")

    # Pied avant
    ax2.add_patch(Rectangle((0, 0), LEG_SECTION * s, FRONT_LEG_HEIGHT * s,
                            fc=WOOD1, ec="black", lw=1))
    # Pied arriere
    ax2.add_patch(Rectangle(((SEAT_DEPTH - LEG_SECTION) * s, 0),
                            LEG_SECTION * s, BACK_LEG_HEIGHT * s,
                            fc=WOOD1, ec="black", lw=1))
    # Assise
    ax2.add_patch(Rectangle((0, (SEAT_HEIGHT - PLANK_THICKNESS) * s),
                            SEAT_DEPTH * s, PLANK_THICKNESS * s,
                            fc=WOOD2, ec="black", lw=1.2))
    # Dossier
    for i in range(N_BACK_PLANKS):
        pz = SEAT_HEIGHT + i * (PLANK_WIDTH + PLANK_GAP)
        ax2.add_patch(Rectangle(((SEAT_DEPTH - LEG_SECTION) * s, pz * s),
                                PLANK_THICKNESS * s, PLANK_WIDTH * s,
                                fc=WOOD3, ec="black", lw=0.6))
    # Traverse laterale
    tz = SEAT_HEIGHT - PLANK_THICKNESS - BRACE_SECTION
    ax2.add_patch(Rectangle((LEG_SECTION * s, tz * s),
                            (SEAT_DEPTH - 2 * LEG_SECTION) * s, BRACE_SECTION * s,
                            fc=WOOD3, ec="black", lw=0.5))
    # Cotes
    _add_dim_h(ax2, 0, SEAT_DEPTH * s, total_h * s,
               f"{SEAT_DEPTH:.0f} mm", offset=8)
    _add_dim_v(ax2, SEAT_DEPTH * s, 0, SEAT_HEIGHT * s,
               f"{SEAT_HEIGHT:.0f}", offset=10)

    ax2.set_xlim(-15, SEAT_DEPTH * s + 40)
    ax2.set_ylim(-15, total_h * s + 30)
    ax2.grid(True, alpha=0.2)
    ax2.set_xlabel("mm")
    ax2.set_ylabel("mm")

    # ===================== VUE EMPILAGE =====================
    ax3 = fig.add_axes([0.68, 0.38, 0.28, 0.52])
    ax3.set_title("Vue empilage (face)", fontsize=10)
    ax3.set_aspect("equal")

    colors = [(WOOD1, WOOD2), (WOOD4, WOOD3)]
    for chair_idx in range(2):
        offset_x = chair_idx * ((FRONT_LEG_SPREAD - BACK_LEG_SPREAD) / 2.0 + STACK_CLEARANCE)
        offset_z = chair_idx * (PLANK_THICKNESS + BRACE_SECTION + STACK_CLEARANCE)
        c1, c2 = colors[chair_idx]
        alpha = 0.8 if chair_idx == 0 else 0.6
        s2 = 0.4
        # Pieds avant
        ax3.add_patch(Rectangle((offset_x * s2, offset_z * s2),
                                LEG_SECTION * s2, FRONT_LEG_HEIGHT * s2,
                                fc=c1, ec="black", lw=0.8, alpha=alpha))
        ax3.add_patch(Rectangle(((offset_x + FRONT_LEG_SPREAD - LEG_SECTION) * s2, offset_z * s2),
                                LEG_SECTION * s2, FRONT_LEG_HEIGHT * s2,
                                fc=c1, ec="black", lw=0.8, alpha=alpha))
        # Assise
        ax3.add_patch(Rectangle((offset_x * s2, (offset_z + SEAT_HEIGHT - PLANK_THICKNESS) * s2),
                                FRONT_LEG_SPREAD * s2, PLANK_THICKNESS * s2,
                                fc=c2, ec="black", lw=0.8, alpha=alpha))
        label = f"Chaise {chair_idx + 1}" if chair_idx < 2 else ""
        ax3.text((offset_x + FRONT_LEG_SPREAD / 2) * s2,
                 (offset_z + SEAT_HEIGHT / 2) * s2,
                 label, ha="center", va="center", fontsize=7, color="white",
                 fontweight="bold")

    ax3.set_xlim(-10, 300)
    ax3.set_ylim(-10, total_h * s2 + 40)
    ax3.grid(True, alpha=0.2)
    ax3.set_xlabel("mm")

    # ===================== CARTOUCHE =====================
    ax_info = fig.add_axes([0.04, 0.04, 0.92, 0.26])
    ax_info.axis("off")
    info = (
        "Objet : Chaise de Jardin Empilable en Palettes Recyclees\n"
        f"Dimensions : {FRONT_LEG_SPREAD:.0f} x {SEAT_DEPTH:.0f} x {BACK_LEG_HEIGHT:.0f} mm "
        f"(L x P x H)  |  Assise : {SEAT_HEIGHT:.0f} mm\n"
        f"Assise : {N_SEAT_PLANKS} lattes de {PLANK_WIDTH:.0f} x {PLANK_THICKNESS:.0f} mm  |  "
        f"Dossier : {N_BACK_PLANKS} lattes de {PLANK_WIDTH:.0f} x {PLANK_THICKNESS:.0f} mm\n"
        f"Pieds avant : {LEG_SECTION:.0f} x {LEG_SECTION:.0f} x {FRONT_LEG_HEIGHT:.0f} mm  |  "
        f"Pieds arriere : {LEG_SECTION:.0f} x {LEG_SECTION:.0f} x {BACK_LEG_HEIGHT:.0f} mm\n"
        "Materiau : Euro-palette recyclee  |  Echelle : 1:1 (mm)\n"
        "Inspire de : instructables.com/A-Deck-Chair-Made-From-Pallet-Wood-Leftovers"
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
