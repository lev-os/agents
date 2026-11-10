// Tests for scripts/citations.mjs. Run: node --test ~/.agents/skills/lev-ceo/tests/citations.test.mjs
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { afterEach, test } from "node:test";
import { fileURLToPath } from "node:url";

const SCRIPT = join(dirname(fileURLToPath(import.meta.url)), "..", "scripts", "citations.mjs");
const made = [];
afterEach(() => { for (const dir of made.splice(0)) rmSync(dir, { recursive: true, force: true }); });

function check(skillText, extra = {}) {
  const dir = mkdtempSync(join(tmpdir(), "citations-test-"));
  made.push(dir);
  const skill = join(dir, "skill");
  const root = join(dir, "checkout");
  mkdirSync(join(skill, "references"), { recursive: true });
  mkdirSync(join(skill, "scripts"), { recursive: true });
  mkdirSync(join(root, "core", "pkg"), { recursive: true });
  writeFileSync(join(skill, "SKILL.md"), skillText);
  writeFileSync(join(skill, "references", "workers.md"), extra.reference ?? "# Workers\n");
  writeFileSync(join(skill, "scripts", "settle.mjs"), "// one\n");
  writeFileSync(join(root, "AGENTS.md"), "one\ntwo\nthree\n");
  writeFileSync(join(root, "core", "pkg", "file.ts"), "export {};\n");
  return spawnSync(process.execPath, [SCRIPT, "--skill", skill, "--root", root], { encoding: "utf8" });
}

test("citations that resolve pass: checkout paths, skill paths, a line inside its file", () => {
  const run = check("Read `AGENTS.md`, then `AGENTS.md:3`, `core/pkg/file.ts`, `references/workers.md` and `scripts/settle.mjs`.\n");
  assert.equal(run.status, 0, run.stderr);
  assert.match(run.stdout, /5 citations checked in 2 files, 0 failed/);
});

test("known bad: a line past the end of its file fails, the way AGENTS.md:152 did on 2026-11-10", () => {
  const run = check("The footer rule is `AGENTS.md:152`.\n");
  assert.equal(run.status, 1);
  assert.match(run.stderr, /SKILL\.md:1: AGENTS\.md:152 → line 152 is past the end/);
});

test("a line citation written outside backticks is checked too", () => {
  const run = check("Stage by path (AGENTS.md:88).\n");
  assert.equal(run.status, 1);
  assert.match(run.stderr, /AGENTS\.md:88 → line 88 is past the end/);
});

test("a missing file fails, in a reference file as well", () => {
  const run = check("Fine.\n", { reference: "See `core/pkg/gone.ts` and `references/nope.md`.\n" });
  assert.equal(run.status, 1);
  assert.match(run.stderr, /workers\.md:1: core\/pkg\/gone\.ts → no such file/);
  assert.match(run.stderr, /references\/nope\.md → no such file/);
});

test("patterns, runtime paths and commands are not citations", () => {
  const run = check("Write `.lev/pm/decisions/<date>-<slug>.yaml`, keep state in `~/.local/state/lev/ceo/`, run `pnpm --dir core/pkg typecheck`.\n");
  assert.equal(run.status, 0, run.stderr);
  assert.match(run.stdout, /0 citations checked/);
});
