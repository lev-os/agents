#!/usr/bin/env node
// Lists the open top-level chats of every T3 project with the t3 command line, and writes them as one file in
// the form `sweep.mjs scan --threads` takes. No model and no T3 tool: a timer can run it.
// Usage: node list-chats.mjs --projects <projects json> --out <threads json> [--t3 <program>] [--ssh <host>]
//   --projects  {projects: [{id, title}]}: the t3 command has no command that lists projects, so the ids come
//               from the last `t3_project_list` result that a chat saved. A project made after that file is
//               not listed: save the file again when a project is added.
//   --t3        the t3 program (default ~/.t3/bin/t3, a wrapper around the desktop app; the app must run)
//   --ssh       list another machine: runs `ssh <host> ~/.t3/bin/t3 ...` there
// A project that cannot be listed stops the run and writes no file, because the scan reads a chat that is
// missing from the list as closed. JP 2026-11-20: "is it using the t3 cli?" (the list was a model's job before).
import { execFileSync } from "node:child_process";
import { readFileSync, renameSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

const args = process.argv.slice(2);
const opt = (name) => (args.includes(name) ? args[args.indexOf(name) + 1] : undefined);
const projectsFile = opt("--projects");
const out = opt("--out");
if (!projectsFile || !out) { console.error("usage: list-chats.mjs --projects <projects json> --out <threads json> [--t3 <program>] [--ssh <host>]"); process.exit(2); }
const ssh = opt("--ssh");
const t3 = opt("--t3") ?? (ssh ? "~/.t3/bin/t3" : join(homedir(), ".t3/bin/t3"));
if (ssh && !/^[A-Za-z0-9._-]+$/.test(ssh)) { console.error("the --ssh host holds a character that is not allowed"); process.exit(2); }

const projects = JSON.parse(readFileSync(projectsFile, "utf8")).projects;
const threads = [];
for (const project of projects) {
  if (!/^[A-Za-z0-9:._-]+$/.test(project.id)) { console.error(`the project id holds a character that is not allowed: ${project.id}`); process.exit(1); }
  const list = ["thread", "list", "--project", project.id, "--json"];
  let text;
  try {
    text = ssh
      ? execFileSync("ssh", ["-o", "BatchMode=yes", "-o", "ConnectTimeout=10", ssh, `${t3} ${list.join(" ")}`], { encoding: "utf8", maxBuffer: 64 * 1024 * 1024, stdio: ["ignore", "pipe", "pipe"] })
      : execFileSync(t3, list, { encoding: "utf8", maxBuffer: 64 * 1024 * 1024, stdio: ["ignore", "pipe", "pipe"] });
  } catch (error) {
    console.error(`the project ${project.title ?? project.id} (${project.id}) could not be listed, so no file is written: ${String(error.stderr ?? error.message).trim().split("\n").pop()}`);
    process.exit(1);
  }
  for (const row of JSON.parse(text)) {
    // A fork of another chat, and a chat imported from another tool, have a parent and are still top-level
    // chats that JP talks to. Only a worker (any other relationship) is left out.
    if (row.settled || (row.relationshipToParent && row.relationshipToParent !== "fork")) continue;
    threads.push({ ...row, projectId: row.projectId ?? project.id });
  }
}
threads.sort((a, b) => (a.updatedAt < b.updatedAt ? 1 : -1));
const temp = `${out}.part`;
writeFileSync(temp, JSON.stringify({ projectId: null, threads, nextCursor: null, total: threads.length }));
renameSync(temp, out);
console.log(`${threads.length} open top-level chats of ${projects.length} projects -> ${out}`);
