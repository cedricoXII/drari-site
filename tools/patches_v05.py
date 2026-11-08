"""v0.5 : les remplacements appliqués après ceux de v0.2 à v0.4 (tools/patches.py les ajoute à la fin de la liste).

Chaque entrée : (texte d'origine, texte Drari[, nombre d'occurrences attendu]), ou (("@range", début, fin), texte)
pour remplacer tout un bloc, du début jusqu'à la fin comprise (voir tools/build.py).
Les morceaux longs sont dans tools/v05/ : head.html (balises), top.html (en-tête, haut de page, barre du bas),
style.css (la feuille de style v0.5), boot.js (ce qui marche avant la 3D) ; book.js, price.js et footer.js remplacent
des modules entiers (voir build.py).
"""
import base64, os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)


def _read(*p):
    return open(os.path.join(_HERE, "v05", *p), encoding="utf-8").read()


HEAD_V05 = _read("head.html").strip()
TOP = ('<style id="dr-v05">\n' + _read("style.css") + '</style>\n<script>\n' + _read("boot.js") + '</script>\n'
       + _read("top.html"))
GLOBE_JPG = base64.b64encode(open(os.path.join(_ROOT, "data", "globe-sdf-1024.jpg"), "rb").read()).decode("ascii")

PATCHES_V05 = [
    # ---------- HTML : en-tête, haut de page et barre du bas en tête du <body>, lus et affichés avant tout script
    (("@range", '<header class="top">', '</main>\n'), ''),
    ('<body>\n', '<body>\n' + TOP + '\n'),
    # l'ancien texte de secours anglais (« Valmora ») : le haut de page statique, en français, le remplace
    (("@range", '<div class="fallback">', '</div>\n'), ''),
    ('<aside class="strip" id="strip" aria-label="Elevation profile of the route">', '<aside class="strip" id="strip" aria-hidden="true" hidden>'),
    ('<div class="readout"><b id="roAlt">1 132 m</b><span id="roKm">km 0.0</span></div>', '<div class="readout"><b id="roAlt"></b><span id="roKm"></span></div>'),
    ('jo.textContent="km "+i.toFixed(1)+" of 58"', 'jo.textContent=""'),
    ('e.fillText("The Valmora Round",48*l,232*l)', 'e.fillText("Drari",48*l,232*l)'),
    # pas d'écran noir : le fond de la pièce dès le premier affichage, l'en-tête et le texte ne sont plus cachés
    ('html.hero-on,html.hero-on body{background:#0a0909}', 'html.hero-on,html.hero-on body{background:#0A1019}'),
    ('html.hero-on .hero-copy,html.hero-on .top{visibility:hidden}', ''),
    ('html.hero-on .hero-exit{height:var(--hero-exit,150vh)}', ''),

    # ---------- main.js : le gros script attend que le haut de page soit affiché et son entrée finie (0,9 s), puis construit la 3D
    ('(async function(){"use strict";const P={',
     '(async function(){"use strict";await new Promise(r=>{const g=()=>setTimeout(r,window.DR&&DR.rm?0:900);"requestAnimationFrame"in window?requestAnimationFrame(g):g()});const P={'),
    # sans WebGL : on ne demande pas de contexte (pas d'erreurs Three.js en console) ; les sections et le ticket sont
    # construits quand même (tools/v05/boot.js, DR.noGL)
    ('try{D=new THREE.WebGLRenderer({canvas:It,antialias:!0,alpha:!1,powerPreference:"high-performance"})}catch{D=null}',
     'try{D=(()=>{try{const c=document.createElement("canvas");return!!(c.getContext("webgl2")||c.getContext("webgl"))}catch{return!1}})()?new THREE.WebGLRenderer({canvas:It,antialias:!0,alpha:!1,powerPreference:"high-performance"}):null}catch{D=null}'),
    ('document.documentElement.classList.add("no-webgl");return}',
     'document.documentElement.classList.add("no-webgl"),window.DR&&DR.noGL&&DR.noGL();return}'),
    # taille de dessin : 1,5 au plus sur téléphone, ombres en 1 024 ; largeur prise sur clientWidth (pas innerWidth)
    ('const Ze=()=>window.innerWidth*window.innerHeight>26e5?1.5:1.75;',
     'const Ze=()=>window.DR&&DR.phone?1.5:window.innerWidth*window.innerHeight>26e5?1.5:1.75;'),
    ('SHADOW:2048}', 'SHADOW:window.DR&&DR.phone?1024:2048}'),
    ('function W0(){const e=window.innerWidth,t=window.innerHeight;', 'function W0(){const e=document.documentElement.clientWidth||window.innerWidth,t=window.innerHeight;'),
    # mouvement réduit : pas de défilement lissé (Lenis)
    ('const mt=new Lenis({', 'const mt=window.DR&&DR.rm?null:new Lenis({'),
    ('mt.on("scroll",ScrollTrigger.update);', 'mt&&mt.on("scroll",ScrollTrigger.update);'),
    ('mt.raf(e*1e3),Rt(e)', 'mt&&mt.raf(e*1e3),Rt(e)'),
    # le bouton de l'en-tête passe par tools/v05/boot.js (comme tous les boutons « Inscrire mon trajet »)
    ('document.getElementById("bookTop").addEventListener("click",e=>{if(e.preventDefault(),v&&v.book)return v.book();mt.scrollTo(Jt(),{duration:V?0:2.6})}),', ''),
    ('return v.home();mt.scrollTo(0,{duration:V?0:2.2})', 'return v.home();mt&&mt.scrollTo(0,{duration:V?0:2.2})'),
    # la 3D apparaît en fondu derrière le texte, une fois la première image dessinée
    ('D.compile(L,R),D.render(L,R),I0=!0,', 'D.compile(L,R),D.render(L,R),I0=!0,requestAnimationFrame(()=>document.documentElement.classList.add("dr-3d")),'),

    # ---------- le haut de page 3D (hero-kit.js, fold.js) : il garde le texte statique au lieu d'écrire le sien
    ('const h=document.getElementById("heroCopy");h.innerHTML="";', 'const h=document.getElementById("heroCopy");'),
    ('a=document.createElement("div");a.className="fo",a.innerHTML=\'<div class="fo-head"><h1 id="h-hero" class="v2-display fo-h1"><span class="v2-line"><span><span class="x">Ton trajet</span></span></span><span class="v2-line"><span><span class="x">trouve ses</span></span></span><span class="v2-line"><span><span class="x"><em class="acc">clients.</em></span></span></span></h1><p class="v2-lede fo-lede">\'+s+\'</p><p class="fo-hint"><i></i><span>Survole une carte pour la soulever</span><span class="sep">/</span><span>Fais défiler pour la suite</span></p></div><div class="fo-side">',
     'a=document.getElementById("drFo")||document.createElement("div");a.className="fo",a.insertAdjacentHTML("beforeend",\'<div class="fo-side">'),
    ('aria-label="Trajet suivant">→</button>\',d.copy.appendChild(a),m={root:a,head:a.querySelector(".fo-head"),lines:Array.from(a.querySelectorAll(".fo-h1 .v2-line > span")),xs:Array.from(a.querySelectorAll(".fo-h1 .x")),lede:a.querySelector(".fo-lede"),hint:a.querySelector(".fo-hint"),',
     'aria-label="Trajet suivant">→</button>\'),a.parentNode||d.copy.appendChild(a),m={root:a,head:a.querySelector(innerWidth<761?".fo-head":".dr-frame")||a.querySelector(".fo-head")||a,lines:[document.createElement("span")],xs:[],lede:document.createElement("p"),hint:document.createElement("p"),'),
    ('<h2 class="fc-name">\'+ve(c.name)+\'</h2><p class="fc-sub">', '<p class="fc-name">\'+ve(c.name)+\'</p><p class="fc-sub">'),
    ('const te={off:d.Q.get("pop")==="off",', 'const te={off:!0,'),
    ('.fo:not(.fo-live){visibility:hidden;opacity:0;}', '.fo:not(.fo-live) .fo-side,.fo:not(.fo-live) .fo-arrow{visibility:hidden;opacity:0;}'),
    # l'en-tête ne glisse plus à l'entrée : il est là dès le premier affichage
    ('o=Array.from(document.querySelectorAll(".top .brand, .top #bookTop"))', 'o=[]'),
    ('.to(n[0],{v:0,duration:1.2,ease:"expo.out",onUpdate:()=>s(o[0],n[0])},.95).to(n[1]||{},',
     '.to(n[0]||{v:0},{v:0,duration:1.2,ease:"expo.out",onUpdate:()=>o[0]&&s(o[0],n[0])},.95).to(n[1]||{v:0},'),
    # la fiche du trajet ne parle plus du relief (« couche 3 sur 10 ») : reste du modèle
    ('if(p===$&&je>=0&&h){', 'if(!1){'),

    # ---------- le menu (nav.js)
    ('html.hero-on:not(.hero-live) .navx{opacity:0;visibility:hidden;transition:none;}', ''),
    ('f.i>=0&&e>=t.at(f.i,0)-o*.45&&(r=v)', 'f.i>=0&&e>=(t.navAt?t.navAt(f.i):t.at(f.i,0))-o*.4&&(r=v)'),
    ('const o=window.APP&&window.APP.TR;o&&o.go&&o.go(d[+e.dataset.k].i)}', 'const o=window.APP&&window.APP.TR;o&&o.go?o.go(d[+e.dataset.k].i):window.DR&&DR.go&&DR.go(d[+e.dataset.k].i)}'),

    # ---------- les sections (landing.js, sections.js)
    # page simple : les titres ne sont pas cachés pour être révélés au défilement
    ('l.stops.forEach(e=>{if(e.el.classList.contains("lead")||e.el.classList.contains("flow")){gsap.set(',
     'window.DR&&DR.flat||l.stops.forEach(e=>{if(e.el.classList.contains("lead")||e.el.classList.contains("flow")){gsap.set('),
    # plus de H2 anglais caché (« One day, 22 km… ») écrit dans #finaleLine
    ('function Ce(t,o){const i=', 'function Ce(t,o){return;const i='),
    ('function Xe(){const t=window.innerWidth,', 'function Xe(){const t=document.documentElement.clientWidth||window.innerWidth,'),
    ('const v=[...e.el.querySelectorAll(".pg")],b=i?2:4;', 'const v=[...e.el.querySelectorAll(".pg")],b=e.el.classList.contains("dr-free")?99:i?2:4;'),
    # sections « libres » (03 Ta carte, 04 Gratuit ?, 05 FAQ, 06 Inscription) et page simple : ni épinglage ni mise à l'échelle
    ('if(m&&w){m.style.height="",w.style.transform="",e.pinH=w.offsetHeight;const A=i?80:98,O=o-A-(i?10:22);e.pinK=Math.min(1,O/e.pinH),w.style.transform=e.pinK<1?"scale("+e.pinK.toFixed(4)+")":"",e.pinTop=Math.round(A+Math.max(0,(O-e.pinH*e.pinK)*.5)),',
     'if(m&&w){m.style.height="",w.style.transform="",e.pinH=w.offsetHeight;const A=i?80:98,O=o-A-(i?10:22),Fx=window.DR&&DR.flat||e.el.classList.contains("dr-free");e.pinK=Fx?1:Math.min(1,O/e.pinH),w.style.transform=e.pinK<1?"scale("+e.pinK.toFixed(4)+")":"",e.pinTop=Fx?0:Math.round(A+Math.max(0,(O-e.pinH*e.pinK)*.5)),'),
    ('e.wo=H,e.pinLen=Math.round(H?o*H.pinLen(i):(e.sets-1)*e.step+o*.5),w.style.top=e.pinTop+"px",m.style.height=Math.round(e.pinH+e.pinLen)+"px",',
     'e.wo=H,e.pinLen=Fx?0:Math.round(H?o*H.pinLen(i):(e.sets-1)*e.step+o*.5),w.style.top=Fx?"":e.pinTop+"px",m.style.height=Fx?"":Math.round(e.pinH+e.pinLen)+"px",'),
    # sections épinglées plus courtes sur ordinateur : 01 (3 cartes) 2,8 → 1,3 écran, 02 (5 cartes) 3,4 → 1,6 écran après l'entrée
    ('P=o*(e.S.focus?i?2.2:2.8:e.S.orb?i?3:1.04+3.4:', 'P=o*(e.S.focus?i?2.2:1.3:e.S.orb?i?3:1.04+1.6:'),
    # page simple : aucune section ne s'épingle ni ne dessine de 3D sous le haut de page, la camionnette ne suit plus la ligne
    ('let x=null;for(const n of l.stops){if(n.flow){', 'let x=null;const Df=window.DR&&DR.flat;for(const n of l.stops){if(Df){n.vis=!1,n.held=!1,n.wo&&n.wo.frame(n,o,s);continue}if(n.flow){'),
    ('if(b&&b.off&&(b=null),b&&!x)', 'if((b&&b.off||Df)&&(b=null),b&&!x)'),
    # chaque bouton mène au ticket lui-même ; le menu change d'onglet quand la section arrive vraiment
    ('a.book=function(){a.mode==="trek"?de("#book"):J(document.getElementById("book"))}',
     'a.navAt=function(t){const i=l.stops[t];return i?!(window.DR&&DR.flat)&&i.orb&&!l.narrow?i.top+l.vh*.85:i.head!==void 0?i.head:i.top:0},'
     'a.book=function(){const k=document.getElementById("ticket"),h=document.querySelector(".top");a.mode==="trek"?de("#book"):J(k?Math.max(0,Math.round(k.getBoundingClientRect().top+window.scrollY-(h?h.offsetHeight:64)-12)):document.getElementById("book"))}'),
    # un onglet du menu montre sa section : 02 (globe) là où elle est vraiment à l'écran, les sections libres et la page simple
    # avec leur sur-titre sous l'en-tête (avant : le sur-titre passait sous l'en-tête, et « 02 Inclus » montrait encore la 01)
    ('a.go=function(t){const o=t>=0?l.stops[t]:null;if(a.mode==="trek"){de(o?"#"+o.el.id:0);return}J(o?o.el:0)}',
     'a.go=function(t){const o=t>=0?l.stops[t]:null;if(a.mode==="trek"){de(o?"#"+o.el.id:0);return}if(!o){J(0);return}'
     'const h=document.querySelector(".top"),H=h?h.offsetHeight:64,F=window.DR&&DR.flat,y=o.el.getBoundingClientRect().top+window.scrollY;'
     'J(Math.max(0,Math.round(!F&&o.orb&&!l.narrow?o.top+l.vh*1.04:F||o.flow||o.el.classList.contains("dr-free")?y-H-12:o.top)))}'),
    # le bouton après « Ta carte » (champ after des sections)
    ('+"</ul>":"")+"</section>"}function Z(){', '+"</ul>":"")+(t.after||"")+"</section>"}function Z(){'),

    # ---------- 05 FAQ (faq.js) : la carte une seule fois dans la page, centrée sur l'Europe et le Maghreb, pas d'épinglage
    ('a&&n.querySelectorAll(".fm-face").forEach(r=>{r.style.backgroundImage="url("+a+")"})',
     'a&&(()=>{const st=document.createElement("style");st.id="dr-faq-map",st.textContent=".fm-face{background-image:url("+a+")}",document.head.appendChild(st)})()'),
    ('window.FL_LATER?window.FL_LATER.push(c):c();const s=[...n.querySelectorAll(".fq-q")]',
     'window.DR&&DR.flat&&innerWidth<761||(window.FL_LATER?window.FL_LATER.push(c):c());const s=[...n.querySelectorAll(".fq-q")]'),
    ('const s=D(k((n-(e.pinStart-c*.55))/(c*.75)));', 'const s=window.DR&&DR.flat?1:D(k((n-(e.pinStart-c*.95))/(c*.75)));'),
    ('cls:"faqmap",title:', 'cls:"faqmap dr-free",title:'),
    # la carte commence à 150° ouest : les trajets (de 10° ouest à 10° est) tombent au milieu d'un pli, à droite des questions
    ('j=Math.round(91/360*2048)', 'j=Math.round(30/360*2048)'),
    ('const x=(l- -89+360)%360/360*2048;', 'const x=(l- -150+360)%360/360*2048;'),
    ('const O=e=>(e- -89+360)%360/360', 'const O=e=>(e- -150+360)%360/360'),
    ('transform:translate(-43.5%, -50%) rotateX(52deg) rotateZ(-8deg);}', 'transform:translate(-24.6%, -26%) rotateX(52deg) rotateZ(-8deg);}'),

    # ---------- 02 Inclus (stations.js) : le globe regarde l'Europe et le Maghreb, et ne tourne plus avec la roue
    ('i0=new u.Quaternion().setFromEuler(new u.Euler(.38,-1.95,0,"XYZ"))', 'i0=new u.Quaternion().setFromEuler(new u.Euler(.52,-.03,0,"XYZ"))'),
    ('e.globe&&a&&(N.setFromAxisAngle(a0,i).multiply(i0),', 'e.globe&&a&&(N.copy(i0),'),
    ('N.setFromAxisAngle(a0,n*2*Math.PI/V).multiply(i0),', 'N.copy(i0),'),

    # ---------- vitesse : la texture du globe en 1 024 × 512 JPEG (environ 50 Ko au lieu de 215 Ko)
    (("@range", 'window.GLOBE_DATA={w:2048,h:1024,scale:4,src:"', '",tint:"'),
     'window.GLOBE_DATA={w:1024,h:512,scale:4,src:"data:image/jpeg;base64,' + GLOBE_JPG + '",tint:"'),

    # ---------- haut de page sur téléphone : les numéros 01 à 05 sont déjà écrits sur les tranches ; le bouton garde son nom
    ("style=\"--c:'+d.catOf(i).color+'\">'+r(i)+\"</button>\").join(\"\")+'</div><div class=\"ro-body\">",
     "style=\"--c:'+d.catOf(i).color+'\"><span class=\"ro-n\">'+r(i)+\"</span></button>\").join(\"\")+'</div><div class=\"ro-body\">"),
    # ---------- menu : avant la 3D (menu construit tout de suite, voir boot.js) et sans WebGL, l'onglet suit quand même
    # la section à l'écran (« 00 Trajets » tant que les sections ne sont pas construites)
    ('else c!==null&&t&&t.mode==="trek"&&(c=null,i&&i.classList.remove("nav-on"));requestAnimationFrame(b)};',
     'else if(!t){const st=document.querySelectorAll("#landing .stop"),e=window.scrollY,o=window.innerHeight;let r=0;'
     'p.forEach((f,v)=>{const q=f.i>=0&&st[f.i];q&&e>=q.getBoundingClientRect().top+e-o*.4&&(r=v)}),r!==c&&(c=r,m(r))}'
     'else c!==null&&t&&t.mode==="trek"&&(c=null,i&&i.classList.remove("nav-on"));requestAnimationFrame(b)};'),
]
