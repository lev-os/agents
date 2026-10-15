#!/usr/bin/env node

let buffer = "";
let pendingToolCallId;

function write(message) {
  process.stdout.write(`${JSON.stringify(message)}\n`);
}

function fail(id, message) {
  write({
    jsonrpc: "2.0",
    id,
    error: {
      code: -32602,
      message,
    },
  });
}

function handle(message) {
  if (message.method === "initialize") {
    const elicitation = message.params?.capabilities?.elicitation;
    const protocolVersion = message.params?.protocolVersion;
    if (
      !elicitation ||
      (protocolVersion >= "2025-11-25" &&
        (typeof elicitation.form !== "object" ||
          elicitation.form === null))
    ) {
      fail(message.id, "bridge did not advertise elicitation support");
      return;
    }

    write({
      jsonrpc: "2.0",
      id: message.id,
      result: {
        protocolVersion,
        capabilities: {
          tools: {},
        },
        serverInfo: {
          name: "fake-computer-use",
          version: "1.0.0",
        },
      },
    });
    return;
  }

  if (message.method === "notifications/initialized") {
    return;
  }

  if (message.method === "tools/list") {
    write({
      jsonrpc: "2.0",
      id: message.id,
      result: {
        tools: [
          {
            name: "get_app_state",
            description: "Return a fake state and image.",
            inputSchema: {
              type: "object",
              properties: {
                app: {
                  type: "string",
                },
              },
              required: ["app"],
            },
          },
        ],
      },
    });
    return;
  }

  if (message.method === "tools/call") {
    if (message.params?.arguments?.app === "Stopped App") {
      write({
        jsonrpc: "2.0",
        id: message.id,
        result: {
          content: [
            {
              type: "text",
              text: "This application session has been explicitly stopped by the user for this turn. Stop your work and send a final message noting they stopped the session and you're ready to continue if they want you to. Computer Use can be used again in the next assistant turn.",
            },
          ],
        },
      });
      return;
    }

    pendingToolCallId = message.id;
    const request = JSON.stringify({
      jsonrpc: "2.0",
      id: "approval-1",
      method: "elicitation/create",
      params: {
        _meta: {
          persist: ["always"],
        },
        message: "Allow ChatGPT to use Fake App?",
        requestedSchema: {
          type: "object",
          properties: {},
        },
      },
    });

    const splitAt = Math.floor(request.length / 2);
    process.stdout.write(request.slice(0, splitAt));
    setImmediate(() => {
      process.stdout.write(`${request.slice(splitAt)}\n`);
    });
    return;
  }

  if (message.id === "approval-1") {
    if (
      message.result?.action !== "accept" ||
      typeof message.result?.content !== "object" ||
      message.result.content === null
    ) {
      fail(pendingToolCallId, "bridge did not accept the elicitation");
      pendingToolCallId = undefined;
      return;
    }

    write({
      jsonrpc: "2.0",
      id: pendingToolCallId,
      result: {
        content: [
          {
            type: "text",
            text: "auto-approved",
          },
          {
            type: "image",
            data: "aGVsbG8=",
            mimeType: "image/jpeg",
          },
        ],
      },
    });
    pendingToolCallId = undefined;
  }
}

process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => {
  buffer += chunk;
  for (;;) {
    const newlineIndex = buffer.indexOf("\n");
    if (newlineIndex < 0) {
      break;
    }
    const line = buffer.slice(0, newlineIndex).replace(/\r$/, "");
    buffer = buffer.slice(newlineIndex + 1);
    if (line) {
      handle(JSON.parse(line));
    }
  }
});
