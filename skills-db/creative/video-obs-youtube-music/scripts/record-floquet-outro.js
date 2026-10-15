#!/usr/bin/env node
/**
 * Record FloquetTopoCA outro video at 4K resolution
 * Uses step-driven animation for frame-perfect capture
 */

import { chromium } from 'playwright';
import { createServer } from 'http';
import { readFileSync, existsSync, mkdirSync, writeFileSync } from 'fs';
import { join, extname } from 'path';
import { execSync, spawn } from 'child_process';

const HOME = process.env.HOME || '';
const PROJECT_DIR = process.env.SMEARED_LIFE_DIR || join(HOME, 'projects', 'smeared_life');
const OUTPUT_DIR = process.env.OUTPUT_DIR || join(HOME, 'Movies');
const TEMP_DIR = process.env.TEMP_DIR || '/tmp/floquet_outro_frames';
const HTML_FILE = 'outro-workflow-capture.html';

// MIME types
const MIME_TYPES = {
  '.html': 'text/html',
  '.js': 'application/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
};

async function main() {
  // Create HTTP server for the project
  const server = createServer((req, res) => {
    let filePath = join(PROJECT_DIR, req.url === '/' ? HTML_FILE : req.url);

    if (!existsSync(filePath)) {
      res.writeHead(404);
      res.end('Not found');
      return;
    }

    const ext = extname(filePath);
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    try {
      const content = readFileSync(filePath);
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
    } catch (err) {
      res.writeHead(500);
      res.end('Server error');
    }
  });

  const PORT = 8765;
  server.listen(PORT);
  console.log(`Server running at http://localhost:${PORT}`);

  // Launch browser
  const browser = await chromium.launch({
    headless: true,
    args: ['--disable-web-security', '--use-gl=angle', '--use-angle=metal'],
  });

  const context = await browser.newContext({
    viewport: { width: 4096, height: 2304 },
    deviceScaleFactor: 1,
  });

  const page = await context.newPage();

  // Navigate to the page
  await page.goto(`http://localhost:${PORT}/${HTML_FILE}`);

  // Wait for initialization
  await page.waitForFunction(() => window.CONFIG !== undefined);

  // Get config
  const config = await page.evaluate(() => window.CONFIG);
  console.log(`Recording: ${config.width}x${config.height} @ ${config.fps}fps for ${config.duration / 1000}s`);

  const totalFrames = Math.ceil((config.duration / 1000) * config.fps);
  console.log(`Total frames: ${totalFrames}`);

  // Create temp directory for frames
  const tempDir = TEMP_DIR;
  if (!existsSync(tempDir)) {
    mkdirSync(tempDir, { recursive: true });
  }

  // Clear any existing frames
  execSync(`rm -f ${tempDir}/*.png`);

  console.log('Recording frames...');
  const startTime = Date.now();

  for (let frame = 0; frame < totalFrames; frame++) {
    // Step the animation
    await page.evaluate(() => window.stepFrame());

    // Capture screenshot
    const framePath = join(tempDir, `frame_${String(frame).padStart(6, '0')}.png`);
    await page.screenshot({ path: framePath, type: 'png' });

    // Progress update every 60 frames
    if (frame % 60 === 0) {
      const elapsed = (Date.now() - startTime) / 1000;
      const fps = frame / elapsed;
      const remaining = (totalFrames - frame) / fps;
      console.log(`  Frame ${frame}/${totalFrames} (${(frame / totalFrames * 100).toFixed(1)}%) - ${fps.toFixed(1)} fps - ETA: ${remaining.toFixed(0)}s`);
    }
  }

  const elapsed = (Date.now() - startTime) / 1000;
  console.log(`\nCapture complete in ${elapsed.toFixed(1)}s (${(totalFrames / elapsed).toFixed(1)} fps avg)`);

  await browser.close();
  server.close();

  // Encode to video with FFmpeg
  const outputPath = join(OUTPUT_DIR, 'floquet_outro.mp4');
  console.log(`\nEncoding to ${outputPath}...`);

  const ffmpegArgs = [
    '-y',
    '-framerate', String(config.fps),
    '-i', `${tempDir}/frame_%06d.png`,
    '-c:v', 'libx264',
    '-preset', 'slow',
    '-crf', '18',
    '-pix_fmt', 'yuv420p',
    '-movflags', '+faststart',
    outputPath,
  ];

  const ffmpeg = spawn('ffmpeg', ffmpegArgs, { stdio: 'inherit' });

  await new Promise((resolve, reject) => {
    ffmpeg.on('close', (code) => {
      if (code === 0) {
        console.log(`\nOutro video created: ${outputPath}`);
        resolve();
      } else {
        reject(new Error(`FFmpeg exited with code ${code}`));
      }
    });
  });

  // Cleanup frames
  execSync(`rm -rf ${tempDir}`);
  console.log('Cleaned up temp frames');
}

main().catch(console.error);
