/* ============================================================================
 * Nila Dhamma · progressive enhancement
 * Everything below is optional: every page reads correctly with JS disabled.
 * Motion stays functional (Canopy): no entrance choreography, no parallax.
 * ==========================================================================*/
(function () {
  'use strict';

  /* ---- Image fallback ----
     Event photos are still served from the original Blogger CDN; some older
     posts no longer resolve. Swap a broken one for a local plate rather than
     leaving an empty grey panel. */
  var FALLBACK = 'assets/img/lion-capital-sarnath.jpg';
  Array.prototype.forEach.call(document.images, function (img) {
    if (img.getAttribute('src') === FALLBACK) return;
    img.addEventListener('error', function once() {
      img.removeEventListener('error', once);
      img.src = FALLBACK;
      img.style.objectFit = 'cover';
      img.style.opacity = '0.9';
    });
    if (img.complete && img.naturalWidth === 0) {
      img.src = FALLBACK;
    }
  });

  /* ---- Mobile navigation ---- */
  var toggle = document.querySelector('[data-navtoggle]');
  var nav = document.getElementById('nd-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.getAttribute('data-open') === 'true';
      nav.setAttribute('data-open', String(!open));
      toggle.setAttribute('aria-expanded', String(!open));
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.getAttribute('data-open') === 'true') {
        nav.setAttribute('data-open', 'false');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  /* ---- Writings: year filter + title search ---- */
  var list = document.querySelector('[data-list]');
  if (list) {
    var cards = Array.prototype.slice.call(list.children);
    // scope to the filter bar: the cards themselves also carry data-year
    var chips = Array.prototype.slice.call(document.querySelectorAll('[data-filters] [data-year]'));
    var search = document.querySelector('[data-search]');
    var empty = document.querySelector('[data-empty]');
    var year = 'all';
    // Topics exist only once member posts carry tags; the row is absent before.
    var topics = Array.prototype.slice.call(document.querySelectorAll('[data-tagfilters] [data-tag]'));
    var topic = '';

    function apply() {
      var q = (search && search.value || '').trim().toLowerCase();
      var shown = 0;
      cards.forEach(function (card) {
        var okYear = year === 'all' || card.getAttribute('data-year') === year;
        var okText = !q || card.getAttribute('data-title').indexOf(q) !== -1;
        var okTopic = !topic ||
          (card.getAttribute('data-tags') || '').indexOf('|' + topic + '|') !== -1;
        var show = okYear && okText && okTopic;
        card.classList.toggle('nd-hidden', !show);
        if (show) shown++;
      });
      if (empty) empty.classList.toggle('nd-hidden', shown !== 0);
    }

    topics.forEach(function (chip) {
      chip.addEventListener('click', function () {
        // a second press on the chosen topic clears it
        topic = topic === chip.getAttribute('data-tag') ? '' : chip.getAttribute('data-tag');
        topics.forEach(function (c) {
          c.setAttribute('aria-pressed', String(c.getAttribute('data-tag') === topic));
        });
        apply();
      });
    });

    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        year = chip.getAttribute('data-year');
        chips.forEach(function (c) {
          c.setAttribute('aria-pressed', String(c === chip));
        });
        apply();
      });
    });
    if (search) search.addEventListener('input', apply);
  }

  /* ---- Tabs ----
     Panels are real content, present in the HTML and indexable; only their
     visibility is switched. Without JS a <noscript> rule shows them all. */
  Array.prototype.forEach.call(document.querySelectorAll('[data-tabs]'), function (wrap) {
    var tabs = Array.prototype.slice.call(wrap.querySelectorAll('[role="tab"]'));
    function select(tab) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      });
    }
    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () { select(tab); });
      tab.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        var next = tabs[(i + d + tabs.length) % tabs.length];
        select(next);
        next.focus();
      });
    });
  });

  /* ---- Long lists: show the first few, reveal the rest on request ---- */
  Array.prototype.forEach.call(document.querySelectorAll('[data-more]'), function (list) {
    var keep = parseInt(list.getAttribute('data-more'), 10);
    var body = list.tagName === 'TABLE' ? list.tBodies[0] : list;
    var items = Array.prototype.slice.call(body.children);
    if (items.length <= keep + 2) return;
    var hidden = items.slice(keep);
    hidden.forEach(function (el) { el.classList.add('nd-more'); });

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'nd-morebtn';
    var more = list.getAttribute('data-more-label') || document.documentElement.lang === 'ta'
      ? 'மேலும் ' + hidden.length + ' காட்டு' : 'Show ' + hidden.length + ' more';
    var less = document.documentElement.lang === 'ta' ? 'சுருக்கு' : 'Show less';
    btn.textContent = more;
    btn.setAttribute('aria-expanded', 'false');
    (list.tagName === 'TABLE' ? list.parentNode : list).after(btn);

    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      hidden.forEach(function (el) { el.classList.toggle('nd-more', open); });
      btn.setAttribute('aria-expanded', String(!open));
      btn.textContent = open ? more : less;
      if (open) btn.scrollIntoView({ block: 'nearest' });
    });
  });

  /* ---- Calendar: highlight and summarise the next full moon ----
     Computed from the table already in the page, so it stays correct as days
     pass without a rebuild. */
  var moonRows = Array.prototype.slice.call(document.querySelectorAll('[data-moon]'));
  if (moonRows.length) {
    var today = new Date();
    today.setHours(0, 0, 0, 0);
    var next = null;
    moonRows.forEach(function (row) {
      var parts = row.getAttribute('data-moon').split('-');
      var d = new Date(+parts[0], +parts[1] - 1, +parts[2]);
      if (!next && d >= today) { next = { row: row, date: d }; }
    });
    if (next) {
      next.row.classList.add('is-next');
      var box = document.querySelector('[data-nextmoon]');
      if (box) {
        var days = Math.round((next.date - today) / 864e5);
        var when = days === 0 ? 'இன்று' : days === 1 ? 'நாளை' : 'இன்னும் ' + days + ' நாட்களில்';
        box.hidden = false;
        box.querySelector('[data-nextmoon-date]').textContent =
          next.row.children[0].textContent.trim();
        box.querySelector('[data-nextmoon-meta]').textContent =
          when + ' · மாலை 6 மணி முதல் · அசோக் நகர் புத்த விஹார், சென்னை';
      }
    }
  }

  /* ---- Dhamma stories: title search ---- */
  var klist = document.querySelector('[data-klist]');
  var ksearch = document.querySelector('[data-ksearch]');
  if (klist && ksearch) {
    var kcards = Array.prototype.slice.call(klist.children);
    var kempty = document.querySelector('[data-kempty]');
    ksearch.addEventListener('input', function () {
      var q = ksearch.value.trim().toLowerCase();
      var shown = 0;
      kcards.forEach(function (card) {
        var show = !q || card.getAttribute('data-title').indexOf(q) !== -1;
        card.classList.toggle('nd-hidden', !show);
        if (show) shown++;
      });
      if (kempty) kempty.classList.toggle('nd-hidden', shown !== 0);
    });
  }

  /* ---- Names: panel switch + search ---- */
  var tabs = Array.prototype.slice.call(document.querySelectorAll('[data-tab]'));
  if (tabs.length) {
    var panels = Array.prototype.slice.call(document.querySelectorAll('[data-panel]'));
    var nsearch = document.querySelector('[data-namesearch]');
    var nempty = document.querySelector('[data-nempty]');
    var active = 'boys';

    function applyNames() {
      var q = (nsearch && nsearch.value || '').trim().toLowerCase();
      var shown = 0;
      panels.forEach(function (panel) {
        var on = panel.getAttribute('data-panel') === active;
        panel.classList.toggle('nd-hidden', !on);
        if (!on) return;
        Array.prototype.forEach.call(panel.querySelectorAll('li'), function (li) {
          var show = !q || li.textContent.toLowerCase().indexOf(q) !== -1;
          li.classList.toggle('nd-hidden', !show);
          if (show) shown++;
        });
      });
      if (nempty) nempty.classList.toggle('nd-hidden', shown !== 0);
    }

    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        active = tab.getAttribute('data-tab');
        tabs.forEach(function (t) {
          t.setAttribute('aria-pressed', String(t === tab));
        });
        applyNames();
      });
    });
    if (nsearch) nsearch.addEventListener('input', applyNames);
  }

  /* ---- Copy link ----
     Rendered hidden so a browser without the clipboard API never shows a
     button that cannot do anything. */
  var copy = document.querySelector('[data-copy]');
  if (copy && navigator.clipboard) {
    var label = copy.querySelector('span');
    var said = label && label.textContent;
    copy.hidden = false;
    function confirmCopy() {
      copy.setAttribute('data-state', 'done');
      if (label) label.textContent = copy.getAttribute('data-done');
      setTimeout(function () {
        copy.removeAttribute('data-state');
        if (label) label.textContent = said;
      }, 2400);
    }

    copy.addEventListener('click', function () {
      navigator.clipboard.writeText(location.href).then(confirmCopy, function () {
        /* Permission refused. The older path still works in that case, and it
           says nothing at all rather than reporting a copy that never
           happened. */
        var t = document.createElement('textarea');
        t.value = location.href;
        t.setAttribute('readonly', '');
        t.style.cssText = 'position:fixed;top:0;left:-9999px';
        document.body.appendChild(t);
        t.select();
        try { if (document.execCommand('copy')) confirmCopy(); } catch (e) {}
        t.remove();
      });
    });
  }

  /* ---- Photograph viewer ----
     Every photograph in an archive post is already a link to the full file,
     so this only intercepts the click. With scripting off the link still
     opens the picture, which is why nothing here is required. */
  var shots = Array.prototype.slice.call(document.querySelectorAll('[data-shot]'));
  if (shots.length) {
    var view = null, at = 0, cameFrom = null;

    function build() {
      view = document.createElement('div');
      view.className = 'nd-viewer';
      view.setAttribute('role', 'dialog');
      view.setAttribute('aria-modal', 'true');
      view.setAttribute('data-open', 'false');
      view.innerHTML =
        '<div class="nd-viewer__bar">' +
          '<span data-count></span>' +
          '<span class="nd-viewer__nav">' +
            '<button class="nd-viewer__btn" type="button" data-prev>&#8592;</button>' +
            '<button class="nd-viewer__btn" type="button" data-next>&#8594;</button>' +
            '<button class="nd-viewer__btn" type="button" data-close>&#215;</button>' +
          '</span>' +
        '</div>' +
        '<div class="nd-viewer__stage"><img alt=""></div>' +
        '<p class="nd-viewer__cap" data-vcap></p>';
      document.body.appendChild(view);

      view.querySelector('[data-close]').addEventListener('click', close);
      view.querySelector('[data-prev]').addEventListener('click', function () { go(at - 1); });
      view.querySelector('[data-next]').addEventListener('click', function () { go(at + 1); });
      view.addEventListener('click', function (e) {
        if (e.target === view || e.target.className === 'nd-viewer__stage') close();
      });
    }

    function go(i) {
      if (i < 0 || i >= shots.length) return;
      at = i;
      var a = shots[i];
      var img = view.querySelector('img');
      img.src = a.getAttribute('href');
      img.alt = a.getAttribute('data-cap') || '';
      view.querySelector('[data-vcap]').textContent = a.getAttribute('data-cap') || '';
      view.querySelector('[data-count]').textContent = a.getAttribute('aria-label') || '';
      view.setAttribute('aria-label', a.getAttribute('aria-label') || '');
      view.querySelector('[data-prev]').disabled = i === 0;
      view.querySelector('[data-next]').disabled = i === shots.length - 1;
    }

    function open(i) {
      if (!view) build();
      cameFrom = document.activeElement;
      go(i);
      view.setAttribute('data-open', 'true');
      document.body.setAttribute('data-viewer', 'open');
      view.querySelector('[data-close]').focus();
    }

    function close() {
      if (!view) return;
      view.setAttribute('data-open', 'false');
      document.body.removeAttribute('data-viewer');
      if (cameFrom && cameFrom.focus) cameFrom.focus();
    }

    shots.forEach(function (a, i) {
      a.addEventListener('click', function (e) {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
        e.preventDefault();
        open(i);
      });
    });

    document.addEventListener('keydown', function (e) {
      if (!view || view.getAttribute('data-open') !== 'true') return;
      if (e.key === 'Escape') { close(); }
      else if (e.key === 'ArrowLeft') { go(at - 1); }
      else if (e.key === 'ArrowRight') { go(at + 1); }
      else if (e.key === 'Tab') {
        /* The viewer covers the page, so focus stays inside it. */
        var keys = Array.prototype.slice.call(
          view.querySelectorAll('button:not([disabled])'));
        var first = keys[0], last = keys[keys.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
  }
})();
