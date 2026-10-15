#!/usr/bin/env node
// Scaffolds a promo project from the skill's template (assets/template): picture (index.html, css, js/scenes), the
// shared timeline, the synth + a demo score (audio/), and the tools (capture, render, qa, audio-check), then checks the
// environment. The demo scenes and the demo score are marked @template-demo: replace them — tools/qa.mjs warns if any
// are left. A file already in the folder is never overwritten.
//
//   node <skill>/scripts/new-project.mjs <dir> [--name "Brand"] [--format 16:9|9:16|1:1|4:5] [--fps 60] [--bpm 120]
//                                               [--lang xx] [--markdown-notes]
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { safeLanguage } from '../assets/template/js/lang.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const TEMPLATE = path.resolve(HERE, '..', 'assets', 'template');
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(`--${k}`); return i >= 0 && args[i + 1] !== undefined ? args[i + 1] : d; };
const BOOL = new Set(['--markdown-notes']);
let dir = null;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--force') { console.error('--force is not supported; use a fresh project directory'); process.exit(1); }
  if (args[i].startsWith('--')) { if (!BOOL.has(args[i])) i++; continue; }
  dir = dir ?? args[i];
}
if (!dir) {
  console.log('usage: node scripts/new-project.mjs <fresh-dir> [--name "Brand"] [--format 16:9|9:16|1:1|4:5] [--fps 60] [--bpm 120] [--lang en] [--markdown-notes]');
  process.exit(1);
}
const dest = path.resolve(dir);
if (fs.existsSync(dest) && fs.lstatSync(dest).isSymbolicLink()) { console.error(`${dest} is a symlink — choose a fresh directory`); process.exit(1); }
const FORMATS = { '16:9': [1920, 1080], '9:16': [1080, 1920], '1:1': [1080, 1080], '4:5': [1080, 1350] };
const format = opt('format', '16:9');
if (!FORMATS[format]) { console.error(`--format must be one of ${Object.keys(FORMATS).join(', ')}`); process.exit(1); }
const [W, H] = FORMATS[format];
const fps = Number(opt('fps', 60));
const bpm = Number(opt('bpm', 120));
const name = opt('name', 'NOVA');
const lang = safeLanguage(opt('lang', 'en'));
// file-name slug in any script: "Café Lumière" → "cafe-lumiere-promo"; a name in another alphabet keeps its letters
const slug = String(opt('slug', null) || `${name}-promo`).toLowerCase().normalize('NFKD').replace(/(\p{Script=Latin})\p{M}+/gu, '$1').normalize('NFC').replace(/[^\p{L}\p{M}\p{N}_-]+/gu, '-')
  .replace(/-+/g, '-').replace(/^-+|-+$/g, '') || 'promo';

// Only the early brand/reference inputs may already exist. Other project contents need a new destination.
const EARLY = new Set(['brand', 'refs', 'brief.md', 'README.md', '.cache', '.DS_Store']);
const foreign = fs.existsSync(dest) ? fs.readdirSync(dest).filter((f) => !EARLY.has(f)) : [];
if (foreign.length) {
  console.error(`${dest} already holds ${foreign.slice(0, 5).join(', ')}${foreign.length > 5 ? ', …' : ''} — use a fresh directory`);
  process.exit(1);
}
const fresh = new Set();
const kept = [];
const copy = (rel) => {
  for (const e of fs.readdirSync(path.join(TEMPLATE, rel), { withFileTypes: true })) {
    if (['out', '.cache', 'node_modules'].includes(e.name)) continue;
    const r = rel ? `${rel}/${e.name}` : e.name;
    const to = path.join(dest, r);
    if (e.isDirectory()) { fs.mkdirSync(to, { recursive: true }); copy(r); }
    else if (!args.includes('--markdown-notes') && r.endsWith('.md')) continue;
    else if (fs.existsSync(to)) kept.push(r);
    else { fs.copyFileSync(path.join(TEMPLATE, r), to); fresh.add(r); }
  }
};
fs.mkdirSync(dest, { recursive: true });
copy('');
for (const d of ['out', 'refs', 'assets/img']) fs.mkdirSync(path.join(dest, d), { recursive: true });

// fill the @param lines — only in files this run wrote: a kept file is the user's
const edit = (rel, fn) => { if (!fresh.has(rel)) return; const f = path.join(dest, rel); fs.writeFileSync(f, fn(fs.readFileSync(f, 'utf8'))); };
const param = (src, key, value) => src.replace(new RegExp(`^(export const \\w+ = )[^;]+(; // @param ${key}\\b.*)$`, 'm'), (_, head, tail) => `${head}${value}${tail}`);
edit('js/timeline.mjs', (s) => [['width', W], ['height', H], ['fps', fps], ['bpm', bpm]].reduce((a, [k, v]) => param(a, k, v), s));
edit('js/copy.mjs', (s) => param(param(param(s, 'name', JSON.stringify(name)), 'slug', JSON.stringify(slug)), 'lang', JSON.stringify(lang)));
edit('index.html', (s) => s.replace('<html lang="en">', () => `<html lang="${lang}">`).replace('<title>promo</title>', () => `<title>${name.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')} — promo</title>`));
if (!fs.existsSync(path.join(dest, '.gitignore'))) fs.writeFileSync(path.join(dest, '.gitignore'), 'out/\n.cache/\n');
for (const f of ['README.md', 'brief.md']) edit(f, (s) => s.replaceAll('__BRAND__', () => name));

console.log(`scaffolded ${dest}  (${W}x${H} @ ${fps} fps, ${bpm} BPM, "${name}", ${lang})`);
if (kept.length) console.log(`kept ${kept.length} file${kept.length > 1 ? 's' : ''} already there: ${kept.slice(0, 6).join(', ')}${kept.length > 6 ? ', …' : ''}`);
const doc = spawnSync(process.execPath, [path.join(TEMPLATE, 'tools', 'capture.mjs'), 'doctor'], { cwd: dest, encoding: 'utf8' });
process.stdout.write(doc.stdout || '');
process.stderr.write(doc.stderr || '');
console.log(`
next (from ${path.relative(process.cwd(), dest) || '.'}):
  node tools/capture.mjs sheet 0 12 24               the demo as a contact sheet → out/sheet.png (proves the pipeline)
  plan js/timeline.mjs (scene windows, cues, ENERGY), then: node tools/plan-check.mjs
  then replace the demo: js/copy.mjs, js/scenes/*, js/reel.js SCENES, css/style.css, audio/score.mjs`);
if (doc.status !== 0) process.exitCode = 1;
