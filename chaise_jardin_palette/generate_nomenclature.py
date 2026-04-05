"""Generateur de nomenclature PDF - Deck Chair de jardin.

Design minimaliste fidele au modele Instructables.
17 pieces, 7 references, 1 palette.
"""
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_pdf import PdfPages

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(OUTPUT_DIR, "nomenclature.pdf")
WOOD1, WOOD2, WOOD3, WOOD4 = "#d2a679", "#c49a6c", "#b8956a", "#a0784e"

# Dimensions calculees (coherentes avec generate_table.py)
SLAT_W = 95; SLAT_T = 22; SLAT_GAP = 6
FRAME_W = 44; FRAME_D = 70; N_SEAT = 5; N_BACK = 4
SEAT_H = 250; SEAT_DEPTH = N_SEAT * SLAT_W + (N_SEAT - 1) * SLAT_GAP
RUNNER_EXTEND = 200; RUNNER_L = SEAT_DEPTH + RUNNER_EXTEND
BACKREST_TILT = 25; BACK_LENGTH = 500
INNER_W = 600 - 2 * FRAME_W
BACK_DZ = BACK_LENGTH * math.cos(math.radians(BACKREST_TILT))
TOTAL_H = SEAT_H + BACK_DZ

PIECES = [
    ("A", "Latte assise", 5, "600 x 95 x 22", "Lattes pleine largeur", WOOD2),
    ("B", "Latte dossier", 4, f"{INNER_W:.0f} x 95 x 22", "Lattes pleine largeur", WOOD3),
    ("C", "Pied avant", 2, f"44 x 70 x {SEAT_H:.0f}", "2 lattes collees", WOOD1),
    ("D", "Longeron lateral", 2, f"{RUNNER_L:.0f} x 70 x 44", "2 lattes collees", WOOD1),
    ("E", "Support dossier", 2, "500 x 70 x 44", "2 lattes collees", WOOD1),
    ("F", "Traverse avant", 1, f"{INNER_W:.0f} x 44 x 22", "Latte recoupee", WOOD3),
    ("G", "Traverse basse arr.", 1, f"{INNER_W:.0f} x 22 x 22", "Latte refendue", WOOD3),
]

TOOLS = [
    ("Pied-de-biche / levier", "Demontage des lattes"),
    ("Arrache-clou / tenaille", "Retrait des clous"),
    ("Scie circulaire + guide", "Refente a 44 mm (pieds)"),
    ("Scie a onglet", "Decoupe a longueur"),
    ("Ponceuse orbitale", "Poncage (80, 120, 180)"),
    ("Visseuse + vis 4x50 mm", "Assemblage"),
    ("Serre-joints (x4)", "Collage des pieds"),
    ("Colle a bois D3", "Collage pieces doublees"),
    ("Fausse equerre", "Angle dossier ~115 deg"),
]

ASSEMBLY = [
    ("Demontage", "Demonter la palette, trier les pieces"),
    ("Debit", "Decouper toutes les pieces aux bonnes dimensions"),
    ("Poncage", "Poncer toutes les pieces (grains 80, 120, 180)"),
    ("Collage", "Coller les lattes par 2 pour pieds, longerons, supports (24h)"),
    ("Cadres lateraux", "Longeron + pied avant + support dossier (x2)"),
    ("Traverses", "Visser traverse avant F et traverse basse G"),
    ("Assise", f"Visser {N_SEAT} lattes A (espacement {SLAT_GAP} mm)"),
    ("Dossier", f"Visser {N_BACK} lattes B sur supports dossier"),
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
    fig, ax = new_page(pdf, "Nomenclature",
                       "Deck Chair de Jardin en Palettes Recyclees")
    ax.text(50, 122, "Design minimaliste - assise basse, sans accoudoirs",
            ha="center", fontsize=11, style="italic", color=WOOD4)
    ax.add_patch(Rectangle((15, 85), 70, 30, fc="#faf5ef", ec=WOOD4, lw=1.5))
    summary = [
        ("Materiau", "1 euro-palette standard"),
        ("Dimensions", f"600 x {RUNNER_L:.0f} x {TOTAL_H:.0f} mm (L x P x H)"),
        ("Assise", f"{SEAT_H:.0f} mm (adaptee table basse 450 mm)"),
        ("Dossier", f"Incline a ~{90+BACKREST_TILT} degres"),
        ("Pieces", f"17 pieces (7 references)"),
    ]
    for i, (label, value) in enumerate(summary):
        y = 110 - i * 5
        ax.text(20, y, f"{label} :", fontsize=10, fontweight="bold", color=WOOD4)
        ax.text(48, y, value, fontsize=10)
    pdf.savefig(fig); plt.close(fig)

def page_bom(pdf):
    fig, ax = new_page(pdf, "Recapitulatif des pieces")
    headers = [("Ref", 8), ("Piece", 22), ("Qte", 48),
               ("Dimensions", 58), ("Origine", 83)]
    ax.add_patch(Rectangle((5, 120), 90, 7, fc=WOOD4, ec="black", lw=0.8))
    for label, x in headers:
        ax.text(x, 123.5, label, fontsize=8.5, fontweight="bold", color="white")
    for i, (ref, name, qty, dims, origin, color) in enumerate(PIECES):
        y = 113 - i * 7
        bg = "#faf5ef" if i % 2 == 0 else "#f0e8dc"
        ax.add_patch(Rectangle((5, y), 90, 6, fc=bg, ec="#ccc", lw=0.5))
        ax.add_patch(Rectangle((6, y + 0.5), 4, 5, fc=color, ec="black", lw=0.5))
        ax.text(8, y + 3, ref, ha="center", va="center", fontsize=9, fontweight="bold")
        ax.text(15, y + 3, name, va="center", fontsize=8)
        ax.text(50, y + 3, str(qty), ha="center", va="center",
                fontsize=9, fontweight="bold")
        ax.text(55, y + 3, dims, va="center", fontsize=7.5)
        ax.text(80, y + 3, origin, va="center", fontsize=7)
    total = sum(p[2] for p in PIECES)
    ax.text(50, 55, f"Total : {total} pieces a partir de 1 euro-palette",
            ha="center", fontsize=11, fontweight="bold", color=WOOD4)
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
        y = 120 - i * 11
        ax.add_patch(plt.Circle((10, y + 2), 3, fc=WOOD4, ec="black",
                                lw=0.5, zorder=3))
        ax.text(10, y + 2, str(i + 1), ha="center", va="center",
                fontsize=10, fontweight="bold", color="white", zorder=4)
        ax.add_patch(Rectangle((16, y - 1.5), 78, 8, fc="#faf5ef",
                                ec="#e0d5c5", lw=0.8))
        ax.text(19, y + 3.5, title, fontsize=10, fontweight="bold", color=WOOD4)
        ax.text(19, y + 0.2, desc, fontsize=9, color="#555")
    pdf.savefig(fig); plt.close(fig)

def generate_nomenclature():
    with PdfPages(PDF_PATH) as pdf:
        page_cover(pdf)
        page_bom(pdf)
        page_tools(pdf)
        page_assembly(pdf)
    print(f"Nomenclature PDF generee : {PDF_PATH} "
          f"({os.path.getsize(PDF_PATH) // 1024} Ko)")

if __name__ == "__main__":
    generate_nomenclature()
