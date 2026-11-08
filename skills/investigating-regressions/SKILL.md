---
name: investigating-regressions
description: Find when a regression was introduced and which releases are affected, separating code changes from activation or environment changes. Use for regression-history or bisect requests, rather than general diagnosis.
---

# Investigating Regressions

Read and follow the [regression history workflow](references/regression-history.md) and [evidence guidance](references/evidence.md). Establish the supported introduction boundary or candidate interval, explain how it produces the failure, and map it to affected releases only when deployment evidence supports that mapping. Keep code introduction, activation, changed context, and first detection distinct.

Use existing reproduction evidence, version facts, and investigation notes; start at the first unanswered question. Preserve a live failing state before resetting it, and handle urgent authorized mitigation before ordinary history work. Prefer focused history and available artifacts before rebuilding old versions or bisecting. A suspicious commit is a lead, and an untestable revision remains unresolved. Stop unnecessary history work once the requested boundary and explanation are supported.

When entering from a larger diagnosis or bug hunt, retain its original symptom, requested outcome, authorization, and remaining coverage. Return the boundary evidence, causal explanation, skipped or untested revisions, and limits to that investigation. Locating a commit does not complete a requested repair or the remaining hunt. For a history-only request, report the result and repair direction without unsolicited product changes.

When repair is requested, continue through repair and verification. The [diagnosis checklist](../diagnosing-bugs/references/checklist.md), if installed, provides deeper guidance; the [discovery checklist](../finding-bugs/references/checklist.md), if installed, can resume a broader hunt. Neither sibling is required:

- Repair the supported mechanism while preserving intended behavior, validation, error handling, and existing test protection. Reuse or add a meaningful regression check at the real trigger; demonstrate failure before and success after where feasible.
- Recheck the original workflow, risk-relevant neighboring behavior, and required project checks. Keep actual-use verification distinct from isolated tests; report unavailable integration checks as gaps. Verify final behavior without temporary probes wherever their removal could matter.
- Check whether existing affected data or persisted state needs recovery within the task's authorization, and verify that recovery separately from preventing recurrence.
- Remove only temporary investigation changes, preserve user work and intended repairs, and inspect the retained diff. Report the supported boundary, repair and verification results, remaining uncertainty, and unfinished parent scope. Failed verification returns to investigation; unavailable verification does not establish a verified repair.
