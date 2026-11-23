#!/usr/bin/env node
/**
 * zadarma-mcp: an MCP server (stdio) for the Zadarma API. Packaged as a Claude
 * desktop extension (.mcpb); the desktop app passes the API key and secret in
 * as environment variables.
 */
import { serveStdio } from "@modelcontextprotocol/server/stdio";

import { createServer, SERVER_NAME } from "./server.js";

serveStdio(() => createServer(), {
  onerror: (error: Error) => {
    process.stderr.write(`${SERVER_NAME}: ${error.message}\n`);
  },
});
