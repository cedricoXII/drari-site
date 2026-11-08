"""v0.5 : la texture du globe (champ de distance à la côte) passe de 2 048 × 1 024 (PNG, 215 Ko) à 1 024 × 512 (JPEG, environ 50 Ko).

Usage : python3 tools/make_globe_small.py  (écrit data/globe-sdf-1024.jpg, lu par tools/patches_v05.py)
Les valeurs restent les mêmes (distance à la côte, en texels de la carte de 2 048 de large, échelle 4) :
seule la finesse du dessin des côtes est divisée par deux. Écart mesuré près des côtes : 4 niveaux au plus sur 255.
"""
import base64, io, os, re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(os.path.join(ROOT, "base", "fold-line-v7.html"), encoding="utf-8").read()
m = re.search(r'window\.GLOBE_DATA=\{w:2048,h:1024,scale:4,src:"data:image/png;base64,([^"]+)"', html)
img = Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert("L")
small = img.resize((1024, 512), Image.BOX)  # moyenne par zone : garde les distances linéaires
out = os.path.join(ROOT, "data", "globe-sdf-1024.jpg")
small.save(out, quality=95, optimize=True, progressive=True)
print("ok", out, os.path.getsize(out), "octets")
