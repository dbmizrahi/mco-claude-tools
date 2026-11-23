/**
 * PBX: settings, call forwarding on extensions, call info and webhook URLs,
 * extensions, external lines, call recordings and hold music. API reference
 * sections "PBX", "PBX (extensions)" and "PBX (external lines)".
 */
import { z } from "zod";

import { audioFilePath, extension, none, phone } from "./common.js";
import { defineAction, defineTool, type ToolDef } from "./define.js";

const trueFalse = z.boolean().optional();

export const pbxTool: ToolDef = defineTool(
  "zadarma_pbx",
  "Zadarma PBX",
  "PBX settings: create the PBX, call forwarding on an extension, call-info (NOTIFY_*) and other webhook URLs. " +
    "Receiving webhooks is not part of this tool; it only sets where Zadarma sends them.",
  [
    defineAction("create", {
      description: "Create the PBX. password is for the first extension 100; sip_id picks the SIP to connect (optional).",
      method: "POST",
      path: "/v1/pbx/create/",
      params: z.strictObject({ password: z.string().min(8), sip_id: z.string().optional() }),
      kind: "write",
    }),
    defineAction("get_redirection", {
      description: "Show call forwarding on an extension.",
      method: "GET",
      path: "/v1/pbx/redirection/",
      params: z.strictObject({ pbx_number: extension }),
      kind: "read",
    }),
    defineAction("set_redirection", {
      description:
        "Turn call forwarding on an extension on or off. With status \"on\": type phone|voicemail|menu|sip|sip_uri, " +
        "destination (phone, email, menu or scenario ID, SIP/extension or SIP URI), condition always|noanswer; " +
        "for voicemail, voicemail_greeting no|standart|own and, for own, greeting_file_path (MP3/WAV up to 5 MB).",
      method: "POST",
      path: "/v1/pbx/redirection/",
      params: z
        .strictObject({
          pbx_number: extension,
          status: z.enum(["on", "off"]),
          type: z.enum(["phone", "voicemail", "menu", "sip", "sip_uri"]).optional(),
          destination: z.string().min(1).optional(),
          condition: z.enum(["always", "noanswer"]).optional(),
          voicemail_greeting: z.enum(["no", "standart", "own"]).optional(),
          greeting_file_path: audioFilePath.optional(),
        })
        .superRefine((v, ctx) => {
          if (v.status === "on") {
            for (const key of ["type", "destination", "condition"] as const) {
              if (v[key] === undefined) {
                ctx.addIssue({ code: "custom", path: [key], message: 'required when status is "on"' });
              }
            }
          }
          if (v.greeting_file_path !== undefined && !(v.type === "voicemail" && v.voicemail_greeting === "own")) {
            ctx.addIssue({
              code: "custom",
              path: ["greeting_file_path"],
              message: 'only with type "voicemail" and voicemail_greeting "own"',
            });
          }
        }),
      kind: "write",
      files: { greeting_file_path: "greeting_file" },
    }),
    defineAction("callinfo_get", {
      description: "Show the call-info webhook settings (URL and which NOTIFY_* events are on).",
      method: "GET",
      path: "/v1/pbx/callinfo/",
      params: none,
      kind: "read",
    }),
    defineAction("callinfo_set_url", {
      description: "Set the URL that receives call-info webhooks (NOTIFY_*).",
      method: "POST",
      path: "/v1/pbx/callinfo/url/",
      params: z.strictObject({ url: z.url() }),
      kind: "write",
    }),
    defineAction("callinfo_set_notifications", {
      description: "Turn individual NOTIFY_* call-info webhooks on (true) or off (false).",
      method: "POST",
      path: "/v1/pbx/callinfo/notifications/",
      params: z.strictObject({
        notify_start: trueFalse,
        notify_internal: trueFalse,
        notify_answer: trueFalse,
        notify_end: trueFalse,
        notify_out_start: trueFalse,
        notify_out_end: trueFalse,
      }),
      kind: "write",
    }),
    defineAction("callinfo_delete_url", {
      description: "Remove the call-info webhook URL.",
      method: "DELETE",
      path: "/v1/pbx/callinfo/url/",
      params: none,
      kind: "dangerous",
      risk: "stops call-info webhooks to the current URL",
    }),
    defineAction("webhooks_get", {
      description: "Show the other webhook settings (contact updates, call tracking, SMS, speech analytics).",
      method: "GET",
      path: "/v1/pbx/webhooks/",
      params: none,
      kind: "read",
    }),
    defineAction("webhooks_set_url", {
      description: "Set the URL for the other webhooks.",
      method: "POST",
      path: "/v1/pbx/webhooks/url/",
      params: z.strictObject({ url: z.url() }),
      kind: "write",
    }),
    defineAction("webhooks_set_hooks", {
      description: "Turn the other webhooks on (true) or off (false).",
      method: "POST",
      path: "/v1/pbx/webhooks/hooks/",
      params: z.strictObject({
        number_lookup: trueFalse,
        call_tracking: trueFalse,
        sms: trueFalse,
        speech_recognition: trueFalse,
      }),
      kind: "write",
    }),
    defineAction("webhooks_delete_url", {
      description: "Remove the URL for the other webhooks.",
      method: "DELETE",
      path: "/v1/pbx/webhooks/url/",
      params: none,
      kind: "dangerous",
      risk: "stops the other webhooks to the current URL",
    }),
  ],
);

export const pbxExtensionsTool: ToolDef = defineTool(
  "zadarma_pbx_extensions",
  "Zadarma PBX extensions",
  "PBX extensions (e.g. 100): list, online status, details, call recording, create, passwords, supervisor mode, Caller ID.",
  [
    defineAction("list", {
      description: "List the PBX extensions.",
      method: "GET",
      path: "/v1/pbx/internal/",
      params: none,
      kind: "read",
    }),
    defineAction("status", {
      description: "Online status of an extension.",
      method: "GET",
      path: "/v1/pbx/internal/{extension}/status/",
      params: z.strictObject({ extension }),
      kind: "read",
    }),
    defineAction("info", {
      description: "Details of an extension (name, Caller ID, lines, recording settings).",
      method: "GET",
      path: "/v1/pbx/internal/{extension}/info/",
      params: z.strictObject({ extension }),
      kind: "read",
    }),
    defineAction("set_recording", {
      description:
        "Call recording on an extension: status on|off|on_email|off_email|on_store|off_store; " +
        "email (up to 3, comma-separated); speech_recognition all|optional|off.",
      method: "PUT",
      path: "/v1/pbx/internal/recording/",
      params: z.strictObject({
        id: extension,
        status: z.enum(["on", "off", "on_email", "off_email", "on_store", "off_store"]),
        email: z.string().optional(),
        speech_recognition: z.enum(["all", "optional", "off"]).optional(),
      }),
      kind: "write",
    }),
    defineAction("create", {
      description:
        'Create extensions: start_number 100-999 or "any", quantity; return_password returns the new passwords; ' +
        "buy: true buys extensions over the limit.",
      method: "POST",
      path: "/v1/pbx/internal/create/",
      params: z.strictObject({
        start_number: z.union([z.literal("any"), z.string().regex(/^[1-9][0-9]{2}$/, "100-999")]),
        quantity: z.number().int().min(1).max(100),
        return_password: z.boolean().optional(),
        buy: z.boolean().optional(),
      }),
      kind: "write",
      dangerousWhen: (args) => args.buy === true,
      risk: "buy: true charges the Zadarma balance for extensions over the limit",
    }),
    defineAction("get_password", {
      description: "Show an extension's password (available only for a limited time after it is set).",
      method: "GET",
      path: "/v1/pbx/internal/{extension}/password/",
      params: z.strictObject({ extension }),
      kind: "read",
    }),
    defineAction("change_password", {
      description: "Change an extension's password (value = new password).",
      method: "PUT",
      path: "/v1/pbx/internal/{extension}/password/",
      params: z.strictObject({ extension, value: z.string().min(8) }),
      kind: "dangerous",
      risk: "devices using the old password lose their connection",
    }),
    defineAction("set_supervisor", {
      description: "Supervisor mode on an extension: 1 = on, 0 = off.",
      method: "PUT",
      path: "/v1/pbx/internal/{extension}/edit/",
      params: z.strictObject({ extension, supervisor_status: z.union([z.literal(0), z.literal(1)]) }),
      kind: "write",
    }),
    defineAction("set_caller_id", {
      description: "Set an extension's Caller ID to one of the account's numbers (international format).",
      method: "PUT",
      path: "/v1/pbx/internal/{extension}/callerid/",
      params: z.strictObject({ extension, number: phone }),
      kind: "write",
    }),
    defineAction("delete_caller_id", {
      description: "Remove an extension's Caller ID.",
      method: "DELETE",
      path: "/v1/pbx/internal/{extension}/callerid/",
      params: z.strictObject({ extension }),
      kind: "dangerous",
      risk: "removes the Caller ID setting from the extension",
    }),
  ],
);

const channels = z.enum(["free", "3", "10"]);
const dtmfMode = z.enum(["rfc2833", "info", "inband"]);
const lineName = z.string().regex(/^[A-Za-z0-9 _-]{1,25}$/, "latin letters, digits, space, - and _, up to 25 characters");
const prefix = z.string().regex(/^(\+?[0-9]{0,10})$/, '"+" and up to 10 digits');

const extLineFields = {
  name: lineName,
  connection_type: z.enum(["gateway", "server"]).optional(),
  server: z.string().optional(),
  port: z.number().int().min(1).max(65535).optional(),
  login: z.string().optional(),
  secret: z.string().optional(),
  domain: z.string().optional(),
  contact: z.string().regex(/^[A-Za-z0-9]{0,30}$/).optional(),
  dtmf_mode: dtmfMode.optional(),
  prefix_add: prefix.optional(),
  prefix_remove: prefix.optional(),
};

export const pbxExtLinesTool: ToolDef = defineTool(
  "zadarma_pbx_ext_lines",
  "Zadarma PBX external lines",
  "External lines of the PBX (up to 20, one of them free): list, create, edit, delete. " +
    "connection_type gateway = your device registers on Zadarma; server = Zadarma registers on your SIP server " +
    "(then server, login and secret are required). Paths are /v1/pbx/ext_lines/* (unverified: the reference shows them without /v1).",
  [
    defineAction("list", {
      description: "List external lines (passwords are not returned).",
      method: "GET",
      path: "/v1/pbx/ext_lines/",
      params: none,
      kind: "read",
    }),
    defineAction("create", {
      description: "Create an external line. channels: free (default) or a paid line with 3 or 10 channels.",
      method: "POST",
      path: "/v1/pbx/ext_lines/create/",
      params: z.strictObject({ ...extLineFields, channels: channels.optional() }),
      kind: "write",
      dangerousWhen: (args) => args.channels === "3" || args.channels === "10",
      risk: "a paid line (3 or 10 channels) is charged to the Zadarma balance unless an unused paid period exists",
    }),
    defineAction("edit", {
      description:
        "Change an external line (id from list). Only the given fields change; an empty prefix removes it. " +
        "transfer_name 1/0 passes the line name to the extension; gateway_password sets a new connection password.",
      method: "PUT",
      path: "/v1/pbx/ext_lines/edit/",
      params: z.strictObject({
        id: z.number().int().min(1),
        ...extLineFields,
        name: lineName.optional(),
        channels: channels.optional(),
        transfer_name: z.union([z.literal(0), z.literal(1)]).optional(),
        gateway_password: z.string().min(8).optional(),
      }),
      kind: "write",
      dangerousWhen: (args) => args.channels === "3" || args.channels === "10",
      risk: "changing to a paid line (3 or 10 channels) is charged to the Zadarma balance unless an unused paid period exists",
    }),
    defineAction("delete", {
      description: "Delete an external line (id from list). A paid period is kept for a later line with the same channels.",
      method: "DELETE",
      path: "/v1/pbx/ext_lines/delete/",
      params: z.strictObject({ id: z.number().int().min(1) }),
      kind: "dangerous",
      risk: "deletes the external line; this cannot be undone",
    }),
  ],
);

const recordingIds = z
  .strictObject({
    call_id: z.string().min(1).optional(),
    pbx_call_id: z.string().min(1).optional(),
  })
  .refine((v) => v.call_id !== undefined || v.pbx_call_id !== undefined, {
    message: "give call_id or pbx_call_id",
  });

export const pbxRecordsTool: ToolDef = defineTool(
  "zadarma_pbx_records",
  "Zadarma call recordings",
  "Call recordings: get a temporary download link, or delete recordings. Returns links only, never audio. " +
    "Use call_id (one recording) or pbx_call_id (all recordings of a call) from the PBX statistics.",
  [
    defineAction("get_link", {
      description: "Get download link(s) for a recording; lifetime in seconds (180-5184000, default 1800).",
      method: "GET",
      path: "/v1/pbx/record/request/",
      params: z
        .strictObject({
          call_id: z.string().min(1).optional(),
          pbx_call_id: z.string().min(1).optional(),
          lifetime: z.number().int().min(180).max(5_184_000).optional(),
        })
        .refine((v) => v.call_id !== undefined || v.pbx_call_id !== undefined, {
          message: "give call_id or pbx_call_id",
        }),
      kind: "read",
    }),
    defineAction("delete", {
      description: "Delete recording file(s).",
      method: "DELETE",
      path: "/v1/pbx/record/request/",
      params: recordingIds,
      kind: "dangerous",
      risk: "deletes call recordings permanently",
    }),
  ],
);

export const pbxHoldMusicTool: ToolDef = defineTool(
  "zadarma_pbx_hold_music",
  "Zadarma hold music",
  "Hold music of the PBX (played instead of ringing): upload (MP3 or WAV, up to 5 MB, from a local path), switch, delete.",
  [
    defineAction("upload", {
      description: "Upload a local MP3 or WAV file as hold music.",
      method: "POST",
      path: "/v1/pbx/waitmelody/upload",
      params: z.strictObject({ file_path: audioFilePath }),
      kind: "write",
      files: { file_path: "file" },
    }),
    defineAction("switch", {
      description: "Turn hold music on or off: state on|off; melody none (default ringing) or mymelody (the uploaded file).",
      method: "PUT",
      path: "/v1/pbx/waitmelody/switch",
      params: z.strictObject({ state: z.enum(["on", "off"]), melody: z.enum(["none", "mymelody"]) }),
      kind: "write",
    }),
    defineAction("delete", {
      description: "Delete the uploaded hold music.",
      method: "DELETE",
      path: "/v1/pbx/waitmelody/delete",
      params: none,
      kind: "dangerous",
      risk: "deletes the uploaded hold music; this cannot be undone",
    }),
  ],
);
