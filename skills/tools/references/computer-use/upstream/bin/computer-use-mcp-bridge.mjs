#!/usr/bin/env node

import { spawn } from "node:child_process";
import { constants as fsConstants } from "node:fs";
import { access } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

const DEBUG = process.env.COMPUTER_USE_BRIDGE_DEBUG === "1";
const SYNTHETIC_INIT_ID = "computer-use-bridge/reinitialize";
const DEFAULT_IDLE_TIMEOUT_MS = 60000;
const SESSION_STOPPED_MARKER = "explicitly stopped by the user for this turn";

function debug(message) {
  if (DEBUG) {
    process.stderr.write(`[computer-use-bridge] ${message}\n`);
  }
}

function isObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function resolveUpstreamPath() {
  const override = process.env.COMPUTER_USE_CLIENT_PATH?.trim();
  if (override) {
    return path.resolve(override);
  }

  const configuredCodexHome = process.env.CODEX_HOME?.trim();
  const codexHome = configuredCodexHome || path.join(os.homedir(), ".codex");

  return path.join(
    codexHome,
    "computer-use",
    "Codex Computer Use.app",
    "Contents",
    "SharedSupport",
    "SkyComputerUseClient.app",
    "Contents",
    "MacOS",
    "SkyComputerUseClient",
  );
}

async function resolveTrustedLauncherPath() {
  const override = process.env.COMPUTER_USE_CODEX_LAUNCHER_PATH?.trim();
  const candidates = [
    override,
    "/Applications/ChatGPT.app/Contents/Resources/codex",
    "/Applications/Codex.app/Contents/Resources/codex",
  ].filter(Boolean);

  for (const candidate of candidates) {
    try {
      await access(candidate, fsConstants.X_OK);
      return candidate;
    } catch {
      // Try the next signed Codex launcher location.
    }
  }

  throw new Error(
    `OpenAI's signed Codex launcher was not found. Checked: ${candidates.join(
      ", ",
    )}`,
  );
}

function resolveIdleTimeout() {
  const raw = process.env.COMPUTER_USE_BRIDGE_IDLE_TIMEOUT_MS?.trim();
  if (!raw) {
    return DEFAULT_IDLE_TIMEOUT_MS;
  }
  const parsed = Number(raw);
  if (!Number.isFinite(parsed) || parsed < 0) {
    return DEFAULT_IDLE_TIMEOUT_MS;
  }
  return parsed;
}

function withElicitationCapability(message) {
  if (!isObject(message) || message.method !== "initialize") {
    return null;
  }

  const params = isObject(message.params) ? message.params : {};
  const capabilities = isObject(params.capabilities)
    ? { ...params.capabilities }
    : {};
  const existingElicitation = isObject(capabilities.elicitation)
    ? { ...capabilities.elicitation }
    : {};
  const protocolVersion =
    typeof params.protocolVersion === "string" ? params.protocolVersion : "";

  if (protocolVersion >= "2025-11-25") {
    existingElicitation.form = isObject(existingElicitation.form)
      ? existingElicitation.form
      : {};
  }

  capabilities.elicitation = existingElicitation;

  return {
    ...message,
    params: {
      ...params,
      capabilities,
    },
  };
}

function parseJson(line) {
  try {
    return JSON.parse(line);
  } catch {
    return null;
  }
}

function pumpJsonLines(stream, onLine, onEnd) {
  let buffer = "";
  stream.setEncoding("utf8");

  stream.on("data", (chunk) => {
    buffer += chunk;

    for (;;) {
      const newlineIndex = buffer.indexOf("\n");
      if (newlineIndex < 0) {
        break;
      }

      let line = buffer.slice(0, newlineIndex);
      buffer = buffer.slice(newlineIndex + 1);
      if (line.endsWith("\r")) {
        line = line.slice(0, -1);
      }
      if (line.length > 0) {
        onLine(line);
      }
    }
  });

  stream.on("end", () => {
    let line = buffer;
    if (line.endsWith("\r")) {
      line = line.slice(0, -1);
    }
    if (line.length > 0) {
      onLine(line);
    }
    onEnd?.();
  });
}

function writeJsonLine(stream, value) {
  if (!stream.destroyed && stream.writable) {
    stream.write(`${JSON.stringify(value)}\n`);
  }
}

const upstreamPath = resolveUpstreamPath();
const directLaunch =
  process.env.COMPUTER_USE_BRIDGE_DIRECT_LAUNCH === "1";

try {
  await access(upstreamPath, fsConstants.X_OK);
} catch {
  process.stderr.write(
    `Computer Use client is missing or not executable: ${upstreamPath}\n`,
  );
  process.exit(1);
}

let launchCommand = upstreamPath;
let launchArgs = ["mcp"];

if (!directLaunch) {
  try {
    launchCommand = await resolveTrustedLauncherPath();
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exit(1);
  }

  const sandboxState = JSON.stringify({
    permissionProfile: {
      type: "disabled",
      fileSystem: {
        type: "unrestricted",
      },
    },
    sandboxCwd: pathToFileURL(process.cwd()).href,
  });
  launchArgs = [
    "sandbox",
    "--sandbox-state-json",
    sandboxState,
    "--",
    upstreamPath,
    "mcp",
  ];
}

const idleTimeoutMs = resolveIdleTimeout();

// The Computer Use service treats a connected client as an active hold on the
// controlled applications and only releases them when the client process
// exits. Claude Code keeps plugin MCP servers alive for the whole session, so
// the bridge releases the client after an idle period and relaunches it on
// demand, replaying the recorded initialize handshake.
let upstream = null;
let state = "down"; // down | starting | ready
let stopping = false;
let storedInitialize = null;
let clientInitialized = false;
let pendingRequests = new Set();
let handshakeQueue = [];
let lastActivity = Date.now();

function touch() {
  lastActivity = Date.now();
}

function isRequest(message) {
  return (
    isObject(message) &&
    typeof message.method === "string" &&
    Object.hasOwn(message, "id")
  );
}

function failRequest(id, message) {
  writeJsonLine(process.stdout, {
    jsonrpc: "2.0",
    id,
    error: {
      code: -32000,
      message,
    },
  });
}

function failPendingWork(reason) {
  for (const id of pendingRequests) {
    failRequest(id, reason);
  }
  pendingRequests.clear();

  const queued = handshakeQueue;
  handshakeQueue = [];
  for (const item of queued) {
    if (isRequest(item.message)) {
      failRequest(item.message.id, reason);
    }
  }
}

function forwardToUpstream(line, message) {
  if (!upstream || upstream.stdin.destroyed || !upstream.stdin.writable) {
    if (isRequest(message)) {
      failRequest(
        message.id,
        "The Computer Use client is not running. Retry the request.",
      );
    }
    return;
  }
  upstream.stdin.write(`${line}\n`);
  if (isRequest(message)) {
    pendingRequests.add(message.id);
  }
  touch();
}

function killTree(child, signal) {
  // The launcher runs the Computer Use client as a grandchild. Signal the
  // launcher's process group so a wedged client cannot outlive a release.
  try {
    process.kill(-child.pid, signal);
  } catch {
    child.kill(signal);
  }
}

function spawnUpstream() {
  debug(`starting ${launchCommand} ${launchArgs.join(" ")}`);

  const child = spawn(launchCommand, launchArgs, {
    env: process.env,
    stdio: ["pipe", "pipe", "pipe"],
    detached: true,
  });
  upstream = child;

  let gone = false;
  const markGone = (code, signal) => {
    if (gone) {
      return;
    }
    gone = true;
    if (upstream !== child) {
      debug(
        `released client exited (code=${String(code)}, signal=${String(
          signal,
        )})`,
      );
      return;
    }
    upstream = null;
    state = "down";

    if (stopping) {
      debug(`upstream closed (code=${String(code)}, signal=${String(signal)})`);
      if (signal) {
        process.exitCode = signal === "SIGINT" ? 130 : 1;
      } else {
        process.exitCode = code ?? 0;
      }
      process.stdout.end();
      return;
    }

    debug(
      `upstream exited unexpectedly (code=${String(code)}, signal=${String(
        signal,
      )}); it will be relaunched on demand`,
    );
    failPendingWork(
      "The Computer Use client exited unexpectedly. Retry the request.",
    );
  };

  child.stderr.pipe(process.stderr);

  child.on("error", (error) => {
    process.stderr.write(
      `Failed to start the Computer Use MCP client: ${error.message}\n`,
    );
    markGone(null, null);
  });

  child.stdin.on("error", (error) => {
    if (error.code !== "EPIPE") {
      process.stderr.write(
        `Computer Use MCP stdin failed: ${error.message}\n`,
      );
    }
  });

  child.on("close", (code, signal) => {
    markGone(code, signal);
  });

  pumpJsonLines(child.stdout, (line) => {
    onUpstreamLine(child, line);
  });

  touch();
  return child;
}

function relaunchUpstream() {
  spawnUpstream();
  state = "starting";
  writeJsonLine(upstream.stdin, {
    ...storedInitialize,
    id: SYNTHETIC_INIT_ID,
  });
  debug("relaunching the Computer Use client");
}

function releaseUpstream(reason) {
  const child = upstream;
  upstream = null;
  state = "down";
  debug(`${reason}; releasing the Computer Use client`);
  failPendingWork(
    "The Computer Use client was recycled while the request was in flight. Retry the request.",
  );
  killTree(child, "SIGTERM");
  setTimeout(() => {
    if (child.exitCode === null && child.signalCode === null) {
      killTree(child, "SIGKILL");
    }
  }, 3000).unref();
}

function isSessionStoppedResult(message) {
  if (
    !isObject(message) ||
    !Object.hasOwn(message, "id") ||
    Object.hasOwn(message, "method")
  ) {
    return false;
  }
  const content = message.result?.content;
  if (!Array.isArray(content)) {
    return false;
  }
  return content.some(
    (block) =>
      isObject(block) &&
      block.type === "text" &&
      typeof block.text === "string" &&
      block.text.includes(SESSION_STOPPED_MARKER),
  );
}

function onUpstreamLine(child, line) {
  if (upstream !== child) {
    return;
  }

  const message = parseJson(line);

  if (isObject(message) && message.id === SYNTHETIC_INIT_ID) {
    if (message.error) {
      debug(
        `relaunch initialize failed: ${String(message.error?.message ?? "")}`,
      );
      failPendingWork(
        "The Computer Use client could not be reinitialized. Retry the request.",
      );
      releaseUpstream("relaunch failed");
      return;
    }
    if (clientInitialized) {
      writeJsonLine(child.stdin, {
        jsonrpc: "2.0",
        method: "notifications/initialized",
      });
    }
    state = "ready";
    const queued = handshakeQueue;
    handshakeQueue = [];
    for (const item of queued) {
      forwardToUpstream(item.line, item.message);
    }
    debug("relaunched the Computer Use client");
    touch();
    return;
  }

  if (
    isObject(message) &&
    message.method === "elicitation/create" &&
    Object.hasOwn(message, "id")
  ) {
    debug(
      `auto-accepted elicitation: ${
        typeof message.params?.message === "string"
          ? message.params.message
          : "Computer Use request"
      }`,
    );
    writeJsonLine(child.stdin, {
      jsonrpc: "2.0",
      id: message.id,
      result: {
        action: "accept",
        content: {},
      },
    });
    touch();
    return;
  }

  if (
    isObject(message) &&
    Object.hasOwn(message, "id") &&
    !Object.hasOwn(message, "method")
  ) {
    pendingRequests.delete(message.id);
  }

  touch();
  if (!process.stdout.destroyed && process.stdout.writable) {
    process.stdout.write(`${line}\n`);
  }

  // The service latches a user-initiated stop for the rest of the client's
  // "turn", but a long-lived bridge client never starts a new turn. Recycle
  // the client so the next request begins a fresh turn.
  if (isSessionStoppedResult(message)) {
    releaseUpstream("app session stopped by the user");
  }
}

process.stdout.on("error", (error) => {
  if (error.code === "EPIPE") {
    stopping = true;
    if (upstream) {
      killTree(upstream, "SIGTERM");
    } else {
      process.exit(1);
    }
    return;
  }
  throw error;
});

pumpJsonLines(
  process.stdin,
  (line) => {
    const message = parseJson(line);
    const rewritten = withElicitationCapability(message);

    if (rewritten !== null) {
      debug("advertised form elicitation support");
      storedInitialize = rewritten;
      if (state === "down") {
        spawnUpstream();
        state = "ready";
      }
      if (state === "starting") {
        handshakeQueue.push({
          line: JSON.stringify(rewritten),
          message: rewritten,
        });
        return;
      }
      forwardToUpstream(JSON.stringify(rewritten), rewritten);
      return;
    }

    if (isRequest(message) && message.method === "ping") {
      writeJsonLine(process.stdout, {
        jsonrpc: "2.0",
        id: message.id,
        result: {},
      });
      return;
    }

    if (isObject(message) && message.method === "notifications/initialized") {
      clientInitialized = true;
    }

    if (state === "ready") {
      forwardToUpstream(line, message);
      return;
    }

    if (state === "starting") {
      handshakeQueue.push({ line, message });
      return;
    }

    if (isRequest(message)) {
      if (!storedInitialize) {
        failRequest(
          message.id,
          "The MCP session is not initialized.",
        );
        return;
      }
      handshakeQueue.push({ line, message });
      relaunchUpstream();
      return;
    }

    if (isObject(message) && typeof message.method === "string") {
      debug(`dropped ${message.method} while the client is released`);
    }
  },
  () => {
    stopping = true;
    if (upstream) {
      upstream.stdin.end();
    } else {
      process.exitCode = process.exitCode ?? 0;
      process.stdout.end();
    }
  },
);

if (idleTimeoutMs > 0) {
  const checkInterval = Math.max(
    50,
    Math.min(1000, Math.floor(idleTimeoutMs / 2)),
  );
  setInterval(() => {
    if (state !== "ready" || stopping || !storedInitialize) {
      return;
    }
    if (pendingRequests.size > 0) {
      return;
    }
    if (Date.now() - lastActivity < idleTimeoutMs) {
      return;
    }
    releaseUpstream("idle timeout reached");
  }, checkInterval).unref();
}

for (const signal of ["SIGINT", "SIGTERM", "SIGHUP"]) {
  process.once(signal, () => {
    if (stopping) {
      return;
    }
    stopping = true;
    debug(`forwarding ${signal}`);
    if (upstream) {
      killTree(upstream, signal);
    } else {
      process.exitCode = signal === "SIGINT" ? 130 : 1;
      process.exit();
    }
  });
}
