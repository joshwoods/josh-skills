# Bug discovery checklist

Use this to find unknown correctness defects in a repository, change set, or product. Start with the lowest-effort relevant check: **existing evidence and quick checks → targeted experiments → expensive investigations when warranted**. Actual cost and relevance decide; do not run unrelated cheap probes or every technique. Record blocked actions as blocked, not passed.

## 1. Define the assignment

- [ ] Record repository/revision, workflows or diff, depth, time limits, runtime access, and exclusions. Inspect project guidance and starting changes; preserve user edits. Establish whether repairs are requested. A review allows reversible local probes within its constraints, but not unsolicited product fixes or permanent tests. Honor explicit read-only instructions.
- [ ] Establish the expected result and its basis: specification, public contract, caller, documentation, or invariant. Existing code or a passing test alone is not the authority. Resolve conflicting evidence; if intent remains ambiguous, record the missing decision and continue independent areas.
- [ ] Before a broad hunt, map callers, boundaries, and consumers. For a diff, include relevant surrounding behavior. Use enough rows to expose the scope:

| Area / workflow | Contract and scenario | Method | Status and evidence |
|---|---|---|---|
| Behavior to inspect | Expected result and trigger | Trace, test, runtime | Planned / source examined / executed / blocked |

**Next:** choose an area and start with quick relevant checks. Prioritization changes the order, not an exhaustive assignment's scope.

## 2. Start with quick, relevant checks

- [ ] Inspect the relevant change/path, callers, existing failures, and available errors or logs. Run an existing focused check or straightforward normal interaction where useful. Try a cheap contract-based example such as empty, boundary, duplicate, null, or optional input; a normal-path pass alone does not cover those cases.
- [ ] Check the actual implementation using existing tests, a faithful harness, or the runtime. Preserve relevant state and ordering; use isolated state for mutations. Record command/steps, revision/configuration, inputs, assertions, and output. Temporary probes remain subject to authorization.
- [ ] Classify **PASS** (exercised correct behavior), **FAIL** (target violation), or **UNRESOLVED** (setup/observation failure). Another exception is not confirmation. If execution is unavailable, continue useful static investigation and record the missing runtime evidence.
- [ ] For frontend/API paths, compare intended action → actual request → raw response against the contract → client state → rendered output. Localize the first mismatch before assigning ownership. Retain the matching exchange and starting state; use [coverage guidance](coverage.md#frontend-and-backend-data-boundaries) when localization needs more detail.

**Next:** take leads to step 3. A pass covers only its exercised scenario: return to another quick check or escalate remaining scenarios in step 4. When the map is complete, go to step 7. Do not stop after the first finding.

## 3. Validate the lead with the least additional work

- [ ] Establish `supported trigger → reachable path → violated contract → observable consequence`. Check callers, guards, intended behavior, dependency semantics, and probe artifacts. A suspicious pattern or missing test is only a lead.
- [ ] Use the available counterexample, a focused reproduction, or a complete static argument. State what could disprove the candidate; obtain only the additional evidence needed. Reduce only while preserving the claimed failure. Consult [validation guidance](validation.md) for ambiguous evidence or probe design.

**Next:** **validated** → step 5, then repair if requested; **disproved** → record why and resume coverage; **unresolved** → identify the missing premise and choose a discriminating experiment in step 4. A supported cause needs no further technique quota.

## 4. Escalate unresolved questions and coverage

- [ ] Choose the next experiment from the unresolved contract or mechanism. Start with a focused sequence, trace, isolated fault, or captured-data replay when it can answer the question. Examples include retry/reorder/cancel, late completions, partial failure then recovery, save/reload, or existing/upgraded state versus fresh state. For malformed responses, test the specified error handling. Preserve supported preconditions; use [coverage guidance](coverage.md) for scenario selection.
- [ ] Escalate to costly environment reconstruction, long integration runs, broad property/stress searches, multi-version comparisons, or bisection only when cheaper relevant evidence is insufficient or the requested coverage requires it. State the question and predicted distinction first. Use existing infrastructure; do not invent properties or build a framework for a small audit.
- [ ] Retain results, conditions, and intermittent schedules/trial counts. A clean stress run does not establish absence. Update the map after each experiment; do not repeat an uninformative probe without a reason its result should change.

**Next:** new evidence returns to step 3 or resolves its coverage row. If blocked, record the missing evidence and next useful check, then continue independent areas. Cost alone does not remove an exhaustive obligation; disclose unfinished work rather than claiming completion.

## 5. Triage without stopping coverage

- [ ] For each validated finding, record location, trigger, expected/actual behavior, mechanism, and affected users or data. Judge **severity** from reachable impact and **confidence** from evidence strength. Label static reasoning and unverified premises. Keep unresolved concerns separate.
- [ ] Inspect related occurrences within scope when useful; textual similarity alone does not validate them.

**Next:** repair in step 6 if included; otherwise resume the map at its next appropriate effort level.

## 6. Repair when requested

- [ ] Address the supported mechanism with a coherent change. Preserve validation, error handling, and test protection; do not bypass the failing path or weaken assertions to obtain a pass. The optional [diagnosis checklist](../../diagnosing-bugs/references/checklist.md) offers deeper investigation when installed.
- [ ] Retain a meaningful regression check at the actual trigger. Where feasible, demonstrate failure before and success after. Rerun the original scenario, relevant reduced check, required project checks, and neighboring behavior selected from the change's risks.
- [ ] Check whether affected data or persisted state also needs recovery within the authorized scope. Verify the affected existing state as well as fresh behavior; distinguish preventing new damage from repairing prior damage, and report any remaining recovery work.

**Next:** failed verification returns to investigation; unavailable verification means an unverified repair. Report **repaired and verified** only when relevant checks pass. Return to remaining coverage; repeat passed checks only for new changes, failures, or unresolved concerns.

## 7. Reconcile and report

- [ ] Account for every planned area with evidence or a concrete gap. Do not replace exhaustive coverage with sampling or the existing suite. For blocked work, name the missing access/evidence and next useful check. Report partial completion while coverage gaps remain.
- [ ] Remove only your temporary experiments, preserve intended repairs and user changes, and inspect retained edits. Lead with findings by impact, then repair results, coverage, unresolved concerns, and limits. Runtime evidence is required for visual or end-to-end readiness claims. No validated findings means none within the examined scope, not bug-free. Call it a fix loop only when repairs were made and retested.
