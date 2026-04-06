"""Generateur de nomenclature PDF - Deck Chair de jardin.

Structure palette, dossier inclinable 3 positions (cremaillere). 25 pieces, 1 palette.
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
BAR_COLOR = "#c06030"; CREM_COLOR = "#e8c88a"

CHAIR_W = 600
SLAT_W = 95; SLAT_T = 22; SLAT_GAP = 15
PANEL_W = 95; BLOCK_H = 78; BLOCK_W = 44
PANEL_H = SLAT_T + BLOCK_H + SLAT_T  # 122
SEAT_H = PANEL_H + SLAT_T  # 144
N_SEAT = 4; N_BACK = 5
SEAT_DEPTH = N_SEAT * SLAT_W + (N_SEAT - 1) * SLAT_GAP
RUNNER_EXTEND = 350; RUNNER_L = SEAT_DEPTH + RUNNER_EXTEND
BACKREST_TILT = 35; BACK_LENGTH = 650
FRAME_W = 44; FRAME_D = 70; INNER_W = CHAIR_W - 2 * PANEL_W
BACK_DZ = BACK_LENGTH * math.cos(math.radians(BACKREST_TILT))
PIVOT_Y = SEAT_DEPTH; PIVOT_Z = PANEL_H
TOTAL_H = PIVOT_Z + BACK_DZ
SUPPORT_BELOW = 50.0
SUPPORT_PIVOT_L = BACK_LENGTH + SUPPORT_BELOW
STRUT_ATTACH = 400.0; STRUT_L = 380.0; STRUT_SECTION = SLAT_T
CREM_W = SLAT_T; CREM_HEIGHT = 40.0
BACKREST_ANGLES = [25.0, 35.0, 50.0]
_NP = []
for _a in BACKREST_ANGLES:
    _r = math.radians(_a)
    _yt = PIVOT_Y + STRUT_ATTACH * math.sin(_r)
    _zt = PIVOT_Z + STRUT_ATTACH * math.cos(_r)
    _yd = math.sqrt(STRUT_L**2 - (_zt - PIVOT_Z)**2)
    _NP.append(_yt - _yd)
CREM_L = max(_NP) - min(_NP) + 3 * STRUT_SECTION

PIECES = [
    ("A", "Latte assise", 4, "600 x 95 x 22", "Lattes pleine largeur", WOOD2),
    ("B", "Latte dossier", 5, f"{INNER_W:.0f} x 95 x 22", "Lattes pleine largeur", WOOD3),
    ("C", "Planche lat. basse", 2, f"{RUNNER_L:.0f} x 95 x 22", "Lattes pleine largeur", WOOD1),
    ("D", "Planche lat. haute", 2, f"{RUNNER_L:.0f} x 95 x 22", "Lattes pleine largeur", WOOD1),
    ("E", "Bloc lateral", 6, f"44 x 44 x {BLOCK_H:.0f}", "Blocs de palette", WOOD4),
    ("F", "Support dossier", 2, f"{SUPPORT_PIVOT_L:.0f} x 70 x 44", "2 lattes collees", WOOD1),
    ("G", "Traverse avant", 1, f"{INNER_W:.0f} x 44 x 22", "Latte recoupee", WOOD3),
    ("H", "Cremaillere", 2, f"{CREM_L:.0f} x {CREM_W} x {CREM_HEIGHT:.0f}", "Bloc palette", CREM_COLOR),
    ("I", "Barre stabilisatrice", 2, f"{STRUT_L:.0f} x {STRUT_SECTION} x {STRUT_SECTION}", "Latte recoupee", BAR_COLOR),
]

TOOLS = [
    ("Pied-de-biche / levier", "Demontage des lattes et blocs"),
    ("Arrache-clou / tenaille", "Retrait des clous"),
    ("Scie circulaire + guide", "Decoupe a longueur"),
    ("Scie a onglet", "Decoupe encoches cremaillere"),
    ("Ponceuse orbitale", "Poncage (80, 120, 180)"),
    ("Visseuse + vis 4x50 mm", "Assemblage"),
    ("Serre-joints (x4)", "Collage supports dossier"),
    ("Colle a bois D3", "Collage pieces doublees"),
    ("Fausse equerre", "Angle dossier (25/35/50 deg)"),
    ("Boulon M10 x 120 + rondelles", "Pivot dossier (x2)"),
]

ASSEMBLY = [
    ("Demontage", "Demonter la palette, conserver lattes ET blocs"),
    ("Debit", "Decouper toutes les pieces aux bonnes dimensions"),
    ("Poncage", "Poncer toutes les pieces (grains 80, 120, 180)"),
    ("Panneaux lat.", "Planche basse + 3 blocs + planche haute (x2)"),
    ("Traverses", "Visser traverse avant G entre les panneaux"),
    ("Assise", f"Visser {N_SEAT} lattes A (espacement {SLAT_GAP:.0f} mm)"),
    ("Cremailleres", "Tailler 3 encoches en V dans H, fixer a l'INTERIEUR"),
    ("Supports", f"Coller F, monter sur pivot M10 au sommet du panneau"),
    ("Barres stab.", "Fixer barres I au support, pied dans cremaillere"),
    ("Dossier", f"Visser {N_BACK} lattes B sur supports"),
    ("Verification", "Tester les 3 positions, controler stabilite"),
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
    ax.text(50, 122, "Dossier inclinable 3 positions - mecanisme cremaillere", ha="center", fontsize=11, style="italic", color=WOOD4)
    ax.add_patch(Rectangle((15, 82), 70, 33, fc="#faf5ef", ec=WOOD4, lw=1.5))
    angles = "/".join(f"{a:.0f}" for a in BACKREST_ANGLES)
    summary = [
        ("Materiau", "1 euro-palette standard"),
        ("Dimensions", f"600 x {RUNNER_L:.0f} x {TOTAL_H:.0f} mm (L x P x H)"),
        ("Assise", f"{SEAT_H:.0f} mm (tres basse, style transat)"),
        ("Dossier", f"Inclinable {angles} deg (cremaillere)"),
        ("Pieces", f"{sum(p[2] for p in PIECES)} pieces ({len(PIECES)} references)"),
        ("Mecanisme", "Pivot + barre + 2 cremailleres"),
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
        y = 113 - i * 7
        bg = "#faf5ef" if i % 2 == 0 else "#f0e8dc"
        ax.add_patch(Rectangle((5, y), 90, 6, fc=bg, ec="#ccc", lw=0.5))
        ax.add_patch(Rectangle((6, y + 0.5), 4, 5, fc=color, ec="black", lw=0.5))
        ax.text(8, y + 3, ref, ha="center", va="center", fontsize=9, fontweight="bold")
        ax.text(15, y + 3, name, va="center", fontsize=8)
        ax.text(50, y + 3, str(qty), ha="center", va="center", fontsize=9, fontweight="bold")
        ax.text(55, y + 3, dims, va="center", fontsize=7.5)
        ax.text(80, y + 3, origin, va="center", fontsize=7)
    total = sum(p[2] for p in PIECES)
    ax.text(50, 55, f"Total : {total} pieces a partir de 1 euro-palette", ha="center", fontsize=11, fontweight="bold", color=WOOD4)
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
