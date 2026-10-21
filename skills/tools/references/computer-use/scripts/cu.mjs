#!/usr/bin/env node
// cu: one computer-use JavaScript session that stays open between shell calls, so variables
// (app, trees, parsed lists) carry over, as in Codex's own cua_repl.
//   cu.mjs js '<code>' | cu.mjs js --file f.mjs | cu.mjs js -   run code, print its output
//   cu.mjs reset                                                  drop all variables
//   cu.mjs stop                                                   end the session
//   cu.mjs engine                                                 print the engine in use
// Engine: Codex's cua_repl (OpenAI's engine, from the ChatGPT app) when installed, else open-computer-use
// (`ocu repl`). CU_ENGINE=codex|ocu picks one. Helpers from cu-helpers.js load into every session.
// The session starts on the first call and ends after 10 idle minutes. No window, no login item.
import { spawn } from "node:child_process";
import fs from "node:fs";
import net from "node:net";
import os from "node:os";
import path from "node:path";

const DIR = path.join(os.tmpdir(), "cu-session");
const SOCK = path.join(DIR, "cu.sock");
const IDLE_MS = 10 * 60 * 1000;
const CALL_MS = 110000; // stays inside a 120 s shell-tool limit
const [cmd, ...rest] = process.argv.slice(2);

if (cmd === "__serve") serve();
else if (["js", "reset", "stop", "engine"].includes(cmd)) client(cmd, rest);
else {
  console.error("usage: cu.mjs js '<code>' | js --file <path> | js - | reset | stop | engine");
  process.exit(2);
}

function codexServerConfig() {
  const root = path.join(os.homedir(), ".codex/plugins/cache/openai-bundled/unified-computer-use");
  let versions = [];
  try { versions = fs.readdirSync(root).sort(); } catch { return null; }
  for (const v of versions.reverse()) {
    try { return JSON.parse(fs.readFileSync(path.join(root, v, ".mcp.json"), "utf8")).mcpServers.cua_repl; } catch {}
  }
  return null;
}

const helpersSource = () => fs.readFileSync(new URL("./cu-helpers.js", import.meta.url), "utf8");

// Codex engine: talk MCP over stdio to cua_repl and call its `js` tool.
function codexEngine(cfg) {
  let p = null, buf = "", id = 0, waiters = {}, ready = null;
  const send = (m) => p.stdin.write(JSON.stringify(m) + "\n");
  const rpc = (method, params) => new Promise((res) => { const i = ++id; waiters[i] = res; send({ jsonrpc: "2.0", id: i, method, params }); });
  const start = () => {
    p = spawn(cfg.command, cfg.args || [], { env: { ...process.env, ...(cfg.env || {}) }, stdio: ["pipe", "pipe", "ignore"] });
    p.on("exit", () => { p = null; ready = null; for (const w of Object.values(waiters)) w({ error: { message: "engine exited" } }); waiters = {}; });
    p.stdout.on("data", (d) => {
      buf += d;
      let i;
      while ((i = buf.indexOf("\n")) >= 0) {
        const line = buf.slice(0, i); buf = buf.slice(i + 1);
        let m; try { m = JSON.parse(line); } catch { continue; }
        if (m.method === "elicitation/create") {
          // App-access approval ("Allow Computer Use to use Discord?"). Accepted here, as the
          // open-computer-use and songkeys paths do; the skill's rules decide what an agent may do.
          fs.appendFileSync(path.join(DIR, "approvals.log"), `${new Date().toISOString()} ${m.params?.message || ""}\n`);
          send({ jsonrpc: "2.0", id: m.id, result: { action: "accept", content: {} } });
        } else if (m.id && waiters[m.id]) { const w = waiters[m.id]; delete waiters[m.id]; w(m); }
      }
    });
    ready = (async () => {
      await rpc("initialize", { protocolVersion: "2025-06-18", capabilities: { elicitation: { form: {} } }, clientInfo: { name: "cu", version: "1" } });
      send({ jsonrpc: "2.0", method: "notifications/initialized" });
      // The first call must be a single entry point; it returns Codex's documentation. Keep it in a file.
      const first = await call("var __cuState = await cua.getState({ emit: false });", true);
      fs.writeFileSync(path.join(DIR, "codex-computer-use.md"), first);
      await call(helpersSource(), true);
    })();
  };
  const call = async (code, raw) => {
    const r = await rpc("tools/call", { name: "js", arguments: { code, timeout_ms: CALL_MS } });
    if (r.error) return `Error: ${r.error.message}`;
    const parts = [];
    for (const c of r.result?.content || []) {
      if (c.type === "text") parts.push(c.text);
      else if (c.type === "image") {
        fs.mkdirSync("/tmp/ocu-shots", { recursive: true });
        const f = `/tmp/ocu-shots/emitted-${Date.now()}.${(c.mimeType || "image/png").split("/")[1]}`;
        fs.writeFileSync(f, Buffer.from(c.data, "base64"));
        parts.push(`[image saved: ${f}]`);
      }
    }
    // save() inside the sandbox sends its text back between markers; write it to /tmp/ocu-out here.
    const text = parts.join("\n").replace(/<<CU_SAVE ([^>\n/]+)>>\n([\s\S]*?)\n<<CU_SAVE_END>>/g, (_, name, body) => {
      fs.mkdirSync("/tmp/ocu-out", { recursive: true });
      fs.writeFileSync(path.join("/tmp/ocu-out", name), body);
      return "";
    });
    return raw ? text : text.replace(/nodeRepl\.createElicitation is unavailable[^\n]*\n?/g, "");
  };
  return {
    name: "codex",
    async run(code) {
      if (!p) start();
      await ready;
      return (await call(code)).trim() + "\n";
    },
    async reset() { if (p) { await rpc("tools/call", { name: "js_reset", arguments: {} }); ready = (async () => { await call("var __cuState = await cua.getState({ emit: false });", true); await call(helpersSource(), true); })(); } },
    stop() { try { p && p.kill(); } catch {} },
  };
}

// open-computer-use engine: a piped `ocu repl`.
function ocuEngine() {
  let repl = null, out = "";
  const loadHelpers = () => repl.stdin.write(`.editor\n${helpersSource()}\n.end\n`);
  const start = () => {
    // ACTION_READ_BACK=0: an action no longer rereads the window (about 6 s in Discord, 0.1 s without).
    repl = spawn("ocu", ["repl", "--timeout", String(CALL_MS)], {
      stdio: ["pipe", "pipe", "pipe"],
      env: { OPEN_COMPUTER_USE_ACTION_READ_BACK: "0", ...process.env },
    });
    repl.stdout.on("data", (d) => { out += d; });
    repl.stderr.on("data", (d) => { out += d; });
    repl.on("exit", () => { repl = null; });
    loadHelpers();
  };
  return {
    name: "ocu",
    run: (code) => new Promise((resolve) => {
      if (!repl) start();
      const mark = `__CU_END_${Date.now()}_${Math.random().toString(36).slice(2)}__`;
      out = "";
      repl.stdin.write(`.editor\ntry {\n${code}\n} catch (e) { nodeRepl.write("Error: " + (e && e.stack || e)); }\n.end\nnodeRepl.write(${JSON.stringify(mark)})\n`);
      const t0 = Date.now();
      const tick = setInterval(() => {
        const i = out.indexOf(mark);
        if (i >= 0 || !repl || Date.now() - t0 > CALL_MS + 5000) {
          clearInterval(tick);
          if (/session reset/.test(out) && repl) loadHelpers();
          resolve(cleanOcu(i >= 0 ? out.slice(0, i) : out + (repl ? "\n[cu: timed out after 110 s; split the work into shorter calls]" : "\n[cu: session ended]")));
        }
      }, 25);
    }),
    async reset() { try { repl && repl.stdin.end(".exit\n"); } catch {} repl = null; },
    stop() { try { repl && repl.stdin.end(".exit\n"); } catch {} },
  };
}

function cleanOcu(s) {
  // Drop REPL prompts, empty lines, "(no output)", and the API summary the REPL prints when it starts.
  const out = [];
  let inSummary = false;
  for (const l of s.split("\n")) {
    if (/^## Open Computer Use JavaScript API/.test(l)) { inSummary = true; continue; }
    if (inSummary) { if (/^After actions,/.test(l)) inSummary = false; continue; }
    if (/^(> |\.\.\. |\/\/ Entering editor mode)/.test(l) || /^(> |\.\.\. )*$/.test(l) || l.trim() === "(no output)") continue;
    out.push(l);
  }
  return (out.join("\n").trim() || "(no output)") + "\n";
}

// Long output (a big window's tree) goes to a file; the caller sees the start and the path.
function cap(text, max = 20000, head = 4000) {
  if (text.length <= max) return text;
  fs.mkdirSync("/tmp/ocu-out", { recursive: true });
  const file = `/tmp/ocu-out/output-${Date.now()}.txt`;
  fs.writeFileSync(file, text);
  return `${text.slice(0, head)}\n[cu: output was ${Math.round(text.length / 1024)} KB; full text in ${file}. Filter in the session (grep) instead of printing whole trees.]\n`;
}

function serve() {
  fs.mkdirSync(DIR, { recursive: true });
  try { fs.unlinkSync(SOCK); } catch {}
  const want = process.env.CU_ENGINE;
  const cfg = want === "ocu" ? null : codexServerConfig();
  const engine = cfg ? codexEngine(cfg) : ocuEngine();
  let queue = Promise.resolve(), idle;
  const touch = () => { clearTimeout(idle); idle = setTimeout(shutdown, IDLE_MS); };
  const shutdown = () => { engine.stop(); server.close(); try { fs.unlinkSync(SOCK); } catch {} process.exit(0); };
  const server = net.createServer({ allowHalfOpen: true }, (c) => {
    let buf = "";
    c.on("data", (d) => { buf += d; });
    c.on("end", () => {
      touch();
      const req = JSON.parse(buf);
      if (req.cmd === "stop") { c.end("stopped\n"); return shutdown(); }
      if (req.cmd === "engine") { c.end(engine.name + "\n"); return; }
      if (req.cmd === "reset") { queue = queue.then(() => engine.reset()).then(() => c.end("reset\n")); return; }
      queue = queue.then(() => engine.run(req.code).then((r) => c.end(cap(r)), (e) => c.end(`Error: ${e}\n`)));
    });
  });
  server.listen(SOCK, touch);
}

async function client(cmd, args) {
  let code = "";
  if (cmd === "js") {
    if (args[0] === "--file") code = fs.readFileSync(args[1], "utf8");
    else if (args[0] === "-") code = fs.readFileSync(0, "utf8");
    else code = args.join(" ");
  }
  const connect = () => new Promise((res, rej) => {
    const c = net.connect({ path: SOCK, allowHalfOpen: true }, () => res(c));
    c.on("error", rej);
  });
  let c;
  try { c = await connect(); }
  catch {
    if (cmd === "stop" || cmd === "reset") { console.log("no session"); return; }
    const d = spawn(process.execPath, [process.argv[1], "__serve"], { detached: true, stdio: "ignore", env: process.env });
    d.unref();
    for (let i = 0; i < 100 && !c; i++) {
      await new Promise((r) => setTimeout(r, 100));
      try { c = await connect(); } catch {}
    }
    if (!c) { console.error("cu: session did not start"); process.exit(1); }
  }
  let out = "";
  c.on("data", (d) => { out += d; });
  c.on("end", () => process.stdout.write(out));
  c.end(JSON.stringify({ cmd, code }));
}
