---
name: osstatus-local
description: Explain Apple API error codes in iOS/macOS logs and help debug the failing call. Use the offline catalog for OSStatus/NSError, Keychain/audio failures, numeric or FourCC codes, and error symbols.
---

# Apple error lookup and debugging

Turn an Apple error from a log or failing call into a supported interpretation
and a useful next debugging step. This is a lookup aid within the user's task;
when a repair is requested, continue investigating and fixing the caller after
identifying the code.

## Start from the error

Read the supplied log, screenshot, or failing call. Extract the error code or
symbol and retain the domain, API, and surrounding failure context. For example,
`Error Domain=NSOSStatusErrorDomain Code=-50 "(null)"` supplies the query `-50`;
the full log is not a text-search query. If the user only says “help debug this
iOS error” without an error attached or accessible in the project, ask for the
exact message/log and the call that failed. Do not run an empty catalog search.

Keep error namespaces separate: an HTTP status, POSIX errno, or custom NSError
domain is not an OSStatus merely because the number appears in this catalog.

## Retrieve candidates

Run the bundled helper with Python 3.10+; no network or third-party packages are
needed. Resolve `<skill-dir>` to the directory containing this `SKILL.md`.

```bash
python3 <skill-dir>/scripts/osstatus.py -50 --json
python3 <skill-dir>/scripts/osstatus.py errSecItemNotFound --json
python3 <skill-dir>/scripts/osstatus.py "'fmt?'" --json
```

Search the exact code or symbol first. Numeric searches match valid signed and
unsigned 32-bit equivalents; hex input also works. A quoted FourCC preserves all
four bytes, including spaces. Text search requires all supplied terms.

Use the caller to interpret the returned candidates. Do not assume the caller's
module is the catalog's framework: Keychain records commonly belong to
`Security`; AVFoundation calls can surface records under `AVFAudio`,
`AudioToolbox`, `AudioUnit`, or `CoreAudioTypes`. Filter by `--framework`, `--header`,
or `--platform` when the returned records support that choice. Retry a filtered
miss without filters before reporting no match. Platform flags in this older
snapshot are not a definitive availability check.

Check `total`, `shown`, and `truncated`; fetch remaining candidates with `--all`
when needed to resolve ambiguity. `--frameworks` lists valid framework names.
Exit 1 means no matches; exit 2 means the lookup failed. Distinguish both from a
successful result. An absent code may be newer than the snapshot or outside it.

## Explain and investigate

Lead with the contextually relevant symbol and meaning, followed by the matching
framework/header and source link. Preserve alternative meanings if the failing
API is unknown. Most records have no prose description: explain what the symbol
supports, and distinguish your interpretation from a source-provided definition.

An error's name does not establish the cause in this program. Use the failing
call and its inputs to choose the next check; inspect available code or ask for
the missing call site instead of listing generic fixes. For absent codes, sparse
descriptions, conflicting matches, or source `warnings`, consult the relevant
local SDK declaration or official Apple documentation as needed. The returned
header filename and symbol are useful search keys. A flagged source value must
be verified before it is used in code; do not silently correct it.

The catalog reports an upstream update of **July 2024**. `--stats` gives the
capture's provenance. Keep ordinary queries offline; consult additional sources
when the investigation requires them. Do not refresh as part of a lookup.

For full JSON exports (`--all --full-json`), SQLite schema, raw captures,
attribution, or a user-requested refresh, read
[references/catalog.md](references/catalog.md). Do not load the whole database
or HTML capture into model context.
