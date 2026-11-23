import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { mkdtemp, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, it } from "node:test";

import { isRecord } from "../src/client.js";
import { loadConfig } from "../src/config.js";
import { formatResult } from "../src/output.js";
import { runTool, type RunDeps } from "../src/run.js";
import { createServer, toolInputSchema } from "../src/server.js";
import type { ActionDef, ToolDef } from "../src/tools/define.js";
import { ALL_TOOLS } from "../src/tools/index.js";
import { MAX_UPLOAD_BYTES } from "../src/uploads.js";
import { jsonResponse, stubFetch, TEST_CONFIG } from "./helpers.js";

function tool(name: string): ToolDef {
  const found = ALL_TOOLS.find((t) => t.name === name);
  assert.ok(found, `tool ${name} exists`);
  return found;
}

function action(toolName: string, actionName: string): ActionDef {
  const found = tool(toolName).actions.find((a) => a.name === actionName);
  assert.ok(found, `${toolName}.${actionName} exists`);
  return found;
}

function deps(respond: () => Response = () => jsonResponse({ status: "success" })): RunDeps & { calls: number } {
  const stub = stubFetch(respond);
  const result = {
    loadConfig: () => ({ ok: true as const, config: TEST_CONFIG }),
    fetch: stub.fetch,
    get calls(): number {
      return stub.calls.length;
    },
  };
  return result;
}

function parseText(result: { content: ReadonlyArray<{ type: string }> }): Record<string, unknown> {
  const first = result.content[0];
  assert.ok(first && "text" in first && typeof first.text === "string");
  const parsed: unknown = JSON.parse(first.text);
  assert.ok(isRecord(parsed));
  return parsed;
}

describe("tool list", () => {
  it("has 26 tools named zadarma_<section>, each with unique action names", () => {
    assert.equal(ALL_TOOLS.length, 26);
    const names = ALL_TOOLS.map((t) => t.name);
    assert.equal(new Set(names).size, names.length);
    for (const t of ALL_TOOLS) {
      assert.match(t.name, /^zadarma_[a-z_]+$/);
      for (const a of t.actions) {
        assert.match(a.name, /^[a-z0-9_]+$/);
      }
    }
  });

  it("matches the tools listed in manifest.json", () => {
    const raw: unknown = JSON.parse(readFileSync(new URL("../../manifest.json", import.meta.url), "utf8"));
    assert.ok(isRecord(raw) && Array.isArray(raw["tools"]));
    const listed = raw["tools"].map((t: unknown) => (isRecord(t) ? t["name"] : undefined));
    assert.deepEqual(listed, ALL_TOOLS.map((t) => t.name));
  });

  it("builds the MCP server and an input schema for every tool", () => {
    assert.doesNotThrow(() => createServer());
    for (const t of ALL_TOOLS) {
      const schema = toolInputSchema(t);
      assert.equal(schema.safeParse({ action: t.actions[0]?.name }).success, true);
      assert.equal(schema.safeParse({ action: "no_such_action" }).success, false);
    }
  });

  it("annotations follow the most dangerous action (R3.2)", () => {
    for (const t of ALL_TOOLS) {
      const allRead = t.actions.every((a) => a.kind === "read");
      const risky = t.actions.some((a) => a.kind === "dangerous" || a.conditional);
      assert.equal(t.annotations.readOnlyHint, allRead, t.name);
      assert.equal(t.annotations.destructiveHint, risky, t.name);
      assert.equal(t.description.includes("explicit approval"), risky, `${t.name} safety text (R3.3)`);
    }
  });

  it("read-only actions are GET; every DELETE needs confirm", () => {
    for (const t of ALL_TOOLS) {
      for (const a of t.actions) {
        if (a.kind === "read") {
          assert.equal(a.method, "GET", `${t.name}.${a.name}`);
        }
        if (a.method === "DELETE") {
          assert.equal(a.kind, "dangerous", `${t.name}.${a.name}`);
        }
        if (a.kind === "dangerous" || a.conditional) {
          assert.ok(a.risk !== undefined && a.risk.length > 0, `${t.name}.${a.name} risk text`);
        }
      }
    }
  });

  it("the actions named in R3.1 need confirm", () => {
    const required: Array<[string, string]> = [
      ["zadarma_numbers", "order"],
      ["zadarma_numbers", "prolong"],
      ["zadarma_tariff", "change"],
      ["zadarma_sip", "create"],
      ["zadarma_sip", "change_password"],
      ["zadarma_pbx_extensions", "change_password"],
      ["zadarma_sms", "send"],
      ["zadarma_callback", "start"],
      ["zadarma_verify", "send"],
      ["zadarma_esim", "create_order"],
    ];
    for (const [t, a] of required) {
      assert.equal(action(t, a).kind, "dangerous", `${t}.${a}`);
    }
  });
});

describe("input validation (every action)", () => {
  it("every action rejects unknown parameters", async () => {
    for (const t of ALL_TOOLS) {
      for (const a of t.actions) {
        const result = await a.prepare({ definitely_not_a_param: 1 });
        assert.equal(result.ok, false, `${t.name}.${a.name}`);
      }
    }
  });

  it("every action rejects a non-object params value", async () => {
    for (const t of ALL_TOOLS) {
      for (const a of t.actions) {
        assert.equal((await a.prepare("nope")).ok, false, `${t.name}.${a.name}`);
      }
    }
  });

  it("checks required fields, formats and combinations", async () => {
    const bad: Array<[string, string, unknown]> = [
      ["zadarma_ivr_scenarios", "create", { menu_id: 1, push_button: 1, extension: "100" }],
      ["zadarma_ivr_scenarios", "create", { menu_id: 1, push_button: 31, title: "x", extension: "100" }],
      ["zadarma_ivr_menus", "delete", { menu_id: 0 }],
      ["zadarma_statistics", "calls", { start: "2026-11-01" }],
      ["zadarma_statistics", "pbx", { limit: 5000 }],
      ["zadarma_pbx", "set_redirection", { pbx_number: "100", status: "on" }],
      ["zadarma_pbx", "set_redirection", { pbx_number: "100", status: "off", greeting_file_path: "/tmp/a.mp3" }],
      ["zadarma_pbx_records", "get_link", {}],
      ["zadarma_verify", "send", { channel: "email", to: "a@b.co", email_body: "no code here" }],
      ["zadarma_verify", "send", { channel: "fax", to: "972501234567" }],
      ["zadarma_info", "check_number", { caller_id: "972501234567", to: "972501234568", code: "12ab" }],
      ["zadarma_sip", "status", { sip: "../etc" }],
      ["zadarma_crm_customers", "create", { customer: { status: "company" } }],
      ["zadarma_sms", "send", { number: [], message: "hi" }],
    ];
    for (const [t, a, params] of bad) {
      assert.equal((await action(t, a).prepare(params)).ok, false, `${t}.${a} ${JSON.stringify(params)}`);
    }
    const good: Array<[string, string, unknown]> = [
      ["zadarma_ivr_scenarios", "create", { menu_id: 1, push_button: -1, title: "No key", extension: "100 101" }],
      ["zadarma_statistics", "pbx", { start: "2026-11-01 00:00:00", end: "2026-11-23 23:59:59", call_type: "in" }],
      ["zadarma_pbx", "set_redirection", { pbx_number: "100", status: "on", type: "phone", destination: "972501234567", condition: "noanswer" }],
      ["zadarma_verify", "send", { channel: "sms", to: "972501234567" }],
      ["zadarma_crm_customers", "list", { filter: { status: "company" }, sort: { attr: "name", desc: 1 }, take: 5 }],
    ];
    for (const [t, a, params] of good) {
      const result = await action(t, a).prepare(params);
      assert.equal(result.ok, true, `${t}.${a} ${JSON.stringify(result)}`);
    }
  });

  it("fills path parameters and leaves them out of the body", async () => {
    const result = await action("zadarma_pbx_extensions", "set_caller_id").prepare({ extension: "100", number: "972501234567" });
    assert.ok(result.ok);
    assert.equal(result.request.path, "/v1/pbx/internal/100/callerid/");
    assert.deepEqual(result.request.params, { number: "972501234567" });
  });

  it("maps parameters the way each endpoint expects", async () => {
    const scenario = await action("zadarma_ivr_scenarios", "create").prepare({ menu_id: 1, push_button: 2, title: "Hebrew", extension: "101" });
    assert.ok(scenario.ok);
    assert.equal(scenario.request.params["push_button"], "2");
    const sms = await action("zadarma_sms", "send").prepare({ number: ["972501234567", "972501234568"], message: "hi" });
    assert.ok(sms.ok);
    assert.equal(sms.request.params["number"], "972501234567,972501234568");
    const hooks = await action("zadarma_pbx", "webhooks_set_hooks").prepare({ sms: true, call_tracking: false });
    assert.ok(hooks.ok);
    assert.deepEqual(hooks.request.params, { sms: "true", call_tracking: "false" });
    const menu = await action("zadarma_ivr_menus", "create").prepare({});
    assert.ok(menu.ok);
    assert.deepEqual(menu.request.params, { buy: "false" });
  });
});

describe("confirm gate (R3.1)", () => {
  it("a dangerous action without confirm changes nothing and returns a preview", async () => {
    const d = deps();
    const result = await runTool(tool("zadarma_sms"), { action: "send", params: { number: ["972501234567"], message: "hi" } }, d);
    assert.equal(d.calls, 0);
    assert.equal(result.isError, undefined);
    const body = parseText(result);
    assert.equal(body["status"], "confirmation_required");
    assert.equal(body["changed"], "nothing");
    assert.equal(body["would_call"], "POST /v1/sms/send/");
  });

  it("confirm: false is the same as no confirm", async () => {
    const d = deps();
    await runTool(tool("zadarma_ivr_menus"), { action: "delete", params: { menu_id: 3 }, confirm: false }, d);
    assert.equal(d.calls, 0);
  });

  it("with confirm: true the request is sent once", async () => {
    const d = deps();
    const result = await runTool(tool("zadarma_ivr_menus"), { action: "delete", params: { menu_id: 3 }, confirm: true }, d);
    assert.equal(d.calls, 1);
    assert.equal(parseText(result)["status"], "success");
  });

  it("conditional actions need confirm only for the risky arguments", async () => {
    const free = deps();
    await runTool(tool("zadarma_ivr_menus"), { action: "create", params: {} }, free);
    assert.equal(free.calls, 1);
    const paid = deps();
    const result = await runTool(tool("zadarma_ivr_menus"), { action: "create", params: { buy: true } }, paid);
    assert.equal(paid.calls, 0);
    assert.equal(parseText(result)["status"], "confirmation_required");
    const lead = deps();
    await runTool(tool("zadarma_crm_leads"), { action: "update", params: { lead_id: 5, convert: 2, lead: {} } }, lead);
    assert.equal(lead.calls, 0);
  });

  it("passwords are hidden in the preview", async () => {
    const result = await runTool(
      tool("zadarma_sip"),
      { action: "create", params: { name: "Desk", password: "Sup3rSecretPass", callerid: "972501234567" } },
      deps(),
    );
    const body = parseText(result);
    assert.ok(isRecord(body["params"]));
    assert.equal(body["params"]["password"], "***");
    const change = await runTool(tool("zadarma_sip"), { action: "change_password", params: { sip: "100", value: "An0therSecret" } }, deps());
    assert.ok(!JSON.stringify(change).includes("An0therSecret"));
  });
});

describe("runTool errors", () => {
  it("unknown action", async () => {
    const result = await runTool(tool("zadarma_info"), { action: "nope" }, deps());
    assert.equal(result.isError, true);
    assert.match(String(parseText(result)["next_step"]), /balance/);
  });

  it("invalid params do not reach Zadarma", async () => {
    const d = deps();
    const result = await runTool(tool("zadarma_info"), { action: "price", params: {} }, d);
    assert.equal(result.isError, true);
    assert.equal(d.calls, 0);
    assert.match(String(parseText(result)["error"]), /number/);
  });

  it("missing settings name the setting to fill in (R1.4)", async () => {
    const stub = stubFetch(() => jsonResponse({ status: "success" }));
    const result = await runTool(
      tool("zadarma_info"),
      { action: "balance" },
      { loadConfig: () => loadConfig({ ZADARMA_API_KEY: "k", ZADARMA_API_SECRET: "${user_config.api_secret}" }), fetch: stub.fetch },
    );
    assert.equal(result.isError, true);
    assert.equal(stub.calls.length, 0);
    const error = String(parseText(result)["error"]);
    assert.match(error, /"API secret"/);
    assert.doesNotMatch(error, /"API key"/);
  });

  it("Zadarma errors become isError with message and next step (R5.1)", async () => {
    const result = await runTool(
      tool("zadarma_ivr_scenarios"),
      { action: "list", params: { menu_id: 0 } },
      deps(() => jsonResponse({ status: "error", message: "Wrong parameters!" })),
    );
    assert.equal(result.isError, true);
    const body = parseText(result);
    assert.equal(body["error"], "Zadarma error: Wrong parameters!");
    assert.equal(typeof body["next_step"], "string");
  });

  it("429 reports the reset time (R5.2)", async () => {
    const reset = Math.floor(Date.now() / 1000) + 30;
    const result = await runTool(
      tool("zadarma_statistics"),
      { action: "calls" },
      deps(() => jsonResponse({ status: "error" }, 429, { "X-RateLimit-Reset": String(reset) })),
    );
    assert.equal(result.isError, true);
    assert.equal(parseText(result)["rate_limit_reset"], new Date(reset * 1000).toISOString());
  });
});

describe("large results (R5.3)", () => {
  it("shortens the longest list and says how to narrow the request", () => {
    const data = { status: "success", stats: Array.from({ length: 500 }, (_, i) => ({ id: i, note: "x".repeat(50) })) };
    const text = formatResult(data, "use a shorter start/end range", 5000);
    assert.ok(text.length <= 5100);
    const parsed: unknown = JSON.parse(text);
    assert.ok(isRecord(parsed));
    assert.match(String(parsed["truncated"]), /of 500 items in "stats".*shorter start\/end range/);
  });

  it("leaves small results unchanged", () => {
    assert.equal(formatResult({ status: "success", balance: 1 }, undefined), '{"status":"success","balance":1}');
  });
});

describe("audio uploads (R4.1)", () => {
  const upload = action("zadarma_ivr_sounds", "upload");

  async function tempFile(name: string, bytes: Uint8Array): Promise<string> {
    const dir = await mkdtemp(join(tmpdir(), "zadarma-mcp-test-"));
    const path = join(dir, name);
    await writeFile(path, bytes);
    return path;
  }

  const wav = new Uint8Array([...Buffer.from("RIFF"), 0, 0, 0, 0, ...Buffer.from("WAVE"), 1, 2, 3, 4]);
  const mp3 = new Uint8Array([...Buffer.from("ID3"), 4, 0, 0, 0, 0, 0, 0]);

  it("accepts a WAV and an MP3 file and sends them as multipart", async () => {
    for (const [name, bytes, mime] of [["greeting.wav", wav, "audio/wav"], ["greeting.mp3", mp3, "audio/mpeg"]] as const) {
      const result = await upload.prepare({ name: "Greeting", file_path: await tempFile(name, bytes) });
      assert.ok(result.ok, JSON.stringify(result));
      assert.equal(result.request.files?.[0]?.mimeType, mime);
      assert.equal(result.request.files?.[0]?.field, "file");
      assert.deepEqual(result.request.params, { name: "Greeting" });
    }
  });

  it("rejects other extensions, fake audio, empty and oversize files, relative and missing paths", async () => {
    const big = new Uint8Array(MAX_UPLOAD_BYTES + 1);
    big.set(mp3);
    const cases: Array<[string, RegExp]> = [
      [await tempFile("notes.txt", mp3), /Only MP3 or WAV/],
      [await tempFile("fake.mp3", Buffer.from("not audio at all")), /not MP3 audio/],
      [await tempFile("fake.wav", mp3), /not WAV audio/],
      [await tempFile("empty.mp3", new Uint8Array(0)), /empty/],
      [await tempFile("big.mp3", big), /up to 5 MB/],
      ["relative/greeting.mp3", /absolute/],
      ["/definitely/missing/greeting.mp3", /not found/],
    ];
    for (const [path, message] of cases) {
      const result = await upload.prepare({ name: "x", file_path: path });
      assert.equal(result.ok, false, path);
      if (!result.ok) {
        assert.match(result.error, message, path);
      }
    }
  });

  it("an invalid file never reaches Zadarma", async () => {
    const d = deps();
    const result = await runTool(
      tool("zadarma_pbx_hold_music"),
      { action: "upload", params: { file_path: await tempFile("x.mp3", Buffer.from("hello")) } },
      d,
    );
    assert.equal(result.isError, true);
    assert.equal(d.calls, 0);
  });
});
