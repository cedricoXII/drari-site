"""Le bas de page Drari : le code JavaScript qui remplace les fonctions de sections/sections.js.
(v0.5 : 01 « Le métier », 02 « Inclus », 03 « Ta carte » et la FAQ des transporteurs, d'après le fichier des textes.)

Chaque bloc remplace une fonction entière du template (même structure de sortie, textes Drari).
Les apostrophes sont typographiques (’) : le code est inséré dans du JavaScript minifié.
Règle : pas de faux transporteurs, pas de faux avis, pas de fausse rareté, chiffres sourcés.
"""

# v0.5 · 01 · Le métier (remplace « Traversées » : mêmes décors, mêmes 3 cartes, nouveaux textes).
# Chaque carte porte sa règle et sa source, juste à côté de la phrase qu'elle prouve.
# Les fonds des étiquettes sont foncés pour qu'un texte crème reste lisible (contraste 4,5:1).
SEC_B = (
    'function B(){const t={day:[],multi:[],exp:[]};f.forEach(s=>t[s.cat||z(s.days)].push(s));'
    'const R={day:"Une nuit en mer",multi:"2 à 3 jours",exp:"3 à 4 jours"},'
    'TB={day:"#3F6B44",multi:"#D2A23A",exp:"#2F5F8F"},'
    'RU={day:\'<b>La licence :</b> au-dessus de 2,5 t à l’international, la licence communautaire est obligatoire depuis le 21 mai 2022.\','
    'multi:\'<b>Le toit :</b> depuis le 1<sup>er</sup> décembre 2025, Tanger Med refuse les utilitaires des pros chargés sur le toit. Nador a suivi.\','
    'exp:\'<b>Le tachygraphe :</b> depuis le 1<sup>er</sup> juillet 2026, il est obligatoire pour les utilitaires de plus de 2,5 t à l’international.\'},'
    'SR={day:\'Source : <a href="https://eur-lex.europa.eu/eli/reg/2009/1072/2022-02-21/fra" target="_blank" rel="noopener">EUR-Lex, règlement 1072/2009</a>\','
    'multi:\'Sources : <a href="https://www.bladi.net/tanger-med-bagages-toit-interdits-vehicules-commerciaux,118199.html" target="_blank" rel="noopener">Bladi, 2 décembre 2025</a> ; <a href="https://www.hespress.com/1705262-1705262.html" target="_blank" rel="noopener">Hespress, 22 février 2026</a>\','
    'exp:\'Source : <a href="https://www.ela.europa.eu/en/news/driving-and-rest-rules-and-compulsory-tachographs-apply-light-commercial-vehicles-cross-border" target="_blank" rel="noopener">Autorité européenne du travail, 24 juin 2026</a>\'},'
    'Y=[-3,2.2,-2];'
    'return{id:"lengths",kick:"Le métier a changé",eyebrow:"Le métier",title:["Le métier","<em>a changé.</em>"],'
    'lede:"Les règles se durcissent aux ports et sur la route. Elles pèsent sur tout le monde, et elles avantagent celui qui est en règle et qui peut le montrer.",'
    'more:\'<p class="stop-sub">En face, les familles cherchent la même chose depuis toujours : quelqu’un de confiance. '
    'Aujourd’hui, elles le trouvent par un cousin, un voisin, un courtier. Drari le montre à tous.</p>\','
    'flip:!0,cards:["day","multi","exp"].filter(s=>t[s].length).map((s,b)=>({cat:x.cats[s],paper:!0,'
    'html:\'<p class="pc-top"><span class="pc-tag" style="--tilt:\'+Y[b%3]+"deg;--tag-bg:"+TB[s]+";--tag-ink:"+(s==="multi"?"#1B2230":"#F6EFE3")'
    '+\'"><span>\'+r(x.cats[s].name)+\'</span></span><span class="pc-n">0\'+(b+1)+\' / 03</span></p>'
    '<p class="pc-routes">\'+t[s].map(V=>r(V.name)).join(", ")+\'</p><p class="pc-range">\'+r(R[s])+\'</p>'
    '<p class="pc-line pc-rule">\'+RU[s]+\'</p><p class="pc-src">\'+SR[s]+\'</p>'
    '<p class="pc-from">Sur ta carte Drari, tu pourras montrer que tu es en règle.</p>\'}))}}'
)

# v0.5 · 02 · Inclus. L'ordre suit les objets 3D : la carte pliée, une personne, une tente, un van, un ticket.
# « Les familles la verront » : au futur, le site des familles n'est pas encore ouvert. Jamais « vérifié ».
SEC_J = (
    'function j(){const l=['
    '["Le trajet, sur une carte","Ta route, tes dates et ton prix sur une seule fiche. Les familles la verront avant de t’appeler.","Une carte par transporteur",x.accent||"#D63B2F","#B3312A","#F6EFE3"],'
    '["Le contact direct","Les familles t’appelleront ou t’écriront. Pas d’intermédiaire entre vous.","Toi et la famille",x.cats.day.color,"#3F6B44","#F6EFE3"],'
    '["Tes points de collecte","Les villes où tu prends les colis, et celles où tu livres.","Au départ et à l’arrivée",x.cats.multi.color,"#D2A23A","#1B2230"],'
    '["Ce que ton van prend","Colis, valises, électroménager, meubles : tu dis ce que tu acceptes.","Colis ou déménagement",x.cats.exp.color,"#2F5F8F","#F6EFE3"],'
    '["Ta carte, gratuite","Ta carte est gratuite. Pas de commission sur tes clients : l’argent du transport reste entre toi et la famille.","","#B48A5C","#B48A5C","#1B2230"]],'
    'g=[-2.6,2,-1.8,2.4,-2.2];'
    'return{id:"pocket",kick:"Ce qui est inclus",eyebrow:"Ce que Drari te donne",lead:!0,orb:!0,'
    'title:["Tout ce qu’il faut","<em>pour qu’on te trouve.</em>"],'
    'lede:"Cinq choses sur ta carte, quel que soit ton trajet.",'
    'more:\'<p class="stop-sub">Drari met en relation, c’est tout. Le prix, la date et les conditions se fixent entre toi et la famille, avant le départ.</p>\','
    'cards:l.map(([c,m,i,h,tb,ti],d)=>({cat:{color:h},paper:!0,'
    'html:\'<p class="pc-top"><span class="pc-tag" style="--tilt:\'+g[d]+"deg;--tag-bg:"+tb+";--tag-ink:"+ti'
    '+\'"><span>\'+r(c)+\'</span></span><span class="pc-n">0\'+(d+1)+\' / 05</span></p>\'+(i?\'<p class="pc-range">\'+r(i)+\'</p>\':"")'
    '+\'<p class="pc-line pc-what">\'+r(m)+"</p>"}))}}'
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

# v0.5 · 03 · Ta carte : les 3 étapes, puis les 5 cartes d'exemple (marquées « Exemple »), puis le bouton.
SEC_I = (
    'function I(){const t=[-2.2,1.6,-1.2,2.4,1.8,-2.6,1.1,-1.6],'
    'st=\'<ol class="dr-steps">\'+['
    '"Tu inscris ton trajet : ta route, tes mois de départ, ton prénom et ton numéro.",'
    '"On te rappelle pour préparer ta carte avec toi : tes dates, ton prix, ce que tu prends.",'
    '"Ta carte sera en ligne quand le site des familles ouvrira. Elles t’appelleront en direct."'
    '].map((s,i)=>\'<li><b aria-hidden="true">\'+(i+1)+"</b><p>"+s+"</p></li>").join("")+"</ol>",'
    'n=st+\'<ul class="pols">\'+T.map((e,p)=>{'
    'const o=e.key?u(e.key):null,l=o?y(o):x.cats.day,g=o?o.name:"";'
    'return\'<li class="pg" data-k="\'+p+\'" style="--tilt:\'+t[p%t.length]+"deg;--cat:"+l.color+\'"><figure class="pol-frame">'
    '<div class="pol-photo">\'+W(e,p,l.color)+O(e,p)+\'<span class="pol-ex">Exemple</span></div><figcaption><b>\'+r(e.name)+"</b><span>"+r(e.from)'
    '+\'</span></figcaption></figure><div class="pol-text"><p class="pol-trek"><i></i>\'+r(g)+\'</p><p class="pol-why">“\'+r(e.why)'
    '+\'”</p><p class="pol-line">\'+r(e.line)+\'</p><div class="pol-foot"><p class="pol-stats"><span><b>Nouveau</b> sur Drari</span></p>'
    '<p class="pol-off"><em>Langues</em>\'+r(e.off)+"</p></div></div></li>"}).join("")+"</ul>";'
    'return{id:"guides",kick:"Ta carte",eyebrow:"Ta carte",flow:!0,cls:"dr-free",title:["Ta carte,","<em>à cette place.</em>"],'
    'lede:"Drari commence par les transporteurs. Chaque inscrit aura sa carte, comme celles-ci : son trajet, ses départs, '
    'ce qu’il prend. Ces cinq cartes sont des exemples, elles attendent un nom.",pols:n,cards:[],'
    'after:\'<div class="dr-after"><a class="dr-cta" href="#ticket" data-cta>Inscrire mon trajet<i aria-hidden="true">→</i></a></div>\'}}'
)

# v0.5 · 05 · FAQ : les 9 questions des transporteurs (le rendu est fait par sections/faq.js, les questions viennent d'ici).
# Retirées (pour la landing n° 2, familles) : « Quand faut-il éviter de partir ? », « Qu'est-ce que je prépare ? », « Et la douane ? ».
SEC_Q = (
    'function Q(){const c=['
    '["C’est vraiment gratuit ?","Ta carte, oui : ta route, tes dates, ton prix et les demandes des familles. Les options Pro et Pro+ sont payantes, et c’est toi qui choisis. Pas de commission sur tes clients."],'
    '["Qui fixe le prix ?","Toi. Drari ne fixe aucun prix. Tu affiches ton prix au kilo ou à la pièce, et tu te mets d’accord avec la famille avant le départ."],'
    '["Drari s’occupe des colis ?","Non. Drari met en relation. C’est toi qui charges, traverses et livres, à ton prix et à tes conditions."],'
    '["Comment je m’inscris ?","Tu remplis le ticket en bas de la page : ton trajet, tes mois de départ, ton prénom et ton numéro. On te rappelle pour préparer ta carte."],'
    '["Qui voit mon numéro ?","Pour l’instant, personne d’autre que Drari : il sert à te rappeler pour préparer ta carte. Ensuite, il ne sert qu’à la mise en relation avec les familles. Il n’est ni vendu, ni prêté."],'
    '["Faut-il être déclaré ?","Drari est fait pour les transporteurs en règle. Ce qu’il faut pour l’être (registre, licence, assurance) sera expliqué sur le site."],'
    '["Vous allez prendre une commission ?","Non. Drari vit des options Pro et Pro+, que tu prends seulement si tu veux. Si les conditions changent un jour, tu le sauras au moins 15 jours avant."],'
    '["Quand les familles envoient-elles le plus ?","Au moment du ramadan, d’après les transporteurs cités par Hespress (22 février 2026). Le reste de l’année, ça dépend des trajets : c’est toi qui connais tes mois forts."],'
    '["Combien de temps dure la traversée ?","Algésiras - Tanger Med : 1 h 30 (DFDS). Almería - Nador : 7 à 11 h (Ferryhopper). '
    'Marseille - Tunis : 22 à 26 h (Ferryhopper). Marseille - Oran : 28 à 29 h (aFerry)."]'
    '];if(window.FAQ_MAP)return window.FAQ_MAP.def({T:f,catOf:y,esc:r,fmt:k,PAL:x,faq:c});'
    'return{id:"ready",kick:"Des questions ?",title:["Combien,","<em>comment, quand.</em>"],lede:"Les questions que posent les transporteurs.",'
    'more:\'<div class="faq">\'+c.map(([i,h])=>"<details><summary>"+r(i)+"</summary><p>"+h+"</p></details>").join("")+"</div>",cards:[]}}'
)
