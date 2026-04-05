"""Generateur de nomenclature PDF - Chaise de jardin empilable."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_pdf import PdfPages

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(OUTPUT_DIR, "nomenclature.pdf")
WOOD1, WOOD2, WOOD3, WOOD4 = "#d2a679", "#c49a6c", "#b8956a", "#a0784e"

PIECES = [
    ("A", "Latte assise", 6, "500 x 70 x 22", "Lattes refendues", WOOD2),
    ("B", "Latte dossier", 4, "436 x 70 x 22", "Lattes refendues", WOOD3),
    ("C", "Pied avant", 2, "44 x 44 x 370", "2 lattes collees", WOOD1),
    ("D", "Pied arriere", 2, "44 x 44 x 770", "2 lattes collees", WOOD1),
    ("E", "Traverse avant/arriere", 2, "588 x 44 x 22", "Lattes recoupees", WOOD3),
    ("F", "Traverse laterale", 2, "362 x 44 x 22", "Lattes recoupees", WOOD3),
    ("G", "Traverse basse avant", 1, "500 x 22 x 22", "Latte refendue", WOOD3),
    ("H", "Traverse basse arriere", 1, "372 x 22 x 22", "Latte refendue", WOOD3),
]

TOOLS = [
    ("Pied-de-biche / levier", "Demontage des lattes"),
    ("Arrache-clou / tenaille", "Retrait des clous"),
    ("Scie circulaire (guide parallele)", "Refente a 70 mm et 44 mm"),
    ("Scie a onglet", "Decoupe a longueur"),
    ("Ponceuse orbitale", "Poncage (grains 80, 120, 180)"),
    ("Visseuse + vis a bois (4x40 mm)", "Assemblage"),
    ("Serre-joints (x4 min.)", "Collage des pieds"),
    ("Colle a bois D3", "Collage pieds"),
    ("Equerre de menuisier", "Verification des angles"),
]

ASSEMBLY = [
    ("Demontage", "Demonter la palette, trier les pieces"),
    ("Debit", "Decouper et refendre toutes les pieces"),
    ("Poncage", "Poncer toutes les pieces (grains 80, 120, 180)"),
    ("Pieds", "Coller les lattes par 2 pour les pieds (24h)"),
    ("Cadre assise", "Visser traverses E et F entre les 4 pieds"),
    ("Traverses basses", "Visser G et H entre les pieds (120 mm du sol)"),
    ("Assise", "Visser les 6 lattes A sur le cadre (gap 5 mm)"),
    ("Dossier", "Visser les 4 lattes B sur les pieds arriere"),
    ("Finition", "Huile de lin, vernis ou lasure"),
]

def new_page(pdf, title, subtitle=None):
    fig, ax = plt.subplots(figsize=(8.27, 11.69))
    ax.set_xlim(0, 100); ax.set_ylim(0, 140); ax.axis("off")
    ax.text(50, 135, title, ha="center", va="top", fontsize=16, fontweight="bold")
    if subtitle:
        ax.text(50, 130, subtitle, ha="center", va="top", fontsize=11, color="#555")
    return fig, ax

def page_cover(pdf):
    fig, ax = new_page(pdf, "Nomenclature", "Chaise de Jardin Empilable en Palettes Recyclees")
    ax.text(50, 122, "Liste de debit et instructions d'assemblage", ha="center", fontsize=12, style="italic", color=WOOD4)
    ax.add_patch(Rectangle((15, 85), 70, 30, fc="#faf5ef", ec=WOOD4, lw=1.5))
    summary = [
        ("Materiau", "1 euro-palette standard (1200 x 800 mm)"),
        ("Dimensions chaise", "588 x 450 x 770 mm (L x P x H)"),
        ("Hauteur assise", "370 mm (adaptee table basse 450 mm)"),
        ("Nombre de pieces", "20 pieces (8 references)"),
        ("Empilable", "Oui, 4-5 chaises"),
    ]
    for i, (label, value) in enumerate(summary):
        y = 110 - i * 5
        ax.text(20, y, f"{label} :", fontsize=10, fontweight="bold", color=WOOD4)
        ax.text(52, y, value, fontsize=10)
    pdf.savefig(fig); plt.close(fig)

def page_bom(pdf):
    fig, ax = new_page(pdf, "Recapitulatif des pieces")
    headers = [("Ref", 8), ("Piece", 25), ("Qte", 50), ("Dimensions", 62), ("Origine", 85)]
    ax.add_patch(Rectangle((5, 120), 90, 7, fc=WOOD4, ec="black", lw=0.8))
    for label, x in headers:
        ax.text(x, 123.5, label, fontsize=9, fontweight="bold", color="white")
    for i, (ref, name, qty, dims, origin, color) in enumerate(PIECES):
        y = 113 - i * 7
        bg = "#faf5ef" if i % 2 == 0 else "#f0e8dc"
        ax.add_patch(Rectangle((5, y), 90, 6, fc=bg, ec="#ccc", lw=0.5))
        ax.add_patch(Rectangle((6, y + 0.5), 4, 5, fc=color, ec="black", lw=0.5))
        ax.text(8, y + 3, ref, ha="center", va="center", fontsize=9, fontweight="bold")
        ax.text(15, y + 3, name, va="center", fontsize=8.5)
        ax.text(52, y + 3, str(qty), ha="center", va="center", fontsize=10, fontweight="bold")
        ax.text(57, y + 3, dims, va="center", fontsize=8)
        ax.text(82, y + 3, origin, va="center", fontsize=7.5)
    ax.text(50, 48, "Total : 20 pieces a partir de 1 euro-palette", ha="center", fontsize=11, fontweight="bold", color=WOOD4)
    pdf.savefig(fig); plt.close(fig)

def page_tools(pdf):
    fig, ax = new_page(pdf, "Outillage necessaire")
    ax.add_patch(Rectangle((5, 117), 90, 7, fc=WOOD4, ec="black", lw=0.8))
    ax.text(10, 120.5, "Outil", fontsize=10, fontweight="bold", color="white")
    ax.text(60, 120.5, "Usage", fontsize=10, fontweight="bold", color="white")
    for i, (tool, usage) in enumerate(TOOLS):
        y = 110 - i * 7
        bg = "#faf5ef" if i % 2 == 0 else "#f0e8dc"
        ax.add_patch(Rectangle((5, y), 90, 6, fc=bg, ec="#ccc", lw=0.5))
        ax.text(8, y + 3, tool, va="center", fontsize=9, fontweight="bold")
        ax.text(55, y + 3, usage, va="center", fontsize=9, color="#555")
    pdf.savefig(fig); plt.close(fig)

def page_assembly(pdf):
    fig, ax = new_page(pdf, "Ordre d'assemblage")
    for i, (title, desc) in enumerate(ASSEMBLY):
        y = 120 - i * 10
        ax.add_patch(plt.Circle((10, y + 2), 3, fc=WOOD4, ec="black", lw=0.5, zorder=3))
        ax.text(10, y + 2, str(i + 1), ha="center", va="center", fontsize=10, fontweight="bold", color="white", zorder=4)
        ax.add_patch(Rectangle((16, y - 1.5), 78, 8, fc="#faf5ef", ec="#e0d5c5", lw=0.8))
        ax.text(19, y + 3.5, title, fontsize=10, fontweight="bold", color=WOOD4)
        ax.text(19, y + 0.2, desc, fontsize=9, color="#555")
    pdf.savefig(fig); plt.close(fig)

def page_stacking(pdf):
    fig, ax = new_page(pdf, "Empilabilite")
    ax.text(50, 125, "Les chaises s'empilent grace au retrecissement des pieds arriere", ha="center", fontsize=10, color="#666")
    # Draw 3 stacked chairs from front
    s = 0.35
    front_w, back_w = 588, 480
    seat_h, back_h = 370, 770
    leg = 44
    for i in range(3):
        ox = i * ((front_w - back_w) / 2 + 10)
        oz = i * (22 + 22 + 10)
        alpha = 0.9 - i * 0.2
        c = [WOOD1, WOOD2, WOOD4][i]
        # front legs
        ax.add_patch(Rectangle((10 + ox * s, 50 + oz * s), leg * s, seat_h * s, fc=c, ec="black", lw=0.7, alpha=alpha))
        ax.add_patch(Rectangle((10 + (ox + front_w - leg) * s, 50 + oz * s), leg * s, seat_h * s, fc=c, ec="black", lw=0.7, alpha=alpha))
        # seat
        ax.add_patch(Rectangle((10 + ox * s, 50 + (oz + seat_h - 22) * s), front_w * s, 22 * s, fc=c, ec="black", lw=0.7, alpha=alpha))
    ax.text(50, 43, "Vue de face - 3 chaises empilees", ha="center", fontsize=9, color="#666")
    tips = [
        "Pieds avant : 588 mm d'ecart (largeur totale)",
        "Pieds arriere : 480 mm d'ecart (retreci)",
        "Jeu d'empilage : 10 mm entre chaises",
        "Capacite : 4-5 chaises empilees",
    ]
    for i, t in enumerate(tips):
        ax.text(15, 35 - i * 5, f"  {t}", fontsize=10)
    pdf.savefig(fig); plt.close(fig)

def generate_nomenclature():
    with PdfPages(PDF_PATH) as pdf:
        page_cover(pdf)
        page_bom(pdf)
        page_tools(pdf)
        page_assembly(pdf)
        page_stacking(pdf)
    print(f"Nomenclature PDF generee : {PDF_PATH} ({os.path.getsize(PDF_PATH) // 1024} Ko)")

if __name__ == "__main__":
    generate_nomenclature()
