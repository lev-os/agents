#!/usr/bin/env node

import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import path from "node:path";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const pluginRoot = path.resolve(scriptDir, "..");
const bridgePath =
  process.env.CLAUDE_CODEX_COMPUTER_USE_BRIDGE_PATH ??
  path.join(pluginRoot, "bin", "computer-use-mcp-bridge.mjs");

function createMessageReader(stream) {
  let buffer = "";
  const queued = [];
  const waiters = [];

  function deliver(message) {
    const waiterIndex = waiters.findIndex((waiter) =>
      waiter.predicate(message),
    );
    if (waiterIndex >= 0) {
      const [waiter] = waiters.splice(waiterIndex, 1);
      clearTimeout(waiter.timeout);
      waiter.resolve(message);
      return;
    }
    queued.push(message);
  }

  stream.setEncoding("utf8");
  stream.on("data", (chunk) => {
    buffer += chunk;
    for (;;) {
      const newlineIndex = buffer.indexOf("\n");
      if (newlineIndex < 0) {
        break;
      }
      const line = buffer.slice(0, newlineIndex).replace(/\r$/, "");
      buffer = buffer.slice(newlineIndex + 1);
      if (line) {
        deliver(JSON.parse(line));
      }
    }
  });

  return function waitFor(predicate, timeoutMs = 15000) {
    const queuedIndex = queued.findIndex(predicate);
    if (queuedIndex >= 0) {
      const [message] = queued.splice(queuedIndex, 1);
      return Promise.resolve(message);
    }

    return new Promise((resolve, reject) => {
      const waiter = {
        predicate,
        resolve,
        timeout: setTimeout(() => {
          const index = waiters.indexOf(waiter);
          if (index >= 0) {
            waiters.splice(index, 1);
          }
          reject(new Error("timed out waiting for Computer Use MCP output"));
        }, timeoutMs),
      };
      waiters.push(waiter);
    });
  };
}

function write(child, message) {
  child.stdin.write(`${JSON.stringify(message)}\n`);
}

const child = spawn(process.execPath, [bridgePath], {
  env: process.env,
  stdio: ["pipe", "pipe", "pipe"],
});
const waitFor = createMessageReader(child.stdout);
let stderr = "";

child.stderr.setEncoding("utf8");
child.stderr.on("data", (chunk) => {
  stderr += chunk;
});

try {
  write(child, {
    jsonrpc: "2.0",
    id: 1,
    method: "initialize",
    params: {
      protocolVersion: "2025-11-25",
      capabilities: {},
      clientInfo: {
        name: "claude-codex-computer-use-smoke-test",
        version: "0.1.0",
      },
    },
  });

  const initialized = await waitFor((message) => message.id === 1);
  assert.ok(initialized.result, initialized.error?.message);

  write(child, {
    jsonrpc: "2.0",
    method: "notifications/initialized",
  });

  write(child, {
    jsonrpc: "2.0",
    id: 2,
    method: "tools/list",
    params: {},
  });

  const listed = await waitFor((message) => message.id === 2);
  const toolNames = listed.result?.tools?.map((tool) => tool.name) ?? [];
  assert.ok(toolNames.includes("list_apps"));
  assert.ok(toolNames.includes("get_app_state"));
  assert.ok(toolNames.includes("press_key"));

  write(child, {
    jsonrpc: "2.0",
    id: 3,
    method: "tools/call",
    params: {
      name: "list_apps",
      arguments: {},
    },
  });

  const appsResult = await waitFor((message) => message.id === 3);
  assert.ok(
    appsResult.result && !appsResult.result.isError,
    `list_apps failed: ${JSON.stringify(appsResult)}`,
  );

  write(child, {
    jsonrpc: "2.0",
    id: 4,
    method: "tools/call",
    params: {
      name: "get_app_state",
      arguments: {
        app: "com.apple.calculator",
      },
    },
  });

  const stateResult = await waitFor((message) => message.id === 4);
  assert.ok(
    stateResult.result && !stateResult.result.isError,
    `get_app_state failed: ${JSON.stringify(stateResult)}`,
  );
  const content = stateResult.result.content ?? [];
  const textBlocks = content.filter((block) => block.type === "text");
  const imageBlocks = content.filter((block) => block.type === "image");
  assert.ok(textBlocks.length > 0);
  assert.ok(imageBlocks.length > 0);

  process.stdout.write(
    `${JSON.stringify(
      {
        protocolVersion: initialized.result.protocolVersion,
        toolCount: toolNames.length,
        listAppsSucceeded: true,
        appStateTextBlocks: textBlocks.length,
        appStateImageBlocks: imageBlocks.length,
        imageMimeTypes: imageBlocks.map((block) => block.mimeType),
      },
      null,
      2,
    )}\n`,
  );
} finally {
  child.stdin.end();
  const closed = await Promise.race([
    new Promise((resolve) => {
      child.once("close", resolve);
    }),
    new Promise((resolve) => {
      setTimeout(() => {
        child.kill("SIGTERM");
        resolve();
      }, 3000).unref();
    }),
  ]);
  void closed;
  if (stderr.trim()) {
    process.stderr.write(stderr);
  }
}
