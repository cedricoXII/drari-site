"""Construit index.html : le template Fold Line (base/) + les données et les textes Drari.

Usage : python3 tools/build.py
Chaque remplacement vérifie qu'il trouve le texte le bon nombre de fois, sinon le script s'arrête.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from patches import PATCHES  # noqa: E402

BASE = os.path.join(ROOT, "base", "fold-line-v7.html")
OUT = os.path.join(ROOT, "index.html")

DATA_MODULES = {
    "hero/treks-data.js": os.path.join(ROOT, "data", "treks-data.js"),
    "hero/terrain-data.js": os.path.join(ROOT, "data", "terrain-data.js"),
}


def replace_module(html, src, new_body):
    pat = re.compile(r'(<script type="text/x-fold" data-src="' + re.escape(src) + r'">)(.*?)(</script>)', re.S)
    m = list(pat.finditer(html))
    assert len(m) == 1, (src, len(m))
    m = m[0]
    body = new_body.replace("</script", "<\\/script")
    return html[: m.start(2)] + body + html[m.end(2):]


def main():
    html = open(BASE, encoding="utf-8").read()
    for src, path in DATA_MODULES.items():
        html = replace_module(html, src, open(path, encoding="utf-8").read())
    errors = []
    for i, p in enumerate(PATCHES):
        old, new = p[0], p[1]
        count = p[2] if len(p) > 2 else 1
        n = html.count(old)
        if n != count:
            errors.append("patch %d : trouvé %d fois au lieu de %d : %r" % (i, n, count, old[:90]))
            continue
        html = html.replace(old, new)
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    leftover = [s for s in ("Sam1983Aing",) if s in html]
    assert not leftover, leftover
    open(OUT, "w", encoding="utf-8").write(html)
    print("ok", OUT, len(html.encode("utf-8")), "octets,", len(PATCHES), "remplacements")


if __name__ == "__main__":
    main()
