"""
Chaise de jardin type deck chair en palettes recyclees - Modele 3D

Inspiree du projet Instructables "A Deck Chair Made From Pallet Wood Leftovers".
Design classique deck chair : assise basse et legerement inclinee, dossier
recline a ~110 degres, accoudoirs larges, 2 cadres lateraux.

Adaptee pour accompagner la table basse palette (450 mm) :
assise a ~350 mm, compatible empilage.

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
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch
from matplotlib.backends.backend_pdf import PdfPages

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Dimensions (mm) - style deck chair / Adirondack ---
# Gabarit global
CHAIR_WIDTH = 600.0         # largeur totale (ext. accoudoirs)
SEAT_WIDTH = 500.0          # largeur interieure (entre cadres lateraux)

# Pieds avant (courts, verticaux)
FRONT_LEG_W = 44.0          # 2 lattes collees
FRONT_LEG_D = 70.0          # profondeur pied avant
FRONT_LEG_H = 350.0         # hauteur = hauteur assise avant

# Pieds arriere (longs, inclines, montent au dossier)
BACK_LEG_W = 44.0
BACK_LEG_D = 70.0
BACK_LEG_H = 900.0          # hauteur totale pied arriere
BACK_LEG_ANGLE = 15.0       # inclinaison vers l'arriere (degres)

# Assise
SEAT_DEPTH = 480.0          # profondeur assise
SEAT_FRONT_H = 350.0        # hauteur avant de l'assise
SEAT_BACK_H = 300.0         # hauteur arriere (assise inclinee ~6 deg)
N_SEAT_SLATS = 6            # nombre de lattes assise
SLAT_WIDTH = 70.0           # largeur latte (refendue)
SLAT_THICKNESS = 22.0
SLAT_GAP = 5.0

# Dossier
BACKREST_ANGLE = 110.0      # angle dossier/assise (degres)
BACKREST_H = 500.0          # hauteur utile du dossier
N_BACK_SLATS = 5            # nombre de lattes dossier

# Accoudoirs
ARMREST_L = 550.0           # longueur accoudoir
ARMREST_W = 95.0            # largeur (latte pleine)
ARMREST_T = 22.0            # epaisseur
ARMREST_H = 600.0           # hauteur du dessus de l'accoudoir

# Traverses
BRACE_SECTION = 44.0
BRACE_T = 22.0

# Empilabilite
STACK_TAPER = 30.0          # retrecissement pieds arriere pour empilage


def _box_faces(x, y, z, dx, dy, dz):
    """Genere les 12 triangles (6 faces) d'un parallelipede."""
    v = np.array([
        [x, y, z], [x+dx, y, z], [x+dx, y+dy, z], [x, y+dy, z],
        [x, y, z+dz], [x+dx, y, z+dz], [x+dx, y+dy, z+dz], [x, y+dy, z+dz],
    ])
    return [
        [v[0],v[2],v[1]], [v[0],v[3],v[2]],
        [v[4],v[5],v[6]], [v[4],v[6],v[7]],
        [v[0],v[1],v[5]], [v[0],v[5],v[4]],
        [v[2],v[3],v[7]], [v[2],v[7],v[6]],
        [v[0],v[4],v[7]], [v[0],v[7],v[3]],
        [v[1],v[2],v[6]], [v[1],v[6],v[5]],
    ]


def generate_stl():
    """Genere le fichier STL de la deck chair."""
    all_faces = []
    rad = math.radians(BACK_LEG_ANGLE)
    back_offset_y = math.sin(rad) * BACK_LEG_H  # recul du haut du pied arriere

    # --- Pieds avant (x2) ---
    for side_x in [0, CHAIR_WIDTH - FRONT_LEG_W]:
        all_faces.extend(_box_faces(side_x, 0, 0,
                                    FRONT_LEG_W, FRONT_LEG_D, FRONT_LEG_H))

    # --- Pieds arriere (x2, verticaux simplifies pour STL) ---
    back_y = SEAT_DEPTH - BACK_LEG_D
    taper = STACK_TAPER
    for side_x in [taper, CHAIR_WIDTH - BACK_LEG_W - taper]:
        all_faces.extend(_box_faces(side_x, back_y, 0,
                                    BACK_LEG_W, BACK_LEG_D, BACK_LEG_H))

    # --- Assise (lattes inclinees) ---
    total_slats_w = N_SEAT_SLATS * SLAT_WIDTH + (N_SEAT_SLATS - 1) * SLAT_GAP
    slat_start_x = (CHAIR_WIDTH - total_slats_w) / 2
    for i in range(N_SEAT_SLATS):
        sx = slat_start_x + i * (SLAT_WIDTH + SLAT_GAP)
        # Assise legerement inclinee (avant plus haut)
        z_front = SEAT_FRONT_H - SLAT_THICKNESS
        all_faces.extend(_box_faces(sx, 0, z_front,
                                    SLAT_WIDTH, SEAT_DEPTH, SLAT_THICKNESS))

    # --- Dossier (lattes) ---
    back_plank_w = SEAT_WIDTH - 2 * BACK_LEG_W + 2 * taper
    back_start_x = (CHAIR_WIDTH - back_plank_w) / 2
    for i in range(N_BACK_SLATS):
        bz = SEAT_FRONT_H + 30 + i * (SLAT_WIDTH + SLAT_GAP)
        all_faces.extend(_box_faces(back_start_x, back_y, bz,
                                    back_plank_w, SLAT_THICKNESS, SLAT_WIDTH))

    # --- Accoudoirs (x2) ---
    for side_x in [0, CHAIR_WIDTH - ARMREST_W]:
        all_faces.extend(_box_faces(side_x, 0, ARMREST_H,
                                    ARMREST_W, ARMREST_L, ARMREST_T))

    # --- Traverses structure ---
    # Avant
    all_faces.extend(_box_faces(FRONT_LEG_W, 0, SEAT_FRONT_H - SLAT_THICKNESS - BRACE_T,
                                CHAIR_WIDTH - 2 * FRONT_LEG_W, BRACE_T, BRACE_T))
    # Arriere
    all_faces.extend(_box_faces(taper + BACK_LEG_W, back_y,
                                SEAT_BACK_H - SLAT_THICKNESS - BRACE_T,
                                CHAIR_WIDTH - 2*(taper + BACK_LEG_W), BRACE_T, BRACE_T))
    # Laterales
    for side_x in [0, CHAIR_WIDTH - FRONT_LEG_W]:
        all_faces.extend(_box_faces(side_x, FRONT_LEG_D,
                                    SEAT_FRONT_H - SLAT_THICKNESS - BRACE_T,
                                    FRONT_LEG_W, SEAT_DEPTH - FRONT_LEG_D - BACK_LEG_D,
                                    BRACE_T))
    # Barre basse avant
    all_faces.extend(_box_faces(FRONT_LEG_W, 0, 100,
                                CHAIR_WIDTH - 2 * FRONT_LEG_W, BRACE_T, BRACE_T))

    # --- Construire mesh ---
    faces_array = np.array(all_faces)
    m = mesh.Mesh(np.zeros(faces_array.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces_array):
        m.vectors[i] = f

    stl_path = os.path.join(OUTPUT_DIR, "chaise_jardin_palette.stl")
    m.save(stl_path)
    print(f"STL genere: {stl_path}")
    return stl_path


def _add_dim_h(ax, x1, x2, y, label, offset=8):
    yo = y + offset
    ax.annotate("", xy=(x2, yo), xytext=(x1, yo),
                arrowprops=dict(arrowstyle="<->", color="blue", lw=0.8))
    ax.plot([x1, x1], [y, yo], "b-", lw=0.4)
    ax.plot([x2, x2], [y, yo], "b-", lw=0.4)
    ax.text((x1+x2)/2, yo+3, label, ha="center", fontsize=7, color="blue")

def _add_dim_v(ax, x, y1, y2, label, offset=8):
    xo = x + offset
    ax.annotate("", xy=(xo, y2), xytext=(xo, y1),
                arrowprops=dict(arrowstyle="<->", color="blue", lw=0.8))
    ax.plot([x, xo], [y1, y1], "b-", lw=0.4)
    ax.plot([x, xo], [y2, y2], "b-", lw=0.4)
    ax.text(xo+3, (y1+y2)/2, label, ha="left", va="center", fontsize=7, color="blue", rotation=90)


def generate_pdf():
    """Genere le plan technique PDF de la deck chair."""
    pdf_path = os.path.join(OUTPUT_DIR, "chaise_jardin_palette_plan.pdf")
    W1, W2, W3, W4 = "#d2a679", "#c49a6c", "#b8956a", "#a0784e"

    fig = plt.figure(figsize=(11.69, 8.27))
    fig.suptitle("Plan Technique - Deck Chair en Palettes Recyclees",
                 fontsize=13, fontweight="bold")

    # ===================== VUE DE COTE =====================
    ax1 = fig.add_axes([0.04, 0.38, 0.30, 0.52])
    ax1.set_title("Vue de cote", fontsize=10)
    ax1.set_aspect("equal")

    s = 0.45  # scale
    # Pied avant
    ax1.add_patch(Rectangle((0, 0), FRONT_LEG_D*s, FRONT_LEG_H*s,
                            fc=W1, ec="black", lw=1.2))
    # Pied arriere (incline dans la vue de cote)
    back_y0 = SEAT_DEPTH - BACK_LEG_D
    ax1.add_patch(Rectangle((back_y0*s, 0), BACK_LEG_D*s, BACK_LEG_H*s,
                            fc=W1, ec="black", lw=1.2))
    # Assise (lattes) - legerement inclinee
    for i in range(3):  # representation simplifiee
        ax1.add_patch(Rectangle((i*SEAT_DEPTH/3*s, (SEAT_FRONT_H - SLAT_THICKNESS)*s),
                                (SEAT_DEPTH/3)*s, SLAT_THICKNESS*s,
                                fc=W2, ec="black", lw=0.6))
    # Dossier
    for i in range(N_BACK_SLATS):
        bz = SEAT_FRONT_H + 30 + i * (SLAT_WIDTH + SLAT_GAP)
        ax1.add_patch(Rectangle((back_y0*s, bz*s),
                                SLAT_THICKNESS*s, SLAT_WIDTH*s,
                                fc=W3, ec="black", lw=0.6))
    # Accoudoir
    ax1.add_patch(Rectangle((0, ARMREST_H*s), ARMREST_L*s, ARMREST_T*s,
                            fc=W2, ec="black", lw=1, ls="--"))
    ax1.text(ARMREST_L*s/2, (ARMREST_H+ARMREST_T)*s+3, "Accoudoir", ha="center", fontsize=7, color=W4)
    # Traverse basse
    ax1.add_patch(Rectangle((FRONT_LEG_D*s, 100*s),
                            (back_y0-FRONT_LEG_D)*s, BRACE_T*s,
                            fc=W3, ec="black", lw=0.5))
    # Cotes
    _add_dim_h(ax1, 0, SEAT_DEPTH*s, BACK_LEG_H*s, f"{SEAT_DEPTH:.0f} mm", offset=8)
    _add_dim_v(ax1, SEAT_DEPTH*s, 0, SEAT_FRONT_H*s, f"{SEAT_FRONT_H:.0f}", offset=10)
    _add_dim_v(ax1, SEAT_DEPTH*s+20, 0, BACK_LEG_H*s, f"{BACK_LEG_H:.0f}", offset=0)
    # Angle dossier
    ax1.text(back_y0*s+15, (SEAT_FRONT_H+100)*s, f"~{BACKREST_ANGLE:.0f}deg",
             fontsize=8, color="red", fontweight="bold")

    ax1.set_xlim(-15, SEAT_DEPTH*s+50)
    ax1.set_ylim(-15, BACK_LEG_H*s+30)
    ax1.grid(True, alpha=0.2)
    ax1.set_xlabel("mm"); ax1.set_ylabel("mm")

    # ===================== VUE DE FACE =====================
    ax2 = fig.add_axes([0.38, 0.38, 0.28, 0.52])
    ax2.set_title("Vue de face", fontsize=10)
    ax2.set_aspect("equal")

    s2 = 0.4
    # Pieds avant
    ax2.add_patch(Rectangle((0, 0), FRONT_LEG_W*s2, FRONT_LEG_H*s2,
                            fc=W1, ec="black", lw=1))
    ax2.add_patch(Rectangle(((CHAIR_WIDTH-FRONT_LEG_W)*s2, 0),
                            FRONT_LEG_W*s2, FRONT_LEG_H*s2,
                            fc=W1, ec="black", lw=1))
    # Pieds arriere (en retrait, pointilles)
    t = STACK_TAPER
    ax2.add_patch(Rectangle((t*s2, 0), BACK_LEG_W*s2, BACK_LEG_H*s2,
                            fc=W1, ec="black", lw=0.7, ls="--", alpha=0.5))
    ax2.add_patch(Rectangle(((CHAIR_WIDTH-BACK_LEG_W-t)*s2, 0),
                            BACK_LEG_W*s2, BACK_LEG_H*s2,
                            fc=W1, ec="black", lw=0.7, ls="--", alpha=0.5))
    # Assise
    ax2.add_patch(Rectangle((0, (SEAT_FRONT_H-SLAT_THICKNESS)*s2),
                            CHAIR_WIDTH*s2, SLAT_THICKNESS*s2,
                            fc=W2, ec="black", lw=1))
    # Accoudoirs
    for ax_x in [0, (CHAIR_WIDTH-ARMREST_W)*s2]:
        ax2.add_patch(Rectangle((ax_x, ARMREST_H*s2),
                                ARMREST_W*s2, ARMREST_T*s2,
                                fc=W2, ec="black", lw=0.8))
    # Dossier lattes
    for i in range(N_BACK_SLATS):
        bz = SEAT_FRONT_H + 30 + i * (SLAT_WIDTH + SLAT_GAP)
        bw = SEAT_WIDTH - 2*BACK_LEG_W + 2*t
        bx0 = (CHAIR_WIDTH - bw) / 2
        ax2.add_patch(Rectangle((bx0*s2, bz*s2), bw*s2, SLAT_WIDTH*s2,
                                fc=W3, ec="black", lw=0.5))
    # Traverse basse
    ax2.add_patch(Rectangle((FRONT_LEG_W*s2, 100*s2),
                            (CHAIR_WIDTH-2*FRONT_LEG_W)*s2, BRACE_T*s2,
                            fc=W3, ec="black", lw=0.5))
    # Cotes
    _add_dim_h(ax2, 0, CHAIR_WIDTH*s2, BACK_LEG_H*s2, f"{CHAIR_WIDTH:.0f} mm", offset=8)
    _add_dim_v(ax2, CHAIR_WIDTH*s2, 0, ARMREST_H*s2, f"{ARMREST_H:.0f}", offset=12)

    ax2.set_xlim(-15, CHAIR_WIDTH*s2+40)
    ax2.set_ylim(-15, BACK_LEG_H*s2+30)
    ax2.grid(True, alpha=0.2)
    ax2.set_xlabel("mm"); ax2.set_ylabel("mm")

    # ===================== VUE DESSUS =====================
    ax3 = fig.add_axes([0.70, 0.38, 0.27, 0.52])
    ax3.set_title("Vue de dessus", fontsize=10)
    ax3.set_aspect("equal")

    s3 = 0.12
    # Accoudoirs
    ax3.add_patch(Rectangle((0, 0), ARMREST_W*s3, ARMREST_L*s3,
                            fc=W2, ec="black", lw=0.8))
    ax3.add_patch(Rectangle(((CHAIR_WIDTH-ARMREST_W)*s3, 0),
                            ARMREST_W*s3, ARMREST_L*s3,
                            fc=W2, ec="black", lw=0.8))
    # Lattes assise
    total_sw = N_SEAT_SLATS * SLAT_WIDTH + (N_SEAT_SLATS-1) * SLAT_GAP
    ss = (CHAIR_WIDTH - total_sw) / 2
    colors = [W2, W1, W3, W2, W1, W3]
    for i in range(N_SEAT_SLATS):
        sx = ss + i * (SLAT_WIDTH + SLAT_GAP)
        ax3.add_patch(Rectangle((sx*s3, ARMREST_W*s3*0.3), SLAT_WIDTH*s3, SEAT_DEPTH*s3,
                                fc=colors[i%len(colors)], ec="black", lw=0.4))
    # Cotes
    _add_dim_h(ax3, 0, CHAIR_WIDTH*s3, ARMREST_L*s3, f"{CHAIR_WIDTH:.0f} mm", offset=5)
    _add_dim_v(ax3, CHAIR_WIDTH*s3, 0, ARMREST_L*s3, f"{ARMREST_L:.0f} mm", offset=8)

    ax3.set_xlim(-8, CHAIR_WIDTH*s3+25)
    ax3.set_ylim(-8, ARMREST_L*s3+20)
    ax3.grid(True, alpha=0.2)
    ax3.set_xlabel("mm"); ax3.set_ylabel("mm")

    # ===================== CARTOUCHE =====================
    ax_info = fig.add_axes([0.04, 0.04, 0.92, 0.26])
    ax_info.axis("off")
    info = (
        "Objet : Deck Chair de Jardin en Palettes Recyclees (style Adirondack)\n"
        f"Dimensions : {CHAIR_WIDTH:.0f} x {SEAT_DEPTH:.0f} x {BACK_LEG_H:.0f} mm "
        f"(L x P x H)  |  Assise : {SEAT_FRONT_H:.0f} mm  |  Accoudoirs : {ARMREST_H:.0f} mm\n"
        f"Assise : {N_SEAT_SLATS} lattes de {SLAT_WIDTH:.0f} x {SLAT_THICKNESS:.0f} mm  |  "
        f"Dossier : {N_BACK_SLATS} lattes, incline ~{BACKREST_ANGLE:.0f} deg\n"
        f"Accoudoirs : {ARMREST_W:.0f} x {ARMREST_L:.0f} x {ARMREST_T:.0f} mm  |  "
        f"Pieds avant : {FRONT_LEG_H:.0f} mm  |  Pieds arriere : {BACK_LEG_H:.0f} mm\n"
        "Materiau : 1.5 euro-palettes recyclees  |  Echelle : 1:1 (mm)\n"
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
