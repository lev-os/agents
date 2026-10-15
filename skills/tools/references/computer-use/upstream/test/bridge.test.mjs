import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import path from "node:path";
import test from "node:test";

const testDir = path.dirname(fileURLToPath(import.meta.url));
const pluginRoot = path.resolve(testDir, "..");
const bridgePath = path.join(
  pluginRoot,
  "bin",
  "computer-use-mcp-bridge.mjs",
);
const fakeUpstreamPath = path.join(
  testDir,
  "fixtures",
  "fake-computer-use.mjs",
);

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

  return function waitFor(predicate, timeoutMs = 3000) {
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
          reject(new Error("timed out waiting for bridge output"));
        }, timeoutMs),
      };
      waiters.push(waiter);
    });
  };
}

function write(child, message) {
  child.stdin.write(`${JSON.stringify(message)}\n`);
}

test("injects elicitation support, auto-accepts, and preserves image blocks", async () => {
  const child = spawn(process.execPath, [bridgePath], {
    env: {
      ...process.env,
      COMPUTER_USE_CLIENT_PATH: fakeUpstreamPath,
      COMPUTER_USE_BRIDGE_DIRECT_LAUNCH: "1",
    },
    stdio: ["pipe", "pipe", "pipe"],
  });

  let stderr = "";
  child.stderr.setEncoding("utf8");
  child.stderr.on("data", (chunk) => {
    stderr += chunk;
  });

  const waitFor = createMessageReader(child.stdout);

  write(child, {
    jsonrpc: "2.0",
    id: 1,
    method: "initialize",
    params: {
      protocolVersion: "2025-11-25",
      capabilities: {},
      clientInfo: {
        name: "bridge-test",
        version: "1.0.0",
      },
    },
  });

  const initialized = await waitFor((message) => message.id === 1);
  assert.equal(initialized.result?.serverInfo?.name, "fake-computer-use");

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

  const tools = await waitFor((message) => message.id === 2);
  assert.deepEqual(
    tools.result?.tools?.map((tool) => tool.name),
    ["get_app_state"],
  );

  write(child, {
    jsonrpc: "2.0",
    id: 3,
    method: "tools/call",
    params: {
      name: "get_app_state",
      arguments: {
        app: "Fake App",
      },
    },
  });

  const result = await waitFor((message) => message.id === 3);
  assert.equal(result.result?.content?.[0]?.text, "auto-approved");
  assert.deepEqual(result.result?.content?.[1], {
    type: "image",
    data: "aGVsbG8=",
    mimeType: "image/jpeg",
  });

  child.stdin.end();
  const exit = await new Promise((resolve) => {
    child.on("close", (code, signal) => resolve({ code, signal }));
  });

  assert.deepEqual(exit, {
    code: 0,
    signal: null,
  });
  assert.equal(stderr, "");
});

test("releases the client when idle and relaunches it on demand", async () => {
  const child = spawn(process.execPath, [bridgePath], {
    env: {
      ...process.env,
      COMPUTER_USE_CLIENT_PATH: fakeUpstreamPath,
      COMPUTER_USE_BRIDGE_DIRECT_LAUNCH: "1",
      COMPUTER_USE_BRIDGE_IDLE_TIMEOUT_MS: "300",
      COMPUTER_USE_BRIDGE_DEBUG: "1",
    },
    stdio: ["pipe", "pipe", "pipe"],
  });

  let stderr = "";
  child.stderr.setEncoding("utf8");
  child.stderr.on("data", (chunk) => {
    stderr += chunk;
  });

  const waitFor = createMessageReader(child.stdout);

  write(child, {
    jsonrpc: "2.0",
    id: 1,
    method: "initialize",
    params: {
      protocolVersion: "2025-11-25",
      capabilities: {},
      clientInfo: {
        name: "bridge-test",
        version: "1.0.0",
      },
    },
  });

  const initialized = await waitFor((message) => message.id === 1);
  assert.equal(initialized.result?.serverInfo?.name, "fake-computer-use");

  write(child, {
    jsonrpc: "2.0",
    method: "notifications/initialized",
  });

  write(child, {
    jsonrpc: "2.0",
    id: 2,
    method: "tools/call",
    params: {
      name: "get_app_state",
      arguments: {
        app: "Fake App",
      },
    },
  });

  const first = await waitFor((message) => message.id === 2);
  assert.equal(first.result?.content?.[0]?.text, "auto-approved");

  await new Promise((resolve) => {
    setTimeout(resolve, 900);
  });
  assert.match(stderr, /releasing the Computer Use client/);

  write(child, {
    jsonrpc: "2.0",
    id: 3,
    method: "tools/call",
    params: {
      name: "get_app_state",
      arguments: {
        app: "Fake App",
      },
    },
  });

  const second = await waitFor((message) => message.id === 3);
  assert.equal(second.result?.content?.[0]?.text, "auto-approved");
  assert.deepEqual(second.result?.content?.[1], {
    type: "image",
    data: "aGVsbG8=",
    mimeType: "image/jpeg",
  });
  assert.match(stderr, /relaunched the Computer Use client/);

  child.stdin.end();
  const exit = await new Promise((resolve) => {
    child.on("close", (code, signal) => resolve({ code, signal }));
  });

  assert.deepEqual(exit, {
    code: 0,
    signal: null,
  });
});

test("recycles the client after a user-stopped app session", async () => {
  const child = spawn(process.execPath, [bridgePath], {
    env: {
      ...process.env,
      COMPUTER_USE_CLIENT_PATH: fakeUpstreamPath,
      COMPUTER_USE_BRIDGE_DIRECT_LAUNCH: "1",
      COMPUTER_USE_BRIDGE_IDLE_TIMEOUT_MS: "0",
      COMPUTER_USE_BRIDGE_DEBUG: "1",
    },
    stdio: ["pipe", "pipe", "pipe"],
  });

  let stderr = "";
  child.stderr.setEncoding("utf8");
  child.stderr.on("data", (chunk) => {
    stderr += chunk;
  });

  const waitFor = createMessageReader(child.stdout);

  write(child, {
    jsonrpc: "2.0",
    id: 1,
    method: "initialize",
    params: {
      protocolVersion: "2025-11-25",
      capabilities: {},
      clientInfo: {
        name: "bridge-test",
        version: "1.0.0",
      },
    },
  });
  await waitFor((message) => message.id === 1);
  write(child, {
    jsonrpc: "2.0",
    method: "notifications/initialized",
  });

  write(child, {
    jsonrpc: "2.0",
    id: 2,
    method: "tools/call",
    params: {
      name: "get_app_state",
      arguments: {
        app: "Stopped App",
      },
    },
  });

  const stopped = await waitFor((message) => message.id === 2);
  assert.match(
    stopped.result?.content?.[0]?.text ?? "",
    /explicitly stopped by the user/,
  );

  await new Promise((resolve) => {
    setTimeout(resolve, 300);
  });
  assert.match(stderr, /app session stopped by the user; releasing/);

  write(child, {
    jsonrpc: "2.0",
    id: 3,
    method: "tools/call",
    params: {
      name: "get_app_state",
      arguments: {
        app: "Fake App",
      },
    },
  });

  const recovered = await waitFor((message) => message.id === 3);
  assert.equal(recovered.result?.content?.[0]?.text, "auto-approved");
  assert.match(stderr, /relaunched the Computer Use client/);

  child.stdin.end();
  const exit = await new Promise((resolve) => {
    child.on("close", (code, signal) => resolve({ code, signal }));
  });

  assert.deepEqual(exit, {
    code: 0,
    signal: null,
  });
});
