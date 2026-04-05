"""Generateur de nomenclature PDF - Deck Chair de jardin."""
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
    ("A", "Latte assise", 6, "600 x 70 x 22", "Lattes refendues", WOOD2),
    ("B", "Latte dossier", 5, "480 x 70 x 22", "Lattes refendues", WOOD3),
    ("C", "Pied avant", 2, "44 x 70 x 350", "2 lattes collees", WOOD1),
    ("D", "Pied arriere", 2, "44 x 70 x 900", "2 lattes collees", WOOD1),
    ("E", "Accoudoir", 2, "550 x 95 x 22", "Lattes pleine larg.", WOOD2),
    ("F", "Traverse avant", 1, "512 x 44 x 22", "Latte recoupee", WOOD3),
    ("G", "Traverse arriere", 1, "452 x 44 x 22", "Latte recoupee", WOOD3),
    ("H", "Traverse laterale", 2, "340 x 44 x 22", "Lattes recoupees", WOOD3),
    ("I", "Traverse basse", 1, "512 x 22 x 22", "Latte refendue", WOOD3),
]

TOOLS = [
    ("Pied-de-biche / levier", "Demontage des lattes"),
    ("Arrache-clou / tenaille", "Retrait des clous"),
    ("Scie circulaire + guide", "Refente a 70 et 44 mm"),
    ("Scie a onglet", "Decoupe a longueur"),
    ("Ponceuse orbitale", "Poncage (80, 120, 180)"),
    ("Visseuse + vis 4x50 mm", "Assemblage"),
    ("Serre-joints (x4)", "Collage des pieds"),
    ("Colle a bois D3", "Collage pieds"),
    ("Fausse equerre", "Angle dossier ~110 deg"),
]

ASSEMBLY = [
    ("Demontage", "Demonter 1.5 palettes, trier les pieces"),
    ("Debit", "Decouper et refendre toutes les pieces"),
    ("Poncage", "Poncer toutes les pieces (grains 80, 120, 180)"),
    ("Pieds", "Coller les lattes par 2 pour les pieds (24h)"),
    ("Cadres lateraux", "Pied avant + pied arriere + traverse H (x2)"),
    ("Traverses", "Visser traverses F, G et basse I"),
    ("Assise", "Visser 6 lattes A (espacement 5 mm)"),
    ("Dossier", "Visser 5 lattes B sur pieds arriere (5 mm)"),
    ("Accoudoirs", "Visser accoudoirs E sur les pieds"),
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
    fig, ax = new_page(pdf, "Nomenclature", "Deck Chair de Jardin en Palettes Recyclees")
    ax.text(50, 122, "Style Adirondack - assise basse, dossier recline, accoudoirs", ha="center", fontsize=11, style="italic", color=WOOD4)
    ax.add_patch(Rectangle((15, 85), 70, 30, fc="#faf5ef", ec=WOOD4, lw=1.5))
    summary = [
        ("Materiau", "1.5 euro-palettes standard"),
        ("Dimensions", "600 x 480 x 900 mm (L x P x H)"),
        ("Assise", "350 mm (adaptee table basse 450 mm)"),
        ("Dossier", "Recline a ~110 degres"),
        ("Pieces", "22 pieces (9 references)"),
    ]
    for i, (label, value) in enumerate(summary):
        y = 110 - i * 5
        ax.text(20, y, f"{label} :", fontsize=10, fontweight="bold", color=WOOD4)
        ax.text(48, y, value, fontsize=10)
    pdf.savefig(fig); plt.close(fig)

def page_bom(pdf):
    fig, ax = new_page(pdf, "Recapitulatif des pieces")
    headers = [("Ref", 8), ("Piece", 22), ("Qte", 48), ("Dimensions", 58), ("Origine", 83)]
    ax.add_patch(Rectangle((5, 120), 90, 7, fc=WOOD4, ec="black", lw=0.8))
    for label, x in headers:
        ax.text(x, 123.5, label, fontsize=8.5, fontweight="bold", color="white")
    for i, (ref, name, qty, dims, origin, color) in enumerate(PIECES):
        y = 113 - i * 6.5
        bg = "#faf5ef" if i % 2 == 0 else "#f0e8dc"
        ax.add_patch(Rectangle((5, y), 90, 5.5, fc=bg, ec="#ccc", lw=0.5))
        ax.add_patch(Rectangle((6, y + 0.5), 4, 4.5, fc=color, ec="black", lw=0.5))
        ax.text(8, y + 2.8, ref, ha="center", va="center", fontsize=9, fontweight="bold")
        ax.text(15, y + 2.8, name, va="center", fontsize=8)
        ax.text(50, y + 2.8, str(qty), ha="center", va="center", fontsize=9, fontweight="bold")
        ax.text(55, y + 2.8, dims, va="center", fontsize=7.5)
        ax.text(80, y + 2.8, origin, va="center", fontsize=7)
    ax.text(50, 48, "Total : 22 pieces a partir de 1.5 euro-palettes", ha="center", fontsize=11, fontweight="bold", color=WOOD4)
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

def generate_nomenclature():
    with PdfPages(PDF_PATH) as pdf:
        page_cover(pdf)
        page_bom(pdf)
        page_tools(pdf)
        page_assembly(pdf)
    print(f"Nomenclature PDF generee : {PDF_PATH} ({os.path.getsize(PDF_PATH) // 1024} Ko)")

if __name__ == "__main__":
    generate_nomenclature()
