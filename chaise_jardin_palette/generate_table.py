"""
Deck chair de jardin en palettes recyclees - Modele 3D

Inspire fidellement du projet Instructables "A Deck Chair Made From
Pallet Wood Leftovers" par Well Done Tips.

Structure type palette : panneaux lateraux (planche basse + blocs +
planche haute), assise tres basse, dossier tres incline, sans
accoudoirs, longerons depassant loin a l'arriere.

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
from matplotlib.patches import Rectangle, Polygon
from matplotlib.backends.backend_pdf import PdfPages

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Dimensions (mm) - fidele au modele Instructables ---
CHAIR_WIDTH = 600.0

# Lattes (planches de palette pleine largeur)
SLAT_W = 95.0
SLAT_T = 22.0
SLAT_GAP = 15.0             # ecarts visibles comme sur l'original

# Panneau lateral style palette (planche basse + blocs + planche haute)
PANEL_W = 95.0               # largeur panneau = largeur planche
BLOCK_H = 78.0               # hauteur bloc palette standard
BLOCK_W = 44.0               # largeur bloc (2 planches collees)
BLOCK_D = 44.0               # profondeur bloc
PANEL_H = SLAT_T + BLOCK_H + SLAT_T   # = 122 mm

# Assise (tres basse, fesses presque au sol)
SEAT_H = PANEL_H + SLAT_T    # ~ 144 mm (surface d'assise)
N_SEAT_SLATS = 4              # 4 lattes (assise courte)
SEAT_DEPTH = N_SEAT_SLATS * SLAT_W + (N_SEAT_SLATS - 1) * SLAT_GAP  # ~ 425

# Longerons (depassent loin a l'arriere)
RUNNER_EXTEND = 350.0
RUNNER_L = SEAT_DEPTH + RUNNER_EXTEND  # ~ 775

# Dossier (tres incline, haut)
BACKREST_TILT = 35.0          # deg depuis la verticale (= ~125 deg de l'assise)
BACK_LENGTH = 650.0           # longueur supports dossier
N_BACK_SLATS = 5

# Structure dossier
FRAME_W = 44.0                # epaisseur support dossier (2 planches collees)
FRAME_D = 70.0

# Dimensions calculees
INNER_WIDTH = CHAIR_WIDTH - 2 * PANEL_W  # espace entre panneaux ~ 410
BACK_DZ = BACK_LENGTH * math.sin(math.radians(90 - BACKREST_TILT))
BACK_DY = BACK_LENGTH * math.sin(math.radians(BACKREST_TILT))
TOTAL_H = SEAT_H + BACK_DZ


def _box_faces(x, y, z, dx, dy, dz):
    """12 triangles (6 faces) d'un parallelipede."""
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


def _tilted_box_faces(x, y, z, width, depth, length, tilt_deg):
    """Parallelipede incline vers l'arriere (plan Y-Z)."""
    rad = math.radians(tilt_deg)
    dy = length * math.sin(rad)
    dz = length * math.cos(rad)
    v = np.array([
        [x, y, z], [x+width, y, z],
        [x+width, y+depth, z], [x, y+depth, z],
        [x, y+dy, z+dz], [x+width, y+dy, z+dz],
        [x+width, y+depth+dy, z+dz], [x, y+depth+dy, z+dz],
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

    # === PANNEAUX LATERAUX (x2) - structure palette ===
    for side_x in [0, CHAIR_WIDTH - PANEL_W]:
        # Planche basse (au sol)
        all_faces.extend(_box_faces(side_x, 0, 0,
                                    PANEL_W, RUNNER_L, SLAT_T))
        # 3 blocs (avant, milieu, arriere)
        bx = side_x + (PANEL_W - BLOCK_W) / 2
        for by in [30, SEAT_DEPTH / 2, RUNNER_L - 70]:
            all_faces.extend(_box_faces(bx, by, SLAT_T,
                                        BLOCK_W, BLOCK_D, BLOCK_H))
        # Planche haute
        all_faces.extend(_box_faces(side_x, 0, SLAT_T + BLOCK_H,
                                    PANEL_W, RUNNER_L, SLAT_T))

    # === LATTES D'ASSISE (x4) - pleine largeur, sur les panneaux ===
    for i in range(N_SEAT_SLATS):
        sy = i * (SLAT_W + SLAT_GAP)
        all_faces.extend(_box_faces(0, sy, PANEL_H,
                                    CHAIR_WIDTH, SLAT_W, SLAT_T))

    # === SUPPORTS DOSSIER (x2) - inclines, centres sur les panneaux ===
    back_y = SEAT_DEPTH
    for side_x in [0, CHAIR_WIDTH - PANEL_W]:
        bx = side_x + (PANEL_W - FRAME_W) / 2
        all_faces.extend(_tilted_box_faces(
            bx, back_y, PANEL_H + SLAT_T,
            FRAME_W, FRAME_D, BACK_LENGTH, BACKREST_TILT))

    # === LATTES DE DOSSIER (x5) - entre les panneaux lateraux ===
    back_start_x = PANEL_W
    back_slat_w = INNER_WIDTH
    for i in range(N_BACK_SLATS):
        frac = (i + 0.5) / N_BACK_SLATS
        bz = PANEL_H + SLAT_T + frac * BACK_DZ
        by = back_y + frac * BACK_DY
        all_faces.extend(_box_faces(back_start_x, by, bz,
                                    back_slat_w, SLAT_T, SLAT_W))

    # === TRAVERSE AVANT (entre les panneaux, sous l'assise) ===
    all_faces.extend(_box_faces(PANEL_W, 0, PANEL_H - SLAT_T,
                                INNER_WIDTH, FRAME_W, SLAT_T))

    # Construire mesh
    faces_array = np.array(all_faces)
    m = mesh.Mesh(np.zeros(faces_array.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces_array):
        m.vectors[i] = f

    stl_path = os.path.join(OUTPUT_DIR, "chaise_jardin_palette.stl")
    m.save(stl_path)
    print(f"STL genere: {stl_path}")
    return stl_path


# ---------- helpers PDF ----------
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
    ax.text(xo+3, (y1+y2)/2, label, ha="left", va="center", fontsize=7,
            color="blue", rotation=90)


def generate_pdf():
    """Genere le plan technique PDF."""
    pdf_path = os.path.join(OUTPUT_DIR, "chaise_jardin_palette_plan.pdf")
    W1, W2, W3, W4 = "#d2a679", "#c49a6c", "#b8956a", "#a0784e"

    fig = plt.figure(figsize=(11.69, 8.27))
    fig.suptitle("Plan Technique - Deck Chair en Palettes Recyclees",
                 fontsize=13, fontweight="bold")

    # ===================== VUE DE COTE =====================
    ax1 = fig.add_axes([0.04, 0.38, 0.30, 0.52])
    ax1.set_title("Vue de cote", fontsize=10)
    ax1.set_aspect("equal")

    s = 0.22
    # Panneau lateral - planche basse
    ax1.add_patch(Rectangle((0, 0), RUNNER_L*s, SLAT_T*s,
                             fc=W1, ec="black", lw=1))
    # Blocs
    for by in [30, SEAT_DEPTH/2, RUNNER_L - 70]:
        ax1.add_patch(Rectangle((by*s, SLAT_T*s), BLOCK_D*s, BLOCK_H*s,
                                 fc=W4, ec="black", lw=0.8))
    # Planche haute
    ax1.add_patch(Rectangle((0, (SLAT_T+BLOCK_H)*s), RUNNER_L*s, SLAT_T*s,
                             fc=W1, ec="black", lw=1))

    # Lattes assise
    for i in range(N_SEAT_SLATS):
        sy = i * (SLAT_W + SLAT_GAP)
        ax1.add_patch(Rectangle((sy*s, PANEL_H*s),
                                SLAT_W*s, SLAT_T*s, fc=W2, ec="black", lw=0.6))

    # Support dossier (incline)
    back_y0 = SEAT_DEPTH * s
    seat_top = (PANEL_H + SLAT_T) * s
    back_pts = [
        [back_y0, seat_top],
        [back_y0 + FRAME_D*s, seat_top],
        [back_y0 + FRAME_D*s + BACK_DY*s, seat_top + BACK_DZ*s],
        [back_y0 + BACK_DY*s, seat_top + BACK_DZ*s],
    ]
    ax1.add_patch(Polygon(back_pts, closed=True, fc=W1, ec="black", lw=1.2))

    # Lattes dossier
    for i in range(N_BACK_SLATS):
        frac = (i + 0.5) / N_BACK_SLATS
        bz = PANEL_H + SLAT_T + frac * BACK_DZ
        by = SEAT_DEPTH + frac * BACK_DY
        ax1.add_patch(Rectangle((by*s, bz*s), SLAT_T*s, SLAT_W*s,
                                fc=W3, ec="black", lw=0.6))

    _add_dim_h(ax1, 0, RUNNER_L*s, TOTAL_H*s, f"{RUNNER_L:.0f} mm", offset=8)
    _add_dim_v(ax1, -5, 0, SEAT_H*s, f"{SEAT_H:.0f}", offset=-18)
    _add_dim_v(ax1, RUNNER_L*s, 0, TOTAL_H*s, f"{TOTAL_H:.0f}", offset=12)
    ax1.text(back_y0 + 20*s, seat_top + 30*s,
             f"~{90 + BACKREST_TILT:.0f}deg", fontsize=8, color="red",
             fontweight="bold")

    ax1.set_xlim(-25, RUNNER_L*s + 45)
    ax1.set_ylim(-12, TOTAL_H*s + 25)
    ax1.grid(True, alpha=0.2)
    ax1.set_xlabel("mm"); ax1.set_ylabel("mm")

    # ===================== VUE DE FACE =====================
    ax2 = fig.add_axes([0.38, 0.38, 0.28, 0.52])
    ax2.set_title("Vue de face", fontsize=10)
    ax2.set_aspect("equal")

    s2 = 0.28
    # Panneaux lateraux
    for px in [0, (CHAIR_WIDTH - PANEL_W)*s2]:
        # Planche basse
        ax2.add_patch(Rectangle((px, 0), PANEL_W*s2, SLAT_T*s2,
                                 fc=W1, ec="black", lw=0.8))
        # Bloc visible (front)
        bx = px + ((PANEL_W - BLOCK_W)/2)*s2
        ax2.add_patch(Rectangle((bx, SLAT_T*s2), BLOCK_W*s2, BLOCK_H*s2,
                                 fc=W4, ec="black", lw=0.8))
        # Planche haute
        ax2.add_patch(Rectangle((px, (SLAT_T+BLOCK_H)*s2), PANEL_W*s2, SLAT_T*s2,
                                 fc=W1, ec="black", lw=0.8))

    # Assise (simplifiee)
    ax2.add_patch(Rectangle((0, PANEL_H*s2), CHAIR_WIDTH*s2, SLAT_T*s2,
                             fc=W2, ec="black", lw=1))

    # Supports dossier (pointilles, en retrait)
    for px in [0, (CHAIR_WIDTH - PANEL_W)*s2]:
        bx = px + ((PANEL_W - FRAME_W)/2)*s2
        ax2.add_patch(Rectangle((bx, SEAT_H*s2), FRAME_W*s2, BACK_DZ*s2,
                                 fc=W1, ec="black", lw=0.6, ls="--", alpha=0.5))

    # Dossier lattes
    for i in range(N_BACK_SLATS):
        frac = (i + 0.5) / N_BACK_SLATS
        bz = SEAT_H + frac * BACK_DZ
        ax2.add_patch(Rectangle((PANEL_W*s2, bz*s2),
                                INNER_WIDTH*s2, SLAT_W*s2,
                                fc=W3, ec="black", lw=0.5))

    # Traverse avant
    ax2.add_patch(Rectangle((PANEL_W*s2, (PANEL_H - SLAT_T)*s2),
                             INNER_WIDTH*s2, SLAT_T*s2,
                             fc=W3, ec="black", lw=0.5))

    _add_dim_h(ax2, 0, CHAIR_WIDTH*s2, TOTAL_H*s2,
               f"{CHAIR_WIDTH:.0f} mm", offset=8)
    _add_dim_v(ax2, CHAIR_WIDTH*s2, 0, TOTAL_H*s2,
               f"{TOTAL_H:.0f}", offset=12)

    ax2.set_xlim(-15, CHAIR_WIDTH*s2 + 40)
    ax2.set_ylim(-12, TOTAL_H*s2 + 25)
    ax2.grid(True, alpha=0.2)
    ax2.set_xlabel("mm"); ax2.set_ylabel("mm")

    # ===================== VUE DESSUS =====================
    ax3 = fig.add_axes([0.70, 0.38, 0.27, 0.52])
    ax3.set_title("Vue de dessus", fontsize=10)
    ax3.set_aspect("equal")

    s3 = 0.10
    # Panneaux lateraux
    ax3.add_patch(Rectangle((0, 0), PANEL_W*s3, RUNNER_L*s3,
                             fc=W1, ec="black", lw=0.8))
    ax3.add_patch(Rectangle(((CHAIR_WIDTH - PANEL_W)*s3, 0),
                             PANEL_W*s3, RUNNER_L*s3,
                             fc=W1, ec="black", lw=0.8))
    # Lattes assise
    colors = [W2, W1, W3, W2]
    for i in range(N_SEAT_SLATS):
        sy = i * (SLAT_W + SLAT_GAP)
        ax3.add_patch(Rectangle((0, sy*s3), CHAIR_WIDTH*s3, SLAT_W*s3,
                                fc=colors[i % len(colors)], ec="black", lw=0.4))

    _add_dim_h(ax3, 0, CHAIR_WIDTH*s3, RUNNER_L*s3,
               f"{CHAIR_WIDTH:.0f} mm", offset=5)
    _add_dim_v(ax3, CHAIR_WIDTH*s3, 0, RUNNER_L*s3,
               f"{RUNNER_L:.0f} mm", offset=8)

    ax3.set_xlim(-8, CHAIR_WIDTH*s3 + 25)
    ax3.set_ylim(-8, RUNNER_L*s3 + 20)
    ax3.grid(True, alpha=0.2)
    ax3.set_xlabel("mm"); ax3.set_ylabel("mm")

    # ===================== CARTOUCHE =====================
    ax_info = fig.add_axes([0.04, 0.04, 0.92, 0.26])
    ax_info.axis("off")
    n_pieces = N_SEAT_SLATS + N_BACK_SLATS + 4 + 6 + 2 + 1  # A+B+C/D+E+F+G
    info = (
        "Objet : Deck Chair de Jardin en Palettes Recyclees\n"
        f"Dimensions : {CHAIR_WIDTH:.0f} x {RUNNER_L:.0f} x {TOTAL_H:.0f} mm "
        f"(L x P x H)  |  Assise : {SEAT_H:.0f} mm\n"
        f"Assise : {N_SEAT_SLATS} lattes de {SLAT_W:.0f} x {SLAT_T:.0f} mm  |  "
        f"Dossier : {N_BACK_SLATS} lattes, incline ~{90 + BACKREST_TILT:.0f} deg\n"
        f"Panneaux lateraux style palette (planche + blocs {BLOCK_H:.0f} mm + planche)\n"
        f"Sans accoudoirs  |  Longerons depassent de {RUNNER_EXTEND:.0f} mm "
        f"a l'arriere\n"
        f"Materiau : 1 euro-palette  |  {n_pieces} pieces  |  Echelle 1:1 (mm)\n"
        "Inspire de : instructables.com/A-Deck-Chair-Made-From-Pallet-Wood-Leftovers"
    )
    ax_info.text(0.5, 0.5, info, transform=ax_info.transAxes,
                 fontsize=8, va="center", ha="center",
                 bbox=dict(boxstyle="round,pad=0.5", facecolor="#f5e6d3",
                           edgecolor="black"),
                 family="monospace")

    plt.savefig(pdf_path, format="pdf", dpi=150)
    plt.close()
    print(f"PDF technique genere: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    generate_stl()
    generate_pdf()
    print("\nGeneration terminee!")
