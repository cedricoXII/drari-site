/* Drari v0.5 · 04 Gratuit ? : comment Drari gagne sa vie (remplace sections/when.js, « Quand partir », qui parle aux
   familles et ira sur la landing n° 2). Même branchement que l'ancien module (window.WHEN_STOP), section simple,
   sans épinglage. Les prix sont ceux du dossier (19,99 € et 49,99 € par mois) ; aucun prix barré, aucune urgence. */
(function () {
  "use strict";
  const OFFERS = [
    { name: "Gratuit", price: "0 €", per: "", text: "ta carte, ton trajet, les demandes des familles, tes papiers de voyage.", tone: "free" },
    { name: "Pro", price: "19,99 €", per: "par mois", text: "l’IA qui lit tes documents et t’aide à écrire.", tone: "pro" },
    { name: "Pro+", price: "49,99 €", per: "par mois", text: "ta carte en premier sur ton trajet, toujours signalée comme payante. Quand les familles seront sur le site.", tone: "plus" },
  ];
  function html() {
    return (
      '<div class="prc-in">' +
      '<ul class="prc-list">' +
      OFFERS.map((o) =>
        '<li class="prc-o prc-' + o.tone + '"><p class="prc-name">' + o.name + '</p>' +
        '<p class="prc-price"><b>' + o.price + "</b>" + (o.per ? "<span>" + o.per + "</span>" : "") + "</p>" +
        '<p class="prc-text">' + o.text + "</p></li>").join("") +
      "</ul>" +
      '<p class="prc-note">Pas de commission sur tes clients&nbsp;: l’argent du transport reste entre toi et la famille.</p>' +
      '<figure class="prc-quote"><blockquote><p>«&nbsp;Notre combat&nbsp;: rendre visibles les transporteurs sérieux, et remettre de la confiance dans ce métier.&nbsp;»</p></blockquote>' +
      "<figcaption>Cédric, fondateur de Drari</figcaption></figure>" +
      "</div>"
    );
  }
  const CSS = `
.prc-in{max-width:1080px;margin:0 auto;padding:0 calc(var(--pad-x) + 1vw);}
.prc-list{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(280px,100%),1fr));gap:16px;}
.prc-o{position:relative;display:flex;flex-direction:column;gap:10px;padding:22px 22px 24px;border-radius:4px;color:#121A26;
  background:#F3EEE4 linear-gradient(170deg, rgba(255,255,255,0.4), rgba(0,0,0,0.05));box-shadow:0 22px 34px -22px rgba(0,0,0,0.9);}
.prc-o::before{content:'';position:absolute;left:0;right:0;top:0;height:6px;border-radius:4px 4px 0 0;background:#3F6B44;}
.prc-pro::before{background:#2F5F8F;} .prc-plus::before{background:#B3312A;}
.prc-name{margin:6px 0 0;font-family:var(--f-label);font-stretch:var(--l-st,100%);font-size:13px;letter-spacing:0.14em;text-transform:uppercase;color:#3A4252;}
.prc-price{margin:0;display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;font-variant-numeric:tabular-nums;}
.prc-price b{font-family:var(--f-display);font-weight:500;font-size:clamp(28px,2.6vw,36px);letter-spacing:-0.02em;color:#121A26;}
.prc-price span{font-size:15px;color:#3A4252;}
.prc-text{margin:0;font-size:16px;line-height:1.5;color:#2A3242;}
.prc-note{max-width:60ch;margin:26px 0 0;font-size:17px;line-height:1.5;color:rgba(var(--c-text-rgb),0.9);}
.prc-quote{max-width:62ch;margin:30px 0 0;padding:4px 0 4px 20px;border-left:3px solid #E5483B;}
.prc-quote blockquote{margin:0;}
.prc-quote p{margin:0;font-family:var(--f-display);font-weight:400;font-size:clamp(19px,1.6vw,23px);line-height:1.4;letter-spacing:-0.01em;color:var(--c-text);}
.prc-quote figcaption{margin-top:10px;font-size:15px;color:rgba(var(--c-text-rgb),0.82);}
.landing .stop.flow.prc .stop-text{padding-bottom:4vh;}
@media (min-width:761px){ .prc-o{padding:26px 26px 28px;} .prc-text{font-size:17px;} }
`;
  let done = false;
  window.WHEN_STOP = {
    def() {
      if (!done) {
        const s = document.createElement("style");
        s.id = "dr-price-css";
        s.textContent = CSS;
        document.head.appendChild(s);
        done = true;
      }
      return {
        id: "gratuit",
        kick: "Gratuit ?",
        eyebrow: "Gratuit ?",
        flow: !0,
        cls: "prc dr-free",
        title: ["Comment Drari", "<em>gagne sa vie.</em>"],
        lede: "Ta carte est gratuite : ta route, tes dates, ton prix, les demandes des familles. Drari gagnera sa vie avec des options pour ceux qui veulent plus, quand l’espace pro ouvrira.",
        pols: html(),
        cards: [],
      };
    },
    owns: (el) => !!el && el.classList.contains("prc"),
    pinLen: () => 0,
    frame() {},
  };
})();
