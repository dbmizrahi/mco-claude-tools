/**
 * PBX voice menus (IVR): sounds, menus and scenarios. API reference section
 * "PBX (IVR)". Note: the API has no method to set a menu's greeting or
 * timeout, and a scenario's target is extensions, phone numbers or "fax";
 * those menu settings are made in the Zadarma web account.
 */
import { z } from "zod";

import { audioFilePath, none, positiveInt } from "./common.js";
import { defineAction, defineTool, type ToolDef } from "./define.js";

export const ivrSoundsTool: ToolDef = defineTool(
  "zadarma_ivr_sounds",
  "Zadarma IVR sounds",
  "Voice-menu (IVR) sound files: list, upload (MP3 or WAV, up to 5 MB, from a local path) and delete.",
  [
    defineAction("list", {
      description: "List uploaded IVR sound files with their IDs.",
      method: "GET",
      path: "/v1/pbx/ivr/sounds/list",
      params: none,
      kind: "read",
    }),
    defineAction("upload", {
      description: "Upload a local MP3 or WAV file (up to 5 MB) as an IVR sound.",
      method: "POST",
      path: "/v1/pbx/ivr/sounds/upload",
      params: z.strictObject({ name: z.string().min(1).max(100), file_path: audioFilePath }),
      kind: "write",
      files: { file_path: "file" },
    }),
    defineAction("delete", {
      description: "Delete an IVR sound file by its ID.",
      method: "DELETE",
      path: "/v1/pbx/ivr/sounds/delete",
      params: z.strictObject({ id: z.string().min(1) }),
      kind: "dangerous",
      risk: "deletes the sound file; this cannot be undone",
    }),
  ],
);

export const ivrMenusTool: ToolDef = defineTool(
  "zadarma_ivr_menus",
  "Zadarma IVR menus",
  "Voice menus (IVR) of the PBX: list (with status, type and working hours), create, delete. Menu 0 is the main menu.",
  [
    defineAction("list", {
      description: "List voice menus with their settings.",
      method: "GET",
      path: "/v1/pbx/ivr/",
      params: none,
      kind: "read",
    }),
    defineAction("create", {
      description: "Create a voice menu. buy: true creates a paid menu when the free ones are used up.",
      method: "POST",
      path: "/v1/pbx/ivr/create/",
      params: z.strictObject({ buy: z.boolean().optional() }),
      kind: "write",
      dangerousWhen: (args) => args.buy === true,
      risk: "buy: true charges the Zadarma balance for a paid menu",
      toParams: (args) => ({ buy: args.buy === true ? "true" : "false" }),
    }),
    defineAction("delete", {
      description: "Delete a voice menu (menu_id > 0; the main menu 0 cannot be deleted).",
      method: "DELETE",
      path: "/v1/pbx/ivr/delete/",
      params: z.strictObject({ menu_id: positiveInt }),
      kind: "dangerous",
      risk: "deletes the menu and its scenarios; this cannot be undone",
    }),
  ],
);

const queueStrategy = z.enum(["off", "random", "roundrobin", "leastrecent", "rrmemory", "fewestcalls"]);

export const ivrScenariosTool: ToolDef = defineTool(
  "zadarma_ivr_scenarios",
  "Zadarma IVR scenarios",
  "Scenarios of a voice menu: what happens on a key press (or no press). " +
    "push_button: -1 = no key pressed, 0-9 = keys, 10 = autoresponder, 11-30 = additional scenarios. " +
    "A scenario rings extensions or phone numbers (space-separated) or \"fax\".",
  [
    defineAction("list", {
      description: "List the scenarios of a menu.",
      method: "GET",
      path: "/v1/pbx/ivr/scenario/",
      params: z.strictObject({ menu_id: z.number().int().min(0) }),
      kind: "read",
    }),
    defineAction("create", {
      description:
        "Create a scenario in a menu. Optional triggers limit it to calls to given numbers or external lines, or from given caller numbers (space-separated).",
      method: "POST",
      path: "/v1/pbx/ivr/scenario/create/",
      params: z.strictObject({
        menu_id: z.number().int().min(0),
        push_button: z.number().int().min(-1).max(30),
        title: z.string().min(1).max(100),
        extension: z.string().min(1).describe('extension(s) or phone numbers separated by spaces, or "fax"'),
        trigger_to_did_numbers: z.string().optional(),
        trigger_to_did_ext_lines: z.string().optional(),
        trigger_from_clid_numbers: z.string().optional(),
      }),
      kind: "write",
      toParams: (args) => ({ ...args, push_button: String(args.push_button) }),
    }),
    defineAction("edit", {
      description:
        "Change a scenario: title, queue strategy and the extensions it rings. delay/duration (seconds) apply only with queue_strategy \"off\".",
      method: "PUT",
      path: "/v1/pbx/ivr/scenario/edit/",
      params: z.strictObject({
        id: z.string().min(1),
        title: z.string().min(1).max(100).optional(),
        queue_strategy: queueStrategy.optional(),
        queue_announce_position: z.union([z.literal(0), z.literal(1)]).optional(),
        numbers: z
          .array(
            z.strictObject({
              number: z.string().min(1).describe('extension or "fax"'),
              delay: z.number().int().min(0).optional(),
              duration: z.number().int().min(1).optional(),
            }),
          )
          .optional(),
      }),
      kind: "write",
    }),
    defineAction("delete", {
      description: "Delete a scenario by its ID.",
      method: "DELETE",
      path: "/v1/pbx/ivr/scenario/delete/",
      params: z.strictObject({ scenario_id: z.string().min(1) }),
      kind: "dangerous",
      risk: "deletes the scenario; this cannot be undone",
    }),
  ],
);
