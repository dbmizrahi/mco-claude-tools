import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { callApi, isRecord } from "../src/client.js";
import { buildQuery } from "../src/encode.js";
import { signature } from "../src/signature.js";
import { header, jsonResponse, stubFetch, TEST_CONFIG } from "./helpers.js";

describe("callApi requests", () => {
  it("GET: signed query string with format=json and the Authorization header", async () => {
    const stub = stubFetch(() => jsonResponse({ status: "success", balance: 10 }));
    const result = await callApi(TEST_CONFIG, { method: "GET", path: "/v1/info/price/", params: { number: "972501234567" } }, stub.fetch);
    assert.deepEqual(result, { ok: true, data: { status: "success", balance: 10 } });
    const call = stub.calls[0];
    assert.ok(call);
    const query = "format=json&number=972501234567";
    assert.equal(call.url, `https://api.zadarma.com/v1/info/price/?${query}`);
    assert.equal(call.init.method, "GET");
    assert.equal(call.init.body, undefined);
    assert.equal(header(call.init, "authorization"), `test-key:${signature("/v1/info/price/", query, "test-secret")}`);
  });

  it("POST/PUT/DELETE: form-urlencoded body equal to the signed string", async () => {
    for (const method of ["POST", "PUT", "DELETE"] as const) {
      const stub = stubFetch(() => jsonResponse({ status: "success" }));
      await callApi(TEST_CONFIG, { method, path: "/v1/pbx/ivr/delete/", params: { menu_id: 2 } }, stub.fetch);
      const call = stub.calls[0];
      assert.ok(call);
      assert.equal(call.url, "https://api.zadarma.com/v1/pbx/ivr/delete/");
      assert.equal(call.init.method, method);
      assert.equal(call.init.body, "format=json&menu_id=2");
      assert.equal(header(call.init, "content-type"), "application/x-www-form-urlencoded");
      assert.equal(header(call.init, "authorization"), `test-key:${signature("/v1/pbx/ivr/delete/", "format=json&menu_id=2", "test-secret")}`);
    }
  });

  it("multipart upload: fields and file in the body; the file is not part of the signature", async () => {
    const stub = stubFetch(() => jsonResponse({ status: "success" }));
    const bytes = new Uint8Array([0x49, 0x44, 0x33, 1, 2, 3]);
    await callApi(
      TEST_CONFIG,
      {
        method: "POST",
        path: "/v1/pbx/ivr/sounds/upload",
        params: { name: "greeting" },
        files: [{ field: "file", fileName: "greeting.mp3", mimeType: "audio/mpeg", bytes }],
      },
      stub.fetch,
    );
    const call = stub.calls[0];
    assert.ok(call);
    const body = call.init.body;
    assert.ok(body instanceof FormData);
    assert.equal(body.get("name"), "greeting");
    assert.equal(body.get("format"), "json");
    const file = body.get("file");
    assert.ok(file instanceof Blob);
    assert.equal(file.size, 6);
    assert.equal(header(call.init, "content-type"), null, "fetch sets the multipart boundary itself");
    const signed = buildQuery({ format: "json", name: "greeting" });
    assert.equal(header(call.init, "authorization"), `test-key:${signature("/v1/pbx/ivr/sounds/upload", signed, "test-secret")}`);
  });
});

describe("callApi errors", () => {
  it("status: error is returned as an error with Zadarma's message and a next step", async () => {
    const stub = stubFetch(() => jsonResponse({ status: "error", message: "Wrong parameters!" }));
    const result = await callApi(TEST_CONFIG, { method: "GET", path: "/v1/sip/", params: {} }, stub.fetch);
    assert.equal(result.ok, false);
    if (!result.ok) {
      assert.equal(result.error, "Zadarma error: Wrong parameters!");
      assert.match(result.nextStep, /parameters/);
    }
  });

  it("HTTP 401 points to the key and secret settings", async () => {
    const stub = stubFetch(() => jsonResponse({ status: "error", message: "Not authorized" }, 401));
    const result = await callApi(TEST_CONFIG, { method: "GET", path: "/v1/sip/", params: {} }, stub.fetch);
    assert.equal(result.ok, false);
    if (!result.ok) {
      assert.equal(result.httpStatus, 401);
      assert.match(result.nextStep, /API key and secret/);
    }
  });

  it("HTTP 500 with a non-JSON body is an error", async () => {
    const stub = stubFetch(() => new Response("<html>oops</html>", { status: 500, headers: { "content-type": "text/html" } }));
    const result = await callApi(TEST_CONFIG, { method: "GET", path: "/v1/sip/", params: {} }, stub.fetch);
    assert.equal(result.ok, false);
    if (!result.ok) {
      assert.equal(result.httpStatus, 500);
      assert.match(result.nextStep, /try again later/);
    }
  });

  it("HTTP 429: reset time from X-RateLimit-Reset, and no retry", async () => {
    const reset = Math.floor(Date.now() / 1000) + 42;
    const stub = stubFetch(() => jsonResponse({ status: "error", message: "You exceeded the rate limit" }, 429, { "X-RateLimit-Reset": String(reset) }));
    const result = await callApi(TEST_CONFIG, { method: "GET", path: "/v1/statistics/", params: {} }, stub.fetch);
    assert.equal(stub.calls.length, 1);
    assert.equal(result.ok, false);
    if (!result.ok) {
      assert.equal(result.httpStatus, 429);
      assert.equal(result.rateLimitReset, new Date(reset * 1000).toISOString());
      assert.match(result.nextStep, /Do not retry in a loop/);
    }
  });

  it("network failure is an error naming the host", async () => {
    const stub = stubFetch(() => {
      throw new TypeError("fetch failed");
    });
    const result = await callApi(TEST_CONFIG, { method: "GET", path: "/v1/sip/", params: {} }, stub.fetch);
    assert.equal(result.ok, false);
    if (!result.ok) {
      assert.match(result.error, /api\.zadarma\.com: fetch failed/);
    }
  });

  it("binary responses return metadata only, never the bytes", async () => {
    const stub = stubFetch(
      () => new Response(new Uint8Array([1, 2, 3, 4]), { status: 200, headers: { "content-type": "application/pdf" } }),
    );
    const result = await callApi(TEST_CONFIG, { method: "GET", path: "/v1/zcrm/files/7", params: {} }, stub.fetch);
    assert.equal(result.ok, true);
    if (result.ok) {
      assert.ok(isRecord(result.data));
      assert.deepEqual(Object.keys(result.data).sort(), ["bytes", "content_disposition", "content_type", "note"]);
    }
  });

  it("never puts the secret in the request URL, body or result", async () => {
    const stub = stubFetch(() => jsonResponse({ status: "error", message: "bad" }, 400));
    const result = await callApi(TEST_CONFIG, { method: "POST", path: "/v1/sms/send/", params: { message: "hi" } }, stub.fetch);
    const call = stub.calls[0];
    assert.ok(call);
    assert.ok(!call.url.includes(TEST_CONFIG.apiSecret));
    assert.ok(!String(call.init.body).includes(TEST_CONFIG.apiSecret));
    assert.ok(!JSON.stringify(result).includes(TEST_CONFIG.apiSecret));
  });
});
