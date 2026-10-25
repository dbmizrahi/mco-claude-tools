/**
 * SubQ Decisions API client. Never throws: every failure becomes a
 * `skipped` result, so the caller (the council skill) can carry on without
 * SubQ Snap.
 */
import type { SubqConfig } from "./config.js";
import { checkLimits, decideRequestSchema, type DecideRequest } from "./schema.js";

export interface DecideOk {
  readonly status: "ok";
  readonly model: string | null;
  readonly answers: Record<string, unknown>;
  readonly usage: unknown;
}

export interface DecideSkipped {
  readonly status: "skipped";
  readonly reason: string;
  readonly http_status?: number;
  readonly detail?: unknown;
}

export type DecideResult = DecideOk | DecideSkipped;

export type FetchLike = (input: string, init: RequestInit) => Promise<Response>;

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function skipped(reason: string, extra: { http_status?: number; detail?: unknown } = {}): DecideSkipped {
  return { status: "skipped", reason, ...extra };
}

const HTTP_REASONS: Readonly<Record<number, string>> = {
  400: "request rejected (over the token limit, or not accepted by the model)",
  401: "missing or invalid API key",
  402: "insufficient SubQ credits",
  403: "the API key cannot use this model",
  422: "invalid request (e.g. an invalid image, or not a decision model)",
  429: "SubQ rate limit exceeded",
  503: "SubQ is temporarily unavailable",
};

function httpReason(status: number): string {
  const known = HTTP_REASONS[status];
  if (known !== undefined) {
    return `SubQ API returned HTTP ${status}: ${known}`;
  }
  if (status >= 500) {
    return `SubQ API returned HTTP ${status}: server error`;
  }
  return `SubQ API returned HTTP ${status}`;
}

async function readJson(response: Response): Promise<unknown> {
  try {
    const text = await response.text();
    return text === "" ? null : (JSON.parse(text) as unknown);
  } catch {
    return null;
  }
}

function isTimeout(error: unknown): boolean {
  return error instanceof Error && (error.name === "TimeoutError" || error.name === "AbortError");
}

export async function decide(
  input: unknown,
  config: SubqConfig,
  fetchImpl: FetchLike = fetch,
): Promise<DecideResult> {
  if (config.apiKey === "") {
    return skipped("SubQ API key is not set (enter it in the extension's settings)");
  }

  const parsed = decideRequestSchema.safeParse(input);
  if (!parsed.success) {
    const first = parsed.error.issues[0];
    const where = first === undefined ? "" : ` at ${first.path.join(".") || "request"}`;
    return skipped(`invalid request${where}: ${first?.message ?? "schema mismatch"}`);
  }
  const request: DecideRequest = parsed.data;
  const limitError = checkLimits(request);
  if (limitError !== null) {
    return skipped(`invalid request: ${limitError}`);
  }

  const body: Record<string, unknown> = {
    model: config.model,
    state: request.state,
    questions: request.questions,
  };
  if (request.images !== undefined) {
    body["images"] = request.images;
  }

  let response: Response;
  try {
    response = await fetchImpl(config.apiUrl, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${config.apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(config.timeoutMs),
    });
  } catch (error: unknown) {
    if (isTimeout(error)) {
      return skipped(`SubQ API did not answer within ${config.timeoutMs / 1000} s`);
    }
    const message = error instanceof Error ? error.message : String(error);
    return skipped(`cannot reach the SubQ API: ${message}`);
  }

  const payload = await readJson(response);
  if (!response.ok) {
    const detail = isRecord(payload) ? payload["detail"] : undefined;
    return skipped(httpReason(response.status), {
      http_status: response.status,
      ...(detail === undefined ? {} : { detail }),
    });
  }
  if (!isRecord(payload) || !isRecord(payload["answers"])) {
    return skipped("SubQ API response has no answers");
  }
  const model = payload["model"];
  return {
    status: "ok",
    model: typeof model === "string" ? model : null,
    answers: payload["answers"],
    usage: payload["usage"] ?? null,
  };
}
