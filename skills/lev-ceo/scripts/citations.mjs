#!/usr/bin/env node
/**
 * Citation check: every file the skill cites exists, and every cited line is inside its file.
 *
 * Usage: node ~/.agents/skills/lev-ceo/scripts/citations.mjs [--skill <dir>] [--root <checkout>] [file.md ...]
 *
 * With no files, it reads SKILL.md and references/*.md under --skill (default: this skill).
 * A citation is a path in backticks, with an optional `:line`, `:line-line` or `#anchor`, and any
 * `file.ext:line` written outside backticks. Where a path resolves:
 *   ~/...                                   the home folder
 *   SKILL.md, references/, scripts/, tests/ the skill folder
 *   anything else                           --root (default: the working directory)
 * Skipped: a pattern (it holds < > { } * $ or a space) and a runtime path (~/.local, ~/.config, ~/.Trash, /tmp).
 * Exit 0 when every citation resolves; exit 1 with one line per failure.
 */
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

const { values, positionals } = parseArgs({
  options: { skill: { type: "string" }, root: { type: "string" } },
  allowPositionals: true,
});
const skill = resolve(values.skill ?? join(dirname(fileURLToPath(import.meta.url)), ".."));
const root = resolve(values.root ?? process.cwd());
const files = positionals.length > 0
  ? positionals.map((file) => resolve(file))
  : [join(skill, "SKILL.md"), ...(existsSync(join(skill, "references")) ? readdirSync(join(skill, "references")).filter((f) => f.endsWith(".md")).map((f) => join(skill, "references", f)) : [])];

const PATH_START = /^(~\/|\.\/|\.lev\/|\.agents\/|\.claude\/|core\/|plugins\/|dna\/|docs\/|apps\/|tooling\/|references\/|scripts\/|tests\/)|^(AGENTS|CLAUDE|SKILL)\.md\b/;
const PATTERN = /[<>{}*$|\s]/;
const RUNTIME = /^(~\/\.local\/|~\/\.config\/|~\/\.Trash|\/tmp\/)/;
const SKILL_LOCAL = /^(SKILL\.md|references\/|scripts\/|tests\/)/;
const BARE_LINE = /(?<![`\w/.~-])((?:~\/|\.{0,2}\/)?[\w.-]+(?:\/[\w.-]+)*\.(?:md|ya?ml|ts|mjs|js|json|sh)):(\d+)/g;

function locate(path) {
  if (path.startsWith("~/")) return join(homedir(), path.slice(2));
  if (SKILL_LOCAL.test(path)) return join(skill, path);
  return join(root, path);
}

function check(path, line) {
  const target = locate(path);
  if (!existsSync(target)) return "no such file";
  if (line === undefined || statSync(target).isDirectory()) return null;
  const count = readFileSync(target, "utf8").split("\n").length;
  return line > count ? `line ${line} is past the end (${count} lines)` : null;
}

let checked = 0;
const failures = [];
for (const file of files) {
  const rows = readFileSync(file, "utf8").split("\n");
  rows.forEach((row, index) => {
    const seen = new Set();
    const cite = (path, line) => {
      const key = `${path}:${line ?? ""}`;
      if (seen.has(key) || PATTERN.test(path) || RUNTIME.test(path)) return;
      seen.add(key);
      checked += 1;
      const why = check(path, line);
      if (why) failures.push(`${file}:${index + 1}: ${path}${line === undefined ? "" : `:${line}`} → ${why}`);
    };
    for (const [, span] of row.matchAll(/`([^`]+)`/g)) {
      if (!PATH_START.test(span)) continue;
      const [, path, line] = span.match(/^([^:#]+)(?::(\d+)(?:-\d+)?)?(?:#.*)?$/) ?? [];
      if (path) cite(path.replace(/[.,;]$/, ""), line === undefined ? undefined : Number(line));
    }
    for (const [, path, line] of row.replace(/`[^`]*`/g, "").matchAll(BARE_LINE)) cite(path, Number(line));
  });
}

for (const failure of failures) console.error(failure);
console.log(`${checked} citations checked in ${files.length} files, ${failures.length} failed`);
process.exit(failures.length > 0 ? 1 : 0);
