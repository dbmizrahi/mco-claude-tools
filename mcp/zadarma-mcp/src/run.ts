/**
 * Runs one tool call: validate the action's params, apply the confirm gate,
 * check the settings, call Zadarma and format the result.
 */
import type { CallToolResult } from "@modelcontextprotocol/server";

import { callApi, type FetchLike } from "./client.js";
import type { ConfigResult } from "./config.js";
import { formatResult, MAX_OUTPUT_CHARS } from "./output.js";
import type { ToolDef } from "./tools/define.js";

export interface RunDeps {
  readonly loadConfig: () => ConfigResult;
  readonly fetch: FetchLike;
  readonly maxOutputChars?: number;
}

export interface ToolInput {
  readonly action: string;
  readonly params?: Readonly<Record<string, unknown>> | undefined;
  readonly confirm?: boolean | undefined;
}

function text(value: unknown, isError: boolean): CallToolResult {
  return {
    content: [{ type: "text", text: typeof value === "string" ? value : JSON.stringify(value) }],
    ...(isError ? { isError: true } : {}),
  };
}

export async function runTool(tool: ToolDef, input: ToolInput, deps: RunDeps): Promise<CallToolResult> {
  const action = tool.actions.find((a) => a.name === input.action);
  if (action === undefined) {
    return text(
      {
        status: "error",
        error: `Unknown action "${input.action}" for ${tool.name}.`,
        next_step: `Use one of: ${tool.actions.map((a) => a.name).join(", ")}.`,
      },
      true,
    );
  }

  const prepared = await action.prepare(input.params ?? {});
  if (!prepared.ok) {
    return text(
      { status: "error", error: prepared.error, next_step: `See the "${action.name}" entry in the ${tool.name} description.` },
      true,
    );
  }

  if (prepared.dangerous && input.confirm !== true) {
    return text(
      {
        status: "confirmation_required",
        changed: "nothing",
        tool: tool.name,
        action: action.name,
        would_call: `${prepared.request.method} ${prepared.request.path}`,
        params: prepared.preview,
        risk: action.risk,
        next_step:
          "Show this to the user and ask for explicit approval. Only after the user approves, call again with the same action and params and \"confirm\": true.",
      },
      false,
    );
  }

  const config = deps.loadConfig();
  if (!config.ok) {
    return text({ status: "error", error: config.error, next_step: "Fill in the settings, then try again." }, true);
  }

  const result = await callApi(config.config, prepared.request, deps.fetch);
  if (!result.ok) {
    return text(
      {
        status: "error",
        error: result.error,
        next_step: result.nextStep,
        ...(result.httpStatus === undefined ? {} : { http_status: result.httpStatus }),
        ...(result.rateLimitReset === undefined ? {} : { rate_limit_reset: result.rateLimitReset }),
      },
      true,
    );
  }
  return text(formatResult(result.data, action.narrowHint, deps.maxOutputChars ?? MAX_OUTPUT_CHARS), false);
}
