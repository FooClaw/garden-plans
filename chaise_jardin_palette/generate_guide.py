"""Guide de construction illustre - Deck Chair de jardin en palettes."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_pdf import PdfPages

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(OUTPUT_DIR, "guide_construction.pdf")
WOOD1, WOOD2, WOOD3, WOOD4 = "#d2a679", "#c49a6c", "#b8956a", "#a0784e"

# Dimensions deck chair
CHAIR_W = 600; SEAT_D = 480; BACK_H = 900; SEAT_H = 350
ARMREST_H = 600; ARMREST_L = 550; ARMREST_W = 95
N_SEAT = 6; N_BACK = 5
SLAT_W = 70; SLAT_T = 22; SLAT_GAP = 5
FRONT_LEG = (44, 70, 350); BACK_LEG = (44, 70, 900)

def new_page(pdf, title, subtitle=None):
    fig, ax = plt.subplots(figsize=(8.27, 11.69))
    ax.set_xlim(0, 100); ax.set_ylim(0, 140); ax.axis("off")
    ax.text(50, 133, title, ha="center", va="top", fontsize=16, fontweight="bold")
    if subtitle:
        ax.text(50, 128, subtitle, ha="center", va="top", fontsize=11, color="#555")
    return fig, ax

def draw_side(ax, x0, y0, s=0.05):
    """Vue de cote simplifiee de la deck chair."""
    # Pied avant (court)
    ax.add_patch(Rectangle((x0, y0), 70*s, 350*s, fc=WOOD1, ec="black", lw=1))
    # Pied arriere (long, dossier)
    ax.add_patch(Rectangle((x0+(SEAT_D-70)*s, y0), 70*s, BACK_H*s, fc=WOOD1, ec="black", lw=1))
    # Assise
    ax.add_patch(Rectangle((x0, y0+(SEAT_H-SLAT_T)*s), SEAT_D*s, SLAT_T*s, fc=WOOD2, ec="black", lw=1))
    # Dossier lattes
    for i in range(N_BACK):
        bz = SEAT_H + 30 + i * (SLAT_W + SLAT_GAP)
        ax.add_patch(Rectangle((x0+(SEAT_D-70)*s, y0+bz*s), SLAT_T*s, SLAT_W*s, fc=WOOD3, ec="black", lw=0.5))
    # Accoudoir
    ax.add_patch(Rectangle((x0, y0+ARMREST_H*s), ARMREST_L*s, SLAT_T*s, fc=WOOD2, ec="black", lw=0.8, ls="--"))
    # Traverse basse
    ax.add_patch(Rectangle((x0+70*s, y0+100*s), (SEAT_D-140)*s, 22*s, fc=WOOD3, ec="black", lw=0.4))

def draw_front(ax, x0, y0, s=0.05):
    """Vue de face simplifiee."""
    # Pieds avant
    ax.add_patch(Rectangle((x0, y0), 44*s, SEAT_H*s, fc=WOOD1, ec="black", lw=1))
    ax.add_patch(Rectangle((x0+(CHAIR_W-44)*s, y0), 44*s, SEAT_H*s, fc=WOOD1, ec="black", lw=1))
    # Pieds arriere (pointilles)
    t = 30
    ax.add_patch(Rectangle((x0+t*s, y0), 44*s, BACK_H*s, fc=WOOD1, ec="black", lw=0.6, ls="--", alpha=0.5))
    ax.add_patch(Rectangle((x0+(CHAIR_W-44-t)*s, y0), 44*s, BACK_H*s, fc=WOOD1, ec="black", lw=0.6, ls="--", alpha=0.5))
    # Assise
    ax.add_patch(Rectangle((x0, y0+(SEAT_H-SLAT_T)*s), CHAIR_W*s, SLAT_T*s, fc=WOOD2, ec="black", lw=1))
    # Accoudoirs
    ax.add_patch(Rectangle((x0, y0+ARMREST_H*s), ARMREST_W*s, SLAT_T*s, fc=WOOD2, ec="black", lw=0.8))
    ax.add_patch(Rectangle((x0+(CHAIR_W-ARMREST_W)*s, y0+ARMREST_H*s), ARMREST_W*s, SLAT_T*s, fc=WOOD2, ec="black", lw=0.8))

def page_cover(pdf):
    fig, ax = new_page(pdf, "Guide de Construction", "Deck Chair de Jardin en Palettes Recyclees")
    ax.text(50, 123, "Style Adirondack - assise basse, dossier recline, accoudoirs", ha="center", fontsize=11, style="italic", color=WOOD4)
    draw_side(ax, 20, 60, 0.055)
    ax.text(50, 55, f"{CHAIR_W} x {SEAT_D} x {BACK_H} mm  |  Assise {SEAT_H} mm  |  Dossier ~110 deg", ha="center", fontsize=10, color="#333")
    ax.text(50, 50, "Adaptee a la table basse palette (450 mm)", ha="center", fontsize=10, color="#666")
    ax.text(50, 15, "Inspire de : instructables.com/A-Deck-Chair-Made-From-Pallet-Wood-Leftovers", ha="center", fontsize=8, color="#999")
    pdf.savefig(fig); plt.close(fig)

def page_materials(pdf):
    fig, ax = new_page(pdf, "Materiaux et Outillage")
    ax.text(50, 125, "1.5 euro-palettes standard (1200 x 800 mm)", ha="center", fontsize=11)
    ax.add_patch(Rectangle((20, 105), 25, 12, fc="#f0dcc0", ec="black", lw=1))
    for i in range(5): ax.add_patch(Rectangle((21, 106.5+i*2), 23, 1.5, fc=WOOD1, ec="black", lw=0.4))
    ax.text(32.5, 102, "Palette 1", ha="center", fontsize=8)
    ax.add_patch(Rectangle((55, 105), 25, 12, fc="#f0dcc0", ec="black", lw=1))
    for i in range(3): ax.add_patch(Rectangle((56, 106.5+i*2), 23, 1.5, fc=WOOD1, ec="black", lw=0.4))
    ax.text(67.5, 102, "1/2 Palette 2", ha="center", fontsize=8)
    ax.text(50, 95, "Choisir des palettes marquees HT", ha="center", fontsize=9, color="green")
    tools = ["Pied-de-biche / levier", "Arrache-clou / tenaille", "Scie circulaire + guide parallele",
             "Scie a onglet", "Ponceuse orbitale (80, 120, 180)", "Visseuse + vis 4x50 mm",
             "Serre-joints (x4)", "Colle a bois D3", "Fausse equerre (angle 110 deg)"]
    ax.text(50, 85, "Outillage :", ha="center", fontsize=12, fontweight="bold")
    for i, t in enumerate(tools):
        ax.text(20, 79 - i*4.5, f"  * {t}", fontsize=10)
    pdf.savefig(fig); plt.close(fig)

def page_dismantling(pdf):
    fig, ax = new_page(pdf, "Etape 1 : Demontage des palettes")
    ax.add_patch(Rectangle((15, 108), 70, 3, fc=WOOD3, ec="black", lw=0.8))
    for bx in [20, 47, 74]: ax.add_patch(Rectangle((bx, 111), 8, 8, fc=WOOD1, ec="black", lw=0.8))
    ax.add_patch(Rectangle((15, 119), 70, 3, fc=WOOD2, ec="black", lw=0.8))
    ax.annotate("", xy=(17, 122), xytext=(10, 112), arrowprops=dict(arrowstyle="->", color="red", lw=2))
    ax.text(7, 117, "Levier", fontsize=9, color="red", rotation=50)
    ax.text(50, 100, "Pieces a recuperer :", ha="center", fontsize=11, fontweight="bold")
    ax.text(15, 93, "Au moins 11 lattes longues (1200 mm)", fontsize=9)
    ax.text(15, 88, "Dont 2 non refendues (95 mm) pour accoudoirs", fontsize=9)
    tips = ["- Levier doucement pour ne pas casser les lattes", "- Retirer tous les clous", "- Garder les plus belles lattes pour l'assise et les accoudoirs"]
    for i, t in enumerate(tips):
        ax.text(15, 75 - i*5, t, fontsize=9)
    pdf.savefig(fig); plt.close(fig)

def page_cutting(pdf):
    fig, ax = new_page(pdf, "Etape 2 : Debit des pieces")
    pieces = [("A", "Latte assise x6", "600 x 70 x 22", WOOD2, 60),
              ("B", "Latte dossier x5", "480 x 70 x 22", WOOD3, 48),
              ("E", "Accoudoir x2", "550 x 95 x 22", WOOD2, 55),
              ("F/G", "Traverses", "512/452 x 44 x 22", WOOD3, 50),
              ("C", "Pied avant (2 collees)", "44 x 70 x 350", WOOD1, 8),
              ("D", "Pied arriere (2 collees)", "44 x 70 x 900", WOOD1, 8)]
    for i, (ref, name, dims, color, w) in enumerate(pieces):
        y = 115 - i * 10
        h = 3 if "Pied" not in name else 6
        ax.add_patch(Rectangle((10, y), w, h, fc=color, ec="black", lw=0.6))
        ax.text(10 + w/2, y + h/2, ref, ha="center", va="center", fontsize=8, fontweight="bold", color="white")
        ax.text(75, y + h/2, f"{name}\n{dims} mm", va="center", fontsize=8)
    ax.text(50, 48, "Refendre les lattes a 70 mm (sauf accoudoirs : 95 mm)", ha="center", fontsize=10, fontweight="bold", color=WOOD4)
    pdf.savefig(fig); plt.close(fig)

def page_legs(pdf):
    fig, ax = new_page(pdf, "Etape 3 : Fabrication des pieds")
    ax.text(50, 125, "Coller 2 lattes face a face pour chaque pied (section 44 x 70 mm)", ha="center", fontsize=10, color="#666")
    # Pied avant
    ax.text(25, 115, "Pied avant (C)", ha="center", fontsize=10, fontweight="bold")
    ax.add_patch(Rectangle((18, 100), 14, 2.5, fc=WOOD1, ec="black", lw=0.8))
    ax.add_patch(Rectangle((18, 103.5), 14, 2.5, fc=WOOD2, ec="black", lw=0.8))
    ax.annotate("", xy=(38, 103), xytext=(35, 103), arrowprops=dict(arrowstyle="->", color="blue", lw=2))
    ax.add_patch(Rectangle((40, 98), 5, 10, fc=WOOD1, ec="black", lw=1))
    ax.text(42.5, 103, "350\nmm", ha="center", va="center", fontsize=7, fontweight="bold")
    # Pied arriere
    ax.text(70, 115, "Pied arriere (D)", ha="center", fontsize=10, fontweight="bold")
    ax.add_patch(Rectangle((63, 100), 14, 2.5, fc=WOOD1, ec="black", lw=0.8))
    ax.add_patch(Rectangle((63, 103.5), 14, 2.5, fc=WOOD2, ec="black", lw=0.8))
    ax.annotate("", xy=(83, 103), xytext=(80, 103), arrowprops=dict(arrowstyle="->", color="blue", lw=2))
    ax.add_patch(Rectangle((85, 86), 5, 24, fc=WOOD1, ec="black", lw=1))
    ax.text(87.5, 98, "900\nmm", ha="center", va="center", fontsize=7, fontweight="bold")
    ax.text(50, 78, "Le pied arriere monte du sol au haut du dossier d'une seule piece", ha="center", fontsize=10, fontweight="bold", color=WOOD4)
    ax.text(50, 72, "Serre-joints + colle D3, 24h de sechage", ha="center", fontsize=9, color="#555")
    pdf.savefig(fig); plt.close(fig)

def page_side_frames(pdf):
    fig, ax = new_page(pdf, "Etape 4 : Cadres lateraux")
    ax.text(50, 125, "Assembler 2 cadres : pied avant + pied arriere + traverse laterale", ha="center", fontsize=10, color="#666")
    s = 0.045
    x0 = 20
    y0 = 70
    # Pied avant
    ax.add_patch(Rectangle((x0, y0), 70*s, 350*s, fc=WOOD1, ec="black", lw=1.2))
    ax.text(x0+35*s, y0+175*s, "C", ha="center", va="center", fontsize=9, fontweight="bold")
    # Pied arriere
    ax.add_patch(Rectangle((x0+(SEAT_D-70)*s, y0), 70*s, BACK_H*s, fc=WOOD1, ec="black", lw=1.2))
    ax.text(x0+(SEAT_D-35)*s, y0+450*s, "D", ha="center", va="center", fontsize=9, fontweight="bold")
    # Traverse laterale
    tz = SEAT_H - SLAT_T - 44
    ax.add_patch(Rectangle((x0+70*s, y0+tz*s), (SEAT_D-140)*s, 44*s, fc=WOOD3, ec="black", lw=0.8))
    ax.text(x0+SEAT_D/2*s, y0+(tz+22)*s, "H", ha="center", va="center", fontsize=9, fontweight="bold", color="white")
    # Vis
    for vx in [x0+70*s, x0+(SEAT_D-70)*s]:
        ax.plot(vx, y0+(tz+22)*s, "x", color="red", ms=6, mew=2)
    ax.text(50, y0-5, "Vis 4x50 mm aux intersections  |  Repeter x2 (gauche + droite)", ha="center", fontsize=9, color="red")
    ax.text(50, y0-12, "Les pieds arriere depassent au-dessus pour former le dossier", ha="center", fontsize=9, color="#555")
    pdf.savefig(fig); plt.close(fig)

def page_seat(pdf):
    fig, ax = new_page(pdf, "Etape 5 : Pose de l'assise")
    ax.text(50, 125, "Visser les 6 lattes (A) avec espacement de 5 mm", ha="center", fontsize=10, color="#666")
    # Vue de dessus
    colors = [WOOD2, WOOD1, WOOD3, WOOD2, WOOD1, WOOD3]
    total = N_SEAT * SLAT_W + (N_SEAT - 1) * SLAT_GAP
    ss = (CHAIR_W - total) / 2
    s = 0.065
    for i in range(N_SEAT):
        sx = ss + i * (SLAT_W + SLAT_GAP)
        ax.add_patch(Rectangle((14+sx*s, 85), SLAT_W*s, SEAT_D*s*0.5, fc=colors[i], ec="black", lw=0.6))
    ax.text(50, 80, "Vue de dessus - 6 lattes de 600 x 70 mm", ha="center", fontsize=9, color="#666")
    # Gap detail
    ax.add_patch(Rectangle((30, 62), 18, 6, fc=WOOD2, ec="black", lw=0.8))
    ax.add_patch(Rectangle((30, 70), 18, 6, fc=WOOD1, ec="black", lw=0.8))
    ax.annotate("", xy=(50, 70), xytext=(50, 68), arrowprops=dict(arrowstyle="<->", color="red", lw=1))
    ax.text(53, 68.5, "5 mm", fontsize=9, color="red", fontweight="bold")
    ax.text(50, 52, "Cale de 5 mm entre chaque latte  |  2 vis par intersection", ha="center", fontsize=10)
    pdf.savefig(fig); plt.close(fig)

def page_backrest(pdf):
    fig, ax = new_page(pdf, "Etape 6 : Pose du dossier")
    ax.text(50, 125, "Visser les 5 lattes (B) sur les pieds arriere", ha="center", fontsize=10, color="#666")
    s = 0.045
    x0 = 25
    y0 = 60
    t = 30
    ax.add_patch(Rectangle((x0+t*s, y0), 44*s, BACK_H*s, fc=WOOD1, ec="black", lw=1))
    ax.add_patch(Rectangle((x0+(CHAIR_W-44-t)*s, y0), 44*s, BACK_H*s, fc=WOOD1, ec="black", lw=1))
    bw = CHAIR_W - 2*(44+t)
    bx = (CHAIR_W - bw) / 2
    for i in range(N_BACK):
        bz = SEAT_H + 30 + i * (SLAT_W + SLAT_GAP)
        ax.add_patch(Rectangle((x0+bx*s, y0+bz*s), bw*s, SLAT_W*s, fc=WOOD3, ec="black", lw=0.7))
        if i == 0:
            ax.text(x0+(CHAIR_W/2)*s, y0+(bz+SLAT_W/2)*s, "B", ha="center", va="center", fontsize=9, fontweight="bold", color="white")
    ax.text(50, y0-5, "Vue arriere - 5 lattes de 480 x 70 mm  |  Angle ~110 deg", ha="center", fontsize=9, color="#666")
    ax.text(50, y0-12, "2 vis par latte et par pied = 20 vis", ha="center", fontsize=10, fontweight="bold")
    pdf.savefig(fig); plt.close(fig)

def page_armrests(pdf):
    fig, ax = new_page(pdf, "Etape 7 : Pose des accoudoirs")
    ax.text(50, 125, "Visser les accoudoirs (E) sur les pieds, a 600 mm du sol", ha="center", fontsize=10, color="#666")
    # Side view with armrest highlighted
    draw_side(ax, 15, 70, 0.06)
    ax.annotate("Accoudoir (E)\n550 x 95 mm", xy=(15+50, 70+ARMREST_H*0.06+5),
                fontsize=9, color=WOOD4, fontweight="bold")
    ax.text(50, 62, "Les accoudoirs sont les seules pieces en largeur pleine (95 mm)", ha="center", fontsize=10, color="#555")
    ax.text(50, 56, "Hauteur accoudoir : 600 mm  |  Largeur : 95 mm (confort)", ha="center", fontsize=10, fontweight="bold", color=WOOD4)
    ax.text(50, 48, "Visser par-dessous dans les pieds avant et arriere", ha="center", fontsize=9)
    pdf.savefig(fig); plt.close(fig)

def page_finishing(pdf):
    fig, ax = new_page(pdf, "Etape 8 : Finition")
    ax.text(50, 125, "Proteger et embellir votre deck chair", ha="center", fontsize=11, color="#666")
    draw_front(ax, 20, 85, 0.04)
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
    ax.text(22, 77, "Vue de cote", ha="center", fontsize=8, color="#666")
    draw_front(ax, 55, 80, 0.04)
    ax.text(68, 77, "Vue de face", ha="center", fontsize=8, color="#666")
    summary = [
        "Materiau : 1.5 euro-palettes recyclees (marquage HT)",
        f"Dimensions : {CHAIR_W} x {SEAT_D} x {BACK_H} mm",
        f"Hauteur assise : {SEAT_H} mm (table basse 450 mm)",
        "Angle dossier : ~110 degres (position detendue)",
        "Accoudoirs larges : 95 mm (poser un verre)",
        "Nombre de pieces : 22",
        "Empilable grace au retrecissement des pieds arriere",
    ]
    for i, s in enumerate(summary):
        ax.text(15, 68 - i*5, f"  {s}", fontsize=9)
    ax.text(50, 20, "Inspire de : instructables.com/A-Deck-Chair-Made-From-Pallet-Wood-Leftovers", ha="center", fontsize=8, color="#999")
    pdf.savefig(fig); plt.close(fig)

def generate_guide():
    with PdfPages(PDF_PATH) as pdf:
        page_cover(pdf)
        page_materials(pdf)
        page_dismantling(pdf)
        page_cutting(pdf)
        page_legs(pdf)
        page_side_frames(pdf)
        page_seat(pdf)
        page_backrest(pdf)
        page_armrests(pdf)
        page_finishing(pdf)
        page_final(pdf)
    print(f"Guide PDF genere : {PDF_PATH} ({os.path.getsize(PDF_PATH) // 1024} Ko)")

if __name__ == "__main__":
    generate_guide()
