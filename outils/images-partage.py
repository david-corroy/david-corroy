#!/usr/bin/env python3
"""Génère les images de partage des dépôts, au format attendu par GitHub.

1280 x 640, aux couleurs de david-corroy.com : fond #17181b, accent #ff9b00.
C'est l'image que LinkedIn, X et Slack affichent quand on partage un lien de dépôt.
Sans elle, GitHub sert une carte grise générique.

    python3 outils/images-partage.py            # tout régénérer dans images-partage/
    python3 outils/images-partage.py prompts-geo

Rendu par rsvg-convert, qui lit les polices du système.
"""

import pathlib
import subprocess
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
SORTIE = RACINE / "images-partage"

FOND = "#17181b"
ACCENT = "#ff9b00"
TEXTE = "#ffffff"
SECONDAIRE = "#a3a4a7"
POLICE = "Open Sans, Noto Sans, DejaVu Sans, sans-serif"

# Titre court, puis la phrase qui dit à quoi ça sert. Pas de superlatif :
# l'image est lue en une seconde dans un fil LinkedIn.
DEPOTS = {
    "prompts-geo": (
        "Prompts GEO",
        "19 prompts en français pour savoir si ChatGPT,",
        "Perplexity et Gemini vous citent, et pourquoi.",
    ),
    "grille-suivi-visibilite-ia": (
        "Grille de suivi IA",
        "Un tableur gratuit pour relever chaque mois",
        "vos citations dans les réponses des IA.",
    ),
    "skills-seo-geo": (
        "Skills SEO et GEO",
        "25 compétences en français pour Claude Code,",
        "adaptées au marché francophone.",
    ),
    "skills-marketing-fr": (
        "Skills marketing",
        "47 compétences marketing en français :",
        "copywriting, acquisition, RGPD compris.",
    ),
    "html-head-seo": (
        "La balise head",
        "Ce que Google, les IA et les réseaux sociaux",
        "lisent vraiment dans votre en-tête.",
    ),
    "HEAD": (
        "HEAD",
        "A complete, maintained reference of HTML",
        "head elements. English, français, español.",
    ),
}


def echappe(texte):
    return texte.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(titre, ligne1, ligne2):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="640" viewBox="0 0 1280 640">
  <rect width="1280" height="640" fill="{FOND}"/>

  <!-- Barre d'accent à gauche : repère de marque reconnaissable en vignette -->
  <rect x="0" y="0" width="14" height="640" fill="{ACCENT}"/>

  <!-- Filet court au-dessus du titre, même rôle qu'une surtitre imprimée -->
  <rect x="96" y="150" width="88" height="6" fill="{ACCENT}"/>

  <text x="96" y="268" font-family="{POLICE}" font-size="82" font-weight="700"
        fill="{TEXTE}" letter-spacing="-1.5">{echappe(titre)}</text>

  <text x="96" y="352" font-family="{POLICE}" font-size="34" fill="{SECONDAIRE}">{echappe(ligne1)}</text>
  <text x="96" y="400" font-family="{POLICE}" font-size="34" fill="{SECONDAIRE}">{echappe(ligne2)}</text>

  <text x="96" y="548" font-family="{POLICE}" font-size="27" font-weight="600"
        fill="{ACCENT}" letter-spacing="0.5">david-corroy.com</text>
  <text x="96" y="588" font-family="{POLICE}" font-size="23"
        fill="{SECONDAIRE}">Bernard David Corroy, consultant SEO et GEO</text>
</svg>"""


def genere(nom):
    titre, l1, l2 = DEPOTS[nom]
    SORTIE.mkdir(exist_ok=True)
    chemin_svg = SORTIE / f"{nom}.svg"
    chemin_png = SORTIE / f"{nom}.png"
    chemin_svg.write_text(svg(titre, l1, l2), encoding="utf-8")
    subprocess.run(
        ["rsvg-convert", "-w", "1280", "-h", "640", "-o", str(chemin_png), str(chemin_svg)],
        check=True,
    )
    chemin_svg.unlink()  # le SVG n'est qu'une étape, GitHub veut un PNG
    return chemin_png


if __name__ == "__main__":
    demandes = sys.argv[1:] or list(DEPOTS)
    for nom in demandes:
        if nom not in DEPOTS:
            print(f"  inconnu : {nom}")
            continue
        p = genere(nom)
        print(f"  {p.name:<34} {p.stat().st_size // 1024} Ko")
