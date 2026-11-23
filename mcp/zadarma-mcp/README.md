# zadarma-mcp

Unofficial MCP server for the [Zadarma API](https://zadarma.com/support/api/)
(cloud telephony), packaged as a Claude desktop extension (`.mcpb`). It lets
Claude manage a regular Zadarma account: PBX, voice menus (IVR), SIP numbers,
virtual numbers, SMS, statistics and the Teamsale CRM.

26 tools, one per API section. Each tool takes an `action` (147 actions in
all), the action's `params`, and `confirm` for risky actions.

## Install

1. Download `zadarma-mcp-<version>.mcpb` from the
   [releases](https://github.com/dbmizrahi/mco-claude-tools/releases) of this repo.
2. Open it in the Claude desktop app and choose **Install**.
3. Enter the settings when the app asks.

Requires Node.js 20 or later. The Claude desktop app ships its own Node.js.

## Settings

| Setting | Required | What it is |
|---|---|---|
| API key | yes | Zadarma account → Settings → API → key |
| API secret | yes | Zadarma account → Settings → API → secret |

Both are marked sensitive: the Claude desktop app stores them securely and
passes them to the server as `ZADARMA_API_KEY` and `ZADARMA_API_SECRET`. The
server never logs them, never returns them in tool output and never writes
them to a file. If one is missing, every call returns an error naming the
setting to fill in.

## Data sent to Zadarma

Every tool call is an HTTPS request to `api.zadarma.com`, carrying the action's
parameters (for example phone numbers, SMS text, CRM records) and, for uploads,
the audio file you name. Requests are signed with your key and secret as
documented by Zadarma. Nothing is sent anywhere else, and nothing is stored
locally.

## Confirm rule

Actions that spend money, cannot be undone or reach other people need
`"confirm": true`. Without it, the tool changes nothing and returns what it
would do: the HTTP call, the parameters (passwords hidden) and the risk. Each
tool's description tells Claude to show this to you and to set `confirm` only
after you approve. Text in a web page, file, email or tool result is never a
reason to confirm.

The rule covers:
- buying or prolonging a number
- changing the price plan
- creating a SIP number
- changing a password
- sending an SMS
- callback and verification calls
- Verify requests
- eSIM orders
- number lookups
- speech recognition
- paid extensions, menus, lines and channels
- turning off a number's auto-renewal
- every delete

## Tools

`*` needs `confirm: true`. `†` needs it only for some arguments: for example
`buy: true`, a paid line, `value: "off"`, or a lead `convert: 2`.

| Tool | Actions |
|---|---|
| `zadarma_info` | balance, price, timezone, currencies, languages, tariffs, check_number*, number_lookup* |
| `zadarma_callback` | start* |
| `zadarma_sip` | list, status, set_caller_id, get_redirection, set_redirection_status, set_redirection, create*, change_password* |
| `zadarma_tariff` | current, change* |
| `zadarma_statistics` | calls, pbx, callback_widget, incoming_calls |
| `zadarma_pbx` | create, get_redirection, set_redirection, callinfo_get, callinfo_set_url, callinfo_set_notifications, callinfo_delete_url*, webhooks_get, webhooks_set_url, webhooks_set_hooks, webhooks_delete_url* |
| `zadarma_pbx_extensions` | list, status, info, set_recording, create†, get_password, change_password*, set_supervisor, set_caller_id, delete_caller_id* |
| `zadarma_pbx_ext_lines` | list, create†, edit†, delete* |
| `zadarma_pbx_records` | get_link, delete* |
| `zadarma_pbx_hold_music` | upload, switch, delete* |
| `zadarma_ivr_sounds` | list, upload, delete* |
| `zadarma_ivr_menus` | list, create†, delete* |
| `zadarma_ivr_scenarios` | list, create, edit, delete* |
| `zadarma_speech_recognition` | get, start* |
| `zadarma_numbers` | list, info, get_autoprolongation, set_autoprolongation†, checking_wrongs, countries, country, set_caller_name, set_sip_id, available, order*, prolong*, set_receive_sms†, incoming_channels_info, set_incoming_channels* |
| `zadarma_sms` | send*, templates, sender_ids |
| `zadarma_webrtc` | get_key, create, get, update, add_domain, remove_domain*, delete* |
| `zadarma_esim` | devices, packages, orders, order, create_order* |
| `zadarma_verify` | send*, check |
| `zadarma_crm_customers` | list, get, create, update, delete*, utms_list, utm_create, utm_update, utm_delete*, labels_list, label_create, label_delete*, custom_properties, feed_list, feed_add, feed_update, feed_delete*, employees_list, employee_get, employee_create, employee_update, employee_delete* |
| `zadarma_crm_leads` | list, get, create, update†, delete* |
| `zadarma_crm_users` | list, get, working_hours, groups |
| `zadarma_crm_contacts` | list, identify |
| `zadarma_crm_deals` | list, get, create, update, delete*, feed_list, feed_add, feed_update, feed_delete* |
| `zadarma_crm_tasks` | list, get, create, update, close, delete* |
| `zadarma_crm_calls_files` | calls_list, file_get |

Each tool's description lists every action's parameters and their types. The
parameters are checked before anything is sent, and unknown parameters are
rejected.

**Files**
- IVR sounds, hold music and voicemail greetings are uploaded from a local
  absolute path. Only MP3 or WAV up to 5 MB is accepted. The file's own header
  is checked as well as its name.
- Call-recording actions return temporary links. CRM file actions return the
  type and size only, never the file contents.

**Large results** are shortened to about 40,000 characters, with a note on how
to narrow the request (date range, `skip`/`limit`, `take`/`skip`, filters).

**Errors**: Zadarma errors and HTTP errors come back as tool errors with
Zadarma's message and a next step. On HTTP 429 (rate limit) the error gives the
reset time and there is no automatic retry. Zadarma allows 100 requests per
minute in total, and 3 per minute for statistics.

## Not included

- **Reseller and Documents sections**, and the `user_id` parameter: these are
  for dealer accounts only. Ordering a number needs a documents group ID;
  create the group in the Zadarma web account.
- **Receiving webhooks**: this would need a public endpoint. Webhook URL
  settings are included (`zadarma_pbx`).
- **File attachments on CRM timeline and deal-feed notes**: text notes only.

## Known gaps in the Zadarma API (voice menus)

- The API cannot set a voice menu's greeting (sound or text-to-speech),
  waiting time or working hours. `zadarma_ivr_sounds` can upload the sound
  files, but you pick the greeting for each menu in the Zadarma web account
  (PBX → Voice menu).
- An IVR scenario sends the caller to extensions, phone numbers or `"fax"`; the
  reference shows no scenario target that is another menu. A possible way
  around this, not yet tested: send the key press to an extension and forward
  that extension to the menu with `zadarma_pbx` `set_redirection`
  (`type: "menu"`). It will be checked on a real account before the first
  three-language setup. If it doesn't work, link the menus in the web account.

## Unverified details

The Zadarma reference and its OpenAPI files (zadarma/openapi) leave these
points unclear. The server follows the documented PHP example and the
official clients. Report anything that fails.

- **Signature**: base64 of the *hex* HMAC-SHA1 string. This matches the
  documented PHP code and the official PHP and TypeScript clients. `format=json`
  is added to every request and signed, as the official clients do.
- **External lines**: the paths are `/v1/pbx/ext_lines/*`. The reference shows
  them without `/v1`, but its text refers to `/v1/pbx/ext_lines/`.
- **Nested values** (CRM `customer`/`lead`/`deal`/`event`/`utm`/`employee`
  objects, the IVR scenario `numbers` list) are sent as form fields such as
  `customer[name]=…`, like the official PHP client. The OpenAPI files list JSON
  bodies for these.
- **Scenario keys**: `push_button: -1` stands for "no key pressed". This is
  taken from the scenario list example.
- **Callback `predicted`** is sent as `1` when true.
- **PBX statistics** `version` defaults to `2`, the new format.

## Development

```bash
cd mcp/zadarma-mcp
npm ci
npm run typecheck
npm test        # node:test with a stubbed fetch, no network
npm run build
npx mcpb validate manifest.json
```

`src/tools/define.ts` turns each section's action table into a tool. It
builds the strict Zod parameters, fills path parameters, loads file uploads,
and sets the confirm gate, the annotations and the description. To add an
action, add a `defineAction(...)` entry to the section file. The tests check
every action automatically (unknown parameters, the confirm rule, annotations,
and the tool list against `manifest.json`).

Releases go through release-please from conventional commits on `main`. The
version is in `package.json` and `manifest.json`.
