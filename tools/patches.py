"""Les remplacements appliqués au template par tools/build.py.

Chaque entrée : (texte d'origine, texte Drari[, nombre d'occurrences attendu]).
Les apostrophes des textes sont typographiques (’) : beaucoup de textes sont dans des
chaînes JavaScript entre apostrophes droites.
v0.2 : l'en-tête, le haut de page (les 5 cartes, le globe, le panneau du trajet) et le menu.
Le reste de la page est encore celui du template : prochaine étape.
"""
import os

_BASE = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "base", "fold-line-v7.html"),
             encoding="utf-8").read()


def _between(start, end, include_end=True):
    """Le texte exact du template entre deux repères (pour les longs blocs)."""
    i = _BASE.index(start)
    j = _BASE.index(end, i) + (len(end) if include_end else 0)
    return _BASE[i:j]


BRAND_MARK = (
    '<span class="brand-mark" aria-hidden="true"><svg viewBox="0 0 50 42" focusable="false">'
    '<defs><filter id="fl-sh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="1.3" dy="0.2" stdDeviation="0.8" flood-color="#2a1a0c" flood-opacity="0.6"/></filter></defs>'
    '<g transform="translate(1 1)" filter="url(#fl-sh)">'
    '<path d="M2 10 L16.5 6 L16.5 35 L2 39 Z" fill="#F4EEE3"/>'
    '<path d="M16.5 6 L31 10 L31 39 L16.5 35 Z" fill="#E2D2B4"/>'
    '<path d="M31 10 L45.5 6 L45.5 35 L31 39 Z" fill="#F4EEE3"/>'
    '<path d="M7 31 C 14 29, 15 22, 22 21 S 33 18, 38 13.5" fill="none" stroke="#C8432B" stroke-width="1.6" stroke-dasharray="2.4 1.8" stroke-linecap="round"/>'
    '<circle cx="38.6" cy="12.6" r="3" fill="#C8432B"/>'
    '</g></svg></span>'
)

PATCHES = [
    # ---- Photos des guides : servies par ce dépôt (adresse injectée par la page Aura)
    ("https://cdn.jsdelivr.net/gh/Sam1983Aing/aura-assets@1.18.0/foldline/guides/", "__DRARI_BASE__guides/"),
    ("https://raw.githubusercontent.com/Sam1983Aing/aura-assets/1.18.0/foldline/guides/", "__DRARI_RAW__guides/"),

    # ---- <head>
    ('<html lang="en" class="hero-on" data-hero="fold">', '<html lang="fr" class="hero-on" data-hero="fold">'),
    # v0.2 : la plongée dans l'épingle (la balade en 3D) n'est pas encore adaptée aux routes, donc on la coupe
    ('<title>Fold Line · Guided treks, folded</title>',
     '<title>Drari · Transporteurs Europe-Maghreb</title>\n<style>.fo-explore{display:none!important}</style>'),
    ('Ee=Qe==="none"?null:Qe||"story"', 'Ee=Qe==="story"?"story":null'),
    ('<meta name="description" content="Fold Line, guided treks and expeditions since 2011. Every trek comes with its own folded pocket map. Five to start with: Tongariro, the Inca Trail, the W Trek, Kilimanjaro and Everest Base Camp." />',
     '<meta name="description" content="Drari relie les petits transporteurs Europe-Maghreb aux familles de la diaspora. Trajets, dates et prix affichés. Gratuit pour tous." />'),
    # les trois familles de trajets (couleurs du template gardées)
    ('cats:{day:{name:"Day walk",color:"#5E8C61"},multi:{name:"Multi-day",color:"#D2A23A"},exp:{name:"Expedition",color:"#5B8FC4"}}',
     'cats:{day:{name:"Ferry direct",color:"#5E8C61"},multi:{name:"Route + détroit",color:"#D2A23A"},exp:{name:"Grande route",color:"#5B8FC4"}}', 2),

    # ---- En-tête
    ('aria-label="Fold Line, back to the top"', 'aria-label="Drari, retour en haut"'),
    (_between('<span class="brand-mark" aria-hidden="true">', '</svg></span>'), BRAND_MARK),
    ('<span class="brand-name">Fold Line</span>', '<span class="brand-name">Drari</span>'),
    ('<span class="bt-label">Book a trek</span>', '<span class="bt-label">Inscris ton trajet</span>'),
    ('x.textContent="Book a trek"', 'x.textContent="Inscris ton trajet"'),
    ('document.title=s.name+" · Guided treks, folded"', 'document.title=s.name+" · Transporteurs Europe-Maghreb"'),

    # ---- Menu
    ('const p=[{i:-1,label:"Treks",short:"Treks"},{i:0,label:"Lengths",short:"Lengths"},{i:1,label:"Included",short:"Included"},{i:2,label:"Guides",short:"Guides"},{i:3,label:"When to go",short:"When"},{i:4,label:"FAQ",short:"FAQ"},{i:5,label:"Book",short:"Book",chip:!0}]',
     'const p=[{i:-1,label:"Trajets",short:"Trajets"},{i:0,label:"Envois",short:"Envois"},{i:1,label:"Inclus",short:"Inclus"},{i:2,label:"Transporteurs",short:"Transp."},{i:3,label:"Quand partir",short:"Quand"},{i:4,label:"FAQ",short:"FAQ"},{i:5,label:"Inscription",short:"Inscription",chip:!0}]'),
    ('aria-label="Sections, now Treks"><b>00</b><span>Treks</span>', 'aria-label="Sections, ici Trajets"><b>00</b><span>Trajets</span>'),
    ('Sections, now ', 'Sections, ici '),

    # ---- La marque sur les couvertures des cartes
    ('foldline:{name:"Fold Line",cover:"FOLD LINE",sub:"Trekking company",note:"the crease where a printed sheet folds"}',
     'foldline:{name:"Drari",cover:"DRARI",sub:"Europe - Maghreb",note:"les petits transporteurs et les familles, sur la même carte"}'),
    # bas de couverture : la traversée à la place de l'altitude max
    ('r.high&&r.high.m?"MAX "+$(r.high.m).toUpperCase():""', 'r.coverK?r.coverK:r.high&&r.high.m?"MAX "+$(r.high.m).toUpperCase():""'),
    # famille du trajet : lue dans les données (cat) si elle est donnée
    ('a=isFinite(t)?t<=1?"day":t<=4?"multi":"exp":"multi"', 'a=l.cat||(isFinite(t)?t<=1?"day":t<=4?"multi":"exp":"multi")'),

    # ---- Le relief en papier : une couche tous les 200 m, relief très exagéré (cartes de 1 000 à 3 500 km)
    ('Ta={tongariro:{step:50,ve:1.5},inca:{step:50,ve:1},torres:{step:100,ve:1},kili:{step:200,ve:1.5},everest:{step:200,ve:1,win:[.024,.135,.93,.865]}}',
     'Ta={tongariro:{step:200,ve:105},inca:{step:200,ve:122},torres:{step:200,ve:208},kili:{step:200,ve:248},everest:{step:200,ve:348}}'),
    ('sub:C?e===0?"HIGH POINT OF THE CROSSING":"HIGH POINT OF THE TREK":"ON THE ROUTE"', 'sub:_.sub||(C?"POINT HAUT DU TRAJET":"SUR LA ROUTE")'),
    ('kind:"SUMMIT"', 'kind:"SOMMET"'),
    ('"HIGH POINT OF THE TREK":"HIGHEST ON THIS SHEET"', '"POINT HAUT DU TRAJET":"POINT LE PLUS HAUT DE LA CARTE"'),
    ('kind:"TOP CARD"', 'kind:"COUCHE DU HAUT"'),

    # ---- Le haut de page
    (_between('xa=["Over an active volcano', '"],ya=', include_end=False) + '"]',
     'xa=["Une nuit en mer, et le van sort à La Goulette.","Environ 28 heures de mer jusqu’à Oran.",'
     '"Deux jours de route, puis le détroit.","Toute la côte espagnole, puis le ferry pour Nador.",'
     '"L’Europe de haut en bas, puis tout le Maroc."]'),
    ('Ct=["no","one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen","fifteen"]',
     'Ct=["zéro","un","deux","trois","quatre","cinq","six","sept","huit","neuf","dix","onze","douze","treize","quatorze","quinze"]'),
    ('" DAY":" DAYS"', '" JOUR":" JOURS"', 2),
    ('s=o&&n&&Ct[o]&&Ct[n]?"Guided treks and expeditions since 2011. Five to start with, from "+(o===1?"one day":Ct[o]+" days")+" on a volcano to "+Ct[n]+" under Everest.":"Guided treks and expeditions since 2011. Five to start with, from a day on a volcano to the long walk under Everest."',
     's="Drari relie les petits transporteurs Europe-Maghreb aux familles de la diaspora. Tu affiches ta route, ta date et ton prix. C’est gratuit."'),
    ('<span class="x">Every trek</span>', '<span class="x">Ton trajet</span>'),
    ('<span class="x">folds into</span>', '<span class="x">trouve ses</span>'),
    ('<span class="x">a <em class="acc">pocket.</em></span>', '<span class="x"><em class="acc">clients.</em></span>'),
    ('<span>Point at a map to raise it</span>', '<span>Survole une carte pour la soulever</span>'),
    ('<span>Scroll to go in at the pin</span>', '<span>Fais défiler pour la suite</span>'),
    ('<i></i>Tap a map to raise it</p>', '<i></i>Touche une carte pour la soulever</p>'),
    ('aria-label="Featured treks"', 'aria-label="Les trajets"'),
    ('aria-label="Previous trek"', 'aria-label="Trajet précédent"'),
    ('aria-label="Next trek"', 'aria-label="Trajet suivant"'),
    ('d.hint="Scroll down for lengths, guides and dates"', 'd.hint="Fais défiler : envois, transporteurs et dates"'),
    ('d.tip="Swipe or tap a number to turn the table"', 'd.tip="Glisse ou touche un numéro pour tourner la table"'),
    # le grand chiffre du panneau : la distance (ou la durée du ferry) au lieu de l'altitude
    ('const Uo=e=>zt(xe[e].summit.m)', 'const Uo=e=>ce[e]&&ce[e].big?ce[e].big:zt(xe[e].summit.m)'),
    ('Go=e=>"<b>"+ve(xe[e].summit.name)+"</b>&nbsp;· "+xe[e].summit.kind+"&nbsp;· "+xe[e].n+"&nbsp;cards, "+xe[e].step+"&nbsp;m&nbsp;apart"',
     'Go=e=>ce[e]&&ce[e].bigK?"<b>"+ve(ce[e].bigK)+"</b>&nbsp;· relief en "+xe[e].n+"&nbsp;couches":"<b>"+ve(xe[e].summit.name)+"</b>&nbsp;· "+xe[e].summit.kind+"&nbsp;· "+xe[e].n+"&nbsp;couches, "+xe[e].step+"&nbsp;m&nbsp;d’écart"'),
    ('<span class="k">\'+ve(xe[i].summit.name)+"</span>', '<span class="k">\'+ve(c.bigK||xe[i].summit.name)+"</span>'),
    ('const z=_>=1?f.summit.m:f.L0+(f.summit.m-f.L0)*Ke(_);Vo(p,zt(z),Go(p),f.summit.name)',
     'const z=_>=1?f.summit.m:f.L0+(f.summit.m-f.L0)*Ke(_);ce[p]&&ce[p].big?Vo(p,ce[p].big,Go(p),ce[p].bigK):Vo(p,zt(z),Go(p),f.summit.name)'),
    ('"<b>Contour</b>&nbsp;· card&nbsp;"+(je+1)+"&nbsp;of&nbsp;"+f.n+"&nbsp;· under the cursor","CONTOUR · CARD "+(je+1)+" OF "+f.n',
     '"<b>Relief</b>&nbsp;· couche&nbsp;"+(je+1)+"&nbsp;sur&nbsp;"+f.n+"&nbsp;· sous le curseur","RELIEF · COUCHE "+(je+1)+" SUR "+f.n'),
    ('<b>Explore the trail</b><em aria-hidden="true">Go in at the <i>pin</i></em>',
     '<b>Explore le trajet</b><em aria-hidden="true">Entre par l’<i>épingle</i></em>'),
    ('"Explore the trail: go in at the pin and walk the map"', '"Explore le trajet : entre par l’épingle et suis la carte"'),

    # ---- Le globe : l'épingle sur la destination, pas d'autres lieux pour l'instant
    ('const t=n.waypoints&&n.waypoints[0]||{}', 'const t=n.waypoints&&n.waypoints[n.waypoints.length-1]||{}'),
    (_between('H=[["Half Dome, Yosemite"', '];window.FOLD_GLOBE_MORE=H'), 'H=[];window.FOLD_GLOBE_MORE=H'),
]
