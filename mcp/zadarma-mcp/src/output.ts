/**
 * Keeps tool output a manageable size (R5.3): when a result is too large, the
 * longest list in it is shortened and a note says how to narrow the request.
 */
import { isRecord } from "./client.js";

export const MAX_OUTPUT_CHARS = 40_000;
const DEFAULT_HINT = "use the action's filters or paging (skip/limit, take/skip, start/end)";

interface ListLocation {
  readonly key: string | undefined;
  readonly items: readonly unknown[];
}

/** The longest array at the top level or one level down. */
function longestList(data: unknown): ListLocation | undefined {
  if (Array.isArray(data)) {
    return { key: undefined, items: data };
  }
  if (!isRecord(data)) {
    return undefined;
  }
  let best: ListLocation | undefined;
  for (const [key, value] of Object.entries(data)) {
    if (Array.isArray(value) && (best === undefined || value.length > best.items.length)) {
      best = { key, items: value };
    }
  }
  return best;
}

function withList(data: unknown, key: string | undefined, items: readonly unknown[]): unknown {
  if (key === undefined || !isRecord(data)) {
    return items;
  }
  return { ...data, [key]: items };
}

export function formatResult(data: unknown, narrowHint: string | undefined, max: number = MAX_OUTPUT_CHARS): string {
  const full = JSON.stringify(data);
  if (full.length <= max) {
    return full;
  }
  const hint = narrowHint ?? DEFAULT_HINT;
  const list = longestList(data);
  if (list !== undefined && list.items.length > 1) {
    let count = list.items.length;
    while (count > 1) {
      count = Math.floor(count / 2);
      const shown = withList(data, list.key, list.items.slice(0, count));
      const text = JSON.stringify(shown);
      if (text.length <= max) {
        const where = list.key === undefined ? "the result" : `"${list.key}"`;
        return JSON.stringify({
          truncated: `Showing the first ${count} of ${list.items.length} items in ${where}. To see the rest, ${hint}.`,
          result: shown,
        });
      }
    }
  }
  return JSON.stringify({
    truncated: `The result is ${full.length} characters; showing the first ${max}. To narrow it, ${hint}.`,
    result_text: full.slice(0, max),
  });
}
