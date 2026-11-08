# Validating a candidate

Read this when a plausible defect depends on assumptions or is difficult to reproduce. The goal is to distinguish an actual violation from a suspicious fragment of code.

## Build a causal account

Write the shortest supported chain:

`supported trigger → reachable implementation path → violated contract → observable consequence`

Verify each link in context. Check call sites, guards, ordering, dependency semantics, and tests that might contradict it. A locally missing guard may be enforced at an earlier boundary. A value may be invalid under an internal precondition but valid at a public entry point; those are different cases.

If the expected behavior is disputed, isolate the ambiguity. Do not hide a product decision inside a correctness finding. If an external API's behavior is material, consult its primary documentation for the relevant version or inspect the actual dependency.

## Use review and history as clues

Follow the [local review and history guidance](review-history.md) when warnings, corrections, dependencies, or unfinished validation can inform the current question. Check current applicability and distinguish explicit prediction, related concern, and hindsight. Thread status and repeated summaries do not establish remediation or independent corroboration.

## Design a discriminating probe

Choose a probe that could disprove the candidate. State the expected failure and an observation that would rule it out before execution. Exercise the actual implementation rather than a handwritten copy of the suspect logic.

Prefer actual use first; if unavailable or a reasonable attempt does not reproduce the failure, choose a [faithful fallback](evidence.md#reproduce-faithfully). Reuse cheap existing checks and inspect available evidence before constructing new tests. Keep actual-use, test-only, and not-yet-reproduced evidence separate; continue useful static investigation when runtime is unavailable.

For an audit, choose existing checks, an external harness, a disposable checkout, or a narrowly scoped reversible test/instrumentation probe according to which can faithfully reach the behavior. A native test target or private compiled boundary may require a temporary in-project probe. Honor explicit read-only or no-edit instructions. Record the starting state, preserve user edits, and remove only your probe changes afterward. If repairs are also authorized, retain the intended repair and useful regression checks; probe cleanup must not undo that work.

Use supported entry points and isolated state. Follow the [reproduction and recording guidance](evidence.md#reproduce-faithfully) for substituted boundaries, captured conditions, and faithful failure signatures. Preserve a live failure [before reset or retry](evidence.md#preserve-failing-state-before-resetting-it); compare against separate fresh state where feasible. A disappearing symptom is an observation, not a causal explanation or verified repair.

Reduce a reproduction only while preserving the claimed failure. An exception from a different line, an impossible object state, or a replaced integration boundary may explain why the reduced case fails without validating the original concern.

## Bind evidence to the behavior tested

For a replacement, eligibility, or routing change, assert the actual consumer-level result and relevant subsequent reads or side effects. A counter showing fewer evaluations, requests, or calls can support the intended optimization without establishing correctness. Use the [consumer and decision-case guidance](coverage.md#replacements-eligibility-and-actual-consumers) to select the observation point and distinguish a valid fallback from a violating path.

Apply the [shared evidence limits](evidence.md#bind-evidence-to-its-conditions): record revisions, effective scope/population, actual serving branch, and consumer assertions. When scope expands, revisit affected callers and decision cases. Refresh checks whose premises changed and retain unaffected checks; earlier success does not automatically cover a new configuration or consumer.

## Difficult runtime cases

- **Intermittent ordering:** identify the specific conflicting operations and the observation point. Control order with existing synchronization hooks or a faithful isolated harness where feasible. Record which schedules were exercised; stress runs that do not fail do not prove absence.
- **Unavailable environment:** establish as much of the path as static evidence supports. Name the missing dependency, configuration, or runtime check. Do not present a hypothetical execution as observed.
- **Potential destructive effects:** use a safe fixture or sandbox within the existing authorization. If that cannot exercise the relevant behavior, report the limit rather than mutating a live system to strengthen the finding.
- **Long or expensive reproduction:** preserve the original evidence and choose targeted probes that distinguish explanations. A minimal deterministic example is useful but is not a prerequisite for recording a well-supported concern.

## Grade the conclusion

Use the [evidence distinctions](evidence.md#separate-result-evidence-and-conclusion) to report candidate disposition, validation method, and confidence separately. A complete static argument can validate a deterministic defect; label it static and state unverified premises. Keep unresolved candidates outside established findings, with the missing premise and next decisive check. Judge severity by reachable impact, independently of confidence.

## Follow related mechanisms without overclaiming

After a validated defect, state the invariant that failed and search for equivalent reachable cases within scope, including inherited or indirect consumers where relevant. A list of previously named fixes is a starting point, not proof that the affected set is exhausted. Inspect each candidate's trigger, guard, route, and consequence; keep it as a search hit until those links are checked. Avoid expanding one concrete bug into speculative claims about an entire subsystem. If the affected set extends beyond the requested scope, disclose that boundary rather than claiming all instances are fixed.
