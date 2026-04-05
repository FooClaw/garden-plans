"""
Deck chair de jardin en palettes recyclees - Modele 3D

Inspire fidellement du projet Instructables "A Deck Chair Made From
Pallet Wood Leftovers" par Well Done Tips. Design minimaliste :
assise tres basse, dossier incline, pas d'accoudoirs, longerons
au sol depassant a l'arriere pour la stabilite.

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
CHAIR_WIDTH = 600.0         # largeur totale

# Lattes (planches de palette pleine largeur, non refendues)
SLAT_W = 95.0               # largeur pleine d'une planche palette
SLAT_T = 22.0               # epaisseur
SLAT_GAP = 10.0             # espace entre lattes (visible comme sur l'original)

# Structure laterale (section doublee : 2 planches collees)
FRAME_W = 44.0              # epaisseur cadre (2 x 22 mm)
FRAME_D = 70.0              # profondeur cadre

# Assise (tres basse, comme sur les photos)
SEAT_H = 180.0              # hauteur assise (genoux au-dessus des hanches)
N_SEAT_SLATS = 4            # 4 lattes (assise courte, jambes depassent)
SEAT_DEPTH = N_SEAT_SLATS * SLAT_W + (N_SEAT_SLATS - 1) * SLAT_GAP  # ~410

# Pieds avant (tres courts, a peine visibles)
FRONT_LEG_H = SEAT_H

# Longerons lateraux (au sol, depassent loin a l'arriere pour stabilite)
RUNNER_EXTEND = 300.0       # depassement a l'arriere (stabilite)
RUNNER_L = SEAT_DEPTH + RUNNER_EXTEND  # longueur totale ~710

# Dossier (plus incline et plus haut que la version precedente)
BACKREST_TILT = 30.0        # inclinaison du dossier (deg depuis la verticale)
BACK_LENGTH = 600.0         # longueur des supports dossier (plus haut)
N_BACK_SLATS = 5            # 5 lattes dossier

# Dimensions calculees
INNER_WIDTH = CHAIR_WIDTH - 2 * FRAME_W    # largeur interieure (~512)
BACK_DY = BACK_LENGTH * math.sin(math.radians(BACKREST_TILT))  # recul
BACK_DZ = BACK_LENGTH * math.cos(math.radians(BACKREST_TILT))  # montee
TOTAL_H = SEAT_H + BACK_DZ                                     # ~703


def _box_faces(x, y, z, dx, dy, dz):
    """12 triangles (6 faces) d'un parallelipede aligne sur les axes."""
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
    """Parallelipede incline vers l'arriere (plan Y-Z).
    Base a (x, y, z), s'eleve de 'length' mm en s'inclinant de tilt_deg."""
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

    # --- Longerons lateraux (x2) : au sol, depassent a l'arriere ---
    for side_x in [0, CHAIR_WIDTH - FRAME_W]:
        all_faces.extend(_box_faces(side_x, 0, 0,
                                    FRAME_W, RUNNER_L, FRAME_W))

    # --- Pieds avant (x2) : verticaux, courts ---
    for side_x in [0, CHAIR_WIDTH - FRAME_W]:
        all_faces.extend(_box_faces(side_x, 0, FRAME_W,
                                    FRAME_W, FRAME_D, FRONT_LEG_H - FRAME_W))

    # --- Supports dossier (x2) : inclines vers l'arriere ---
    back_y = SEAT_DEPTH - FRAME_D  # depart a l'arriere de l'assise
    for side_x in [0, CHAIR_WIDTH - FRAME_W]:
        all_faces.extend(_tilted_box_faces(
            side_x, back_y, SEAT_H,
            FRAME_W, FRAME_D, BACK_LENGTH, BACKREST_TILT))

    # --- Lattes d'assise (x5) : pleine largeur ---
    for i in range(N_SEAT_SLATS):
        sy = i * (SLAT_W + SLAT_GAP)
        all_faces.extend(_box_faces(0, sy, SEAT_H - SLAT_T,
                                    CHAIR_WIDTH, SLAT_W, SLAT_T))

    # --- Lattes de dossier (x4) : fixees sur les supports inclines ---
    back_slat_len = INNER_WIDTH  # largeur entre supports
    back_start_x = FRAME_W
    for i in range(N_BACK_SLATS):
        frac = (i + 0.5) / N_BACK_SLATS
        # Position le long du support incline
        bz = SEAT_H + frac * BACK_DZ
        by = back_y + frac * BACK_DY
        all_faces.extend(_box_faces(back_start_x, by, bz,
                                    back_slat_len, SLAT_T, SLAT_W))

    # --- Traverse avant (relie les 2 pieds avant) ---
    all_faces.extend(_box_faces(FRAME_W, 0, SEAT_H - SLAT_T - FRAME_W,
                                INNER_WIDTH, FRAME_W, SLAT_T))

    # --- Traverse basse arriere (renfort entre longerons) ---
    all_faces.extend(_box_faces(FRAME_W, RUNNER_L - FRAME_D, 0,
                                INNER_WIDTH, SLAT_T, SLAT_T))

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

    s = 0.25  # echelle
    # Longeron (au sol)
    ax1.add_patch(Rectangle((0, 0), RUNNER_L*s, FRAME_W*s,
                             fc=W1, ec="black", lw=1.2))
    # Pied avant
    ax1.add_patch(Rectangle((0, FRAME_W*s), FRAME_D*s,
                             (FRONT_LEG_H - FRAME_W)*s,
                             fc=W1, ec="black", lw=1))
    # Support dossier (incline)
    back_y0 = (SEAT_DEPTH - FRAME_D) * s
    back_pts = np.array([
        [back_y0, SEAT_H*s],
        [back_y0 + FRAME_D*s, SEAT_H*s],
        [back_y0 + FRAME_D*s + BACK_DY*s, (SEAT_H + BACK_DZ)*s],
        [back_y0 + BACK_DY*s, (SEAT_H + BACK_DZ)*s],
    ])
    ax1.add_patch(Polygon(back_pts, closed=True, fc=W1, ec="black", lw=1.2))

    # Lattes assise
    for i in range(N_SEAT_SLATS):
        sy = i * (SLAT_W + SLAT_GAP)
        ax1.add_patch(Rectangle((sy*s, (SEAT_H - SLAT_T)*s),
                                SLAT_W*s, SLAT_T*s, fc=W2, ec="black", lw=0.6))
    # Lattes dossier
    for i in range(N_BACK_SLATS):
        frac = (i + 0.5) / N_BACK_SLATS
        bz = SEAT_H + frac * BACK_DZ
        by = (SEAT_DEPTH - FRAME_D) + frac * BACK_DY
        ax1.add_patch(Rectangle((by*s, bz*s), SLAT_T*s, SLAT_W*s,
                                fc=W3, ec="black", lw=0.6))

    # Cotes
    _add_dim_h(ax1, 0, RUNNER_L*s, TOTAL_H*s, f"{RUNNER_L:.0f} mm", offset=8)
    _add_dim_v(ax1, -5, 0, SEAT_H*s, f"{SEAT_H:.0f}", offset=-15)
    _add_dim_v(ax1, RUNNER_L*s, 0, TOTAL_H*s, f"{TOTAL_H:.0f}", offset=12)

    # Angle
    ax1.text(back_y0 + 15, (SEAT_H + 50)*s,
             f"~{90 + BACKREST_TILT:.0f}deg", fontsize=8, color="red",
             fontweight="bold")

    ax1.set_xlim(-25, RUNNER_L*s + 45)
    ax1.set_ylim(-15, TOTAL_H*s + 25)
    ax1.grid(True, alpha=0.2)
    ax1.set_xlabel("mm"); ax1.set_ylabel("mm")

    # ===================== VUE DE FACE =====================
    ax2 = fig.add_axes([0.38, 0.38, 0.28, 0.52])
    ax2.set_title("Vue de face", fontsize=10)
    ax2.set_aspect("equal")

    s2 = 0.3
    # Pieds avant
    ax2.add_patch(Rectangle((0, 0), FRAME_W*s2, FRONT_LEG_H*s2,
                             fc=W1, ec="black", lw=1))
    ax2.add_patch(Rectangle(((CHAIR_WIDTH - FRAME_W)*s2, 0),
                             FRAME_W*s2, FRONT_LEG_H*s2,
                             fc=W1, ec="black", lw=1))
    # Supports dossier (en retrait, pointilles)
    ax2.add_patch(Rectangle((0, SEAT_H*s2), FRAME_W*s2,
                             BACK_DZ*s2, fc=W1, ec="black",
                             lw=0.7, ls="--", alpha=0.5))
    ax2.add_patch(Rectangle(((CHAIR_WIDTH - FRAME_W)*s2, SEAT_H*s2),
                             FRAME_W*s2, BACK_DZ*s2,
                             fc=W1, ec="black", lw=0.7, ls="--", alpha=0.5))
    # Assise (representation simplifiee)
    ax2.add_patch(Rectangle((0, (SEAT_H - SLAT_T)*s2),
                             CHAIR_WIDTH*s2, SLAT_T*s2,
                             fc=W2, ec="black", lw=1))
    # Dossier lattes
    for i in range(N_BACK_SLATS):
        frac = (i + 0.5) / N_BACK_SLATS
        bz = SEAT_H + frac * BACK_DZ
        ax2.add_patch(Rectangle((FRAME_W*s2, bz*s2),
                                INNER_WIDTH*s2, SLAT_W*s2,
                                fc=W3, ec="black", lw=0.5))
    # Traverse avant
    ax2.add_patch(Rectangle((FRAME_W*s2, (SEAT_H - SLAT_T - FRAME_W)*s2),
                             INNER_WIDTH*s2, SLAT_T*s2,
                             fc=W3, ec="black", lw=0.5))
    # Cotes
    _add_dim_h(ax2, 0, CHAIR_WIDTH*s2, TOTAL_H*s2,
               f"{CHAIR_WIDTH:.0f} mm", offset=8)
    _add_dim_v(ax2, CHAIR_WIDTH*s2, 0, TOTAL_H*s2,
               f"{TOTAL_H:.0f}", offset=12)

    ax2.set_xlim(-15, CHAIR_WIDTH*s2 + 40)
    ax2.set_ylim(-15, TOTAL_H*s2 + 25)
    ax2.grid(True, alpha=0.2)
    ax2.set_xlabel("mm"); ax2.set_ylabel("mm")

    # ===================== VUE DESSUS =====================
    ax3 = fig.add_axes([0.70, 0.38, 0.27, 0.52])
    ax3.set_title("Vue de dessus", fontsize=10)
    ax3.set_aspect("equal")

    s3 = 0.12
    # Longerons
    ax3.add_patch(Rectangle((0, 0), FRAME_W*s3, RUNNER_L*s3,
                             fc=W1, ec="black", lw=0.8))
    ax3.add_patch(Rectangle(((CHAIR_WIDTH - FRAME_W)*s3, 0),
                             FRAME_W*s3, RUNNER_L*s3,
                             fc=W1, ec="black", lw=0.8))
    # Lattes assise
    colors = [W2, W1, W3, W2, W1]
    for i in range(N_SEAT_SLATS):
        sy = i * (SLAT_W + SLAT_GAP)
        ax3.add_patch(Rectangle((0, sy*s3), CHAIR_WIDTH*s3, SLAT_W*s3,
                                fc=colors[i % len(colors)], ec="black", lw=0.4))
    # Cotes
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
    info = (
        "Objet : Deck Chair de Jardin en Palettes Recyclees\n"
        f"Dimensions : {CHAIR_WIDTH:.0f} x {RUNNER_L:.0f} x {TOTAL_H:.0f} mm "
        f"(L x P x H)  |  Assise : {SEAT_H:.0f} mm\n"
        f"Assise : {N_SEAT_SLATS} lattes de {SLAT_W:.0f} x {SLAT_T:.0f} mm  |  "
        f"Dossier : {N_BACK_SLATS} lattes, incline ~{90 + BACKREST_TILT:.0f} deg\n"
        f"Longerons : {RUNNER_L:.0f} mm (depassent de {RUNNER_EXTEND:.0f} mm "
        f"a l'arriere)  |  Pas d'accoudoirs (design minimaliste)\n"
        "Materiau : 1 euro-palette recyclee  |  17 pieces  |  Echelle : 1:1 (mm)\n"
        "Inspire de : instructables.com/A-Deck-Chair-Made-From-Pallet-Wood-Leftovers"
    )
    ax_info.text(0.5, 0.5, info, transform=ax_info.transAxes,
                 fontsize=8.5, va="center", ha="center",
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
