#!/usr/bin/env python3
"""Query the bundled OSStatus catalog offline. Exit 0: results, 1: none, 2: error."""

from __future__ import annotations

import argparse
from contextlib import closing
import json
from pathlib import Path
import re
import sqlite3
import sys
from typing import Any


DEFAULT_DB = Path(__file__).resolve().parent.parent / "data" / "osstatus.sqlite3"
PLATFORMS = {
    "mac": "mac", "macos": "mac", "osx": "mac", "ios": "ios",
    "watch": "watch", "watchos": "watch", "tv": "tv", "tvos": "tv",
    "vision": "vision", "visionos": "vision",
}
PLATFORM_NAMES = {"mac": "macOS", "ios": "iOS", "watch": "watchOS",
                  "tv": "tvOS", "vision": "visionOS"}


def integer_aliases(number: int) -> list[int]:
    """Include signed/unsigned 32-bit equivalents only within that domain."""
    aliases = {number}
    if -(1 << 31) <= number < 0:
        aliases.add(number + (1 << 32))
    elif (1 << 31) <= number < (1 << 32):
        aliases.add(number - (1 << 32))
    return sorted(aliases)


def code_query(query: str) -> tuple[list[int], bool]:
    """Return numeric matches and whether this is an explicitly numeric query.

    Bare four-character strings also remain text searches, so words such as
    'file' can find symbol/description text. Quoted FourCCs are code-only.
    """
    if re.fullmatch(r"[+-]?\d+", query):
        return integer_aliases(int(query, 10)), True
    if re.fullmatch(r"[+-]?0[xX][0-9a-fA-F]+", query):
        return integer_aliases(int(query, 16)), True
    quoted = len(query) >= 2 and query[0] == query[-1] and query[0] in "\"'"
    value = query[1:-1] if quoted else query
    if len(value) == 4:
        try:
            encoded = value.encode("latin-1")
        except UnicodeEncodeError:
            return [], False
        return integer_aliases(int.from_bytes(encoded, "big")), quoted or value != value.strip()
    return [], False


def like_pattern(value: str) -> str:
    return "%" + value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"


def connect(path: Path) -> sqlite3.Connection:
    path = path.expanduser().resolve()
    if not path.is_file():
        raise ValueError(f"Database not found: {path}. Restore or rebuild the bundled catalog.")
    connection = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def read_metadata(connection: sqlite3.Connection) -> dict[str, Any]:
    result = {}
    for row in connection.execute("SELECT key, value FROM metadata ORDER BY key"):
        try:
            result[row["key"]] = json.loads(row["value"])
        except json.JSONDecodeError:
            result[row["key"]] = row["value"]
    return result


def search(connection: sqlite3.Connection, query: str = "", *, framework: str | None = None,
           header: str | None = None, platform: str | None = None,
           limit: int | None = 20) -> dict[str, Any]:
    clauses: list[str] = []
    parameters: list[Any] = []
    if framework:
        clauses.append("e.framework = ? COLLATE NOCASE")
        parameters.append(framework)
    if header:
        clauses.append("e.header LIKE ? ESCAPE '\\'")
        parameters.append(like_pattern(header))
    if platform:
        canonical = PLATFORMS.get(platform.lower())
        if canonical is None:
            raise ValueError(f"Unknown platform: {platform}")
        clauses.append("EXISTS (SELECT 1 FROM platforms p WHERE p.error_id=e.id AND p.platform=?)")
        parameters.append(canonical)
    if query:
        numbers, numeric_only = code_query(query)
        alternatives: list[str] = []
        # SQLite INTEGER values are signed 64-bit; larger inputs cannot match.
        numbers = [number for number in numbers if -(1 << 63) <= number < (1 << 63)]
        if numbers:
            placeholders = ",".join("?" for _ in numbers)
            alternatives.append(f"EXISTS (SELECT 1 FROM codes c WHERE c.error_id=e.id AND c.integer_value IN ({placeholders}))")
            parameters.extend(numbers)
        if not numeric_only:
            text_clauses = []
            for token in query.split():
                text_clauses.append("((e.symbol || ' ' || e.framework || ' ' || e.header || ' ' || e.description) LIKE ? ESCAPE '\\' OR EXISTS (SELECT 1 FROM codes c WHERE c.error_id=e.id AND c.text LIKE ? ESCAPE '\\'))")
                parameters.extend([like_pattern(token), like_pattern(token)])
            if text_clauses:
                alternatives.append("(" + " AND ".join(text_clauses) + ")")
        clauses.append("(" + " OR ".join(alternatives or ["0"]) + ")")
    where = " WHERE " + " AND ".join(clauses) if clauses else ""
    total = connection.execute("SELECT count(*) FROM errors e" + where, parameters).fetchone()[0]
    order = " ORDER BY CASE WHEN e.symbol = ? COLLATE NOCASE THEN 0 WHEN e.framework = ? COLLATE NOCASE OR e.header = ? COLLATE NOCASE THEN 1 ELSE 2 END, e.framework COLLATE NOCASE, e.symbol COLLATE NOCASE, e.header COLLATE NOCASE, e.id"
    result_parameters = parameters + [query, query, query]
    if limit is not None:
        if limit < 1:
            raise ValueError("Limit must be positive")
        order += " LIMIT ?"
        result_parameters.append(limit)
    rows = connection.execute("SELECT e.* FROM errors e" + where + order, result_parameters).fetchall()
    metadata = read_metadata(connection)
    warnings = {entry["id"]: entry["warnings"] for entry in metadata.get("source_anomalies", [])}
    results = []
    for row in rows:
        result = dict(row)
        result["raw_fields"] = json.loads(result.pop("raw_fields_json"))
        result["platforms"] = [p[0] for p in connection.execute(
            "SELECT platform FROM platforms WHERE error_id=? ORDER BY platform", (row["id"],))]
        result["codes"] = [dict(c) for c in connection.execute(
            "SELECT kind, text, integer_value FROM codes WHERE error_id=? ORDER BY rowid", (row["id"],))]
        result["warnings"] = warnings.get(row["id"], [])
        results.append(result)
    return {"query": query, "filters": {"framework": framework, "header": header, "platform": platform},
            "total": total, "shown": len(results), "truncated": len(results) < total,
            "results": results, "metadata": metadata}


def stats(connection: sqlite3.Connection) -> dict[str, Any]:
    return {
        "records": connection.execute("SELECT count(*) FROM errors").fetchone()[0],
        "frameworks": connection.execute("SELECT count(DISTINCT framework) FROM errors").fetchone()[0],
        "headers": connection.execute("SELECT count(DISTINCT header) FROM errors").fetchone()[0],
        "descriptions": connection.execute("SELECT count(*) FROM errors WHERE description != ''").fetchone()[0],
        "platforms": dict(connection.execute("SELECT platform,count(*) FROM platforms GROUP BY platform ORDER BY platform")),
        "metadata": read_metadata(connection),
    }


def compact_json(payload: dict[str, Any]) -> dict[str, Any]:
    """Project CLI output without altering the full programmatic result."""
    compact = dict(payload)
    if "results" in payload:
        compact["results"] = [{key: value for key, value in row.items() if key != "raw_fields"}
                              for row in payload["results"]]
    provenance = ("source_name", "source_url", "source_updated", "retrieved_at", "schema_version")
    compact["metadata"] = {key: payload["metadata"][key] for key in provenance
                           if key in payload["metadata"]}
    return compact


def print_results(payload: dict[str, Any]) -> None:
    total, shown = payload["total"], payload["shown"]
    print(f"{total} matching records; showing {shown}." + (" Use --all or increase --limit for the rest." if payload["truncated"] else ""))
    for row in payload["results"]:
        print(f"\n{row['symbol']} — {row['framework']} / {row['header']}")
        codes = [code["text"] for code in row["codes"] if code["kind"] != "type"]
        print("  Code: " + " | ".join(dict.fromkeys(codes)))
        print("  Platforms: " + ", ".join(PLATFORM_NAMES.get(p, p) for p in row["platforms"]))
        print("  Description: " + (row["description"] or "Not supplied by the source."))
        for warning in row["warnings"]:
            print("  Source warning: " + warning)
        print("  Source: " + row["source_url"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search the OSStatus snapshot locally; no network requests.",
                                     epilog="Exit codes: 0 results/success; 1 no matches; 2 invalid input or database error. Quote multiword queries or FourCCs containing shell punctuation.")
    parser.add_argument("query", nargs="*", help="Code, symbol, framework, header, or words to match")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="SQLite catalog path")
    parser.add_argument("--framework", help="Exact framework name, case-insensitive")
    parser.add_argument("--header", help="Header filename substring")
    parser.add_argument("--platform", type=str.lower, choices=sorted(PLATFORMS), help="Platform filter")
    parser.add_argument("--limit", type=int, default=20, help="Maximum results (default: 20)")
    parser.add_argument("--all", action="store_true", help="Return every match")
    parser.add_argument("--json", action="store_true", help="Compact machine-readable JSON")
    parser.add_argument("--full-json", action="store_true", help="Include raw fields and full provenance; implies --json")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--stats", action="store_true", help="Show catalog counts and provenance")
    mode.add_argument("--frameworks", action="store_true", help="List framework names and record counts")
    # argparse recognizes negative decimals but not negative hexadecimal values.
    arguments = list(sys.argv[1:] if argv is None else argv)
    arguments = [str(int(arg, 16)) if re.fullmatch(r"-0[xX][0-9a-fA-F]+", arg) else arg for arg in arguments]
    args = parser.parse_args(arguments)
    if args.limit < 1:
        parser.error("--limit must be positive")
    if (args.stats or args.frameworks) and (args.query or args.framework or args.header or args.platform):
        parser.error("--stats and --frameworks do not accept search terms or filters")
    try:
        with closing(connect(args.db)) as connection:
            if args.stats:
                payload = stats(connection)
                if args.json and not args.full_json:
                    payload = compact_json(payload)
                print(json.dumps(payload, indent=2, ensure_ascii=False))
                return 0
            if args.frameworks:
                frameworks = [dict(row) for row in connection.execute("SELECT framework, count(*) AS records FROM errors GROUP BY framework ORDER BY framework COLLATE NOCASE")]
                if args.json or args.full_json:
                    payload = {"frameworks": frameworks, "metadata": read_metadata(connection)}
                    print(json.dumps(payload if args.full_json else compact_json(payload), indent=2, ensure_ascii=False))
                else:
                    print("\n".join(f"{row['framework']}\t{row['records']}" for row in frameworks))
                return 0
            query_text = args.query[0] if len(args.query) == 1 and len(args.query[0]) == 4 else " ".join(args.query).strip()
            payload = search(connection, query_text, framework=args.framework,
                             header=args.header, platform=args.platform, limit=None if args.all else args.limit)
            if args.json or args.full_json:
                print(json.dumps(payload if args.full_json else compact_json(payload), indent=2, ensure_ascii=False))
            else:
                print_results(payload)
            return 0 if payload["total"] else 1
    except (sqlite3.Error, ValueError, OSError) as exc:
        print(f"osstatus: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
