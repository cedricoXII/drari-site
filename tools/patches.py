"""Les remplacements appliqués au template par tools/build.py.

Chaque entrée : (texte d'origine, texte Drari[, nombre d'occurrences attendu]).
Les apostrophes des textes sont typographiques (’) : beaucoup de textes sont dans des
chaînes JavaScript entre apostrophes droites.
v0.2 : l'en-tête, le haut de page (les 5 cartes, le globe, le panneau du trajet) et le menu.
v0.3 : le bas de page (traversées, inclus, transporteurs, quand partir, FAQ, inscription, pied de page).
"""
import os
from sections_fr import SEC_B, SEC_J, SEC_T, SEC_I, SEC_Q, MONTHS_FR_SHORT, MONTHS_FR_CAP, VAN_ICON, BUBBLE_ICON
from scenery_fr import VAN_HIKER, VAN_CSS, NEW_SHAPES, LENGTHS, FOOT_CAMP_NEW, TABLE_VAN

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
    (_between('<div class="fx-camp" aria-hidden="true"><svg viewBox="0 0 220 90">', '</svg></div>'), FOOT_CAMP_NEW),

    # ---- 04 · Quand partir (sections/when.js)
    ('f=["January","February","March","April","May","June","July","August","September","October","November","December"]', 'f=' + MONTHS_FR_CAP),
    ('season:e.seasonShort', 'season:e.seasonLabel||e.seasonShort'),
    ('r.name+": "+r.season+". Not outside it: "+r.avoid.replace(/"/g,"")', 'r.name+" : "+r.season+". En dehors : "+r.avoid.replace(/"/g,"")'),
    ('<span>Today</span>', '<span>Aujourd’hui</span>'),
    ('f[d]+": "+(i.length?i.join(" and ")+(i.length>1?" are":" is")+" in season.":"nothing in season, a good month to plan.")',
     'f[d]+" : "+(i.length?(i.length===e.length?"tous les trajets sont en période calme.":i.join(" et ")+(i.length>1?" sont":" est")+" en période calme."):"haute saison, réserve tôt.")'),
    ('(n%2?1.2:-1.2)+\'deg">\'+r+"</b>").join("")', '(n%2?1.2:-1.2)+\'deg">\'+' + MONTHS_FR_SHORT + '[n]+"</b>").join("")'),
    ('kick:"When to go",eyebrow:"When to go",flow:!0,cls:"wopt wo-ribbons",title:["Every trek keeps","<em>its own calendar.</em>"],lede:"These are the months we run each one. Outside them we leave the mountain alone, for snow, for rain or for the monsoon."',
     'kick:"Quand partir",eyebrow:"Quand partir",flow:!0,cls:"wopt wo-ribbons",title:["Chaque trajet","<em>a son calendrier.</em>"],lede:"Les bandes montrent les mois les plus calmes. L’été, la diaspora rentre au pays : les ports sont pleins, réserve tôt."'),

    # ---- 05 · FAQ (sections/faq.js) : la carte et ses épingles sur les destinations
    ('const f=(t.waypoints||[])[0]||{},p=e.catOf(t)', 'const f=(t.waypoints||[]).slice(-1)[0]||{},p=e.catOf(t)'),
    ('d=t=>t.group.min+" to "+t.group.max', 'd=t=>t.group.min+" à "+t.group.max'),
    ('kick:"Ready for it?",eyebrow:"Ready for it?",flow:!0,cls:"faqmap",title:["How hard,","<em>how high.</em>"],lede:"None of the five needs climbing gear in season. All of them need legs that have done a few long days first."',
     'kick:"Des questions ?",eyebrow:"Des questions ?",flow:!0,cls:"faqmap",title:["Combien,","<em>comment, quand.</em>"],lede:"Les questions qu’on nous pose le plus, côté transporteurs et côté familles."'),

    # ---- Inscription (sections/book.js) : le ticket du transporteur
    ('m=["January","February","March","April","May","June","July","August","September","October","November","December"]', 'm=' + MONTHS_FR_CAP),
    ('on:c.months(t.seasonShort)', 'on:c.months("Jan to Dec")'),
    ('mo:e>=0?m[e]:"Any month"', 'mo:e>=0?m[e]:"Tous les mois"'),
    ('a.title=s?m[o]:m[o]+": not in season, we leave the mountain alone"', 'a.title=m[o]'),
    ('!n.name||!/.+@.+\\..+/.test(n.mail)', '!n.name||!/.+@.+\\..+|^[+0-9 ().-]{8,}$/.test(n.mail)'),
    ('We need a name and an email to write back to.', 'Il nous faut ton prénom, et un email ou un téléphone pour te répondre.', 2),
    ('"Thanks, "+n.name.split(" ")[0]+". We write back about the "+i.full+(n.m>=0?" in "+m[n.m]:"")+" within two working days, with dates, a price and your map."',
     '"Merci, "+n.name.split(" ")[0]+". Ton ticket "+i.full+(n.m>=0?" en "+m[n.m].toLowerCase():"")+" est prêt. Version de test : rien n’est encore envoyé."'),
    ('aria-label="\'+o+(o===1?" walker":" walkers")', 'aria-label="\'+o+(o===1?" départ par mois":" départs par mois")'),
    (_between('D=\'<svg viewBox="0 0 24 40" aria-hidden="true"><circle cx="12" cy="5" r="4.2"/>', '</svg>\';function h(){'),
     "D='" + VAN_ICON + "';function h(){"),
    ('c.MON.map((o,s)=>\'<button type="button" data-mo="\'+s+\'" aria-label="\'+m[s]+\'"><span>\'+o+"</span></button>")',
     'c.MON.map((o,s)=>\'<button type="button" data-mo="\'+s+\'" aria-label="\'+m[s]+\'"><span>\'+' + MONTHS_FR_SHORT + '[s]+"</span></button>")'),
    ('<p class="bt-top"><span>Fold Line</span><span>Walker’s ticket</span>', '<p class="bt-top"><span>Drari</span><span>Ticket transporteur</span>'),
    ('<p class="bo-lab" id="btTrek">Trek</p>', '<p class="bo-lab" id="btTrek">Trajet</p>'),
    ('<p class="bo-lab" id="btMonth">Month</p>', '<p class="bo-lab" id="btMonth">Mois de départ</p>'),
    ('<p class="bo-lab" id="btWalk">Walkers</p>', '<p class="bo-lab" id="btWalk">Départs par mois</p>'),
    ('<label class="bo-in"><span>Your name</span>', '<label class="bo-in"><span>Ton prénom</span>'),
    ('<label class="bo-in"><span>Email</span><input name="email" type="email" autocomplete="email" spellcheck="false"></label>',
     '<label class="bo-in"><span>Email ou téléphone</span><input name="email" type="text" autocomplete="email" spellcheck="false"></label>'),
    ('data-again>Punch another ticket</button>', 'data-again>Refaire un ticket</button>'),
    ('aria-label="Tear off the stub to send the enquiry"', 'aria-label="Détache le talon pour envoyer ton inscription"'),
    ('<span class="bt-l bt-lm"><em>Month</em><i data-f="mo">Any month</i></span>', '<span class="bt-l bt-lm"><em>Mois</em><i data-f="mo">Tous les mois</i></span>'),
    ('<span class="bt-l bt-lw"><em>Walkers</em><i data-f="n">2</i></span>', '<span class="bt-l bt-lw"><em>Départs</em><i data-f="n">2</i></span>'),
    ('<span class="bt-l"><em>From</em><i>USD <i data-f="est">\'+L(a.price*2)+\'</i></i></span>', '<span class="bt-l"><em>Inscription</em><i>Gratuite</i></span>'),
    ('Tear here to send</span>', 'Détache ici pour envoyer</span>'),
    ('kick:"Book",eyebrow:"Your turn",flow:!0,cls:"bopt bo-ticket",title:["Pick a map.","<em>We do the folding.</em>"],lede:"Punch in the trek, the month and how many of you. Tear off the stub and we write back within two working days."',
     'kick:"Inscription",eyebrow:"À toi",flow:!0,cls:"bopt bo-ticket",title:["Inscris ton trajet.","<em>C’est gratuit.</em>"],lede:"Choisis ton trajet, tes mois de départ et combien de fois tu pars. Laisse ton prénom et un moyen de te joindre, puis détache le talon."'),
    ('i("name","Ana Ruiz"),await b(250),await i("email","ana@example.com")', 'i("name","Karim"),await b(250),await i("email","karim@exemple.fr")'),

    # ---- Pied de page (sections/footer.js)
    ('C={tongariro:"Pacific/Auckland",inca:"America/Lima",torres:"America/Punta_Arenas",kili:"Africa/Dar_es_Salaam",everest:"Asia/Kathmandu"}',
     'C={tongariro:"Africa/Tunis",inca:"Africa/Algiers",torres:"Africa/Casablanca",kili:"Africa/Casablanca",everest:"Africa/Casablanca"}'),
    ('F="hello@foldline.example",z="@foldline"', 'F="bonjour@drari.example",z="@drari"'),
    (_between('strava:\'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 15 L10.2 4 L15.4 15"', "</svg>'},S=[{k:\"instagram\""),
     "strava:'" + BUBBLE_ICON + "'},S=[{k:\"instagram\""),
    ('S=[{k:"instagram",name:"Instagram",line:"Trail days, every day",c:"#D2A23A"},{k:"youtube",name:"YouTube",line:"The five walks, filmed end to end",c:"#D63B2F"},{k:"tiktok",name:"TikTok",line:"Sixty seconds on a ridge",c:"#5B8FC4"},{k:"strava",name:"Strava",line:"Our guides’ routes, live in season",c:"#5E8C61"}]',
     'S=[{k:"instagram",name:"Instagram",line:"Les départs de la semaine",c:"#D2A23A"},{k:"youtube",name:"YouTube",line:"Les trajets, filmés de bout en bout",c:"#D63B2F"},{k:"tiktok",name:"TikTok",line:"Une traversée en 60 secondes",c:"#5B8FC4"},{k:"strava",name:"WhatsApp",line:"Le groupe des transporteurs",c:"#5E8C61"}]'),
    ('aria-label="Fold Line on \'+e.name+\' (placeholder)"', 'aria-label="Drari sur \'+e.name+\' (compte à créer)"'),
    ('const n=(e.waypoints||[])[0];return\'<li data-tz="', 'const n=(e.waypoints||[]).slice(-1)[0];return\'<li data-tz="'),
    ('<p class="fx-k">Fold Line post</p><h3>A map in your inbox, <em>once a month.</em></h3><p class="fx-p">One trek, folded into an email: the route, the season that is opening and a note from a guide on the trail. Nothing else. We are mostly outside.</p>',
     '<p class="fx-k">Le courrier Drari</p><h3>Les nouveaux trajets, <em>une fois par mois.</em></h3><p class="fx-p">Un email par mois : les transporteurs qui arrivent, les trajets qui ouvrent et les dates à retenir. Rien d’autre.</p>'),
    ('placeholder="your@email" aria-label="Your email"', 'placeholder="ton@email" aria-label="Ton email"'),
    ('<button type="submit">Send me maps<i aria-hidden="true">→</i></button>', '<button type="submit">Recevoir les trajets<i aria-hidden="true">→</i></button>'),
    ('<span>Fold Line<br>post</span>', '<span>Courrier<br>Drari</span>'),
    ('toLocaleDateString("en-GB",{day:"2-digit",month:"short"})', 'toLocaleDateString("fr-FR",{day:"2-digit",month:"short"})'),
    ('<em>Follow the walks</em><b>\'+z+\', everywhere</b>', '<em>Suis les trajets</em><b>\'+z+\', partout</b>'),
    ('<p class="fx-h">Follow the walks</p>', '<p class="fx-h">Suis les trajets</p>'),
    ('<p class="fx-h">Right now at the trailheads</p>', '<p class="fx-h">En ce moment, à l’arrivée</p>'),
    ('aria-label="Fold Line">\'+y("Fold","a")+y("Line","b")', 'aria-label="Bon trajet">\'+y("Bon","a")+y("trajet","b")'),
    ('<p>End of the trail. Camp is up, the fire is lit.</p>', '<p>Fin du trajet. Tout le monde est bien arrivé.</p>'),
    ('>Back to the trailhead<i', '>Retour au départ<i'),
    ('<p class="fx-h">Talk to us</p>', '<p class="fx-h">Nous écrire</p>'),
    ('<p>We answer within two working days, from Ōhakune, New Zealand, where the first map was folded.</p>',
     '<p>Une question, une idée de trajet, un souci ? Écris-nous.</p>'),
    ('"That email does not look right yet."', '"Cet email n’a pas l’air bon."'),
    ('"Stamped. Your first map lands on the first of the month."', '"Merci ! Version de test : l’envoi n’est pas encore branché."'),
    ('"In season":"Out of season"', '"Mois calme":"Haute saison"'),
    ('"Open now, Mon to Fri, 8 to 6 NZ time":"Closed now. Mon to Fri, 8 to 6 NZ time"', '"Lancement en cours":"Lancement en cours"'),

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
     'const p=[{i:-1,label:"Trajets",short:"Trajets"},{i:0,label:"Traversées",short:"Traversées"},{i:1,label:"Inclus",short:"Inclus"},{i:2,label:"Transporteurs",short:"Transp."},{i:3,label:"Quand partir",short:"Quand"},{i:4,label:"FAQ",short:"FAQ"},{i:5,label:"Inscription",short:"Inscription",chip:!0}]'),
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
    ('d.hint="Scroll down for lengths, guides and dates"', 'd.hint="Fais défiler : traversées, transporteurs et dates"'),
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
