"""Guide de construction illustre - Deck Chair de jardin en palettes.

Structure palette : panneaux lateraux (planche + blocs + planche),
assise tres basse, dossier tres incline, sans accoudoirs.
"""
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from matplotlib.backends.backend_pdf import PdfPages

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(OUTPUT_DIR, "guide_construction.pdf")
WOOD1, WOOD2, WOOD3, WOOD4 = "#d2a679", "#c49a6c", "#b8956a", "#a0784e"

CHAIR_W = 600
SLAT_W = 95; SLAT_T = 22; SLAT_GAP = 15
PANEL_W = 95; BLOCK_H = 78; BLOCK_W = 44
PANEL_H = SLAT_T + BLOCK_H + SLAT_T  # 122
SEAT_H = PANEL_H + SLAT_T  # 144
N_SEAT = 4; N_BACK = 5
SEAT_DEPTH = N_SEAT * SLAT_W + (N_SEAT - 1) * SLAT_GAP  # 425
RUNNER_EXTEND = 350; RUNNER_L = SEAT_DEPTH + RUNNER_EXTEND
BACKREST_TILT = 35; BACK_LENGTH = 650
FRAME_W = 44; FRAME_D = 70
INNER_W = CHAIR_W - 2 * PANEL_W  # 410
BACK_DZ = BACK_LENGTH * math.cos(math.radians(BACKREST_TILT))
BACK_DY = BACK_LENGTH * math.sin(math.radians(BACKREST_TILT))
TOTAL_H = SEAT_H + BACK_DZ
BACK_SLATS_TOTAL = N_BACK * SLAT_W + (N_BACK - 1) * SLAT_GAP
BACK_SLAT_MARGIN = (BACK_LENGTH - BACK_SLATS_TOTAL) / 2

def new_page(pdf, title, subtitle=None):
    fig, ax = plt.subplots(figsize=(8.27, 11.69))
    ax.set_xlim(0, 100); ax.set_ylim(0, 140); ax.axis("off")
    ax.text(50, 133, title, ha="center", va="top", fontsize=16, fontweight="bold")
    if subtitle:
        ax.text(50, 128, subtitle, ha="center", va="top", fontsize=11, color="#555")
    return fig, ax

SUPPORT_BASE_Y = SEAT_DEPTH - SEAT_H * math.tan(math.radians(BACKREST_TILT))
SUPPORT_FULL_L = TOTAL_H / math.cos(math.radians(BACKREST_TILT))

def draw_side(ax, x0, y0, s=0.04):
    """Vue de cote avec panneaux palette et support dossier continu."""
    # Planche basse
    ax.add_patch(Rectangle((x0, y0), RUNNER_L*s, SLAT_T*s, fc=WOOD1, ec="black", lw=1))
    # Blocs
    for by in [30, SEAT_DEPTH/2, RUNNER_L-70]:
        ax.add_patch(Rectangle((x0+by*s, y0+SLAT_T*s), BLOCK_W*s, BLOCK_H*s, fc=WOOD4, ec="black", lw=0.6))
    # Planche haute
    ax.add_patch(Rectangle((x0, y0+(SLAT_T+BLOCK_H)*s), RUNNER_L*s, SLAT_T*s, fc=WOOD1, ec="black", lw=1))
    # Support dossier continu (du sol au sommet)
    base_y = SUPPORT_BASE_Y * s
    sup_dy = SUPPORT_FULL_L * math.sin(math.radians(BACKREST_TILT)) * s
    sup_dz = TOTAL_H * s
    pts = [
        [x0+base_y, y0],
        [x0+base_y+FRAME_D*s, y0],
        [x0+base_y+FRAME_D*s+sup_dy, y0+sup_dz],
        [x0+base_y+sup_dy, y0+sup_dz],
    ]
    ax.add_patch(Polygon(pts, closed=True, fc=WOOD1, ec="black", lw=1))
    # Assise
    ax.add_patch(Rectangle((x0, y0+PANEL_H*s), SEAT_DEPTH*s, SLAT_T*s, fc=WOOD2, ec="black", lw=0.8))
    # Lattes dossier (inclinées à 35 deg)
    _rad = math.radians(BACKREST_TILT)
    _sn, _cs = math.sin(_rad), math.cos(_rad)
    for i in range(N_BACK):
        along = BACK_SLAT_MARGIN + i * (SLAT_W + SLAT_GAP)
        frac = along / BACK_LENGTH
        by0 = SEAT_DEPTH + frac * BACK_DY
        bz0 = SEAT_H + frac * BACK_DZ
        pts = [
            [x0 + by0 * s,                                y0 + bz0 * s],
            [x0 + (by0 + SLAT_W * _sn) * s,               y0 + (bz0 + SLAT_W * _cs) * s],
            [x0 + (by0 + SLAT_W * _sn - SLAT_T * _cs) * s,
             y0 + (bz0 + SLAT_W * _cs + SLAT_T * _sn) * s],
            [x0 + (by0 - SLAT_T * _cs) * s,               y0 + (bz0 + SLAT_T * _sn) * s],
        ]
        ax.add_patch(Polygon(pts, closed=True, fc=WOOD3, ec="black", lw=0.5))

def draw_front(ax, x0, y0, s=0.04):
    """Vue de face simplifiee."""
    for px in [0, CHAIR_W - PANEL_W]:
        ax.add_patch(Rectangle((x0+px*s, y0), PANEL_W*s, SLAT_T*s, fc=WOOD1, ec="black", lw=0.8))
        bx = px + (PANEL_W-BLOCK_W)/2
        ax.add_patch(Rectangle((x0+bx*s, y0+SLAT_T*s), BLOCK_W*s, BLOCK_H*s, fc=WOOD4, ec="black", lw=0.6))
        ax.add_patch(Rectangle((x0+px*s, y0+(SLAT_T+BLOCK_H)*s), PANEL_W*s, SLAT_T*s, fc=WOOD1, ec="black", lw=0.8))
    ax.add_patch(Rectangle((x0, y0+PANEL_H*s), CHAIR_W*s, SLAT_T*s, fc=WOOD2, ec="black", lw=1))

def page_cover(pdf):
    fig, ax = new_page(pdf, "Guide de Construction", "Deck Chair de Jardin en Palettes Recyclees")
    ax.text(50, 123, "Design minimaliste - panneaux lateraux palette, sans accoudoirs", ha="center", fontsize=11, style="italic", color=WOOD4)
    draw_side(ax, 12, 60, 0.055)
    ax.text(50, 55, f"{CHAIR_W} x {RUNNER_L} x {TOTAL_H:.0f} mm  |  Assise {SEAT_H} mm  |  Dossier ~{90+BACKREST_TILT} deg", ha="center", fontsize=10, color="#333")
    ax.text(50, 50, "Adaptee a la table basse palette (450 mm)", ha="center", fontsize=10, color="#666")
    ax.text(50, 15, "Inspire de : instructables.com/A-Deck-Chair-Made-From-Pallet-Wood-Leftovers", ha="center", fontsize=8, color="#999")
    pdf.savefig(fig); plt.close(fig)

def page_materials(pdf):
    fig, ax = new_page(pdf, "Materiaux et Outillage")
    ax.text(50, 125, "1 euro-palette standard (1200 x 800 mm)", ha="center", fontsize=11)
    ax.add_patch(Rectangle((30, 105), 40, 12, fc="#f0dcc0", ec="black", lw=1))
    for i in range(5):
        ax.add_patch(Rectangle((31, 106.5+i*2), 38, 1.5, fc=WOOD1, ec="black", lw=0.4))
    ax.text(50, 102, "1 palette suffit (22 pieces)", ha="center", fontsize=8)
    ax.text(50, 96, "Choisir une palette marquee HT", ha="center", fontsize=9, color="green")
    tools = ["Pied-de-biche / levier", "Arrache-clou / tenaille", "Scie circulaire + guide",
             "Scie a onglet", "Ponceuse orbitale (80, 120, 180)", "Visseuse + vis 4x50 mm",
             "Serre-joints (x4)", "Colle a bois D3", "Fausse equerre (angle 125 deg)"]
    ax.text(50, 86, "Outillage :", ha="center", fontsize=12, fontweight="bold")
    for i, t in enumerate(tools):
        ax.text(20, 80 - i*4.5, f"  * {t}", fontsize=10)
    pdf.savefig(fig); plt.close(fig)

def page_dismantling(pdf):
    fig, ax = new_page(pdf, "Etape 1 : Demontage de la palette")
    ax.add_patch(Rectangle((15, 108), 70, 3, fc=WOOD3, ec="black", lw=0.8))
    for bx in [20, 47, 74]:
        ax.add_patch(Rectangle((bx, 111), 8, 8, fc=WOOD1, ec="black", lw=0.8))
    ax.add_patch(Rectangle((15, 119), 70, 3, fc=WOOD2, ec="black", lw=0.8))
    ax.annotate("", xy=(17, 122), xytext=(10, 112), arrowprops=dict(arrowstyle="->", color="red", lw=2))
    ax.text(7, 117, "Levier", fontsize=9, color="red", rotation=50)
    ax.text(50, 100, "Pieces a recuperer :", ha="center", fontsize=11, fontweight="bold")
    ax.text(15, 93, "- Lattes du dessus (pleine largeur 95 mm)", fontsize=9)
    ax.text(15, 88, "- Blocs de palette (78 mm de haut) pour les panneaux lateraux", fontsize=9, color=WOOD4, fontweight="bold")
    tips = ["- Levier doucement pour ne pas casser les lattes",
            "- Retirer tous les clous a la tenaille",
            "- Conserver les blocs de palette (important !)",
            "- Pas de refente : on garde la largeur 95 mm"]
    for i, t in enumerate(tips):
        ax.text(15, 75 - i*5, t, fontsize=9)
    pdf.savefig(fig); plt.close(fig)

def page_cutting(pdf):
    fig, ax = new_page(pdf, "Etape 2 : Debit des pieces")
    pieces = [
        ("A", f"Latte assise x{N_SEAT}", "600 x 95 x 22", WOOD2, 60),
        ("B", f"Latte dossier x{N_BACK}", f"{INNER_W} x 95 x 22", WOOD3, 41),
        ("C", f"Planche lat. basse x2", f"{RUNNER_L} x 95 x 22", WOOD1, 77),
        ("D", f"Planche lat. haute x2", f"{RUNNER_L} x 95 x 22", WOOD1, 77),
        ("E", "Bloc lateral x6", f"44 x 44 x {BLOCK_H}", WOOD4, 8),
        ("F", "Support dossier x2", f"{SUPPORT_FULL_L:.0f} x 70 x 44", WOOD1, 82),
        ("G", "Traverse avant x1", f"{INNER_W} x 44 x 22", WOOD3, 41),
    ]
    for i, (ref, name, dims, color, w) in enumerate(pieces):
        y = 118 - i * 11
        h = 3 if "Bloc" not in name and "Support" not in name else 5
        ax.add_patch(Rectangle((10, y), w*0.65, h, fc=color, ec="black", lw=0.6))
        ax.text(10 + w*0.65/2, y + h/2, ref, ha="center", va="center", fontsize=8, fontweight="bold", color="white")
        ax.text(58, y + h/2, f"{name}\n{dims} mm", va="center", fontsize=8)
    ax.text(50, 35, "Les lattes gardent leur pleine largeur (95 mm)", ha="center", fontsize=10, fontweight="bold", color=WOOD4)
    ax.text(50, 29, "Blocs : recuperes directement de la palette (78 mm)", ha="center", fontsize=9, color="#555")
    pdf.savefig(fig); plt.close(fig)

def page_panels(pdf):
    fig, ax = new_page(pdf, "Etape 3 : Panneaux lateraux")
    ax.text(50, 125, "Assembler 2 panneaux : planche basse + 3 blocs + planche haute", ha="center", fontsize=10, color="#666")
    s = 0.06
    x0 = 10; y0 = 75
    # Planche basse
    ax.add_patch(Rectangle((x0, y0), RUNNER_L*s, SLAT_T*s, fc=WOOD1, ec="black", lw=1.2))
    ax.text(x0+RUNNER_L*s/2, y0+SLAT_T*s/2, "C", ha="center", va="center", fontsize=9, fontweight="bold")
    # Blocs
    for by in [30, SEAT_DEPTH/2, RUNNER_L-70]:
        ax.add_patch(Rectangle((x0+by*s, y0+SLAT_T*s), BLOCK_W*s, BLOCK_H*s, fc=WOOD4, ec="black", lw=0.8))
    ax.text(x0+30*s+BLOCK_W*s/2, y0+(SLAT_T+BLOCK_H/2)*s, "E", ha="center", va="center", fontsize=8, fontweight="bold", color="white")
    # Planche haute
    ax.add_patch(Rectangle((x0, y0+(SLAT_T+BLOCK_H)*s), RUNNER_L*s, SLAT_T*s, fc=WOOD1, ec="black", lw=1.2))
    ax.text(x0+RUNNER_L*s/2, y0+(SLAT_T+BLOCK_H+SLAT_T/2)*s, "D", ha="center", va="center", fontsize=9, fontweight="bold")
    ax.text(50, y0-5, "Structure identique a une mini-palette  |  Repeter x2", ha="center", fontsize=10, fontweight="bold", color=WOOD4)
    ax.text(50, y0-12, "Vis 4x50 mm a travers les planches dans les blocs", ha="center", fontsize=9, color="#555")
    ax.text(50, y0-19, f"Hauteur panneau : {PANEL_H} mm  |  Longueur : {RUNNER_L} mm", ha="center", fontsize=9)
    pdf.savefig(fig); plt.close(fig)

def page_seat(pdf):
    fig, ax = new_page(pdf, "Etape 4 : Pose de l'assise")
    ax.text(50, 125, f"Visser les {N_SEAT} lattes (A) sur les panneaux lateraux", ha="center", fontsize=10, color="#666")
    s = 0.055
    colors = [WOOD2, WOOD1, WOOD3, WOOD2]
    for i in range(N_SEAT):
        sy = i * (SLAT_W + SLAT_GAP)
        ax.add_patch(Rectangle((15, 85+sy*s), CHAIR_W*s, SLAT_W*s, fc=colors[i], ec="black", lw=0.6))
        if i == 0:
            ax.text(15+CHAIR_W*s/2, 85+sy*s+SLAT_W*s/2, "A", ha="center", va="center", fontsize=10, fontweight="bold")
    ax.text(50, 80, f"Vue de dessus - {N_SEAT} lattes de 600 x 95 mm", ha="center", fontsize=9, color="#666")
    # Gap
    ax.add_patch(Rectangle((30, 62), 18, 6, fc=WOOD2, ec="black", lw=0.8))
    ax.add_patch(Rectangle((30, 72), 18, 6, fc=WOOD1, ec="black", lw=0.8))
    ax.annotate("", xy=(50, 72), xytext=(50, 68), arrowprops=dict(arrowstyle="<->", color="red", lw=1))
    ax.text(53, 69, f"{SLAT_GAP:.0f} mm", fontsize=9, color="red", fontweight="bold")
    ax.text(50, 52, f"Cale de {SLAT_GAP:.0f} mm entre chaque latte  |  2 vis par cote", ha="center", fontsize=10)
    ax.text(50, 45, f"Hauteur d'assise : seulement {SEAT_H} mm !", ha="center", fontsize=10, fontweight="bold", color=WOOD4)
    pdf.savefig(fig); plt.close(fig)

def page_angle_prep(pdf):
    """Page detaillant la preparation de l'angle a 35 deg."""
    fig, ax = new_page(pdf, "Etape 4b : Preparation de l'angle",
                       "Tracer et couper l'angle du dossier")
    # Schema de l'angle
    x0, y0 = 20, 85
    s = 0.08
    # Sol
    ax.plot([x0, x0 + 80], [y0, y0], "k-", lw=1.5)
    # Support vertical (reference)
    ax.plot([x0 + 40, x0 + 40], [y0, y0 + 40], "k--", lw=0.8, alpha=0.5)
    ax.text(x0 + 42, y0 + 38, "verticale", fontsize=7, color="#999")
    # Support incline
    length = 45
    rad = math.radians(BACKREST_TILT)
    dx = length * math.sin(rad)
    dy = length * math.cos(rad)
    ax.plot([x0 + 40, x0 + 40 + dx], [y0, y0 + dy], color=WOOD4, lw=3)
    ax.text(x0 + 40 + dx + 2, y0 + dy, "F", fontsize=10,
            fontweight="bold", color=WOOD4)
    # Arc pour l'angle
    import matplotlib.patches as mpatches
    arc = mpatches.Arc((x0 + 40, y0), 20, 20, angle=90,
                       theta1=0, theta2=BACKREST_TILT,
                       color="red", lw=1.5)
    ax.add_patch(arc)
    ax.text(x0 + 44, y0 + 12, f"{BACKREST_TILT} deg", fontsize=10,
            color="red", fontweight="bold")
    # Arc pour l'angle avec l'assise
    arc2 = mpatches.Arc((x0 + 40, y0), 30, 30, angle=0,
                        theta1=90 - BACKREST_TILT, theta2=90,
                        color="blue", lw=1)
    ax.add_patch(arc2)

    steps = [
        "1. Regler la fausse equerre a 35 deg par rapport a la verticale",
        f"   (= {90 + BACKREST_TILT} deg par rapport a l'horizontale de l'assise)",
        "",
        "2. Reporter l'angle sur les 2 supports dossier (F)",
        f"   Longueur totale du support : {SUPPORT_FULL_L:.0f} mm",
        "",
        "3. Couper le pied du support en biseau a 35 deg",
        "   pour qu'il repose a plat au sol",
        "",
        "4. Couper le sommet du support en biseau inverse",
        "   pour que le haut soit horizontal",
        "",
        "5. Verifier les 2 supports ensemble :",
        "   - Meme longueur a +/- 2 mm",
        "   - Memes angles de coupe",
        "   - Poser cote a cote pour comparer",
    ]
    for i, line in enumerate(steps):
        ax.text(10, 72 - i * 3.5, line, fontsize=9,
                color="#333" if not line.startswith("   ") else "#555")
    ax.text(50, 15, "ASTUCE : tracer sur un panneau de MDF un gabarit grandeur nature",
            ha="center", fontsize=9, fontweight="bold", color=WOOD4)
    pdf.savefig(fig); plt.close(fig)

def page_back_supports(pdf):
    fig, ax = new_page(pdf, "Etape 5 : Supports dossier")
    ax.text(50, 125, "Fixer les 2 supports dossier (F) - continus du sol au sommet",
            ha="center", fontsize=10, color="#666")
    draw_side(ax, 10, 65, 0.055)
    ax.annotate(f"Support dossier (F)\n{SUPPORT_FULL_L:.0f} x 70 x 44 mm\nAngle ~{BACKREST_TILT} deg",
                xy=(55, 95), fontsize=9, color=WOOD4, fontweight="bold")

    # Instructions detaillees
    steps = [
        "Assemblage du support :",
        "  1. Coller 2 lattes face a face (section 44 x 70 mm)",
        "     Serrer avec 4 serre-joints, laisser secher 24h",
        "",
        "Fixation au panneau lateral :",
        f"  2. Positionner le support contre le panneau a Y = {SUPPORT_BASE_Y:.0f} mm",
        "     Le pied du support repose au sol, le haut depasse",
        f"  3. Verifier l'angle a {BACKREST_TILT} deg avec la fausse equerre",
        "  4. Percer 2 trous de 8 mm a travers panneau + support",
        "     - Trou bas : ~60 mm au-dessus du sol",
        f"     - Trou haut : ~{PANEL_H - 20} mm (sous la planche haute)",
        "  5. Boulonner avec M8 x 100 mm + rondelles + ecrous",
        "",
        "Repeter pour le 2e cote (symetrique).",
        "Verifier que les 2 supports sont paralleles.",
    ]
    for i, line in enumerate(steps):
        y = 58 - i * 3.2
        bold = not line.startswith(" ") and line.endswith(":")
        ax.text(10, y, line, fontsize=8,
                fontweight="bold" if bold else "normal",
                color=WOOD4 if bold else "#333")
    pdf.savefig(fig); plt.close(fig)

def page_backrest(pdf):
    fig, ax = new_page(pdf, "Etape 6 : Pose du dossier")
    ax.text(50, 125, f"Visser les {N_BACK} lattes (B) sur les supports", ha="center", fontsize=10, color="#666")
    # Vue arriere (X-Z) avec hauteur projetee des lattes
    s = 0.04
    x0 = 15; y0 = 60
    slat_proj_h = SLAT_W * math.cos(math.radians(BACKREST_TILT))
    for px in [0, CHAIR_W - PANEL_W]:
        bx = px + (PANEL_W - FRAME_W) / 2
        ax.add_patch(Rectangle((x0 + bx * s, y0 + SEAT_H * s),
                                FRAME_W * s, BACK_DZ * s,
                                fc=WOOD1, ec="black", lw=1))
    for i in range(N_BACK):
        along = BACK_SLAT_MARGIN + i * (SLAT_W + SLAT_GAP)
        frac = along / BACK_LENGTH
        bz = SEAT_H + frac * BACK_DZ
        ax.add_patch(Rectangle((x0 + PANEL_W * s, y0 + bz * s),
                                INNER_W * s, slat_proj_h * s,
                                fc=WOOD3, ec="black", lw=0.7))
        if i == 0:
            ax.text(x0 + CHAIR_W * s / 2,
                    y0 + (bz + slat_proj_h / 2) * s,
                    "B", ha="center", va="center", fontsize=10,
                    fontweight="bold", color="white")
    ax.text(50, y0 - 3, f"Vue arriere - {N_BACK} lattes de {INNER_W} x 95 mm",
            ha="center", fontsize=9, color="#666")
    ax.text(50, y0 - 9, f"2 vis par latte et par support = {N_BACK * 4} vis",
            ha="center", fontsize=10, fontweight="bold")
    # Instructions detaillees
    tips = [
        f"- Commencer par la latte du bas, {BACK_SLAT_MARGIN:.0f} mm au-dessus de l'assise (le long du support)",
        f"- Espacement de {SLAT_GAP} mm entre chaque latte (utiliser une cale)",
        "- Pre-percer les lattes pour eviter de fendre le bois",
        "- Vis 4x50 mm, 2 par cote, a ~20 mm des bords de la latte",
        "- Verifier l'equerrage avec une equerre avant de serrer",
    ]
    for i, tip in enumerate(tips):
        ax.text(10, y0 - 16 - i * 5, tip, fontsize=8, color="#333")
    pdf.savefig(fig); plt.close(fig)

def page_verification(pdf):
    """Page de verification avant finition."""
    fig, ax = new_page(pdf, "Etape 7 : Verification",
                       "Controles avant finition")
    checks = [
        ("Stabilite", [
            "Poser la chaise sur une surface plane",
            "Verifier qu'elle ne bascule pas (4 points d'appui au sol)",
            "S'asseoir doucement pour tester la solidite",
        ]),
        ("Angle du dossier", [
            f"Verifier l'angle de {90 + BACKREST_TILT} deg entre assise et dossier",
            "Utiliser la fausse equerre pour controler",
            "Le dossier doit etre confortable en position allongee",
        ]),
        ("Alignement des lattes", [
            "Les lattes d'assise doivent etre paralleles entre elles",
            f"Espacement regulier de {SLAT_GAP} mm entre les lattes",
            "Les lattes de dossier suivent l'inclinaison du support",
        ]),
        ("Fixations", [
            "Toutes les vis doivent etre serrees et affleurantes",
            "Les boulons M8 des supports doivent etre bien bloques",
            "Aucun jeu dans les assemblages",
        ]),
        ("Securite", [
            "Pas d'eclats ni d'aretes vives (poncer si necessaire)",
            "Pas de clous ou vis qui depassent",
            "Verifier la solidite des panneaux lateraux",
        ]),
    ]
    y = 120
    for title, items in checks:
        ax.add_patch(Rectangle((8, y - 1), 84, 4 + len(items) * 3.5,
                                fc="#faf5ef", ec=WOOD4, lw=0.8))
        ax.text(12, y + len(items) * 3.5 - 0.5, title,
                fontsize=10, fontweight="bold", color=WOOD4)
        for j, item in enumerate(items):
            ax.text(14, y + (len(items) - 1 - j) * 3.5 - 0.5,
                    f"[ ]  {item}", fontsize=8, color="#333")
        y -= 5 + len(items) * 3.5

    ax.text(50, 15, "Si tout est OK, passer a la finition !",
            ha="center", fontsize=11, fontweight="bold", color="green")
    pdf.savefig(fig); plt.close(fig)

def page_finishing(pdf):
    fig, ax = new_page(pdf, "Etape 8 : Finition")
    ax.text(50, 125, "Proteger et embellir votre deck chair", ha="center", fontsize=11, color="#666")
    draw_front(ax, 25, 90, 0.04)
    options = [
        ("Huile de lin", "#c8a050", ["Aspect naturel", "2-3 couches", "Interieur"]),
        ("Vernis", "#e0c080", ["Protection max", "Surface lisse", "Anti-taches"]),
        ("Lasure", "#a07840", ["Exterieur", "UV + intemperies", "2-3 ans"]),
    ]
    for i, (name, color, details) in enumerate(options):
        x = 8 + i * 30
        ax.add_patch(Rectangle((x, 50), 26, 25, fc="#faf5ef", ec=color, lw=2))
        ax.add_patch(Rectangle((x, 69), 26, 6, fc=color, ec=color, lw=1))
        ax.text(x+13, 72, name, ha="center", va="center", fontsize=9, fontweight="bold", color="white")
        for j, d in enumerate(details):
            ax.text(x+2, 64 - j*4.5, f"- {d}", fontsize=8)
    pdf.savefig(fig); plt.close(fig)

def page_final(pdf):
    fig, ax = new_page(pdf, "Resultat Final")
    ax.text(50, 125, "Votre deck chair en palettes est terminee !", ha="center", fontsize=11, color=WOOD4)
    draw_side(ax, 5, 80, 0.045)
    ax.text(25, 77, "Vue de cote", ha="center", fontsize=8, color="#666")
    draw_front(ax, 55, 80, 0.035)
    ax.text(68, 77, "Vue de face", ha="center", fontsize=8, color="#666")
    summary = [
        "Materiau : 1 euro-palette recyclee (marquage HT)",
        f"Dimensions : {CHAIR_W} x {RUNNER_L} x {TOTAL_H:.0f} mm",
        f"Hauteur assise : {SEAT_H} mm seulement !",
        f"Angle dossier : ~{90+BACKREST_TILT} deg (tres detendu)",
        "Panneaux lateraux style palette (blocs 78 mm)",
        "Sans accoudoirs (design minimaliste)",
        f"Longerons depassent de {RUNNER_EXTEND} mm a l'arriere",
        "22 pieces au total",
    ]
    for i, line in enumerate(summary):
        ax.text(15, 68 - i*5, f"  {line}", fontsize=9)
    ax.text(50, 20, "Inspire de : instructables.com/A-Deck-Chair-Made-From-Pallet-Wood-Leftovers", ha="center", fontsize=8, color="#999")
    pdf.savefig(fig); plt.close(fig)

def generate_guide():
    with PdfPages(PDF_PATH) as pdf:
        page_cover(pdf)
        page_materials(pdf)
        page_dismantling(pdf)
        page_cutting(pdf)
        page_panels(pdf)
        page_seat(pdf)
        page_angle_prep(pdf)
        page_back_supports(pdf)
        page_backrest(pdf)
        page_verification(pdf)
        page_finishing(pdf)
        page_final(pdf)
    print(f"Guide PDF genere : {PDF_PATH} ({os.path.getsize(PDF_PATH) // 1024} Ko)")

if __name__ == "__main__":
    generate_guide()
