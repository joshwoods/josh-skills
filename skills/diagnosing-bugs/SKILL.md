---
name: diagnosing-bugs
description: Diagnose reported software failures or performance regressions and complete requested repairs. Use for a known symptom; use finding-bugs for proactive bug hunts.
---

# Diagnosing Bugs

Read and follow [the diagnosis and repair checklist](references/checklist.md). It is the shared workflow for humans and agents: establish the failure, collect faithful evidence, distinguish explanations, repair when requested, and verify the actual outcome.

Use the request and prior context to decide whether completion means diagnosis, mitigation, or a verified repair. When asked to fix or resolve the problem, continue through implementation and verification. For explicitly diagnosis-only work, deliver the explanation and repair direction without product edits.

Prefer reproduction through actual use first; use a faithful test as the fallback when the affected workflow is unavailable or a reasonable attempt does not reproduce it. Keep actual-use, test-only, and not-yet-reproduced evidence distinct, including when verifying a repair.

Follow its low-to-high effort investigation order: quick triage and reproduction, existing evidence and focused history, targeted experiments, then expensive escalation such as historical rebuilds or bisect. Skip remaining investigation once the cause is sufficiently supported. Choose relevant checks; do not exhaust cheaper but unrelated techniques or skip required verification. Keep longer investigations recorded so probes and speculative patches do not repeat. Preserve PASS, FAIL, and UNRESOLVED distinctions. A blocked runtime check does not prevent useful static investigation and does not justify claiming a verified repair.

Read supporting material only when it helps the current task:

- [Frontend boundaries](references/frontend-boundary.md): reproducing UI failures and distinguishing request defects, backend data/contract problems, and client handling errors.
- [Configuration and rollouts](references/configuration-and-rollouts.md): decision origins, defaults, actual serving paths, differing reports, and rollback behavior.
- [Regression history](references/regression-history.md): last-known-good versions, review warnings and correction history as leads, release-to-commit mapping, changed context, and bisect.
- [Techniques](references/techniques.md): intermittent failures, performance, history bisection, input reduction, UI/lifecycle behavior, incidents, and human-assisted reproduction.
- [Sources](references/sources.md): provenance, further study, or evaluation of this method.
- [Finding Bugs](../finding-bugs/SKILL.md), if available: proactive discovery and coverage of unknown defects.

The checklist and local references contain the complete diagnosis workflow; no repository-level document is required after installation.
