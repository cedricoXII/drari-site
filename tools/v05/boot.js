/* Drari v0.5 : ce qui doit marcher avant la 3D (lu tout de suite, avant les gros scripts).
   - DR.flat : page simple, sans sections épinglées ni défilement « scrub » (mouvement réduit, téléphone, ou pas de WebGL)
   - les boutons « Inscrire mon trajet » [data-cta] mènent au ticket lui-même (même touchés avant qu'il soit construit)
   - la barre du bas (téléphone) : visible quand le bouton du haut de page est sorti de l'écran, cachée sur le ticket
   - l'en-tête prend un fond dès que la page défile
   - sans WebGL : les sections et le ticket sont construits quand même, sans la 3D (DR.noGL, appelé par le script principal)
   - le menu est construit dès que la page est lue */
(function () {
  "use strict";
  var d = document.documentElement;
  var mq = function (q) { try { return window.matchMedia(q).matches; } catch (e) { return false; } };
  var rm = mq("(prefers-reduced-motion: reduce)");
  var vw = Math.min(window.innerWidth || 9999, d.clientWidth || 9999);
  var narrow = vw <= 760;
  var phone = mq("(pointer: coarse)") && Math.min(screen.width || 9999, screen.height || 9999) < 600;
  var flat = rm || narrow || phone;
  var DR = window.DR = { rm: rm, narrow: narrow, phone: phone, flat: flat };
  if (rm) d.classList.add("dr-rm");
  if (flat) d.classList.add("dr-flat");

  var headerH = function () { var t = document.querySelector(".top"); return t ? t.offsetHeight : 64; };

  /* aller au ticket : par le script de la page s'il est prêt (défilement doux), sinon directement.
     Touché trop tôt (les premières secondes, sur un téléphone lent : ticket pas encore construit, ou arrivée de la 3D
     pas finie, défilement bloqué) : on y va dès que la page est prête. */
  var wantTicket = 0, waiting = false;
  var isLive = function () { return d.classList.contains("hero-live") || d.classList.contains("no-webgl"); };
  var scrollToTicket = function (t) {
    var a = window.APP && window.APP.TR;
    if (a && a.book) { a.book(); return; }
    var y = t.getBoundingClientRect().top + window.scrollY - headerH() - 12;
    window.scrollTo({ top: Math.max(0, y), behavior: rm ? "auto" : "smooth" });
  };
  DR.toTicket = function () {
    var t = document.getElementById("ticket");
    if (!t) { wantTicket = Date.now(); return true; }
    if (!isLive()) { if (!waiting) { waiting = true; goWhenReady(60, -1, false); } return true; }
    scrollToTicket(t);
    return true;
  };
  /* attendre la fin de la mise en place (classe hero-live ou no-webgl, hauteur de page stable ; 18 s au plus), aller au ticket,
     puis vérifier une fois qu'on y est bien */
  var goWhenReady = function (n, h0, done) {
    var h = d.scrollHeight, t = document.getElementById("ticket");
    if ((isLive() && h === h0) || n <= 0) {
      waiting = false;
      if (!t) return;
      scrollToTicket(t);
      if (!done) setTimeout(function () {
        var r = t.getBoundingClientRect().top;
        if (r < 0 || r > 240) goWhenReady(10, -1, true);
      }, 2500);
      return;
    }
    setTimeout(function () { goWhenReady(n - 1, h, done); }, 300);
  };
  /* aller à une section (menu), sans la 3D */
  DR.go = function (i) {
    var s = i >= 0 ? document.querySelectorAll("#landing .stop")[i] : null;
    var y = s ? s.getBoundingClientRect().top + window.scrollY - headerH() : 0;
    window.scrollTo({ top: Math.max(0, y), behavior: rm ? "auto" : "smooth" });
  };
  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest("[data-cta]") : null;
    if (!a) return;
    if (DR.toTicket()) e.preventDefault();
  });

  /* l'en-tête : un fond dès qu'on a quitté le tout haut de la page */
  var sc = false;
  var onScroll = function () {
    var s = window.scrollY > 8;
    if (s !== sc) { sc = s; d.classList.toggle("dr-scrolled", s); }
  };
  window.addEventListener("scroll", onScroll, { passive: true });

  /* la barre du bas, sur téléphone (cachée aussi quand le bouton après « Ta carte » est à l'écran : un seul bouton à la fois) */
  var heroGone = false, formOn = false, ctaOn = false, bar = null, ctas = [], ctaIO = null;
  var watchCtas = function () {
    if (!("IntersectionObserver" in window)) return;
    if (!ctaIO) ctaIO = new IntersectionObserver(function (es) {
      es.forEach(function (e) { e.target._drIn = e.isIntersecting; });
      ctaOn = ctas.some(function (x) { return x._drIn; });
      paint();
    });
    document.querySelectorAll(".dr-after [data-cta]").forEach(function (a) {
      if (ctas.indexOf(a) < 0) { ctas.push(a); ctaIO.observe(a); }
    });
  };
  var paint = function () {
    if (!bar) return;
    var on = heroGone && !formOn && !ctaOn;
    if (on === bar._on) return;
    bar._on = on;
    bar.classList.toggle("on", on);
    bar.setAttribute("aria-hidden", on ? "false" : "true");
    var a = bar.querySelector("a");
    if (a) { if (on) a.removeAttribute("tabindex"); else a.setAttribute("tabindex", "-1"); }
  };
  DR.ticketReady = function (el) {
    watchCtas();
    if (wantTicket && Date.now() - wantTicket < 20000 && !waiting) { wantTicket = 0; waiting = true; goWhenReady(60, -1, false); }
    if (!el || !("IntersectionObserver" in window)) return;
    new IntersectionObserver(function (es) {
      es.forEach(function (e) { formOn = e.isIntersecting; });
      paint();
    }, { rootMargin: "0px 0px -40px 0px" }).observe(el);
  };
  var startBar = function () {
    bar = document.getElementById("drBar");
    var hc = document.getElementById("heroCta");
    if (!bar || !hc || !("IntersectionObserver" in window)) return;
    new IntersectionObserver(function (es) {
      es.forEach(function (e) { heroGone = !e.isIntersecting && e.boundingClientRect.bottom <= 1; });
      paint();
    }).observe(hc);
  };
  /* le menu : construit dès que la page est lue, sans attendre la 3D (le script principal relance ce module plus tard : sans effet, le menu existe déjà) */
  var navEarly = function () {
    try {
      var t = document.querySelector('script[type="text/x-fold"][data-src="sections/nav.js"]');
      if (!t || document.querySelector(".navx")) return;
      var s = document.createElement("script");
      s.textContent = t.textContent;
      document.head.appendChild(s);
    } catch (e) { /* le script principal le construira */ }
  };
  var ready = function () { startBar(); navEarly(); };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", ready); else ready();

  /* sans WebGL : les sections du bas, la FAQ, le ticket et le pied de page, sans la 3D */
  DR.noGL = function () {
    DR.flat = true;
    d.classList.add("dr-flat");
    try {
      var S = window.SECTIONS, hero = document.querySelector("main > .hero");
      if (!S || !hero || document.getElementById("landing")) return;
      var M = document.createElement("div");
      M.className = "landing";
      M.id = "landing";
      hero.after(M);
      var stops = S.build(M);
      var owners = [window.WHEN_STOP, window.FAQ_MAP, window.BOOK_STOP];
      stops.forEach(function (el) {
        var o = { el: el, pinStart: 0, flow: true };
        owners.forEach(function (w) {
          if (w && w.owns(el) && w.frame) { try { w.frame(o, window.scrollY, window.innerHeight); } catch (e) { console.warn(e); } }
        });
      });
    } catch (e) { console.warn(e); }
  };
})();
