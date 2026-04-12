# E2E Test Reporting

## Table of Contents
- [Report Types](#report-types)
- [Playwright Built-in Reports](#playwright-built-in-reports)
- [Custom Report Generation](#custom-report-generation)
- [CI Integration](#ci-integration)
- [Screenshot Management](#screenshot-management)

---

## Report Types

| Type | Format | Purpose | When |
|------|--------|---------|------|
| **HTML Report** | `.html` | Human review, debugging | Local dev, PR review |
| **JSON Report** | `.json` | Programmatic analysis, dashboards | CI pipelines |
| **JUnit XML** | `.xml` | CI integration (GitHub, Jenkins) | CI systems |
| **Console Summary** | stdout | Quick pass/fail | All runs |

---

## Playwright Built-in Reports

### Configuration

```typescript
// playwright.config.ts
export default defineConfig({
  reporter: [
    // Console output
    ['list'],

    // HTML report (auto-opens on failure)
    ['html', { open: 'on-failure', outputFolder: 'playwright-report' }],

    // JSON for programmatic access
    ['json', { outputFile: 'test-results/results.json' }],

    // JUnit for CI systems
    ['junit', { outputFile: 'test-results/junit.xml' }],
  ],
});
```

### HTML Report Features

```bash
# Generate and open HTML report
bunx playwright show-report

# Serve report on specific port
bunx playwright show-report --port 9323
```

The HTML report includes:
- Test tree with pass/fail status
- Screenshots (automatic on failure)
- Video recordings (if enabled)
- Trace viewer (step-by-step debugging)
- Console logs captured during test
- Network requests timeline

---

## Custom Report Generation

### E2E Report Generator

```typescript
// e2e/utils/report-generator.ts
import * as fs from 'fs';
import * as path from 'path';

export interface TestResult {
  name: string;
  status: 'passed' | 'failed' | 'skipped';
  duration: number;
  screenshots: string[];
  consoleErrors: number;
}

export interface E2EReport {
  runId: string;
  timestamp: string;
  summary: {
    total: number;
    passed: number;
    failed: number;
    skipped: number;
    duration: number;
  };
  screenshotsCount: number;
  tests: TestResult[];
  consoleErrorsSummary: Record<string, number>;
}

export class ReportGenerator {
  private results: TestResult[] = [];
  private startTime: number;

  constructor() {
    this.startTime = Date.now();
  }

  addResult(result: TestResult): void {
    this.results.push(result);
  }

  generate(): E2EReport {
    const passed = this.results.filter(r => r.status === 'passed').length;
    const failed = this.results.filter(r => r.status === 'failed').length;
    const skipped = this.results.filter(r => r.status === 'skipped').length;

    return {
      runId: `run-${Date.now()}`,
      timestamp: new Date().toISOString(),
      summary: {
        total: this.results.length,
        passed,
        failed,
        skipped,
        duration: Date.now() - this.startTime,
      },
      screenshotsCount: this.results.reduce((sum, r) => sum + r.screenshots.length, 0),
      tests: this.results,
      consoleErrorsSummary: this.aggregateConsoleErrors(),
    };
  }

  private aggregateConsoleErrors(): Record<string, number> {
    const summary: Record<string, number> = {};
    for (const result of this.results) {
      if (result.consoleErrors > 0) {
        summary[result.name] = result.consoleErrors;
      }
    }
    return summary;
  }

  writeJSON(outputPath: string): void {
    const report = this.generate();
    fs.writeFileSync(outputPath, JSON.stringify(report, null, 2));
  }

  writeHTML(outputPath: string): void {
    const report = this.generate();
    const html = this.renderHTML(report);
    fs.writeFileSync(outputPath, html);
  }

  private renderHTML(report: E2EReport): string {
    return `<!DOCTYPE html>
<html>
<head>
  <title>E2E Test Report - ${report.timestamp}</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 2rem; }
    .summary { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem; }
    .stat { padding: 1rem; border-radius: 8px; text-align: center; }
    .stat.passed { background: #d4edda; }
    .stat.failed { background: #f8d7da; }
    .stat.total { background: #e2e3e5; }
    .stat.screenshots { background: #d1ecf1; }
    .stat h3 { margin: 0; font-size: 2rem; }
    .stat p { margin: 0.5rem 0 0; color: #666; }
    table { width: 100%; border-collapse: collapse; }
    th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #ddd; }
    .status-passed { color: #28a745; }
    .status-failed { color: #dc3545; font-weight: bold; }
    .status-skipped { color: #6c757d; }
    .screenshot { max-width: 200px; cursor: pointer; }
  </style>
</head>
<body>
  <h1>E2E Test Report</h1>
  <p>Run ID: ${report.runId} | ${report.timestamp}</p>

  <div class="summary">
    <div class="stat total">
      <h3>${report.summary.total}</h3>
      <p>Total Tests</p>
    </div>
    <div class="stat passed">
      <h3>${report.summary.passed}</h3>
      <p>Passed</p>
    </div>
    <div class="stat failed">
      <h3>${report.summary.failed}</h3>
      <p>Failed</p>
    </div>
    <div class="stat screenshots">
      <h3>${report.screenshotsCount}</h3>
      <p>Screenshots</p>
    </div>
  </div>

  <h2>Test Results</h2>
  <table>
    <thead>
      <tr>
        <th>Test</th>
        <th>Status</th>
        <th>Duration</th>
        <th>Console Errors</th>
        <th>Screenshots</th>
      </tr>
    </thead>
    <tbody>
      ${report.tests.map(test => `
        <tr>
          <td>${test.name}</td>
          <td class="status-${test.status}">${test.status.toUpperCase()}</td>
          <td>${(test.duration / 1000).toFixed(2)}s</td>
          <td>${test.consoleErrors || 0}</td>
          <td>${test.screenshots.length}</td>
        </tr>
      `).join('')}
    </tbody>
  </table>

  ${Object.keys(report.consoleErrorsSummary).length > 0 ? `
  <h2>Console Errors Summary</h2>
  <ul>
    ${Object.entries(report.consoleErrorsSummary).map(([test, count]) =>
      `<li><strong>${test}</strong>: ${count} errors</li>`
    ).join('')}
  </ul>
  ` : ''}
</body>
</html>`;
  }
}
```

---

## CI Integration

### GitHub Actions Artifact Upload

```yaml
# .github/workflows/e2e.yml
- name: Run E2E tests
  run: bun run test:e2e:prod
  env:
    E2E_TEST_EMAIL: ${{ secrets.E2E_TEST_EMAIL }}
    E2E_TEST_PASSWORD: ${{ secrets.E2E_TEST_PASSWORD }}

- name: Upload test results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: e2e-results-${{ github.run_id }}
    path: |
      playwright-report/
      test-results/
    retention-days: 14

- name: Upload screenshots on failure
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: e2e-screenshots-${{ github.run_id }}
    path: test-results/screenshots/
    retention-days: 7
```

### PR Comment with Results

```yaml
- name: Comment PR with results
  if: github.event_name == 'pull_request'
  uses: actions/github-script@v7
  with:
    script: |
      const fs = require('fs');
      const results = JSON.parse(fs.readFileSync('test-results/results.json', 'utf8'));

      const passed = results.summary.passed;
      const failed = results.summary.failed;
      const total = results.summary.total;

      const emoji = failed === 0 ? '✅' : '❌';
      const body = `## ${emoji} E2E Test Results

      | Metric | Value |
      |--------|-------|
      | Total | ${total} |
      | Passed | ${passed} |
      | Failed | ${failed} |
      | Duration | ${(results.summary.duration / 1000).toFixed(1)}s |
      | Screenshots | ${results.screenshotsCount} |

      ${failed > 0 ? `### Failed Tests\n${results.tests.filter(t => t.status === 'failed').map(t => `- ${t.name}`).join('\n')}` : ''}
      `;

      github.rest.issues.createComment({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: context.issue.number,
        body
      });
```

---

## Screenshot Management

### Organized Screenshot Storage

```typescript
// e2e/utils/screenshot-manager.ts
import * as fs from 'fs';
import * as path from 'path';

export class ScreenshotManager {
  private baseDir: string;
  private runId: string;

  constructor(baseDir = 'test-results/screenshots') {
    this.baseDir = baseDir;
    this.runId = `run-${Date.now()}`;
    this.ensureDir();
  }

  private ensureDir(): void {
    const runDir = path.join(this.baseDir, this.runId);
    fs.mkdirSync(runDir, { recursive: true });
  }

  /**
   * Generate a consistent screenshot path.
   */
  getPath(testName: string, step: string, viewport: string): string {
    const safeName = testName.replace(/[^a-z0-9]/gi, '-').toLowerCase();
    const safeStep = step.replace(/[^a-z0-9]/gi, '-').toLowerCase();
    const filename = `${safeName}_${safeStep}_${viewport}_${Date.now()}.png`;
    return path.join(this.baseDir, this.runId, filename);
  }

  /**
   * Clean up old screenshots (keep last N runs).
   */
  cleanup(keepRuns = 5): void {
    const runs = fs.readdirSync(this.baseDir)
      .filter(d => d.startsWith('run-'))
      .sort()
      .reverse();

    for (const run of runs.slice(keepRuns)) {
      fs.rmSync(path.join(this.baseDir, run), { recursive: true });
    }
  }

  /**
   * Get total size of screenshots.
   */
  getTotalSizeMB(): number {
    let totalBytes = 0;

    const walkDir = (dir: string) => {
      for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          walkDir(fullPath);
        } else {
          totalBytes += fs.statSync(fullPath).size;
        }
      }
    };

    walkDir(this.baseDir);
    return totalBytes / (1024 * 1024);
  }
}
```

### Compression for CI

```typescript
import sharp from 'sharp';

export async function compressScreenshot(
  inputPath: string,
  quality = 80
): Promise<string> {
  const outputPath = inputPath.replace('.png', '.webp');

  await sharp(inputPath)
    .webp({ quality })
    .toFile(outputPath);

  // Remove original
  fs.unlinkSync(inputPath);

  return outputPath;
}
```

---

## Report Viewer Script

```bash
#!/usr/bin/env bash
# scripts/view-report.sh

# Open the latest HTML report
if [ -f "playwright-report/index.html" ]; then
  echo "Opening Playwright HTML report..."
  bunx playwright show-report
elif [ -f "test-results/report.html" ]; then
  echo "Opening custom HTML report..."
  open test-results/report.html  # macOS
  # xdg-open test-results/report.html  # Linux
else
  echo "No report found. Run tests first: bun run test:e2e"
  exit 1
fi
```
