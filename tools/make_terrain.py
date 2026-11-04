"""Fabrique data/terrain-data.js : un relief 128 x 128 par trajet, au format du template.

Source des altitudes : ETOPO 10 minutes d'arc (NOAA, domaine public), fichier
ETOPO_10min_Ice.vtp du dépôt pyvista/vtk-data, converti en .npz par etopo_to_npz.py.

Usage : python3 tools/make_terrain.py chemin/etopo10.npz data/terrain-data.js
"""
import base64, json, math, sys
import numpy as np

# Les 5 emplacements du template, dans l'ordre. Les clés internes restent celles du
# template en v0.2 (tongariro, inca...), pour ne rien casser ; on les renommera plus tard.
ROUTES = [
    # clé interne, centre (lat, lon), côté du carré en km, note
    ("tongariro", 40.05, 7.75, 1050, "Marseille, la Sardaigne et le golfe de Tunis"),
    ("inca",      39.50, 2.35, 1220, "Marseille, les Baléares et Oran"),
    ("torres",    42.30, -1.75, 2080, "Paris, l'Espagne et le détroit"),
    ("kili",      43.00, 0.70, 2480, "Bruxelles, la côte espagnole et Nador"),
    ("everest",   41.40, -2.35, 3480, "Amsterdam, l'Espagne et le Souss"),
]
N = 128
SEA = -1.0  # la mer, juste sous zéro : la côte devient la première couche

def main(npz_path, out_path):
    d = np.load(npz_path)
    alt = d["alt"].reshape(1081, 2161).astype("f8")  # ligne 0 = 90° N, colonne 0 = 0° E, pas de 1/6°

    def sample(lat, lon):
        r = (90.0 - lat) * 6.0
        c = ((lon % 360.0) + 360.0) % 360.0 * 6.0
        r0 = np.clip(np.floor(r).astype(int), 0, 1079); c0 = np.clip(np.floor(c).astype(int), 0, 2159)
        fr = r - r0; fc = c - c0
        a = alt[r0, c0]; b = alt[r0, c0 + 1]; e = alt[r0 + 1, c0]; f = alt[r0 + 1, c0 + 1]
        return (a * (1 - fc) + b * fc) * (1 - fr) + (e * (1 - fc) + f * fc) * fr

    out = {}
    for key, lat, lon, km, note in ROUTES:
        # même projection que le template : u = .5 + dlon*cos(lat)*111.32/km, v = .5 - dlat*110.57/km
        u = (np.arange(N) / (N - 1))
        v = (np.arange(N) / (N - 1))
        U, V = np.meshgrid(u, v)  # V : ligne (nord en haut)
        LAT = lat - (V - 0.5) * km / 110.57
        LON = lon + (U - 0.5) * km / (math.cos(math.radians(lat)) * 111.32)
        H = sample(LAT, LON)
        H = np.where(H <= 0.0, SEA, H)
        lo, hi = float(np.floor(H.min())), float(np.ceil(H.max()))
        q = np.round((H - lo) / (hi - lo) * 255.0).clip(0, 255).astype(np.uint8)
        out[key] = {"crop": {"lat": lat, "lon": lon, "km": km, "peak": "", "note": note,
                             "n": N, "lo": lo, "hi": hi,
                             "bytes": base64.b64encode(q.tobytes()).decode("ascii")}}
        print(key, "lo", lo, "hi", hi, "land %.0f%%" % (100.0 * (H > 0).mean()))
    js = ("/* Reliefs des trajets Drari. Généré par tools/make_terrain.py, ne pas modifier à la main.\n"
          "   Altitudes : ETOPO 10' (NOAA, domaine public). */\n"
          "window.TERRAIN=" + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n")
    open(out_path, "w", encoding="utf-8").write(js)
    print("ok", out_path, len(js))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
