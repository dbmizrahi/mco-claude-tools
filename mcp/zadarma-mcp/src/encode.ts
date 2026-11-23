/**
 * Request parameter encoding that matches PHP's
 * `http_build_query($params, '', '&', PHP_QUERY_RFC1738)`, which is what
 * Zadarma's documented signing example and official PHP client use.
 */

/** A parameter value as it is sent to Zadarma. Nested values become `a[b]=c`. */
export type ParamValue =
  | string
  | number
  | boolean
  | null
  | undefined
  | readonly ParamValue[]
  | { readonly [key: string]: ParamValue };

export type ParamRecord = { readonly [key: string]: ParamValue };

/**
 * PHP `urlencode`: everything except ASCII letters, digits and `-_.` is
 * percent-encoded (upper-case hex), and a space becomes `+`.
 */
export function phpUrlencode(value: string): string {
  return encodeURIComponent(value)
    .replace(/[!'()*~]/g, (ch) => `%${ch.charCodeAt(0).toString(16).toUpperCase()}`)
    .replace(/%20/g, "+");
}

function scalarToString(value: string | number | boolean): string {
  if (typeof value === "boolean") {
    return value ? "1" : "0"; // PHP http_build_query
  }
  return String(value);
}

function isParamArray(value: ParamValue): value is readonly ParamValue[] {
  return Array.isArray(value);
}

/** Flattens a value into `[key, value]` pairs in PHP order; null/undefined are skipped. */
export function flattenParams(params: ParamRecord, prefix?: string): Array<[string, string]> {
  const pairs: Array<[string, string]> = [];
  const visit = (key: string, value: ParamValue): void => {
    if (value === null || value === undefined) {
      return;
    }
    if (isParamArray(value)) {
      value.forEach((item, index) => visit(`${key}[${index}]`, item));
      return;
    }
    if (typeof value === "object") {
      for (const [child, childValue] of Object.entries(value)) {
        visit(`${key}[${child}]`, childValue);
      }
      return;
    }
    pairs.push([key, scalarToString(value)]);
  };
  for (const [key, value] of Object.entries(params)) {
    visit(prefix === undefined ? key : `${prefix}[${key}]`, value);
  }
  return pairs;
}

export function buildQuery(params: ParamRecord): string {
  return flattenParams(params)
    .map(([key, value]) => `${phpUrlencode(key)}=${phpUrlencode(value)}`)
    .join("&");
}

/** Top-level keys sorted by name (PHP `ksort`); nested values keep their order. */
export function sortTopLevel(params: ParamRecord): ParamRecord {
  const sorted: { [key: string]: ParamValue } = {};
  for (const key of Object.keys(params).sort()) {
    sorted[key] = params[key];
  }
  return sorted;
}
