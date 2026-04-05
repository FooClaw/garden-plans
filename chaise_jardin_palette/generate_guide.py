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

def new_page(pdf, title, subtitle=None):
    fig, ax = plt.subplots(figsize=(8.27, 11.69))
    ax.set_xlim(0, 100); ax.set_ylim(0, 140); ax.axis("off")
    ax.text(50, 133, title, ha="center", va="top", fontsize=16, fontweight="bold")
    if subtitle:
        ax.text(50, 128, subtitle, ha="center", va="top", fontsize=11, color="#555")
    return fig, ax

def draw_side(ax, x0, y0, s=0.04):
    """Vue de cote avec panneaux palette et montants d'ancrage."""
    # Planche basse
    ax.add_patch(Rectangle((x0, y0), RUNNER_L*s, SLAT_T*s, fc=WOOD1, ec="black", lw=1))
    # Blocs
    for by in [30, SEAT_DEPTH/2, RUNNER_L-70]:
        ax.add_patch(Rectangle((x0+by*s, y0+SLAT_T*s), BLOCK_W*s, BLOCK_H*s, fc=WOOD4, ec="black", lw=0.6))
    # Planche haute
    ax.add_patch(Rectangle((x0, y0+(SLAT_T+BLOCK_H)*s), RUNNER_L*s, SLAT_T*s, fc=WOOD1, ec="black", lw=1))
    # Montant d'ancrage dossier (vertical, du sol a l'assise)
    ax.add_patch(Rectangle((x0+SEAT_DEPTH*s, y0), FRAME_D*s, SEAT_H*s, fc=WOOD4, ec="black", lw=0.8))
    # Assise
    ax.add_patch(Rectangle((x0, y0+PANEL_H*s), SEAT_DEPTH*s, SLAT_T*s, fc=WOOD2, ec="black", lw=0.8))
    # Support dossier (incline, sur le montant)
    seat_top = SEAT_H * s
    pts = [
        [x0+SEAT_DEPTH*s, y0+seat_top],
        [x0+SEAT_DEPTH*s+FRAME_D*s, y0+seat_top],
        [x0+SEAT_DEPTH*s+FRAME_D*s+BACK_DY*s, y0+seat_top+BACK_DZ*s],
        [x0+SEAT_DEPTH*s+BACK_DY*s, y0+seat_top+BACK_DZ*s],
    ]
    ax.add_patch(Polygon(pts, closed=True, fc=WOOD1, ec="black", lw=1))
    # Lattes dossier
    for i in range(N_BACK):
        frac = (i + 0.5) / N_BACK
        bz = PANEL_H + SLAT_T + frac * BACK_DZ
        by = SEAT_DEPTH + frac * BACK_DY
        ax.add_patch(Rectangle((x0+by*s, y0+bz*s), SLAT_T*s, SLAT_W*s, fc=WOOD3, ec="black", lw=0.5))

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
    ax.text(50, 102, "1 palette suffit (24 pieces)", ha="center", fontsize=8)
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
        ("F", "Support dossier x2", f"650 x 70 x 44", WOOD1, 65),
        ("G", "Traverse avant x1", f"{INNER_W} x 44 x 22", WOOD3, 41),
        ("H", "Montant ancrage x2", f"{SEAT_H} x 70 x 44", WOOD4, 14),
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

def page_anchors(pdf):
    fig, ax = new_page(pdf, "Etape 5 : Montants d'ancrage dossier")
    ax.text(50, 125, "Boulonner les 2 montants (H) a travers les panneaux lateraux", ha="center", fontsize=10, color="#666")
    s = 0.055
    x0 = 10; y0 = 75
    # Panneau lateral (simplifie)
    ax.add_patch(Rectangle((x0, y0), RUNNER_L*s, SLAT_T*s, fc=WOOD1, ec="black", lw=1))
    ax.add_patch(Rectangle((x0, y0+(SLAT_T+BLOCK_H)*s), RUNNER_L*s, SLAT_T*s, fc=WOOD1, ec="black", lw=1))
    # Montant d'ancrage (mis en evidence)
    ax.add_patch(Rectangle((x0+SEAT_DEPTH*s, y0), FRAME_D*s, SEAT_H*s, fc=WOOD4, ec="red", lw=2.5))
    ax.text(x0+SEAT_DEPTH*s+FRAME_D*s/2, y0+SEAT_H*s/2, "H", ha="center", va="center", fontsize=12, fontweight="bold", color="white")
    ax.annotate("Montant H\n144 x 70 x 44 mm\nBoulonne au panneau", xy=(x0+SEAT_DEPTH*s+FRAME_D*s+2, y0+SEAT_H*s/2), fontsize=9, color="red", fontweight="bold")
    ax.text(50, y0-8, "Le montant va du sol au niveau de l'assise", ha="center", fontsize=10, fontweight="bold", color=WOOD4)
    ax.text(50, y0-14, "Boulons M8 traversant panneau + montant (2 par cote)", ha="center", fontsize=9, color="#555")
    ax.text(50, y0-20, "Ancrage solide pour supporter le poids du dossier", ha="center", fontsize=9, color="#555")
    pdf.savefig(fig); plt.close(fig)

def page_back_supports(pdf):
    fig, ax = new_page(pdf, "Etape 6 : Supports dossier")
    ax.text(50, 125, "Fixer les 2 supports dossier (F) sur les montants (H)", ha="center", fontsize=10, color="#666")
    draw_side(ax, 10, 65, 0.055)
    ax.annotate("Support dossier (F)\n650 x 70 x 44 mm\nAngle ~35 deg", xy=(55, 95), fontsize=9, color=WOOD4, fontweight="bold")
    ax.text(50, 58, "2 lattes collees face a face (section 44 x 70 mm)", ha="center", fontsize=10)
    ax.text(50, 52, f"Angle : ~{BACKREST_TILT} deg de la verticale  |  Utiliser une fausse equerre", ha="center", fontsize=9, color="red")
    ax.text(50, 46, "Les supports F reposent sur les montants H (ancrage solide)", ha="center", fontsize=9, fontweight="bold", color=WOOD4)
    pdf.savefig(fig); plt.close(fig)

def page_backrest(pdf):
    fig, ax = new_page(pdf, "Etape 7 : Pose du dossier")
    ax.text(50, 125, f"Visser les {N_BACK} lattes (B) sur les supports", ha="center", fontsize=10, color="#666")
    s = 0.04
    x0 = 15; y0 = 60
    for px in [0, CHAIR_W - PANEL_W]:
        bx = px + (PANEL_W-FRAME_W)/2
        ax.add_patch(Rectangle((x0+bx*s, y0+SEAT_H*s), FRAME_W*s, BACK_DZ*s, fc=WOOD1, ec="black", lw=1))
    for i in range(N_BACK):
        frac = (i + 0.5) / N_BACK
        bz = SEAT_H + frac * BACK_DZ
        ax.add_patch(Rectangle((x0+PANEL_W*s, y0+bz*s), INNER_W*s, SLAT_W*s, fc=WOOD3, ec="black", lw=0.7))
        if i == 0:
            ax.text(x0+CHAIR_W*s/2, y0+(bz+SLAT_W/2)*s, "B", ha="center", va="center", fontsize=10, fontweight="bold", color="white")
    ax.text(50, y0-5, f"Vue arriere - {N_BACK} lattes de {INNER_W} x 95 mm", ha="center", fontsize=9, color="#666")
    ax.text(50, y0-12, f"2 vis par latte et par support = {N_BACK*4} vis", ha="center", fontsize=10, fontweight="bold")
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
        "24 pieces au total",
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
        page_anchors(pdf)
        page_back_supports(pdf)
        page_backrest(pdf)
        page_finishing(pdf)
        page_final(pdf)
    print(f"Guide PDF genere : {PDF_PATH} ({os.path.getsize(PDF_PATH) // 1024} Ko)")

if __name__ == "__main__":
    generate_guide()
