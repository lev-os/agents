import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { languageFromQuery, safeLanguage } from '../assets/template/js/lang.mjs';
import { createCaptureProfile, removeCaptureProfile, resolveAssetFile } from '../assets/template/tools/runtime-safety.mjs';
import { checkPlan } from '../assets/template/tools/plan-check.mjs';
import { neighbours } from '../assets/template/tools/sound-print.mjs';

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'motion-graphics-regression-'));
const profiles = [];
try {
  const root = path.join(tmp, 'project');
  const sibling = path.join(tmp, 'project-private');
  fs.mkdirSync(path.join(root, 'css'), { recursive: true });
  fs.mkdirSync(path.join(root, 'js'), { recursive: true });
  fs.mkdirSync(path.join(root, 'assets'), { recursive: true });
  fs.mkdirSync(path.join(root, 'assets', 'footage'), { recursive: true });
  fs.mkdirSync(path.join(root, 'assets', 'misc'), { recursive: true });
  fs.mkdirSync(sibling);
  for (const file of ['index.html', 'css/main.css', 'js/main.mjs', 'assets/logo.png', 'assets/footage/scan.json', 'assets/footage/talk.srt', 'assets/footage/talk.vtt']) {
    fs.writeFileSync(path.join(root, file), 'local');
  }
  fs.writeFileSync(path.join(sibling, 'secret.png'), 'secret');
  fs.symlinkSync(path.join(sibling, 'secret.png'), path.join(root, 'assets', 'footage', 'linked.json'));

  assert.equal(resolveAssetFile(root, '/'), fs.realpathSync(path.join(root, 'index.html')));
  assert.equal(resolveAssetFile(root, '/assets/logo.png'), fs.realpathSync(path.join(root, 'assets/logo.png')));
  for (const file of ['scan.json', 'talk.srt', 'talk.vtt']) {
    assert.equal(resolveAssetFile(root, `/assets/footage/${file}`), fs.realpathSync(path.join(root, 'assets', 'footage', file)));
  }
  for (const request of [
    '/%2e%2e/project-private/secret.png',
    '/%ZZ',
    '/.env',
    '/js/credentials.json',
    '/assets/misc/data.json',
    '/assets/misc/talk.srt',
    '/assets/footage/my-token.vtt',
    '/assets/footage/linked.json',
    '/README.md',
  ]) assert.throws(() => resolveAssetFile(root, request), undefined, request);

  const owned = createCaptureProfile();
  const other = createCaptureProfile();
  profiles.push(owned, other);
  assert.equal(removeCaptureProfile(owned), true);
  assert.equal(fs.existsSync(owned), false);
  assert.equal(fs.existsSync(other), true);
  assert.equal(removeCaptureProfile(root), false);
  removeCaptureProfile(other);

  assert.equal(safeLanguage('zh-Hant-TW'), 'zh-Hant-TW');
  assert.equal(languageFromQuery('lang=fr-CA&only=hook'), 'fr-CA');
  for (const lang of ['../../outside', 'en/us', 'en onload', '', 'a'.repeat(36)]) assert.throws(() => safeLanguage(lang));
  assert.throws(() => languageFromQuery('lang=..%2F..%2Foutside'));

  for (const [name, markdownNotes] of [['json-default', false], ['markdown-opt-in', true]]) {
    const dest = path.join(tmp, name);
    const args = [path.join(path.dirname(fileURLToPath(import.meta.url)), 'new-project.mjs'), dest];
    if (markdownNotes) args.push('--markdown-notes');
    const scaffold = spawnSync(process.execPath, args, { encoding: 'utf8', stdio: 'ignore', timeout: 20000 });
    assert.equal(scaffold.error, undefined);
    const note = JSON.parse(fs.readFileSync(path.join(dest, 'production.json'), 'utf8'));
    assert.ok(note.direction && 'energy' in note.direction);
    assert.ok(Array.isArray(note.story));
    assert.ok(note.sound && 'feel_genre' in note.sound);
    assert.equal(fs.existsSync(path.join(dest, 'README.md')), markdownNotes);
    assert.equal(fs.existsSync(path.join(dest, 'brief.md')), markdownNotes);
    assert.equal(fs.existsSync(path.join(dest, 'REVIEW.md')), markdownNotes);
  }
  const plan = checkPlan(
    { S: { hook: [0, 5] }, CUE: { start: 0 }, BEAT: 0.5, DURATION: 5, ENERGY: { hook: 'high' } },
    { production: { direction: { energy: 'dynamic launch' } } },
  );
  assert.equal(plan.find((row) => row.what === 'asked')?.level, 'PASS');
  const markdownPlan = checkPlan(
    { S: { hook: [0, 5] }, CUE: { start: 0 }, BEAT: 0.5, DURATION: 5, ENERGY: { hook: 'high' } },
    { readme: '- Energy: dynamic launch' },
  );
  assert.equal(markdownPlan.find((row) => row.what === 'asked')?.level, 'PASS');

  fs.mkdirSync(path.join(sibling, 'out', 'qa'), { recursive: true });
  fs.writeFileSync(path.join(sibling, 'out', 'qa', 'sibling-print.json'), JSON.stringify({ version: 2, file: 'sibling.wav' }));
  assert.deepEqual(neighbours(root), []);
  // Recorded-sound notes are JSON by default; license edits survive regeneration.
  const clip = path.join(tmp, 'tone.wav');
  const made = spawnSync('ffmpeg', ['-v', 'error', '-f', 'lavfi', '-i', 'sine=frequency=440:duration=0.02', '-ar', '48000', '-ac', '2', clip], { encoding: 'utf8' });
  assert.equal(made.status, 0, made.stderr);
  const kitTool = path.join(path.dirname(fileURLToPath(import.meta.url)), '../assets/template/tools/kit.mjs');
  const kitOut = path.join(tmp, 'kit');
  const runKit = (...flags) => {
    const r = spawnSync(process.execPath, [kitTool, clip, '--out', kitOut, ...flags], { encoding: 'utf8' });
    assert.equal(r.status, 0, r.stderr);
  };
  runKit();
  assert.equal(fs.existsSync(path.join(kitOut, 'KIT.md')), false);
  const kitFile = path.join(kitOut, 'KIT.json');
  const kit = JSON.parse(fs.readFileSync(kitFile, 'utf8'));
  assert.equal(kit.sounds.length, 1);
  kit.sounds[0].source = 'own regression fixture';
  kit.sounds[0].license = 'test-only';
  fs.writeFileSync(kitFile, JSON.stringify(kit));
  runKit();
  assert.equal(JSON.parse(fs.readFileSync(kitFile, 'utf8')).sounds[0].license, 'test-only');
  runKit('--markdown-notes');
  assert.equal(fs.existsSync(path.join(kitOut, 'KIT.md')), true);

  console.log('runtime safety regression checks passed');
} finally {
  for (const profile of profiles) removeCaptureProfile(profile);
  fs.rmSync(tmp, { recursive: true, force: true });
}
