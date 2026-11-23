/**
 * Runtime settings, read from environment variables. The Claude desktop app
 * fills them from the extension's user_config (see manifest.json). The key and
 * secret are never logged, returned in tool output or written to a file.
 */

export const API_BASE_URL = "https://api.zadarma.com";
export const REQUEST_TIMEOUT_MS = 30_000;

export interface ZadarmaConfig {
  readonly apiKey: string;
  readonly apiSecret: string;
  readonly baseUrl: string;
  readonly timeoutMs: number;
}

export type ConfigResult =
  | { readonly ok: true; readonly config: ZadarmaConfig }
  | { readonly ok: false; readonly error: string };

type Env = Readonly<Record<string, string | undefined>>;

/**
 * A value counts as unset when it is missing, blank, or an unsubstituted
 * `${user_config.*}` placeholder left by a host that did not fill it in.
 */
function readSetting(env: Env, name: string): string {
  const raw = env[name];
  if (raw === undefined) {
    return "";
  }
  const value = raw.trim();
  return value === "" || value.startsWith("${") ? "" : value;
}

export function loadConfig(env: Env = process.env): ConfigResult {
  const apiKey = readSetting(env, "ZADARMA_API_KEY");
  const apiSecret = readSetting(env, "ZADARMA_API_SECRET");
  const missing: string[] = [];
  if (apiKey === "") {
    missing.push("\"API key\"");
  }
  if (apiSecret === "") {
    missing.push("\"API secret\"");
  }
  if (missing.length > 0) {
    return {
      ok: false,
      error:
        `Zadarma is not configured: fill in ${missing.join(" and ")} in the Zadarma extension settings ` +
        "(Claude desktop app > Settings > Extensions > Zadarma). The keys are in your Zadarma account under Settings > API.",
    };
  }
  return { ok: true, config: { apiKey, apiSecret, baseUrl: API_BASE_URL, timeoutMs: REQUEST_TIMEOUT_MS } };
}
