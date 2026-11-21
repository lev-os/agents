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
  writeFileSync(join(skill, "scripts", "settle.mjs"), extra.script ?? "// one\n");
  if (extra.referenceText) writeFileSync(join(skill, "references", "brief.txt"), extra.referenceText);
  if (extra.test) {
    mkdirSync(join(skill, "tests"), { recursive: true });
    writeFileSync(join(skill, "tests", "some.test.mjs"), extra.test);
  }
  writeFileSync(join(root, "AGENTS.md"), "one\ntwo\nthree\n");
  writeFileSync(join(root, "core", "pkg", "file.ts"), "export {};\n");
  mkdirSync(join(root, ".lev", "pm", "decisions"), { recursive: true });
  writeFileSync(join(root, ".lev", "pm", "decisions", "20261110-a-ruling.yaml"), "id: 20261110-a-ruling\n");
  return spawnSync(process.execPath, [SCRIPT, "--skill", skill, "--root", root, ...(extra.args ?? [])], { encoding: "utf8" });
}

const RECORD = [".lev", "pm", "decisions", "20261110-a-ruling.yaml"].join("/");

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

test("a decision record cited in SKILL.md fails, also when the record exists in the checkout", () => {
  const run = check(`Fine.\nWait for JP (\`${RECORD}\`).\n`);
  assert.equal(run.status, 1);
  assert.match(run.stderr, /SKILL\.md:2: .*20261110-a-ruling\.yaml → a decision record is cited/);
});

test("a decision record named in any reference file or script fails, inside backticks or not", () => {
  const run = check("Fine.\n", {
    reference: `See ${RECORD} for why.\n`,
    referenceText: `Rule: read \`${RECORD}\` first.\n`,
    script: `// one\n// Decision: ${RECORD}.\n`,
  });
  assert.equal(run.status, 1);
  assert.match(run.stderr, /references\/workers\.md:1: .*a decision record is cited/);
  assert.match(run.stderr, /references\/brief\.txt:1: .*a decision record is cited/);
  assert.match(run.stderr, /scripts\/settle\.mjs:2: .*a decision record is cited/);
});

test("a decision record named in tests/ is not a skill citation", () => {
  const run = check("Fine.\n", { test: `// fixture: ${RECORD}\n` });
  assert.equal(run.status, 0, run.stderr);
  assert.doesNotMatch(run.stderr, /decision record/);
});

test("a skill that names no decision record still exits 0", () => {
  const run = check("Record each ruling in a decision file.\n", { referenceText: "No record here.\n", script: "// plain\n" });
  assert.equal(run.status, 0, run.stderr);
  assert.match(run.stdout, /0 failed/);
});

test("with --pointers, a reference file that only the Contents section names fails", () => {
  const run = check("## Contents\n\n| `references/workers.md` | Workers |\n\n## 1. Start\n\nNothing points there.\n", { args: ["--pointers"] });
  assert.equal(run.status, 1);
  assert.match(run.stderr, /references\/workers\.md → no file of the skill points at it/);
});

test("with --pointers, a pointer in a step or in a script passes, and without the flag the rule does not run", () => {
  const step = check("## Contents\n\n| `references/workers.md` | Workers |\n\n## 3. Workers\n\nBrief it: `references/workers.md`.\n", { args: ["--pointers"] });
  assert.equal(step.status, 0, step.stderr);
  const script = check("## Contents\n\nNone.\n", { args: ["--pointers"], script: "// reads workers.md from the references folder\n" });
  assert.equal(script.status, 0, script.stderr);
  const off = check("## Contents\n\nNone.\n");
  assert.equal(off.status, 0, off.stderr);
});
