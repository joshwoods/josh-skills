# Diagnose and fix a bug

Use this checklist when there is a specific failure or performance regression to explain. A human or an LLM can keep the same working record. Start with the first unanswered question; revisit earlier steps when evidence changes. A straightforward bug can move through these checks quickly.

Check a box when you have its evidence. Mark an inapplicable item **N/A** with a short reason; record blocked work explicitly. Writing a plausible explanation is not completion of an experiment.

## 1. What is wrong?

- [ ] Write: **“When [trigger], I expected [behavior], but observed [result].”** Identify why the expectation is correct: a requirement, API contract, caller, or accepted example. Separate the report from what you have observed yourself.
- [ ] Record the relevant build/version, configuration, input, state, and impact. Check that the code being inspected is the code actually running.
- [ ] Establish the intended outcome from the task: diagnosis, mitigation, or a verified repair. A request to fix the problem includes carrying the repair through verification.

**Next:** If expected behavior is unclear, resolve that ambiguity while investigating what you can. During an incident, perform authorized mitigation and preserve evidence; restored service does not by itself explain the cause.

## 2. How will we tell whether it failed?

- [ ] Run or reconstruct the original steps using the actual implementation. Save the command or actions, inputs, and observed output. Preserve timing, lifecycle, and multiple callers when they matter.
- [ ] Classify the result: **FAIL** = the target failure; **PASS** = the relevant behavior exercised correctly; **UNRESOLVED** = setup or observation prevented a verdict. Another exception is not the same failure.
- [ ] If a smaller case would help, reduce it while preserving the failure signature. Keep the original scenario for final verification.

**Next:** If the failure occurs, go to step 3. If it does not, inspect available logs, traces, dumps, history, or static evidence; provisional explanations can help build a reproduction. For intermittent failures, record failures/trials and conditions. If remaining progress needs unavailable evidence, record the missing item and next decisive check in step 8; continue independent work.

## 3. Where does behavior first go wrong?

- [ ] Follow the relevant input or state through callers and component boundaries. Locate the earliest supported divergence between expected and actual behavior.
- [ ] Compare a working input, caller, configuration, or version where useful. Check guards and assumptions around suspicious code; a recent change or suspicious line is a lead, not proof.

**Keep:** A short path such as `trigger → caller → state change → incorrect result`, with evidence at the disputed boundary.

## 4. What experiment would distinguish the explanations?

- [ ] State the most plausible explanation and, where ambiguous, a credible alternative. Do not invent a fixed number of hypotheses.
- [ ] Before running a probe, write what observation would support or contradict the explanation. Choose the cheapest useful discriminating check: a trace, breakpoint, boundary assertion, comparison, or controlled input change.
- [ ] Execute the probe and record its result. Control relevant variables and restore experimental changes before an unrelated probe; instrumentation can change timing.

For extended work, use a compact log:

| Explanation | Predicted observation | Probe and actual result | Conclusion / next action |
| --- | --- | --- | --- |
| | | | |

**Next:** Revise or discard explanations contradicted by evidence. If a probe teaches nothing, change the probe or revisit an assumption. Do not repeat it or accumulate speculative patches without a reason the outcome should change.

## 5. Is the cause supported?

- [ ] Connect the reachable trigger, executed path, incorrect operation/state, violated expectation, and observed consequence. Identify which links are observed and which are inferred.
- [ ] Check that the explanation accounts for the original failure and survives the strongest relevant alternative. A disappearing symptom alone is insufficient.

**Next:** If unsupported, return to steps 3–4 with a better question, or record the evidence blocker. A complete static argument can support a diagnosis, but label it as static. For diagnosis-only work, report the cause, evidence, uncertainty, and repair direction in step 8. If repair is requested, continue below.

## 6. What change addresses that cause?

- [ ] Make the smallest coherent repair that preserves intended behavior, validation, error handling, and existing test protection. Do not hide the failure by bypassing the path or weakening assertions without a behavioral justification.
- [ ] Reuse or add a regression check that reaches the real trigger. Where feasible, demonstrate that it fails on the buggy version and passes on the repair. Use an integration, UI, or replay check when a unit test cannot exercise the failure.

**Next:** Verify the change; an implemented repair is not yet a verified repair.

## 7. Does the repair hold up?

- [ ] Exercise the original scenario and relevant reduced check after the change. For intermittent or performance failures, compare equivalent conditions and report trials or measurements and their limits.
- [ ] Check risk-relevant neighboring behavior and complete required project checks. Use runtime evidence for claims about actual UI interaction or end-to-end behavior.
- [ ] Verify final conditions with temporary instrumentation removed wherever removal can change behavior, especially timing.

**Next:** Target failure remains → return to investigation. A new regression → diagnose and fix it. Verification unavailable or inconclusive → label the repair unverified or partially verified and state the gap. Checks pass → close; broaden or repeat testing only for new changes, failures, or unresolved concerns.

## 8. What can we honestly conclude?

- [ ] Remove only temporary experiments and inspect the retained diff, including after diagnosis-only work. Preserve intended repairs and unrelated user changes.
- [ ] Record the outcome: **diagnosed**, **repaired and verified**, **mitigated**, or **unresolved / repair not fully verified**. Include the cause, retained change, actual checks, and material uncertainty.
- [ ] If this bug belongs to a larger hunt, return to its remaining coverage. Search nearby code for the same mechanism when useful, and validate each match before calling it another defect.

For specialized techniques, consult the relevant section of [techniques.md](techniques.md). For method sources and limitations, see [sources.md](sources.md). Neither a checked checklist nor a green build proves that every bug is gone.
