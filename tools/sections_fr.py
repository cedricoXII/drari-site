"""Le bas de page Drari : le code JavaScript qui remplace les fonctions de sections/sections.js.

Chaque bloc remplace une fonction entière du template (même structure de sortie, textes Drari).
Les apostrophes sont typographiques (’) : le code est inséré dans du JavaScript minifié.
Règle : pas de faux transporteurs, pas de faux avis, pas de fausse rareté, chiffres sourcés.
"""

# 01 · Traversées (dans le template : « Three kinds of trek »)
SEC_B = (
    'function B(){const t={day:[],multi:[],exp:[]};f.forEach(s=>t[s.cat||z(s.days)].push(s));'
    'const R={day:"Une nuit en mer",multi:"2 à 3 jours",exp:"3 à 4 jours"},'
    'L2={day:"Le van monte sur le ferry à Marseille et sort de l’autre côté de la mer.",'
    'multi:"La route jusqu’au sud de l’Espagne, puis un ferry court.",'
    'exp:"L’Europe de haut en bas, le détroit, puis la route au Maroc."},'
    'X={day:["De 22 à 29 heures de traversée","Départ du port de Marseille","Arrivée à Tunis ou à Oran"],'
    'multi:["Une ou deux nuits en route","Ferry à Algésiras ou à Almería","Arrivée à Tanger ou à Nador"],'
    'exp:["Deux ou trois nuits en route","1 h 30 de ferry au détroit","Arrivée dans le Souss"]},'
    'Y=[-3,2.2,-2];'
    'return{id:"lengths",kick:"Choisis ta traversée",eyebrow:"Premier pas",title:["Trois façons","<em>de traverser.</em>"],'
    'lede:"Les transporteurs passent par la mer, par le détroit, ou font toute la route. Choisis d’abord la traversée, puis le trajet.",'
    'more:\'<p class="stop-sub">Par la mer, le van embarque à Marseille. Par le détroit, il traverse la France et l’Espagne, '
    'puis prend un ferry court. La grande route part du nord de l’Europe et va jusqu’au Souss.</p>'
    '<ul class="stop-tags" aria-label="Sur chaque trajet"><li>La date affichée</li><li>Le prix affiché</li>'
    '<li>Le contact direct</li><li>Gratuit</li></ul>\','
    'flip:!0,cards:["day","multi","exp"].filter(s=>t[s].length).map((s,b)=>({cat:x.cats[s],paper:!0,'
    'html:\'<p class="pc-top"><span class="pc-tag" style="--tilt:\'+Y[b%3]+"deg;--tag-ink:"+(s==="multi"?"#1B2230":"#F6EFE3")'
    '+\'"><span>\'+r(x.cats[s].name)+\'</span></span><span class="pc-n">0\'+(b+1)+\' / 03</span></p>'
    '<p class="pc-range">\'+r(R[s])+\'</p><p class="pc-count"><b>\'+t[s].length+"</b> "+(t[s].length===1?"trajet":"trajets")'
    '+\' pour commencer</p><p class="pc-line">\'+r(L2[s])+\'</p><ul class="pc-facts">\'+X[s].map(V=>"<li>"+r(V)+"</li>").join("")'
    '+\'</ul><p class="pc-from"><span>Inscription</span><b>Gratuite</b><span>pour tous</span></p>\'}))}}'
)

# 02 · Inclus (dans le template : « What's in the pocket »). L'ordre suit les objets 3D :
# la carte pliée, une personne, une tente, un van, un ticket.
SEC_J = (
    'function j(){const l=['
    '["Le trajet, sur une carte","Ta route, tes dates et ton prix sur une seule fiche. Les familles la voient avant de t’appeler.","Une carte par transporteur",x.accent||"#D63B2F"],'
    '["Le contact direct","Les familles t’appellent ou t’écrivent. Pas d’intermédiaire entre vous.","Toi et la famille",x.cats.day.color],'
    '["Tes points de collecte","Les villes où tu prends les colis, et celles où tu livres.","Au départ et à l’arrivée",x.cats.multi.color],'
    '["Ce que ton van prend","Colis, valises, électroménager, meubles : tu dis ce que tu acceptes.","Colis ou déménagement",x.cats.exp.color],'
    '["Gratuit pour tous","Ni abonnement ni commission au lancement, pour toi comme pour les familles.","Pour toi et pour elles","#B48A5C"]],'
    'g=[-2.6,2,-1.8,2.4,-2.2];'
    'return{id:"pocket",kick:"Ce qui est inclus",eyebrow:"Ce que Drari te donne",lead:!0,orb:!0,'
    'title:["Tout ce qu’il faut","pour partir <em>plein.</em>"],'
    'lede:"Cinq choses pour chaque transporteur inscrit, quel que soit ton trajet. La carte n’est que la première.",'
    'more:\'<p class="stop-sub">Drari met en relation, c’est tout. Le prix, la date et les conditions se fixent entre toi et la famille, avant le départ.</p>\','
    'cards:l.map(([c,m,i,h],d)=>({cat:{color:h},paper:!0,'
    'html:\'<p class="pc-top"><span class="pc-tag" style="--tilt:\'+g[d]+"deg;--tag-ink:"+(d===2?"#1B2230":"#F6EFE3")'
    '+\'"><span>\'+r(c)+\'</span></span><span class="pc-n">0\'+(d+1)+\' / 05</span></p><p class="pc-range">\'+r(i)'
    '+\'</p><p class="pc-line pc-what">\'+r(m)+"</p>"}))}}'
)

# 03 · Transporteurs (dans le template : 8 guides avec photos). Ici, 5 cartes d'exemple,
# une par trajet, qui attendent un nom. Pas de photo, pas de faux profil.
SEC_T = (
    'const T=['
    '{key:"tongariro",name:"Ton prénom",from:"Ta ville de départ",look:{hat:"cap"},land:"hills",'
    'why:"Une phrase pour te présenter aux familles.",line:"Tes jours de départ et ton prix.",off:"Français, arabe…"},'
    '{key:"inca",name:"Ton prénom",from:"Ta ville de départ",look:{hat:"beanie"},land:"dome",'
    'why:"Ce que tu dis aux gens avant le départ.",line:"Ce que tu prends : colis, valises, cartons.",off:"Français, arabe…"},'
    '{key:"torres",name:"Ton prénom",from:"Ta ville de départ",look:{hat:"brim"},land:"hills",'
    'why:"Pourquoi on peut te confier ses affaires.",line:"Tes points de collecte en France.",off:"Français, darija…"},'
    '{key:"kili",name:"Ton prénom",from:"Ta ville de départ",look:{hat:"cap"},land:"dome",'
    'why:"Ton trajet, avec tes mots.",line:"Tes villes de livraison au Maroc.",off:"Français, néerlandais, darija…"},'
    '{key:"everest",name:"Ton prénom",from:"Ta ville de départ",look:{hat:"beanie"},land:"hills",'
    'why:"Une phrase, pas plus.",line:"Comment te joindre : téléphone ou WhatsApp.",off:"Néerlandais, darija, tamazight…"}'
    '],M=[],O=(t,a)=>""'
)

SEC_I = (
    'function I(){const t=[-2.2,1.6,-1.2,2.4,1.8,-2.6,1.1,-1.6],n=\'<ul class="pols">\'+T.map((e,p)=>{'
    'const o=e.key?u(e.key):null,l=o?y(o):x.cats.day,g=o?o.name:"";'
    'return\'<li class="pg" data-k="\'+p+\'" style="--tilt:\'+t[p%t.length]+"deg;--cat:"+l.color+\'"><figure class="pol-frame">'
    '<div class="pol-photo">\'+W(e,p,l.color)+O(e,p)+"</div><figcaption><b>"+r(e.name)+"</b><span>"+r(e.from)'
    '+\'</span></figcaption></figure><div class="pol-text"><p class="pol-trek"><i></i>\'+r(g)+\'</p><p class="pol-why">“\'+r(e.why)'
    '+\'”</p><p class="pol-line">\'+r(e.line)+\'</p><div class="pol-foot"><p class="pol-stats"><span><b>Nouveau</b> sur Drari</span></p>'
    '<p class="pol-off"><em>Langues</em>\'+r(e.off)+"</p></div></div></li>"}).join("")+"</ul>";'
    'return{id:"guides",kick:"Les transporteurs",eyebrow:"Qui transporte",flow:!0,title:["Ta carte,","<em>à cette place.</em>"],'
    'lede:"Drari commence par les transporteurs. Chaque inscrit aura sa carte, comme celles-ci : son trajet, ses départs, '
    'ce qu’il prend. Ces cinq cartes sont des exemples, elles attendent un nom.",pols:n,cards:[]}}'
)

# 05 · FAQ (le rendu est fait par sections/faq.js, les questions viennent d'ici)
SEC_Q = (
    'function Q(){const c=['
    '["C’est vraiment gratuit ?","Oui. Au lancement, Drari ne prend rien : ni abonnement, ni commission, pour les transporteurs comme pour les familles."],'
    '["Qui fixe le prix ?","Le transporteur. Il affiche son prix sur son trajet, et vous vous mettez d’accord avant le départ."],'
    '["Drari transporte mes affaires ?","Non. Drari met en relation. Ce sont les transporteurs qui chargent, traversent et livrent."],'
    '["Comment je m’inscris comme transporteur ?","Remplis le ticket en bas de la page : ton trajet, tes mois de départ, ton prénom et un moyen de te joindre."],'
    '["Combien de temps dure la traversée ?","Algésiras - Tanger Med : 1 h 30 (DFDS). Almería - Nador : 7 à 11 h (Ferryhopper). '
    'Marseille - Tunis : 22 à 26 h (Ferryhopper). Marseille - Oran : 28 à 29 h (aFerry)."],'
    '["Quand faut-il éviter de partir ?","L’été, quand la diaspora rentre au pays. Pour le Maroc, c’est l’opération Marhaba : '
    'en 2026, du 10 juin au 15 septembre (maroc.ma)."],'
    '["Qu’est-ce que je prépare ?","La liste de ce que tu envoies, des cartons solides et fermés, et le numéro de la personne qui reçoit."],'
    '["Et la douane ?","Chaque pays a ses règles sur ce qui peut entrer. Demande au transporteur ce qu’il accepte, et garde la liste de ce que tu envoies."]'
    '];if(window.FAQ_MAP)return window.FAQ_MAP.def({T:f,catOf:y,esc:r,fmt:k,PAL:x,faq:c});'
    'return{id:"ready",kick:"Des questions ?",title:["Combien,","<em>comment, quand.</em>"],lede:"Les questions qu’on nous pose le plus.",'
    'more:\'<div class="faq">\'+c.map(([i,h])=>"<details><summary>"+r(i)+"</summary><p>"+h+"</p></details>").join("")+"</div>",cards:[]}}'
)

MONTHS_FR_SHORT = '["JAN","FÉV","MARS","AVR","MAI","JUIN","JUIL","AOÛT","SEPT","OCT","NOV","DÉC"]'
MONTHS_FR = '["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]'
MONTHS_FR_CAP = '["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]'

VAN_ICON = ('<svg viewBox="0 0 24 40" aria-hidden="true"><path d="M2.5 31 V18.5 Q2.5 15 6 15 H14.5 Q17.4 15 18.8 17.6 L21.5 23 V31 Z"/>'
            '<circle cx="7.2" cy="32" r="3"/><circle cx="17.2" cy="32" r="3"/></svg>')
BUBBLE_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5.2 17.6 L4 21 L7.7 19.7 A8.6 8.6 0 1 0 5.2 17.6Z" '
               'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>')
