/**
 * Account info, callback, SIP numbers, price plans and statistics.
 * API reference sections "Info", "SIP", "Tariffs" and "Statistics".
 */
import { z } from "zod";

import { dateTime, language, none, pathId, phone, skipLimit } from "./common.js";
import { defineAction, defineTool, type ToolDef } from "./define.js";

export const infoTool: ToolDef = defineTool(
  "zadarma_info",
  "Zadarma account info",
  "Account information: balance, call price, timezone, currencies, languages, price plans; number verification call; number lookup (HLR).",
  [
    defineAction("balance", {
      description: "Account balance and currency.",
      method: "GET",
      path: "/v1/info/balance/",
      params: none,
      kind: "read",
    }),
    defineAction("price", {
      description: "Price of a call to a number on the current price plan (optionally from a given Caller ID).",
      method: "GET",
      path: "/v1/info/price/",
      params: z.strictObject({ number: phone, caller_id: phone.optional() }),
      kind: "read",
    }),
    defineAction("timezone", {
      description: "Account timezone.",
      method: "GET",
      path: "/v1/info/timezone/",
      params: none,
      kind: "read",
    }),
    defineAction("currencies", {
      description: "List of currencies.",
      method: "GET",
      path: "/v1/info/lists/currencies/",
      params: none,
      kind: "read",
    }),
    defineAction("languages", {
      description: "Languages available in the account.",
      method: "GET",
      path: "/v1/info/lists/languages/",
      params: none,
      kind: "read",
    }),
    defineAction("tariffs", {
      description: "List of price plans, with prices in the given currency (e.g. USD, EUR).",
      method: "GET",
      path: "/v1/info/lists/tariffs/",
      params: z.strictObject({ currency: z.string().regex(/^[A-Za-z]{3}$/, "three-letter currency code") }),
      kind: "read",
    }),
    defineAction("check_number", {
      description:
        "Call a number and play a code (digits, up to 20) to verify it. caller_id must be one of the account's numbers.",
      method: "GET",
      path: "/v1/request/checknumber/",
      params: z.strictObject({
        caller_id: phone,
        to: z.string().min(3),
        code: z.string().regex(/^[0-9]{1,20}$/, "digits only, up to 20"),
        lang: language.optional(),
      }),
      kind: "dangerous",
      risk: "places a paid call to another person's number",
    }),
    defineAction("number_lookup", {
      description:
        "Check numbers in the operator database (HLR). One number: result now; several: the result is sent to the address set on the lookup page in the Zadarma account.",
      method: "POST",
      path: "/v1/info/number_lookup/",
      params: z.strictObject({ numbers: z.array(phone).min(1).max(1000) }),
      kind: "dangerous",
      risk: "number lookups are paid",
    }),
  ],
);

export const callbackTool: ToolDef = defineTool(
  "zadarma_callback",
  "Zadarma callback",
  "Start a callback: Zadarma first calls `from` (your phone, SIP, extension or PBX scenario), then connects it to `to`.",
  [
    defineAction("start", {
      description:
        "Start a callback. sip: SIP or extension whose Caller ID, recording and prefix are used. " +
        "predicted: true calls `to` first and connects `from` only if `to` answers.",
      method: "GET",
      path: "/v1/request/callback/",
      params: z.strictObject({
        from: z.string().min(1),
        to: z.string().min(1),
        sip: z.string().optional(),
        predicted: z.boolean().optional(),
      }),
      kind: "dangerous",
      risk: "places paid calls and rings another person's phone",
      toParams: (args) => ({
        from: args.from,
        to: args.to,
        sip: args.sip,
        predicted: args.predicted === true ? "1" : undefined,
      }),
    }),
  ],
);

export const sipTool: ToolDef = defineTool(
  "zadarma_sip",
  "Zadarma SIP numbers",
  "SIP numbers of the account: list, online status, Caller ID, call forwarding, create, password.",
  [
    defineAction("list", {
      description: "List SIP numbers (ID, name, lines) and how many more can be created.",
      method: "GET",
      path: "/v1/sip/",
      params: none,
      kind: "read",
    }),
    defineAction("status", {
      description: "Online status of a SIP number.",
      method: "GET",
      path: "/v1/sip/{sip}/status/",
      params: z.strictObject({ sip: pathId }),
      kind: "read",
    }),
    defineAction("set_caller_id", {
      description: "Set a SIP number's Caller ID to one of the account's numbers (international format).",
      method: "PUT",
      path: "/v1/sip/callerid/",
      params: z.strictObject({ id: z.string().min(1), number: phone }),
      kind: "write",
    }),
    defineAction("get_redirection", {
      description: "Show call forwarding of all SIP numbers, or of one (id).",
      method: "GET",
      path: "/v1/sip/redirection/",
      params: z.strictObject({ id: z.string().min(1).optional() }),
      kind: "read",
    }),
    defineAction("set_redirection_status", {
      description: "Turn call forwarding of a SIP number on or off.",
      method: "PUT",
      path: "/v1/sip/redirection/",
      params: z.strictObject({ id: z.string().min(1), status: z.enum(["on", "off"]) }),
      kind: "write",
    }),
    defineAction("set_redirection", {
      description: "Forward a SIP number to a phone: condition always (default) or unavailable (no answer or no SIP connection).",
      method: "PUT",
      path: "/v1/sip/redirection/",
      params: z.strictObject({
        id: z.string().min(1),
        number: phone,
        condition: z.enum(["always", "unavailable"]).optional(),
      }),
      kind: "write",
      toParams: (args) => ({ id: args.id, type: "phone", number: args.number, condition: args.condition }),
    }),
    defineAction("create", {
      description: "Create a SIP number: display name, password, callerid; redirect_to_phone optional.",
      method: "POST",
      path: "/v1/sip/create/",
      params: z.strictObject({
        name: z.string().min(1).max(100),
        password: z.string().min(8),
        callerid: phone,
        redirect_to_phone: phone.optional(),
      }),
      kind: "dangerous",
      risk: "creates a SIP number, which may be charged to the Zadarma balance",
    }),
    defineAction("change_password", {
      description: "Change a SIP number's password (value = new password).",
      method: "PUT",
      path: "/v1/sip/{sip}/password/",
      params: z.strictObject({ sip: pathId, value: z.string().min(8) }),
      kind: "dangerous",
      risk: "devices using the old password lose their connection",
    }),
  ],
);

export const tariffTool: ToolDef = defineTool(
  "zadarma_tariff",
  "Zadarma price plan",
  "Current price plan and changing it. See zadarma_info action tariffs for the list of plans.",
  [
    defineAction("current", {
      description: "Current price plan, its cost and used seconds.",
      method: "GET",
      path: "/v1/tariff/",
      params: none,
      kind: "read",
    }),
    defineAction("change", {
      description:
        "Change the price plan (tariff_id from zadarma_info tariffs). period month (default) or year, for package plans only.",
      method: "POST",
      path: "/v1/tariff/change/",
      params: z.strictObject({ tariff_id: z.number().int().positive(), period: z.enum(["month", "year"]).optional() }),
      kind: "dangerous",
      risk: "changes the paid price plan; the cost may be charged to the balance immediately",
    }),
  ],
);

const statsRange = {
  start: dateTime.optional().describe("default: start of this month"),
  end: dateTime.optional().describe("default: now; at most 1 month after start"),
};
const statsHint = "use a shorter start/end range (max 1 month) or skip/limit (max 1000 rows)";

export const statisticsTool: ToolDef = defineTool(
  "zadarma_statistics",
  "Zadarma statistics",
  "Call statistics. Zadarma allows only 3 statistics requests per minute; do not poll. Dates: YYYY-MM-DD HH:MM:SS.",
  [
    defineAction("calls", {
      description:
        "Overall call statistics; sip filters by SIP number; cost_only returns only the amount spent; type overall|toll-free.",
      method: "GET",
      path: "/v1/statistics/",
      params: z.strictObject({
        ...statsRange,
        sip: z.string().optional(),
        cost_only: z.boolean().optional(),
        type: z.enum(["overall", "toll-free"]).optional(),
        ...skipLimit,
      }),
      kind: "read",
      narrowHint: statsHint,
      toParams: (args) => ({ ...args, cost_only: args.cost_only === true ? "1" : undefined }),
    }),
    defineAction("pbx", {
      description: "PBX call statistics (call_id, pbx_call_id, recording flag); call_type in|out; version 2 (new format, default) or 1.",
      method: "GET",
      path: "/v1/statistics/pbx/",
      params: z.strictObject({
        ...statsRange,
        version: z.union([z.literal(1), z.literal(2)]).optional(),
        call_type: z.enum(["in", "out"]).optional(),
        ...skipLimit,
      }),
      kind: "read",
      narrowHint: statsHint,
      toParams: (args) => ({ ...args, version: args.version ?? 2 }),
    }),
    defineAction("callback_widget", {
      description: "Callback widget statistics, for all widgets or one (widget_id).",
      method: "GET",
      path: "/v1/statistics/callback_widget/",
      params: z.strictObject({ ...statsRange, widget_id: z.string().optional() }),
      kind: "read",
      narrowHint: statsHint,
    }),
    defineAction("incoming_calls", {
      description: "Incoming call statistics; sip filters by SIP number.",
      method: "GET",
      path: "/v1/statistics/incoming-calls/",
      params: z.strictObject({ ...statsRange, sip: z.string().optional(), ...skipLimit }),
      kind: "read",
      narrowHint: statsHint,
    }),
  ],
);
