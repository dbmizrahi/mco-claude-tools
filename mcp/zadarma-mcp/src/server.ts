/** Builds the MCP server with every Zadarma tool registered. */
import { readFileSync } from "node:fs";

import { McpServer } from "@modelcontextprotocol/server";
import { z } from "zod";

import { loadConfig } from "./config.js";
import { runTool, type RunDeps } from "./run.js";
import { ALL_TOOLS } from "./tools/index.js";
import type { ToolDef } from "./tools/define.js";

export const SERVER_NAME = "zadarma-mcp";
const FALLBACK_VERSION = "0.0.0";

/** The version lives in package.json only (release-please bumps it there). */
function readVersion(): string {
  try {
    const raw: unknown = JSON.parse(readFileSync(new URL("../package.json", import.meta.url), "utf8"));
    if (typeof raw === "object" && raw !== null && "version" in raw && typeof raw.version === "string") {
      return raw.version;
    }
  } catch {
    // fall through to the fallback
  }
  return FALLBACK_VERSION;
}

export const SERVER_VERSION = readVersion();

export const defaultDeps: RunDeps = { loadConfig: () => loadConfig(), fetch: (input, init) => fetch(input, init) };

export function toolInputSchema(tool: ToolDef) {
  const [first, ...rest] = tool.actions.map((a) => a.name);
  if (first === undefined) {
    throw new Error(`tool ${tool.name} has no actions`);
  }
  return z.object({
    action: z.enum([first, ...rest]).describe("Which action to run; see the tool description."),
    params: z
      .record(z.string(), z.unknown())
      .optional()
      .describe("Parameters of the chosen action, as listed in the tool description."),
    confirm: z
      .boolean()
      .optional()
      .describe("Set true only after the user explicitly approved this exact action in the conversation."),
  });
}

export function createServer(deps: RunDeps = defaultDeps): McpServer {
  const server = new McpServer({ name: SERVER_NAME, version: SERVER_VERSION });
  for (const tool of ALL_TOOLS) {
    server.registerTool(
      tool.name,
      {
        title: tool.title,
        description: tool.description,
        inputSchema: toolInputSchema(tool),
        annotations: { ...tool.annotations },
      },
      async (args) => runTool(tool, args, deps),
    );
  }
  return server;
}
