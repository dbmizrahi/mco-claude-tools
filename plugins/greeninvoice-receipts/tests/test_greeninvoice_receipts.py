"""Unit tests for greeninvoice_receipts.py. No network: a fake transport answers.

Run from the plugin directory:  python3 -m unittest discover -s tests
"""
import contextlib
import csv
import datetime as dt
import io
import json
import os
import stat
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import greeninvoice_receipts as gr  # noqa: E402

API_ID = "id-0000-test"
SECRET = "s3cr3t-value-never-printed"


class FakeTransport:
    """Records calls; answers by URL. storage_code controls the S3 reply."""

    def __init__(self, storage_code=204, exemption=False, bi_monthly=True,
                 expenses=None, documents=None, drafts=None):
        self.calls = []
        self.storage_code = storage_code
        self.exemption = exemption
        self.bi_monthly = bi_monthly
        self.expenses = expenses or []
        self.documents = documents or []
        self.drafts = drafts or []

    def __call__(self, method, url, body, headers):
        self.calls.append((method, url, body, dict(headers)))
        if url == gr.TOKEN_URL:
            return 200, json.dumps({"accessToken": "tok-123"}).encode()
        if url.startswith(gr.PRESIGN_URL):
            return 200, json.dumps({"url": "https://s3.example/bucket",
                                    "fields": {"key": "k/1", "Policy": "p", "X-Amz-Signature": "sig"}}).encode()
        if url == "https://s3.example/bucket":
            return self.storage_code, b"" if self.storage_code == 204 else b"<Error>denied</Error>"
        if url.endswith("/businesses/me"):
            return 200, json.dumps({"nameEn": "Test Co", "exemption": self.exemption}).encode()
        if url.endswith("/expenses/drafts/search"):
            return 200, json.dumps({"items": self.drafts, "pages": 1}).encode()
        if url.endswith("/expenses/search"):
            return 200, json.dumps({"items": self.expenses, "pages": 1,
                                    "aggregations": {"isBiMonthly": self.bi_monthly}}).encode()
        if url.endswith("/documents/search"):
            return 200, json.dumps({"items": self.documents, "pages": 1}).encode()
        return 404, b"not found"

    def methods_to(self, fragment):
        return [m for m, u, _, _ in self.calls if fragment in u]


def run(argv, transport, env=None):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = gr.main(argv, env=env if env is not None else {}, transport=transport)
    out = buf.getvalue()
    return code, json.loads(out), out


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = os.path.join(self.tmp.name, "receipts")
        self.creds = os.path.join(self.tmp.name, "creds")
        os.makedirs(os.path.join(self.root, "2026-10"))
        os.makedirs(self.creds)
        for name, val in (("apikey", API_ID), ("secret", SECRET)):
            p = os.path.join(self.creds, name)
            with open(p, "w") as fh:
                fh.write(val + "\n")
            os.chmod(p, 0o600)

        self._sleep = gr.time.sleep
        gr.time.sleep = lambda _s: None

    def tearDown(self):
        gr.time.sleep = self._sleep
        self.tmp.cleanup()

    def put(self, rel, content=b"%PDF-1.4 test"):
        p = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(content)

    def log(self):
        with open(os.path.join(self.root, gr.LOG_NAME), newline="") as fh:
            return list(csv.DictReader(fh))

    def args(self, *cmd):
        return list(cmd) + ["--folder", self.root, "--creds-dir", self.creds]


class TestScanAndBaseline(Base):
    def test_scan_ignores_hidden_and_other_types(self):
        self.put("2026-10/a.pdf")
        self.put("2026-10/b.JPG")
        self.put("2026-10/.hidden.pdf")
        self.put(".private/c.pdf")
        self.put("2026-10/notes.txt")
        self.assertEqual(gr.scan(self.root), ["2026-10/a.pdf", "2026-10/b.JPG"])

    def test_baseline_marks_existing_and_writes_no_secret(self):
        self.put("2026-05/old.pdf")
        t = FakeTransport()
        code, res, _ = run(self.args("baseline"), t)
        self.assertEqual(code, 0)
        self.assertEqual(res["marked"], ["2026-05/old.pdf"])
        self.assertEqual(t.calls, [], "baseline must not touch the network")
        self.assertEqual(self.log()[0]["status"], "baseline")
        with open(os.path.join(self.root, gr.CONFIG_NAME)) as fh:
            cfg = fh.read()
        self.assertNotIn(SECRET, cfg)
        self.assertNotIn(API_ID, cfg)

    def test_baseline_dry_run_writes_nothing(self):
        self.put("2026-05/old.pdf")
        run(self.args("baseline", "--dry-run"), FakeTransport())
        self.assertFalse(os.path.exists(os.path.join(self.root, gr.LOG_NAME)))


class TestUpload(Base):
    def test_dry_run_lists_new_files_without_network(self):
        self.put("2026-05/old.pdf", b"old")
        run(self.args("baseline"), FakeTransport())
        self.put("2026-10/new.pdf", b"new")
        t = FakeTransport()
        code, res, _ = run(self.args("upload", "--dry-run"), t)
        self.assertEqual(code, 0)
        self.assertEqual(res["to_upload"], ["2026-10/new.pdf"])
        self.assertEqual(t.calls, [])

    def test_upload_logs_and_never_repeats(self):
        self.put("2026-10/new.pdf", b"new")
        t = FakeTransport()
        code, res, out = run(self.args("upload"), t)
        self.assertEqual(code, 0)
        self.assertEqual(res["uploaded"], ["2026-10/new.pdf"])
        self.assertNotIn(SECRET, out)
        self.assertEqual(self.log()[-1]["status"], "uploaded")
        t2 = FakeTransport()
        _, res2, _ = run(self.args("upload"), t2)
        self.assertEqual(res2["to_upload"], [])
        self.assertEqual(t2.methods_to("s3.example"), [])

    def test_same_content_under_new_name_is_duplicate(self):
        self.put("2026-10/a.pdf", b"same")
        run(self.args("upload"), FakeTransport())
        self.put("2026-11/copy-of-a.pdf", b"same")
        t = FakeTransport()
        _, res, _ = run(self.args("upload"), t)
        self.assertEqual(res["duplicates"], ["2026-11/copy-of-a.pdf"])
        self.assertEqual(t.methods_to("s3.example"), [])

    def test_failed_file_retried_at_most_three_times(self):
        self.put("2026-10/bad.pdf", b"bad")
        for _ in range(3):
            _, res, _ = run(self.args("upload"), FakeTransport(storage_code=403))
            self.assertEqual(len(res["failed"]), 1)
        _, res, _ = run(self.args("upload"), FakeTransport(storage_code=403))
        self.assertEqual(res["to_upload"], [])
        self.assertEqual([r["status"] for r in self.log()], ["failed"] * 3)

    def test_multipart_fields_in_order_and_file_last(self):
        body, ctype = gr.multipart([("key", "k/1"), ("Policy", "p")], "file", "r.pdf", b"DATA", "application/pdf")
        text = body.decode("latin-1")
        self.assertTrue(ctype.startswith("multipart/form-data; boundary="))
        self.assertLess(text.index('name="key"'), text.index('name="Policy"'))
        self.assertLess(text.index('name="Policy"'), text.index('name="file"'))
        self.assertIn("DATA", text[text.index('name="file"'):])

    def test_files_are_never_moved_or_deleted(self):
        self.put("2026-10/new.pdf", b"new")
        run(self.args("upload"), FakeTransport())
        self.assertTrue(os.path.exists(os.path.join(self.root, "2026-10/new.pdf")))


class TestCredentials(Base):
    def test_env_credentials_used_when_no_folder_given(self):
        a, s, info = gr.load_credentials(None, {"GREENINVOICE_API_ID": "x", "GREENINVOICE_API_SECRET": "y"})
        self.assertEqual((a, s, info["source"]), ("x", "y", "environment"))

    def test_warns_on_loose_permissions(self):
        os.chmod(os.path.join(self.creds, "secret"), 0o644)
        _, _, info = gr.load_credentials(self.creds, {})
        self.assertEqual(len(info["warnings"]), 1)
        self.assertNotIn(SECRET, json.dumps(info))

    def test_missing_credentials_is_clean_error(self):
        os.remove(os.path.join(self.creds, "secret"))
        code, res, _ = run(self.args("verify"), FakeTransport())
        self.assertEqual(code, 1)
        self.assertIn("credentials file missing", res["error"])


class TestReadOnlyCommands(Base):
    def assert_read_only(self, t):
        writes = [u for m, u, _, _ in t.calls
                  if m != "GET" and u != gr.TOKEN_URL and not u.endswith("/search")]
        self.assertEqual(writes, [], "read-only command made a write call")

    def test_verify(self):
        t = FakeTransport()
        code, res, out = run(self.args("verify"), t)
        self.assertEqual(code, 0)
        self.assertEqual(res["business"], "Test Co")
        self.assertEqual(res["vat_period"], "bi-monthly")
        self.assertNotIn(SECRET, out)
        self.assert_read_only(t)

    def test_checkup_flags_missing_allocation_number(self):
        big = {"number": "1", "date": "2026-11-02", "currency": "ILS", "vat": 1800,
               "amountExcludeVat": 10000, "status": 10, "accountingClassification": {"id": "x"},
               "supplier": {"name": "Supplier"}, "allocationNumber": ""}
        small = dict(big, number="2", amountExcludeVat=100, vat=18)
        nocat = dict(small, number="3", accountingClassification=None)
        docs = [{"number": "50004", "type": 305, "client": {"name": "Client"}, "amountOpened": 100,
                 "currency": "ILS", "dueDate": "2026-10-01"}]
        t = FakeTransport(expenses=[big, small, nocat], documents=docs, drafts=[{"date": "2026-11-01"}])
        res = gr.cmd_checkup(self.root, gr.Client(API_ID, SECRET, t), today=dt.date(2026, 11, 4))
        self.assertEqual(res["vat_period_start"], "2026-11-01")
        self.assertEqual([a["number"] for a in res["allocation_number_issues"]], ["1"])
        self.assertEqual(res["allocation_number_issues"][0]["state"], "missing")
        self.assertEqual([e["number"] for e in res["expenses_without_category"]], ["3"])
        self.assertTrue(res["open_invoices"][0]["overdue"])
        self.assertEqual(res["drafts"]["drafts_waiting"], 1)
        self.assert_read_only(t)

    def test_checkup_skips_vat_checks_for_exempt_business(self):
        t = FakeTransport(exemption=True)
        res = gr.cmd_checkup(self.root, gr.Client(API_ID, SECRET, t), today=dt.date(2026, 11, 4))
        self.assertIsInstance(res["allocation_number_issues"], str)

    def test_vat_period_start(self):
        self.assertEqual(gr.vat_period_start(dt.date(2026, 12, 15), True), dt.date(2026, 11, 1))
        self.assertEqual(gr.vat_period_start(dt.date(2026, 1, 15), True), dt.date(2026, 1, 1))
        self.assertEqual(gr.vat_period_start(dt.date(2026, 12, 15), False), dt.date(2026, 12, 1))


if __name__ == "__main__":
    unittest.main()
