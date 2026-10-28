---
name: finding-bugs
description: Find and validate correctness defects in a requested code or product scope. Use for proactive bug hunts and correctness reviews, rather than diagnosing a reported failure.
---

# Finding Bugs

Produce defensible findings and an honest account of the requested coverage. Keep a broad hunt structured while choosing probes from the behavior and evidence, rather than applying every possible check to every file.

Use the request and prior context to determine completion. For an audit or review, investigate and report; keep product fixes and permanent test changes out of that scope unless authorized. Reversible local probes are part of investigation, subject to explicit read-only or no-edit constraints. When asked to find and fix bugs, continue through repairs, retesting, and the remaining coverage without waiting for another instruction.

## Define coverage and contracts

Establish the requested repository, revision or diff, workflows, runtime, and depth or time limits. Inspect the relevant project guidance and starting changes. For a broad hunt, create a compact coverage map before detailed investigation:

| Area / workflow | Contract and scenario | Check method | Status and evidence |
|---|---|---|---|
| Relevant behavior | Expected result or property | Trace, test, runtime, etc. | Planned / source examined / executed / blocked |

Map callers, boundaries, and consumers that can affect the conclusion. For a diff review, include the requested change set and relevant surrounding behavior; disclose unread portions. Derive expected behavior from specifications, public APIs, callers, documentation, and tests. Conflicting evidence or ambiguous product intent needs resolution; existing code or a passing test alone does not establish the contract.

For multi-workflow scope or boundary/sequence selection, consult [coverage.md](references/coverage.md). Prioritize by impact and likely failure mechanisms. In an exhaustive request, prioritization changes order, not the promised scope.

## Investigate and validate

Trace inputs, decisions, state transitions, dependencies, and observable outputs. Choose probes that could expose or disprove a specific contract violation: boundaries, repeated actions, error recovery, cancellation, persistence, or concurrent completion where relevant. Exercise the actual implementation, retain the conditions and results, and update coverage as evidence arrives.

A defensible finding connects:

- **Contract:** required behavior and its basis.
- **Trigger:** reachable inputs, preconditions, or sequence.
- **Mechanism:** the violating path, accounting for callers and guards.
- **Consequence:** observable incorrect behavior and impact.
- **Evidence:** an executed counterexample or complete static argument, with inference identified.

Challenge candidates against upstream handling, supported preconditions, intended behavior, and probe artifacts. A suspicious pattern or absent test is a lead, not a finding. Reduce counterexamples only while preserving the relevant trigger. Keep candidates **validated**, **unresolved**, or **disproved**; distinguish severity from confidence.

Read [validation.md](references/validation.md) for ambiguous evidence, difficult runtime cases, mocks, ordering, or temporary test/instrumentation probes. Use existing property/stateful infrastructure when a valid invariant makes it useful; do not invent requirements or add a framework for a small audit.

A green suite supports only the scenarios and assertions exercised. Use runtime evidence to claim visual or end-to-end readiness; label static UI or workflow findings by their actual validation method. When runtime access is unavailable, continue useful static investigation and name the missing evidence. After confirming a mechanism, inspect related occurrences within scope when useful; similarity alone does not validate them.

## Complete the requested outcome

Reconcile the map before concluding: each planned area needs evidence or a concrete remaining gap. Continue beyond the first finding; neither a desired finding count nor an existing test suite replaces the requested coverage.

When repairs are included, address demonstrated mechanisms and verify original triggers plus risk-relevant neighboring behavior. Preserve validation, error handling, and test protection. Complete required checks; after they pass, repeat or broaden testing only when changes, failures, or unresolved concerns justify it. Continue any uncompleted coverage. For deeper diagnosis of a discovered failure, use [diagnosing-bugs](../diagnosing-bugs/SKILL.md) if available.

Remove only your temporary experiments, preserve user changes, and inspect retained edits. Report findings by impact with location, trigger, expected/actual behavior, mechanism, evidence, and uncertainty. Include repair and retest results when applicable, then summarize coverage, unresolved candidates, and limits. If no validated defects were found, say so within the examined scope. Describe a fix loop only when repairs were made and retested.

A dedicated security scan or product readiness audit needs its relevant workflow; this skill can support correctness investigation without replacing that scope. Read [provenance.md](references/provenance.md) only for source rationale, further study, or skill evaluation.
