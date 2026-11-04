"""Fabrique data/treks-data.js : les 5 trajets Drari, au format des treks du template.

Les textes sont ici. La géométrie (km le long du trajet, altitudes) est calculée :
- les km sont mis à l'échelle sur une distance routière sourcée ;
- les altitudes viennent d'ETOPO 10' (NOAA), donc lissées : ce sont des ordres de grandeur.

Usage : python3 tools/make_routes.py chemin/etopo10.npz data/treks-data.js

Sources des chiffres (vérifiées le 4 nov. 2026) :
- Paris - Algésiras : 1 914 km, environ 17 h (planderoute.net)
- Bruxelles - Almería : 2 150 km, environ 19 h 40 (planderoute.net)
- Amsterdam - Algésiras : 2 428 km, environ 22 h 40 (1map.com)
- Tanger - Agadir : 791 km, environ 8 h (distancede.com)
- Algésiras - Tanger Med : 1 h 30 de traversée (DFDS)
- Marseille - Tunis : 22 à 26 h de traversée, Corsica Linea et CTN (Ferryhopper)
- Marseille - Oran : 28 à 29 h de traversée, Algérie Ferries (aFerry)
- Almería - Nador : 7 à 11 h selon la compagnie (Ferryhopper)
- Opération Marhaba 2026 : du 10 juin au 15 septembre, plus de 4 millions de MRE accueillis (maroc.ma)
"""
import json, math, sys
import numpy as np

MARHABA = ("De mi-juin à mi-septembre, c'est l'opération Marhaba : en 2026, plus de 4 millions "
           "de Marocains du monde sont passés par les ports (maroc.ma).")

ROUTES = [
    {
        "key": "tongariro", "cat": "day",
        "fullName": "Marseille → Tunis, en ferry",
        "name": "Marseille → Tunis", "line2": "une nuit en mer",
        "country": "Tunisie", "countryShort": "TN",
        "days": 1, "daysLabel": "1 NUIT", "kmLabel": "22 H EN MER",
        "big": "22 h", "bigK": "de traversée, Corsica Linea ou CTN", "coverK": "MARSEILLE",
        "line": "Le van monte à bord à Marseille. Le lendemain, il sort à La Goulette.",
        "nightLabel": "À bord",
        "sea": True,
        "points": [
            ("Port de Marseille", 43.33, 5.35),
            ("Au large de la Sardaigne", 39.90, 7.60),
            ("Golfe de Tunis", 37.05, 10.35),
            ("La Goulette, Tunis", 36.81, 10.30),
        ],
        "marks": [("MARSEILLE", 43.30, 5.37, None), ("TUNIS", 36.81, 10.18, "L'ARRIVÉE")],
        "nights": [{"day": 1, "name": "À bord du ferry", "type": "hut"}],
        "beats": [
            ("climb", "L'embarquement", "Les vans passent la douane du port, puis montent à bord.",
             "La ligne est tenue par Corsica Linea et CTN (Ferryhopper)."),
            ("night", "La nuit en mer", "Une nuit entière à bord, le van dans la cale.",
             "La traversée dure de 22 à 26 heures selon le navire (Ferryhopper)."),
            ("top", "L'arrivée à La Goulette", "Le port de Tunis. La famille attend de l'autre côté.",
             "La Goulette est le port de Tunis (Ferryhopper)."),
        ],
        "season": {"best": "Hors vacances d'été, les ferries sont moins chargés.",
                   "avoid": "Les vacances d'été et les fêtes, quand toute la diaspora rentre en même temps."},
        "seasonShort": "Oct to May",
        "facts": [
            "La traversée Marseille - Tunis dure de 22 à 26 heures selon le navire (Ferryhopper).",
            "Deux compagnies tiennent la ligne : Corsica Linea et CTN (Ferryhopper).",
        ],
    },
    {
        "key": "inca", "cat": "day",
        "fullName": "Marseille → Oran, en ferry",
        "name": "Marseille → Oran", "line2": "par la mer",
        "country": "Algérie", "countryShort": "DZ",
        "days": 2, "daysLabel": "1 NUIT", "kmLabel": "28 H EN MER",
        "big": "28 h", "bigK": "de traversée, Algérie Ferries", "coverK": "MARSEILLE",
        "line": "Une seule compagnie, Algérie Ferries, et environ 28 heures de mer.",
        "nightLabel": "À bord",
        "sea": True,
        "points": [
            ("Port de Marseille", 43.33, 5.35),
            ("Entre Majorque et Minorque", 39.75, 3.60),
            ("Au large de l'Algérie", 36.90, 0.80),
            ("Port d'Oran", 35.71, -0.64),
        ],
        "marks": [("MARSEILLE", 43.30, 5.37, None), ("ORAN", 35.70, -0.64, "L'ARRIVÉE")],
        "nights": [{"day": 1, "name": "À bord du ferry", "type": "hut"}],
        "beats": [
            ("climb", "L'embarquement", "Les vans passent la douane du port, puis montent à bord.",
             "Algérie Ferries est la seule compagnie sur la ligne (aFerry)."),
            ("night", "La nuit en mer", "Plus d'une journée de mer, en passant par les Baléares.",
             "La traversée dure de 28 à 29 heures (aFerry)."),
            ("top", "L'arrivée à Oran", "Le port d'Oran. Le van sort de la cale, la livraison commence.",
             "Algérie Ferries relie Marseille à Oran (aFerry)."),
        ],
        "season": {"best": "Hors vacances d'été, les ferries sont moins chargés.",
                   "avoid": "Les vacances d'été et les fêtes, quand toute la diaspora rentre en même temps."},
        "seasonShort": "Oct to May",
        "facts": [
            "La traversée Marseille - Oran dure de 28 à 29 heures (aFerry).",
            "Une seule compagnie tient la ligne : Algérie Ferries (aFerry).",
        ],
    },
    {
        "key": "torres", "cat": "multi",
        "fullName": "Paris → Tanger, par l'Espagne",
        "name": "Paris → Tanger", "line2": "par l'Espagne et le détroit",
        "country": "Maroc", "countryShort": "MA",
        "days": 2, "daysLabel": "2 JOURS", "kmLabel": "1 914 KM",
        "big": "1 914 km", "bigK": "jusqu'à Algésiras, puis 1 h 30 de ferry", "coverK": "FERRY 1 H 30",
        "line": "Deux jours de route jusqu'à Algésiras, puis une heure et demie de ferry jusqu'à Tanger Med.",
        "nightLabel": "Une nuit en route",
        "road_km": (1914.0, "Algésiras"),
        "points": [
            ("Paris", 48.86, 2.35), ("Bordeaux", 44.84, -0.58), ("Irun, la frontière", 43.34, -1.79),
            ("Burgos", 42.34, -3.70), ("Madrid", 40.42, -3.70), ("Cordoue", 37.89, -4.78),
            ("Malaga", 36.72, -4.42), ("Algésiras", 36.13, -5.45), ("Tanger Med", 35.89, -5.50),
            ("Tanger", 35.77, -5.80),
        ],
        "marks": [("PARIS", 48.86, 2.35, None), ("MADRID", 40.42, -3.70, None),
                  ("ALGÉSIRAS", 36.13, -5.45, "LE DÉTROIT"), ("TANGER", 35.77, -5.80, None)],
        "nights": [{"day": 1, "name": "Une nuit en Espagne, souvent vers Madrid", "type": "hut"}],
        "beats": [
            ("climb", "La traversée de l'Espagne", "Irun, puis le plateau castillan jusqu'à Madrid.",
             "Paris - Algésiras : 1 914 km, environ 17 heures de conduite (planderoute.net)."),
            ("night", "La nuit en route", "Une nuit pour couper le trajet, avant la descente vers le sud.",
             "Paris - Algésiras se fait en deux jours, avec une nuit en route."),
            ("top", "Le détroit de Gibraltar", "À Algésiras, le van monte sur le ferry. Une heure et demie plus tard, c'est le Maroc.",
             "Algésiras - Tanger Med : 1 h 30 de traversée (DFDS)."),
        ],
        "season": {"best": "D'octobre à mai, hors fêtes : moins d'attente au port.", "avoid": MARHABA},
        "seasonShort": "Oct to May",
        "facts": [
            "Paris - Algésiras : 1 914 km, environ 17 heures de conduite (planderoute.net).",
            "Algésiras - Tanger Med : 1 h 30 de traversée (DFDS).",
            MARHABA,
        ],
    },
    {
        "key": "kili", "cat": "multi",
        "fullName": "Bruxelles → Nador, par la côte espagnole",
        "name": "Bruxelles → Nador", "line2": "par la côte espagnole",
        "country": "Maroc", "countryShort": "MA",
        "days": 3, "daysLabel": "2 À 3 JOURS", "kmLabel": "2 150 KM",
        "big": "2 150 km", "bigK": "jusqu'à Almería, puis 7 à 11 h de ferry", "coverK": "FERRY 7-11 H",
        "line": "La France, puis toute la côte espagnole jusqu'à Almería, et le ferry pour Nador.",
        "nightLabel": "Une ou deux nuits",
        "road_km": (2150.0, "Almería"),
        "points": [
            ("Bruxelles", 50.85, 4.35), ("Reims", 49.26, 4.03), ("Lyon", 45.76, 4.84),
            ("Montpellier", 43.61, 3.88), ("La Jonquera, la frontière", 42.42, 2.87),
            ("Barcelone", 41.39, 2.17), ("Valence", 39.47, -0.38), ("Murcie", 37.99, -1.13),
            ("Almería", 36.83, -2.46), ("Nador", 35.17, -2.93),
        ],
        "marks": [("BRUXELLES", 50.85, 4.35, None), ("BARCELONE", 41.39, 2.17, None),
                  ("ALMERÍA", 36.83, -2.46, "LE FERRY"), ("NADOR", 35.17, -2.93, None)],
        "nights": [{"day": 1, "name": "Une nuit vers le sud de la France ou la Catalogne", "type": "hut"},
                   {"day": 2, "name": "Souvent la nuit sur le ferry d'Almería", "type": "hut"}],
        "beats": [
            ("climb", "La descente vers le sud", "Lyon, la vallée du Rhône, puis la frontière à La Jonquera.",
             "Bruxelles - Almería : 2 150 km, environ 19 h 40 de conduite (planderoute.net)."),
            ("night", "La côte espagnole", "Barcelone, Valence, Murcie : la Méditerranée sur la gauche.",
             "Le trajet se fait en deux ou trois jours, avec une ou deux nuits."),
            ("top", "Le ferry d'Almería", "À Almería, le van embarque pour Nador.",
             "Almería - Nador : de 7 à 11 heures de traversée selon la compagnie (Ferryhopper)."),
        ],
        "season": {"best": "D'octobre à mai, hors fêtes : moins d'attente au port.", "avoid": MARHABA},
        "seasonShort": "Oct to May",
        "facts": [
            "Bruxelles - Almería : 2 150 km, environ 19 h 40 de conduite (planderoute.net).",
            "Almería - Nador : de 7 à 11 heures de traversée selon la compagnie (Ferryhopper).",
            MARHABA,
        ],
    },
    {
        "key": "everest", "cat": "exp",
        "fullName": "Amsterdam → Agadir, le grand trajet",
        "name": "Amsterdam → Agadir", "line2": "le grand trajet",
        "country": "Maroc", "countryShort": "MA",
        "days": 4, "daysLabel": "3 À 4 JOURS", "kmLabel": "≈ 3 200 KM",
        "big": "≈ 3 200 km", "bigK": "de route, avec 1 h 30 de ferry au détroit", "coverK": "FERRY 1 H 30",
        "line": "De la mer du Nord au Souss : l'Europe de haut en bas, le détroit, puis tout le Maroc.",
        "nightLabel": "Deux ou trois nuits",
        "road_km": (2428.0, "Algésiras"),
        "after_km": (791.0, "Tanger Med", "Agadir"),
        "points": [
            ("Amsterdam", 52.37, 4.90), ("Bruxelles", 50.85, 4.35), ("Paris", 48.86, 2.35),
            ("Bordeaux", 44.84, -0.58), ("Irun, la frontière", 43.34, -1.79), ("Madrid", 40.42, -3.70),
            ("Algésiras", 36.13, -5.45), ("Tanger Med", 35.89, -5.50), ("Rabat", 34.02, -6.84),
            ("Casablanca", 33.57, -7.59), ("Marrakech", 31.63, -8.00), ("Agadir", 30.42, -9.60),
        ],
        "marks": [("AMSTERDAM", 52.37, 4.90, None), ("MADRID", 40.42, -3.70, None),
                  ("ALGÉSIRAS", 36.13, -5.45, "LE DÉTROIT"), ("AGADIR", 30.42, -9.60, None)],
        "nights": [{"day": 1, "name": "Une nuit en France", "type": "hut"},
                   {"day": 2, "name": "Une nuit en Espagne", "type": "hut"},
                   {"day": 3, "name": "Une nuit au Maroc, selon les livraisons", "type": "hut"}],
        "beats": [
            ("climb", "L'Europe de haut en bas", "Pays-Bas, Belgique, France, Espagne : quatre pays avant la mer.",
             "Amsterdam - Algésiras : 2 428 km, environ 22 h 40 de conduite (1map.com)."),
            ("night", "Le détroit", "À Algésiras, le van monte sur le ferry pour Tanger Med.",
             "Algésiras - Tanger Med : 1 h 30 de traversée (DFDS)."),
            ("top", "Le Souss", "Rabat, Casablanca, Marrakech, puis Agadir.",
             "Tanger - Agadir : 791 km, environ 8 heures de route (distancede.com)."),
        ],
        "season": {"best": "D'octobre à mai, hors fêtes : moins d'attente au port.", "avoid": MARHABA},
        "seasonShort": "Oct to May",
        "facts": [
            "Amsterdam - Algésiras : 2 428 km, environ 22 h 40 de conduite (1map.com).",
            "Tanger - Agadir : 791 km, environ 8 heures de route (distancede.com).",
            MARHABA,
        ],
    },
]

KIT = [
    {"item": "La liste de ce que tu envoies", "why": "Le transporteur la vérifie au chargement."},
    {"item": "Des cartons solides et fermés", "why": "Le van est chargé jusqu'au toit."},
    {"item": "Le nom et le numéro de la personne qui reçoit", "why": "C'est elle que le transporteur appelle à l'arrivée."},
]
PERMITS = [
    "Chaque transporteur gère sa traversée et ses papiers.",
    "Drari met en relation : le prix et les conditions se fixent entre toi et le transporteur.",
]


def haversine(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(h))


def main(npz_path, out_path):
    d = np.load(npz_path)
    alt = d["alt"].reshape(1081, 2161).astype("f8")

    def elev(lat, lon):
        r = (90.0 - lat) * 6.0
        c = ((lon % 360.0) + 360.0) % 360.0 * 6.0
        r0, c0 = int(r), int(c)
        fr, fc = r - r0, c - c0
        v = (alt[r0, c0] * (1 - fc) + alt[r0, c0 + 1] * fc) * (1 - fr) + (alt[r0 + 1, c0] * (1 - fc) + alt[r0 + 1, c0 + 1] * fc) * fr
        return max(0, int(round(v / 10.0) * 10))

    out = []
    for n, r in enumerate(ROUTES, 1):
        pts = r["points"]
        seg = [0.0] + [haversine(pts[i][1:], pts[i + 1][1:]) for i in range(len(pts) - 1)]
        cum = np.cumsum(seg)
        names = [p[0] for p in pts]
        km = cum.copy()
        if "road_km" in r:  # met à l'échelle la partie route sur la distance sourcée
            total, upto = r["road_km"]
            j = names.index(upto)
            km[: j + 1] = cum[: j + 1] * (total / cum[j])
            for i in range(j + 1, len(pts)):
                km[i] = km[i - 1] + seg[i]
            if "after_km" in r:
                total2, a, b = r["after_km"]
                ia, ib = names.index(a), names.index(b)
                part = cum[ia: ib + 1] - cum[ia]
                km[ia: ib + 1] = km[ia] + part * (total2 / part[-1])
        sea = r.get("sea", False)
        wps = []
        for (name, la, lo), k in zip(pts, km):
            m = 0 if sea else elev(la, lo)
            wps.append({"name": name, "lat": la, "lon": lo, "m": m, "km": round(float(k), 1)})
        hi = max(wps, key=lambda w: w["m"])
        t = {
            "n": n, "key": r["key"], "cat": r["cat"], "fullName": r["fullName"], "name": r["name"],
            "line2": r["line2"], "country": r["country"], "countryShort": r["countryShort"],
            "days": r["days"], "daysLabel": r["daysLabel"], "km": int(round(km[-1])), "kmLabel": r["kmLabel"],
            "big": r["big"], "bigK": r["bigK"], "coverK": r["coverK"],
            "start": {"name": wps[0]["name"], "m": wps[0]["m"]},
            "end": {"name": wps[-1]["name"], "m": wps[-1]["m"]},
            "high": {"name": hi["name"], "m": 0},
            "ascent": 0, "descent": 0,
            "nightLabel": r["nightLabel"],
            "nights": [dict(x, m=0) for x in r["nights"]],
            "beats": [{"key": b[0], "name": b[1], "m": 0, "day": i + 1, "line": b[2], "fact": b[3]}
                      for i, b in enumerate(r["beats"])],
            "season": r["season"], "seasonShort": r["seasonShort"],
            "permits": PERMITS, "price": {"low": 0, "high": 0}, "group": {"min": 1, "max": 12},
            "facts": r["facts"], "kit": KIT, "line": r["line"],
            "marks": [dict({"label": m[0], "lat": m[1], "lon": m[2]}, **({"red": True, "sub": m[3]} if m[3] else {}))
                      for m in r["marks"]],
            "summit": None,
            "profile": [[w["km"], w["m"]] for w in wps],
            "waypoints": wps,
        }
        out.append(t)
        print(r["name"], "km", t["km"], "waypoints", [(w["name"], w["km"], w["m"]) for w in wps][:4], "...")
    js = ("/* Les 5 trajets Drari. Généré par tools/make_routes.py, ne pas modifier à la main.\n"
          "   Les sources des chiffres sont en tête de tools/make_routes.py. */\n"
          "window.TREKS=" + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n")
    open(out_path, "w", encoding="utf-8").write(js)
    print("ok", out_path, len(js))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
