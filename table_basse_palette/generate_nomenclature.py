"""
Generateur de nomenclature PDF - Table basse en palettes recyclees.

Genere un PDF multi-pages avec la liste de debit, les instructions
de recuperation des pieces, l'outillage et l'ordre d'assemblage.

Usage :
    python3 generate_nomenclature.py
"""

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
    ("A", "Latte plateau", 6, "1200 x 95 x 22", "Lattes du dessus", WOOD2),
    ("B", "Pied (3 blocs colles)", 4, "95 x 95 x 406", "Blocs empiles", WOOD1),
    ("C", "Latte etagere", 4, "1100 x 95 x 22", "Lattes dessus/dessous", WOOD2),
    ("D", "Traverse plateau", 3, "600 x 22 x 22", "Traverses / chutes", WOOD3),
    ("E", "Entretoise laterale", 2, "1010 x 70 x 22", "Traverses refendues", WOOD3),
    ("F", "Traverse etagere", 2, "600 x 22 x 22", "Traverses / chutes", WOOD3),
]

DEBIT_INSTRUCTIONS = {
    "A": [
        "Retirer les lattes du dessus au pied-de-biche",
        "Arracher les clous restants a la tenaille",
        "Poncer les deux faces (grain 80, puis 120, puis 180)",
        "Recouper a 1200 mm de long si necessaire",
        "Selectionner les lattes de 95 mm de large",
    ],
    "B": [
        "Demonter la palette : retirer toutes les lattes",
        "Recuperer les 9 blocs (plots) par palette",
        "Scier les traverses au ras des blocs",
        "Poncer les blocs (grain 80, puis 120)",
        "Empiler 3 blocs, coller a la colle D3 (serre-joints, 24h)",
        "Recouper l'ensemble a 406 mm a la scie a onglet",
    ],
    "C": [
        "Meme processus que les lattes du plateau (Ref. A)",
        "Recouper a 1100 mm (= 1200 - 2 x 50 mm de retrait)",
        "Les lattes du dessous conviennent parfaitement",
    ],
    "D": [
        "Recuperer les traverses de la palette",
        "Recouper a 600 mm de long (= largeur de la table)",
        "Refendre en largeur a 22 mm si necessaire",
    ],
    "E": [
        "Utiliser des traverses ou des lattes larges",
        "Refendre a 70 mm de largeur a la scie circulaire",
        "Recouper a 1010 mm de long",
    ],
    "F": [
        "Identique a la Ref. D",
        "Recouper a 600 mm de long",
    ],
}

TOOLS = [
    ("Pied-de-biche / levier", "Demontage des lattes"),
    ("Arrache-clou / tenaille", "Retrait des clous"),
    ("Scie circulaire ou scie a onglet", "Decoupe a longueur et refente"),
    ("Ponceuse orbitale", "Poncage (grains 80, 120, 180)"),
    ("Visseuse + vis a bois (4x50 mm)", "Assemblage"),
    ("Serre-joints (x4 min.)", "Collage des blocs pour les pieds"),
    ("Colle a bois D3 (exterieur)", "Collage des blocs pieds"),
    ("Equerre de menuisier", "Verification des angles droits"),
    ("Metre ruban + crayon", "Tracage et mesures"),
]

ASSEMBLY_STEPS = [
    ("Demontage", "Demonter les 2 palettes, trier les pieces"),
    ("Debit", "Decouper toutes les pieces aux dimensions finales"),
    ("Poncage", "Poncer toutes les pieces avant assemblage"),
    ("Pieds", "Coller les blocs par 3, laisser secher 24h, recouper a 406 mm"),
    ("Cadre bas", "Visser les traverses etagere (F) entre les pieds"),
    ("Entretoises", "Visser les entretoises laterales (E) entre les pieds"),
    ("Etagere", "Poser et visser les lattes etagere (C) sur les traverses (F)"),
    ("Traverses plateau", "Visser les traverses (D) sur le haut des pieds"),
    ("Plateau", "Poser et visser les lattes (A) sur les traverses (D)"),
    ("Finition", "Huile de lin, vernis, ou lasure selon usage"),
]


def new_page(pdf, title, subtitle=None):
    fig, ax = plt.subplots(figsize=(8.27, 11.69))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 140)
    ax.axis("off")
    ax.text(50, 135, title, ha="center", va="top", fontsize=16, fontweight="bold")
    if subtitle:
        ax.text(50, 130, subtitle, ha="center", va="top", fontsize=11, color="#555555")
    return fig, ax


def page_cover(pdf):
    fig, ax = new_page(pdf, "Nomenclature", "Table Basse en Palettes Recyclees")
    ax.text(50, 122, "Liste de debit et instructions d'assemblage",
            ha="center", fontsize=12, style="italic", color=WOOD4)

    # Summary box
    ax.add_patch(Rectangle((15, 85), 70, 30, fc="#faf5ef", ec=WOOD4, lw=1.5, zorder=2))
    summary = [
        ("Materiau", "2 euro-palettes standard (1200 x 800 mm)"),
        ("Dimensions table", "1200 x 600 x 450 mm (L x l x H)"),
        ("Nombre de pieces", "21 pieces (6 references)"),
        ("Outillage", "9 outils necessaires"),
        ("Etapes", "10 etapes d'assemblage"),
    ]
    for i, (label, value) in enumerate(summary):
        y = 110 - i * 5
        ax.text(20, y, f"{label} :", fontsize=10, fontweight="bold", color=WOOD4, zorder=3)
        ax.text(52, y, value, fontsize=10, zorder=3)

    ax.text(50, 75, "Choisir des palettes marquees HT (traitement thermique)",
            ha="center", fontsize=9, color="green")
    ax.text(50, 70, "Eviter les palettes marquees MB (bromure de methyle, toxique)",
            ha="center", fontsize=9, color="red")

    # Pallet diagram
    ax.add_patch(Rectangle((25, 40), 50, 22, fc="#f0dcc0", ec="black", lw=1))
    for i in range(5):
        py = 42 + i * 3.8
        ax.add_patch(Rectangle((27, py), 46, 3, fc=WOOD1, ec="black", lw=0.5))
    ax.text(50, 37, "Euro-palette 1200 x 800 mm", ha="center", fontsize=9, color="#666")

    pdf.savefig(fig)
    plt.close(fig)


def page_bom_table(pdf):
    fig, ax = new_page(pdf, "Recapitulatif des pieces")

    # Table header
    headers = [("Ref", 8), ("Piece", 28), ("Qte", 52), ("Dimensions (mm)", 65), ("Origine", 87)]
    ax.add_patch(Rectangle((5, 120), 90, 7, fc=WOOD4, ec="black", lw=0.8))
    for label, x in headers:
        ax.text(x, 123.5, label, fontsize=9, fontweight="bold", color="white", ha="center" if label == "Qte" else "left")

    # Table rows
    for i, (ref, name, qty, dims, origin, color) in enumerate(PIECES):
        y = 113 - i * 9
        bg = "#faf5ef" if i % 2 == 0 else "#f0e8dc"
        ax.add_patch(Rectangle((5, y), 90, 8, fc=bg, ec="#cccccc", lw=0.5))
        # Color swatch
        ax.add_patch(Rectangle((6, y + 1), 5, 6, fc=color, ec="black", lw=0.6))
        ax.text(8.5, y + 4, ref, ha="center", va="center", fontsize=10, fontweight="bold")
        ax.text(15, y + 4, name, va="center", fontsize=9)
        ax.text(52, y + 4, str(qty), ha="center", va="center", fontsize=10, fontweight="bold")
        ax.text(57, y + 4, dims, va="center", fontsize=8.5)
        ax.text(82, y + 4, origin, va="center", fontsize=8)

    # Visual pieces
    ax.text(50, 52, "Vue des pieces (echelle relative) :", ha="center", fontsize=10, fontweight="bold")

    pieces_visual = [
        ("A", 60, WOOD2, 3, "1200 mm"),
        ("C", 55, WOOD2, 3, "1100 mm"),
        ("E", 50, WOOD3, 2.5, "1010 mm"),
        ("D/F", 30, WOOD3, 2, "600 mm"),
    ]
    for i, (label, w, color, h, dim) in enumerate(pieces_visual):
        y = 43 - i * 5.5
        ax.add_patch(Rectangle((5, y), w, h, fc=color, ec="black", lw=0.6))
        ax.text(5 + w / 2, y + h / 2, f"{label} - {dim}", ha="center", va="center",
                fontsize=7, color="white", fontweight="bold")

    # Leg
    ax.add_patch(Rectangle((72, 22), 5, 17, fc=WOOD1, ec="black", lw=0.6))
    ax.text(74.5, 30, "B", ha="center", va="center", fontsize=8, fontweight="bold")
    ax.text(74.5, 19, "406 mm", ha="center", fontsize=7)

    ax.text(50, 14, "Total : 21 pieces a partir de 2 euro-palettes",
            ha="center", fontsize=11, fontweight="bold", color=WOOD4)

    pdf.savefig(fig)
    plt.close(fig)


def page_debit(pdf):
    """2 pages de debit detaille (3 pieces par page)."""
    for page_idx in range(2):
        subset = list(DEBIT_INSTRUCTIONS.items())[page_idx * 3:(page_idx + 1) * 3]
        page_num = page_idx + 1
        fig, ax = new_page(pdf, f"Instructions de debit ({page_num}/2)")

        y_cursor = 122
        for ref, steps in subset:
            piece = next(p for p in PIECES if p[0] == ref)
            _, name, qty, dims, origin, color = piece

            # Piece header
            ax.add_patch(Rectangle((5, y_cursor - 1), 90, 7, fc=color, ec="black", lw=0.8))
            ax.text(8, y_cursor + 2.5, f"Ref. {ref} - {name}",
                    fontsize=11, fontweight="bold", color="white")
            ax.text(92, y_cursor + 2.5, f"x{qty}", fontsize=11, fontweight="bold",
                    color="white", ha="right")

            y_cursor -= 3
            ax.text(8, y_cursor, f"Dimensions : {dims} mm  |  Origine : {origin}",
                    fontsize=8.5, color="#555")
            y_cursor -= 2

            for step in steps:
                y_cursor -= 3.5
                ax.text(10, y_cursor, f"  {step}", fontsize=9)

            y_cursor -= 6

        pdf.savefig(fig)
        plt.close(fig)


def page_tools(pdf):
    fig, ax = new_page(pdf, "Outillage necessaire")

    # Tool table
    ax.add_patch(Rectangle((5, 117), 90, 7, fc=WOOD4, ec="black", lw=0.8))
    ax.text(10, 120.5, "Outil", fontsize=10, fontweight="bold", color="white")
    ax.text(60, 120.5, "Usage", fontsize=10, fontweight="bold", color="white")

    for i, (tool, usage) in enumerate(TOOLS):
        y = 110 - i * 7
        bg = "#faf5ef" if i % 2 == 0 else "#f0e8dc"
        ax.add_patch(Rectangle((5, y), 90, 6, fc=bg, ec="#cccccc", lw=0.5))
        ax.text(8, y + 3, tool, va="center", fontsize=9, fontweight="bold")
        ax.text(55, y + 3, usage, va="center", fontsize=9, color="#555")

    pdf.savefig(fig)
    plt.close(fig)


def page_assembly(pdf):
    fig, ax = new_page(pdf, "Ordre d'assemblage")

    for i, (title, desc) in enumerate(ASSEMBLY_STEPS):
        y = 120 - i * 10
        # Step number circle
        circle_x = 10
        ax.add_patch(plt.Circle((circle_x, y + 2), 3, fc=WOOD4, ec="black", lw=0.5, zorder=3))
        ax.text(circle_x, y + 2, str(i + 1), ha="center", va="center",
                fontsize=10, fontweight="bold", color="white", zorder=4)

        # Step content
        ax.add_patch(Rectangle((16, y - 1.5), 78, 8, fc="#faf5ef", ec="#e0d5c5", lw=0.8))
        ax.text(19, y + 3.5, title, fontsize=10, fontweight="bold", color=WOOD4)
        ax.text(19, y + 0.2, desc, fontsize=9, color="#555")

    pdf.savefig(fig)
    plt.close(fig)


def generate_nomenclature():
    with PdfPages(PDF_PATH) as pdf:
        page_cover(pdf)
        page_bom_table(pdf)
        page_debit(pdf)
        page_tools(pdf)
        page_assembly(pdf)

    print(f"Nomenclature PDF generee : {PDF_PATH} ({os.path.getsize(PDF_PATH) // 1024} Ko)")


if __name__ == "__main__":
    generate_nomenclature()
