---
name: diagnosing-bugs
description: Diagnose reported software failures or performance regressions and complete requested repairs. Use for a known symptom; use finding-bugs for proactive bug hunts.
---

# Diagnosing Bugs

Explain the mechanism behind the reported failure and complete the requested outcome. Use the request and prior context to distinguish diagnosis from repair. When asked to fix or resolve the problem, continue through implementation and verification without waiting for another instruction. For an explicitly diagnosis-only request, deliver the cause and repair direction without product edits.

Use the checklist below as an adaptive investigation loop. Reproduction, tracing, and experiments can inform each other; they need not occur in a fixed order. A clear failure may need one focused check. Ambiguous or extended work needs a compact investigation record.

## Establish a faithful failure check

- Identify expected behavior and its basis, the reported and observed behavior, trigger, impact, and relevant environment. Check the running build, configuration, state, and recent changes when they could explain the discrepancy. Read contracts or architecture notes where they bear on the failing path.
- Choose a check that exercises the actual implementation and trigger. Preserve lifecycle, ordering, and multiple callers when those matter; an isolated call cannot verify a multi-component failure.
- Capture the invocation or steps, relevant inputs, and result. Distinguish **FAIL** (the target failure), **PASS** (the relevant behavior exercised correctly), and **UNRESOLVED** (setup or observation prevented a verdict). A different exception is not reproduction of the report.
- Reduce the case only while preserving its failure signature and making investigation more useful. Keep the original scenario for final verification.

If reproduction is unavailable, continue with logs, traces, code, and provisional explanations. Identify the missing evidence and a useful next check; do not turn inability to reproduce into either a pass or a reason to stop all investigation.

## Distinguish explanations

Trace the trigger through callers and boundaries to the first divergence from the contract. Compare a working input, state, version, or configuration when useful. Suspicious code or a disappearing symptom alone does not establish the cause.

Choose the next probe by what it can distinguish and what it costs. For an ambiguous failure, consider credible competing explanations without inventing a quota. Connect each experiment to a predicted observation, then use the result to revise the explanation. Control relevant variables and restore experimental changes before unrelated probes; instrumentation can perturb timing.

For extended work, retain observations, hypotheses, predicted distinctions, probes/results, and next decisions in brief notes. Do not repeat an uninformative probe or stack speculative patches without a reason the result should change. If progress stalls, revisit an assumption, narrow a boundary, or obtain the missing evidence.

## Repair and demonstrate completion

For an authorized repair, make the smallest coherent change addressing the supported mechanism. Preserve intended behavior, validation, error handling, and existing test protection. Do not make the check pass by bypassing the failing path, swallowing errors, or weakening assertions without a behavioral justification.

Reuse or add a meaningful regression check at the seam that reaches the trigger. Where feasible, show it fails before the repair and passes after; a test already passing on the buggy version does not protect this regression. A missing convenient unit-test seam may call for integration, UI, or replay verification, rather than a redesign.

A repair is verified when the original scenario and relevant reduced check have been exercised after the change, required project checks and risk-relevant neighboring behavior have been checked, and temporary experiments have been removed without disturbing user changes. Once those checks pass, broaden or repeat them only for new changes, failures, or unresolved concerns. An exhaustive task still requires its full requested coverage.

Report the causal chain, repair if made, actual verification, and remaining uncertainty. Distinguish **diagnosed**, **repaired and verified**, **mitigated**, and **unresolved**. Label static evidence as static; a build or source review does not verify runtime UI behavior. A bounded search for the same mechanism can help when evidence points to other affected locations; validate each match.

## Conditional guidance

Read only the relevant section of [techniques.md](references/techniques.md) for intermittent failures, performance comparisons, history bisection, input reduction, UI/lifecycle checks, incidents, or human-assisted reproduction. Intermittent and performance claims need comparable measurements; a single clean run is insufficient.

Read [sources.md](references/sources.md) for provenance, further study, or evaluating changes to this skill. For proactive discovery, use [finding-bugs](../finding-bugs/SKILL.md) if available.
