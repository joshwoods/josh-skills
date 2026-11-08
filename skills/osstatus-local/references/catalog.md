# Catalog provenance and maintenance

Source: [OSStatus.com](https://www.osstatus.com/), created by
[Araelium](https://www.araelium.com). This local tool is not affiliated with either.
The source's footer says **Updated July 2024**. The first local capture was
November 8, 2026; the exact retrieval time and SHA-256 are stored in `metadata`.

The public GET interface is:

```text
https://www.osstatus.com/search/results?platform=all&framework=all&search=
```

An empty search returns 6,453 rows from 143 frameworks in one HTML response.
All framework dropdown options appear in the rows. No pagination or truncation
notice was observed. An independent IOKit-filtered request returned the same 10
records as the corresponding subset of the complete response. This establishes
coverage of the public response, not access to private records or a complete
inventory of any particular Apple SDK version.

The capture contains 484 nonempty descriptions and 5,969 blank descriptions;
6,653 numeric displays (200 records have two), 628 hex displays, and 154 OSType
displays. Platform flags are `mac`, `ios`, `watch`, `tv`, and `vision`. The UI's
platform dropdown only offers Mac and iOS, but the local filters support all
five observed flags. No exact SDK release provenance was provided by the site.

Two anomalous source records are preserved and flagged:

- `MACH_SEND_INVALID_RT_OOL_SIZE`: hex display includes prose, and the decimal
  display is `4294967644`, beyond unsigned 32-bit range. No corrected value is
  inferred; malformed hex is not indexed as a number.
- `kIOPCIExpressCapabilityIDErrorReporting`: hex display is `-0x01`, while decimal
  display is `0`. Both are retained; they disagree.

No dataset license or public source repository was identified in the inspected
page. Source attribution is preserved; this package does not assert ownership
or a redistribution license over the source catalog. The database is the user's
local reference copy.

## SQLite schema

`data/osstatus.sqlite3` is a normal SQLite database. CLI queries open it read-only.

| Table | Fields |
| --- | --- |
| `errors` | `id`, `symbol`, `framework`, `header`, `description`, `source_url`, `raw_fields_json` |
| `platforms` | `error_id`, `platform` |
| `codes` | `error_id`, `kind`, `text`, nullable `integer_value` |
| `metadata` | `key`, JSON-encoded `value` |

`errors.id` is the row's position in that capture, not a stable upstream ID.
Duplicate symbols and code meanings are retained as separate records.
`raw_fields_json` preserves each source CSS field name and all text values,
including type labels. HTML entities are decoded and outer formatting whitespace
is trimmed. For example, a signed display may retain `-2147352468 (int32)`.
All code text remains available even when no numeric interpretation is possible.
FourCC conversion uses four Latin-1 bytes, big-endian; out-of-range integers
are never silently wrapped to 32 bits.

The DB metadata includes source URL, retrieval/import time, source update label,
SHA-256, field counts, platform counts, scope, and source anomalies. The matching
`data/source-<sha256>.html.gz` is a compressed raw HTML capture for verification
or offline rebuilding. Its name hashes the uncompressed bytes. Lookup never
needs to decompress it.

```bash
sqlite3 <skill-dir>/data/osstatus.sqlite3 \
  "SELECT symbol,framework,header FROM errors WHERE symbol='errSecItemNotFound';"
python3 <skill-dir>/scripts/osstatus.py --all --full-json > catalog.json
```

## Refresh and offline rebuild

Ordinary `--json` output includes matched records, code forms, per-record
warnings, result counts, and concise provenance. `--full-json` additionally
includes the original field mapping and all catalog metadata for archival or
inspection. Neither format omits matching records silently: inspect `truncated`
and use `--all` for complete output.

```bash
python3 <skill-dir>/scripts/refresh.py
python3 <skill-dir>/scripts/refresh.py --html <saved-capture.html.gz> --db /tmp/rebuilt.sqlite3
```

Refresh performs a single public request with a 60-second timeout and 20 MB
response bound. It validates table closure, required fields, platform names,
framework coverage, uncaptured text, SQLite integrity, and every raw field's DB
round trip before replacement. A smaller result set is rejected by default;
inspect the changed source before deliberately using `--allow-smaller`.
Unknown field markup fails visibly rather than discarding data.
Refresh only on request; do not automatically override a shrinkage or format
validation failure. A failed refresh preserves the existing database.

An offline rebuild records its import time and leaves `retrieved_at` null instead
of misrepresenting the current time as the original download time. Old raw
captures are retained after refresh for traceability. To move the skill, copy the
whole skill folder; paths resolve relative to the scripts.
