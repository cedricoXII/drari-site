/* Drari v0.5 · 06 Inscription : le ticket du transporteur (remplace sections/book.js du template).
   Un vrai <form> : trajet (les 5 + « Autre trajet »), mois de départ (plusieurs), départs par mois, prénom,
   numéro (type tel), email facultatif, bouton « Envoyer mon inscription ». Le talon reste, en décor.
   Rien n'est envoyé pour l'instant : le message de fin le dit. Aucune requête réseau. */
(function () {
  "use strict";
  const MONTHS = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"];
  const MON_SHORT = ["JAN", "FÉV", "MARS", "AVR", "MAI", "JUIN", "JUIL", "AOÛT", "SEPT", "OCT", "NOV", "DÉC"];
  const INK = "#121A26", PAPER = "#F3EEE4";
  /* fonds lisibles pour un texte crème (contraste 4,5:1 au moins) ; le jaune garde l'encre foncée */
  const DARK = { "#5E8C61": "#3F6B44", "#5B8FC4": "#2F5F8F", "#D63B2F": "#B3312A" };
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");
  const pad2 = (n) => String(n).padStart(2, "0");
  const VAN = '<svg viewBox="0 0 24 40" aria-hidden="true"><path d="M2.5 31 V18.5 Q2.5 15 6 15 H14.5 Q17.4 15 18.8 17.6 L21.5 23 V31 Z"/><circle cx="7.2" cy="32" r="3"/><circle cx="17.2" cy="32" r="3"/></svg>';
  const OTHER = 5;

  let C = null, R = [], root = null, form = null;
  const S = { k: -1, months: [], n: 2, sent: false };

  function routes() {
    R = C.T.map((t, i) => {
      const cat = C.catOf(t), yellow = cat === C.PAL.cats.multi;
      return { t, k: i, name: t.name, bg: yellow ? cat.color : DARK[cat.color] || cat.color, ink: yellow ? INK : PAPER, prof: t.profile || [] };
    });
  }

  /* le code-barres du talon : le relief du trajet, en barres */
  function bars(prof) {
    let h = "";
    const n = 46, a = prof.length ? prof[0][0] : 0, b = prof.length ? prof[prof.length - 1][0] : 1;
    const lo = prof.length ? Math.min(...prof.map((p) => p[1])) : 0, hi = prof.length ? Math.max(...prof.map((p) => p[1])) : 1;
    for (let i = 0; i < n; i++) {
      let v = 0.5 + 0.4 * Math.sin(i * 1.7) * Math.cos(i * 0.6);
      if (prof.length > 1) {
        const x = a + ((b - a) * i) / (n - 1);
        let j = 1;
        while (j < prof.length - 1 && prof[j][0] < x) j++;
        const p0 = prof[j - 1], p1 = prof[j], f = p1[0] - p0[0] ? (x - p0[0]) / (p1[0] - p0[0]) : 0;
        v = 0.18 + (0.82 * (p0[1] + (p1[1] - p0[1]) * f - lo)) / Math.max(1, hi - lo);
      }
      h += '<rect x="' + i * 4 + '" y="' + (40 * (1 - v)).toFixed(1) + '" width="' + (i % 5 === 0 ? 2.4 : 1.6) + '" height="' + (40 * v).toFixed(1) + '"/>';
    }
    return '<svg class="bt-bars" viewBox="0 0 184 40" preserveAspectRatio="none" aria-hidden="true">' + h + "</svg>";
  }

  function html() {
    const chips = R.map((r) =>
      '<button type="button" class="bt-chip" data-tk="' + r.k + '" aria-pressed="false" style="--cat:' + r.bg + ";--ink:" + r.ink + '">' +
      '<span>' + esc(r.name) + '</span><i class="bt-hole" aria-hidden="true"></i></button>').join("") +
      '<button type="button" class="bt-chip bt-chip-other" data-tk="' + OTHER + '" aria-pressed="false" aria-controls="btRouteBox" style="--cat:#1B2230;--ink:' + PAPER + '">' +
      '<span>Autre trajet</span><i class="bt-hole" aria-hidden="true"></i></button>';
    const months = MON_SHORT.map((m, i) =>
      '<button type="button" data-mo="' + i + '" aria-pressed="false" aria-label="' + MONTHS[i] + '"><span>' + m + "</span></button>").join("");
    const vans = [1, 2, 3, 4, 5, 6, 7, 8].map((n) =>
      '<button type="button" class="bt-w" data-n="' + n + '" aria-pressed="false" aria-label="' + n + (n === 1 ? " départ par mois" : " départs par mois") + '">' + VAN + "</button>").join("");
    return (
      '<form class="bo bt" id="ticket" novalidate aria-labelledby="h-book">' +
      '<div class="bt-mouth"><div class="bt-tk"><div class="bt-body">' +
      '<p class="bt-top" aria-hidden="true"><span>Drari</span><span>Ticket transporteur</span><span>No. 06<b data-f="no">··</b></span></p>' +
      '<fieldset class="bt-row"><legend class="bo-lab" id="btTrek">Trajet</legend><div class="bt-field">' +
      '<div class="bt-treks" role="group" aria-labelledby="btTrek" aria-describedby="errTrek">' + chips + "</div>" +
      '<div class="bo-in bt-route" id="btRouteBox" hidden><label for="btRoute">Ton trajet</label>' +
      '<input id="btRoute" name="route" type="text" autocomplete="off" placeholder="par exemple Lyon → Oujda…" aria-describedby="errTrek"></div>' +
      '<p class="bo-err" id="errTrek" aria-live="polite"></p></div></fieldset>' +
      '<fieldset class="bt-row"><legend class="bo-lab" id="btMonth">Mois de départ <small>(plusieurs choix possibles)</small></legend><div class="bt-field">' +
      '<div class="bo-months" role="group" aria-labelledby="btMonth">' + months + "</div></div></fieldset>" +
      '<fieldset class="bt-row"><legend class="bo-lab" id="btWalk">Départs par mois</legend><div class="bt-field">' +
      '<div class="bt-walk" role="group" aria-labelledby="btWalk">' + vans + '<b class="bt-wn" data-f="n" aria-hidden="true">2</b></div></div></fieldset>' +
      '<div class="bt-you">' +
      '<div class="bo-in"><label for="btName">Ton prénom</label><input id="btName" name="name" type="text" autocomplete="given-name" autocapitalize="words" spellcheck="false" aria-describedby="errName">' +
      '<p class="bo-err" id="errName" aria-live="polite"></p></div>' +
      '<div class="bo-in"><label for="btPhone">Ton numéro (WhatsApp)</label><input id="btPhone" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="06 12 34 56 78…" aria-describedby="errPhone">' +
      '<p class="bo-err" id="errPhone" aria-live="polite"></p></div>' +
      '<div class="bo-in"><label for="btMail">Ton email <em>(si tu préfères, facultatif)</em></label><input id="btMail" name="email" type="email" inputmode="email" autocomplete="email" spellcheck="false" aria-describedby="errMail">' +
      '<p class="bo-err" id="errMail" aria-live="polite"></p></div>' +
      "</div>" +
      '<div class="bt-go"><button type="submit" class="bt-send">Envoyer mon inscription<i aria-hidden="true">→</i></button>' +
      '<p class="bt-privacy">Ton numéro sert seulement à te rappeler pour préparer ta carte. Il n’est ni vendu, ni prêté.</p>' +
      '<p class="bo-done-line" role="status" aria-live="polite"></p>' +
      '<button type="button" class="bt-again" data-again hidden>Refaire un ticket</button></div>' +
      "</div>" +
      '<div class="bt-stub" aria-hidden="true"><span class="bt-no" data-f="no">··</span><b class="bt-name" data-f="name">Ton trajet</b>' +
      '<span class="bt-l"><em>Mois</em><i data-f="mo">Tous les mois</i></span><span class="bt-l"><em>Départs</em><i data-f="n">2</i></span>' +
      '<span class="bt-l"><em>Inscription</em><i>Gratuite</i></span><span class="bt-barw">' + bars([]) + "</span>" +
      '<span class="bt-tear"><svg viewBox="0 0 24 24"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M8.2 7.6 L20 17 M8.2 16.4 L20 7"/></svg></span></div>' +
      '</div></div><i class="bt-slot" aria-hidden="true"></i></form>'
    );
  }

  const $ = (s) => root.querySelector(s);
  const $$ = (s) => [...root.querySelectorAll(s)];

  function monthsText() {
    const m = S.months.slice().sort((a, b) => a - b);
    if (!m.length || m.length === 12) return "Tous les mois";
    if (m.length <= 3) return m.map((i) => MONTHS[i]).join(", ");
    return m.length + " mois";
  }

  function render() {
    const other = S.k === OTHER, r = R[S.k];
    const routeTxt = other ? ($("#btRoute").value.trim() || "Autre trajet") : r ? r.name : "Ton trajet";
    const vals = { no: S.k >= 0 ? pad2(S.k + 1) : "··", name: routeTxt, n: S.n, mo: monthsText() };
    $$("[data-f]").forEach((el) => { const v = vals[el.dataset.f]; if (v !== undefined && el.textContent !== String(v)) el.textContent = v; });
    $$("[data-tk]").forEach((b) => { const on = +b.dataset.tk === S.k; b.classList.toggle("on", on); b.setAttribute("aria-pressed", String(on)); });
    $$("[data-mo]").forEach((b) => { const on = S.months.indexOf(+b.dataset.mo) >= 0; b.classList.toggle("on", on); b.setAttribute("aria-pressed", String(on)); });
    $$("[data-n]").forEach((b) => { const n = +b.dataset.n; b.classList.toggle("on", n <= S.n); b.setAttribute("aria-pressed", String(n === S.n)); });
    const box = $("#btRouteBox");
    if (box.hidden === other) box.hidden = !other;
  }

  function setErr(id, input, msg) {
    const p = root.querySelector("#" + id);
    if (p) p.textContent = msg || "";
    if (input) { if (msg) input.setAttribute("aria-invalid", "true"); else input.removeAttribute("aria-invalid"); }
  }

  function pickRoute(k) {
    if (S.sent) return;
    const was = S.k;
    S.k = k;
    setErr("errTrek", $("#btRoute"), "");
    $(".bt-barw").innerHTML = bars(R[k] ? R[k].prof : []);
    render();
    if (k !== was) {
      const s = $(".bt-stub");
      s.classList.remove("flip"); void s.offsetWidth; s.classList.add("flip");
    }
  }

  const digits = (v) => (v.match(/\d/g) || []).length;
  const phoneOk = (v) => /^[+0-9 ().\-\/]+$/.test(v) && digits(v) >= 8 && digits(v) <= 15;
  const mailOk = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);

  function submit(e) {
    if (e) e.preventDefault();
    if (S.sent) return;
    const route = $("#btRoute"), name = $("#btName"), phone = $("#btPhone"), mail = $("#btMail");
    const v = { route: route.value.trim(), name: name.value.trim(), phone: phone.value.trim(), mail: mail.value.trim() };
    let first = null;
    const bad = (id, input, msg, focus) => { setErr(id, input, msg); if (!first) first = focus || input; };
    ["errTrek", "errName", "errPhone", "errMail"].forEach((id) => setErr(id, null, ""));
    [route, name, phone, mail].forEach((i) => i.removeAttribute("aria-invalid"));
    if (S.k < 0) bad("errTrek", null, "Choisis ton trajet.", $('[data-tk="0"]'));
    else if (S.k === OTHER && !v.route) bad("errTrek", route, "Écris ton trajet, par exemple Lyon → Oujda.");
    if (!v.name) bad("errName", name, "Écris ton prénom.");
    if (v.mail && !mailOk(v.mail)) bad("errMail", mail, "Cet email n’a pas l’air bon.");
    if (!v.phone && !(v.mail && mailOk(v.mail))) bad("errPhone", phone, "Écris ton numéro, par exemple 06 12 34 56 78.");
    else if (v.phone && !phoneOk(v.phone)) bad("errPhone", phone, "Ce numéro n’a pas l’air bon. Exemple : 06 12 34 56 78.");
    if (first) {
      const f = first.closest ? first.closest(".bo-in") : null;
      if (f) { f.classList.remove("shake"); void f.offsetWidth; f.classList.add("shake"); }
      first.focus();
      return;
    }
    S.sent = true;
    root.classList.add("sent");
    [route, name, phone, mail].forEach((i) => { i.readOnly = true; });
    $$("[data-tk],[data-mo],[data-n]").forEach((b) => { b.disabled = true; });
    $(".bt-send").disabled = true;
    $(".bo-done-line").textContent = "Merci, " + v.name.split(/\s+/)[0] + ". Version de test : rien n’est encore envoyé.";
    const again = $(".bt-again");
    again.hidden = false;
    setTimeout(() => { if (document.activeElement === $(".bt-send") || document.activeElement === document.body) again.focus({ preventScroll: true }); }, 400);
  }

  function reset() {
    S.sent = false;
    root.classList.remove("sent");
    $$("input").forEach((i) => { i.readOnly = false; });
    $$("[data-tk],[data-mo],[data-n]").forEach((b) => { b.disabled = false; });
    $(".bt-send").disabled = false;
    $(".bo-done-line").textContent = "";
    $(".bt-again").hidden = true;
    render();
    $("#btName").focus({ preventScroll: true });
  }

  function bind() {
    form.addEventListener("submit", submit);
    form.addEventListener("click", (e) => {
      const b = e.target.closest("button");
      if (!b || !form.contains(b) || b.type === "submit") return;
      if (b.dataset.tk !== undefined) {
        pickRoute(+b.dataset.tk);
        if (S.k === OTHER) setTimeout(() => $("#btRoute").focus(), 30);
      } else if (b.dataset.mo !== undefined) {
        if (S.sent) return;
        const m = +b.dataset.mo, i = S.months.indexOf(m);
        if (i >= 0) S.months.splice(i, 1); else S.months.push(m);
        render();
      } else if (b.dataset.n !== undefined) {
        if (S.sent) return;
        S.n = Math.max(1, Math.min(8, +b.dataset.n));
        render();
      } else if (b.hasAttribute("data-again")) reset();
    });
    form.addEventListener("input", (e) => {
      const t = e.target;
      if (t.id === "btRoute") { setErr("errTrek", t, ""); render(); }
      if (t.id === "btName") setErr("errName", t, "");
      if (t.id === "btPhone") setErr("errPhone", t, "");
      if (t.id === "btMail") setErr("errMail", t, "");
    });
    /* la machine à tickets « imprime » le ticket quand il arrive à l'écran ; tout de suite en page simple */
    const tk = $(".bt-tk");
    const print = () => root.classList.add("printed");
    form.addEventListener("focusin", print);
    if ((window.DR && window.DR.flat) || !("IntersectionObserver" in window)) print();
    else {
      const io = new IntersectionObserver((es) => { es.forEach((e) => { if (e.isIntersecting) { print(); io.disconnect(); } }); }, { rootMargin: "0px 0px -15% 0px" });
      io.observe(root);
      setTimeout(() => { if (root.getBoundingClientRect().top < window.innerHeight) print(); }, 3000);
    }
    if (tk) tk.addEventListener("transitionend", () => {}, { once: true });
    if (window.DR && window.DR.ticketReady) window.DR.ticketReady(root);
  }

  function init(el) {
    if (root) return;
    form = el.querySelector("#ticket");
    if (!form) return;
    root = form;
    bind();
    if (S.k >= 0) pickRoute(S.k); else render();
  }

  window.BOOK_STOP = {
    def(t) {
      C = t;
      routes();
      if (!document.getElementById("dr-book-css")) {
        const s = document.createElement("style");
        s.id = "dr-book-css";
        s.textContent = CSS;
        document.head.appendChild(s);
      }
      return {
        id: "book",
        kick: "Inscription",
        eyebrow: "À toi",
        flow: !0,
        cls: "bopt bo-ticket dr-free",
        title: ["Inscris ton trajet.", "<em>Ta carte est gratuite.</em>"],
        lede: "Choisis ton trajet et tes mois de départ. Laisse ton prénom et ton numéro : on te rappelle pour préparer ta carte.",
        pols: html(),
        cards: [],
      };
    },
    owns: (el) => !!el && el.classList.contains("bopt"),
    pinLen: () => 0,
    frame(t) { if (!root && t && t.el) init(t.el); },
    pick(key) {
      const i = R.findIndex((r) => r.t.key === key);
      if (i < 0) return;
      if (!root) { S.k = i; return; }
      if (S.sent) reset();
      pickRoute(i);
    },
    demo() {},
    get state() { return S; },
  };

  const CSS = `
.landing .stop.flow.bopt .stop-text{padding-bottom:3vh;}
.bo{position:relative;max-width:1120px;margin:0 auto;padding:0 calc(var(--pad-x) + 1vw);color:${INK};font-family:var(--f-text);}
.bo button{appearance:none;-webkit-appearance:none;border:0;background:none;margin:0;font:inherit;color:inherit;cursor:pointer;touch-action:manipulation;}
.bo button:focus-visible,.bo input:focus-visible{outline:3px solid ${INK};outline-offset:2px;}
.bo fieldset{border:0;margin:0;padding:0;min-width:0;}
.bt{display:flex;flex-direction:column;align-items:center;}
.bt-mouth{position:relative;width:min(1060px,100%);overflow:hidden;padding:20px 20px 0;margin:-20px auto 0;box-sizing:border-box;}
.bt-tk{position:relative;display:flex;width:100%;filter:drop-shadow(0 22px 26px rgba(0,0,0,0.6));transform:translateY(102%);transition:transform 1.5s steps(9, jump-end);}
.bt.printed .bt-tk{transform:none;transition:transform 1.2s cubic-bezier(.3,.85,.3,1);}
.bt-slot{display:block;width:min(1040px,100%);height:10px;margin-top:-4px;border-radius:5px;background:#05080D;box-shadow:inset 0 2px 3px rgba(0,0,0,0.9), 0 1px 0 rgba(255,255,255,0.08);}
.bt-body{position:relative;flex:1 1 auto;min-width:0;padding:22px 32px 26px;background:${PAPER} linear-gradient(180deg, rgba(255,255,255,0.35), rgba(0,0,0,0.03));
  -webkit-mask:radial-gradient(circle 12px at 0 50%, transparent 98%, #000);mask:radial-gradient(circle 12px at 0 50%, transparent 98%, #000);}
.bt-top{display:flex;justify-content:space-between;gap:12px;margin:0 0 16px;padding-bottom:10px;border-bottom:1.5px solid rgba(18,26,38,0.8);font-family:var(--f-label);font-stretch:var(--l-st,100%);font-size:12px;letter-spacing:0.16em;text-transform:uppercase;color:${INK};}
.bt-top b{font-weight:500;color:#B3312A;}
.bo .bt-row{display:grid;grid-template-columns:150px minmax(0,1fr);align-items:start;column-gap:16px;margin:0 0 20px;}
.bo-lab{float:left;padding:14px 0 0;margin:0;font-family:var(--f-label);font-stretch:var(--l-st,100%);font-size:12px;line-height:1.35;letter-spacing:0.12em;text-transform:uppercase;color:#3A4252;}
.bo-lab small{display:block;margin-top:4px;font-size:12px;letter-spacing:0.04em;text-transform:none;font-family:var(--f-text);color:#4A5263;}
.bt-row > .bo-lab{grid-column:1;}
.bt-field{grid-column:2;min-width:0;}
.bt-treks{display:flex;flex-wrap:wrap;gap:8px;}
.bt-chip{position:relative;min-height:48px;padding:0 34px 0 14px !important;border-radius:3px;border:1.5px solid rgba(18,26,38,0.4) !important;background:rgba(255,255,255,0.55) !important;color:${INK} !important;
  font-family:var(--f-display) !important;font-weight:500;font-size:15px !important;letter-spacing:-0.01em;white-space:nowrap;transition:background-color .18s ease, color .18s ease, transform .18s ease;}
.bt-chip span{display:block;}
.bt-chip.on{background:var(--cat) !important;color:var(--ink) !important;border-color:var(--cat) !important;transform:translateY(-1px);box-shadow:0 6px 10px -6px rgba(0,0,0,0.6);}
.bt-hole{position:absolute;right:11px;top:50%;width:12px;height:12px;margin-top:-6px;border-radius:50%;border:1.5px solid currentColor;opacity:0.55;box-sizing:border-box;}
.bt-chip.on .bt-hole{opacity:1;background:#0A1019;border-color:#0A1019;box-shadow:inset 0 1px 2px rgba(0,0,0,0.8);}
.bt-chip-other.on .bt-hole{background:${PAPER};border-color:${PAPER};}
.bt-route{margin-top:12px;}
.bo-months{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:6px;}
.bo-months button{position:relative;min-height:48px;border-radius:3px;border:1.5px solid rgba(18,26,38,0.35) !important;background:rgba(255,255,255,0.55) !important;color:${INK};
  font-family:var(--f-label);font-stretch:var(--l-st,100%);font-size:13px;letter-spacing:0.06em;text-transform:uppercase;transition:background-color .18s ease, color .18s ease;}
.bo-months button.on{background:#B3312A !important;border-color:#B3312A !important;color:#FFF8EE;}
.bo-months button.on::after{content:'';position:absolute;right:6px;top:6px;width:6px;height:6px;border-radius:50%;background:#FFF8EE;}
.bt-walk{display:flex;flex-wrap:wrap;align-items:center;gap:4px;}
.bt-w{width:44px;height:48px;padding:4px 8px !important;color:rgba(18,26,38,0.32);border-radius:3px;transition:color .18s ease, transform .18s ease;}
.bt-w svg{display:block;width:100%;height:100%;fill:currentColor;}
.bt-w.on{color:#B3312A;}
.bt-wn{margin-left:8px;font-family:var(--f-display);font-weight:500;font-size:20px;color:${INK};font-variant-numeric:tabular-nums;}
.bt-you{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px 18px;margin:4px 0 0;}
.bo-in{display:flex;flex-direction:column;gap:6px;min-width:0;margin:0;}
.bo-in[hidden]{display:none !important;}
.bt-you .bo-in label{min-height:2.7em;}
.bo-in label{font-family:var(--f-label);font-stretch:var(--l-st,100%);font-size:12px;line-height:1.35;letter-spacing:0.1em;text-transform:uppercase;color:#3A4252;}
.bo-in label em{font-style:normal;text-transform:none;letter-spacing:0.02em;font-family:var(--f-text);color:#4A5263;}
.bo-in input{appearance:none;-webkit-appearance:none;width:100%;min-width:0;box-sizing:border-box;height:48px;padding:0 12px;border:0;border-bottom:2px solid rgba(18,26,38,0.45);border-radius:3px 3px 0 0;
  background:rgba(18,26,38,0.05);font:inherit;font-family:var(--f-text);font-size:16px;color:${INK};outline:none;transition:border-color .18s ease, background-color .18s ease;}
.bo-in input::placeholder{color:#6B7280;opacity:1;}
.bo-in input:focus{border-color:${INK};background:rgba(18,26,38,0.09);}
.bo-in input[aria-invalid="true"]{border-color:#A8302A;background:rgba(168,48,42,0.07);}
.bo-in input[readonly]{background:rgba(18,26,38,0.03);}
.bo-in.shake{animation:boShake .35s ease;}
@keyframes boShake{20%,60%{transform:translateX(-4px);}40%,80%{transform:translateX(4px);}}
.bo-err{min-height:0;margin:2px 0 0;font-size:14px;line-height:1.4;color:#A8302A;font-weight:600;}
.bo-err:empty{margin:0;}
.bt-go{margin:22px 0 0;display:flex;flex-direction:column;align-items:flex-start;gap:10px;}
.bt-send{display:inline-flex !important;align-items:center;justify-content:center;gap:12px;min-height:52px;padding:0 26px !important;border-radius:4px;background:#B3312A !important;color:#FFF8EE !important;
  font-family:var(--f-text) !important;font-weight:600;font-size:17px !important;box-shadow:0 12px 22px -12px rgba(0,0,0,0.7);transition:transform .15s ease, background-color .15s ease;}
.bt-send i{font-style:normal;}
.bt-send:hover{background:#9E2B24 !important;transform:translateY(-1px);}
.bt-send:active{transform:scale(.98);}
.bt-send:disabled{background:#6B4A47 !important;cursor:default;transform:none;}
.bt-privacy{margin:0;max-width:60ch;font-size:14px;line-height:1.5;color:#3A4252;}
.bo-done-line{margin:0;font-family:var(--f-display);font-size:18px;line-height:1.4;color:${INK};}
.bo-done-line:empty{display:none;}
.bo-done-line:not(:empty)::before{content:'✓';display:inline-block;margin-right:10px;color:#3F6B44;font-weight:700;}
.bt-again{min-height:44px;padding:0 2px !important;font-family:var(--f-label) !important;font-size:13px;letter-spacing:0.12em;text-transform:uppercase;color:#B3312A !important;border-bottom:1.5px solid rgba(179,49,42,0.5) !important;}
.bt-again[hidden]{display:none !important;}
/* le talon, en décor */
.bt-stub{position:relative;flex:0 0 240px;display:flex;flex-direction:column;align-items:flex-start;padding:22px 22px 18px;box-sizing:border-box;color:${INK};
  background:#E9E0CC linear-gradient(180deg, rgba(255,255,255,0.3), rgba(0,0,0,0.04));border-left:2px dashed rgba(18,26,38,0.35);transform-origin:0 0;
  -webkit-mask:radial-gradient(circle 12px at 100% 50%, transparent 98%, #000);mask:radial-gradient(circle 12px at 100% 50%, transparent 98%, #000);transition:transform 1.1s cubic-bezier(.5,-0.2,.6,1), opacity .9s ease .3s;}
.bt-no{font-family:var(--f-display);font-weight:500;font-size:46px;line-height:0.9;letter-spacing:-0.03em;color:#B3312A;}
.bt-name{margin:8px 0 12px;font-family:var(--f-display);font-weight:500;font-size:18px;line-height:1.2;letter-spacing:-0.015em;color:${INK};overflow-wrap:anywhere;}
.bt-l{display:flex;justify-content:space-between;gap:10px;width:100%;padding:6px 0;border-top:1px dotted rgba(18,26,38,0.35);font-size:14px;}
.bt-l em{font-style:normal;font-family:var(--f-label);font-size:12px;letter-spacing:0.12em;text-transform:uppercase;color:#3A4252;align-self:center;}
.bt-l i{font-style:normal;font-weight:600;text-align:right;}
.bt-barw{display:block;width:100%;margin-top:auto;padding-top:14px;}
.bt-bars{display:block;width:100%;height:34px;fill:${INK};}
.bt-tear{display:block;margin-top:8px;color:#B3312A;}
.bt-tear svg{display:block;width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:1.8;transform:rotate(-90deg);}
.bt-stub.flip .bt-no,.bt-stub.flip .bt-name{animation:btFlip .5s ease;}
@keyframes btFlip{0%{transform:rotateX(0);}45%{transform:rotateX(90deg);}100%{transform:rotateX(0);}}
.bt.sent .bt-stub{transform:translate(40px, 60px) rotate(10deg);opacity:0.25;}
@media (max-width:900px){
  .bt-you{grid-template-columns:1fr 1fr;}
  .bt-you .bo-in:last-child{grid-column:1 / -1;}
}
@media (max-width:760px){
  .bo{padding:0 12px;}
  .bt-mouth{padding:12px 6px 0;margin:-12px auto 0;}
  .bt-tk{flex-direction:column;}
  .bt-body{padding:18px 16px 22px;-webkit-mask:none;mask:none;}
  .bo .bt-row{grid-template-columns:1fr;margin-bottom:18px;}
  .bo-lab{float:none;padding:0 0 8px;}
  .bt-field{grid-column:1;}
  .bt-chip{flex:1 1 auto;}
  .bo-months{grid-template-columns:repeat(4,minmax(0,1fr));}
  .bt-walk{display:grid;grid-template-columns:repeat(4,46px) 1fr;gap:4px 6px;}
  .bt-wn{grid-column:5;grid-row:1 / span 2;align-self:center;justify-self:start;margin-left:6px;font-size:24px;}
  .bt-you{grid-template-columns:1fr;gap:14px;}
  .bt-you .bo-in label{min-height:0;}
  .bt-go{align-items:stretch;}
  .bt-send{width:100%;}
  .bt-stub{flex:0 0 auto;width:100%;display:grid;grid-template-columns:auto 1fr;column-gap:14px;padding:14px 16px;border-left:0;border-top:2px dashed rgba(18,26,38,0.35);-webkit-mask:none;mask:none;}
  .bt-no{grid-row:1 / span 2;font-size:38px;}
  .bt-name{margin:0;font-size:16px;}
  .bt-l{grid-column:2;}
  .bt-barw{grid-column:1 / -1;padding-top:10px;}
  .bt-bars{height:22px;}
  .bt-tear{display:none;}
  .bt.sent .bt-stub{transform:none;opacity:0.4;}
}
@media (prefers-reduced-motion: reduce){ .bt-tk,.bt-stub,.bt-chip,.bt-w,.bo-months button,.bt-send{transition:none !important;} .bt-stub.flip .bt-no,.bt-stub.flip .bt-name,.bo-in.shake{animation:none;} .bt.sent .bt-stub{transform:none;opacity:0.4;} }
html.dr-rm .bt-tk{transition:none !important;}
`;
})();
