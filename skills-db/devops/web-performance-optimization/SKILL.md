# Web Performance Optimization

## Overview

Help developers optimize website and web application performance to improve user experience, SEO rankings, and conversion rates. Systematic approaches to measure, analyze, and improve loading speed, runtime performance, and Core Web Vitals metrics.

## When to Use This Skill

* Use when website or app is loading slowly
* Use when optimizing for Core Web Vitals (LCP, FID, CLS)
* Use when reducing JavaScript bundle size
* Use when improving Time to Interactive (TTI)
* Use when optimizing images and assets
* Use when implementing caching strategies
* Use when debugging performance bottlenecks
* Use when preparing for performance audits

## How It Works

### Step 1: Measure Current Performance

Establish baseline metrics:
* Run Lighthouse audits
* Measure Core Web Vitals (LCP, FID, CLS)
* Check bundle sizes
* Analyze network waterfall
* Identify performance bottlenecks

### Step 2: Identify Issues

* Large JavaScript bundles
* Unoptimized images
* Render-blocking resources
* Slow server response times
* Missing caching headers
* Layout shifts
* Long tasks blocking main thread

### Step 3: Prioritize Optimizations

Focus on high-impact improvements:
* Critical rendering path optimization
* Code splitting and lazy loading
* Image optimization
* Caching strategies
* Third-party script optimization

### Step 4: Implement Optimizations

* Optimize assets (images, fonts, CSS, JS)
* Implement code splitting
* Add caching headers
* Lazy load non-critical resources
* Optimize critical rendering path

### Step 5: Verify Improvements

* Re-run Lighthouse audits
* Compare before/after metrics
* Monitor real user metrics (RUM)
* Test on different devices and networks

## Best Practices

### Do This

* **Measure First** - Always establish baseline metrics before optimizing
* **Use Lighthouse** - Run audits regularly to track progress
* **Optimize Images** - Use modern formats (WebP, AVIF) and responsive images
* **Code Split** - Break large bundles into smaller chunks
* **Lazy Load** - Defer non-critical resources
* **Cache Aggressively** - Set proper cache headers for static assets
* **Minimize Main Thread Work** - Keep JavaScript execution under 50ms chunks
* **Preload Critical Resources** - Use `<link rel="preload">` for critical assets
* **Use CDN** - Serve static assets from CDN for faster delivery
* **Monitor Real Users** - Track Core Web Vitals from real users

### Don't Do This

* **Don't Optimize Blindly** - Measure first, then optimize
* **Don't Ignore Mobile** - Test on real mobile devices and slow networks
* **Don't Block Rendering** - Avoid render-blocking CSS and JavaScript
* **Don't Load Everything Upfront** - Lazy load non-critical resources
* **Don't Forget Dimensions** - Always specify image width/height
* **Don't Use Synchronous Scripts** - Use async or defer attributes
* **Don't Ignore Third-Party Scripts** - They often cause performance issues
* **Don't Skip Compression** - Always compress and minify assets

## Performance Checklist

### Images

* Convert to modern formats (WebP, AVIF)
* Implement responsive images
* Add lazy loading
* Specify dimensions (width/height)
* Compress images (< 200KB each)
* Use CDN for delivery

### JavaScript

* Bundle size < 200KB (gzipped)
* Implement code splitting
* Lazy load non-critical code
* Remove unused dependencies
* Minify and compress
* Use async/defer for scripts

### CSS

* Inline critical CSS
* Defer non-critical CSS
* Remove unused CSS
* Minify CSS files
* Use CSS containment

### Caching

* Set cache headers for static assets
* Implement service worker
* Use CDN caching
* Cache API responses
* Version static assets

### Core Web Vitals Targets

* LCP < 2.5s
* FID < 100ms
* CLS < 0.1
* TTFB < 600ms
* TTI < 3.8s

## Performance Tools

### Measurement
* **Lighthouse** - Comprehensive performance audit
* **WebPageTest** - Detailed waterfall analysis
* **Chrome DevTools** - Performance profiling
* **PageSpeed Insights** - Real user metrics

### Analysis
* **webpack-bundle-analyzer** - Visualize bundle composition
* **source-map-explorer** - Analyze bundle size
* **Bundlephobia** - Check package sizes before installing

### Monitoring
* **Google Analytics** - Track Core Web Vitals
* **Sentry** - Performance monitoring
* **New Relic** - Application performance monitoring
