"""Guide de construction illustre - Table basse en palettes recyclees."""
import os
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle, Polygon
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(OUTPUT_DIR, "guide_construction.pdf")

# Dimensions
TL, TW, TH = 1200, 600, 450
PW, PT, PG = 95, 22, 3
LW, LD, LH = 95, 95, 406
SH, SI = 100, 50
BW, BT = 70, 22
NP = 6

WOOD1, WOOD2, WOOD3, WOOD4 = "#d2a679", "#c49a6c", "#b8956a", "#a0784e"

def new_page(pdf, title, subtitle=None):
    fig, ax = plt.subplots(figsize=(8.27, 11.69))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 140)
    ax.axis("off")
    ax.text(50, 133, title, ha="center", va="top", fontsize=16, fontweight="bold")
    if subtitle:
        ax.text(50, 128, subtitle, ha="center", va="top", fontsize=11, color="#555555")
    return fig, ax

def draw_table_front(ax, x0, y0, scale=0.06):
    s = scale
    # legs
    for lx in [0, TL - LW]:
        ax.add_patch(Rectangle((x0 + lx*s, y0), LW*s, (TH-PT)*s, fc=WOOD1, ec="black", lw=0.8))
    # shelf
    ax.add_patch(Rectangle((x0 + SI*s, y0 + SH*s), (TL-2*SI)*s, PT*s, fc=WOOD2, ec="black", lw=0.6))
    # brace
    ax.add_patch(Rectangle((x0 + LW*s, y0 + (SH+PT)*s), (TL-2*LW)*s, BW*s, fc=WOOD3, ec="black", lw=0.5, ls="--"))
    # top
    ax.add_patch(Rectangle((x0, y0 + (TH-PT)*s), TL*s, PT*s, fc=WOOD2, ec="black", lw=1.0))

def draw_table_side(ax, x0, y0, scale=0.06):
    s = scale
    for lx in [0, TW - LD]:
        ax.add_patch(Rectangle((x0 + lx*s, y0), LD*s, (TH-PT)*s, fc=WOOD1, ec="black", lw=0.8))
    ax.add_patch(Rectangle((x0 + SI*s, y0 + SH*s), (TW-2*SI)*s, PT*s, fc=WOOD2, ec="black", lw=0.6))
    ax.add_patch(Rectangle((x0, y0 + (TH-PT)*s), TW*s, PT*s, fc=WOOD2, ec="black", lw=1.0))

def draw_pallet_top(ax, x0, y0, w, h):
    ax.add_patch(Rectangle((x0, y0), w, h, fc="#f0dcc0", ec="black", lw=1))
    n = 5
    pw = (h - (n+1)*0.3) / n
    for i in range(n):
        py = y0 + 0.3 + i * (pw + 0.3)
        ax.add_patch(Rectangle((x0+0.3, py), w-0.6, pw, fc=WOOD1, ec="black", lw=0.5))

def page_cover(pdf):
    fig, ax = new_page(pdf, "Guide de Construction", "Table Basse en Palettes Recyclees")
    ax.text(50, 123, "100% bois de palette recycle", ha="center", fontsize=13, style="italic", color=WOOD4)
    draw_table_front(ax, 14, 55, 0.06)
    ax.text(50, 50, f"{TL} x {TW} x {TH} mm", ha="center", fontsize=12, color="#333")
    ax.text(50, 45, "6 lattes plateau | 4 pieds | etagere inferieure", ha="center", fontsize=10, color="#666")
    ax.text(50, 15, "Inspire de : instructables.com/DIY-PALLET-TABLE-100-PALLET-WOOD", ha="center", fontsize=8, color="#999")
    pdf.savefig(fig); plt.close(fig)

def page_materials(pdf):
    fig, ax = new_page(pdf, "Materiaux et Outillage")
    ax.text(50, 125, "2 euro-palettes standard (1200 x 800 mm)", ha="center", fontsize=11)
    draw_pallet_top(ax, 10, 100, 35, 18)
    ax.text(27.5, 97, "Palette 1", ha="center", fontsize=9)
    draw_pallet_top(ax, 55, 100, 35, 18)
    ax.text(72.5, 97, "Palette 2", ha="center", fontsize=9)
    ax.add_patch(Rectangle((10, 82, ), 30, 10, fc="#e8e8e8", ec="black", lw=0.8, zorder=2))
    ax.text(25, 87, "HT", ha="center", fontsize=14, fontweight="bold", color="green", zorder=3)
    ax.add_patch(Rectangle((55, 82), 30, 10, fc="#e8e8e8", ec="black", lw=0.8, zorder=2))
    ax.text(70, 87, "MB", ha="center", fontsize=14, fontweight="bold", color="red", zorder=3)
    ax.text(25, 79, "Traitement thermique (OK)", ha="center", fontsize=8, color="green")
    ax.text(70, 79, "Bromure methyle (TOXIQUE)", ha="center", fontsize=8, color="red")
    tools = [
        "Pied-de-biche / levier",
        "Arrache-clou / tenaille",
        "Scie circulaire ou scie a onglet",
        "Ponceuse orbitale (grains 80, 120, 180)",
        "Visseuse + vis a bois 4x50 mm",
        "Serre-joints (x4 minimum)",
        "Colle a bois D3 (exterieur)",
        "Equerre de menuisier",
        "Metre ruban + crayon",
    ]
    ax.text(50, 72, "Outillage necessaire :", ha="center", fontsize=12, fontweight="bold")
    for i, t in enumerate(tools):
        ax.text(20, 66 - i*4.5, f"  * {t}", fontsize=10, va="top")
    pdf.savefig(fig); plt.close(fig)


def page_step1_dismantling(pdf):
    fig, ax = new_page(pdf, "Etape 1 : Demontage des palettes")
    # Side view of pallet
    ax.text(50, 125, "Vue laterale - insertion du pied-de-biche", ha="center", fontsize=10, color="#666")
    # Bottom plank
    ax.add_patch(Rectangle((15, 108), 70, 3, fc=WOOD3, ec="black", lw=0.8))
    ax.text(85.5, 109.5, "latte", fontsize=8, va="center")
    # Blocks
    for bx in [20, 47, 74]:
        ax.add_patch(Rectangle((bx, 111), 8, 8, fc=WOOD1, ec="black", lw=0.8))
    ax.text(85.5, 115, "bloc", fontsize=8, va="center")
    # Top plank
    ax.add_patch(Rectangle((15, 119), 70, 3, fc=WOOD2, ec="black", lw=0.8))
    ax.text(85.5, 120.5, "latte", fontsize=8, va="center")
    # Lever arrow
    ax.annotate("", xy=(17, 122), xytext=(10, 112),
                arrowprops=dict(arrowstyle="->", color="red", lw=2))
    ax.text(7, 117, "Levier", fontsize=9, color="red", rotation=50)
    # Separated parts below
    ax.text(50, 98, "Pieces recuperees :", ha="center", fontsize=11, fontweight="bold")
    # Planks
    ax.text(15, 93, "Lattes (x14)", fontsize=9, fontweight="bold")
    for i in range(5):
        ax.add_patch(Rectangle((15, 85 + i*1.5), 30, 1.2, fc=WOOD2, ec="black", lw=0.4))
    ax.text(30, 83, "...", ha="center", fontsize=10)
    # Blocks
    ax.text(55, 93, "Blocs (x18)", fontsize=9, fontweight="bold")
    for i in range(6):
        ax.add_patch(Rectangle((55 + i*5, 87), 4, 4, fc=WOOD1, ec="black", lw=0.5))
    for i in range(6):
        ax.add_patch(Rectangle((55 + i*5, 82), 4, 4, fc=WOOD1, ec="black", lw=0.5))
    for i in range(6):
        ax.add_patch(Rectangle((55 + i*5, 77), 4, 4, fc=WOOD1, ec="black", lw=0.5))
    # Crosspieces
    ax.text(15, 73, "Traverses (x6)", fontsize=9, fontweight="bold")
    for i in range(4):
        ax.add_patch(Rectangle((15, 66 + i*1.5), 20, 1.2, fc=WOOD3, ec="black", lw=0.4))
    # Tips
    ax.text(50, 55, "Conseils :", ha="center", fontsize=11, fontweight="bold")
    tips = [
        "- Inserer le levier entre la latte et le bloc",
        "- Faire levier doucement pour ne pas casser les lattes",
        "- Retirer tous les clous a la tenaille",
        "- Trier les pieces par taille et etat",
    ]
    for i, t in enumerate(tips):
        ax.text(15, 49 - i*4, t, fontsize=9)
    pdf.savefig(fig); plt.close(fig)

def page_step2_cutting(pdf):
    fig, ax = new_page(pdf, "Etape 2 : Debit des pieces")
    pieces = [
        ("A", "Latte plateau", 6, "1200 x 95 x 22", WOOD2),
        ("B", "Pied (3 blocs colles)", 4, "95 x 95 x 406", WOOD1),
        ("C", "Latte etagere", 4, "1100 x 95 x 22", WOOD2),
        ("D", "Traverse plateau", 3, "600 x 22 x 22", WOOD3),
        ("E", "Entretoise laterale", 2, "1010 x 70 x 22", WOOD3),
        ("F", "Traverse etagere", 2, "600 x 22 x 22", WOOD3),
    ]
    # Header
    ax.add_patch(Rectangle((5, 117), 90, 7, fc="#444444", ec="black", lw=0.8))
    for hx, ht in [(8,"Ref"),(22,"Piece"),(52,"Qte"),(63,"Dimensions (mm)")]:
        ax.text(hx, 120.5, ht, fontsize=9, fontweight="bold", color="white")
    for i, (ref, name, qty, dims, color) in enumerate(pieces):
        y = 110 - i * 10
        ax.add_patch(Rectangle((5, y), 90, 8, fc="#faf5ef" if i%2==0 else "#f0e8dc", ec="#cccccc", lw=0.5))
        # Colored square sample
        ax.add_patch(Rectangle((6, y+1), 6, 6, fc=color, ec="black", lw=0.6))
        ax.text(9, y+4, ref, ha="center", va="center", fontsize=10, fontweight="bold")
        ax.text(22, y+4, name, va="center", fontsize=9)
        ax.text(55, y+4, str(qty), ha="center", va="center", fontsize=10, fontweight="bold")
        ax.text(63, y+4, dims, va="center", fontsize=9)
    # Visual of pieces
    ax.text(50, 43, "Vue des pieces (echelle relative) :", ha="center", fontsize=10, fontweight="bold")
    # Plank A
    ax.add_patch(Rectangle((5, 36), 60, 3, fc=WOOD2, ec="black", lw=0.6))
    ax.text(35, 37.5, "A - 1200 mm", ha="center", va="center", fontsize=7, color="white", fontweight="bold")
    # Plank C
    ax.add_patch(Rectangle((5, 31), 55, 3, fc=WOOD2, ec="black", lw=0.6))
    ax.text(32, 32.5, "C - 1100 mm", ha="center", va="center", fontsize=7, color="white", fontweight="bold")
    # Brace E
    ax.add_patch(Rectangle((5, 26), 50, 2.5, fc=WOOD3, ec="black", lw=0.6))
    ax.text(30, 27.2, "E - 1010 mm", ha="center", va="center", fontsize=7, color="white", fontweight="bold")
    # Traverse D/F
    ax.add_patch(Rectangle((5, 22), 30, 2, fc=WOOD3, ec="black", lw=0.6))
    ax.text(20, 23, "D/F - 600 mm", ha="center", va="center", fontsize=7, color="white", fontweight="bold")
    # Leg B
    ax.add_patch(Rectangle((70, 22), 5, 17, fc=WOOD1, ec="black", lw=0.6))
    ax.text(72.5, 30, "B", ha="center", va="center", fontsize=8, fontweight="bold")
    ax.text(72.5, 19, "406 mm", ha="center", fontsize=7)
    ax.text(50, 14, "Total : 21 pieces a partir de 2 euro-palettes", ha="center", fontsize=11, fontweight="bold", color=WOOD4)
    pdf.savefig(fig); plt.close(fig)


def page_step3_sanding(pdf):
    fig, ax = new_page(pdf, "Etape 3 : Poncage")
    ax.text(50, 125, "Poncer toutes les pieces avant assemblage", ha="center", fontsize=11, color="#666")
    # Draw a plank with 3 zones
    plank_y = 90
    zone_w = 22
    zones = [("Grain 80", "#e8c896", "Degrossissage"), ("Grain 120", "#f0d8a8", "Lissage"), ("Grain 180", "#f8e8c0", "Finition")]
    for i, (label, color, desc) in enumerate(zones):
        x = 14 + i * (zone_w + 3)
        ax.add_patch(Rectangle((x, plank_y), zone_w, 12, fc=color, ec="black", lw=0.8))
        ax.text(x + zone_w/2, plank_y + 6, label, ha="center", va="center", fontsize=10, fontweight="bold")
        ax.text(x + zone_w/2, plank_y - 3, desc, ha="center", fontsize=9, color="#555")
    # Arrows between zones
    for i in range(2):
        x1 = 14 + (i+1) * (zone_w + 3) - 2
        ax.annotate("", xy=(x1+2, plank_y+6), xytext=(x1-1, plank_y+6),
                    arrowprops=dict(arrowstyle="->", color="blue", lw=1.5))
    # Direction arrow
    ax.annotate("", xy=(82, plank_y+13), xytext=(14, plank_y+13),
                arrowprops=dict(arrowstyle="->", color="green", lw=2))
    ax.text(48, plank_y+16, "Sens du poncage (fil du bois)", ha="center", fontsize=9, color="green")
    # Tips
    tips = [
        "1. Commencer par le grain 80 pour retirer les eclats et la salete",
        "2. Passer au grain 120 pour lisser la surface",
        "3. Finir au grain 180 pour une surface douce au toucher",
        "",
        "Toujours poncer dans le sens du fil du bois",
        "Depousssierer entre chaque grain",
        "Insister sur les aretes pour les adoucir (chanfrein leger)",
        "Porter un masque anti-poussiere",
    ]
    for i, t in enumerate(tips):
        y = 75 - i * 5
        ax.text(15, y, t, fontsize=10)
    pdf.savefig(fig); plt.close(fig)

def page_step4_legs(pdf):
    fig, ax = new_page(pdf, "Etape 4 : Fabrication des pieds")
    ax.text(50, 125, "Empiler et coller 3 blocs de palette par pied", ha="center", fontsize=11, color="#666")
    # 3 separate blocks on the left
    ax.text(20, 115, "Avant", ha="center", fontsize=10, fontweight="bold")
    for i in range(3):
        y = 95 + i * 7
        ax.add_patch(Rectangle((13, y), 14, 5.5, fc=WOOD1, ec="black", lw=0.8))
        ax.text(20, y+2.8, f"Bloc {i+1}", ha="center", va="center", fontsize=8)
    # Arrow
    ax.annotate("", xy=(42, 103), xytext=(32, 103),
                arrowprops=dict(arrowstyle="->", color="blue", lw=2.5))
    ax.text(37, 107, "Colle D3", ha="center", fontsize=8, color="blue")
    # Stacked blocks with clamps
    ax.text(58, 115, "Collage", ha="center", fontsize=10, fontweight="bold")
    for i in range(3):
        y = 95 + i * 5.5
        ax.add_patch(Rectangle((51, y), 14, 5, fc=WOOD1, ec="black", lw=0.8))
    # Clamp symbols (C shapes)
    for cy in [96, 105]:
        ax.plot([48, 48, 68, 68], [cy, cy+5, cy+5, cy], color="gray", lw=2.5)
    ax.text(58, 92, "Serre-joints\n24h de sechage", ha="center", fontsize=8, color="gray")
    # Arrow
    ax.annotate("", xy=(82, 103), xytext=(72, 103),
                arrowprops=dict(arrowstyle="->", color="blue", lw=2.5))
    # Final leg
    ax.text(90, 115, "Resultat", ha="center", fontsize=10, fontweight="bold")
    ax.add_patch(Rectangle((84, 95), 12, 16, fc=WOOD1, ec="black", lw=1.2))
    ax.text(90, 103, "406\nmm", ha="center", va="center", fontsize=9, fontweight="bold")
    # Saw line
    ax.plot([83, 97], [111.5, 111.5], color="red", lw=1.5, ls="--")
    ax.text(90, 113, "Recouper", ha="center", fontsize=8, color="red")
    # Repeat x4
    ax.text(50, 82, "Repeter 4 fois (12 blocs au total)", ha="center", fontsize=12, fontweight="bold", color=WOOD4)
    # Diagram of block origin
    ax.text(50, 72, "Origine des blocs sur la palette :", ha="center", fontsize=10, fontweight="bold")
    ax.add_patch(Rectangle((20, 55), 60, 12, fc="#f0dcc0", ec="black", lw=0.8))
    for bx in [25, 47, 69]:
        ax.add_patch(Rectangle((bx, 57), 8, 8, fc=WOOD1, ec="black", lw=0.8))
        ax.annotate("", xy=(bx+4, 55), xytext=(bx+4, 50),
                    arrowprops=dict(arrowstyle="->", color="red", lw=1.2))
    ax.text(50, 47, "9 blocs par palette = 18 blocs disponibles (12 necessaires)", ha="center", fontsize=9)
    pdf.savefig(fig); plt.close(fig)


def page_step5_frame(pdf):
    fig, ax = new_page(pdf, "Etape 5 : Assemblage du cadre inferieur")
    ax.text(50, 125, "Visser les traverses et entretoises entre les pieds", ha="center", fontsize=11, color="#666")
    # Front view of frame
    ax.text(50, 118, "Vue de face", ha="center", fontsize=10, fontweight="bold")
    s = 0.055
    y0 = 70
    # 4 legs
    for lx in [0, TL - LW]:
        ax.add_patch(Rectangle((12 + lx*s, y0), LW*s, LH*s, fc=WOOD1, ec="black", lw=1))
    # Bottom traverses F
    ax.add_patch(Rectangle((12 + SI*s, y0 + (SH-BT)*s), (TL-2*SI)*s, BT*s, fc=WOOD3, ec="black", lw=0.8))
    ax.text(12 + TL*s/2, y0 + (SH-BT/2)*s, "F", ha="center", va="center", fontsize=10, fontweight="bold", color="white")
    # Side braces E
    brace_y = y0 + (SH+PT)*s
    ax.add_patch(Rectangle((12 + LW*s, brace_y), (TL-2*LW)*s, BW*s, fc=WOOD3, ec="black", lw=0.8, ls="--"))
    ax.text(12 + TL*s/2, brace_y + BW*s/2, "E", ha="center", va="center", fontsize=10, fontweight="bold", color="white")
    # Labels
    ax.annotate("Pied (B)", xy=(12 + LW*s/2, y0 + LH*s/2), xytext=(12 + LW*s/2, y0 + LH*s + 5),
                fontsize=8, ha="center", arrowprops=dict(arrowstyle="->", color="blue", lw=0.8), color="blue")
    # Screw marks
    for sx in [SI + 5, TL - SI - 5]:
        ax.plot(12 + sx*s, y0 + (SH-BT/2)*s, "x", color="red", ms=6, mew=1.5)
    ax.text(50, y0 - 5, "Vis 4x50 mm aux intersections (marques X)", ha="center", fontsize=9, color="red")
    # Assembly order
    ax.text(50, 55, "Ordre d'assemblage :", ha="center", fontsize=11, fontweight="bold")
    steps = [
        "1. Poser 2 pieds a plat, ecartement = 1200 mm (ext. a ext.)",
        "2. Visser la traverse F entre les pieds (a 100 mm du sol)",
        "3. Visser l'entretoise E entre les pieds (au-dessus de F)",
        "4. Repeter pour l'autre paire de pieds",
        "5. Relier les 2 cadres avec les traverses F cote largeur",
    ]
    for i, st in enumerate(steps):
        ax.text(12, 48 - i*5, st, fontsize=9)
    pdf.savefig(fig); plt.close(fig)

def page_step6_shelf(pdf):
    fig, ax = new_page(pdf, "Etape 6 : Pose de l'etagere")
    ax.text(50, 125, "Visser 4 lattes (C) sur les traverses inferieures", ha="center", fontsize=11, color="#666")
    # Top view of shelf
    ax.text(50, 118, "Vue de dessus de l'etagere", ha="center", fontsize=10, fontweight="bold")
    shelf_len = 55
    shelf_x0 = 22
    colors = [WOOD2, WOOD1, WOOD2, WOOD1]
    for i in range(4):
        y = 95 + i * 5
        ax.add_patch(Rectangle((shelf_x0, y), shelf_len, 4.5, fc=colors[i], ec="black", lw=0.6))
        ax.text(shelf_x0 + shelf_len/2, y+2.2, f"C{i+1} - 1100 x 95 mm", ha="center", va="center", fontsize=8)
    # Traverses below (dashed)
    for tx in [shelf_x0+2, shelf_x0+shelf_len-4]:
        ax.add_patch(Rectangle((tx, 93), 2, 24, fc="none", ec="red", lw=1, ls="--"))
    ax.text(shelf_x0-1, 105, "F", fontsize=9, color="red", fontweight="bold")
    # Screw marks
    for i in range(4):
        y = 95 + i * 5 + 2.2
        for tx in [shelf_x0+3, shelf_x0+shelf_len-3]:
            ax.plot(tx, y, "x", color="red", ms=5, mew=1.5)
    # Side view
    ax.text(50, 82, "Vue de cote", ha="center", fontsize=10, fontweight="bold")
    s = 0.055
    y0 = 55
    for lx in [0, TW-LD]:
        ax.add_patch(Rectangle((25 + lx*s, y0), LD*s, LH*s, fc=WOOD1, ec="black", lw=0.8))
    ax.add_patch(Rectangle((25 + SI*s, y0+SH*s), (TW-2*SI)*s, PT*s, fc=WOOD2, ec="black", lw=1))
    ax.text(25 + TW*s/2, y0+SH*s+PT*s/2, "Etagere (C)", ha="center", va="center", fontsize=8, fontweight="bold")
    # Height annotation
    ax.annotate("", xy=(25-2, y0+SH*s+PT*s), xytext=(25-2, y0),
                arrowprops=dict(arrowstyle="<->", color="blue", lw=0.8))
    ax.text(22, y0+SH*s/2, f"{SH} mm", fontsize=7, color="blue", rotation=90, ha="center", va="center")
    pdf.savefig(fig); plt.close(fig)


def page_step7_top_traverses(pdf):
    fig, ax = new_page(pdf, "Etape 7 : Traverses du plateau")
    ax.text(50, 125, "Fixer 3 traverses (D) sur le haut des pieds", ha="center", fontsize=11, color="#666")
    # Top view showing traverse positions
    ax.text(50, 118, "Vue de dessus (plateau retire)", ha="center", fontsize=10, fontweight="bold")
    s = 0.06
    x0 = 14
    # Table outline (dashed)
    ax.add_patch(Rectangle((x0, 85), TL*s, TW*s, fc="none", ec="#aaa", lw=0.8, ls=":"))
    # Legs (corners)
    for lx, ly in [(0,0),(TL-LW,0),(0,TW-LD),(TL-LW,TW-LD)]:
        ax.add_patch(Rectangle((x0+lx*s, 85+ly*s), LW*s, LD*s, fc=WOOD1, ec="black", lw=0.8))
    # 3 Traverses
    positions = [LW, (TL-BT)/2, TL-LW-BT]
    for i, tx in enumerate(positions):
        ax.add_patch(Rectangle((x0+tx*s, 85), BT*s, TW*s, fc=WOOD3, ec="black", lw=1))
        label = "D" if i < 3 else ""
        ax.text(x0+(tx+BT/2)*s, 85+TW*s/2, label, ha="center", va="center", fontsize=9, fontweight="bold", color="white")
    # Labels
    ax.text(x0+LW*s/2, 85+LD*s/2, "B", ha="center", va="center", fontsize=8, fontweight="bold")
    # Dimension
    ax.annotate("", xy=(x0+TL*s, 85-3), xytext=(x0, 85-3),
                arrowprops=dict(arrowstyle="<->", color="blue", lw=0.8))
    ax.text(x0+TL*s/2, 85-6, f"{TL} mm", ha="center", fontsize=8, color="blue")
    # Front view
    ax.text(50, 72, "Vue de face", ha="center", fontsize=10, fontweight="bold")
    s2 = 0.05
    y0 = 40
    for lx in [0, TL-LW]:
        ax.add_patch(Rectangle((14+lx*s2, y0), LW*s2, LH*s2, fc=WOOD1, ec="black", lw=0.8))
    # Traverses on top
    for tx in positions:
        ax.add_patch(Rectangle((14+tx*s2, y0+LH*s2), BT*s2, BT*s2, fc=WOOD3, ec="black", lw=0.8))
    ax.text(14+positions[1]*s2, y0+LH*s2+BT*s2+2, "D", ha="center", fontsize=9, fontweight="bold", color=WOOD4)
    # Screw marks
    for tx in positions:
        ax.plot(14+(tx+BT/2)*s2, y0+LH*s2+BT*s2/2, "x", color="red", ms=5, mew=1.5)
    ax.text(50, y0-5, "Visser par le dessous a travers les traverses dans les pieds", ha="center", fontsize=9)
    pdf.savefig(fig); plt.close(fig)

def page_step8_top(pdf):
    fig, ax = new_page(pdf, "Etape 8 : Pose du plateau")
    ax.text(50, 125, "Poser et visser les 6 lattes (A) avec un espacement de 3 mm", ha="center", fontsize=11, color="#666")
    # Top view
    ax.text(50, 118, "Vue de dessus", ha="center", fontsize=10, fontweight="bold")
    s = 0.06
    x0 = 14
    colors = [WOOD2, WOOD1, WOOD3, WOOD2, WOOD1, WOOD3]
    total_pw = NP * PW + (NP - 1) * PG
    start_y = (TW - total_pw) / 2.0
    for i in range(NP):
        py = start_y + i * (PW + PG)
        ax.add_patch(Rectangle((x0, 88+py*s), TL*s, PW*s, fc=colors[i], ec="black", lw=0.6))
        if i == 0:
            ax.text(x0+TL*s/2, 88+(py+PW/2)*s, f"A - {TL} x {PW} mm", ha="center", va="center", fontsize=7, color="white", fontweight="bold")
    # Gap detail
    ax.text(50, 82, "Detail de l'espacement :", ha="center", fontsize=10, fontweight="bold")
    # Zoom on gap
    zx, zy = 30, 65
    ax.add_patch(Rectangle((zx, zy), 20, 6, fc=WOOD2, ec="black", lw=0.8))
    ax.add_patch(Rectangle((zx, zy+7.5), 20, 6, fc=WOOD1, ec="black", lw=0.8))
    ax.annotate("", xy=(zx+22, zy+7.5), xytext=(zx+22, zy+6),
                arrowprops=dict(arrowstyle="<->", color="red", lw=1))
    ax.text(zx+25, zy+6.8, "3 mm", fontsize=9, color="red", fontweight="bold")
    ax.text(zx+10, zy+3, "Latte", ha="center", va="center", fontsize=8)
    ax.text(zx+10, zy+10.5, "Latte", ha="center", va="center", fontsize=8)
    # Spacer tip
    ax.text(50, 55, "Utiliser une cale de 3 mm (ex: morceau de carton)", ha="center", fontsize=10, color="#555")
    ax.text(50, 50, "entre chaque latte pour un espacement regulier.", ha="center", fontsize=10, color="#555")
    ax.text(50, 42, "Visser chaque latte dans les 3 traverses (D) en dessous.", ha="center", fontsize=10)
    ax.text(50, 37, "2 vis par intersection = 36 vis au total.", ha="center", fontsize=10, fontweight="bold")
    pdf.savefig(fig); plt.close(fig)


def page_step9_finishing(pdf):
    fig, ax = new_page(pdf, "Etape 9 : Finition")
    ax.text(50, 125, "Proteger et embellir votre table", ha="center", fontsize=11, color="#666")
    # Draw finished table
    draw_table_front(ax, 14, 85, 0.06)
    # Finishing options
    options = [
        ("Huile de lin", "#c8a050", [
            "Aspect naturel et chaleureux",
            "Nourrit le bois en profondeur",
            "2 a 3 couches, 24h entre couches",
            "Ideal pour usage interieur",
        ]),
        ("Vernis polyurethane", "#e0c080", [
            "Protection maximale",
            "Surface lisse et brillante",
            "2 couches + poncage fin entre couches",
            "Resistant aux taches et a l'eau",
        ]),
        ("Lasure bois", "#a07840", [
            "Pour usage exterieur",
            "Protection UV et intemperies",
            "Teinte au choix (chene, noyer...)",
            "Renouveler tous les 2-3 ans",
        ]),
    ]
    for i, (name, color, details) in enumerate(options):
        x = 8 + i * 30
        ax.add_patch(Rectangle((x, 50), 26, 28, fc="#faf5ef", ec=color, lw=2, zorder=2))
        ax.add_patch(Rectangle((x, 72), 26, 6, fc=color, ec=color, lw=1, zorder=3))
        ax.text(x+13, 75, name, ha="center", va="center", fontsize=9, fontweight="bold", color="white", zorder=4)
        for j, d in enumerate(details):
            ax.text(x+2, 67 - j*4.5, f"- {d}", fontsize=7.5, zorder=3)
    # General tips
    ax.text(50, 40, "Conseils generaux :", ha="center", fontsize=11, fontweight="bold")
    tips = [
        "- Poncer legerement (grain 180) avant la premiere couche",
        "- Depousssierer soigneusement au chiffon humide",
        "- Appliquer dans le sens du fil du bois",
        "- Laisser secher completement entre les couches",
    ]
    for i, t in enumerate(tips):
        ax.text(15, 34 - i*4.5, t, fontsize=9)
    pdf.savefig(fig); plt.close(fig)

def page_final(pdf):
    fig, ax = new_page(pdf, "Resultat Final")
    ax.text(50, 125, "Votre table basse en palettes recyclees est terminee !", ha="center", fontsize=11, color=WOOD4)
    # Front view
    ax.text(25, 118, "Vue de face", ha="center", fontsize=9, fontweight="bold")
    draw_table_front(ax, 2, 90, 0.04)
    # Dimensions
    ax.annotate("", xy=(2+TL*0.04, 89), xytext=(2, 89),
                arrowprops=dict(arrowstyle="<->", color="blue", lw=0.6))
    ax.text(2+TL*0.02, 87, f"{TL} mm", ha="center", fontsize=7, color="blue")
    ax.annotate("", xy=(2+TL*0.04+3, 90+TH*0.04), xytext=(2+TL*0.04+3, 90),
                arrowprops=dict(arrowstyle="<->", color="blue", lw=0.6))
    ax.text(2+TL*0.04+6, 90+TH*0.02, f"{TH} mm", fontsize=7, color="blue", rotation=90, va="center")
    # Side view
    ax.text(75, 118, "Vue de cote", ha="center", fontsize=9, fontweight="bold")
    draw_table_side(ax, 60, 90, 0.04)
    ax.annotate("", xy=(60+TW*0.04, 89), xytext=(60, 89),
                arrowprops=dict(arrowstyle="<->", color="blue", lw=0.6))
    ax.text(60+TW*0.02, 87, f"{TW} mm", ha="center", fontsize=7, color="blue")
    # BOM summary
    ax.text(50, 78, "Recapitulatif", ha="center", fontsize=12, fontweight="bold")
    summary = [
        "Materiau : 2 euro-palettes recyclees (marquage HT)",
        f"Dimensions finales : {TL} x {TW} x {TH} mm (L x l x H)",
        f"Plateau : {NP} lattes de {PW} x {PT} mm",
        f"Pieds : 4 x ({LW} x {LD} x {LH} mm)",
        f"Etagere : 4 lattes a {SH} mm du sol",
        "Nombre total de pieces : 21",
        "Temps estime : 1 week-end (hors sechage colle)",
    ]
    for i, s in enumerate(summary):
        ax.text(15, 72 - i*4.5, f"  {s}", fontsize=9)
    # Credits
    ax.text(50, 25, "Inspire de : instructables.com/DIY-PALLET-TABLE-100-PALLET-WOOD", ha="center", fontsize=8, color="#999")
    ax.text(50, 20, "Genere automatiquement avec Python (matplotlib + numpy-stl)", ha="center", fontsize=8, color="#999")
    pdf.savefig(fig); plt.close(fig)

def generate_guide():
    with PdfPages(PDF_PATH) as pdf:
        page_cover(pdf)
        page_materials(pdf)
        page_step1_dismantling(pdf)
        page_step2_cutting(pdf)
        page_step3_sanding(pdf)
        page_step4_legs(pdf)
        page_step5_frame(pdf)
        page_step6_shelf(pdf)
        page_step7_top_traverses(pdf)
        page_step8_top(pdf)
        page_step9_finishing(pdf)
        page_final(pdf)
    print(f"Guide PDF genere : {PDF_PATH} ({os.path.getsize(PDF_PATH)//1024} Ko)")

if __name__ == "__main__":
    generate_guide()
