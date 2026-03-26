#!/usr/bin/env node
/**
 * Render text overlay at 4K resolution with transparency.
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const HOME = process.env.HOME || '';
const PROJECT_DIR = process.env.SMEARED_LIFE_DIR || path.join(HOME, 'projects', 'smeared_life');
const DEFAULT_HTML = path.join(PROJECT_DIR, 'outro-text-overlay.html');
const DEFAULT_OUTPUT_DIR = path.join(HOME, 'Movies', 'text_frames');
const HTML_FILE = process.argv[2] || process.env.HTML_FILE || DEFAULT_HTML;
const OUTPUT_DIR = process.argv[3] || process.env.OUTPUT_DIR || DEFAULT_OUTPUT_DIR;
const WIDTH = 4096;
const HEIGHT = 2304;
const FPS = 30;
const DURATION_MS = 55000;

async function main() {
  console.log(`Rendering text overlay at ${WIDTH}x${HEIGHT}`);
  console.log(`HTML: ${HTML_FILE}`);
  console.log(`Output: ${OUTPUT_DIR}`);

  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  const browser = await chromium.launch({
    headless: true,
    args: ['--disable-web-security']
  });

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

  await page.goto(`file://${HTML_FILE}`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);

  const expectedFrames = Math.ceil((DURATION_MS / 1000) * FPS);
  let frameCount = 0;
  const startTime = Date.now();

  console.log(`\nCapturing ${expectedFrames} frames...`);

  while (frameCount < expectedFrames) {
    const framePath = path.join(OUTPUT_DIR, `text_${String(frameCount).padStart(5, '0')}.png`);
    await page.screenshot({
      path: framePath,
      omitBackground: true  // Alpha transparency!
    });

    frameCount++;

    if (frameCount % 60 === 0) {
      const elapsed = (Date.now() - startTime) / 1000;
      const realFps = frameCount / elapsed;
      const remaining = expectedFrames - frameCount;
      const eta = remaining / realFps;
      console.log(`Frame ${frameCount}/${expectedFrames} (${realFps.toFixed(1)} fps, ETA: ${eta.toFixed(0)}s)`);
    }

    const complete = await page.evaluate(() => window.stepFrame());
    if (complete) break;
  }

  await browser.close();

  const totalTime = (Date.now() - startTime) / 1000;
  console.log(`\nDone!`);
  console.log(`Frames: ${frameCount}`);
  console.log(`Output: ${OUTPUT_DIR}`);
  console.log(`Time: ${totalTime.toFixed(1)}s`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
