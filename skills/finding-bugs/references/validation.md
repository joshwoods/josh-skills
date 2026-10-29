# Validating a candidate

Read this when a plausible defect depends on assumptions or is difficult to reproduce. The goal is to distinguish an actual violation from a suspicious fragment of code.

## Build a causal account

Write the shortest supported chain:

`supported trigger → reachable implementation path → violated contract → observable consequence`

Verify each link in context. Check call sites, guards, ordering, dependency semantics, and tests that might contradict it. A locally missing guard may be enforced at an earlier boundary. A value may be invalid under an internal precondition but valid at a public entry point; those are different cases.

If the expected behavior is disputed, isolate the ambiguity. Do not hide a product decision inside a correctness finding. If an external API's behavior is material, consult its primary documentation for the relevant version or inspect the actual dependency.

## Design a discriminating probe

Choose a probe that could disprove the candidate. State the expected failure and an observation that would rule it out before execution. Exercise the actual implementation rather than a handwritten copy of the suspect logic.

Prefer reproducing through the affected application workflow in a representative environment first. If unavailable or a reasonable attempt does not reproduce it, use the smallest faithful test as a fallback. Reuse existing evidence and fixtures; this preference does not require prolonged runtime setup or repeated attempts before useful test or static investigation. Distinguish actual-use reproduction from test-only reproduction and from a concern not yet reproduced. Automation of the representative workflow can establish actual-use evidence; isolated tests and substituted boundaries establish only what they exercise.

For an audit, choose existing checks, an external harness, a disposable checkout, or a narrowly scoped reversible test/instrumentation probe according to which can faithfully reach the behavior. A native test target or private compiled boundary may require a temporary in-project probe. Honor explicit read-only or no-edit instructions. Record the starting state, preserve user edits, and remove only your probe changes afterward. If repairs are also authorized, retain the intended repair and useful regression checks; probe cleanup must not undo that work.

Use supported entry points and isolated state. A mock can control a boundary, but a defect in the mock is not evidence against production behavior. Preserve enough context to show that the artificial response or schedule is supported by the real dependency.

Capture the command or steps, relevant revision/configuration, input or action sequence, output, and assertion. Keep evidence proportional to the claim; do not expose unrelated data or produce a large artifact bundle for a simple counterexample.

Reduce a reproduction only while preserving the claimed failure. An exception from a different line, an impossible object state, or a replaced integration boundary may explain why the reduced case fails without validating the original concern.

## Difficult runtime cases

- **Intermittent ordering:** identify the specific conflicting operations and the observation point. Control order with existing synchronization hooks or a faithful isolated harness where feasible. Record which schedules were exercised; stress runs that do not fail do not prove absence.
- **Unavailable environment:** establish as much of the path as static evidence supports. Name the missing dependency, configuration, or runtime check. Do not present a hypothetical execution as observed.
- **Potential destructive effects:** use a safe fixture or sandbox within the existing authorization. If that cannot exercise the relevant behavior, report the limit rather than mutating a live system to strengthen the finding.
- **Long or expensive reproduction:** preserve the original evidence and choose targeted probes that distinguish explanations. A minimal deterministic example is useful but is not a prerequisite for recording a well-supported concern.

## Grade the conclusion

Separate three aspects:

- **Disposition:** validated, unresolved, or disproved.
- **Validation method:** executed reproduction, runtime observation, static path analysis, or a combination.
- **Confidence:** explain the strength of the evidence and any unverified premise. Do not invent numerical probabilities.

A complete static trace can validate a deterministic defect without runtime execution; say how it was established. Timing, platform, and integration claims often need runtime evidence for a strong conclusion. An unresolved candidate can be useful when it comes with its missing premise and the next decisive check, but it belongs outside the established findings.

Judge severity from the reachable impact and affected conditions, independently of how certain you are. Two findings with the same effect may have different confidence; a high-confidence issue may still have low impact.

## Follow related mechanisms without overclaiming

After a validated defect, search for the same causal mistake within scope. Start with the known occurrence, generalize the relevant assumptions, and inspect candidate contexts. Keep a result as a search hit until its trigger, violation, and consequence are checked. Avoid expanding one concrete bug into speculative claims about an entire subsystem.
