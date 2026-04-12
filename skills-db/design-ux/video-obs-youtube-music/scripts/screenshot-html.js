#!/usr/bin/env node
/**
 * Screenshot or record video of an HTML file using Playwright.
 *
 * Usage:
 *   Screenshot: ./screenshot-html.js <html-file> <output.png> [width] [height]
 *   Video:      ./screenshot-html.js <html-file> <output.webm> [width] [height] [duration_ms]
 */

const { chromium } = require('playwright');
const path = require('path');

async function main() {
    const args = process.argv.slice(2);

    if (args.length < 2) {
        console.error('Usage: screenshot-html.js <html-file> <output.(png|webm)> [width] [height] [duration_ms]');
        process.exit(1);
    }

    const htmlFile = path.resolve(args[0]);
    const outputFile = path.resolve(args[1]);
    const width = parseInt(args[2]) || 2280;
    const height = parseInt(args[3]) || 480;
    const durationMs = parseInt(args[4]) || 6000;  // Default 6 seconds for video

    const isVideo = outputFile.endsWith('.webm');

    const browser = await chromium.launch();
    const context = await browser.newContext({
        viewport: { width, height },
        // Required for video recording
        recordVideo: isVideo ? {
            dir: path.dirname(outputFile),
            size: { width, height }
        } : undefined
    });

    const page = await context.newPage();
    await page.goto(`file://${htmlFile}`);

    // Wait for any images to load
    await page.waitForLoadState('networkidle');

    if (isVideo) {
        // Get video reference BEFORE closing the page
        const video = page.video();

        // Wait for animation to complete
        await page.waitForTimeout(durationMs);

        // Close page to finalize video
        await page.close();

        // Now get the video path and move to desired output
        if (video) {
            const videoPath = await video.path();
            const fs = require('fs');
            // Playwright saves to a temp file, move it to our desired location
            // Use try/catch for rename in case of cross-filesystem move
            try {
                fs.renameSync(videoPath, outputFile);
            } catch (e) {
                // Fallback to copy + delete for cross-filesystem
                fs.copyFileSync(videoPath, outputFile);
                fs.unlinkSync(videoPath);
            }
            console.log(`Video saved: ${outputFile}`);
        } else {
            console.error('Warning: No video was recorded');
        }
    } else {
        await page.screenshot({
            path: outputFile,
            omitBackground: true  // Preserve transparency
        });
        console.log(`Screenshot saved: ${outputFile}`);
    }

    await browser.close();
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
