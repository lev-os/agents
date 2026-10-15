import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const TYPES = {
  index: new Set(['.html']),
  css: new Set(['.css']),
  js: new Set(['.js', '.mjs']),
  assets: new Set(['.svg', '.png', '.jpg', '.jpeg', '.webp', '.gif', '.avif', '.ttf', '.otf', '.woff', '.woff2', '.mp3', '.wav', '.ogg', '.m4a', '.mp4', '.webm', '.mov']),
};
const FOOTAGE_DATA = new Set(['.json', '.srt', '.vtt']);

export function resolveAssetFile(root, rawPath) {
  let decoded;
  try { decoded = decodeURIComponent(rawPath); } catch { throw new Error('bad path encoding'); }
  if (!decoded.startsWith('/') || decoded.startsWith('//') || decoded.includes('\\') || decoded.includes('\0')) throw new Error('bad path');
  if (decoded === '/') decoded = '/index.html';
  const parts = decoded.split('/').filter(Boolean);
  const area = parts.length === 1 && parts[0] === 'index.html' ? 'index' : parts[0];
  if (!Object.hasOwn(TYPES, area) || (area === 'index' ? parts.length !== 1 : parts.length < 2)
      || parts.some((part) => part.startsWith('.') || part === '..')) throw new Error('path is not served');
  const name = parts.at(-1).toLowerCase();
  const ext = path.extname(name);
  const footageData = area === 'assets' && parts[1] === 'footage' && parts.length >= 3 && FOOTAGE_DATA.has(ext);
  if (/(?:^|[._-])(?:credentials?|secrets?|token|password|id_rsa|id_ed25519)(?:[._-]|$)/.test(name)
      || (!TYPES[area].has(ext) && !footageData)) throw new Error('file type is not served');

  const base = fs.realpathSync(root);
  let file = base;
  for (const [i, part] of parts.entries()) {
    file = path.join(file, part);
    const st = fs.lstatSync(file);
    if (st.isSymbolicLink() || (i < parts.length - 1 && !st.isDirectory())) throw new Error('symlinks are not served');
  }
  const real = fs.realpathSync(file);
  const rel = path.relative(base, real);
  if (rel.startsWith('..') || path.isAbsolute(rel) || !fs.statSync(real).isFile()) throw new Error('path escapes project');
  return real;
}

export function createCaptureProfile() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'motion-graphics-capture-'));
}

export function removeCaptureProfile(profile) {
  const full = path.resolve(profile);
  const base = path.basename(full);
  if (!base.startsWith('motion-graphics-capture-') || path.dirname(full) !== path.resolve(os.tmpdir())) return false;
  fs.rmSync(full, { recursive: true, force: true, maxRetries: 3 });
  return true;
}
