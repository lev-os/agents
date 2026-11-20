#!/usr/bin/env node
/**
 * Prints the state of a chat and the end of its last long reply (from "For you" on, when the reply has one),
 * through the t3 command line. It reads only and sends nothing. The check "is this card still asked" starts here.
 *
 * Usage: node chat-tail.mjs [--max <chars>] [--t3 <program>] [--ssh <host>] <thread id> [<thread id> ...]
 *   --max   the most characters of the reply to print (default 2000)
 *   --ssh   read a chat of another Mac: runs `ssh <host> ~/.t3/bin/t3 ...`
 * One JSON line for each chat: {thread_id, title, status, running, pending, updated_at, last_user, tail}
 * or {thread_id, error}. Exit 0 when every chat was read, 1 when one could not be read.
 */
import { execFileSync } from "node:child_process";
import { homedir } from "node:os";
import { join } from "node:path";

const args = process.argv.slice(2);
const flag = (name, fallback) => {
  const at = args.indexOf(name);
  if (at < 0) return fallback;
  const [, value] = args.splice(at, 2);
  return value;
};
const max = Number(flag("--max", "2000"));
const ssh = flag("--ssh", null);
const t3 = flag("--t3", ssh ? "~/.t3/bin/t3" : join(homedir(), ".t3/bin/t3"));
if (args.length === 0 || !Number.isFinite(max)) {
  console.error("usage: chat-tail.mjs [--max <chars>] [--t3 <program>] [--ssh <host>] <thread id> ...");
  process.exit(2);
}

const quote = (text) => `'${String(text).replaceAll("'", "'\\''")}'`;
const show = (id) => {
  const words = ["thread", "show", id, "--messages", "6", "--json"];
  const options = { encoding: "utf8", maxBuffer: 64 * 1024 * 1024, stdio: ["ignore", "pipe", "pipe"] };
  return ssh
    ? execFileSync("ssh", ["-o", "BatchMode=yes", "-o", "ConnectTimeout=8", ssh, [t3, ...words.map(quote)].join(" ")], options)
    : execFileSync(t3, words, options);
};

let failed = false;
for (const id of args) {
  try {
    const shown = JSON.parse(show(id));
    const messages = shown.messages ?? [];
    const lastUser = messages.findLast((m) => m.role === "user");
    const last = messages.findLast((m) => m.role === "assistant" && String(m.text ?? "").length > 200) ?? messages.at(-1);
    const text = String(last?.text ?? "");
    const at = text.lastIndexOf("**For you");
    console.log(JSON.stringify({
      thread_id: id,
      title: shown.thread?.title ?? null,
      status: shown.thread?.status ?? null,
      running: Boolean(shown.thread?.activeRunId),
      pending: shown.thread?.pendingRequestCount ?? null,
      updated_at: shown.thread?.updatedAt ?? null,
      last_user: lastUser ? String(lastUser.text).replace(/\s+/g, " ").slice(0, 200) : null,
      tail: (at >= 0 ? text.slice(at) : text.slice(-max)).slice(0, max),
    }));
  } catch (error) {
    failed = true;
    console.log(JSON.stringify({ thread_id: id, error: String(error.stderr || error.message).trim().split("\n")[0] }));
  }
}
process.exit(failed ? 1 : 0);
