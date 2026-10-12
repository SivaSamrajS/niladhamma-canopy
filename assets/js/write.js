/* ============================================================================
 * Niladhamma · the writers' desk
 *
 * Sign in, write, publish. The page is static; this script talks to
 * /api/write/* (netlify/functions), which commits the post to the repository.
 * Every string shown comes from the page, so this file carries no copy.
 *
 * What is sent on publish is a list of blocks, not HTML:
 *   ["p", inline]  ["h2", text]  ["h3", text]  ["quote", inline]
 *   ["ul", [inline]]  ["ol", [inline]]  ["fig", src, caption]  ["video", id]
 * The server reduces them again, so nothing here is relied on for safety.
 * ==========================================================================*/
(function () {
  'use strict';

  var root = document.querySelector('[data-write]');
  var blob = document.getElementById('nd-write-strings');
  if (!root || !blob) return;
  var T = JSON.parse(blob.textContent);
  function $(sel) { return root.querySelector(sel); }

  var TOKEN = 'nd-write-token', DRAFT = 'nd-write-draft', AUTHOR = 'nd-write-author';
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); return true; } catch (e) { return false; } },
    del: function (k) { try { localStorage.removeItem(k); } catch (e) {} }
  };

  var loginForm = $('[data-login]'), desk = $('[data-desk]'), form = $('[data-editor]');
  var body = $('[data-body]'), status = $('[data-status]'), list = $('[data-posts]');
  var publishBtn = $('[data-publish]'), cancelBtn = $('[data-cancel]');
  var f = form.elements;

  var token = store.get(TOKEN);
  var uploads = {};      // src -> { blobs, width, height, preview } for photographs not yet published
  var editing = null;    // slug of the post being edited
  var busy = 0;          // photographs still uploading
  var anchor = null;     // the block the cursor was last in
  var range = null;      // the last selection inside the body

  /* ---- Status line: colour, icon and a sentence, never colour alone ---- */
  function say(kind, text, link) {
    status.className = 'cm-alert nd-write__status cm-alert--' + kind;
    status.innerHTML = (kind === 'success' ? T.icon_ok : T.icon_info) + '<span></span>';
    status.lastChild.textContent = text;
    if (link) {
      var a = document.createElement('a');
      a.href = link.href;
      a.textContent = link.text;
      status.lastChild.appendChild(document.createTextNode(' '));
      status.lastChild.appendChild(a);
    }
    status.hidden = false;
    return status;
  }
  function fail(e) {
    var code = e && e.code || 'server';
    say('danger', T['e_' + code] || T.e_server).scrollIntoView({ block: 'nearest' });
  }
  function hush() { status.hidden = true; }

  /* ---- Server ---- */
  function api(method, path, payload) {
    var headers = {};
    if (payload) headers['content-type'] = 'application/json';
    if (token) headers.authorization = 'Bearer ' + token;
    return fetch('/api/write/' + path, {
      method: method, headers: headers, cache: 'no-store',
      body: payload ? JSON.stringify(payload) : undefined
    }).then(function (res) {
      return res.json().catch(function () { return null; }).then(function (data) {
        if (res.ok && data) return data;
        var code = data && data.error ||
          (res.status === 429 ? 'too_many' : res.status === 404 ? 'not_configured' : 'server');
        if (code === 'signed_out') { saveDraft(); signOut(); }
        throw { code: code };
      });
    }, function () { throw { code: 'network' }; });
  }

  /* ---- Sign in and out ---- */
  function signOut() {
    token = null;
    store.del(TOKEN);
    desk.hidden = true;
    loginForm.hidden = false;
  }

  loginForm.addEventListener('submit', function (e) {
    e.preventDefault();
    var btn = loginForm.querySelector('[type="submit"]');
    btn.disabled = true;
    hush();
    api('POST', 'login', {
      username: loginForm.elements.username.value,
      password: loginForm.elements.password.value
    }).then(function (data) {
      token = data.token;
      store.set(TOKEN, token);
      loginForm.elements.password.value = '';
      openDesk();
    }, fail).then(function () { btn.disabled = false; });
  });

  $('[data-signout]').addEventListener('click', function () {
    saveDraft();
    hush();
    signOut();
  });

  /* ---- Text helpers ---- */
  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
  function today() {
    // Asia/Kolkata, the day the build reckons by.
    return new Date(Date.now() + 5.5 * 36e5).toISOString().slice(0, 10);
  }
  function youtubeId(s) {
    var m = /(?:youtu\.be\/|youtube(?:-nocookie)?\.com\/(?:watch\?(?:[^#\s]*&)?v=|embed\/|shorts\/|live\/))([A-Za-z0-9_-]{11})(?![A-Za-z0-9_-])/.exec(s);
    return m ? m[1] : '';
  }

  /* ---- The body: DOM to blocks ---- */
  var BLOCK = { P: 1, DIV: 1, H1: 1, H2: 1, H3: 1, H4: 1, H5: 1, H6: 1, BLOCKQUOTE: 1,
    UL: 1, OL: 1, LI: 1, FIGURE: 1, SECTION: 1, ARTICLE: 1 };
  var WRAP = { B: 'b', STRONG: 'b', I: 'i', EM: 'i', U: 'u' };

  function inlineOf(node) {
    var out = '';
    Array.prototype.forEach.call(node.childNodes, function (n) {
      if (n.nodeType === 3) { out += esc(n.nodeValue); return; }
      if (n.nodeType !== 1) return;
      var t = n.tagName;
      if (t === 'BR') out += '<br>';
      else if (WRAP[t]) out += '<' + WRAP[t] + '>' + inlineOf(n) + '</' + WRAP[t] + '>';
      else if (t === 'A' && n.getAttribute('href')) {
        out += '<a href="' + esc(n.getAttribute('href')) + '">' + inlineOf(n) + '</a>';
      } else if (BLOCK[t]) {
        // a block nested where only a line can go: keep its words on a new line
        out += (out && !/<br>$/.test(out) ? '<br>' : '') + inlineOf(n);
      } else out += inlineOf(n);
    });
    return out;
  }
  function blank(html) {
    return !html.replace(/<[^>]+>/g, '').replace(/&nbsp;|\s/g, '');
  }
  function hasBlock(node) {
    return Array.prototype.some.call(node.children, function (c) { return BLOCK[c.tagName]; });
  }

  function blocksOf(parent, out) {
    var run = '';
    function flush() { if (!blank(run)) out.push(['p', run]); run = ''; }
    Array.prototype.forEach.call(parent.childNodes, function (n) {
      if (n.nodeType === 3) { run += esc(n.nodeValue); return; }
      if (n.nodeType !== 1) return;
      var t = n.tagName, html;
      if (n.hasAttribute('data-fig')) {
        flush();
        if (n.getAttribute('data-src')) {
          out.push(['fig', n.getAttribute('data-src'), esc(n.querySelector('[data-cap]').value.trim())]);
        }
      } else if (n.hasAttribute('data-video')) {
        flush();
        out.push(['video', n.getAttribute('data-video')]);
      } else if (/^H[1-6]$/.test(t)) {
        flush();
        html = inlineOf(n);
        if (!blank(html)) out.push([t === 'H1' || t === 'H2' ? 'h2' : 'h3', html]);
      } else if (t === 'UL' || t === 'OL') {
        flush();
        var items = Array.prototype.map.call(n.children, inlineOf)
          .filter(function (x) { return !blank(x); });
        if (items.length) out.push([t.toLowerCase(), items]);
      } else if (t === 'BLOCKQUOTE') {
        flush();
        html = inlineOf(n);
        if (!blank(html)) out.push(['quote', html]);
      } else if (BLOCK[t]) {
        flush();
        if (hasBlock(n)) blocksOf(n, out);
        else { html = inlineOf(n); if (!blank(html)) out.push(['p', html]); }
      } else if (t === 'BR') {
        if (/<br>$/.test(run)) flush(); else if (run) run += '<br>';
      } else {
        var wrap = document.createElement('span');
        wrap.appendChild(n.cloneNode(true));
        run += inlineOf(wrap);
      }
    });
    flush();
    return out;
  }
  function readBody() { return blocksOf(body, []); }

  /* ---- The body: blocks to DOM ---- */
  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html) n.innerHTML = html;
    return n;
  }
  function emptyPara() { return el('p', '', '<br>'); }

  function figure(src, caption, preview) {
    var fig = el('figure', 'nd-write__fig');
    fig.contentEditable = 'false';
    fig.setAttribute('data-fig', '');
    if (src) fig.setAttribute('data-src', src);
    var img = el('img');
    img.alt = '';
    if (preview) img.src = preview; else fig.classList.add('nd-write__fig--blank');
    var cap = el('input', 'cm-input');
    cap.type = 'text';
    cap.maxLength = 300;
    cap.placeholder = T.caption;
    cap.setAttribute('aria-label', T.caption);
    cap.setAttribute('data-cap', '');
    cap.value = caption || '';
    var x = el('button', 'nd-write__x');
    x.type = 'button';
    x.textContent = T.remove;
    x.setAttribute('data-remove', '');
    var note = el('span', 'nd-write__busy');
    note.textContent = T.s_uploading;
    fig.appendChild(img); fig.appendChild(note); fig.appendChild(cap); fig.appendChild(x);
    return fig;
  }

  function video(id) {
    var box = el('div', 'nd-write__video');
    box.contentEditable = 'false';
    box.setAttribute('data-video', id);
    var img = el('img');
    img.alt = '';
    img.src = 'https://i.ytimg.com/vi/' + id + '/mqdefault.jpg';
    var label = el('span');
    label.textContent = 'YouTube · ' + id;
    var x = el('button', 'nd-write__x');
    x.type = 'button';
    x.textContent = T.remove;
    x.setAttribute('data-remove', '');
    box.appendChild(img); box.appendChild(label); box.appendChild(x);
    return box;
  }

  function preview(src) {
    if (uploads[src]) return uploads[src].preview || '';
    return src.replace('/pathivu/', '/pathivu/tile/');
  }

  function writeBody(blocks) {
    body.innerHTML = '';
    (blocks || []).forEach(function (b) {
      var k = b[0];
      if (k === 'p') body.appendChild(el('p', '', b[1]));
      else if (k === 'h2' || k === 'h3') body.appendChild(el(k, '', b[1]));
      else if (k === 'quote') body.appendChild(el('blockquote', '', b[1]));
      else if (k === 'ul' || k === 'ol') {
        var l = el(k);
        b[1].forEach(function (x) { l.appendChild(el('li', '', x)); });
        body.appendChild(l);
      } else if (k === 'fig') {
        var cap = el('span', '', b[2] || '').textContent;
        body.appendChild(figure(b[1], cap, preview(b[1])));
      } else if (k === 'video') body.appendChild(video(b[1]));
    });
    tail();
    anchor = null;
  }
  /* A photograph or a video cannot be typed after, so the body always ends in
     a paragraph the cursor can reach. */
  function tail() {
    var last = body.lastElementChild;
    if (!last || last.tagName !== 'P') body.appendChild(emptyPara());
  }

  function place(node) {
    if (anchor && anchor.parentNode === body) body.insertBefore(node, anchor.nextSibling);
    else body.appendChild(node);
    anchor = node;
    tail();
    changed();
  }

  /* ---- Selection ---- */
  document.addEventListener('selectionchange', function () {
    var sel = document.getSelection();
    if (!sel.rangeCount) return;
    var r = sel.getRangeAt(0), n = r.endContainer;
    if (!body.contains(n) || n === body) return;
    range = r.cloneRange();
    while (n && n.parentNode !== body) n = n.parentNode;
    anchor = n;
  });
  function reselect() {
    body.focus();
    if (!range) return false;
    var sel = document.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
    return true;
  }
  function currentBlock() {
    return anchor && anchor.nodeType === 1 ? anchor.tagName : '';
  }

  /* ---- Toolbar ---- */
  try {
    document.execCommand('defaultParagraphSeparator', false, 'p');
    document.execCommand('styleWithCSS', false, false);
  } catch (e) {}

  var linkRow = $('[data-linkrow]'), linkUrl = $('[data-linkurl]');
  var FORMAT = { p: 'P', h2: 'H2', h3: 'H3', quote: 'BLOCKQUOTE' };

  function command(cmd) {
    if (cmd === 'link') {
      if (!range || range.collapsed) { say('info', T.link_pick); return; }
      linkRow.hidden = false;
      linkUrl.focus();
      return;
    }
    reselect();
    if (FORMAT[cmd]) {
      // pressing the same style again returns the block to a paragraph
      var to = currentBlock() === FORMAT[cmd] ? 'P' : FORMAT[cmd];
      document.execCommand('formatBlock', false, '<' + to + '>');
    } else if (cmd === 'ul') document.execCommand('insertUnorderedList');
    else if (cmd === 'ol') document.execCommand('insertOrderedList');
    else document.execCommand(cmd);
    changed();
  }
  Array.prototype.forEach.call(root.querySelectorAll('[data-cmd]'), function (btn) {
    // mousedown would move focus out of the body and drop the selection
    btn.addEventListener('mousedown', function (e) { e.preventDefault(); });
    btn.addEventListener('click', function () { command(btn.getAttribute('data-cmd')); });
  });

  function addLink() {
    var url = linkUrl.value.trim();
    if (url && !/^(https?:\/\/|mailto:)/i.test(url)) url = 'https://' + url;
    linkRow.hidden = true;
    linkUrl.value = '';
    if (!url || !reselect()) return;
    document.execCommand('createLink', false, url);
    hush();
    changed();
  }
  $('[data-linkadd]').addEventListener('click', addLink);
  linkUrl.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') { e.preventDefault(); addLink(); }
    if (e.key === 'Escape') { linkRow.hidden = true; reselect(); }
  });

  /* Pasted text arrives as words only. What a word processor puts on the
     clipboard is markup the page has no use for. */
  body.addEventListener('paste', function (e) {
    var text = (e.clipboardData || window.clipboardData).getData('text');
    if (text == null) return;
    e.preventDefault();
    document.execCommand('insertText', false, text);
  });
  body.addEventListener('click', function (e) {
    var x = e.target.closest && e.target.closest('[data-remove]');
    if (!x) return;
    var block = x.parentNode;
    if (anchor === block) anchor = block.previousSibling;
    block.remove();
    tail();
    changed();
  });
  // a link in the body is text being edited, not somewhere to go
  body.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('a')) e.preventDefault();
  });

  /* ---- Photographs ----
     Reduced in the browser before they are sent: a phone photograph is several
     megabytes and the site shows it at 1800px at most. Three sizes go up, the
     same three the archive keeps: the picture, a 720px display copy and a
     480 by 360 card thumbnail. */
  function decodeImage(file) {
    if (window.createImageBitmap) {
      return createImageBitmap(file, { imageOrientation: 'from-image' })
        .catch(function () { return viaElement(file); });
    }
    return viaElement(file);
  }
  function viaElement(file) {
    return new Promise(function (resolve, reject) {
      var url = URL.createObjectURL(file), img = new Image();
      img.onload = function () { URL.revokeObjectURL(url); resolve(img); };
      img.onerror = function () { URL.revokeObjectURL(url); reject({ code: 'bad_image' }); };
      img.src = url;
    });
  }
  function draw(img, w, h, crop, quality) {
    var c = document.createElement('canvas');
    c.width = w; c.height = h;
    var ctx = c.getContext('2d');
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, w, h);
    ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(img, crop[0], crop[1], crop[2], crop[3], 0, 0, w, h);
    return c.toDataURL('image/jpeg', quality);
  }
  function sizes(img) {
    var W = img.width, H = img.height;
    if (!W || !H) throw { code: 'bad_image' };
    var whole = [0, 0, W, H];
    var k = Math.min(1, 1800 / Math.max(W, H));
    var fw = Math.max(1, Math.round(W * k)), fh = Math.max(1, Math.round(H * k));
    var full = draw(img, fw, fh, whole, 0.84);
    if (full.length > 3.4e6) full = draw(img, fw, fh, whole, 0.68);
    var tk = Math.min(1, 720 / W);
    var tile = draw(img, Math.max(1, Math.round(W * tk)), Math.max(1, Math.round(H * tk)), whole, 0.76);
    // the card thumbnail is a centred 4:3 crop
    var cw = Math.min(W, H * 4 / 3), ch = cw * 3 / 4;
    var thumb = draw(img, 480, 360, [(W - cw) / 2, (H - ch) / 2, cw, ch], 0.72);
    return { full: full, tile: tile, thumb: thumb };
  }
  function b64(dataUrl) { return dataUrl.slice(dataUrl.indexOf(',') + 1); }

  function setBusy(n) {
    busy += n;
    publishBtn.disabled = busy > 0;
  }

  function addPhoto(file) {
    setBusy(1);
    var fig = null;
    return decodeImage(file).then(function (img) {
      var s = sizes(img);
      if (img.close) img.close();
      fig = figure('', '', s.thumb);
      fig.setAttribute('data-state', 'busy');
      place(fig);
      return api('POST', 'image', { full: b64(s.full), tile: b64(s.tile), thumb: b64(s.thumb) })
        .then(function (up) {
          uploads[up.src] = { blobs: up.blobs, width: up.width, height: up.height, preview: s.thumb };
          fig.setAttribute('data-src', up.src);
          fig.removeAttribute('data-state');
          changed();
        });
    }).catch(function (e) {
      if (fig) { if (anchor === fig) anchor = fig.previousSibling; fig.remove(); }
      fail(e && e.code ? e : { code: 'bad_image' });
    }).then(function () { setBusy(-1); });
  }

  $('[data-photos]').addEventListener('change', function (e) {
    var files = Array.prototype.slice.call(e.target.files || []);
    e.target.value = '';
    hush();
    // one at a time, so the photographs land in the order they were picked
    files.reduce(function (chain, file) {
      return chain.then(function () { return addPhoto(file); });
    }, Promise.resolve());
  });

  /* ---- Video ---- */
  var videoUrl = $('[data-videourl]');
  function addVideo() {
    var id = youtubeId(videoUrl.value.trim());
    if (!id) { fail({ code: 'bad_video' }); return; }
    hush();
    videoUrl.value = '';
    place(video(id));
  }
  $('[data-videoadd]').addEventListener('click', addVideo);
  videoUrl.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') { e.preventDefault(); addVideo(); }
  });

  /* ---- Draft ----
     Kept in this browser as the writer types, so a dropped connection, a
     closed tab or an expired sign-in does not cost them the post. */
  var timer = null;
  function snapshot() {
    var blocks = readBody(), used = {};
    blocks.forEach(function (b) { if (b[0] === 'fig' && uploads[b[1]]) used[b[1]] = uploads[b[1]]; });
    return {
      slug: editing, title: f.title.value, subtitle: f.subtitle.value, author: f.author.value,
      date: f.date.value, tags: f.tags.value, blocks: blocks, uploads: used
    };
  }
  function saveDraft() {
    clearTimeout(timer);
    var d = snapshot();
    if (!d.title.trim() && !d.blocks.length) { store.del(DRAFT); return; }
    if (store.set(DRAFT, JSON.stringify(d))) return;
    // over the browser's quota: keep the words and drop the picture previews
    Object.keys(d.uploads).forEach(function (k) {
      var u = d.uploads[k];
      d.uploads[k] = { blobs: u.blobs, width: u.width, height: u.height };
    });
    store.set(DRAFT, JSON.stringify(d));
  }
  function changed() {
    clearTimeout(timer);
    timer = setTimeout(saveDraft, 700);
  }
  form.addEventListener('input', changed);
  window.addEventListener('pagehide', function () { if (!desk.hidden) saveDraft(); });

  function fill(d) {
    editing = d.slug || null;
    uploads = d.uploads || {};
    f.title.value = d.title || '';
    f.subtitle.value = d.subtitle || '';
    f.author.value = d.author || store.get(AUTHOR) || '';
    f.date.value = d.date || today();
    f.tags.value = Array.isArray(d.tags) ? d.tags.join(', ') : d.tags || '';
    writeBody(d.blocks);
    $('[data-mode]').textContent = editing ? T.edit_h : T.new_h;
    publishBtn.textContent = editing ? T.update : T.publish;
    cancelBtn.hidden = !editing;
    linkRow.hidden = true;
  }
  function fresh() {
    clearTimeout(timer);
    store.del(DRAFT);
    fill({});
  }
  cancelBtn.addEventListener('click', function () { hush(); fresh(); });
  $('[data-clear]').addEventListener('click', function () { hush(); fresh(); });

  /* ---- Publish ---- */
  var watching = 0;
  function watch(url) {
    // A new post has no page until the build finishes; say so when it does.
    var mine = ++watching, tries = 0;
    (function poll() {
      if (mine !== watching || ++tries > 28) return;
      setTimeout(function () {
        fetch(url, { method: 'HEAD', cache: 'no-store' }).then(function (res) {
          if (mine !== watching) return;
          if (res.ok) say('success', T.s_live, { href: url, text: T.view });
          else poll();
        }, poll);
      }, 15000);
    })();
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (busy) { say('info', T.s_wait); return; }
    var d = snapshot();
    if (!d.title.trim()) { fail({ code: 'no_title' }); f.title.focus(); return; }
    if (!d.blocks.length) { fail({ code: 'no_body' }); body.focus(); return; }
    d.tags = d.tags.split(/[,\n]/).map(function (t) { return t.trim(); }).filter(Boolean);
    saveDraft();
    publishBtn.disabled = true;
    say('info', T.s_publishing);
    api('POST', 'publish', d).then(function (res) {
      store.set(AUTHOR, d.author.trim());
      fresh();
      var url = T.prefix + res.url;
      say('success', T.s_saved, res.edited ? { href: url, text: T.view } : null)
        .scrollIntoView({ block: 'nearest' });
      if (!res.edited) watch(url); else watching++;
      loadPosts();
    }, fail).then(function () { publishBtn.disabled = busy > 0; });
  });

  /* ---- Earlier posts ---- */
  function row(p) {
    var li = el('li', 'cm-card nd-write__post');
    var text = el('div', 'nd-write__posttext');
    var a = el('a');
    a.href = T.prefix + '/pathivu/' + p.slug + '.html';
    a.textContent = p.title;
    var meta = el('p');
    meta.textContent = [p.date, p.author, p.photos ? p.photos + ' ' + T.photo_n : '']
      .filter(Boolean).join(' · ');
    text.appendChild(a); text.appendChild(meta);
    var acts = el('div', 'nd-write__postacts');
    var edit = el('button', 'cm-btn cm-btn--secondary cm-btn--sm');
    edit.type = 'button';
    edit.textContent = T.edit;
    edit.addEventListener('click', function () {
      hush();
      edit.disabled = true;
      api('GET', 'post?slug=' + encodeURIComponent(p.slug)).then(function (res) {
        clearTimeout(timer);
        fill(res.post);
        saveDraft();
        form.scrollIntoView({ block: 'start' });
        f.title.focus();
      }, fail).then(function () { edit.disabled = false; });
    });
    var del = el('button', 'cm-btn cm-btn--ghost cm-btn--sm nd-write__del');
    del.type = 'button';
    del.textContent = T['delete'];
    var armed = null;
    del.addEventListener('click', function () {
      // two presses rather than a dialog: the first asks, the second deletes
      if (!armed) {
        del.textContent = T.confirm;
        del.setAttribute('data-armed', '');
        armed = setTimeout(function () {
          armed = null;
          del.textContent = T['delete'];
          del.removeAttribute('data-armed');
        }, 5000);
        return;
      }
      clearTimeout(armed);
      del.disabled = true;
      api('POST', 'delete', { slug: p.slug }).then(function () {
        if (editing === p.slug) fresh();
        li.remove();
        if (!list.children.length) empty();
        say('success', T.s_deleted);
      }, function (e) { del.disabled = false; fail(e); });
    });
    acts.appendChild(edit); acts.appendChild(del);
    li.appendChild(text); li.appendChild(acts);
    return li;
  }
  function empty() {
    list.innerHTML = '';
    var li = el('li', 'nd-write__none');
    li.textContent = T.none;
    list.appendChild(li);
  }
  function loadPosts() {
    return api('GET', 'posts').then(function (res) {
      list.innerHTML = '';
      if (!res.posts.length) { empty(); return; }
      res.posts.forEach(function (p) { list.appendChild(row(p)); });
    });
  }

  /* ---- Start ---- */
  function openDesk() {
    hush();
    return loadPosts().then(function () {
      loginForm.hidden = true;
      desk.hidden = false;
      var d = null;
      try { d = JSON.parse(store.get(DRAFT) || 'null'); } catch (e) {}
      if (d && (String(d.title || '').trim() || (d.blocks || []).length)) {
        fill(d);
        say('info', T.s_draft);
      } else fill({});
    }, function (e) {
      if (e.code !== 'signed_out') fail(e);
      desk.hidden = true;
      loginForm.hidden = false;
    });
  }

  if (token) openDesk(); else loginForm.hidden = false;
})();
