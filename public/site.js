/* KKTeX Portfolio — behaviour for the static page.
 *
 * Four things, matching the design handoff: the language toggle, the scroll
 * progress bar, the source-block typewriter, and the scroll-driven reveals.
 *
 * Reveal rule (the one bug the handoff calls out): an element is only ever
 * hidden by a class/inline style that THIS script put there, and only after
 * checking it is both laid out and off-screen. Anything the script has not
 * touched — no-JS, reduced motion, or the inactive language — stays visible. */
(function () {
  'use strict';

  var root = document.documentElement;
  var reduce = window.matchMedia &&
               window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function each(sel, fn) {
    Array.prototype.forEach.call(document.querySelectorAll(sel), fn);
  }

  /* ── language ──────────────────────────────────────────────────────────── */

  var STORE = 'kktex-lang';
  var toggle = document.getElementById('langToggle');

  function applyLang(lang) {
    root.lang = lang;
    if (toggle) toggle.textContent = lang === 'ja' ? 'EN' : 'JA';
    scan(); // the switch may have brought elements into layout for the first time
  }

  var saved = null;
  try { saved = localStorage.getItem(STORE); } catch (e) { /* private mode */ }
  applyLang(saved === 'en' || saved === 'ja' ? saved : 'ja');

  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = root.lang === 'ja' ? 'en' : 'ja';
      applyLang(next);
      try { localStorage.setItem(STORE, next); } catch (e) { /* private mode */ }
    });
  }

  /* ── scroll progress bar ───────────────────────────────────────────────── */

  var bar = document.getElementById('bar');

  function onScroll() {
    if (!bar) return;
    var max = root.scrollHeight - root.clientHeight;
    var y = window.scrollY || root.scrollTop || 0;
    bar.style.width = (max > 0 ? Math.min(100, (y / max) * 100) : 0) + '%';
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  /* ── typewriter ────────────────────────────────────────────────────────── */

  /* The full source is in the HTML, so it is there without JS and under
     reduced motion; we clear it only to type it back in. */
  var typed = document.getElementById('typed');
  if (typed && !reduce) {
    var src = typed.textContent;
    var i = 0;
    typed.textContent = '';
    var timer = setInterval(function () {
      i += 1;
      typed.textContent = src.slice(0, i);
      if (i >= src.length) clearInterval(timer);
    }, 26);
  }

  /* ── reveals ───────────────────────────────────────────────────────────── */

  var maskIo = null, revealIo = null;

  /* false while an element is display:none — i.e. the inactive language */
  function laidOut(el) { return el.getClientRects().length > 0; }

  function onScreen(el, vh) {
    var r = el.getBoundingClientRect();
    return r.top < vh && r.bottom > 0;
  }

  function reveal(el, delay) {
    el.dataset.rv = 'in';
    el.style.transitionDelay = delay + 'ms';
    el.style.opacity = '1';
    el.style.transform = 'none';
  }

  /* Idempotent: every run reveals whatever is on screen right now — armed or
     not — and arms whatever is still below the fold. Safe to call again after
     any layout change (language switch, fonts, images). */
  function scan() {
    if (reduce || !('IntersectionObserver' in window)) return;
    var vh = window.innerHeight || root.clientHeight;

    if (!maskIo) {
      maskIo = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          e.target.classList.add('is-in');
          maskIo.unobserve(e.target);
        });
      }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
    }
    if (!revealIo) {
      revealIo = new IntersectionObserver(function (entries) {
        entries.forEach(function (e, k) {
          if (!e.isIntersecting) return;
          reveal(e.target, k * 60);
          revealIo.unobserve(e.target);
        });
      }, { rootMargin: '0px 0px -12% 0px', threshold: 0.05 });
    }

    /* masked headings, hairline rules, section entrances, vermilion bands */
    each('[data-mask="view"],[data-rule],[data-enter],[data-band]', function (n) {
      if (n.classList.contains('is-in') || !laidOut(n)) return;
      if (onScreen(n, vh)) {
        n.classList.remove('armed');
        n.classList.add('is-in');
        maskIo.unobserve(n);
        return;
      }
      if (n.classList.contains('armed')) return;
      n.classList.add('armed');
      maskIo.observe(n);
    });

    /* staggered element reveals */
    each('[data-reveal]', function (n) {
      if (n.dataset.rv === 'in' || !laidOut(n)) return;
      if (onScreen(n, vh)) {
        if (n.dataset.rv === 'armed') { revealIo.unobserve(n); reveal(n, 0); }
        else n.dataset.rv = 'in';
        return;
      }
      if (n.dataset.rv === 'armed') return;
      n.dataset.rv = 'armed';
      n.style.opacity = '0';
      n.style.transform = 'translateY(22px)';
      n.style.transition = 'opacity .9s var(--ease-expo), transform .9s var(--ease-expo)';
      revealIo.observe(n);
    });
  }

  /* Web fonts and images settle after the first scan and move things around;
     re-run so nothing is left armed inside the reader's view. */
  window.addEventListener('load', scan);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(scan);
}());
