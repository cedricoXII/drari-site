"""Les décors Drari : la camionnette à la place du randonneur, et les décors de la section 01.

- sections/sections.js : le randonneur (fonction R) devient une camionnette chargée, roues qui tournent.
- sections/stations.js : nouvelles formes en papier (ferry, rocher, maison, vagues) et décors de la section 01 :
  « par la mer » = un ferry sur les vagues, « par le détroit » = le rocher de Gibraltar, la ville et un petit ferry,
  « toute la route » = l'Atlas, une kasbah et une maison.
- sections/footer.js : la tente et le feu deviennent une maison et la camionnette garée devant.
"""

VAN_HIKER = (
    'function R(){const t=document.createElement("div");t.className="hk",t.setAttribute("aria-hidden","true"),'
    't.innerHTML=\'<svg viewBox="0 0 68 100"><ellipse class="sh" cx="34" cy="99" rx="30" ry="2.6"/><g class="fig"><g class="bd">'
    '<rect x="9" y="51.5" width="13" height="7.5" rx="1"/><rect x="23.5" y="53.5" width="12" height="5.5" rx="1"/>'
    '<path d="M4 90 L4 63 Q4 59 8 59 L45 59 Q48 59 50 61.5 L57.5 71 L62.5 72.6 Q65 73.4 65 76.5 L65 90 Z"/>'
    '<path class="gl" d="M47.2 62.6 L52.6 62.6 L58.6 70.6 L47.2 70.6 Z"/><path class="ln" d="M30 61.5 L30 88"/>'
    '<rect class="lt" x="61.6" y="78" width="3.4" height="3.2" rx=".8"/></g>'
    '<g class="w1"><circle cx="17" cy="90" r="7"/><circle class="hb" cx="17" cy="90" r="2.6"/><path class="sp" d="M17 84.5 L17 95.5"/></g>'
    '<g class="w2"><circle cx="52" cy="90" r="7"/><circle class="hb" cx="52" cy="90" r="2.6"/><path class="sp" d="M52 84.5 L52 95.5"/></g>'
    '</g></svg>\',document.body.appendChild(t);'
    'const a=t.querySelector(".w1"),n=t.querySelector(".w2"),e=t.querySelector(".bd"),'
    'o={el:t,x:0,y:0,h:100,face:1,phase:0,walk:0,on:!1,rise:1};'
    'return o.set=function(l,g,c,m){o.x=l,o.y=g,o.h=c,m&&(o.face=m);'
    'const i=c/100,h=-Math.abs(Math.sin(o.phase*2))*.9*o.walk;'
    't.style.transform="translate3d("+(l-34).toFixed(1)+"px,"+(g-100).toFixed(1)+"px,0) perspective(300px) rotateX("'
    '+((1-o.rise)*88).toFixed(1)+"deg) scale("+(i*o.face).toFixed(4)+","+i.toFixed(4)+")";'
    'const d=(o.phase*57.3%360).toFixed(1);a.setAttribute("transform","rotate("+d+" 17 90)"),'
    'n.setAttribute("transform","rotate("+d+" 52 90)"),e.setAttribute("transform","translate(0 "+h.toFixed(2)+")")},'
    'o.step=function(l,g,c){const m=c?0:Math.min(1,Math.abs(l)/Math.max(g,.001)/120);'
    'o.walk+=(m-o.walk)*(1-Math.exp(-g*9)),o.phase+=Math.abs(l)/Math.max(18,o.h*.32)*Math.PI*.5},'
    'o.show=function(l){l!==o.on&&(o.on=l,t.style.visibility=l?"visible":"hidden")},'
    'o.colour=function(l){l!==o.col&&(o.col=l,t.style.color=l)},o}'
)

VAN_CSS = (
    '.hk .sh{fill:rgba(0,0,0,0.38);stroke:none;}'
    '\n.hk .gl{fill:rgba(255,255,255,0.4);stroke:none;}.hk .ln{fill:none;stroke:rgba(0,0,0,0.25);stroke-width:1;}'
    '.hk .lt{fill:#FFD66E;stroke:none;}.hk .hb{fill:rgba(255,255,255,0.5);stroke:none;}'
    '.hk .sp{fill:none;stroke:rgba(255,255,255,0.5);stroke-width:1.4;}'
)

NEW_SHAPES = (
    'const d={'
    # un ferry vu de côté : coque, deux ponts, cheminée
    'ferry:(e,l,t)=>{e.beginPath(),e.moveTo(l*.03,t*.62),e.lineTo(l*.97,t*.62),e.lineTo(l*.93,t*.98),e.lineTo(l*.15,t*.98),e.closePath(),e.fill(),'
    'e.beginPath(),e.moveTo(l*.2,t*.63),e.lineTo(l*.25,t*.4),e.lineTo(l*.86,t*.4),e.lineTo(l*.88,t*.63),e.closePath(),e.fill(),'
    'e.beginPath(),e.moveTo(l*.35,t*.41),e.lineTo(l*.39,t*.23),e.lineTo(l*.75,t*.23),e.lineTo(l*.77,t*.41),e.closePath(),e.fill(),'
    'e.fillRect(l*.58,t*.02,l*.1,t*.23)},'
    # le rocher de Gibraltar : pente douce d'un côté, falaise de l'autre
    'rock:(e,l,t)=>{e.beginPath(),e.moveTo(0,t),e.lineTo(l*.08,t*.72),e.quadraticCurveTo(l*.42,t*.36,l*.62,t*.04),'
    'e.lineTo(l*.7,t*.02),e.lineTo(l*.78,t*.3),e.lineTo(l*.9,t*.62),e.lineTo(l,t),e.closePath(),e.fill()},'
    # une maison à toit plat avec sa tour
    'house:(e,l,t)=>{e.beginPath(),e.moveTo(0,t),e.lineTo(0,t*.42),e.lineTo(l*.62,t*.42),e.lineTo(l*.62,t*.12),e.lineTo(l*.66,t*.06),'
    'e.lineTo(l*.94,t*.06),e.lineTo(l*.98,t*.12),e.lineTo(l*.98,t),e.closePath(),e.fill()},'
    # une ville blanche en escalier, avec son minaret (Tanger)
    'medina:(e,l,t)=>{e.beginPath(),e.moveTo(0,t),e.lineTo(0,t*.62),e.lineTo(l*.14,t*.62),e.lineTo(l*.14,t*.5),e.lineTo(l*.3,t*.5),'
    'e.lineTo(l*.3,t*.4),e.lineTo(l*.44,t*.4),e.lineTo(l*.44,t*.12),e.lineTo(l*.455,t*.12),e.lineTo(l*.455,t*.05),e.lineTo(l*.485,t*.05),'
    'e.lineTo(l*.485,t*.12),e.lineTo(l*.5,t*.12),e.lineTo(l*.5,t*.36),e.lineTo(l*.62,t*.36),e.lineTo(l*.62,t*.46),e.lineTo(l*.78,t*.46),'
    'e.lineTo(l*.78,t*.56),e.lineTo(l,t*.56),e.lineTo(l,t),e.closePath(),e.fill()},'
    # la mer
    'waves:(e,l,t)=>{e.beginPath(),e.moveTo(0,t),e.lineTo(0,t*.5);for(let n=0;n<6;n++)e.quadraticCurveTo((n+.5)/6*l,t*(n%2?.28:.16),(n+1)/6*l,t*.5);'
    'e.lineTo(l,t),e.closePath(),e.fill()},'
)

FERRY_PAINT = ('(a,s,i)=>{a.fillStyle=E,a.fillRect(0,i*.7,s,i*.07),a.fillRect(s*.58,i*.02,s*.1,i*.07);a.fillStyle="#1B2230";'
               'for(let f=0;f<9;f++)a.fillRect(s*(.29+f*.062),i*.47,s*.03,i*.07);for(let f=0;f<5;f++)a.fillRect(s*(.42+f*.062),i*.29,s*.03,i*.06);'
               'a.fillStyle="rgba(0,0,0,0.16)",a.fillRect(0,i*.8,s,i*.2)}')
HOUSE_PAINT = ('(a,s,i)=>{a.fillStyle="rgba(0,0,0,0.28)",a.beginPath(),a.moveTo(s*.2,i),a.lineTo(s*.2,i*.74),'
               'a.quadraticCurveTo(s*.28,i*.58,s*.36,i*.74),a.lineTo(s*.36,i),a.fill(),a.fillRect(s*.74,i*.22,s*.1,i*.12),'
               'a.fillRect(s*.46,i*.56,s*.08,i*.1),a.fillStyle="rgba(255,255,255,0.18)",a.fillRect(0,i*.42,s*.62,i*.04)}')

# remplacements dans la scène de la section 01 (textes exacts du template)
LENGTHS = [
    # par la mer : le volcan devient un ferry, sa fumée sort de la cheminée, les collines deviennent la mer
    ('T(e,{scene:l,x:o*-3.05,z:-2.2,w:2.5,h:2.4,col:"#556B5E",shape:d.cone,paint:(a,s,i)=>{a.fillStyle="rgba(0,0,0,0.16)",a.beginPath(),a.moveTo(s*.5,i*.15),a.quadraticCurveTo(s*.6,i*.9,s,i),a.lineTo(s*.5,i),a.fill(),a.fillStyle="#7E5A4A",a.fillRect(s*.44,i*.12,s*.12,i*.06)},card:0,seed:1.1})',
     'T(e,{scene:l,x:o*-3.05,z:-1.95,w:3.1,h:1.7,col:"#EEE9DF",shape:d.ferry,paint:' + FERRY_PAINT + ',card:0,seed:1.1})'),
    ('T(e,{scene:l,x:o*-2.95,z:-2.24,w:.9,h:1.15,col:"#E4E8EA",shape:d.steam,paint:(a,s,i)=>{a.fillStyle="rgba(80,96,120,0.14)",a.fillRect(s*.5,0,s*.5,i)},seed:1.2,y0:2.24})',
     'T(e,{scene:l,x:o*-3.05+.49,z:-1.99,w:.8,h:1,col:"#E4E8EA",shape:d.steam,paint:(a,s,i)=>{a.fillStyle="rgba(80,96,120,0.14)",a.fillRect(s*.5,0,s*.5,i)},seed:1.2,y0:1.6})'),
    ('T(e,{scene:l,x:o*-3,z:-1.2,w:3.2,h:1.1,col:C.day.color,shape:d.hills,paint:(a,s,i)=>{a.fillStyle="rgba(255,255,255,0.12)",a.fillRect(0,i*.55,s,i*.04)},seed:1.3})',
     'T(e,{scene:l,x:o*-3,z:-1.2,w:3.6,h:.75,col:"#3F6F8F",shape:d.waves,paint:(a,s,i)=>{a.fillStyle="rgba(255,255,255,0.18)",a.fillRect(0,i*.62,s,i*.05),a.fillRect(0,i*.82,s,i*.04)},seed:1.3})'),
    ('Z(e,{scene:l,x:o*-3.45,z:-.45,w:.66,d:.4,col:"#4FA690",shape:d.lake,seed:1.4})', 'Z(e,{scene:l,x:o*-3.45,z:-.45,w:.66,d:.4,col:"#4F7FA6",shape:d.lake,seed:1.4})'),
    ('Z(e,{scene:l,x:o*-2.8,z:-.35,w:.5,d:.32,col:"#4FA690",shape:d.lake,seed:1.5})', 'Z(e,{scene:l,x:o*-2.8,z:-.35,w:.5,d:.32,col:"#4F7FA6",shape:d.lake,seed:1.5})'),
    # par le détroit : le pic devient le rocher de Gibraltar, la tente un petit ferry
    ('col:"#8C6A2C",shape:d.spire,paint:(a,s,i)=>{a.fillStyle="rgba(0,0,0,0.18)",a.beginPath(),a.moveTo(s*.5,i*.02),a.lineTo(s*.62,i*.3),a.lineTo(s*.74,i*.28),a.lineTo(s,i),a.lineTo(s*.5,i),a.fill()}',
     'col:"#8C6A2C",shape:d.rock,paint:(a,s,i)=>{a.fillStyle="rgba(0,0,0,0.18)",a.beginPath(),a.moveTo(s*.66,i*.03),a.lineTo(s*.78,i*.3),a.lineTo(s*.9,i*.62),a.lineTo(s,i),a.lineTo(s*.62,i),a.fill()}'),
    ('T(e,{scene:t,x:o*-.75,z:-.4,w:.74,h:.54,col:"#E0B85A",shape:d.tri,paint:(a,s,i)=>{a.fillStyle="rgba(0,0,0,0.3)",a.beginPath(),a.moveTo(s*.5,i*.35),a.lineTo(s*.4,i),a.lineTo(s*.6,i),a.fill()},seed:2.4})',
     'T(e,{scene:t,x:o*-.75,z:-.4,w:1.15,h:.62,col:"#EEE9DF",shape:d.ferry,paint:' + FERRY_PAINT + ',seed:2.4})'),
    ('T(e,{scene:t,x:o*-.15,z:-1.35,w:2.7,h:1.35,col:C.multi.color,shape:d.terraces,paint:(a,s,i)=>{a.fillStyle="rgba(0,0,0,0.12)";for(let f=1;f<6;f++)a.fillRect(0,i-f/6*i*.92-3,s,3)},seed:2.2})',
     'T(e,{scene:t,x:o*-.15,z:-1.35,w:2.7,h:1.35,col:"#E9E1D3",shape:d.medina,paint:(a,s,i)=>{a.fillStyle="rgba(0,0,0,0.22)";for(let f=0;f<14;f++)a.fillRect(s*(.04+f*.068),i*(.66+f%3*.09),s*.025,i*.06)},seed:2.2})'),
    # toute la route : les drapeaux de prière deviennent une kasbah, le refuge une maison
    ('T(e,{scene:n,x:o*3.7,z:-.65,w:1.5,h:.72,col:"#E8E2D6",shape:d.flags,paint:(a,s,i)=>{const f=["#5B8FC4","#F1EBDF","#D63B2F","#5E8C61","#D2A23A"];for(let c=0;c<9;c++){const r=(c+.5)/9,h=i*(.08+.18*Math.sin(Math.PI*r));a.fillStyle=f[c%5],a.fillRect(s*(.04+r*.88)-s*.035,h,s*.07,i*.2)}},seed:3.3})',
     'T(e,{scene:n,x:o*3.7,z:-.65,w:1.15,h:.9,col:"#D9B27A",shape:d.house,paint:' + HOUSE_PAINT + ',seed:3.3})'),
    ('T(e,{scene:n,x:o*1.95,z:-.45,w:.82,h:.64,col:"#EDE6D8",shape:d.hut,paint:(a,s,i)=>{a.fillStyle=C.exp.color,a.beginPath(),a.moveTo(0,i*.5),a.lineTo(s*.5,0),a.lineTo(s,i*.5),a.fill(),a.fillStyle="rgba(0,0,0,0.3)",a.fillRect(s*.42,i*.68,s*.16,i*.32)},seed:3.4})',
     'T(e,{scene:n,x:o*1.95,z:-.45,w:.9,h:.7,col:"#EDE6D8",shape:d.house,paint:' + HOUSE_PAINT + ',seed:3.4})'),
]

FOOT_CAMP_NEW = (
    '<div class="fx-camp" aria-hidden="true"><svg viewBox="0 0 220 90">'
    '<path class="fx-tent" d="M26 84 L26 40 L70 40 L70 30 L74 26 L96 26 L100 30 L100 84Z"/>'
    '<path class="fx-door" d="M42 84 L42 64 Q49 54 56 64 L56 84Z"/><path class="fx-door" d="M80 38 L88 38 L88 48 L80 48Z"/>'
    '<path class="fx-tent" d="M120 80 L120 62 Q120 57 125 57 L160 57 Q163 57 165 60 L172 69 L177 70.6 Q180 71.6 180 75 L180 80Z"/>'
    '<circle class="fx-door" cx="133" cy="81" r="5.5"/><circle class="fx-door" cx="167" cy="81" r="5.5"/>'
    '<circle class="fx-ball" cx="198" cy="30" r="8"/><path class="fx-ground" d="M10 86 L210 86"/></svg></div>'
)

# Le personnage en papier posé sur la table (main.js, fonction Ao) : une camionnette chargée,
# debout sur le même socle que le randonneur du template.
TABLE_VAN = (
    'function Ao(e){return function(t,o,n,l){'
    'const V=()=>{t.beginPath(),t.moveTo(o*.05,n*.76),t.lineTo(o*.05,n*.6),t.quadraticCurveTo(o*.05,n*.56,o*.1,n*.56),'
    't.lineTo(o*.62,n*.56),t.quadraticCurveTo(o*.66,n*.56,o*.69,n*.585),t.lineTo(o*.82,n*.66),t.lineTo(o*.9,n*.675),'
    't.quadraticCurveTo(o*.95,n*.685,o*.95,n*.71),t.lineTo(o*.95,n*.76),t.closePath()},'
    'W=()=>{t.beginPath(),t.arc(o*.25,n*.765,o*.085,0,6.2832),t.arc(o*.75,n*.765,o*.085,0,6.2832)},'
    'B=()=>{t.beginPath(),t.rect(o*.12,n*.495,o*.2,n*.066),t.rect(o*.35,n*.515,o*.18,n*.046)};'
    'if(e==="shape"){V(),t.fill(),W(),t.fill(),B(),t.fill(),Z(t,o*.5,n*.8,n,l,o*.1,null),t.fillRect(o*.2,n*.79,o*.64,n*.05);return}'
    'Z(t,o*.5,n*.8,n,0,o*.1,{body:"#E6DCC8",hi:"#FFFFFF",foot:"#D8CBB2"}),t.fillStyle="#E6DCC8",t.fillRect(o*.2,n*.79,o*.64,n*.05);'
    't.fillStyle=p.red,V(),t.fill(),t.fillStyle=p.ochre,B(),t.fill(),'
    't.fillStyle=p.paperHi,t.beginPath(),t.moveTo(o*.645,n*.59),t.lineTo(o*.71,n*.59),t.lineTo(o*.795,n*.66),t.lineTo(o*.645,n*.66),t.closePath(),t.fill(),'
    't.fillStyle=p.redDk,t.fillRect(o*.42,n*.57,o*.012,n*.18),'
    't.fillStyle=p.ink,W(),t.fill(),'
    't.fillStyle=p.paperHi,t.beginPath(),t.arc(o*.25,n*.765,o*.03,0,6.2832),t.arc(o*.75,n*.765,o*.03,0,6.2832),t.fill()'
)
