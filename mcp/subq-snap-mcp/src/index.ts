#!/usr/bin/env node
/**
 * subq-snap-mcp: an MCP server (stdio) exposing the SubQ Snap decision model
 * as one tool, `decide`. Packaged as a Claude desktop extension (.mcpb); the
 * desktop app passes the user's settings in as environment variables.
 */
import { readFileSync } from "node:fs";

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

import { loadConfig } from "./config.js";
import { decideInputShape } from "./schema.js";
import { decide } from "./subq.js";

export const SERVER_NAME = "subq-snap-mcp";
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

const DESCRIPTION = [
  "Ask the SubQ Snap decision model fixed-choice questions about a piece of content.",
  "Returns a probability per answer instead of text: noul (yes/no) -> probability of yes;",
  "choice -> chosen option, probability per option and confidence; score -> level, probabilities and confidence.",
  "Put all questions about the same content into one call (1-128 questions).",
  "The state, questions and images are sent to SubQ (api.subq.ai) for processing.",
  "On any problem (no key, timeout, HTTP error) the result has status 'skipped' and a reason;",
  "the caller should then continue without it.",
].join(" ");

export function createServer(): McpServer {
  const server = new McpServer({ name: SERVER_NAME, version: SERVER_VERSION });
  server.registerTool(
    "decide",
    {
      title: "SubQ Snap decision",
      description: DESCRIPTION,
      inputSchema: decideInputShape,
      annotations: { readOnlyHint: true, openWorldHint: true },
    },
    async (args) => {
      const result = await decide(args, loadConfig());
      return {
        content: [{ type: "text", text: JSON.stringify(result) }],
        ...(result.status === "ok" ? {} : { isError: true }),
      };
    },
  );
  return server;
}

async function main(): Promise<void> {
  const server = createServer();
  await server.connect(new StdioServerTransport());
}

main().catch((error: unknown) => {
  const message = error instanceof Error ? (error.stack ?? error.message) : String(error);
  process.stderr.write(`${SERVER_NAME}: fatal: ${message}\n`);
  process.exit(1);
});
