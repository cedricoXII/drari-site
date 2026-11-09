"""Construit index.html : le template Fold Line (base/) + les données et les textes Drari.

Usage : python3 tools/build.py
Chaque remplacement vérifie qu'il trouve le texte le bon nombre de fois, sinon le script s'arrête.

Ordre :
1. les modules de données (data/*.js) et les modules réécrits pour Drari (tools/v05/*.js) remplacent
   ceux du template, en entier ;
2. les modules inutiles (la plongée « interior ») sont retirés ;
3. les remplacements de tools/patches.py sont appliqués, dans l'ordre.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from patches import PATCHES  # noqa: E402
from patches_v05 import HEAD_V05  # noqa: E402

BASE = os.path.join(ROOT, "base", "fold-line-v7.html")
OUT = os.path.join(ROOT, "index.html")
AURA = os.path.join(ROOT, "aura", "index.html")

# modules remplacés en entier (chemin dans le template -> fichier du dépôt)
DATA_MODULES = {
    "hero/treks-data.js": os.path.join(ROOT, "data", "treks-data.js"),
    "hero/terrain-data.js": os.path.join(ROOT, "data", "terrain-data.js"),
    # v0.5 : le ticket, la section « Gratuit ? » (à la place de « Quand partir ») et le pied de page
    "sections/book.js": os.path.join(ROOT, "tools", "v05", "book.js"),
    "sections/when.js": os.path.join(ROOT, "tools", "v05", "price.js"),
    "sections/footer.js": os.path.join(ROOT, "tools", "v05", "footer.js"),
}

# v0.5 : modules retirés (la plongée dans la carte, chargée seulement avec ?interior=story, environ 777 Ko)
DROP_MODULES = [
    "interior/walks.js", "interior/interior.js", "interior/tongariro-strip.js", "interior/inca-strip.js",
    "interior/torres-strip.js", "interior/kili-strip.js", "interior/everest-strip.js",
]


def _module_re(src):
    return re.compile(r'(<script type="text/x-fold" data-src="' + re.escape(src) + r'">)(.*?)(</script>)', re.S)


def replace_module(html, src, new_body):
    m = list(_module_re(src).finditer(html))
    assert len(m) == 1, (src, len(m))
    m = m[0]
    body = new_body.replace("</script", "<\\/script")
    return html[: m.start(2)] + body + html[m.end(2):]


def drop_module(html, src):
    m = list(_module_re(src).finditer(html))
    assert len(m) == 1, (src, len(m))
    m = m[0]
    end = m.end(3)
    if html[end:end + 1] == "\n":
        end += 1
    return html[: m.start(1)] + html[end:]


# Polices : les sous-ensembles du modèle (121 signes) n'avaient ni à, ç, è, ê, ô, ù, û, ni « », ni l'espace fine.
# Le navigateur prenait ces lettres dans une autre police (« prête » déformé). On met à la place les sous-ensembles
# « latin » complets de fontsource (mêmes axes variables), rangés dans fonts/ (licence SIL OFL 1.1, fichiers LICENSE-*).
FONTS = {
    "Unbounded": "unbounded-latin-wght.woff2",
    "Instrument Sans": "instrument-sans-latin-wght.woff2",
    "Martian Mono": "martian-mono-latin-standard.woff2",
}


def swap_fonts(html):
    import base64
    for family, name in FONTS.items():
        data = base64.b64encode(open(os.path.join(ROOT, "fonts", name), "rb").read()).decode("ascii")
        pat = re.compile(r'(@font-face\{font-family:' + re.escape(family) + r';[^}]*?src:url\(data:font/woff2;base64,)'
                         r'[A-Za-z0-9+/=]+(\) format\("woff2"\);unicode-range:U\+0000-00FF,)')
        html, n = pat.subn(lambda m: m.group(1) + data + m.group(2), html)
        assert n == 1, (family, n)
    return html


def main():
    html = open(BASE, encoding="utf-8").read()
    for src, path in DATA_MODULES.items():
        html = replace_module(html, src, open(path, encoding="utf-8").read())
    for src in DROP_MODULES:
        html = drop_module(html, src)
    errors = []
    for i, p in enumerate(PATCHES):
        old, new = p[0], p[1]
        if isinstance(old, tuple):
            # ("@range", début, fin) : tout le texte du début jusqu'à la fin comprise (le début doit être unique)
            _, start, end = old
            n = html.count(start)
            j = html.find(end, html.find(start) + len(start)) if n == 1 else -1
            if n != 1 or j < 0:
                errors.append("patch %d (bloc) : début trouvé %d fois, fin %s : %r" % (i, n, "trouvée" if j >= 0 else "absente", start[:90]))
                continue
            a = html.find(start)
            html = html[:a] + new + html[j + len(end):]
            continue
        count = p[2] if len(p) > 2 else 1
        n = html.count(old)
        if n != count:
            errors.append("patch %d : trouvé %d fois au lieu de %d : %r" % (i, n, count, old[:90]))
            continue
        html = html.replace(old, new)
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    html = swap_fonts(html)
    leftover = [s for s in ("Sam1983Aing", "Valmora", "Book the walk", "Day 1. The valley") if s in html]
    assert not leftover, leftover
    open(OUT, "w", encoding="utf-8").write(html)
    print("ok", OUT, len(html.encode("utf-8")), "octets,", len(PATCHES), "remplacements")
    # v0.5 : les mêmes balises (titre, description, Open Graph, Twitter, theme-color, icônes) dans la page de chargement Aura
    aura = open(AURA, encoding="utf-8").read()
    a, b = aura.index("<!-- dr-head"), aura.index("<!-- /dr-head -->")
    a = aura.index("-->", a) + 3
    new = aura[:a] + "\n" + HEAD_V05 + "\n" + aura[b:]
    if new != aura:
        open(AURA, "w", encoding="utf-8").write(new)
    print("ok", AURA, len(new.encode("utf-8")), "octets")


if __name__ == "__main__":
    main()
