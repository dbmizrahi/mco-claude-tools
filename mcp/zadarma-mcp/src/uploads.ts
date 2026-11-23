/**
 * Local audio files for IVR sounds, hold music and voicemail greetings.
 * Zadarma accepts MP3 or WAV up to 5 MB. The file is checked here before
 * anything is sent: path, extension, size and the file's own header, so a
 * file that is not audio is never uploaded, whatever its name.
 */
import { open, stat } from "node:fs/promises";
import { homedir } from "node:os";
import { basename, extname, isAbsolute, join } from "node:path";

export const MAX_UPLOAD_BYTES = 5 * 1024 * 1024;

export interface UploadFile {
  /** Form field name Zadarma expects, e.g. `file`. */
  readonly field: string;
  readonly fileName: string;
  readonly mimeType: "audio/mpeg" | "audio/wav";
  readonly bytes: Uint8Array<ArrayBuffer>;
}

export type UploadResult =
  | { readonly ok: true; readonly file: UploadFile }
  | { readonly ok: false; readonly error: string };

function expandHome(path: string): string {
  return path === "~" || path.startsWith("~/") ? join(homedir(), path.slice(1)) : path;
}

function looksLikeWav(head: Uint8Array): boolean {
  const text = (from: number, to: number): string => String.fromCharCode(...head.subarray(from, to));
  return head.length >= 12 && text(0, 4) === "RIFF" && text(8, 12) === "WAVE";
}

function looksLikeMp3(head: Uint8Array): boolean {
  const [b0, b1, b2] = [head[0], head[1], head[2]];
  if (b0 === undefined || b1 === undefined || b2 === undefined) {
    return false;
  }
  const id3 = b0 === 0x49 && b1 === 0x44 && b2 === 0x33; // "ID3"
  const frameSync = b0 === 0xff && (b1 & 0xe0) === 0xe0;
  return id3 || frameSync;
}

export async function loadAudioFile(rawPath: string, field: string): Promise<UploadResult> {
  const path = expandHome(rawPath.trim());
  if (!isAbsolute(path)) {
    return { ok: false, error: `File path must be absolute (or start with ~/): ${rawPath}` };
  }
  const ext = extname(path).toLowerCase();
  if (ext !== ".mp3" && ext !== ".wav") {
    return { ok: false, error: `Only MP3 or WAV files can be uploaded; got "${ext || "no extension"}": ${rawPath}` };
  }
  let size: number;
  try {
    const info = await stat(path);
    if (!info.isFile()) {
      return { ok: false, error: `Not a file: ${rawPath}` };
    }
    size = info.size;
  } catch {
    return { ok: false, error: `File not found or not readable: ${rawPath}` };
  }
  if (size === 0) {
    return { ok: false, error: `File is empty: ${rawPath}` };
  }
  if (size > MAX_UPLOAD_BYTES) {
    const mb = (size / (1024 * 1024)).toFixed(1);
    return { ok: false, error: `File is ${mb} MB; Zadarma accepts up to 5 MB: ${rawPath}` };
  }
  const handle = await open(path, "r");
  let bytes: Uint8Array<ArrayBuffer>;
  try {
    bytes = new Uint8Array(size);
    await handle.read(bytes, 0, size, 0);
  } finally {
    await handle.close();
  }
  const isWav = ext === ".wav";
  const matches = isWav ? looksLikeWav(bytes) : looksLikeMp3(bytes);
  if (!matches) {
    return { ok: false, error: `File content is not ${isWav ? "WAV" : "MP3"} audio: ${rawPath}` };
  }
  return {
    ok: true,
    file: { field, fileName: basename(path), mimeType: isWav ? "audio/wav" : "audio/mpeg", bytes },
  };
}
