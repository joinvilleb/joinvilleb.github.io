// Menu drawer and scroll reveal. Nothing here is required to read the
// page: the .js class that hides revealed content is set in the head, so
// with scripting off everything renders as plain static markup.
(function () {
  'use strict';

  var burger = document.getElementById('burger');
  var drawer = document.getElementById('drawer');

  if (burger && drawer) {
    setDrawer(false);

    burger.addEventListener('click', function () {
      setDrawer(!drawer.classList.contains('open'));
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('open')) {
        setDrawer(false);
        burger.focus();
      }
    });

    // A tap anywhere else closes it, which is what people expect on a phone.
    document.addEventListener('click', function (e) {
      if (!drawer.classList.contains('open')) return;
      if (drawer.contains(e.target) || burger.contains(e.target)) return;
      setDrawer(false);
    });
  }

  function setDrawer(open) {
    drawer.classList.toggle('open', open);
    burger.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    if (open) drawer.querySelector('a').focus();
  }

  var revealed = document.querySelectorAll('.reveal');

  if (!('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(revealed, function (el) { el.classList.add('in'); });
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('in');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

  Array.prototype.forEach.call(revealed, function (el) { observer.observe(el); });
})();
