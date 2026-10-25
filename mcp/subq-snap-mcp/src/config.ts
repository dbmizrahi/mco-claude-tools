/**
 * Runtime settings, read from environment variables. The Claude desktop app
 * fills them from the extension's user_config (see manifest.json); every
 * setting has a default, and an empty API key means "not configured".
 */

export interface SubqConfig {
  readonly apiKey: string;
  readonly apiUrl: string;
  readonly model: string;
  readonly timeoutMs: number;
}

export const DEFAULT_API_URL = "https://api.subq.ai/v1/systemone";
export const DEFAULT_MODEL = "subq-snap-1.1";
export const DEFAULT_TIMEOUT_SECONDS = 30;
export const MIN_TIMEOUT_SECONDS = 1;
export const MAX_TIMEOUT_SECONDS = 120;

type Env = Readonly<Record<string, string | undefined>>;

/**
 * A value counts as unset when it is missing, blank, or an unsubstituted
 * `${user_config.*}` placeholder left by a host that did not fill it in.
 */
function readString(env: Env, name: string, fallback: string): string {
  const raw = env[name];
  if (raw === undefined) {
    return fallback;
  }
  const value = raw.trim();
  if (value === "" || value.startsWith("${")) {
    return fallback;
  }
  return value;
}

function readTimeoutMs(env: Env): number {
  const raw = readString(env, "SUBQ_TIMEOUT_SECONDS", "");
  const seconds = raw === "" ? DEFAULT_TIMEOUT_SECONDS : Number(raw);
  if (!Number.isFinite(seconds) || seconds < MIN_TIMEOUT_SECONDS || seconds > MAX_TIMEOUT_SECONDS) {
    return DEFAULT_TIMEOUT_SECONDS * 1000;
  }
  return Math.round(seconds * 1000);
}

export function loadConfig(env: Env = process.env): SubqConfig {
  return {
    apiKey: readString(env, "SUBQ_API_KEY", ""),
    apiUrl: readString(env, "SUBQ_API_URL", DEFAULT_API_URL),
    model: readString(env, "SUBQ_MODEL", DEFAULT_MODEL),
    timeoutMs: readTimeoutMs(env),
  };
}
