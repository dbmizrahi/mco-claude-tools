/** Test helpers: a stubbed fetch that records calls and returns canned responses. No network. */
import type { FetchLike } from "../src/client.js";
import type { ZadarmaConfig } from "../src/config.js";

export const TEST_CONFIG: ZadarmaConfig = {
  apiKey: "test-key",
  apiSecret: "test-secret",
  baseUrl: "https://api.zadarma.com",
  timeoutMs: 5000,
};

export interface RecordedCall {
  readonly url: string;
  readonly init: RequestInit;
}

export interface StubFetch {
  readonly fetch: FetchLike;
  readonly calls: RecordedCall[];
}

export function jsonResponse(body: unknown, status = 200, headers: Record<string, string> = {}): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", ...headers },
  });
}

export function stubFetch(respond: (call: RecordedCall) => Response | Promise<Response>): StubFetch {
  const calls: RecordedCall[] = [];
  return {
    calls,
    fetch: async (url, init) => {
      const call = { url, init };
      calls.push(call);
      return respond(call);
    },
  };
}

export function header(init: RequestInit, name: string): string | null {
  return new Headers(init.headers).get(name);
}
