/* Drari v0.5 · le pied de page (remplace sections/footer.js du template).
   Retirés : la carte postale « Le courrier Drari » (l'envoi n'existe pas), les 4 timbres de réseaux (comptes pas créés),
   l'adresse email provisoire en .example (elle ne reçoit rien) et les horloges. Gardés : « Bon trajet », la maison et la
   camionnette, « Fin du trajet… », « Retour au départ », « Lancement en cours ». Ajouté : ce que fait Drari, en une ligne. */
(function () {
  "use strict";
  const CAMP =
    '<div class="fx-camp" aria-hidden="true"><svg viewBox="0 0 220 90">' +
    '<path class="fx-tent" d="M26 84 L26 40 L70 40 L70 30 L74 26 L96 26 L100 30 L100 84Z"/>' +
    '<path class="fx-door" d="M42 84 L42 64 Q49 54 56 64 L56 84Z"/><path class="fx-door" d="M80 38 L88 38 L88 48 L80 48Z"/>' +
    '<path class="fx-tent" d="M120 80 L120 62 Q120 57 125 57 L160 57 Q163 57 165 60 L172 69 L177 70.6 Q180 71.6 180 75 L180 80Z"/>' +
    '<circle class="fx-door" cx="133" cy="81" r="5.5"/><circle class="fx-door" cx="167" cy="81" r="5.5"/>' +
    '<circle class="fx-ball" cx="198" cy="30" r="8"/><path class="fx-ground" d="M10 86 L210 86"/></svg></div>';
  const word = (w, cls) =>
    '<span class="fx-w ' + cls + '">' +
    [...w].map((ch, i) => '<span style="--r:' + [-3, 2, -1.5, 2.5, -2, 1][i % 6] + "deg;--d:" + (i * 0.06).toFixed(2) + 's">' + ch + "</span>").join("") +
    "</span>";
  const pan = (p, inner) => '<div class="fx-pan" data-p="' + p + '"><div class="fx-pan-in">' + inner + "</div></div>";

  function html() {
    return (
      '<footer class="foot fx" id="foot"><div class="fx-sheet">' +
      pan(1, '<p class="fx-big"><span class="sr-only">Bon trajet</span><span class="fx-ws" aria-hidden="true">' + word("Bon", "a") + word("trajet", "b") + "</span></p>") +
      pan(2,
        '<div class="fx-base"><div class="fx-end">' + CAMP +
        "<p>Fin du trajet. Tout le monde est bien arrivé.</p>" +
        '<button type="button" class="fx-up" data-act="top">Retour au départ<i aria-hidden="true">↑</i></button></div>' +
        '<div class="fx-talk"><p class="fx-hours"><i aria-hidden="true"></i><span>Lancement en cours</span></p>' +
        '<p class="fx-what">Drari met en relation&nbsp;: il ne transporte rien et ne touche pas l’argent du transport.</p></div></div>') +
      "</div></footer>"
    );
  }

  function init(doc) {
    const o = doc.querySelector(".fx");
    if (!o || o._init) return;
    o._init = true;
    const up = o.querySelector("[data-act=top]");
    up && up.addEventListener("click", () => {
      const t = window.APP && window.APP.TR;
      t && t.home ? t.home() : window.scrollTo({ top: 0, behavior: window.DR && window.DR.rm ? "auto" : "smooth" });
    });
    const parts = [...o.querySelectorAll(".fx-big, .fx-base")];
    const flat = window.DR && window.DR.flat;
    if (flat || !("IntersectionObserver" in window)) { parts.forEach((p) => p.classList.add("in")); return; }
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { rootMargin: "0px 0px -12% 0px" });
    parts.forEach((p) => io.observe(p));
  }

  const CSS = `
.foot.fx{position:relative;z-index:4;padding:8vh clamp(10px,2.4vw,40px) calc(28px + env(safe-area-inset-bottom));border-top:0;background:var(--c-room,#0A1019);color:var(--c-text);overflow:hidden;}
.fx-sheet{max-width:1460px;margin:0 auto;}
.fx-pan-in{position:relative;container-type:inline-size;background-color:#0F1825;
  background-image:repeating-radial-gradient(ellipse 120% 90% at 16% 24%, rgba(233,226,211,0.032) 0 1px, transparent 1.5px 28px), repeating-radial-gradient(ellipse 110% 100% at 86% 88%, rgba(233,226,211,0.026) 0 1px, transparent 1.5px 34px);
  box-shadow:0 0 0 1px rgba(255,255,255,0.025), 0 40px 60px -40px rgba(0,0,0,0.9);}
.fx-pan + .fx-pan > .fx-pan-in::before{content:'';position:absolute;left:0;right:0;top:0;height:3px;pointer-events:none;background:linear-gradient(rgba(0,0,0,0.5), rgba(255,255,255,0.05) 60%, transparent);}
.fx-pan[data-p="1"] > .fx-pan-in{padding:7vh clamp(16px,3vw,52px) 6vh;}
.fx-pan[data-p="2"] > .fx-pan-in{padding:5vh clamp(16px,3vw,52px) 5vh;}
.fx button{appearance:none;border:0;background:none;padding:0;margin:0;font:inherit;color:inherit;cursor:pointer;}
.fx :focus-visible{outline:3px solid #E5483B;outline-offset:3px;}
/* le nom en lettres de papier : « Bon trajet » fait environ 5,3 fois sa taille de texte, donc 17 % de la largeur du panneau, 220 px au plus */
.fx-big{position:relative;max-width:1320px;margin:0 auto;font-family:var(--f-display);font-weight:var(--d-w,400);font-size:min(220px, 17cqi);line-height:0.9;letter-spacing:-0.05em;perspective:900px;}
.fx-ws{display:flex;flex-wrap:nowrap;white-space:nowrap;align-items:baseline;justify-content:center;gap:0 0.18em;}
.fx-w{display:inline-flex;}
.fx-w > span{display:inline-block;transform-origin:50% 92%;transform:rotateX(88deg);opacity:0;transition:transform .9s cubic-bezier(.2,1.5,.35,1) var(--d), opacity .2s ease var(--d);}
.fx-w.a > span{color:#E9E2D3;text-shadow:0 0.03em 0 rgba(0,0,0,0.35);}
.fx-w.b > span{color:#E5483B;text-shadow:0 0.03em 0 rgba(0,0,0,0.35);transition-delay:calc(var(--d) + .24s);}
.fx-big.in .fx-w > span{transform:rotate(var(--r));opacity:1;}
.fx-base{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);align-items:end;gap:28px;max-width:1320px;margin:0 auto;opacity:0;transition:opacity .8s ease .2s;}
.fx-base.in{opacity:1;}
.fx-end{grid-column:2;display:flex;flex-direction:column;align-items:center;gap:8px;text-align:center;}
.fx-camp svg{display:block;width:132px;height:54px;overflow:visible;}
.fx-end p{margin:0;font-size:15px;line-height:1.5;color:rgba(var(--c-text-rgb),0.82);}
.fx-tent{fill:#D2A23A;} .fx-door{fill:rgba(0,0,0,0.3);} .fx-ball{fill:#E5483B;}
.fx-ground{stroke:rgba(var(--c-text-rgb),0.3);stroke-width:1.5;stroke-dasharray:5 5;}
.fx-up{display:inline-flex !important;align-items:center;gap:8px;min-height:44px;padding:0 4px !important;font-family:var(--f-label) !important;font-stretch:var(--l-st,100%);font-size:13px !important;letter-spacing:0.12em;text-transform:uppercase;color:rgba(var(--c-text-rgb),0.86) !important;border-bottom:1px solid rgba(var(--c-text-rgb),0.25) !important;}
.fx-up i{font-style:normal;color:#E5483B;font-size:14px;}
.fx-up:hover{color:var(--c-text) !important;border-color:#E5483B !important;}
.fx-talk{grid-column:3;justify-self:end;max-width:42ch;text-align:right;}
.fx-hours{display:flex;align-items:center;justify-content:flex-end;gap:9px;margin:0;font-family:var(--f-label);font-stretch:var(--l-st,100%);font-size:13px;letter-spacing:0.1em;text-transform:uppercase;color:rgba(var(--c-text-rgb),0.86);}
.fx-hours i{width:8px;height:8px;border-radius:50%;background:#5E8C61;box-shadow:0 0 0 4px rgba(94,140,97,0.25);flex:0 0 auto;}
.fx-what{margin:10px 0 0;font-size:15px;line-height:1.5;color:rgba(var(--c-text-rgb),0.82);}
@media (max-width:760px){
  .foot.fx{padding:6vh 8px calc(104px + env(safe-area-inset-bottom));}
  .fx-pan[data-p] > .fx-pan-in{padding-left:12px;padding-right:12px;}
  .fx-base{grid-template-columns:1fr;gap:24px;}
  .fx-end{grid-column:1;} .fx-talk{grid-column:1;justify-self:center;text-align:center;} .fx-hours{justify-content:center;}
}
@media (prefers-reduced-motion: reduce){ .fx *{transition:none !important;animation:none !important;} .fx .fx-w > span,.fx .fx-base{opacity:1 !important;} .fx .fx-w > span{transform:rotate(var(--r)) !important;} }
html.dr-flat .fx-w > span{transition:none;}
`;
  let done = false;
  window.FOOT_X = {
    html() {
      if (!done) {
        const s = document.createElement("style");
        s.id = "dr-foot-css";
        s.textContent = CSS;
        document.head.appendChild(s);
        done = true;
      }
      setTimeout(() => init(document), 0);
      return html();
    },
    init,
  };
})();
