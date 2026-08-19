#!/usr/bin/env node
/**
 * Record SpinGlassCA outro at full 4K resolution.
 */

const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const http = require('http');
const fs = require('fs');

const HOME = process.env.HOME || '';
const SMEARED_LIFE_DIR = process.env.SMEARED_LIFE_DIR || path.join(HOME, 'projects', 'smeared_life');
const HTML_FILE = process.argv[2] || 'outro-spinglass-writeup.html';
const OUTPUT_FILE = process.argv[3]
  || process.env.OUTPUT_FILE
  || path.join(HOME, 'Movies', 'outro_2026-01-21.mp4');
const WIDTH = 2048;
const HEIGHT = 1152;
const FPS = 30;
const DURATION_MS = 55000;  // 5s intro + 50s scroll
const PORT = 8768;

function createServer(dir, port) {
  const mimeTypes = {
    '.html': 'text/html',
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.svg': 'image/svg+xml'
  };

  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      let filePath = path.join(dir, req.url.split('?')[0]);
      if (filePath.endsWith('/')) filePath += 'index.html';

      const ext = path.extname(filePath);
      const contentType = mimeTypes[ext] || 'application/octet-stream';

      fs.readFile(filePath, (err, data) => {
        if (err) {
          res.writeHead(404);
          res.end('Not found: ' + filePath);
          return;
        }
        res.writeHead(200, { 'Content-Type': contentType });
        res.end(data);
      });
    });

    server.listen(port, () => {
      console.log(`Server running at http://localhost:${port}/`);
      resolve(server);
    });
  });
}

async function main() {
  console.log(`Recording SpinGlassCA outro at FULL 4K`);
  console.log(`HTML: ${HTML_FILE}`);
  console.log(`Output: ${OUTPUT_FILE}`);
  console.log(`Resolution: ${WIDTH}x${HEIGHT} @ ${FPS}fps`);
  console.log(`Duration: ${DURATION_MS/1000}s`);

  const server = await createServer(SMEARED_LIFE_DIR, PORT);

  const browser = await chromium.launch({
    headless: true,
    args: [
      '--disable-web-security',
      '--use-gl=swiftshader',
      '--enable-webgl',
      '--enable-webgl2',
      '--ignore-gpu-blocklist',
      '--disable-gpu-sandbox'
    ]
  });

  const context = await browser.newContext({
    viewport: { width: WIDTH, height: HEIGHT },
    deviceScaleFactor: 1
  });

  const page = await context.newPage();

  page.on('console', msg => {
    const text = msg.text();
    if (msg.type() === 'error' || text.includes('initialized')) {
      console.log(`Browser: ${text}`);
    }
  });
  page.on('pageerror', err => console.log('Page error:', err.message));

  const url = `http://localhost:${PORT}/${HTML_FILE}`;
  console.log(`Loading: ${url}`);

  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);

  const ffmpeg = spawn('ffmpeg', [
    '-y',
    '-f', 'image2pipe',
    '-framerate', String(FPS),
    '-i', '-',
    '-c:v', 'libx264',
    '-preset', 'slow',
    '-crf', '18',
    '-pix_fmt', 'yuv420p',
    '-movflags', '+faststart',
    OUTPUT_FILE
  ], {
    stdio: ['pipe', 'inherit', 'inherit']
  });

  const expectedFrames = Math.ceil((DURATION_MS / 1000) * FPS);
  let frameCount = 0;
  const startTime = Date.now();

  console.log(`\nCapturing ${expectedFrames} frames...`);

  while (frameCount < expectedFrames) {
    const screenshot = await page.screenshot({
      type: 'png',
      omitBackground: false,
      timeout: 120000
    });

    const written = ffmpeg.stdin.write(screenshot);
    if (!written) {
      await new Promise(resolve => ffmpeg.stdin.once('drain', resolve));
    }

    frameCount++;

    if (frameCount % 30 === 0) {
      const elapsed = (Date.now() - startTime) / 1000;
      const realFps = frameCount / elapsed;
      const remaining = expectedFrames - frameCount;
      const eta = remaining / realFps;
      console.log(`Frame ${frameCount}/${expectedFrames} (${realFps.toFixed(1)} fps, ETA: ${eta.toFixed(0)}s)`);
    }

    const complete = await page.evaluate(() => window.stepFrame());
    if (complete) break;
  }

  console.log(`\nCaptured ${frameCount} frames, encoding...`);

  ffmpeg.stdin.end();
  await new Promise((resolve, reject) => {
    ffmpeg.on('close', code => {
      if (code === 0) resolve();
      else reject(new Error(`ffmpeg exited with ${code}`));
    });
  });

  await browser.close();
  server.close();

  const totalTime = (Date.now() - startTime) / 1000;
  const stats = fs.statSync(OUTPUT_FILE);
  console.log(`\nDone!`);
  console.log(`Output: ${OUTPUT_FILE}`);
  console.log(`Size: ${(stats.size / 1024 / 1024).toFixed(1)} MB`);
  console.log(`Time: ${totalTime.toFixed(1)}s`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
