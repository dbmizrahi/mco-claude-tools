/**
 * Virtual numbers, SMS, WebRTC widget, eSIM, Verify and speech recognition.
 * API reference sections of the same names.
 */
import { z } from "zod";

import { language, none, onOff, pathId, phone, positiveInt } from "./common.js";
import { defineAction, defineTool, type ToolDef } from "./define.js";

export const numbersTool: ToolDef = defineTool(
  "zadarma_numbers",
  "Zadarma virtual numbers",
  "Virtual (direct) numbers: list and details, auto-renewal, Caller name, routing to a SIP, ordering and prolonging, SMS reception, incoming channels. " +
    "Ordering needs a documents group, which is created in the Zadarma web account.",
  [
    defineAction("list", {
      description: "The account's virtual numbers with status, routing and paid-till date.",
      method: "GET",
      path: "/v1/direct_numbers/",
      params: none,
      kind: "read",
    }),
    defineAction("info", {
      description: "Details of one purchased number.",
      method: "GET",
      path: "/v1/direct_numbers/number/",
      params: z.strictObject({ number: phone }),
      kind: "read",
    }),
    defineAction("get_autoprolongation", {
      description: "Auto-renewal status of a number.",
      method: "GET",
      path: "/v1/direct_numbers/autoprolongation/",
      params: z.strictObject({ number: phone }),
      kind: "read",
    }),
    defineAction("set_autoprolongation", {
      description: "Turn auto-renewal of a number on or off. Off means the number is lost when its paid period ends.",
      method: "PUT",
      path: "/v1/direct_numbers/autoprolongation/",
      params: z.strictObject({ number: phone, value: onOff }),
      kind: "write",
      dangerousWhen: (args) => args.value === "off",
      risk: "with auto-renewal off the number is released when its paid period ends",
    }),
    defineAction("checking_wrongs", {
      description: "Document or address verification errors of a documents group.",
      method: "GET",
      path: "/v1/direct_numbers/checking-wrongs/",
      params: z.strictObject({ group_id: positiveInt }),
      kind: "read",
    }),
    defineAction("countries", {
      description: "Countries where numbers can be ordered.",
      method: "GET",
      path: "/v1/direct_numbers/countries/",
      params: z.strictObject({ language: z.string().optional() }),
      kind: "read",
    }),
    defineAction("country", {
      description: "Destinations (cities, types) in a country (ISO 3166-1 alpha-2), or one destination (direction_id).",
      method: "GET",
      path: "/v1/direct_numbers/country/",
      params: z.strictObject({
        country: z.string().regex(/^[A-Za-z]{2}$/, "two-letter country code"),
        language: z.string().optional(),
        direction_id: positiveInt.optional(),
      }),
      kind: "read",
    }),
    defineAction("set_caller_name", {
      description: "Caller name of a number (latin letters and digits, up to 30); an empty string clears it.",
      method: "PUT",
      path: "/v1/direct_numbers/set_caller_name/",
      params: z.strictObject({
        number: phone,
        caller_name: z.string().regex(/^[A-Za-z0-9 ]{0,30}$/, "latin letters and digits, up to 30 characters"),
      }),
      kind: "write",
    }),
    defineAction("set_sip_id", {
      description: "Route a number to a SIP number or external SIP URI; test_mode on|off.",
      method: "PUT",
      path: "/v1/direct_numbers/set_sip_id/",
      params: z.strictObject({ number: phone, sip_id: z.string().min(1), test_mode: onOff.optional() }),
      kind: "write",
    }),
    defineAction("available", {
      description: "Numbers available to order in a destination; mask filters by digits.",
      method: "GET",
      path: "/v1/direct_numbers/available/{direction_id}/",
      params: z.strictObject({ direction_id: pathId, mask: z.string().regex(/^[0-9]{1,15}$/).optional() }),
      kind: "read",
    }),
    defineAction("order", {
      description:
        "Order a number: direction_id, documents_group_id, number_id (from available, if the destination allows choosing), " +
        "purpose (if required), receive_sms, period month|3month, autorenew_period month|year.",
      method: "POST",
      path: "/v1/direct_numbers/order/",
      params: z.strictObject({
        direction_id: positiveInt,
        documents_group_id: positiveInt,
        number_id: z.string().optional(),
        purpose: z.string().optional(),
        receive_sms: z.boolean().optional(),
        period: z.enum(["month", "3month"]).optional(),
        autorenew_period: z.enum(["month", "year"]).optional(),
      }),
      kind: "dangerous",
      risk: "orders a paid number; the cost is charged to the Zadarma balance",
      toParams: (args) => ({ ...args, receive_sms: args.receive_sms === true ? 1 : undefined }),
    }),
    defineAction("prolong", {
      description: "Prepay a number for a number of months.",
      method: "POST",
      path: "/v1/direct_numbers/prolong/",
      params: z.strictObject({ number: phone, months: z.number().int().min(1).max(36) }),
      kind: "dangerous",
      risk: "charges the Zadarma balance for the prepaid months",
    }),
    defineAction("set_receive_sms", {
      description: "Turn SMS reception on a number on or off (only numbers that support it).",
      method: "PUT",
      path: "/v1/direct_numbers/receive_sms/",
      params: z.strictObject({ number: phone, value: onOff, documents_group_id: positiveInt.optional() }),
      kind: "write",
      dangerousWhen: (args) => args.value === "on",
      risk: "SMS reception may be paid",
    }),
    defineAction("incoming_channels_info", {
      description: "Whether and for how much the incoming channels of a number (or destination) can be increased.",
      method: "GET",
      path: "/v1/direct_numbers/incoming_channels/",
      params: z
        .strictObject({ number: phone.optional(), direction_id: positiveInt.optional(), currency: z.string().optional() })
        .refine((v) => v.number !== undefined || v.direction_id !== undefined, { message: "give number or direction_id" }),
      kind: "read",
    }),
    defineAction("set_incoming_channels", {
      description: "Increase the number of incoming channels of a number.",
      method: "PUT",
      path: "/v1/direct_numbers/incoming_channels/",
      params: z.strictObject({ number: phone, channels: z.number().int().min(1).max(100) }),
      kind: "dangerous",
      risk: "extra channels are paid",
    }),
  ],
);

export const smsTool: ToolDef = defineTool(
  "zadarma_sms",
  "Zadarma SMS",
  "Send SMS, list SMS templates, and list allowed senders for a number.",
  [
    defineAction("send", {
      description:
        "Send an SMS to one or more numbers. sender: a virtual number or text from sender_ids; long text is split into several SMS.",
      method: "POST",
      path: "/v1/sms/send/",
      params: z.strictObject({
        number: z.array(phone).min(1).max(100),
        message: z.string().min(1).max(1600),
        sender: z.string().optional(),
        language: z.string().optional(),
      }),
      kind: "dangerous",
      risk: "sends paid SMS to other people",
      toParams: (args) => ({ ...args, number: args.number.join(",") }),
    }),
    defineAction("templates", {
      description: "List SMS templates.",
      method: "GET",
      path: "/v1/sms/templates/",
      params: z.strictObject({
        skip: z.number().int().min(0).optional(),
        limit: z.number().int().min(1).max(1000).optional(),
        language: language.optional(),
      }),
      kind: "read",
      narrowHint: "use skip/limit",
    }),
    defineAction("sender_ids", {
      description: "Allowed SMS senders for a destination number.",
      method: "GET",
      path: "/v1/sms/senderid/",
      params: z.strictObject({ phones: phone }),
      kind: "read",
    }),
  ],
);

export const webrtcTool: ToolDef = defineTool(
  "zadarma_webrtc",
  "Zadarma WebRTC widget",
  "WebRTC web-phone widget: key for a SIP or extension, create/show/change/delete the integration, allowed domains.",
  [
    defineAction("get_key", {
      description: "Key for the widget for a SIP login or extension (valid 72 hours).",
      method: "GET",
      path: "/v1/webrtc/get_key/",
      params: z.strictObject({ sip: z.string().min(1) }),
      kind: "read",
    }),
    defineAction("create", {
      description: "Create the widget integration for a domain.",
      method: "POST",
      path: "/v1/webrtc/create/",
      params: z.strictObject({ domain: z.string().min(3) }),
      kind: "write",
    }),
    defineAction("get", {
      description: "Show the widget integration settings.",
      method: "GET",
      path: "/v1/webrtc/",
      params: none,
      kind: "read",
    }),
    defineAction("update", {
      description: "Change the widget: shape square|rounded; position top_left|top_right|bottom_right|bottom_left.",
      method: "PUT",
      path: "/v1/webrtc/",
      params: z.strictObject({
        shape: z.enum(["square", "rounded"]).optional(),
        position: z.enum(["top_left", "top_right", "bottom_right", "bottom_left"]).optional(),
      }),
      kind: "write",
    }),
    defineAction("add_domain", {
      description: "Allow the widget on another domain.",
      method: "POST",
      path: "/v1/webrtc/domain/",
      params: z.strictObject({ domain: z.string().min(3) }),
      kind: "write",
    }),
    defineAction("remove_domain", {
      description: "Remove a domain from the widget integration.",
      method: "DELETE",
      path: "/v1/webrtc/domain/",
      params: z.strictObject({ domain: z.string().min(3) }),
      kind: "dangerous",
      risk: "the widget stops working on that domain",
    }),
    defineAction("delete", {
      description: "Delete the widget integration.",
      method: "DELETE",
      path: "/v1/webrtc/",
      params: none,
      kind: "dangerous",
      risk: "deletes the widget integration; this cannot be undone",
    }),
  ],
);

export const esimTool: ToolDef = defineTool(
  "zadarma_esim",
  "Zadarma eSIM",
  "eSIM data packages: supported devices, available packages, connected packages, order a package.",
  [
    defineAction("devices", {
      description: "Devices that support eSIM, by brand.",
      method: "GET",
      path: "/v1/esim/devices/",
      params: none,
      kind: "read",
    }),
    defineAction("packages", {
      description: "Available eSIM packages (countries, data, duration, price).",
      method: "GET",
      path: "/v1/esim/packages/",
      params: none,
      kind: "read",
    }),
    defineAction("orders", {
      description: "Connected eSIM packages.",
      method: "GET",
      path: "/v1/esim/order/",
      params: none,
      kind: "read",
    }),
    defineAction("order", {
      description: "One connected package by ICCID (status, remaining data, activation code).",
      method: "GET",
      path: "/v1/esim/order/{iccid}/",
      params: z.strictObject({ iccid: pathId }),
      kind: "read",
    }),
    defineAction("create_order", {
      description: "Connect (buy) an eSIM package by package_id from packages.",
      method: "POST",
      path: "/v1/esim/order/create/",
      params: z.strictObject({ package_id: z.string().min(1) }),
      kind: "dangerous",
      risk: "buys an eSIM package; the price is charged to the Zadarma balance",
    }),
  ],
);

const verifyCode = z.number().int().min(100000).max(999999).optional();

export const verifyTool: ToolDef = defineTool(
  "zadarma_verify",
  "Zadarma Verify",
  "Send a verification code by SMS, call or email (or a press-1 call), and check the code. A request is valid for 10 minutes.",
  [
    defineAction("send", {
      description:
        "Send a verification request. channel sms|call_code|email|call_button; `to` is E.164 or an email. " +
        "code: six digits (generated if omitted). call_button needs three IVR sound IDs and is checked via the NOTIFY_OUT_END webhook, not check.",
      method: "POST",
      path: "/v1/verify/",
      params: z.discriminatedUnion("channel", [
        z.strictObject({
          channel: z.literal("sms"),
          to: phone,
          code: verifyCode,
          language: language.optional(),
          template_id: positiveInt.optional(),
          caller_id: z.string().optional(),
        }),
        z.strictObject({
          channel: z.literal("call_code"),
          to: phone,
          from: phone.optional(),
          code: verifyCode,
          language: language.optional(),
        }),
        z.strictObject({
          channel: z.literal("email"),
          to: z.email(),
          from: z.email().optional(),
          code: verifyCode,
          language: language.optional(),
          email_subject: z.string().optional(),
          email_body: z
            .string()
            .refine((v) => v.includes("{#code#}"), { message: 'must contain "{#code#}"' })
            .optional(),
        }),
        z.strictObject({
          channel: z.literal("call_button"),
          to: phone,
          from: phone.optional(),
          greeting_sound_id: z.string().min(1),
          button_1_sound_id: z.string().min(1),
          fallback_sound_id: z.string().min(1),
        }),
      ]),
      kind: "dangerous",
      risk: "sends a paid SMS, call or email to another person",
    }),
    defineAction("check", {
      description: "Check a code against a request_id from send (sms, call_code and email channels).",
      method: "POST",
      path: "/v1/verify/check/",
      params: z.strictObject({ request_id: z.string().min(1), code: z.number().int().min(0).max(999999) }),
      kind: "write",
    }),
  ],
);

export const speechTool: ToolDef = defineTool(
  "zadarma_speech_recognition",
  "Zadarma speech recognition",
  "Speech recognition of PBX call recordings: get the result, or start recognition (manual recognition must be enabled on the extension).",
  [
    defineAction("get", {
      description: "Recognition result for a call: return words|phrases (default phrases); alternatives 0|1.",
      method: "GET",
      path: "/v1/speech_recognition/",
      params: z.strictObject({
        call_id: z.string().min(1),
        lang: z.string().optional(),
        return: z.enum(["words", "phrases"]).optional(),
        alternatives: z.union([z.literal(0), z.literal(1)]).optional(),
      }),
      kind: "read",
    }),
    defineAction("start", {
      description: "Start recognition of a call recording.",
      method: "PUT",
      path: "/v1/speech_recognition/",
      params: z.strictObject({ call_id: z.string().min(1), lang: z.string().optional() }),
      kind: "dangerous",
      risk: "speech recognition is billed (uses price-plan seconds or the balance)",
    }),
  ],
);
