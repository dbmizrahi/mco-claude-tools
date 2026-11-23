#!/usr/bin/env python3
"""greeninvoice-receipts: upload receipt files to Morning (GreenInvoice) as expense
drafts, and produce a read-only bookkeeping check-up.

Unofficial tool, not affiliated with Morning / GreenInvoice. Not tax advice.

Python 3.9+, standard library only. Every command prints one JSON object on stdout.
Secrets are never printed, logged or accepted as command-line arguments.

Commands (all take --folder <receipts folder>):
  verify                      read-only: authenticate, show business name and VAT setup
  baseline [--dry-run]        mark files already in the folder as handled (never uploaded)
  upload   [--dry-run] [--max-files N]
                              upload new files; Morning OCRs each one into an expense DRAFT
  drafts                      read-only: count expense drafts waiting for approval
  checkup                     read-only: drafts, open invoices, VAT checks, upload problems

Credentials (first match wins):
  --creds-dir DIR             folder with two files: `apikey` (API key ID) and `secret`
  GREENINVOICE_API_ID / GREENINVOICE_API_SECRET environment variables
  ~/.greeninvoice/            default folder with `apikey` and `secret`

Files written (only these, only inside --folder):
  upload-log.csv              append-only record of every file handled
  .greeninvoice-receipts.json settings, written by `baseline` (never contains secrets)

Upload flow (from third-party documentation, verified 2026-11-04):
  token    POST https://api.morning.co/idp/v1/oauth/token (client_credentials)
  presign  GET  https://apigw.greeninvoice.co.il/file-upload/v1/url?context=expense&data={"source":5}
  storage  POST <presigned url>, multipart form: presigned fields in order, file last
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import stat
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Callable, Dict, List, Optional, Tuple

VERSION = "0.1.0"
TOKEN_URL = "https://api.morning.co/idp/v1/oauth/token"
API = "https://api.greeninvoice.co.il/api/v1"
PRESIGN_URL = "https://apigw.greeninvoice.co.il/file-upload/v1/url"

EXTS = {".pdf": "application/pdf", ".png": "image/png", ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg", ".gif": "image/gif", ".svg": "image/svg+xml"}
MAX_BYTES = 16 * 1024 * 1024
MAX_ATTEMPTS = 3
LOG_NAME = "upload-log.csv"
CONFIG_NAME = ".greeninvoice-receipts.json"
HEADER = ["path", "size_bytes", "md5", "sha256", "logged_at", "status", "detail"]
DONE = {"baseline", "uploaded", "duplicate", "too_large"}
ALLOCATION_FROM = dt.date(2026, 6, 1)
ALLOCATION_THRESHOLD = 5000.0
ALLOCATION_KEYS = ("allocationNumber", "taxAuthorityConfirmationNumber")


class GiError(Exception):
    """Error safe to show to the user (never contains secrets)."""


# --------------------------------------------------------------------- HTTP
Transport = Callable[[str, str, Optional[bytes], Dict[str, str]], Tuple[int, bytes]]


def urllib_transport(method: str, url: str, body: Optional[bytes],
                     headers: Dict[str, str]) -> Tuple[int, bytes]:
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except urllib.error.URLError as exc:
        raise GiError("network error reaching %s: %s"
                      % (urllib.parse.urlsplit(url).netloc, exc.reason)) from None


def multipart(fields: List[Tuple[str, str]], file_field: str, filename: str,
              content: bytes, content_type: str) -> Tuple[bytes, str]:
    """Encode a multipart/form-data body: text fields in the given order, file last."""
    boundary = "----gi" + uuid.uuid4().hex
    out = bytearray()
    for name, value in fields:
        out += ("--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n"
                % (boundary, name)).encode()
        out += str(value).encode() + b"\r\n"
    safe_name = filename.replace('"', "_").replace("\r", "_").replace("\n", "_")
    out += ("--%s\r\nContent-Disposition: form-data; name=\"%s\"; filename=\"%s\"\r\n"
            "Content-Type: %s\r\n\r\n" % (boundary, file_field, safe_name, content_type)).encode()
    out += content + b"\r\n" + ("--%s--\r\n" % boundary).encode()
    return bytes(out), "multipart/form-data; boundary=" + boundary


class Client:
    def __init__(self, api_id: str, secret: str, transport: Transport = urllib_transport):
        self._id, self._secret, self._t = api_id, secret, transport
        self._token: Optional[str] = None

    def _json(self, method: str, url: str, payload: Optional[object] = None,
              auth: bool = True) -> object:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if auth:
            headers["Authorization"] = "Bearer " + self.token()
        body = json.dumps(payload).encode() if payload is not None else None
        code, raw = self._t(method, url, body, headers)
        if code >= 400:
            raise GiError("%s %s returned HTTP %d: %s"
                          % (method, urllib.parse.urlsplit(url).path, code, short(raw)))
        try:
            return json.loads(raw.decode() or "null")
        except ValueError:
            raise GiError("unexpected non-JSON reply from %s" % urllib.parse.urlsplit(url).path) from None

    def token(self) -> str:
        if self._token is None:
            j = self._json("POST", TOKEN_URL, {"grant_type": "client_credentials",
                                               "client_id": self._id,
                                               "client_secret": self._secret}, auth=False)
            tok = j.get("accessToken") or j.get("access_token") if isinstance(j, dict) else None
            if not tok:
                raise GiError("token reply had no access token")
            self._token = str(tok)
        return self._token

    def get(self, path: str) -> object:
        return self._json("GET", API + path)

    def post(self, path: str, payload: object) -> object:
        return self._json("POST", API + path, payload)

    def upload_draft(self, filename: str, content: bytes, content_type: str) -> str:
        q = urllib.parse.urlencode({"context": "expense", "data": json.dumps({"source": 5})})
        p = self._json("GET", PRESIGN_URL + "?" + q)
        if not isinstance(p, dict) or "url" not in p or not isinstance(p.get("fields"), dict):
            raise GiError("presign reply had no url/fields")
        fields = [(str(k), str(v)) for k, v in p["fields"].items()]
        body, ctype = multipart(fields, "file", filename, content, content_type)
        code, raw = self._t("POST", str(p["url"]), body, {"Content-Type": ctype})
        if code not in (200, 201, 204):
            raise GiError("storage upload returned HTTP %d: %s" % (code, short(raw)))
        return str(p["fields"].get("key", ""))


def as_dict(value: object) -> Dict[str, object]:
    return value if isinstance(value, dict) else {}


def short(raw: bytes) -> str:
    return raw[:200].decode("utf-8", "replace").replace("\n", " ").strip()


# -------------------------------------------------------------- credentials
def load_credentials(creds_dir: Optional[str], env: Dict[str, str]) -> Tuple[str, str, Dict[str, object]]:
    """Return (api_id, secret, info). info is safe to print."""
    if creds_dir is None and env.get("GREENINVOICE_API_ID") and env.get("GREENINVOICE_API_SECRET"):
        return env["GREENINVOICE_API_ID"].strip(), env["GREENINVOICE_API_SECRET"].strip(), \
            {"source": "environment", "warnings": []}
    folder = os.path.expanduser(creds_dir or "~/.greeninvoice")
    warnings: List[str] = []
    values = []
    for name in ("apikey", "secret"):
        path = os.path.join(folder, name)
        if not os.path.isfile(path):
            raise GiError("credentials file missing: %s (expected files 'apikey' and 'secret')" % path)
        mode = os.stat(path).st_mode
        if mode & (stat.S_IRWXG | stat.S_IRWXO):
            warnings.append("%s is readable by other users; run: chmod 600 %s" % (path, path))
        with open(path, encoding="utf-8") as fh:
            values.append(fh.read().strip())
    if not values[0] or not values[1]:
        raise GiError("credentials files in %s are empty" % folder)
    return values[0], values[1], {"source": "folder", "folder": folder, "warnings": warnings}


# --------------------------------------------------------------- folder/log
def now() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def scan(root: str) -> List[str]:
    out = []
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if not x.startswith("."))
        for f in sorted(files):
            if f.startswith(".") or os.path.splitext(f)[1].lower() not in EXTS:
                continue
            out.append(os.path.relpath(os.path.join(d, f), root).replace(os.sep, "/"))
    return out


def read_log(root: str) -> List[Dict[str, str]]:
    path = os.path.join(root, LOG_NAME)
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def append_log(root: str, rows: List[Dict[str, object]]) -> None:
    if not rows:
        return
    path = os.path.join(root, LOG_NAME)
    new = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(HEADER)
        for r in rows:
            w.writerow([r[k] for k in HEADER])


def latest_status(log: List[Dict[str, str]]) -> Dict[str, str]:
    st: Dict[str, str] = {}
    for r in log:
        st[r["path"]] = r["status"]
    return st


def plan(root: str, log: List[Dict[str, str]]):
    """Classify files: (todo, skipped_rows). todo = list of (row, bytes)."""
    done_paths = {r["path"] for r in log if r["status"] in DONE}
    done_hashes = {r["sha256"] for r in log if r["status"] in DONE}
    attempts: Dict[str, int] = {}
    for r in log:
        if r["status"] == "failed":
            attempts[r["path"]] = attempts.get(r["path"], 0) + 1
    todo, skipped, seen = [], [], set()
    for rel in scan(root):
        if rel in done_paths or attempts.get(rel, 0) >= MAX_ATTEMPTS:
            continue
        with open(os.path.join(root, rel), "rb") as fh:
            data = fh.read()
        sha, md5 = hashlib.sha256(data).hexdigest(), hashlib.md5(data).hexdigest()
        row: Dict[str, object] = {"path": rel, "size_bytes": len(data), "md5": md5,
                                  "sha256": sha, "logged_at": now(), "status": "", "detail": ""}
        if sha in done_hashes or sha in seen:
            row.update(status="duplicate", detail="same content already handled")
            skipped.append(row)
        elif len(data) > MAX_BYTES:
            row.update(status="too_large", detail="over 16 MB; upload manually in Morning")
            skipped.append(row)
        else:
            seen.add(sha)
            todo.append((row, data))
    return todo, skipped


# ------------------------------------------------------------------ commands
def cmd_verify(client: Client, info: Dict[str, object]) -> Dict[str, object]:
    b = client.get("/businesses/me")
    if not isinstance(b, dict):
        raise GiError("unexpected business reply")
    s = client.post("/expenses/search", {"page": 1, "pageSize": 1})
    bi = as_dict(as_dict(s).get("aggregations")).get("isBiMonthly")
    return {"ok": True, "business": b.get("nameEn") or b.get("name"),
            "charges_vat": not bool(b.get("exemption")),
            "vat_period": "bi-monthly" if bi is True else "monthly" if bi is False else "unknown",
            "credentials": info}


def cmd_baseline(root: str, dry: bool) -> Dict[str, object]:
    log = read_log(root)
    known = {r["path"] for r in log}
    rows = []
    for rel in scan(root):
        if rel in known:
            continue
        with open(os.path.join(root, rel), "rb") as fh:
            data = fh.read()
        rows.append({"path": rel, "size_bytes": len(data), "md5": hashlib.md5(data).hexdigest(),
                     "sha256": hashlib.sha256(data).hexdigest(), "logged_at": now(),
                     "status": "baseline", "detail": "existing before automation; not uploaded"})
    if not dry:
        append_log(root, rows)
        cfg_path = os.path.join(root, CONFIG_NAME)
        cfg: Dict[str, object] = {}
        if os.path.exists(cfg_path):
            with open(cfg_path, encoding="utf-8") as fh:
                cfg = json.load(fh)
        cfg.update({"tool": "greeninvoice-receipts", "version": VERSION,
                    "baseline_at": now(), "baseline_files": len(rows)})
        with open(cfg_path, "w", encoding="utf-8") as fh:
            json.dump(cfg, fh, indent=2)
    return {"dry_run": dry, "marked": [r["path"] for r in rows], "count": len(rows)}


def cmd_upload(root: str, client: Optional[Client], dry: bool, max_files: int,
               pause: float = 1.0) -> Dict[str, object]:
    log = read_log(root)
    todo, skipped = plan(root, log)
    todo = todo[:max_files]
    uploaded: List[object] = []
    failed: List[Dict[str, object]] = []
    res: Dict[str, object] = {
        "dry_run": dry, "to_upload": [r["path"] for r, _ in todo],
        "duplicates": [r["path"] for r in skipped if r["status"] == "duplicate"],
        "too_large": [r["path"] for r in skipped if r["status"] == "too_large"],
        "uploaded": uploaded, "failed": failed}
    if dry:
        return res
    rows = list(skipped)
    for row, data in todo:
        rel = str(row["path"])
        try:
            if client is None:
                raise GiError("no client")
            key = client.upload_draft(os.path.basename(rel), data,
                                      EXTS[os.path.splitext(rel)[1].lower()])
            row.update(status="uploaded", detail="draft requested; storage key " + key)
            uploaded.append(rel)
        except GiError as exc:
            row.update(status="failed", detail=str(exc)[:300])
            failed.append({"path": rel, "reason": row["detail"]})
        row["logged_at"] = now()
        rows.append(row)
        if pause:
            time.sleep(pause)
    append_log(root, rows)
    return res


def search_all(client: Client, path: str, payload: Dict[str, object], limit_pages: int = 10) -> List[Dict[str, object]]:
    items: List[Dict[str, object]] = []
    for page in range(1, limit_pages + 1):
        r = client.post(path, dict(payload, page=page, pageSize=100))
        if not isinstance(r, dict):
            break
        batch = r.get("items") or []
        items.extend(x for x in batch if isinstance(x, dict))
        if page >= int(r.get("pages") or 1):
            break
    return items


def cmd_drafts(client: Client) -> Dict[str, object]:
    d = search_all(client, "/expenses/drafts/search", {})
    dates = sorted(str(x.get("creationDate") or x.get("date") or "") for x in d)
    return {"drafts_waiting": len(d), "oldest": dates[0] if dates else None}


def vat_period_start(today: dt.date, bi_monthly: bool) -> dt.date:
    m = today.month - ((today.month - 1) % 2) if bi_monthly else today.month
    return dt.date(today.year, m, 1)


def cmd_checkup(root: str, client: Client, today: Optional[dt.date] = None) -> Dict[str, object]:
    today = today or dt.date.today()
    biz = client.get("/businesses/me")
    charges_vat = not bool(as_dict(biz).get("exemption"))
    probe = client.post("/expenses/search", {"page": 1, "pageSize": 1})
    bi = as_dict(as_dict(probe).get("aggregations")).get("isBiMonthly")
    start = vat_period_start(today, bi is not False)

    out: Dict[str, object] = {"today": today.isoformat(), "charges_vat": charges_vat,
                              "vat_period": "bi-monthly" if bi is not False else "monthly",
                              "vat_period_start": start.isoformat()}
    out["drafts"] = cmd_drafts(client)

    docs = search_all(client, "/documents/search", {"type": [305, 300], "status": [0]})
    open_docs = []
    for d in docs:
        due = str(d.get("dueDate") or "")
        open_docs.append({"number": d.get("number"), "type": d.get("type"),
                          "client": as_dict(d.get("client")).get("name"),
                          "amount": d.get("amountOpened", d.get("amount")),
                          "currency": d.get("currency"), "due": due or None,
                          "overdue": bool(due) and due < today.isoformat()})
    out["open_invoices"] = open_docs

    exps = search_all(client, "/expenses/search", {"fromDate": start.isoformat()})
    no_cat, open_count, alloc = [], 0, []
    for e in exps:
        if not e.get("accountingClassification"):
            no_cat.append({"number": e.get("number"), "date": e.get("date")})
        if e.get("status") == 10:
            open_count += 1
        if not charges_vat:
            continue
        try:
            net = float(e.get("amountExcludeVat") or 0)
            vat = float(e.get("vat") or 0)
            day = dt.date.fromisoformat(str(e.get("date")))
        except (TypeError, ValueError):
            continue
        if e.get("currency") == "ILS" and vat > 0 and net > ALLOCATION_THRESHOLD and day >= ALLOCATION_FROM:
            data = as_dict(e.get("data"))
            has_field = any(k in e or k in data for k in ALLOCATION_KEYS)
            number = next((e.get(k) or data.get(k) for k in ALLOCATION_KEYS
                           if e.get(k) or data.get(k)), None)
            if not number:
                alloc.append({"number": e.get("number"), "date": e.get("date"), "net": net,
                              "supplier": as_dict(e.get("supplier")).get("name"),
                              "state": "missing" if has_field else "not_in_api_reply_check_manually"})
    out["expenses_without_category"] = no_cat
    out["open_expenses_this_period"] = open_count
    out["allocation_number_issues"] = alloc if charges_vat else "not applicable (business does not charge VAT)"

    st = latest_status(read_log(root))
    out["upload_problems"] = {"failed": sorted(p for p, s in st.items() if s == "failed"),
                              "too_large": sorted(p for p, s in st.items() if s == "too_large")}
    return out


# ---------------------------------------------------------------------- main
def main(argv: Optional[List[str]] = None, env: Optional[Dict[str, str]] = None,
         transport: Transport = urllib_transport) -> int:
    ap = argparse.ArgumentParser(prog="greeninvoice_receipts")
    ap.add_argument("command", choices=["verify", "baseline", "upload", "drafts", "checkup"])
    ap.add_argument("--folder", required=True, help="receipts folder")
    ap.add_argument("--creds-dir", help="folder with files 'apikey' and 'secret'")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-files", type=int, default=50)
    a = ap.parse_args(argv)
    env = dict(os.environ) if env is None else env
    root = os.path.expanduser(a.folder)

    try:
        if not os.path.isdir(root):
            raise GiError("receipts folder not found: %s" % root)
        if a.command == "baseline":
            result = cmd_baseline(root, a.dry_run)
        elif a.command == "upload" and a.dry_run:
            result = cmd_upload(root, None, True, a.max_files)
        else:
            api_id, secret, info = load_credentials(a.creds_dir, env)
            client = Client(api_id, secret, transport)
            if a.command == "verify":
                result = cmd_verify(client, info)
            elif a.command == "upload":
                result = cmd_upload(root, client, False, a.max_files)
                result["credential_warnings"] = info["warnings"]
            elif a.command == "drafts":
                result = cmd_drafts(client)
            else:
                result = cmd_checkup(root, client)
                result["credential_warnings"] = info["warnings"]
    except GiError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
