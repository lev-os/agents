#!/usr/bin/env node
/**
 * Render music card to WebM with alpha transparency.
 */

const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const HOME = process.env.HOME || '';
const CARDS_DIR = process.env.CARDS_DIR || path.join(HOME, 'Movies', 'cards');
const CARD_HTML = process.argv[2]
  || process.env.CARD_HTML
  || path.join(CARDS_DIR, 'morgana_card.html');
const OUTPUT_FILE = process.argv[3]
  || process.env.OUTPUT_FILE
  || path.join(CARDS_DIR, 'morgana_card.webm');
const WIDTH = 1900;
const HEIGHT = 480;
const FPS = 60;
const DURATION_S = 6;

async function main() {
  console.log(`Rendering card: ${CARD_HTML}`);
  console.log(`Output: ${OUTPUT_FILE}`);
  console.log(`Resolution: ${WIDTH}x${HEIGHT} @ ${FPS}fps`);
  console.log(`Duration: ${DURATION_S}s`);

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: WIDTH, height: HEIGHT },
    deviceScaleFactor: 1
  });

  const page = await context.newPage();

  page.on('console', msg => {
    if (msg.type() === 'error' || msg.text().includes('initialized')) {
      console.log(`Browser: ${msg.text()}`);
    }
  });

  await page.goto(`file://${CARD_HTML}`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  // Render to PNG frames with transparency
  const framesDir = path.join(path.dirname(OUTPUT_FILE), 'frames_card');
  if (!fs.existsSync(framesDir)) fs.mkdirSync(framesDir, { recursive: true });

  const totalFrames = FPS * DURATION_S;
  const startTime = Date.now();

  console.log(`\nCapturing ${totalFrames} frames...`);

  for (let f = 0; f < totalFrames; f++) {
    const framePath = path.join(framesDir, `frame_${String(f).padStart(4, '0')}.png`);
    await page.screenshot({
      path: framePath,
      omitBackground: true  // Alpha transparency!
    });

    const complete = await page.evaluate(() => window.stepFrame());

    if ((f + 1) % 60 === 0) {
      const elapsed = (Date.now() - startTime) / 1000;
      const fps = (f + 1) / elapsed;
      console.log(`Frame ${f + 1}/${totalFrames} (${fps.toFixed(1)} fps)`);
    }

    if (complete) break;
  }

  await browser.close();

  console.log(`\nEncoding to WebM with alpha...`);

  // Encode to WebM VP9 with alpha
  await new Promise((resolve, reject) => {
    const ffmpeg = spawn('ffmpeg', [
      '-y',
      '-framerate', String(FPS),
      '-i', path.join(framesDir, 'frame_%04d.png'),
      '-c:v', 'libvpx-vp9',
      '-pix_fmt', 'yuva420p',
      '-b:v', '2M',
      OUTPUT_FILE
    ], { stdio: 'inherit' });

    ffmpeg.on('close', code => {
      if (code === 0) resolve();
      else reject(new Error(`ffmpeg exited with ${code}`));
    });
  });

  // Cleanup frames
  const files = fs.readdirSync(framesDir);
  for (const file of files) {
    fs.unlinkSync(path.join(framesDir, file));
  }
  fs.rmdirSync(framesDir);

  const stats = fs.statSync(OUTPUT_FILE);
  const totalTime = (Date.now() - startTime) / 1000;
  console.log(`\nDone!`);
  console.log(`Output: ${OUTPUT_FILE}`);
  console.log(`Size: ${(stats.size / 1024 / 1024).toFixed(1)} MB`);
  console.log(`Time: ${totalTime.toFixed(1)}s`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
