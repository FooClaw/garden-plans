"""Guide de construction illustre - Chaise de jardin empilable."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_pdf import PdfPages

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(OUTPUT_DIR, "guide_construction.pdf")
WOOD1, WOOD2, WOOD3, WOOD4 = "#d2a679", "#c49a6c", "#b8956a", "#a0784e"

# Dimensions
FRONT_SPREAD = 588
BACK_SPREAD = 480
SEAT_DEPTH = 450
SEAT_HEIGHT = 370
BACK_HEIGHT = 770
LEG = 44
PLANK_T = 22
PLANK_W = 70
N_SEAT = 6
N_BACK = 4

def new_page(pdf, title, subtitle=None):
    fig, ax = plt.subplots(figsize=(8.27, 11.69))
    ax.set_xlim(0, 100); ax.set_ylim(0, 140); ax.axis("off")
    ax.text(50, 133, title, ha="center", va="top", fontsize=16, fontweight="bold")
    if subtitle:
        ax.text(50, 128, subtitle, ha="center", va="top", fontsize=11, color="#555")
    return fig, ax

def draw_chair_front(ax, x0, y0, s=0.06):
    bo = (FRONT_SPREAD - BACK_SPREAD) / 2
    ax.add_patch(Rectangle((x0, y0), LEG*s, SEAT_HEIGHT*s, fc=WOOD1, ec="black", lw=1))
    ax.add_patch(Rectangle((x0+(FRONT_SPREAD-LEG)*s, y0), LEG*s, SEAT_HEIGHT*s, fc=WOOD1, ec="black", lw=1))
    ax.add_patch(Rectangle((x0+bo*s, y0), LEG*s, BACK_HEIGHT*s, fc=WOOD1, ec="black", lw=0.7, ls="--"))
    ax.add_patch(Rectangle((x0+(bo+BACK_SPREAD-LEG)*s, y0), LEG*s, BACK_HEIGHT*s, fc=WOOD1, ec="black", lw=0.7, ls="--"))
    ax.add_patch(Rectangle((x0, y0+(SEAT_HEIGHT-PLANK_T)*s), FRONT_SPREAD*s, PLANK_T*s, fc=WOOD2, ec="black", lw=1))
    for i in range(N_BACK):
        pz = SEAT_HEIGHT + i * (PLANK_W + 5)
        ax.add_patch(Rectangle((x0+(bo+LEG)*s, y0+pz*s), (BACK_SPREAD-2*LEG)*s, PLANK_W*s, fc=WOOD3, ec="black", lw=0.5))

def draw_chair_side(ax, x0, y0, s=0.06):
    ax.add_patch(Rectangle((x0, y0), LEG*s, SEAT_HEIGHT*s, fc=WOOD1, ec="black", lw=1))
    ax.add_patch(Rectangle((x0+(SEAT_DEPTH-LEG)*s, y0), LEG*s, BACK_HEIGHT*s, fc=WOOD1, ec="black", lw=1))
    ax.add_patch(Rectangle((x0, y0+(SEAT_HEIGHT-PLANK_T)*s), SEAT_DEPTH*s, PLANK_T*s, fc=WOOD2, ec="black", lw=1))
    for i in range(N_BACK):
        pz = SEAT_HEIGHT + i * (PLANK_W + 5)
        ax.add_patch(Rectangle((x0+(SEAT_DEPTH-LEG)*s, y0+pz*s), PLANK_T*s, PLANK_W*s, fc=WOOD3, ec="black", lw=0.5))

def page_cover(pdf):
    fig, ax = new_page(pdf, "Guide de Construction", "Chaise de Jardin Empilable en Palettes Recyclees")
    ax.text(50, 123, "1 palette = 1 chaise  |  Design empilable", ha="center", fontsize=12, style="italic", color=WOOD4)
    draw_chair_front(ax, 16, 60, 0.06)
    ax.text(50, 55, f"{FRONT_SPREAD} x {SEAT_DEPTH} x {BACK_HEIGHT} mm  |  Assise {SEAT_HEIGHT} mm", ha="center", fontsize=11, color="#333")
    ax.text(50, 50, "Adaptee a la table basse palette (450 mm)", ha="center", fontsize=10, color="#666")
    ax.text(50, 15, "Inspire de : instructables.com/A-Deck-Chair-Made-From-Pallet-Wood-Leftovers", ha="center", fontsize=8, color="#999")
    pdf.savefig(fig); plt.close(fig)

def page_materials(pdf):
    fig, ax = new_page(pdf, "Materiaux et Outillage")
    ax.text(50, 125, "1 euro-palette standard (1200 x 800 mm)", ha="center", fontsize=11)
    ax.add_patch(Rectangle((30, 105), 40, 12, fc="#f0dcc0", ec="black", lw=1))
    for i in range(5):
        ax.add_patch(Rectangle((32, 106.5 + i*2, ), 36, 1.5, fc=WOOD1, ec="black", lw=0.4))
    ax.text(50, 102, "Palette marquee HT", ha="center", fontsize=9, color="green")
    tools = ["Pied-de-biche", "Arrache-clou / tenaille", "Scie circulaire + guide parallele",
             "Scie a onglet", "Ponceuse orbitale (80, 120, 180)", "Visseuse + vis 4x40 mm",
             "Serre-joints (x4)", "Colle a bois D3", "Equerre + metre"]
    ax.text(50, 92, "Outillage :", ha="center", fontsize=12, fontweight="bold")
    for i, t in enumerate(tools):
        ax.text(20, 86 - i*4.5, f"  * {t}", fontsize=10)
    pdf.savefig(fig); plt.close(fig)

def page_step_dismantling(pdf):
    fig, ax = new_page(pdf, "Etape 1 : Demontage de la palette")
    ax.add_patch(Rectangle((15, 108), 70, 3, fc=WOOD3, ec="black", lw=0.8))
    for bx in [20, 47, 74]:
        ax.add_patch(Rectangle((bx, 111), 8, 8, fc=WOOD1, ec="black", lw=0.8))
    ax.add_patch(Rectangle((15, 119), 70, 3, fc=WOOD2, ec="black", lw=0.8))
    ax.annotate("", xy=(17, 122), xytext=(10, 112), arrowprops=dict(arrowstyle="->", color="red", lw=2))
    ax.text(7, 117, "Levier", fontsize=9, color="red", rotation=50)
    ax.text(50, 100, "Pieces recuperees :", ha="center", fontsize=11, fontweight="bold")
    ax.text(15, 93, "Lattes (x7 minimum)", fontsize=9, fontweight="bold")
    for i in range(5):
        ax.add_patch(Rectangle((15, 85 + i*1.5), 30, 1.2, fc=WOOD2, ec="black", lw=0.4))
    tips = ["- Inserer le levier entre latte et bloc", "- Faire levier doucement", "- Retirer tous les clous", "- Trier par taille et etat"]
    for i, t in enumerate(tips):
        ax.text(15, 70 - i*4, t, fontsize=9)
    pdf.savefig(fig); plt.close(fig)

def page_step_cutting(pdf):
    fig, ax = new_page(pdf, "Etape 2 : Debit des pieces")
    pieces = [("A", "Latte assise x6", "500 x 70 x 22", WOOD2, 50),
              ("B", "Latte dossier x4", "436 x 70 x 22", WOOD3, 43),
              ("E", "Traverse x2", "588 x 44 x 22", WOOD3, 58),
              ("F", "Traverse lat. x2", "362 x 44 x 22", WOOD3, 36),
              ("C/D", "Pieds (2 lattes collees)", "44 x 44 mm", WOOD1, 10)]
    for i, (ref, name, dims, color, w) in enumerate(pieces):
        y = 115 - i * 10
        ax.add_patch(Rectangle((10, y), w, 3 if ref != "C/D" else 5, fc=color, ec="black", lw=0.6))
        ax.text(10 + w/2, y + 1.5, f"{ref}", ha="center", va="center", fontsize=8, fontweight="bold", color="white")
        ax.text(75, y + 1.5, f"{name} - {dims}", va="center", fontsize=9)
    ax.text(50, 55, "Refendre les lattes a 70 mm avec guide parallele", ha="center", fontsize=10, fontweight="bold", color=WOOD4)
    ax.text(50, 48, "Important : la refente a 70 mm rend la chaise plus legere\net plus elegante qu'avec des lattes pleine largeur (95 mm)", ha="center", fontsize=9, color="#555")
    pdf.savefig(fig); plt.close(fig)

def page_step_legs(pdf):
    fig, ax = new_page(pdf, "Etape 3 : Fabrication des pieds")
    ax.text(50, 125, "Coller 2 lattes face a face pour chaque pied (section 44 x 44 mm)", ha="center", fontsize=10, color="#666")
    # Before
    ax.text(20, 115, "Avant", ha="center", fontsize=10, fontweight="bold")
    ax.add_patch(Rectangle((13, 100), 14, 2.5, fc=WOOD1, ec="black", lw=0.8))
    ax.add_patch(Rectangle((13, 104), 14, 2.5, fc=WOOD2, ec="black", lw=0.8))
    # Arrow
    ax.annotate("", xy=(42, 103), xytext=(32, 103), arrowprops=dict(arrowstyle="->", color="blue", lw=2.5))
    ax.text(37, 107, "Colle D3", ha="center", fontsize=8, color="blue")
    # After
    ax.text(58, 115, "Resultat", ha="center", fontsize=10, fontweight="bold")
    ax.add_patch(Rectangle((51, 96), 5, 14, fc=WOOD1, ec="black", lw=1))
    ax.text(53.5, 103, "C\n370", ha="center", va="center", fontsize=7, fontweight="bold")
    ax.add_patch(Rectangle((62, 88), 5, 22, fc=WOOD1, ec="black", lw=1))
    ax.text(64.5, 99, "D\n770", ha="center", va="center", fontsize=7, fontweight="bold")
    ax.text(50, 82, "Pieds avant (C) : 370 mm  |  Pieds arriere (D) : 770 mm", ha="center", fontsize=10, fontweight="bold", color=WOOD4)
    ax.text(50, 76, "Serre-joints 24h de sechage, puis recouper a longueur", ha="center", fontsize=9, color="#555")
    pdf.savefig(fig); plt.close(fig)

def page_step_frame(pdf):
    fig, ax = new_page(pdf, "Etape 4 : Cadre de l'assise")
    ax.text(50, 125, "Visser les traverses E et F entre les 4 pieds", ha="center", fontsize=10, color="#666")
    s = 0.05
    y0 = 75
    bo = (FRONT_SPREAD - BACK_SPREAD) / 2
    # Front legs
    ax.add_patch(Rectangle((14, y0), LEG*s, SEAT_HEIGHT*s, fc=WOOD1, ec="black", lw=1))
    ax.add_patch(Rectangle((14+(FRONT_SPREAD-LEG)*s, y0), LEG*s, SEAT_HEIGHT*s, fc=WOOD1, ec="black", lw=1))
    # Back legs
    ax.add_patch(Rectangle((14+bo*s, y0), LEG*s, BACK_HEIGHT*s, fc=WOOD1, ec="black", lw=1))
    ax.add_patch(Rectangle((14+(bo+BACK_SPREAD-LEG)*s, y0), LEG*s, BACK_HEIGHT*s, fc=WOOD1, ec="black", lw=1))
    # Traverse E (front)
    tz = SEAT_HEIGHT - PLANK_T - 22
    ax.add_patch(Rectangle((14, y0+tz*s), FRONT_SPREAD*s, 22*s, fc=WOOD3, ec="black", lw=0.8))
    ax.text(14+FRONT_SPREAD*s/2, y0+(tz+11)*s, "E", ha="center", va="center", fontsize=8, fontweight="bold", color="white")
    # Rung G
    ax.add_patch(Rectangle((14+LEG*s, y0+120*s), (FRONT_SPREAD-2*LEG)*s, 22*s, fc=WOOD3, ec="black", lw=0.6))
    ax.text(14+FRONT_SPREAD*s/2, y0+131*s, "G", ha="center", va="center", fontsize=8, fontweight="bold", color="white")
    for sx in [14+5, 14+FRONT_SPREAD*s-5]:
        ax.plot(sx, y0+(tz+11)*s, "x", color="red", ms=5, mew=1.5)
    ax.text(50, y0-5, "Vis 4x40 mm aux intersections (marques X)", ha="center", fontsize=9, color="red")
    pdf.savefig(fig); plt.close(fig)

def page_step_seat(pdf):
    fig, ax = new_page(pdf, "Etape 5 : Pose de l'assise")
    ax.text(50, 125, "Visser les 6 lattes (A) avec espacement de 5 mm", ha="center", fontsize=10, color="#666")
    s = 0.055
    x0 = 14
    colors = [WOOD2, WOOD1, WOOD3, WOOD2, WOOD1, WOOD3]
    total = N_SEAT * PLANK_W + (N_SEAT - 1) * 5
    start = (FRONT_SPREAD - total) / 2
    for i in range(N_SEAT):
        px = start + i * (PLANK_W + 5)
        ax.add_patch(Rectangle((x0+px*s, 85), PLANK_W*s, SEAT_DEPTH*s*0.6, fc=colors[i], ec="black", lw=0.6))
        if i == 0:
            ax.text(x0+(px+PLANK_W/2)*s, 85+SEAT_DEPTH*s*0.3, "A", ha="center", va="center", fontsize=8, fontweight="bold", color="white")
    ax.text(50, 80, "Vue de dessus - 6 lattes de 500 x 70 mm", ha="center", fontsize=9, color="#666")
    # Gap detail
    ax.add_patch(Rectangle((30, 60), 15, 6, fc=WOOD2, ec="black", lw=0.8))
    ax.add_patch(Rectangle((30, 68), 15, 6, fc=WOOD1, ec="black", lw=0.8))
    ax.annotate("", xy=(47, 68), xytext=(47, 66), arrowprops=dict(arrowstyle="<->", color="red", lw=1))
    ax.text(50, 66.5, "5 mm", fontsize=9, color="red", fontweight="bold")
    ax.text(50, 50, "Utiliser une cale de 5 mm entre chaque latte", ha="center", fontsize=10, color="#555")
    pdf.savefig(fig); plt.close(fig)

def page_step_backrest(pdf):
    fig, ax = new_page(pdf, "Etape 6 : Pose du dossier")
    ax.text(50, 125, "Visser les 4 lattes (B) sur les pieds arriere", ha="center", fontsize=10, color="#666")
    s = 0.055
    x0 = 25
    bo = (FRONT_SPREAD - BACK_SPREAD) / 2
    # Back legs
    ax.add_patch(Rectangle((x0+bo*s, 60), LEG*s, BACK_HEIGHT*s, fc=WOOD1, ec="black", lw=1))
    ax.add_patch(Rectangle((x0+(bo+BACK_SPREAD-LEG)*s, 60), LEG*s, BACK_HEIGHT*s, fc=WOOD1, ec="black", lw=1))
    # Backrest planks
    for i in range(N_BACK):
        pz = SEAT_HEIGHT + i * (PLANK_W + 5)
        ax.add_patch(Rectangle((x0+(bo+LEG)*s, 60+pz*s), (BACK_SPREAD-2*LEG)*s, PLANK_W*s, fc=WOOD3, ec="black", lw=0.7))
        if i == 0:
            ax.text(x0+(bo+BACK_SPREAD/2)*s, 60+(pz+PLANK_W/2)*s, "B", ha="center", va="center", fontsize=9, fontweight="bold", color="white")
    ax.text(50, 55, "Vue arriere - 4 lattes de 436 x 70 mm", ha="center", fontsize=9, color="#666")
    ax.text(50, 48, "2 vis par latte et par pied = 16 vis", ha="center", fontsize=10, fontweight="bold")
    pdf.savefig(fig); plt.close(fig)

def page_step_finishing(pdf):
    fig, ax = new_page(pdf, "Etape 7 : Finition")
    ax.text(50, 125, "Proteger et embellir votre chaise", ha="center", fontsize=11, color="#666")
    draw_chair_side(ax, 30, 85, 0.05)
    options = [
        ("Huile de lin", "#c8a050", ["Aspect naturel", "2-3 couches", "Interieur"]),
        ("Vernis", "#e0c080", ["Protection max", "Surface lisse", "Anti-taches"]),
        ("Lasure", "#a07840", ["Exterieur", "Protection UV", "2-3 ans"]),
    ]
    for i, (name, color, details) in enumerate(options):
        x = 8 + i * 30
        ax.add_patch(Rectangle((x, 50), 26, 25, fc="#faf5ef", ec=color, lw=2))
        ax.add_patch(Rectangle((x, 69), 26, 6, fc=color, ec=color, lw=1))
        ax.text(x+13, 72, name, ha="center", va="center", fontsize=9, fontweight="bold", color="white")
        for j, d in enumerate(details):
            ax.text(x+2, 64 - j*4.5, f"- {d}", fontsize=8)
    pdf.savefig(fig); plt.close(fig)

def page_stacking(pdf):
    fig, ax = new_page(pdf, "Etape 8 : Empilage")
    ax.text(50, 125, "Votre chaise est concue pour s'empiler facilement", ha="center", fontsize=11, color="#666")
    s = 0.04
    for i in range(3):
        ox = i * ((FRONT_SPREAD - BACK_SPREAD) / 2 + 10)
        oz = i * (PLANK_T + 22 + 10)
        alpha = 0.9 - i * 0.2
        c = [WOOD1, WOOD2, WOOD4][i]
        ax.add_patch(Rectangle((10+ox*s, 70+oz*s), LEG*s, SEAT_HEIGHT*s, fc=c, ec="black", lw=0.6, alpha=alpha))
        ax.add_patch(Rectangle((10+(ox+FRONT_SPREAD-LEG)*s, 70+oz*s), LEG*s, SEAT_HEIGHT*s, fc=c, ec="black", lw=0.6, alpha=alpha))
        ax.add_patch(Rectangle((10+ox*s, 70+(oz+SEAT_HEIGHT-PLANK_T)*s), FRONT_SPREAD*s, PLANK_T*s, fc=c, ec="black", lw=0.6, alpha=alpha))
    ax.text(50, 63, "Vue de face - 3 chaises empilees", ha="center", fontsize=9, color="#666")
    ax.text(50, 55, "Principe d'empilage :", ha="center", fontsize=11, fontweight="bold")
    tips = [
        "Les pieds arriere (480 mm) passent a l'interieur des pieds avant (588 mm)",
        "Decalage lateral de 64 mm par chaise empilee",
        "Jeu de 10 mm pour faciliter l'empilage/depilage",
        "4-5 chaises empilables sans risque de basculement",
    ]
    for i, t in enumerate(tips):
        ax.text(12, 47 - i*5, f"  {t}", fontsize=9)
    pdf.savefig(fig); plt.close(fig)

def page_final(pdf):
    fig, ax = new_page(pdf, "Resultat Final")
    ax.text(50, 125, "Votre chaise de jardin en palettes est terminee !", ha="center", fontsize=11, color=WOOD4)
    draw_chair_front(ax, 5, 80, 0.05)
    ax.text(25, 77, "Vue de face", ha="center", fontsize=8, color="#666")
    draw_chair_side(ax, 55, 80, 0.05)
    ax.text(70, 77, "Vue de cote", ha="center", fontsize=8, color="#666")
    summary = [
        "Materiau : 1 euro-palette recyclee (marquage HT)",
        f"Dimensions : {FRONT_SPREAD} x {SEAT_DEPTH} x {BACK_HEIGHT} mm",
        f"Hauteur assise : {SEAT_HEIGHT} mm (table basse 450 mm)",
        "Nombre de pieces : 20",
        "Empilable : oui, 4-5 chaises",
        "Temps estime : 1 journee (hors sechage colle)",
    ]
    for i, s in enumerate(summary):
        ax.text(15, 68 - i*5, f"  {s}", fontsize=9)
    ax.text(50, 20, "Inspire de : instructables.com/A-Deck-Chair-Made-From-Pallet-Wood-Leftovers", ha="center", fontsize=8, color="#999")
    pdf.savefig(fig); plt.close(fig)

def generate_guide():
    with PdfPages(PDF_PATH) as pdf:
        page_cover(pdf)
        page_materials(pdf)
        page_step_dismantling(pdf)
        page_step_cutting(pdf)
        page_step_legs(pdf)
        page_step_frame(pdf)
        page_step_seat(pdf)
        page_step_backrest(pdf)
        page_step_finishing(pdf)
        page_stacking(pdf)
        page_final(pdf)
    print(f"Guide PDF genere : {PDF_PATH} ({os.path.getsize(PDF_PATH) // 1024} Ko)")

if __name__ == "__main__":
    generate_guide()
