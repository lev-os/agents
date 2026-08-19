#!/usr/bin/env node
/**
 * Record intro animation to video using Playwright and ffmpeg.
 *
 * Usage: node record-intro.js <html-file> <output.mp4> [fps] [width] [height]
 *
 * Captures frames from the browser at a consistent FPS and pipes them to ffmpeg.
 */

const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');

async function main() {
    const args = process.argv.slice(2);

    if (args.length < 2) {
        console.error('Usage: record-intro.js <html-file> <output.mp4> [fps] [width] [height]');
        process.exit(1);
    }

    const htmlFile = path.resolve(args[0]);
    const outputFile = path.resolve(args[1]);
    const fps = parseInt(args[2]) || 60;
    const width = parseInt(args[3]) || 1920;
    const height = parseInt(args[4]) || 1080;

    console.log(`Recording ${htmlFile}`);
    console.log(`Output: ${outputFile}`);
    console.log(`Resolution: ${width}x${height} @ ${fps}fps`);

    // Start ffmpeg process to receive frames via stdin
    const ffmpeg = spawn('ffmpeg', [
        '-y',                          // Overwrite output
        '-f', 'image2pipe',            // Input from pipe
        '-framerate', String(fps),     // Input framerate
        '-i', '-',                      // Read from stdin
        '-c:v', 'libx264',             // H.264 codec
        '-preset', 'fast',             // Encoding speed
        '-crf', '18',                  // Quality (lower = better)
        '-pix_fmt', 'yuv420p',         // Pixel format for compatibility
        '-movflags', '+faststart',     // Web streaming optimization
        outputFile
    ], {
        stdio: ['pipe', 'inherit', 'inherit']
    });

    ffmpeg.on('error', (err) => {
        console.error('ffmpeg error:', err);
        process.exit(1);
    });

    // Launch browser with WebGL support
    const browser = await chromium.launch({
        headless: true,
        args: [
            '--disable-web-security',
            '--use-gl=swiftshader',     // Software OpenGL for headless
            '--enable-webgl',
            '--enable-webgl2',
            '--ignore-gpu-blocklist',
            '--disable-gpu-sandbox'
        ]
    });

    const context = await browser.newContext({
        viewport: { width, height },
        deviceScaleFactor: 1
    });

    const page = await context.newPage();

    // Log any page errors
    page.on('console', msg => {
        if (msg.type() === 'error' || msg.type() === 'warning') {
            console.log(`Browser ${msg.type()}: ${msg.text()}`);
        }
    });
    page.on('pageerror', err => console.log('Page error:', err.message));

    // Load the HTML file
    await page.goto(`file://${htmlFile}`, { waitUntil: 'networkidle' });

    // Wait a moment for WebGL to initialize
    await page.waitForTimeout(500);

    // Get the expected duration from the page config
    const durationMs = await page.evaluate(() => window.CONFIG?.duration || 5000);
    const expectedFrames = Math.ceil((durationMs / 1000) * fps);

    console.log(`Starting synchronized frame capture (target: ${expectedFrames} frames for ${durationMs/1000}s)...`);

    let frameCount = 0;
    let startTime = Date.now();

    // Synchronized capture loop: screenshot first, then step animation
    // This ensures the animation only advances when we're ready for the next frame
    while (frameCount < expectedFrames) {
        // Capture current frame as PNG and pipe to ffmpeg
        const screenshot = await page.screenshot({
            type: 'png',
            omitBackground: false,
            timeout: 120000  // 2 min timeout for 4K captures
        });

        // Write frame to ffmpeg stdin
        const written = ffmpeg.stdin.write(screenshot);
        if (!written) {
            // Wait for drain if buffer is full
            await new Promise(resolve => ffmpeg.stdin.once('drain', resolve));
        }

        frameCount++;

        // Log progress every 30 frames
        if (frameCount % 30 === 0) {
            const elapsed = (Date.now() - startTime) / 1000;
            const realFps = frameCount / elapsed;
            const remaining = expectedFrames - frameCount;
            const eta = remaining / realFps;
            console.log(`Frame ${frameCount}/${expectedFrames}, ${realFps.toFixed(2)} fps, ETA: ${eta.toFixed(0)}s`);
        }

        // Step the animation forward AFTER capturing the current frame
        // This keeps animation in sync with our capture rate
        const complete = await page.evaluate(() => window.stepFrame());
        if (complete) {
            console.log(`Animation complete after ${frameCount} frames`);
            break;
        }

        // Safety limit
        if (frameCount > fps * 60) { // Max 60 seconds
            console.log('Max frame limit reached');
            break;
        }
    }

    console.log(`Captured ${frameCount} frames, finalizing video...`);

    // Close ffmpeg stdin to signal end of input
    ffmpeg.stdin.end();

    // Wait for ffmpeg to finish
    await new Promise((resolve, reject) => {
        ffmpeg.on('close', (code) => {
            if (code === 0) {
                resolve();
            } else {
                reject(new Error(`ffmpeg exited with code ${code}`));
            }
        });
    });

    await browser.close();

    const totalTime = (Date.now() - startTime) / 1000;
    console.log(`\nRecording complete!`);
    console.log(`Frames: ${frameCount}`);
    console.log(`Duration: ${(frameCount / fps).toFixed(2)}s`);
    console.log(`Capture time: ${totalTime.toFixed(1)}s`);
    console.log(`Output: ${outputFile}`);
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
