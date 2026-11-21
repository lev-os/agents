// Tests for mods/continue-approved, the stop hook mod of a CEO chat. Run: node --test tests/mod-copy.test.mjs
// The mod's own tests of its rules run in Claude Code: claude plugin test mods/continue-approved
// The mod imports no file outside its folder, so it holds a copy of scripts/for-you-form.mjs. This file fails when
// the copy differs, and when the mod's folder lacks a file that Claude Code needs to load it.
import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

const skill = join(dirname(fileURLToPath(import.meta.url)), "..");
const mod = join(skill, "mods", "continue-approved");

test("the mod's copy of for-you-form.mjs has the same bytes as scripts/for-you-form.mjs", () => {
  const source = readFileSync(join(skill, "scripts", "for-you-form.mjs"));
  const copy = readFileSync(join(mod, "hooks", "for-you-form.mjs"));
  assert.ok(source.equals(copy), "copy scripts/for-you-form.mjs to mods/continue-approved/hooks/for-you-form.mjs");
});

test("the mod's folder holds its manifest and each module that hooks.json names", () => {
  const manifest = JSON.parse(readFileSync(join(mod, ".claude-plugin", "plugin.json"), "utf8"));
  assert.equal(manifest.name, "continue-approved");
  const hooks = JSON.parse(readFileSync(join(mod, "hooks", "hooks.json"), "utf8"));
  assert.ok(Array.isArray(hooks.modules) && hooks.modules.length > 0, "hooks.json names no module");
  for (const module of hooks.modules) {
    assert.ok(existsSync(join(mod, "hooks", module)), `hooks.json names ${module}, which is not in the folder`);
  }
});
