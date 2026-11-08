#!/usr/bin/env python3
"""Capture OSStatus.com's public catalog and build a validated SQLite snapshot."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import gzip
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sqlite3
import tempfile
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SOURCE_URL = "https://www.osstatus.com/search/results?platform=all&framework=all&search="
FIELDS = {"ec-framework", "ec-header_file", "value-symbol", "ec-description",
          "value-number", "value-hex", "value-ostype", "value-string", "value-type"}
PLATFORMS = {"mac", "ios", "watch", "tv", "vision"}
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
             "link", "meta", "param", "source", "track", "wbr"}


class CatalogParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self.framework_menu = set()
        self.updated = ""
        self.in_body = False
        self.body_closed = False
        self.row = None
        self.cells = 0
        self.stack = []
        self.captures = []
        self.outside_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if "data-search-framework" in attrs:
            self.framework_menu.add(attrs["data-search-framework"])
        if tag == "tbody":
            if self.in_body or self.body_closed:
                raise ValueError("Unexpected multiple result bodies")
            self.in_body = True
        if self.in_body and tag == "tr":
            if self.row is not None:
                raise ValueError("Nested result rows")
            self.row = {}
            self.cells = 0
        if self.row is not None and tag == "td":
            self.cells += 1
        if tag == "br":
            for cap in self.captures:
                cap["parts"].append("\n")
        if tag in VOID_TAGS:
            return
        self.stack.append(tag)
        for cls in classes:
            if cls == "updated":
                self.captures.append({"depth": len(self.stack), "field": cls, "parts": []})
            elif self.row is not None:
                if cls.startswith("platform-"):
                    if cls[9:] not in PLATFORMS:
                        raise ValueError(f"Unknown platform {cls}; update parser")
                    self.row.setdefault(cls, []).append("")
                elif cls in FIELDS:
                    self.captures.append({"depth": len(self.stack), "field": cls, "parts": []})
                else:
                    raise ValueError(f"Unknown result field class {cls!r}; update parser")
        if self.row is not None and (tag == "a" or "title" in attrs or "data-content" in attrs):
            raise ValueError("New link/tooltip in result; update parser to preserve it")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        if not self.stack or self.stack[-1] != tag:
            raise ValueError(f"Unbalanced HTML at closing {tag}")
        remaining = []
        for cap in self.captures:
            if cap["depth"] == len(self.stack):
                value = "".join(cap["parts"]).strip()
                if cap["field"] == "updated":
                    self.updated = value
                elif self.row is not None:
                    self.row.setdefault(cap["field"], []).append(value)
            else:
                remaining.append(cap)
        self.captures = remaining
        self.stack.pop()
        if tag == "tr" and self.row is not None:
            if self.cells != 5:
                raise ValueError(f"Expected 5 cells, found {self.cells}")
            self.rows.append(self.row)
            self.row = None
        if tag == "tbody":
            self.in_body = False
            self.body_closed = True

    def handle_data(self, data):
        for cap in self.captures:
            cap["parts"].append(data)
        if self.row is not None and data.strip() and not self.captures:
            self.outside_text.append(data.strip())

    def validate(self):
        if self.stack or self.in_body or not self.body_closed or self.row is not None:
            raise ValueError("Incomplete catalog HTML")
        if not self.rows:
            raise ValueError("No result rows")
        if self.outside_text:
            raise ValueError(f"Uncaptured result text: {self.outside_text[:3]}")
        for index, row in enumerate(self.rows, 1):
            for key in ("ec-framework", "ec-header_file", "value-symbol", "ec-description"):
                if len(row.get(key, [])) != 1:
                    raise ValueError(f"Row {index}: expected one {key}")
            if not row["value-symbol"][0] or not row["ec-framework"][0]:
                raise ValueError(f"Row {index}: missing symbol/framework")
            if not any(k.startswith("platform-") for k in row):
                raise ValueError(f"Row {index}: no platform")
            if not any(row.get(k) for k in ("value-number", "value-hex", "value-ostype", "value-string")):
                raise ValueError(f"Row {index}: no code")
        frameworks = {r["ec-framework"][0] for r in self.rows}
        if frameworks != self.framework_menu - {"all"}:
            raise ValueError("Framework menu differs from captured result frameworks")
        if not self.updated:
            raise ValueError("Missing site update date")


def parse_catalog(data):
    text = data.decode("utf-8")
    if re.search(r'class=["\'][^"\']*(?:pagination|load-more)', text, re.I):
        raise ValueError("Pagination detected; cannot assume a complete catalog")
    parser = CatalogParser()
    parser.feed(text)
    parser.close()
    parser.validate()
    return parser


def integer_value(kind, text):
    if kind == "number":
        if not re.fullmatch(r"[+-]?\d+(?:\s+\(int32\))?", text):
            raise ValueError(f"Unrecognized number {text!r}")
        value = int(text.split()[0])
    elif kind == "hex":
        if not re.fullmatch(r"[+-]?0[xX][0-9a-fA-F]+", text):
            # Source sometimes embeds prose in the hex span. Preserve it as text
            # without guessing a corrected value; record it in source_anomalies.
            return None
        value = int(text, 16)
    elif kind == "ostype":
        chars = text[1:-1] if len(text) >= 2 and text[0] == text[-1] == "'" else text
        try:
            raw = chars.encode("latin-1")
        except UnicodeEncodeError:
            return None
        return int.from_bytes(raw, "big") if len(raw) == 4 else None
    else:
        return None
    if not -(2**63) <= value < 2**63:
        raise ValueError(f"Code exceeds SQLite integer range: {text}")
    return value


def source_anomalies(rows):
    anomalies = []
    for index, row in enumerate(rows, 1):
        values = []
        problems = []
        for key in ("value-number", "value-hex", "value-ostype"):
            for value in row.get(key, []):
                parsed = integer_value(key[6:], value)
                if parsed is None:
                    problems.append(f"Unparsed {key[6:]} display: {value}")
                else:
                    # Compare valid 32-bit signed/unsigned equivalents without
                    # silently wrapping the source's out-of-range numbers.
                    values.append(parsed + 2**32 if -(2**31) <= parsed < 0 else parsed)
        if len(set(values)) > 1:
            problems.append("Displayed code representations disagree in the source")
        if problems:
            anomalies.append({"id": index, "symbol": row["value-symbol"][0],
                              "framework": row["ec-framework"][0], "warnings": problems})
    return anomalies


SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE errors(id INTEGER PRIMARY KEY, symbol TEXT NOT NULL, framework TEXT NOT NULL,
    header TEXT NOT NULL, description TEXT NOT NULL, source_url TEXT NOT NULL, raw_fields_json TEXT NOT NULL);
CREATE TABLE platforms(error_id INTEGER NOT NULL REFERENCES errors(id), platform TEXT NOT NULL,
    PRIMARY KEY(error_id, platform));
CREATE TABLE codes(error_id INTEGER NOT NULL REFERENCES errors(id), kind TEXT NOT NULL,
    text TEXT NOT NULL, integer_value INTEGER);
CREATE TABLE metadata(key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE INDEX errors_symbol ON errors(symbol COLLATE NOCASE);
CREATE INDEX errors_framework ON errors(framework COLLATE NOCASE);
CREATE INDEX codes_number ON codes(integer_value, error_id);
CREATE INDEX codes_error ON codes(error_id);
CREATE INDEX platforms_name ON platforms(platform, error_id);
"""


def build_database(path, parser, metadata):
    with sqlite3.connect(path) as conn:
        conn.executescript(SCHEMA)
        for index, row in enumerate(parser.rows, 1):
            symbol, framework = row["value-symbol"][0], row["ec-framework"][0]
            url = "https://www.osstatus.com/search/results?" + urlencode(
                {"platform": "all", "framework": framework, "search": symbol})
            conn.execute("INSERT INTO errors VALUES(?,?,?,?,?,?,?)", (
                index, symbol, framework, row["ec-header_file"][0], row["ec-description"][0],
                url, json.dumps(row, ensure_ascii=False, sort_keys=True)))
            for key, values in row.items():
                if key.startswith("platform-"):
                    conn.execute("INSERT INTO platforms VALUES(?,?)", (index, key[9:]))
                elif key.startswith("value-") and key != "value-symbol":
                    kind = key[6:]
                    for value in values:
                        conn.execute("INSERT INTO codes VALUES(?,?,?,?)",
                                     (index, kind, value, integer_value(kind, value)))
        conn.executemany("INSERT INTO metadata VALUES(?,?)",
                         ((k, json.dumps(v, ensure_ascii=False)) for k, v in metadata.items()))
        if conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("Database integrity check failed")
        if conn.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("Database foreign key check failed")
        stored = [json.loads(row[0]) for row in conn.execute("SELECT raw_fields_json FROM errors ORDER BY id")]
        if stored != parser.rows:
            raise ValueError("Database field round-trip mismatch")


def main():
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument("--html", type=Path, help="Import saved HTML (or .gz) without networking")
    argp.add_argument("--db", type=Path, default=ROOT / "data/osstatus.sqlite3")
    argp.add_argument("--allow-smaller", action="store_true", help="Allow replacing an existing snapshot with fewer rows")
    args = argp.parse_args()
    try:
        if args.html:
            data = args.html.read_bytes()
            if args.html.suffix == ".gz":
                data = gzip.decompress(data)
            capture_method = "saved HTML import"
        else:
            req = Request(SOURCE_URL, headers={"User-Agent": "OSStatusLocal/1.0 (personal offline catalog)",
                                              "Accept": "text/html"})
            with urlopen(req, timeout=60) as response:
                if response.status != 200 or "text/html" not in response.headers.get("Content-Type", ""):
                    raise ValueError("Unexpected source response")
                data = response.read(20_000_001)
            capture_method = "public GET"
        if len(data) > 20_000_000:
            raise ValueError("Catalog exceeded 20 MB; review before importing")
        parser = parse_catalog(data)
        args.db.parent.mkdir(parents=True, exist_ok=True)
        if args.db.exists() and not args.allow_smaller:
            with sqlite3.connect(args.db.resolve().as_uri() + "?mode=ro", uri=True) as old:
                old_count = old.execute("SELECT count(*) FROM errors").fetchone()[0]
            if len(parser.rows) < old_count:
                raise ValueError(f"Catalog shrank from {old_count} to {len(parser.rows)}; review before using --allow-smaller")
        digest = hashlib.sha256(data).hexdigest()
        timestamp = datetime.now(timezone.utc).isoformat()
        metadata = {
            "schema_version": 1, "source_url": SOURCE_URL, "source_name": "OSStatus.com by Araelium",
            "source_updated": parser.updated, "imported_at": timestamp,
            "retrieved_at": timestamp if not args.html else None, "capture_method": capture_method,
            "source_sha256": digest, "source_bytes": len(data), "record_count": len(parser.rows),
            "framework_count": len(parser.framework_menu - {"all"}),
            "description_count": sum(bool(r["ec-description"][0]) for r in parser.rows),
            "source_anomalies": source_anomalies(parser.rows),
            "platform_counts": dict(Counter(k[9:] for r in parser.rows for k in r if k.startswith("platform-"))),
            "field_counts": dict(Counter({k: sum(len(r.get(k, [])) for r in parser.rows)
                                           for k in sorted({k for r in parser.rows for k in r})})),
            "scope": "All rows returned by public blank search, all frameworks/platforms; private backend and Apple SDK completeness unverified.",
        }
        # Build/validate first. The sole authoritative artifact is replaced atomically.
        fd, temp_name = tempfile.mkstemp(prefix=".osstatus-", suffix=".sqlite3", dir=args.db.parent)
        os.close(fd)
        temp = Path(temp_name)
        try:
            build_database(temp, parser, metadata)
            # Content-addressed raw input remains paired with its DB via metadata.
            raw_path = args.db.parent / ("source-" + digest + ".html.gz")
            if not raw_path.exists():
                raw_path.write_bytes(gzip.compress(data, mtime=0))
            os.replace(temp, args.db)
        finally:
            temp.unlink(missing_ok=True)
        print(json.dumps({"database": str(args.db.resolve()), **metadata}, indent=2))
    except Exception as exc:
        argp.exit(2, f"Refresh failed; existing database retained: {exc}\n")


if __name__ == "__main__":
    main()
