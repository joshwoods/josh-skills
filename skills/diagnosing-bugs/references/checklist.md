# Diagnose and fix a bug

Use this checklist when there is a specific failure or performance regression to explain. A human or an LLM can keep the same working record. Investigation is ordered from quick checks to more costly work: basic facts → simple reproduction → existing evidence and focused history → targeted experiments → expensive escalation. Start with the first unanswered question; use only checks relevant to the failure. A clear cause lets you skip remaining investigation and move to the requested repair or report.

The order is a default, not a requirement to try every cheaper technique. Follow evidence when a particular check is clearly decisive. Required verification still applies even when it is expensive.

Check a box when you have its evidence. Mark an inapplicable item **N/A** with a short reason; record blocked work explicitly. Writing a plausible explanation is not completion of an experiment.

## 1. Quick triage: what is wrong?

- [ ] Write: **“When [trigger], I expected [behavior], but observed [result].”** Identify why the expectation is correct: a requirement, API contract, caller, or accepted example. Separate the report from what you have observed yourself.
- [ ] Record the relevant build/version, configuration, input, state, and impact. Check that the code being inspected is the code actually running.
- [ ] If this previously worked, record readily available last-observed-good and first-observed-bad version facts and their evidence. Leave missing identities as unknown for now; do not begin rebuilding old releases before trying a simple reproduction. First detection is not necessarily introduction.
- [ ] Establish the intended outcome from the task: diagnosis, mitigation, or a verified repair. A request to fix the problem includes carrying the repair through verification.

**Next:** If expected behavior is unclear, resolve that ambiguity while investigating what you can. During an incident, perform authorized mitigation and preserve evidence; restored service does not by itself explain the cause.

## 2. Quick attempt: can we reproduce it?

- [ ] Prefer reproducing through actual use first: follow the affected UI, CLI, or API workflow in a representative environment, with the relevant version, configuration, data, state, and action order. Automation can drive this workflow; manual interaction or production access is not required. Use isolated state for mutations within the task's authorization. Save the steps, inputs, and result; preserve timing, lifecycle, and multiple callers when they matter.
- [ ] For a frontend failure, preserve the relevant route, session/data/cache state, action order, and matching request/response. Use the [frontend reproduction and data-boundary checklist](frontend-boundary.md) when reproducing or locating the mismatch is difficult.
- [ ] If that workflow is unavailable or a reasonable attempt does not reproduce the failure, reuse, adapt, or build the smallest faithful test that can expose the same failure in the real implementation. Use available evidence to preserve reachable inputs, state, and ordering; an impossible setup, copied implementation, or unrelated exception does not reproduce the reported bug. Reuse existing fixtures before building a harness, and do not repeat uninformative real-use attempts indefinitely.
- [ ] Classify the result: **FAIL** = the target failure; **PASS** = the relevant behavior exercised correctly; **UNRESOLVED** = setup or observation prevented a verdict. Another exception is not the same failure.
- [ ] Separately record the reproduction evidence: **actual use**, **test only**, or **not yet reproduced**, with the conditions and observer/source. A test driving the representative application workflow can count as actual use; an isolated test or substituted integration boundary cannot establish that the full workflow failed. Preserve useful existing reproduction evidence instead of repeating it solely to satisfy the sequence.
- [ ] Simplify the case if it is quick and preserves the failure signature. Keep the original scenario; defer building a new harness or extensive reduction until cheaper checks leave a question it can answer.

**Next:** If the failure occurs, go to step 3. If it does not, inspect available logs, traces, dumps, history, or static evidence; provisional explanations can help build a reproduction. For intermittent failures, record failures/trials and conditions. If remaining progress needs unavailable evidence, record the missing item and next decisive check in step 8; continue independent work.

## 3. Cheap evidence: is there an obvious mismatch?

- [ ] Read the relevant existing error/stack trace, console or network result, and targeted test output. Check straightforward mismatches in build, configuration, input, or state before adding instrumentation.
- [ ] Follow the small relevant input/state path far enough to identify the first supported mismatch. Start from the error, failed assertion, or incorrect value; expand tracing only when the evidence requires it.
- [ ] For frontend/API behavior, check the outbound request, raw response against the contract, client transformations/state, and rendered result. Distinguish incorrect backend data, valid-but-unexpected data, and incorrect client handling; more than one boundary can be defective.
- [ ] Compare a working input, caller, configuration, or version where useful. Check guards and assumptions around suspicious code; a recent change or suspicious line is a lead, not proof.
- [ ] For a regression, inspect a brief relevant history summary or diff and note changes in flags, dependencies, runtime, API/schema, or data. Use the early steps of the [history checklist](regression-history.md); reserve historical rebuilds and bisect for escalation.

**Keep:** A short path such as `trigger → caller → state change → incorrect result`, with evidence at the disputed boundary.

## 4. Focused experiments: what would distinguish the explanations?

- [ ] State the most plausible explanation and, where ambiguous, a credible alternative. Do not invent a fixed number of hypotheses.
- [ ] Before running a probe, write what observation would support or contradict the explanation. Choose the cheapest useful discriminating check: a trace, breakpoint, boundary assertion, comparison, or controlled input change.
- [ ] Execute the probe and record its result. Control relevant variables and restore experimental changes before an unrelated probe; instrumentation can change timing.

For extended work, use a compact log:

| Explanation | Predicted observation | Probe and actual result | Conclusion / next action |
| --- | --- | --- | --- |
| | | | |

**Next:** Revise or discard explanations contradicted by evidence. If a probe teaches nothing, change the probe or revisit an assumption. Do not repeat it or accumulate speculative patches without a reason the outcome should change.

## 5. Decide, or escalate only if still unresolved

- [ ] Connect the reachable trigger, executed path, incorrect operation/state, violated expectation, and observed consequence. Identify which links are observed and which are inferred.
- [ ] Check that the explanation accounts for the original failure and survives the strongest relevant alternative. A disappearing symptom alone is insufficient.

**If supported:** For diagnosis-only work, report the cause, evidence, uncertainty, and repair direction in step 8. If repair is requested, go to step 6. Label a static diagnosis as static.

**If unresolved:** Choose the least costly remaining method that could change the diagnosis. The usual escalation order is:

1. A bounded debugger/instrumentation probe, captured-data replay, or focused regression check.
2. A new faithful integration harness, substantial input reduction, or controlled comparison of code versus environment/data. Reuse available fixtures and artifacts first.
3. Repeated timing/stress runs, profiling under representative load, or reconstructing difficult environments when required by the symptom.
4. Historical rebuilds and [manual/automated bisect](regression-history.md#4-narrow-a-large-interval-with-bisect), once known-good/bad endpoints and a reliable failure check justify the setup.

Actual cost depends on existing tooling; a ready-made decisive check can move earlier. Each escalation needs a question cheaper evidence did not answer. Do not perform every method or keep retrying without new information. If remaining progress needs unavailable access/evidence, record the blocker and continue independent work.

## 6. Repair the supported cause

- [ ] Make the smallest coherent repair that preserves intended behavior, validation, error handling, and existing test protection. Do not hide the failure by bypassing the path or weakening assertions without a behavioral justification.
- [ ] Reuse or add a regression check that reaches the real trigger. Where feasible, demonstrate that it fails on the buggy version and passes on the repair. Use an integration, UI, or replay check when a unit test cannot exercise the failure.
- [ ] Determine whether the bug already left incorrect records, stale persisted/cache state, or queued effects. Separate preventing recurrence from recovering affected state. Perform recovery only within the task's authorization; report outstanding damage or recovery work explicitly.

**Next:** Verify the change; an implemented repair is not yet a verified repair.

## 7. Does the repair hold up?

- [ ] Exercise the original scenario and relevant reduced check after the change. If only a fallback test can run, verify against it and report test-level verification with the actual-use gap; retry the actual workflow when available. Do not claim end-to-end verification from an isolated test. For intermittent or performance failures, compare equivalent conditions and report trials or measurements and their limits.
- [ ] Check risk-relevant neighboring behavior and complete required project checks. Use runtime evidence for claims about actual UI interaction or end-to-end behavior.
- [ ] Where existing state was affected, verify recovery from that state as well as behavior with fresh state. A passing clean install does not establish that existing users have recovered.
- [ ] Verify final conditions with temporary instrumentation removed wherever removal can change behavior, especially timing.

**Next:** Target failure remains → return to investigation. A new regression → diagnose and fix it. Verification unavailable or inconclusive → label the repair unverified or partially verified and state the gap. Checks pass → close; broaden or repeat testing only for new changes, failures, or unresolved concerns.

## 8. What can we honestly conclude?

- [ ] Remove only temporary experiments and inspect the retained diff, including after diagnosis-only work. Preserve intended repairs and unrelated user changes.
- [ ] Record the outcome: **diagnosed**, **repaired and verified**, **mitigated**, or **unresolved / repair not fully verified**. Include the cause, retained change, actual checks, and material uncertainty.
- [ ] If this bug belongs to a larger hunt, return to its remaining coverage. Search nearby code for the same mechanism when useful, and validate each match before calling it another defect.

For specialized techniques, consult the relevant section of [techniques.md](techniques.md). For method sources and limitations, see [sources.md](sources.md). Neither a checked checklist nor a green build proves that every bug is gone.
