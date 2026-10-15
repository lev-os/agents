import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";

const ENV_FILES = [
  ".env.production.local",
  ".env.local",
  ".env.production",
  ".env",
];

const TEST_SITE_KEYS = /^(1x|2x|3x)0{20}/;

const errors: string[] = [];
const warnings: string[] = [];

function readEnv(file: string): Record<string, string> {
  let raw: string;
  try {
    raw = readFileSync(file, "utf8");
  } catch {
    return {};
  }

  const values: Record<string, string> = {};
  for (const line of raw.split("\n")) {
    const match = /^\s*([A-Z0-9_]+)\s*=\s*(.*)$/.exec(line);
    if (!match) continue;
    values[match[1]] = match[2].trim().replace(/^["']|["']$/g, "");
  }
  return values;
}

function resolve(name: string): string | undefined {
  if (process.env[name]) return process.env[name];
  for (const file of ENV_FILES) {
    const value = readEnv(file)[name];
    if (value) return value;
  }
  return undefined;
}

function workerSecrets(): string[] | null {
  try {
    const raw = execFileSync("npx", ["wrangler", "secret", "list"], {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
    });
    const parsed = JSON.parse(raw) as { name?: string }[];
    return parsed.map((entry) => entry.name ?? "");
  } catch {
    return null;
  }
}

const config = JSON.parse(
  readFileSync("wrangler.jsonc", "utf8").replace(/^\s*\/\/.*$/gm, ""),
) as { vars?: Record<string, string> };

const turnstileRequired = config.vars?.TURNSTILE_ENABLED === "true";
const siteKey = resolve("NEXT_PUBLIC_TURNSTILE_SITE_KEY");

if (!config.vars?.RESEND_SEGMENT_ID) {
  errors.push(
    "RESEND_SEGMENT_ID is missing from wrangler.jsonc. Every signup must be assigned to the Canvas UI Newsletter segment.",
  );
}

if (turnstileRequired) {
  if (!siteKey) {
    errors.push(
      "NEXT_PUBLIC_TURNSTILE_SITE_KEY is not set, but wrangler.jsonc has TURNSTILE_ENABLED=\"true\".\n" +
        "  Every signup would fail with 403. Add the site key to .env.production.local.",
    );
  } else if (TEST_SITE_KEYS.test(siteKey)) {
    errors.push(
      `NEXT_PUBLIC_TURNSTILE_SITE_KEY is a Cloudflare test key (${siteKey}).\n` +
        "  Replace it with the real site key in .env.production.local before deploying.",
    );
  }
} else if (siteKey) {
  warnings.push(
    'wrangler.jsonc has TURNSTILE_ENABLED="false", so the Worker accepts unverified signups.',
  );
}

if (!resolve("NEXT_PUBLIC_HTML_IN_CANVAS_OT_TOKEN")) {
  warnings.push(
    "NEXT_PUBLIC_HTML_IN_CANVAS_OT_TOKEN is not set — html-in-canvas demos will fall back on canvasui.dev.",
  );
}

const secrets = workerSecrets();
if (secrets === null) {
  warnings.push(
    "Could not read Worker secrets (`wrangler secret list`). Verify RESEND_API_KEY" +
      (turnstileRequired ? " and TURNSTILE_SECRET_KEY" : "") +
      " are set on the deployed Worker.",
  );
} else {
  if (!secrets.includes("RESEND_API_KEY")) {
    errors.push(
      "Worker secret RESEND_API_KEY is missing. Run: npx wrangler secret put RESEND_API_KEY",
    );
  }
  if (turnstileRequired && !secrets.includes("TURNSTILE_SECRET_KEY")) {
    errors.push(
      "Worker secret TURNSTILE_SECRET_KEY is missing. Run: npx wrangler secret put TURNSTILE_SECRET_KEY",
    );
  }
}

for (const warning of warnings) {
  console.warn(`⚠ ${warning}`);
}

if (errors.length > 0) {
  console.error("\n✖ Deploy preflight failed:\n");
  for (const error of errors) {
    console.error(`  • ${error}\n`);
  }
  process.exit(1);
}

console.log("✓ Deploy preflight passed.");
