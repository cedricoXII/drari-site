"""Les remplacements appliqués au template par tools/build.py.

Chaque entrée : (texte d'origine, texte Drari[, nombre d'occurrences attendu]).
Les apostrophes des textes sont typographiques (’) : beaucoup de textes sont dans des
chaînes JavaScript entre apostrophes droites.
v0.2 : l'en-tête, le haut de page (les 5 cartes, le globe, le panneau du trajet) et le menu.
v0.3 : le bas de page (traversées, inclus, transporteurs, quand partir, FAQ, inscription, pied de page).
v0.4 : les décors (la camionnette, le ferry, le rocher, l'Atlas, la maison du pied de page).
v0.5 : les textes transporteurs, le haut de page en HTML, un seul bouton, le ticket, les tailles de texte,
       le téléphone, la vitesse et les balises de partage : voir tools/patches_v05.py et tools/v05/.
"""
import os
from sections_fr import SEC_B, SEC_J, SEC_T, SEC_I, SEC_Q
from scenery_fr import VAN_HIKER, VAN_CSS, NEW_SHAPES, LENGTHS, TABLE_VAN
from patches_v05 import PATCHES_V05, HEAD_V05

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
    # ---- Bas de page, sections/sections.js : fonctions remplacées en entier (avant tout autre remplacement)
    (_between('function B(){const t={day:[],multi:[],exp:[]};', 'function j(){', include_end=False), SEC_B),
    (_between('function j(){', 'const T=[{key:"tongariro"', include_end=False), SEC_J),
    (_between('const T=[{key:"tongariro"', ',D="#1B2230";function W(', include_end=False), SEC_T),
    (_between('function I(){const t=[-2.2,1.6,-1.2,2.4,1.8,-2.6,1.1,-1.6],', 'function P(){const t=window.WHEN_STOP', include_end=False), SEC_I),
    (_between('function Q(){const t=f.map(i=>r(v(i.high.name)', 'function C(){if(window.BOOK_STOP)', include_end=False), SEC_Q),
    # la famille d'un trajet : lue dans les données (cat)
    ('y=t=>x.cats[z(t.days)]', 'y=t=>x.cats[t.cat||z(t.days)]'),
    # les panneaux sur la table de la section 01
    ('[["1 DAY",-2.9],["2 TO 4 DAYS",0],["5 DAYS AND OVER",2.9]]', '[["PAR LA MER",-2.9],["PAR LE DÉTROIT",0],["TOUTE LA ROUTE",2.9]]'),

    # ---- v0.4 · Décors : la camionnette à la place du randonneur, ferry, rocher, maisons (tools/scenery_fr.py)
    (_between('function R(){const t=document.createElement("div");t.className="hk"', 'window.SECTIONS={', include_end=False), VAN_HIKER),
    ('.hk .sh{fill:rgba(0,0,0,0.38);stroke:none;}', VAN_CSS),
    ('const d={hill:(e,l,t)=>{', NEW_SHAPES + 'hill:(e,l,t)=>{'),
] + [tuple(x) for x in LENGTHS] + [
    # le rocher de Gibraltar : plus large que haut
    ('x:o*.4,z:-2.35,w:1.9,h:2.8,col:"#8C6A2C",shape:d.rock', 'x:o*.4,z:-2.35,w:2.7,h:1.9,col:"#8C6A2C",shape:d.rock'),
    # la camionnette en papier sur la table, à la place du randonneur
    (_between('function Ao(e){return function(t,o,n,l){', '}}const Tt=[],fe=.014;', include_end=False), TABLE_VAN),
    # v0.5 : le pied de page (sections/footer.js) et « Quand partir » (sections/when.js) sont réécrits en entier,
    # voir tools/v05/footer.js et tools/v05/price.js

    # ---- 05 · FAQ (sections/faq.js) : la carte et ses épingles sur les destinations
    ('const f=(t.waypoints||[])[0]||{},p=e.catOf(t)', 'const f=(t.waypoints||[]).slice(-1)[0]||{},p=e.catOf(t)'),
    ('d=t=>t.group.min+" to "+t.group.max', 'd=t=>t.group.min+" à "+t.group.max'),
    ('kick:"Ready for it?",eyebrow:"Ready for it?",flow:!0,cls:"faqmap",title:["How hard,","<em>how high.</em>"],lede:"None of the five needs climbing gear in season. All of them need legs that have done a few long days first."',
     'kick:"Des questions ?",eyebrow:"Des questions ?",flow:!0,cls:"faqmap",title:["Combien,","<em>comment, quand.</em>"],lede:"Les questions que posent les transporteurs."'),

    # ---- Inscription : le ticket est réécrit en entier en v0.5 (tools/v05/book.js) ; ici, le texte d'erreur de l'ancien
    # formulaire anglais de sections/landing.js (jamais affiché, gardé pour ne rien casser)
    ('We need a name and an email to write back to.', 'Il nous faut ton prénom, et un email ou un téléphone pour te répondre.'),

    # ---- <head>
    ('<html lang="en" class="hero-on" data-hero="fold">', '<html lang="fr" class="hero-on" data-hero="fold">'),
    # v0.2 : la plongée dans l'épingle (la balade en 3D) n'est pas encore adaptée aux routes, donc on la coupe
    # v0.5 : titre, description, aperçus WhatsApp / Facebook (Open Graph), couleur du navigateur, icônes (tools/v05/head.html)
    ('<title>Fold Line · Guided treks, folded</title>', HEAD_V05 + '\n<style>.fo-explore{display:none!important}</style>'),
    # v0.5 : la plongée dans la carte (?interior=story) est retirée, avec ses modules
    ('Ee=Qe==="none"?null:Qe||"story"', 'Ee=null'),
    ('<meta name="description" content="Fold Line, guided treks and expeditions since 2011. Every trek comes with its own folded pocket map. Five to start with: Tongariro, the Inca Trail, the W Trek, Kilimanjaro and Everest Base Camp." />\n', ''),
    # les trois familles de trajets (couleurs du template gardées)
    ('cats:{day:{name:"Day walk",color:"#5E8C61"},multi:{name:"Multi-day",color:"#D2A23A"},exp:{name:"Expedition",color:"#5B8FC4"}}',
     'cats:{day:{name:"Ferry direct",color:"#5E8C61"},multi:{name:"Route + détroit",color:"#D2A23A"},exp:{name:"Grande route",color:"#5B8FC4"}}', 2),

    # ---- En-tête
    ('aria-label="Fold Line, back to the top"', 'aria-label="Drari, retour en haut"'),
    (_between('<span class="brand-mark" aria-hidden="true">', '</svg></span>'), BRAND_MARK),
    ('<span class="brand-name">Fold Line</span>', '<span class="brand-name">Drari</span>'),
    ('<span class="bt-label">Book a trek</span>', '<span class="bt-label">Inscrire mon trajet</span>'),
    ('x.textContent="Book a trek"', 'x.textContent="Inscrire mon trajet"'),
    ('document.title=s.name+" · Guided treks, folded"', 'document.title=s.name+" · Transporteurs Europe-Maghreb : inscris ton trajet"'),

    # ---- Menu
    ('const p=[{i:-1,label:"Treks",short:"Treks"},{i:0,label:"Lengths",short:"Lengths"},{i:1,label:"Included",short:"Included"},{i:2,label:"Guides",short:"Guides"},{i:3,label:"When to go",short:"When"},{i:4,label:"FAQ",short:"FAQ"},{i:5,label:"Book",short:"Book",chip:!0}]',
     'const p=[{i:-1,label:"Trajets",short:"Trajets"},{i:0,label:"Le métier",short:"Le métier"},{i:1,label:"Inclus",short:"Inclus"},{i:2,label:"Ta carte",short:"Ta carte"},{i:3,label:"Gratuit ?",short:"Gratuit ?"},{i:4,label:"FAQ",short:"FAQ"},{i:5,label:"Inscription",short:"Inscription",chip:!0}]'),
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
    ('d.hint="Scroll down for lengths, guides and dates"', 'd.hint="Fais défiler : le métier, ce qui est inclus, ta carte"'),
    ('d.tip="Swipe or tap a number to turn the table"', 'd.tip="Glisse ou touche un numéro pour tourner la table"'),
    # le grand chiffre du panneau : la distance (ou la durée du ferry) au lieu de l'altitude
    ('const Uo=e=>zt(xe[e].summit.m)', 'const Uo=e=>ce[e]&&ce[e].big?ce[e].big:zt(xe[e].summit.m)'),
    ('Go=e=>"<b>"+ve(xe[e].summit.name)+"</b>&nbsp;· "+xe[e].summit.kind+"&nbsp;· "+xe[e].n+"&nbsp;cards, "+xe[e].step+"&nbsp;m&nbsp;apart"',
     'Go=e=>ce[e]&&ce[e].bigK?"<b>"+ve(ce[e].bigK)+"</b>":"<b>"+ve(xe[e].summit.name)+"</b>&nbsp;· "+xe[e].summit.kind+"&nbsp;· "+xe[e].n+"&nbsp;couches, "+xe[e].step+"&nbsp;m&nbsp;d’écart"'),
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
] + PATCHES_V05
