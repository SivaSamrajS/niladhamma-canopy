/* Niladhamma · the writers' desk, server side.
 *
 * The site is static: a post exists once it is committed to the repository
 * and the next build has rendered it. So "publishing" here means writing one
 * commit through the GitHub API, which is what triggers that build. Nothing is
 * stored on Netlify.
 *
 * Settings, read from the environment (Netlify: Site configuration >
 * Environment variables). None of them belongs in the repository.
 *   WRITER_USERNAME      the shared sign-in name
 *   WRITER_PASSWORD      the shared password
 *   WRITER_GITHUB_TOKEN  fine-grained token, Contents read and write, this repo
 *   WRITER_REPO          optional, defaults to SivaSamrajS/niladhamma-canopy
 *   WRITER_BRANCH        optional, defaults to main
 */

import { createHash, createHmac, randomBytes, timingSafeEqual } from 'node:crypto';

const env = (k) => (process.env[k] || '').trim();
const REPO = () => env('WRITER_REPO') || 'SivaSamrajS/niladhamma-canopy';
const BRANCH = () => env('WRITER_BRANCH') || 'main';

export const SESSION_DAYS = 7;
const IMG_DIR = 'assets/img/pathivu';
const POST_DIR = 'data/blog';
const IMG_SRC = /^\/assets\/img\/pathivu\/(m[0-9a-f]{14})\.jpg$/;
const SLUG = /^\d{4}-\d{2}-\d{2}-[0-9a-f]{6}$/;
const SHA = /^[0-9a-f]{40}$/;
const MAX_FULL = 3 * 1024 * 1024;
const MAX_SMALL = 600 * 1024;

export class Fail extends Error {
  constructor(status, code, detail) {
    super(detail || code);
    this.status = status;
    this.code = code;
  }
}

export function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
  });
}

/** Run a handler and turn a thrown Fail into its response. */
export async function guard(run) {
  try {
    return await run();
  } catch (e) {
    if (e instanceof Fail) return json({ error: e.code, detail: e.message }, e.status);
    console.error(e);
    return json({ error: 'server', detail: 'Unexpected error' }, 500);
  }
}

export async function body(req) {
  try {
    return await req.json();
  } catch {
    throw new Fail(400, 'bad_request', 'Body is not JSON');
  }
}

/* ---- Sign-in ----
   The session token is an expiry time signed with a key derived from the
   username and password. Changing either setting therefore signs everyone
   out, which is the behaviour wanted when a shared password is replaced. */

function configured() {
  if (!env('WRITER_USERNAME') || !env('WRITER_PASSWORD')) {
    throw new Fail(503, 'not_configured', 'WRITER_USERNAME and WRITER_PASSWORD are not set');
  }
}

function key() {
  return createHash('sha256')
    .update(`nd-write|${env('WRITER_USERNAME')}|${env('WRITER_PASSWORD')}`).digest();
}

function same(a, b) {
  // Compared as digests so the lengths never differ and nothing leaks by time.
  const x = createHash('sha256').update(String(a)).digest();
  const y = createHash('sha256').update(String(b)).digest();
  return timingSafeEqual(x, y);
}

const sign = (exp) => createHmac('sha256', key()).update(String(exp)).digest('hex');

export function login(username, password) {
  configured();
  const ok = same(String(username || '').trim(), env('WRITER_USERNAME'))
    & same(String(password || ''), env('WRITER_PASSWORD'));
  if (!ok) throw new Fail(401, 'bad_login', 'Wrong username or password');
  const exp = Date.now() + SESSION_DAYS * 864e5;
  return { token: `${exp}.${sign(exp)}`, expires: exp };
}

export function requireSession(req) {
  configured();
  const m = /^Bearer (\d{10,16})\.([0-9a-f]{64})$/.exec(req.headers.get('authorization') || '');
  if (!m || Number(m[1]) < Date.now() || !same(m[2], sign(m[1]))) {
    throw new Fail(401, 'signed_out', 'Sign in again');
  }
}

/* ---- Text ----
   Everything a writer types is reduced to a small set of inline tags before
   it is stored. build.py applies the same rule again when it renders, so the
   pages are safe even if a file in data/blog is edited by hand. */

const ENT = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ' };
const decode = (s) => s.replace(/&(#x?[0-9a-f]+|[a-z]+);/gi, (m, n) => {
  if (n[0] === '#') {
    const cp = n[1].toLowerCase() === 'x' ? parseInt(n.slice(2), 16) : parseInt(n.slice(1), 10);
    return cp > 0 && cp < 0x110000 ? String.fromCodePoint(cp) : '';
  }
  return n.toLowerCase() in ENT ? ENT[n.toLowerCase()] : m;
});
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;');
const clean = (s) => s.replace(/[\u0000-\u0008\u000b-\u001f\u007f\u200b\u2028\u2029]/g, '');

const INLINE = { b: 'b', strong: 'b', i: 'i', em: 'i', u: 'u' };

function href(attrs) {
  const m = /\bhref\s*=\s*(?:"([^"]*)"|'([^']*)')/i.exec(attrs);
  if (!m) return '';
  let url = decode(m[1] ?? m[2]).trim();
  // The deploy audit rejects plain http links, and so should the page.
  url = url.replace(/^http:\/\//i, 'https://');
  return /^(https:\/\/|mailto:)[^\s<>"]+$/i.test(url) ? url : '';
}

export function inline(input, limit = 20000) {
  const src = clean(String(input ?? '')).slice(0, limit);
  const open = [];
  let out = '';
  let at = 0;
  const text = (s) => { out += esc(decode(s)).replace(/\s+/g, ' '); };
  for (const m of src.matchAll(/<(\/?)([a-zA-Z][a-zA-Z0-9]*)([^>]*)>/g)) {
    text(src.slice(at, m.index));
    at = m.index + m[0].length;
    const tag = m[2].toLowerCase();
    const name = INLINE[tag] || (tag === 'a' ? 'a' : null);
    if (tag === 'br' && !m[1]) {
      if (out && !out.endsWith('<br>')) out += '<br>';
    } else if (name && !m[1]) {
      if (name === 'a') {
        const url = href(m[3]);
        if (!url || open.includes('a')) continue;
        out += `<a href="${esc(url)}">`;
      } else {
        out += `<${name}>`;
      }
      open.push(name);
    } else if (name && m[1] && open.includes(name)) {
      while (open.length) {
        const top = open.pop();
        out += `</${top}>`;
        if (top === name) break;
      }
    }
  }
  text(src.slice(at));
  while (open.length) out += `</${open.pop()}>`;
  return out.replace(/^(\s|<br>)+|(\s|<br>)+$/g, '');
}

const bare = (s) => decode(String(s).replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();

/** A single line of plain text: titles, names, tags. Stored unescaped. */
export function line(input, limit) {
  return clean(String(input ?? '')).replace(/<[^<>]*>/g, '').replace(/[<>]/g, '')
    .replace(/\s+/g, ' ').trim()
    .slice(0, limit);
}

export function youtubeId(input) {
  const s = String(input ?? '').trim();
  if (/^[A-Za-z0-9_-]{11}$/.test(s)) return s;
  const m = /(?:youtu\.be\/|youtube(?:-nocookie)?\.com\/(?:watch\?(?:[^#\s]*&)?v=|embed\/|shorts\/|live\/))([A-Za-z0-9_-]{11})(?![A-Za-z0-9_-])/.exec(s);
  return m ? m[1] : '';
}

/** Blocks as the editor sends them, reduced to what build.py renders. */
export function blocks(input) {
  if (!Array.isArray(input)) throw new Fail(400, 'bad_request', 'blocks must be a list');
  const out = [];
  for (const b of input.slice(0, 400)) {
    if (!Array.isArray(b)) continue;
    const kind = b[0];
    if (kind === 'p' || kind === 'quote') {
      const html = inline(b[1]);
      if (bare(html)) out.push([kind, html]);
    } else if (kind === 'h2' || kind === 'h3') {
      const t = esc(bare(inline(b[1], 300)));
      if (t) out.push([kind, t]);
    } else if (kind === 'ul' || kind === 'ol') {
      const items = (Array.isArray(b[1]) ? b[1] : []).slice(0, 200)
        .map((x) => inline(x)).filter((x) => bare(x));
      if (items.length) out.push([kind, items]);
    } else if (kind === 'fig') {
      if (IMG_SRC.test(String(b[1]))) out.push(['fig', b[1], inline(b[2], 600)]);
    } else if (kind === 'video') {
      const id = youtubeId(b[1]);
      if (id) out.push(['video', id]);
    }
  }
  return out;
}

/* ---- Photographs ---- */

function jpeg(b64, max, what) {
  if (typeof b64 !== 'string' || !/^[A-Za-z0-9+/]+=*$/.test(b64)) {
    throw new Fail(400, 'bad_image', `${what} is not base64`);
  }
  const buf = Buffer.from(b64, 'base64');
  if (buf.length > max) throw new Fail(413, 'image_too_large', `${what} is too large`);
  if (buf.length < 100 || buf[0] !== 0xff || buf[1] !== 0xd8 || buf[2] !== 0xff) {
    throw new Fail(400, 'bad_image', `${what} is not a JPEG`);
  }
  return buf;
}

/** Pixel size from the JPEG's own frame header, not from what the client says. */
export function jpegSize(buf) {
  let i = 2;
  while (i + 9 < buf.length) {
    if (buf[i] !== 0xff) { i += 1; continue; }
    const marker = buf[i + 1];
    if (marker === 0xff) { i += 1; continue; }
    if (marker === 0xd8 || (marker >= 0xd0 && marker <= 0xd7) || marker === 0x01) { i += 2; continue; }
    const len = buf.readUInt16BE(i + 2);
    const sof = marker >= 0xc0 && marker <= 0xcf && ![0xc4, 0xc8, 0xcc].includes(marker);
    if (sof) return [buf.readUInt16BE(i + 7), buf.readUInt16BE(i + 5)];
    i += 2 + len;
  }
  return null;
}

/* ---- GitHub ---- */

async function gh(method, path, payload, accept) {
  const token = env('WRITER_GITHUB_TOKEN');
  if (!token) throw new Fail(503, 'not_configured', 'WRITER_GITHUB_TOKEN is not set');
  const res = await fetch(`https://api.github.com/repos/${REPO()}${path}`, {
    method,
    headers: {
      authorization: `Bearer ${token}`,
      accept: accept || 'application/vnd.github+json',
      'x-github-api-version': '2022-11-28',
      'user-agent': 'niladhamma-writers-desk',
      ...(payload ? { 'content-type': 'application/json' } : {}),
    },
    body: payload ? JSON.stringify(payload) : undefined,
  });
  return res;
}

async function ghJson(method, path, payload) {
  const res = await gh(method, path, payload);
  if (!res.ok) {
    const detail = (await res.text()).slice(0, 300);
    console.error(`GitHub ${method} ${path} -> ${res.status} ${detail}`);
    if (res.status === 401 || res.status === 403) {
      throw new Fail(502, 'storage_denied', 'The GitHub token was refused');
    }
    const err = new Fail(502, 'storage', `GitHub answered ${res.status}`);
    err.upstream = res.status;
    throw err;
  }
  return res.json();
}

async function readPost(slug) {
  if (!SLUG.test(slug)) throw new Fail(400, 'bad_request', 'Unknown post');
  const res = await gh('GET', `/contents/${POST_DIR}/${slug}.json?ref=${BRANCH()}`, null,
    'application/vnd.github.raw+json');
  if (res.status === 404) return null;
  if (!res.ok) throw new Fail(502, 'storage', `GitHub answered ${res.status}`);
  try {
    return JSON.parse(await res.text());
  } catch {
    return null;
  }
}

const figs = (post) => (post?.blocks || []).filter((b) => b[0] === 'fig').map((b) => b[1]);

function imagePaths(src) {
  const name = `${IMG_SRC.exec(src)[1]}.jpg`;
  return [`${IMG_DIR}/${name}`, `${IMG_DIR}/tile/${name}`, `${IMG_DIR}/thumb/${name}`];
}

/** One commit on top of the branch. Retried when someone else got there first. */
async function commitOnce(message, entries) {
  for (let attempt = 0; ; attempt += 1) {
    const ref = await ghJson('GET', `/git/ref/heads/${BRANCH()}`);
    const head = await ghJson('GET', `/git/commits/${ref.object.sha}`);
    let tree;
    try {
      tree = await ghJson('POST', '/git/trees', { base_tree: head.tree.sha, tree: entries });
    } catch (e) {
      // GitHub refuses a tree that names a blob it does not have, or deletes
      // a path that is not there.
      if (e.upstream === 422 || e.upstream === 404) throw new Fail(409, 'tree', 'Tree refused');
      throw e;
    }
    // No author is named, so GitHub records the owner of the token. Netlify
    // only builds commits from a contributor it recognises, and a made-up
    // "writers" identity is not one: the post would be saved and never appear.
    const made = await ghJson('POST', '/git/commits', {
      message, tree: tree.sha, parents: [ref.object.sha],
    });
    try {
      await ghJson('PATCH', `/git/refs/heads/${BRANCH()}`, { sha: made.sha, force: false });
      return made.sha;
    } catch (e) {
      if (attempt >= 2 || e.upstream !== 422) throw e;
    }
  }
}

/** Deletions are a courtesy: if one is refused, the commit goes ahead without
    them rather than failing the writer over a file that was already gone. */
async function commit(message, entries) {
  try {
    return await commitOnce(message, entries);
  } catch (e) {
    const kept = entries.filter((x) => x.sha !== null);
    if (e.code !== 'tree' || kept.length === entries.length || !kept.length) throw e;
    return commitOnce(message, kept);
  }
}

const file = (path, sha) => ({ path, mode: '100644', type: 'blob', sha });

/* ---- Actions ---- */

export async function listPosts() {
  const res = await gh('GET', `/contents/${POST_DIR}?ref=${BRANCH()}`);
  if (res.status === 404) return [];
  if (!res.ok) throw new Fail(502, 'storage', `GitHub answered ${res.status}`);
  const names = (await res.json())
    .map((f) => f.name.replace(/\.json$/, '')).filter((n) => SLUG.test(n))
    .sort().reverse().slice(0, 60);
  const posts = await Promise.all(names.map((n) => readPost(n).catch(() => null)));
  return posts.filter(Boolean).map((p) => ({
    slug: p.slug, title: p.title, date: p.date, author: p.author || '',
    photos: figs(p).length,
  }));
}

export async function getPost(slug) {
  const post = await readPost(slug);
  if (!post) throw new Fail(404, 'not_found', 'That post no longer exists');
  return post;
}

export async function storeImage(input) {
  const full = jpeg(input.full, MAX_FULL, 'The photograph');
  const tile = jpeg(input.tile, MAX_SMALL, 'The display copy');
  const thumb = jpeg(input.thumb, MAX_SMALL, 'The thumbnail');
  const size = jpegSize(full);
  if (!size || !size[0] || !size[1]) throw new Fail(400, 'bad_image', 'Unreadable JPEG');
  // Salted, so the same photograph in two posts is two files and withdrawing
  // one post cannot take a picture out of the other.
  const id = `m${createHash('sha256').update(full).update(randomBytes(8)).digest('hex').slice(0, 14)}`;
  const [a, b, c] = await Promise.all([full, tile, thumb].map((buf) =>
    ghJson('POST', '/git/blobs', { content: buf.toString('base64'), encoding: 'base64' })));
  return {
    src: `/${IMG_DIR}/${id}.jpg`, width: size[0], height: size[1],
    blobs: [a.sha, b.sha, c.sha],
  };
}

function today() {
  // Asia/Kolkata, as build.py reckons it.
  return new Date(Date.now() + 5.5 * 36e5).toISOString().slice(0, 10);
}

export async function publish(input) {
  const title = line(input.title, 160);
  if (!title) throw new Fail(400, 'no_title', 'A title is needed');
  const body = blocks(input.blocks);
  if (!body.length) throw new Fail(400, 'no_body', 'The post is empty');

  const date = /^\d{4}-\d{2}-\d{2}$/.test(input.date || '')
    && !Number.isNaN(Date.parse(input.date)) ? input.date : today();
  const editing = input.slug ? await getPost(String(input.slug)) : null;
  const slug = editing ? editing.slug
    : `${date}-${createHash('sha256').update(`${title}|${Date.now()}|${Math.random()}`)
      .digest('hex').slice(0, 6)}`;

  const had = new Set(figs(editing));
  const uploads = input.uploads && typeof input.uploads === 'object' ? input.uploads : {};
  const entries = [];
  const sizes = { ...(editing?.sizes || {}) };
  const used = new Set();
  for (const src of figs({ blocks: body })) {
    if (used.has(src)) continue;
    used.add(src);
    if (had.has(src)) continue;
    const up = uploads[src];
    const ok = up && Array.isArray(up.blobs) && up.blobs.length === 3
      && up.blobs.every((s) => SHA.test(s));
    if (!ok) throw new Fail(400, 'missing_image', 'A photograph did not finish uploading');
    imagePaths(src).forEach((p, i) => entries.push(file(p, up.blobs[i])));
    sizes[src] = [Number(up.width) | 0, Number(up.height) | 0];
  }
  for (const src of Object.keys(sizes)) if (!used.has(src)) delete sizes[src];
  // Photographs taken out of an edited post leave the repository with it.
  for (const src of had) {
    if (!used.has(src) && IMG_SRC.test(src)) imagePaths(src).forEach((p) => entries.push(file(p, null)));
  }

  const tags = [...new Set((Array.isArray(input.tags) ? input.tags : [])
    .map((t) => line(t, 40)).filter(Boolean))].slice(0, 8);
  const now = new Date().toISOString();
  const post = {
    slug, title,
    subtitle: line(input.subtitle, 240),
    author: line(input.author, 80),
    date, tags, blocks: body, sizes,
    created: editing?.created || now, updated: now,
  };
  entries.push({
    path: `${POST_DIR}/${slug}.json`, mode: '100644', type: 'blob',
    content: `${JSON.stringify(post, null, 1)}\n`,
  });

  try {
    await commit(`${editing ? 'Revise' : 'Publish'} the post: ${title}`.slice(0, 120), entries);
  } catch (e) {
    // A photograph blob GitHub no longer has: the writer must add it again.
    if (e.code === 'tree') throw new Fail(409, 'missing_image', 'A photograph has to be added again');
    throw e;
  }
  return { slug, url: `/pathivu/${slug}.html`, edited: Boolean(editing) };
}

export async function remove(slug) {
  const post = await getPost(String(slug || ''));
  const entries = [file(`${POST_DIR}/${post.slug}.json`, null)];
  for (const src of new Set(figs(post))) {
    if (IMG_SRC.test(src)) imagePaths(src).forEach((p) => entries.push(file(p, null)));
  }
  await commit(`Withdraw the post: ${line(post.title, 90)}`, entries);
  return { slug: post.slug };
}
