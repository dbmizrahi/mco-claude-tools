/**
 * HTTP client for the Zadarma API: signing, form and multipart bodies,
 * parsing into `unknown`, error mapping and HTTP 429 handling. There is no
 * automatic retry loop; a rate-limited call returns the reset time instead.
 */
import type { ZadarmaConfig } from "./config.js";
import { flattenParams, type ParamRecord } from "./encode.js";
import { signRequest } from "./signature.js";
import type { UploadFile } from "./uploads.js";

export type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";

export interface ApiRequest {
  readonly method: HttpMethod;
  /** Path after the domain, with path parameters filled in, e.g. `/v1/sip/100/status/`. */
  readonly path: string;
  readonly params: ParamRecord;
  readonly files?: readonly UploadFile[];
}

export type FetchLike = (input: string, init: RequestInit) => Promise<Response>;

export type ApiResult =
  | { readonly ok: true; readonly data: unknown }
  | {
      readonly ok: false;
      readonly error: string;
      readonly nextStep: string;
      readonly httpStatus?: number;
      readonly rateLimitReset?: string;
    };

export function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function messageOf(data: unknown): string | undefined {
  if (isRecord(data)) {
    const message = data["message"];
    if (typeof message === "string" && message.trim() !== "") {
      return message.trim();
    }
  }
  return undefined;
}

function nextStepFor(status: number, message: string): string {
  const lower = message.toLowerCase();
  if (status === 401 || status === 403 || lower.includes("not authorized") || lower.includes("signature")) {
    return "Check the API key and secret in the Zadarma extension settings (Zadarma account > Settings > API).";
  }
  if (lower.includes("balance") || lower.includes("money") || lower.includes("funds")) {
    return "Top up the Zadarma balance, or ask the user how to proceed.";
  }
  if (status >= 500) {
    return "Zadarma had a server problem; try again later.";
  }
  if (status === 404) {
    return "Check the IDs in the request; the object may not exist on this account.";
  }
  return "Check the parameters against the action's description and the Zadarma API reference, then try again.";
}

function rateLimitReset(headers: Headers): { iso: string; seconds: number } | undefined {
  const raw = headers.get("x-ratelimit-reset");
  const epoch = raw === null ? Number.NaN : Number(raw);
  if (!Number.isFinite(epoch) || epoch <= 0) {
    return undefined;
  }
  const seconds = Math.max(0, Math.ceil(epoch - Date.now() / 1000));
  return { iso: new Date(epoch * 1000).toISOString(), seconds };
}

function buildBody(params: ParamRecord, files: readonly UploadFile[], query: string): { body: NonNullable<RequestInit["body"]>; contentType?: string } {
  if (files.length === 0) {
    return { body: query, contentType: "application/x-www-form-urlencoded" };
  }
  const form = new FormData();
  for (const [key, value] of flattenParams(params)) {
    form.append(key, value);
  }
  for (const file of files) {
    form.append(file.field, new Blob([file.bytes], { type: file.mimeType }), file.fileName);
  }
  // fetch sets multipart/form-data with the boundary itself.
  return { body: form };
}

/** Reads the response: JSON into `unknown`; anything else as metadata only (never file bytes). */
async function readPayload(response: Response): Promise<{ json: true; data: unknown } | { json: false; data: unknown }> {
  const contentType = response.headers.get("content-type") ?? "";
  if (contentType.includes("json") || contentType.startsWith("text/")) {
    const text = await response.text();
    try {
      const data: unknown = JSON.parse(text);
      return { json: true, data };
    } catch {
      return { json: false, data: { content_type: contentType || "unknown", text_preview: text.slice(0, 300) } };
    }
  }
  const bytes = (await response.arrayBuffer()).byteLength;
  return {
    json: false,
    data: {
      content_type: contentType || "unknown",
      bytes,
      content_disposition: response.headers.get("content-disposition") ?? undefined,
      note: "Binary content is not returned by this tool; open the file in the Zadarma or Teamsale web account.",
    },
  };
}

export async function callApi(config: ZadarmaConfig, request: ApiRequest, fetchImpl: FetchLike = fetch): Promise<ApiResult> {
  const params: ParamRecord = { ...request.params, format: "json" };
  const files = request.files ?? [];
  const signed = signRequest(request.path, params, config.apiKey, config.apiSecret);
  const headers: Record<string, string> = { Authorization: signed.authorization, Accept: "application/json" };

  let url = `${config.baseUrl}${request.path}`;
  const init: RequestInit = { method: request.method, headers, signal: AbortSignal.timeout(config.timeoutMs) };
  if (request.method === "GET") {
    url = signed.query === "" ? url : `${url}?${signed.query}`;
  } else {
    const { body, contentType } = buildBody(params, files, signed.query);
    init.body = body;
    if (contentType !== undefined) {
      headers["Content-Type"] = contentType;
    }
  }

  let response: Response;
  try {
    response = await fetchImpl(url, init);
  } catch (error: unknown) {
    const timedOut = error instanceof Error && (error.name === "TimeoutError" || error.name === "AbortError");
    const detail = error instanceof Error ? error.message : String(error);
    return {
      ok: false,
      error: timedOut ? `Zadarma did not answer within ${config.timeoutMs / 1000} seconds.` : `Could not reach api.zadarma.com: ${detail}`,
      nextStep: "Check the internet connection and try again.",
    };
  }

  if (response.status === 429) {
    const reset = rateLimitReset(response.headers);
    const when = reset === undefined ? "in about a minute" : `after ${reset.iso} (in ${reset.seconds} s)`;
    return {
      ok: false,
      httpStatus: 429,
      error: "Zadarma rate limit exceeded (100 requests per minute; statistics: 3 per minute).",
      nextStep: `Wait and try again ${when}. Do not retry in a loop.`,
      ...(reset === undefined ? {} : { rateLimitReset: reset.iso }),
    };
  }

  const payload = await readPayload(response);
  const zadarmaError = payload.json && isRecord(payload.data) && payload.data["status"] === "error";
  if (!response.ok || zadarmaError) {
    const message = messageOf(payload.data) ?? `HTTP ${response.status} ${response.statusText}`.trim();
    return {
      ok: false,
      httpStatus: response.status,
      error: `Zadarma error: ${message}`,
      nextStep: nextStepFor(response.status, message),
    };
  }
  return { ok: true, data: payload.data };
}
