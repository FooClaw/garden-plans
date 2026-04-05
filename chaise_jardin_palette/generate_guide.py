"""Guide de construction illustre - Deck Chair de jardin en palettes.

Design minimaliste fidele au modele Instructables : assise tres basse,
dossier incline, pas d'accoudoirs, longerons depassant a l'arriere.
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

# Dimensions (coherentes avec generate_table.py)
CHAIR_W = 600
SLAT_W = 95; SLAT_T = 22; SLAT_GAP = 6
FRAME_W = 44; FRAME_D = 70
SEAT_H = 250; N_SEAT = 5; N_BACK = 4
SEAT_DEPTH = N_SEAT * SLAT_W + (N_SEAT - 1) * SLAT_GAP  # ~499
RUNNER_EXTEND = 200; RUNNER_L = SEAT_DEPTH + RUNNER_EXTEND
BACKREST_TILT = 25; BACK_LENGTH = 500
INNER_W = CHAIR_W - 2 * FRAME_W
BACK_DY = BACK_LENGTH * math.sin(math.radians(BACKREST_TILT))
BACK_DZ = BACK_LENGTH * math.cos(math.radians(BACKREST_TILT))
TOTAL_H = SEAT_H + BACK_DZ

def new_page(pdf, title, subtitle=None):
    fig, ax = plt.subplots(figsize=(8.27, 11.69))
    ax.set_xlim(0, 100); ax.set_ylim(0, 140); ax.axis("off")
    ax.text(50, 133, title, ha="center", va="top", fontsize=16, fontweight="bold")
    if subtitle:
        ax.text(50, 128, subtitle, ha="center", va="top", fontsize=11, color="#555")
    return fig, ax

def draw_side(ax, x0, y0, s=0.05):
    """Vue de cote simplifiee."""
    # Longeron (au sol)
    ax.add_patch(Rectangle((x0, y0), RUNNER_L*s, FRAME_W*s,
                            fc=WOOD1, ec="black", lw=1))
    # Pied avant
    ax.add_patch(Rectangle((x0, y0+FRAME_W*s), FRAME_D*s,
                            (SEAT_H-FRAME_W)*s, fc=WOOD1, ec="black", lw=1))
    # Support dossier (incline)
    by0 = (SEAT_DEPTH - FRAME_D) * s
    pts = [
        [x0+by0, y0+SEAT_H*s],
        [x0+by0+FRAME_D*s, y0+SEAT_H*s],
        [x0+by0+FRAME_D*s+BACK_DY*s, y0+(SEAT_H+BACK_DZ)*s],
        [x0+by0+BACK_DY*s, y0+(SEAT_H+BACK_DZ)*s],
    ]
    ax.add_patch(Polygon(pts, closed=True, fc=WOOD1, ec="black", lw=1))
    # Assise (simplifie)
    ax.add_patch(Rectangle((x0, y0+(SEAT_H-SLAT_T)*s),
                            SEAT_DEPTH*s, SLAT_T*s, fc=WOOD2, ec="black", lw=0.8))
    # Dossier lattes
    for i in range(N_BACK):
        frac = (i + 0.5) / N_BACK
        bz = SEAT_H + frac * BACK_DZ
        by = (SEAT_DEPTH - FRAME_D) + frac * BACK_DY
        ax.add_patch(Rectangle((x0+by*s, y0+bz*s), SLAT_T*s, SLAT_W*s,
                                fc=WOOD3, ec="black", lw=0.5))

def draw_front(ax, x0, y0, s=0.05):
    """Vue de face simplifiee."""
    # Pieds avant
    ax.add_patch(Rectangle((x0, y0), FRAME_W*s, SEAT_H*s,
                            fc=WOOD1, ec="black", lw=1))
    ax.add_patch(Rectangle((x0+(CHAIR_W-FRAME_W)*s, y0), FRAME_W*s,
                            SEAT_H*s, fc=WOOD1, ec="black", lw=1))
    # Supports dossier (pointilles)
    ax.add_patch(Rectangle((x0, y0+SEAT_H*s), FRAME_W*s, BACK_DZ*s,
                            fc=WOOD1, ec="black", lw=0.6, ls="--", alpha=0.5))
    ax.add_patch(Rectangle((x0+(CHAIR_W-FRAME_W)*s, y0+SEAT_H*s),
                            FRAME_W*s, BACK_DZ*s,
                            fc=WOOD1, ec="black", lw=0.6, ls="--", alpha=0.5))
    # Assise
    ax.add_patch(Rectangle((x0, y0+(SEAT_H-SLAT_T)*s), CHAIR_W*s,
                            SLAT_T*s, fc=WOOD2, ec="black", lw=1))

def page_cover(pdf):
    fig, ax = new_page(pdf, "Guide de Construction",
                       "Deck Chair de Jardin en Palettes Recyclees")
    ax.text(50, 123, "Design minimaliste - assise basse, dossier incline, sans accoudoirs",
            ha="center", fontsize=11, style="italic", color=WOOD4)
    draw_side(ax, 18, 60, 0.06)
    ax.text(50, 55, (f"{CHAIR_W} x {RUNNER_L:.0f} x {TOTAL_H:.0f} mm  |  "
                     f"Assise {SEAT_H} mm  |  Dossier ~{90+BACKREST_TILT} deg"),
            ha="center", fontsize=10, color="#333")
    ax.text(50, 50, "Adaptee a la table basse palette (450 mm)",
            ha="center", fontsize=10, color="#666")
    ax.text(50, 15, "Inspire de : instructables.com/A-Deck-Chair-Made-From-Pallet-Wood-Leftovers",
            ha="center", fontsize=8, color="#999")
    pdf.savefig(fig); plt.close(fig)

def page_materials(pdf):
    fig, ax = new_page(pdf, "Materiaux et Outillage")
    ax.text(50, 125, "1 euro-palette standard (1200 x 800 mm)",
            ha="center", fontsize=11)
    ax.add_patch(Rectangle((30, 105), 40, 12, fc="#f0dcc0", ec="black", lw=1))
    for i in range(5):
        ax.add_patch(Rectangle((31, 106.5+i*2), 38, 1.5,
                                fc=WOOD1, ec="black", lw=0.4))
    ax.text(50, 102, "1 palette suffit (17 pieces)",
            ha="center", fontsize=8)
    ax.text(50, 96, "Choisir une palette marquee HT",
            ha="center", fontsize=9, color="green")
    tools = [
        "Pied-de-biche / levier",
        "Arrache-clou / tenaille",
        "Scie circulaire + guide parallele",
        "Scie a onglet",
        "Ponceuse orbitale (80, 120, 180)",
        "Visseuse + vis a bois 4x50 mm",
        "Serre-joints (x4)",
        "Colle a bois D3",
        "Fausse equerre (angle ~115 deg)",
    ]
    ax.text(50, 86, "Outillage :", ha="center", fontsize=12, fontweight="bold")
    for i, t in enumerate(tools):
        ax.text(20, 80 - i*4.5, f"  * {t}", fontsize=10)
    pdf.savefig(fig); plt.close(fig)

def page_dismantling(pdf):
    fig, ax = new_page(pdf, "Etape 1 : Demontage de la palette")
    # Palette schematique
    ax.add_patch(Rectangle((15, 108), 70, 3, fc=WOOD3, ec="black", lw=0.8))
    for bx in [20, 47, 74]:
        ax.add_patch(Rectangle((bx, 111), 8, 8, fc=WOOD1, ec="black", lw=0.8))
    ax.add_patch(Rectangle((15, 119), 70, 3, fc=WOOD2, ec="black", lw=0.8))
    ax.annotate("", xy=(17, 122), xytext=(10, 112),
                arrowprops=dict(arrowstyle="->", color="red", lw=2))
    ax.text(7, 117, "Levier", fontsize=9, color="red", rotation=50)
    ax.text(50, 100, "Pieces a recuperer :", ha="center", fontsize=11,
            fontweight="bold")
    ax.text(15, 93, "Au moins 8 lattes longues (1200 mm)", fontsize=9)
    ax.text(15, 88, "Toutes les lattes restent en pleine largeur (95 mm)",
            fontsize=9, color=WOOD4, fontweight="bold")
    tips = [
        "- Levier doucement pour ne pas casser les lattes",
        "- Retirer tous les clous a la tenaille",
        "- Garder les plus belles lattes pour l'assise",
        "- Pas besoin de refendre : on garde la largeur 95 mm",
    ]
    for i, t in enumerate(tips):
        ax.text(15, 75 - i*5, t, fontsize=9)
    pdf.savefig(fig); plt.close(fig)

def page_cutting(pdf):
    fig, ax = new_page(pdf, "Etape 2 : Debit des pieces")
    pieces = [
        ("A", "Latte assise x5", "600 x 95 x 22", WOOD2, 60),
        ("B", "Latte dossier x4", f"{INNER_W:.0f} x 95 x 22", WOOD3, 52),
        ("D", "Longeron lateral x2", f"{RUNNER_L:.0f} x 70 x 44", WOOD1, 70),
        ("E", "Support dossier x2", "500 x 70 x 44", WOOD1, 50),
        ("C", "Pied avant x2", f"44 x 70 x {SEAT_H:.0f}", WOOD1, 8),
        ("F", "Traverse avant", f"{INNER_W:.0f} x 44 x 22", WOOD3, 52),
        ("G", "Traverse arriere", f"{INNER_W:.0f} x 22 x 22", WOOD3, 52),
    ]
    for i, (ref, name, dims, color, w) in enumerate(pieces):
        y = 118 - i * 11
        h = 3 if "Pied" not in name and "Longeron" not in name else 6
        ax.add_patch(Rectangle((10, y), w*0.7, h, fc=color, ec="black", lw=0.6))
        ax.text(10 + w*0.7/2, y + h/2, ref, ha="center", va="center",
                fontsize=8, fontweight="bold", color="white")
        ax.text(60, y + h/2, f"{name}\n{dims} mm", va="center", fontsize=8)
    ax.text(50, 35, "Les lattes gardent leur pleine largeur (95 mm)",
            ha="center", fontsize=10, fontweight="bold", color=WOOD4)
    ax.text(50, 29, "Pieds et longerons : 2 lattes collees (section 44 x 70)",
            ha="center", fontsize=9, color="#555")
    pdf.savefig(fig); plt.close(fig)

def page_legs(pdf):
    fig, ax = new_page(pdf, "Etape 3 : Fabrication des pieces doublees")
    ax.text(50, 125, "Coller 2 lattes face a face pour pieds, longerons et supports",
            ha="center", fontsize=10, color="#666")
    # Pied avant
    ax.text(25, 115, "Pied avant (C)", ha="center", fontsize=10, fontweight="bold")
    ax.add_patch(Rectangle((18, 104), 14, 2, fc=WOOD1, ec="black", lw=0.8))
    ax.add_patch(Rectangle((18, 107), 14, 2, fc=WOOD2, ec="black", lw=0.8))
    ax.annotate("", xy=(38, 106), xytext=(35, 106),
                arrowprops=dict(arrowstyle="->", color="blue", lw=2))
    ax.add_patch(Rectangle((40, 101), 5, 8, fc=WOOD1, ec="black", lw=1))
    ax.text(42.5, 105, f"{SEAT_H:.0f}\nmm", ha="center", va="center",
            fontsize=7, fontweight="bold")

    # Longeron
    ax.text(25, 92, "Longeron (D)", ha="center", fontsize=10, fontweight="bold")
    ax.add_patch(Rectangle((10, 82), 30, 2, fc=WOOD1, ec="black", lw=0.8))
    ax.add_patch(Rectangle((10, 85), 30, 2, fc=WOOD2, ec="black", lw=0.8))
    ax.annotate("", xy=(45, 84), xytext=(42, 84),
                arrowprops=dict(arrowstyle="->", color="blue", lw=2))
    ax.add_patch(Rectangle((48, 81), 30, 5, fc=WOOD1, ec="black", lw=1))
    ax.text(63, 83.5, f"{RUNNER_L:.0f} mm", ha="center", va="center",
            fontsize=7, fontweight="bold")

    # Support dossier
    ax.text(25, 72, "Support dossier (E)", ha="center", fontsize=10, fontweight="bold")
    ax.add_patch(Rectangle((14, 62), 22, 2, fc=WOOD1, ec="black", lw=0.8))
    ax.add_patch(Rectangle((14, 65), 22, 2, fc=WOOD2, ec="black", lw=0.8))
    ax.annotate("", xy=(42, 64), xytext=(39, 64),
                arrowprops=dict(arrowstyle="->", color="blue", lw=2))
    ax.add_patch(Rectangle((45, 61), 22, 5, fc=WOOD1, ec="black", lw=1))
    ax.text(56, 63.5, "500 mm", ha="center", va="center",
            fontsize=7, fontweight="bold")

    ax.text(50, 52, "Section finale : 44 x 70 mm  |  Colle D3 + serre-joints 24h",
            ha="center", fontsize=10, fontweight="bold", color=WOOD4)
    pdf.savefig(fig); plt.close(fig)

def page_side_frames(pdf):
    fig, ax = new_page(pdf, "Etape 4 : Cadres lateraux")
    ax.text(50, 125, "Assembler 2 cadres : longeron + pied avant + support dossier",
            ha="center", fontsize=10, color="#666")
    s = 0.055
    x0 = 10; y0 = 65
    # Longeron
    ax.add_patch(Rectangle((x0, y0), RUNNER_L*s, FRAME_W*s,
                            fc=WOOD1, ec="black", lw=1.2))
    ax.text(x0+RUNNER_L*s/2, y0+FRAME_W*s/2, "D", ha="center", va="center",
            fontsize=9, fontweight="bold")
    # Pied avant
    ax.add_patch(Rectangle((x0, y0+FRAME_W*s), FRAME_D*s, (SEAT_H-FRAME_W)*s,
                            fc=WOOD2, ec="black", lw=1))
    ax.text(x0+FRAME_D*s/2, y0+(SEAT_H/2)*s, "C", ha="center", va="center",
            fontsize=9, fontweight="bold")
    # Support dossier (incline)
    by0 = (SEAT_DEPTH - FRAME_D) * s
    pts = [
        [x0+by0, y0+SEAT_H*s],
        [x0+by0+FRAME_D*s, y0+SEAT_H*s],
        [x0+by0+FRAME_D*s+BACK_DY*s, y0+(SEAT_H+BACK_DZ)*s],
        [x0+by0+BACK_DY*s, y0+(SEAT_H+BACK_DZ)*s],
    ]
    ax.add_patch(Polygon(pts, closed=True, fc=WOOD3, ec="black", lw=1.2))
    ax.text(x0+by0+FRAME_D*s/2+BACK_DY*s/2, y0+(SEAT_H+BACK_DZ/2)*s,
            "E", ha="center", va="center", fontsize=9, fontweight="bold", color="white")
    # Vis
    ax.plot(x0+FRAME_D*s/2, y0+SEAT_H*s, "x", color="red", ms=8, mew=2)
    ax.plot(x0+by0+FRAME_D*s/2, y0+SEAT_H*s, "x", color="red", ms=8, mew=2)
    ax.text(50, y0-5, "Vis 4x50 aux jonctions  |  Repeter x2 (gauche + droite)",
            ha="center", fontsize=9, color="red")
    ax.text(50, y0-12, "Le support dossier (E) s'appuie sur le longeron (D) a l'arriere",
            ha="center", fontsize=9, color="#555")
    pdf.savefig(fig); plt.close(fig)

def page_traverses(pdf):
    fig, ax = new_page(pdf, "Etape 5 : Traverses")
    ax.text(50, 125, "Relier les 2 cadres lateraux avec les traverses",
            ha="center", fontsize=10, color="#666")
    # Vue de face simplifiee
    s = 0.04
    x0 = 15; y0 = 80
    # Cadres lateraux
    ax.add_patch(Rectangle((x0, y0), FRAME_W*s, SEAT_H*s,
                            fc=WOOD1, ec="black", lw=1))
    ax.add_patch(Rectangle((x0+(CHAIR_W-FRAME_W)*s, y0), FRAME_W*s,
                            SEAT_H*s, fc=WOOD1, ec="black", lw=1))
    # Traverse avant (F)
    tz = SEAT_H - SLAT_T - FRAME_W
    ax.add_patch(Rectangle((x0+FRAME_W*s, y0+tz*s), INNER_W*s, FRAME_W*s,
                            fc=WOOD3, ec="black", lw=1))
    ax.text(x0+CHAIR_W*s/2, y0+(tz+FRAME_W/2)*s, "F", ha="center",
            va="center", fontsize=10, fontweight="bold", color="white")
    # Traverse basse arriere (G)
    ax.add_patch(Rectangle((x0+FRAME_W*s, y0+SLAT_T*s), INNER_W*s, SLAT_T*s,
                            fc=WOOD3, ec="black", lw=0.8))
    ax.text(x0+CHAIR_W*s/2, y0+SLAT_T*1.5*s, "G", ha="center",
            va="center", fontsize=9, fontweight="bold", color="white")
    ax.text(50, y0-5, "F : traverse avant sous l'assise  |  G : traverse basse arriere",
            ha="center", fontsize=9, color="#555")
    ax.text(50, y0-12, "2 vis par extremite  |  Le cadre est maintenant rigide",
            ha="center", fontsize=10, fontweight="bold", color=WOOD4)
    pdf.savefig(fig); plt.close(fig)

def page_seat(pdf):
    fig, ax = new_page(pdf, "Etape 6 : Pose de l'assise")
    ax.text(50, 125, "Visser les 5 lattes (A) avec espacement regulier",
            ha="center", fontsize=10, color="#666")
    # Vue de dessus
    colors = [WOOD2, WOOD1, WOOD3, WOOD2, WOOD1]
    s = 0.06
    for i in range(N_SEAT):
        sy = i * (SLAT_W + SLAT_GAP)
        ax.add_patch(Rectangle((15, 85+sy*s), CHAIR_W*s, SLAT_W*s,
                                fc=colors[i], ec="black", lw=0.6))
        if i == 0:
            ax.text(15+CHAIR_W*s/2, 85+sy*s+SLAT_W*s/2, "A",
                    ha="center", va="center", fontsize=10, fontweight="bold")
    ax.text(50, 80, "Vue de dessus - 5 lattes de 600 x 95 mm",
            ha="center", fontsize=9, color="#666")
    # Gap detail
    ax.add_patch(Rectangle((30, 62), 18, 6, fc=WOOD2, ec="black", lw=0.8))
    ax.add_patch(Rectangle((30, 70), 18, 6, fc=WOOD1, ec="black", lw=0.8))
    ax.annotate("", xy=(50, 70), xytext=(50, 68),
                arrowprops=dict(arrowstyle="<->", color="red", lw=1))
    ax.text(53, 68.5, f"{SLAT_GAP} mm", fontsize=9, color="red", fontweight="bold")
    ax.text(50, 52, f"Cale de {SLAT_GAP} mm entre chaque latte  |  2 vis par cote",
            ha="center", fontsize=10)
    pdf.savefig(fig); plt.close(fig)

def page_backrest(pdf):
    fig, ax = new_page(pdf, "Etape 7 : Pose du dossier")
    ax.text(50, 125, "Visser les 4 lattes (B) sur les supports dossier",
            ha="center", fontsize=10, color="#666")
    s = 0.04
    x0 = 20; y0 = 60
    # Supports dossier (vue de face)
    ax.add_patch(Rectangle((x0, y0+SEAT_H*s), FRAME_W*s, BACK_DZ*s,
                            fc=WOOD1, ec="black", lw=1))
    ax.add_patch(Rectangle((x0+(CHAIR_W-FRAME_W)*s, y0+SEAT_H*s),
                            FRAME_W*s, BACK_DZ*s,
                            fc=WOOD1, ec="black", lw=1))
    # Lattes dossier
    for i in range(N_BACK):
        frac = (i + 0.5) / N_BACK
        bz = SEAT_H + frac * BACK_DZ
        ax.add_patch(Rectangle((x0+FRAME_W*s, y0+bz*s), INNER_W*s, SLAT_W*s,
                                fc=WOOD3, ec="black", lw=0.7))
        if i == 0:
            ax.text(x0+CHAIR_W*s/2, y0+(bz+SLAT_W/2)*s, "B",
                    ha="center", va="center", fontsize=10, fontweight="bold",
                    color="white")
    ax.text(50, y0-5, f"Vue arriere - 4 lattes de {INNER_W:.0f} x 95 mm",
            ha="center", fontsize=9, color="#666")
    ax.text(50, y0-12, "2 vis par latte et par support = 16 vis",
            ha="center", fontsize=10, fontweight="bold")
    pdf.savefig(fig); plt.close(fig)

def page_finishing(pdf):
    fig, ax = new_page(pdf, "Etape 8 : Finition")
    ax.text(50, 125, "Proteger et embellir votre deck chair",
            ha="center", fontsize=11, color="#666")
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
        ax.text(x+13, 72, name, ha="center", va="center", fontsize=9,
                fontweight="bold", color="white")
        for j, d in enumerate(details):
            ax.text(x+2, 64 - j*4.5, f"- {d}", fontsize=8)
    pdf.savefig(fig); plt.close(fig)

def page_final(pdf):
    fig, ax = new_page(pdf, "Resultat Final")
    ax.text(50, 125, "Votre deck chair en palettes est terminee !",
            ha="center", fontsize=11, color=WOOD4)
    draw_side(ax, 5, 80, 0.05)
    ax.text(25, 77, "Vue de cote", ha="center", fontsize=8, color="#666")
    draw_front(ax, 55, 80, 0.04)
    ax.text(68, 77, "Vue de face", ha="center", fontsize=8, color="#666")
    summary = [
        "Materiau : 1 euro-palette recyclee (marquage HT)",
        f"Dimensions : {CHAIR_W} x {RUNNER_L:.0f} x {TOTAL_H:.0f} mm",
        f"Hauteur assise : {SEAT_H} mm (table basse 450 mm)",
        f"Angle dossier : ~{90+BACKREST_TILT} degres (position detendue)",
        "Design minimaliste sans accoudoirs",
        "Nombre de pieces : 17",
        f"Longerons depassent de {RUNNER_EXTEND} mm a l'arriere (stabilite)",
    ]
    for i, line in enumerate(summary):
        ax.text(15, 68 - i*5, f"  {line}", fontsize=9)
    ax.text(50, 20, "Inspire de : instructables.com/A-Deck-Chair-Made-From-Pallet-Wood-Leftovers",
            ha="center", fontsize=8, color="#999")
    pdf.savefig(fig); plt.close(fig)

def generate_guide():
    with PdfPages(PDF_PATH) as pdf:
        page_cover(pdf)
        page_materials(pdf)
        page_dismantling(pdf)
        page_cutting(pdf)
        page_legs(pdf)
        page_side_frames(pdf)
        page_traverses(pdf)
        page_seat(pdf)
        page_backrest(pdf)
        page_finishing(pdf)
        page_final(pdf)
    print(f"Guide PDF genere : {PDF_PATH} ({os.path.getsize(PDF_PATH) // 1024} Ko)")

if __name__ == "__main__":
    generate_guide()
