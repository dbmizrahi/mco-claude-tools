import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { DEFAULT_API_URL, DEFAULT_MODEL, DEFAULT_TIMEOUT_SECONDS, loadConfig, type SubqConfig } from "../src/config.js";
import { decide, type DecideResult, type FetchLike } from "../src/subq.js";

const config: SubqConfig = {
  apiKey: "test-key",
  apiUrl: "https://example.invalid/v1/systemone",
  model: "subq-snap-1.1",
  timeoutMs: 1000,
};

const request = {
  state: "Should we move from ECS to EKS?",
  questions: {
    worthy: { type: "noul", instructions: "Is this a real decision?" },
    kind: { type: "choice", criteria: { technical: "how to build", business_value: null } },
  },
};

interface Captured {
  url: string;
  init: RequestInit;
}

function jsonResponse(status: number, body: unknown): Response {
  return new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
}

function stubFetch(status: number, body: unknown, captured?: Captured[]): FetchLike {
  return async (url, init) => {
    captured?.push({ url, init });
    return jsonResponse(status, body);
  };
}

function assertSkipped(result: DecideResult, pattern: RegExp): void {
  assert.equal(result.status, "skipped");
  if (result.status === "skipped") {
    assert.match(result.reason, pattern);
  }
}

describe("decide", () => {
  it("returns answers and sends the documented request", async () => {
    const captured: Captured[] = [];
    const answers = { worthy: { type: "noul", noul: 0.9 } };
    const result = await decide(
      request,
      config,
      stubFetch(200, { model: "subq-snap-1.1", answers, usage: { input_tokens: 12, output_tokens: 0 } }, captured),
    );
    assert.deepEqual(result, {
      status: "ok",
      model: "subq-snap-1.1",
      answers,
      usage: { input_tokens: 12, output_tokens: 0 },
    });
    const call = captured[0];
    assert.ok(call);
    assert.equal(call.url, config.apiUrl);
    assert.equal(call.init.method, "POST");
    const headers = new Headers(call.init.headers);
    assert.equal(headers.get("Authorization"), "Bearer test-key");
    const sent: unknown = JSON.parse(String(call.init.body));
    assert.deepEqual(sent, { model: "subq-snap-1.1", ...request });
  });

  it("skips without calling the API when the key is missing", async () => {
    let called = false;
    const result = await decide(request, { ...config, apiKey: "" }, async () => {
      called = true;
      return jsonResponse(200, {});
    });
    assertSkipped(result, /API key is not set/);
    assert.equal(called, false);
  });

  for (const status of [400, 401, 402, 403, 422, 429, 500, 503]) {
    it(`maps HTTP ${status} to skipped with status and detail`, async () => {
      const detail = { error_type: "validation_error", message: "nope" };
      const result = await decide(request, config, stubFetch(status, { detail }));
      assertSkipped(result, new RegExp(`HTTP ${status}`));
      if (result.status === "skipped") {
        assert.equal(result.http_status, status);
        assert.deepEqual(result.detail, detail);
      }
    });
  }

  it("skips on timeout", async () => {
    // AbortSignal.timeout uses an unref'd timer; a ref'd one keeps the test
    // process alive until the abort fires (a real server stays alive on stdio).
    const slow: FetchLike = (_url, init) =>
      new Promise<Response>((_resolve, reject) => {
        const keepAlive = setTimeout(() => reject(new Error("abort never fired")), 5000);
        init.signal?.addEventListener("abort", () => {
          clearTimeout(keepAlive);
          reject(init.signal?.reason);
        });
      });
    const result = await decide(request, { ...config, timeoutMs: 50 }, slow);
    assertSkipped(result, /did not answer within 0.05 s/);
  });

  it("skips on a network error", async () => {
    const result = await decide(request, config, async () => {
      throw new TypeError("fetch failed");
    });
    assertSkipped(result, /cannot reach the SubQ API: fetch failed/);
  });

  it("skips when the response has no answers", async () => {
    assertSkipped(await decide(request, config, stubFetch(200, { model: "x" })), /no answers/);
  });

  it("rejects a choice question with one option", async () => {
    const bad = { state: "x", questions: { q: { type: "choice", criteria: { only: null } } } };
    assertSkipped(await decide(bad, config, stubFetch(200, {})), /needs 2-255 options/);
  });

  it("rejects a score question with too many levels", async () => {
    const levels = Array.from({ length: 11 }, (_v, i) => `l${i}`);
    const bad = { state: "x", questions: { q: { type: "score", criteria: levels } } };
    assertSkipped(await decide(bad, config, stubFetch(200, {})), /invalid request/);
  });

  it("rejects a noul question with neither instructions nor criteria", async () => {
    const bad = { state: "x", questions: { q: { type: "noul" } } };
    assertSkipped(await decide(bad, config, stubFetch(200, {})), /needs instructions or criteria/);
  });

  it("rejects an empty question set and too many questions", async () => {
    assertSkipped(await decide({ state: "x", questions: {} }, config, stubFetch(200, {})), /1-128 questions/);
    const many = Object.fromEntries(
      Array.from({ length: 129 }, (_v, i) => [`q${i}`, { type: "noul", instructions: "?" }]),
    );
    assertSkipped(await decide({ state: "x", questions: many }, config, stubFetch(200, {})), /1-128 questions/);
  });

  it("rejects an unsupported image type", async () => {
    const bad = { ...request, images: [{ mediaType: "image/gif", base64: "AAAA" }] };
    assertSkipped(await decide(bad, config, stubFetch(200, {})), /invalid request at images/);
  });
});

describe("loadConfig", () => {
  it("uses defaults when nothing is set", () => {
    assert.deepEqual(loadConfig({}), {
      apiKey: "",
      apiUrl: DEFAULT_API_URL,
      model: DEFAULT_MODEL,
      timeoutMs: DEFAULT_TIMEOUT_SECONDS * 1000,
    });
  });

  it("treats unsubstituted placeholders and bad numbers as unset", () => {
    const cfg = loadConfig({
      SUBQ_API_KEY: "${user_config.api_key}",
      SUBQ_API_URL: "  ",
      SUBQ_TIMEOUT_SECONDS: "abc",
    });
    assert.equal(cfg.apiKey, "");
    assert.equal(cfg.apiUrl, DEFAULT_API_URL);
    assert.equal(cfg.timeoutMs, DEFAULT_TIMEOUT_SECONDS * 1000);
    assert.equal(loadConfig({ SUBQ_TIMEOUT_SECONDS: "500" }).timeoutMs, DEFAULT_TIMEOUT_SECONDS * 1000);
  });

  it("reads explicit values", () => {
    const cfg = loadConfig({ SUBQ_API_KEY: "k", SUBQ_MODEL: "m", SUBQ_TIMEOUT_SECONDS: "10" });
    assert.equal(cfg.apiKey, "k");
    assert.equal(cfg.model, "m");
    assert.equal(cfg.timeoutMs, 10000);
  });
});
