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

- [ ] Choose representative workflows from the requested scope and changed behavior; use the relevant code, callers, logs, and existing failures to orient the checks. Exercise those workflows even when source inspection has produced no candidate defect. Observe the changed outcome and surrounding behavior users or consumers still depend on. Plausible code and passing lower-level checks do not replace observing that outcome.
- [ ] Prefer the affected UI, CLI, or API workflow in a representative environment for discovery and candidate reproduction. Automation can drive that workflow; manual interaction or production access is not required. Preserve relevant version, configuration, data, state, and action order; use isolated state for mutations. Select checks proportional to the change and scope rather than launching an expensive environment for every edit. If execution is unavailable or outside the requested scope, record what was not exercised and why; continue useful independent investigation without implying runtime coverage.
- [ ] If the workflow is unavailable, or a candidate remains unreproduced after a reasonable attempt, reuse, adapt, or build the smallest faithful test against the real implementation. Check a supported contract; preserve reachable preconditions and, for a suspected failure, its signature. Copied logic, impossible state, or an unrelated exception does not validate a candidate. Reuse existing fixtures before building a harness. Temporary probes remain subject to authorization; honor source-only or read-only scope and do not repeat uninformative runtime attempts indefinitely. Include relevant boundary inputs or sequences where warranted; a normal-path pass alone does not cover them.
- [ ] Classify **PASS** (exercised correct behavior), **FAIL** (target violation), or **UNRESOLVED** (setup/observation failure). Another exception is not confirmation. If execution is unavailable, continue useful static investigation and record the missing runtime evidence.
- [ ] Record discovery coverage as **actual workflow observed**, **test-only coverage**, **source examined**, or **not exercised**, with conditions, observer/source, steps/command, assertions, and observed output or reason not exercised. Launching the product or driving steps without inspecting the relevant result does not establish outcome coverage.
- [ ] For a candidate failure, additionally record reproduction evidence: **actual use**, **test only**, or **not yet reproduced**. Retain each attempt's result even when a fallback later succeeds. An automated test driving the representative application workflow can count as actual use; an isolated test or substituted integration boundary cannot establish that the full workflow failed. Reuse useful existing evidence instead of repeating it solely to satisfy the sequence; a static finding remains labeled static.
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
- [ ] Retain a meaningful regression check at the actual trigger. Where feasible, demonstrate failure before and success after. Rerun the original scenario, relevant reduced check, required project checks, and neighboring behavior selected from the change's risks. If only a fallback test can run, report test-level verification with the actual-use gap and retry the actual workflow when available; an isolated test does not establish end-to-end verification.
- [ ] Check whether affected data or persisted state also needs recovery within the authorized scope. Verify the affected existing state as well as fresh behavior; distinguish preventing new damage from repairing prior damage, and report any remaining recovery work.

**Next:** failed verification returns to investigation; unavailable verification means an unverified repair. Report **repaired and verified** only when relevant checks pass. Return to remaining coverage; repeat passed checks only for new changes, failures, or unresolved concerns.

## 7. Reconcile and report

- [ ] Account for every planned area with evidence or a concrete gap, including representative workflows not exercised because no candidate was found in source. Source inspection and passing lower-level checks do not complete a planned runtime check. Do not replace exhaustive coverage with sampling or the existing suite. For blocked work, name the missing access/evidence and next useful check. Report partial completion while required coverage gaps remain; an explicitly source-only review can be complete within that scope while disclosing its runtime limits.
- [ ] Remove only your temporary experiments, preserve intended repairs and user changes, and inspect retained edits. Lead with findings by impact, then repair results, coverage, unresolved concerns, and limits. Runtime evidence is required for visual or end-to-end readiness claims. No validated findings means none within the examined scope, not bug-free. Call it a fix loop only when repairs were made and retested.
