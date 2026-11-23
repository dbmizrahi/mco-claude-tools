import assert from "node:assert/strict";
import { createHash, createHmac } from "node:crypto";
import { describe, it } from "node:test";

import { buildQuery, phpUrlencode, sortTopLevel } from "../src/encode.js";
import { signRequest, signature } from "../src/signature.js";

/** Independent re-implementation of the documented PHP formula, for cross-checking. */
function referenceSignature(path: string, query: string, secret: string): string {
  const md5 = createHash("md5").update(query).digest("hex");
  const hex = createHmac("sha1", secret).update(`${path}${query}${md5}`).digest("hex");
  return Buffer.from(hex).toString("base64");
}

describe("phpUrlencode (PHP urlencode / RFC 1738)", () => {
  it("encodes like PHP: space as +, ~ * ! ' ( ) percent-encoded, -_. kept", () => {
    assert.equal(phpUrlencode("a b"), "a+b");
    assert.equal(phpUrlencode("~*!'()"), "%7E%2A%21%27%28%29");
    assert.equal(phpUrlencode("-_.AZaz09"), "-_.AZaz09");
    assert.equal(phpUrlencode("+972"), "%2B972");
    assert.equal(phpUrlencode("[]"), "%5B%5D");
  });

  it("encodes non-ASCII text as UTF-8 with upper-case hex", () => {
    assert.equal(phpUrlencode("שלום"), "%D7%A9%D7%9C%D7%95%D7%9D");
  });
});

describe("buildQuery (PHP http_build_query)", () => {
  it("flattens nested objects and arrays as a[b]=c and a[0]=c, skips null and undefined", () => {
    const query = buildQuery({
      filter: { status: "company", type: "client" },
      numbers: [{ number: "100", delay: 0 }],
      skip: null,
      gone: undefined,
    });
    assert.equal(
      query,
      "filter%5Bstatus%5D=company&filter%5Btype%5D=client&numbers%5B0%5D%5Bnumber%5D=100&numbers%5B0%5D%5Bdelay%5D=0",
    );
  });

  it("writes booleans as 1 and 0, like PHP", () => {
    assert.equal(buildQuery({ a: true, b: false }), "a=1&b=0");
  });

  it("sorts top-level keys only (PHP ksort)", () => {
    const sorted = sortTopLevel({ to: "1", filter: { z: "1", a: "2" }, format: "json" });
    assert.deepEqual(Object.keys(sorted), ["filter", "format", "to"]);
    assert.equal(buildQuery(sorted), "filter%5Bz%5D=1&filter%5Ba%5D=2&format=json&to=1");
  });
});

describe("signature (known vectors, computed independently with Python hmac/hashlib)", () => {
  it("callback request", () => {
    const signed = signRequest("/v1/request/callback/", { to: "+972501234567", from: "100", format: "json" }, "test-key", "test-secret");
    assert.equal(signed.query, "format=json&from=100&to=%2B972501234567");
    assert.equal(signed.authorization, "test-key:YmRiMGNhNTdkYzEzMTkzNzM2MjQzOTZmOGUwMjNiMjlkNjRlMzk2MA==");
  });

  it("text with characters PHP and JavaScript encode differently", () => {
    const signed = signRequest(
      "/v1/sms/send/",
      { number: "972501234567", message: "Hello world ~*!", format: "json" },
      "k",
      "test-secret",
    );
    assert.equal(signed.query, "format=json&message=Hello+world+%7E%2A%21&number=972501234567");
    assert.equal(signed.authorization, "k:ODFiODQ2ZDUzMGJlNjI4YzI4YWQ4MDYwNDAzOWQxMWQ4MzliMTk2YQ==");
  });

  it("nested CRM filter", () => {
    const signed = signRequest("/v1/zcrm/customers", { take: 5, filter: { status: "company", type: "client" }, format: "json" }, "k", "test-secret");
    assert.equal(signed.query, "filter%5Bstatus%5D=company&filter%5Btype%5D=client&format=json&take=5");
    assert.equal(signed.authorization, "k:ZjY4MjQwNTU5NzU2ZmQzNTZhNTc1ODY1NTk5ODY0NTQ1ODk5NmFiMA==");
  });

  it("matches the reference formula for an empty query", () => {
    assert.equal(signature("/v1/info/balance/", "", "s3cret"), referenceSignature("/v1/info/balance/", "", "s3cret"));
  });
});
