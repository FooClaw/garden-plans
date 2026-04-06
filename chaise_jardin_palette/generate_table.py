"""
Deck chair de jardin en palettes recyclees - Modele 3D

Inspire du projet Instructables "A Deck Chair Made From Pallet Wood
Leftovers" par Well Done Tips.

Structure type palette : panneaux lateraux, assise tres basse,
dossier inclinable (3 positions, mecanisme cremaillere type chaise
de plage), sans accoudoirs, longerons depassant a l'arriere.

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
from matplotlib.patches import Rectangle, Polygon, Arc, Circle
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
BACK_DZ = BACK_LENGTH * math.cos(math.radians(BACKREST_TILT))
BACK_DY = BACK_LENGTH * math.sin(math.radians(BACKREST_TILT))

# --- Mecanisme d'inclinaison (type chaise de plage) ---
BACKREST_ANGLES = [25.0, 35.0, 50.0]  # 3 crans (assis / detendu / allonge)
PIVOT_Y = SEAT_DEPTH                   # pivot au bord arriere de l'assise
PIVOT_Z = SLAT_T + BLOCK_H / 2         # pivot ENTRE les planches laterales (61 mm)

TOTAL_H = PIVOT_Z + BACK_DZ            # hauteur totale (position par defaut)

# Distance le long du support entre le pivot et le niveau de l'assise
DIST_TO_SEAT = (SEAT_H - PIVOT_Z) / math.cos(math.radians(BACKREST_TILT))

# Support dossier (F) - pivotant
SUPPORT_BELOW = 50.0                                   # extension sous le pivot
SUPPORT_PIVOT_L = BACK_LENGTH + SUPPORT_BELOW           # longueur totale support

# Barre stabilisatrice (I) - du haut du dossier a la cremaillere
STRUT_ATTACH = 400.0         # point d'attache sur le support (depuis le pivot)
STRUT_L = 380.0              # longueur de la barre stabilisatrice
STRUT_SECTION = SLAT_T       # section 22 mm

# Cremaillere (H) - support crante a l'INTERIEUR des panneaux
# Monte entre les planches laterales, sur la planche basse
CREM_W = SLAT_T              # 22 mm (epaisseur en X)
CREM_HEIGHT = 40.0           # hauteur (Z)
CREM_BASE_Z = SLAT_T         # pose sur la planche basse du panneau
CREM_TOP_Z = CREM_BASE_Z + CREM_HEIGHT   # sommet de la cremaillere (62 mm)

# Positions des encoches sur la cremaillere pour chaque angle
# Le pied de la barre stab. repose sur le sommet de la cremaillere
_NOTCH_POSITIONS = []
for _a in BACKREST_ANGLES:
    _r = math.radians(_a)
    _yt = PIVOT_Y + STRUT_ATTACH * math.sin(_r)
    _zt = PIVOT_Z + STRUT_ATTACH * math.cos(_r)
    _zd = _zt - CREM_TOP_Z
    _yd = math.sqrt(STRUT_L**2 - _zd**2)
    _NOTCH_POSITIONS.append(_yt - _yd)
CREM_Y_START = min(_NOTCH_POSITIONS) - STRUT_SECTION
CREM_L = max(_NOTCH_POSITIONS) - CREM_Y_START + 2 * STRUT_SECTION

# Geometrie de la barre stab. a l'angle par defaut (pour STL)
_dr = math.radians(BACKREST_TILT)
_syt = PIVOT_Y + STRUT_ATTACH * math.sin(_dr)
_szt = PIVOT_Z + STRUT_ATTACH * math.cos(_dr)
_szd = _szt - CREM_TOP_Z
_syd = math.sqrt(STRUT_L**2 - _szd**2)
STRUT_Y_BOT = _syt - _syd                                # pied sur la cremaillere
STRUT_TILT = math.degrees(math.atan2(_syd, _szd))        # inclinaison

# Espacement des lattes de dossier (uniquement au-dessus de l'assise)
BACK_SLATS_TOTAL = N_BACK_SLATS * SLAT_W + (N_BACK_SLATS - 1) * SLAT_GAP
BACK_VISIBLE = BACK_LENGTH - DIST_TO_SEAT    # portion visible au-dessus de l'assise
BACK_SLAT_MARGIN = (BACK_VISIBLE - BACK_SLATS_TOTAL) / 2
BACK_SLAT_START = DIST_TO_SEAT + BACK_SLAT_MARGIN  # debut 1ere latte depuis le pivot


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


def _backrest_slat_faces(x, y, z, width, slat_w, slat_t, tilt_deg):
    """Latte de dossier inclinee a l'angle du dossier.

    La face arriere est contre le support, la face avant pointe vers
    l'assise.  *slat_w* court le long du dossier, *slat_t* est
    l'epaisseur perpendiculaire a la surface du dossier.
    """
    rad = math.radians(tilt_deg)
    sn, cs = math.sin(rad), math.cos(rad)
    # Vecteur le long du dossier (monte et recule)
    dyw = slat_w * sn
    dzw = slat_w * cs
    # Vecteur perpendiculaire (vers l'assise / le devant)
    dyt = -slat_t * cs
    dzt = slat_t * sn
    v = np.array([
        # Face arriere (sur le support)
        [x,       y,           z],
        [x+width, y,           z],
        [x+width, y+dyw,       z+dzw],
        [x,       y+dyw,       z+dzw],
        # Face avant (vers l'assise)
        [x,       y+dyt,       z+dzt],
        [x+width, y+dyt,       z+dzt],
        [x+width, y+dyw+dyt,   z+dzw+dzt],
        [x,       y+dyw+dyt,   z+dzw+dzt],
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

    # === SUPPORTS DOSSIER (x2) - pivotants, a l'interieur des panneaux ===
    _tilt_rad = math.radians(BACKREST_TILT)
    sup_base_y = PIVOT_Y - SUPPORT_BELOW * math.sin(_tilt_rad)
    sup_base_z = PIVOT_Z - SUPPORT_BELOW * math.cos(_tilt_rad)
    for bx in [PANEL_W, CHAIR_WIDTH - PANEL_W - FRAME_W]:
        all_faces.extend(_tilted_box_faces(
            bx, sup_base_y, sup_base_z,
            FRAME_W, FRAME_D, SUPPORT_PIVOT_L, BACKREST_TILT))

    # === CREMAILLERES (x2) - entre les planches laterales ===
    for cx in [PANEL_W, CHAIR_WIDTH - PANEL_W - CREM_W]:
        all_faces.extend(_box_faces(cx, CREM_Y_START, CREM_BASE_Z,
                                    CREM_W, CREM_L, CREM_HEIGHT))

    # === BARRES STABILISATRICES (x2) - du dossier a la cremaillere ===
    for bx in [PANEL_W, CHAIR_WIDTH - PANEL_W - STRUT_SECTION]:
        all_faces.extend(_tilted_box_faces(
            bx, STRUT_Y_BOT, CREM_TOP_Z,
            STRUT_SECTION, STRUT_SECTION, STRUT_L, STRUT_TILT))

    # === LATTES DE DOSSIER (x5) - inclinées à 35°, au-dessus de l'assise ===
    back_start_x = PANEL_W
    back_slat_w = INNER_WIDTH
    for i in range(N_BACK_SLATS):
        along = BACK_SLAT_START + i * (SLAT_W + SLAT_GAP)
        frac = along / BACK_LENGTH
        bz = PIVOT_Z + frac * BACK_DZ
        by = PIVOT_Y + frac * BACK_DY
        all_faces.extend(_backrest_slat_faces(
            back_start_x, by, bz,
            back_slat_w, SLAT_W, SLAT_T, BACKREST_TILT))

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

    # --- Mecanisme d'inclinaison ---
    _rad = math.radians(BACKREST_TILT)
    _sn, _cs = math.sin(_rad), math.cos(_rad)
    pys, pzs = PIVOT_Y * s, PIVOT_Z * s

    # Cremaillere (H) entre les planches laterales
    ax1.add_patch(Rectangle((CREM_Y_START * s, CREM_BASE_Z * s),
                             CREM_L * s, CREM_HEIGHT * s,
                             fc="#e8c88a", ec="black", lw=1))
    ax1.text((CREM_Y_START + CREM_L / 2) * s,
             (PANEL_H + CREM_HEIGHT / 2) * s, "H",
             ha="center", va="center", fontsize=7, fontweight="bold")

    # Positions alternatives du dossier + barre stab. (fantomes)
    for angle in BACKREST_ANGLES:
        ar = math.radians(angle)
        asn, acs = math.sin(ar), math.cos(ar)
        sb_y = PIVOT_Y - SUPPORT_BELOW * asn
        sb_z = PIVOT_Z - SUPPORT_BELOW * acs
        st_y = PIVOT_Y + BACK_LENGTH * asn
        st_z = PIVOT_Z + BACK_LENGTH * acs
        # Point d'attache de la barre stab.
        att_y = PIVOT_Y + STRUT_ATTACH * asn
        att_z = PIVOT_Z + STRUT_ATTACH * acs
        zd = att_z - CREM_TOP_Z
        yd = math.sqrt(max(0, STRUT_L**2 - zd**2))
        ybot = att_y - yd
        is_default = (angle == BACKREST_TILT)
        if not is_default:
            # Support fantome
            pts = [
                [sb_y * s, sb_z * s],
                [(sb_y + FRAME_D * asn) * s, (sb_z + FRAME_D * acs) * s],
                [(st_y + FRAME_D * asn) * s, (st_z + FRAME_D * acs) * s],
                [st_y * s, st_z * s],
            ]
            ax1.add_patch(Polygon(pts, closed=True, fc="none", ec="#999",
                                   lw=0.7, ls="--", alpha=0.5))
            ax1.text(st_y * s + 3, st_z * s,
                     f"{angle:.0f}deg", fontsize=6, color="#999")
        # Barre stab. fantome (toutes positions)
        clr = "black" if is_default else "#999"
        lw = 1.5 if is_default else 0.7
        ls = "-" if is_default else "--"
        ax1.plot([ybot * s, att_y * s], [CREM_TOP_Z * s, att_z * s],
                 color=clr, lw=lw, ls=ls, alpha=0.8 if is_default else 0.5)
        if is_default:
            ax1.text((ybot + att_y) / 2 * s - 8,
                     (PIVOT_Z + att_z) / 2 * s,
                     "I", fontsize=7, fontweight="bold", color="#c06030")

    # Support dossier (position par defaut, plein)
    sb_y = PIVOT_Y - SUPPORT_BELOW * _sn
    sb_z = PIVOT_Z - SUPPORT_BELOW * _cs
    st_y = PIVOT_Y + BACK_LENGTH * _sn
    st_z = PIVOT_Z + BACK_LENGTH * _cs
    back_pts = [
        [sb_y * s, sb_z * s],
        [(sb_y + FRAME_D * _sn) * s, (sb_z + FRAME_D * _cs) * s],
        [(st_y + FRAME_D * _sn) * s, (st_z + FRAME_D * _cs) * s],
        [st_y * s, st_z * s],
    ]
    ax1.add_patch(Polygon(back_pts, closed=True, fc=W1, ec="black", lw=1.2))

    # Pivot (cercle)
    ax1.add_patch(Circle((pys, pzs), 4 * s, fc="white", ec="red",
                          lw=1.5, zorder=5))

    # Lattes dossier (inclinées)
    for i in range(N_BACK_SLATS):
        along = BACK_SLAT_START + i * (SLAT_W + SLAT_GAP)
        frac = along / BACK_LENGTH
        by0 = PIVOT_Y + frac * BACK_DY
        bz0 = PIVOT_Z + frac * BACK_DZ
        pts = [
            [by0 * s,                              bz0 * s],
            [(by0 + SLAT_W * _sn) * s,             (bz0 + SLAT_W * _cs) * s],
            [(by0 + SLAT_W * _sn - SLAT_T * _cs) * s,
             (bz0 + SLAT_W * _cs + SLAT_T * _sn) * s],
            [(by0 - SLAT_T * _cs) * s,             (bz0 + SLAT_T * _sn) * s],
        ]
        ax1.add_patch(Polygon(pts, closed=True, fc=W3, ec="black", lw=0.6))

    _add_dim_h(ax1, 0, RUNNER_L*s, TOTAL_H*s, f"{RUNNER_L:.0f} mm", offset=8)
    _add_dim_v(ax1, -5, 0, SEAT_H*s, f"{SEAT_H:.0f}", offset=-18)
    _add_dim_v(ax1, RUNNER_L*s, 0, TOTAL_H*s, f"{TOTAL_H:.0f}", offset=12)
    ax1.text(pys + 10 * s, pzs - 10 * s,
             "3 positions\n25/35/50 deg", fontsize=6, color="red",
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

    # Supports dossier pivotants (a l'interieur des panneaux)
    sup_bot_z = PIVOT_Z - SUPPORT_BELOW * math.cos(math.radians(BACKREST_TILT))
    for bx in [PANEL_W, CHAIR_WIDTH - PANEL_W - FRAME_W]:
        ax2.add_patch(Rectangle((bx*s2, sup_bot_z*s2),
                                 FRAME_W*s2, (TOTAL_H - sup_bot_z)*s2,
                                 fc=W1, ec="black", lw=0.6, ls="--", alpha=0.5))

    # Cremailleres (entre les planches laterales)
    for cx in [PANEL_W, CHAIR_WIDTH - PANEL_W - CREM_W]:
        ax2.add_patch(Rectangle((cx * s2, CREM_BASE_Z * s2),
                                 CREM_W * s2, CREM_HEIGHT * s2,
                                 fc="#e8c88a", ec="black", lw=0.8))

    # Barres stabilisatrices (entre dossier et cremaillere)
    strut_z_top = PIVOT_Z + STRUT_ATTACH * math.cos(math.radians(BACKREST_TILT))
    for bx in [PANEL_W, CHAIR_WIDTH - PANEL_W - STRUT_SECTION]:
        ax2.add_patch(Rectangle((bx * s2, PIVOT_Z * s2),
                                 STRUT_SECTION * s2,
                                 (strut_z_top - PIVOT_Z) * s2,
                                 fc="#c06030", ec="black", lw=0.5,
                                 ls="--", alpha=0.4))

    # Dossier lattes (hauteur projetee)
    slat_proj_h = SLAT_W * math.cos(math.radians(BACKREST_TILT))
    for i in range(N_BACK_SLATS):
        along = BACK_SLAT_START + i * (SLAT_W + SLAT_GAP)
        frac = along / BACK_LENGTH
        bz = PIVOT_Z + frac * BACK_DZ
        ax2.add_patch(Rectangle((PANEL_W*s2, bz*s2),
                                INNER_WIDTH*s2, slat_proj_h*s2,
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
    # A+B+C+D+E+F+G + H(crem x2) + I(barre stab x2)
    n_pieces = N_SEAT_SLATS + N_BACK_SLATS + 4 + 6 + 2 + 1 + 2 + 2
    angles_str = "/".join(f"{a:.0f}" for a in BACKREST_ANGLES)
    info = (
        "Objet : Deck Chair de Jardin en Palettes Recyclees\n"
        f"Dimensions : {CHAIR_WIDTH:.0f} x {RUNNER_L:.0f} x {TOTAL_H:.0f} mm "
        f"(L x P x H)  |  Assise : {SEAT_H:.0f} mm\n"
        f"Assise : {N_SEAT_SLATS} lattes  |  "
        f"Dossier : {N_BACK_SLATS} lattes, inclinable 3 positions "
        f"({angles_str} deg)\n"
        f"Mecanisme cremaillere : pivot + 2 barres stabilisatrices + "
        f"2 supports crantes internes\n"
        f"Panneaux lateraux style palette (planche + blocs "
        f"{BLOCK_H:.0f} mm + planche)\n"
        f"Sans accoudoirs  |  Longerons depassent de "
        f"{RUNNER_EXTEND:.0f} mm a l'arriere\n"
        f"Materiau : 1 euro-palette  |  {n_pieces} pieces  |  "
        f"Echelle 1:1 (mm)\n"
        "Inspire de : instructables.com/A-Deck-Chair-Made-From-"
        "Pallet-Wood-Leftovers"
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
