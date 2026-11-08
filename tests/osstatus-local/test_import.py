"""Whole-snapshot fidelity and refresh failure protection against real artifacts."""

import gzip
import hashlib
from html import unescape
import json
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2] / "skills"
DB = ROOT / "osstatus-local/data/osstatus.sqlite3"
REFRESH = ROOT / "osstatus-local/scripts/refresh.py"


def independent_rows(html):
    """Independent extraction for the observed span-only source table markup."""
    body = html.split("<tbody>", 1)[1].split("</tbody>", 1)[0]
    rows = []
    for row in re.findall(r"<tr>(.*?)</tr>", body, re.S):
        fields = {}
        # Lookahead includes the inner value-type span of a signed number.
        for match in re.finditer(r'(?=<span class="([^"]+)">(.*?)</span>)', row, re.S):
            cls, text = match.groups()
            text = unescape(re.sub(r"<[^>]+>", "", text)).strip()
            fields.setdefault(cls, []).append(text)
        rows.append(fields)
    return rows


class ImportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(DB.as_uri() + "?mode=ro", uri=True)
        cls.meta = {k: json.loads(v) for k, v in cls.conn.execute("SELECT key,value FROM metadata")}
        cls.raw_path = DB.parent / ("source-" + cls.meta["source_sha256"] + ".html.gz")
        cls.data = gzip.decompress(cls.raw_path.read_bytes())
        cls.rows = independent_rows(cls.data.decode())

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_raw_source_hash_and_size(self):
        self.assertEqual(hashlib.sha256(self.data).hexdigest(), self.meta["source_sha256"])
        self.assertEqual(len(self.data), self.meta["source_bytes"])

    def test_every_field_of_every_record_matches_source(self):
        actual = [json.loads(row[0]) for row in self.conn.execute("SELECT raw_fields_json FROM errors ORDER BY id")]
        self.assertEqual(len(actual), self.meta["record_count"])
        self.assertEqual(actual, self.rows)

    def test_all_normalized_fields_and_code_texts_match_source(self):
        for identifier, row in enumerate(self.rows, 1):
            with self.subTest(id=identifier):
                expected = tuple(row[k][0] for k in ("value-symbol", "ec-framework", "ec-header_file", "ec-description"))
                actual = self.conn.execute("SELECT symbol,framework,header,description FROM errors WHERE id=?", (identifier,)).fetchone()
                self.assertEqual(actual, expected)
                platforms = {k[9:] for k in row if k.startswith("platform-")}
                self.assertEqual(platforms, {r[0] for r in self.conn.execute("SELECT platform FROM platforms WHERE error_id=?", (identifier,))})
                codes = sorted((k[6:], v) for k in row if k.startswith("value-") and k != "value-symbol" for v in row[k])
                self.assertEqual(codes, sorted(self.conn.execute("SELECT kind,text FROM codes WHERE error_id=?", (identifier,))))

    def test_every_menu_framework_is_present(self):
        menu = set(re.findall(r'data-search-framework="([^"]+)"', self.data.decode())) - {"all"}
        actual = {r[0] for r in self.conn.execute("SELECT DISTINCT framework FROM errors")}
        self.assertEqual(menu, actual)
        self.assertEqual(len(menu), self.meta["framework_count"])

    def test_sqlite_integrity(self):
        self.assertEqual(self.conn.execute("PRAGMA integrity_check").fetchone()[0], "ok")
        self.assertEqual(self.conn.execute("PRAGMA foreign_key_check").fetchall(), [])

    def test_offline_rebuild_from_bundled_snapshot(self):
        with tempfile.TemporaryDirectory() as folder:
            rebuilt = Path(folder) / "rebuilt.sqlite3"
            result = subprocess.run([sys.executable, str(REFRESH), "--html", str(self.raw_path), "--db", str(rebuilt)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            with sqlite3.connect(rebuilt) as conn:
                for table in ("errors", "codes", "platforms"):
                    self.assertEqual(conn.execute(f"SELECT * FROM {table}").fetchall(), self.conn.execute(f"SELECT * FROM {table}").fetchall())

    def test_failed_refresh_keeps_database_byte_identical(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "existing.sqlite3"
            shutil.copyfile(DB, target)
            before = target.read_bytes()
            invalid = Path(folder) / "truncated.html"
            invalid.write_bytes(self.data[:len(self.data)//2])
            result = subprocess.run([sys.executable, str(REFRESH), "--html", str(invalid), "--db", str(target)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(target.read_bytes(), before)

    def test_smaller_catalog_requires_explicit_override(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "existing.sqlite3"
            shutil.copyfile(DB, target)
            before = target.read_bytes()
            html = self.data.decode()
            # Remove one of several Accounts rows, leaving framework coverage intact.
            pos = html.index("<tbody>")
            prefix, body = html[:pos], html[pos:]
            body = re.sub(r"<tr>.*?</tr>", "", body, count=1, flags=re.S)
            smaller = Path(folder) / "smaller.html"
            smaller.write_text(prefix + body)
            result = subprocess.run([sys.executable, str(REFRESH), "--html", str(smaller), "--db", str(target)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("Catalog shrank", result.stderr)
            self.assertEqual(target.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
