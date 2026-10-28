# Bug discovery checklist

Use this to find unknown correctness defects in a repository, change set, or product. Loop between actions as evidence develops; not every area needs every technique. Record blocked actions as blocked, not passed.

## 1. Define the assignment

- [ ] Record repository/revision, workflows or diff, depth, time limits, runtime access, and exclusions. Inspect project guidance and starting changes; preserve user edits. Establish whether repairs are requested. A review allows reversible local probes within its constraints, but not unsolicited product fixes or permanent tests. Honor explicit read-only instructions.
- [ ] Before a broad hunt, map callers, boundaries, and consumers. For a diff, include relevant surrounding behavior. Use enough rows to expose the scope:

| Area / workflow | Contract and scenario | Method | Status and evidence |
|---|---|---|---|
| Behavior to inspect | Expected result and trigger | Trace, test, runtime | Planned / source examined / executed / blocked |

**Next:** choose an area; prioritization changes the order, not an exhaustive assignment's scope.

## 2. Establish expected behavior

- [ ] Write the expected result and its basis: specification, public contract, caller, documentation, or established invariant. Resolve conflicting evidence; existing code or a passing test alone is not the authority. If intent remains ambiguous, record the missing decision and continue independent areas.

**Evidence:** contract source and concrete expected result. **Next:** choose a scenario that can challenge it.

## 3. Choose a useful scenario

- [ ] Trace inputs, state changes, dependencies, and outputs. Select applicable scenarios, using [coverage guidance](coverage.md) for complex scope:
  - Empty, boundary, duplicate, or invalid inputs with defined handling.
  - Repeat, retry, reorder, undo, or cancel; a late completion after newer work.
  - Partial failure followed by recovery; save/reload or promised compatibility.
  - Conflicting operations or a supported dependency/configuration change.
- [ ] State the prediction or invariant and what observation would contradict it. Use existing property/stateful infrastructure when useful; do not invent idempotence or add a framework for a small audit.

**Next:** choose the cheapest faithful check, preserving relevant ordering and preconditions.

## 4. Check the real target

- [ ] Execute against the actual implementation using targeted tests, a faithful harness, or the relevant runtime. Use isolated state for mutations. Record command/steps, revision/configuration, inputs, assertions, and output. Temporary in-project probes are allowed within authorization; see [validation guidance](validation.md) when needed.
- [ ] Classify the result: **PASS** for exercised correct behavior, **FAIL** for the target violation, **UNRESOLVED** for setup or observation failure. A different exception is not confirmation. If execution is unavailable, continue static investigation and record the missing runtime evidence.

**Next:** passing checks return to coverage; failures become candidates. Unresolved checks need a changed approach or precise missing evidence, not endless identical retries.

## 5. Challenge the candidate

- [ ] Establish `supported trigger → reachable path → violated contract → observable consequence`. Check callers, guards, intended behavior, dependency semantics, and probe artifacts. A missing test or suspicious pattern is only a lead.
- [ ] Seek a counterexample invoking the real implementation or a complete static argument. Reduce only while preserving the claimed failure. Retain relevant schedules and conditions for intermittent cases; a clean stress run does not disprove them.

**Next:** mark **validated**, **disproved**, or **unresolved**, with the decisive evidence or missing premise. Inspect related occurrences within scope when useful; textual similarity alone proves nothing.

## 6. Triage without stopping coverage

- [ ] For each validated finding, record location, trigger, expected/actual behavior, mechanism, and affected users or data. Judge **severity** from reachable impact and **confidence** from evidence strength. Label static reasoning and unverified premises. Keep unresolved concerns separate.

**Next:** repair if included; otherwise resume the map. The first finding is not the finish line.

## 7. Repair when requested

- [ ] Address the supported mechanism with a coherent change. Preserve validation, error handling, and test protection; do not bypass the failing path or weaken assertions to obtain a pass. The optional [diagnosis checklist](../../diagnosing-bugs/references/checklist.md) offers deeper investigation when installed.
- [ ] Retain a meaningful regression check at the actual trigger. Where feasible, demonstrate failure before and success after. Rerun the original scenario, relevant reduced check, required project checks, and neighboring behavior selected from the change's risks.

**Next:** failed verification returns to investigation; unavailable verification means an unverified repair. Report **repaired and verified** only when relevant checks pass. Return to remaining coverage; repeat passed checks only for new changes, failures, or unresolved concerns.

## 8. Reconcile and report

- [ ] Account for every planned area with evidence or a concrete gap. Do not replace exhaustive coverage with sampling or the existing suite. For blocked work, name the missing access/evidence and next useful check. Report partial completion while coverage gaps remain.
- [ ] Remove only your temporary experiments, preserve intended repairs and user changes, and inspect retained edits. Lead with findings by impact, then repair results, coverage, unresolved concerns, and limits. Runtime evidence is required for visual or end-to-end readiness claims. No validated findings means none within the examined scope, not bug-free. Call it a fix loop only when repairs were made and retested.
