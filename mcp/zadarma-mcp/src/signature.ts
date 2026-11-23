/**
 * Zadarma request signature (https://zadarma.com/support/api/, "Authorization"):
 *
 *   query     = http_build_query(ksort(params))          (RFC 1738)
 *   signature = base64( hex( HMAC-SHA1(path + query + md5(query), secret) ) )
 *
 * The documented PHP example base64-encodes the *hex* HMAC string
 * (`hash_hmac` without the binary flag), and the official TypeScript client
 * does the same, so this does too. File fields are not part of the signature.
 */
import { createHash, createHmac } from "node:crypto";

import { buildQuery, type ParamRecord, sortTopLevel } from "./encode.js";

export interface SignedQuery {
  /** The sorted, encoded parameter string that was signed. */
  readonly query: string;
  /** Value for the `Authorization` header: `<key>:<signature>`. */
  readonly authorization: string;
}

export function signature(path: string, query: string, secret: string): string {
  const md5 = createHash("md5").update(query).digest("hex");
  const hmacHex = createHmac("sha1", secret).update(path + query + md5).digest("hex");
  return Buffer.from(hmacHex, "utf8").toString("base64");
}

export function signRequest(path: string, params: ParamRecord, key: string, secret: string): SignedQuery {
  const query = buildQuery(sortTopLevel(params));
  return { query, authorization: `${key}:${signature(path, query, secret)}` };
}
