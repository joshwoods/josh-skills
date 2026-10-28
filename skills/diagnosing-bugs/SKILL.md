---
name: diagnosing-bugs
description: Diagnose reported software failures or performance regressions and complete requested repairs. Use for a known symptom; use finding-bugs for proactive bug hunts.
---

# Diagnosing Bugs

Read and follow [the diagnosis and repair checklist](references/checklist.md). It is the shared workflow for humans and agents: establish the failure, collect faithful evidence, distinguish explanations, repair when requested, and verify the actual outcome.

Use the request and prior context to decide whether completion means diagnosis, mitigation, or a verified repair. When asked to fix or resolve the problem, continue through implementation and verification. For explicitly diagnosis-only work, deliver the explanation and repair direction without product edits.

Use the checklist as a working guide, not a fixed itinerary or a quota of experiments. Keep evidence proportional to the problem; record longer investigations so probes and speculative patches do not repeat. Preserve PASS, FAIL, and UNRESOLVED distinctions. A blocked runtime check does not prevent useful static investigation and does not justify claiming a verified repair.

Read supporting material only when it helps the current task:

- [Frontend boundaries](references/frontend-boundary.md): reproducing UI failures and distinguishing request defects, backend data/contract problems, and client handling errors.
- [Techniques](references/techniques.md): intermittent failures, performance, history bisection, input reduction, UI/lifecycle behavior, incidents, and human-assisted reproduction.
- [Sources](references/sources.md): provenance, further study, or evaluation of this method.
- [Finding Bugs](../finding-bugs/SKILL.md), if available: proactive discovery and coverage of unknown defects.

The checklist and local references contain the complete diagnosis workflow; no repository-level document is required after installation.
