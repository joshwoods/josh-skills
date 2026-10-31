---
name: finding-bugs
description: Find and validate correctness defects in a requested code or product scope. Use for proactive bug hunts and correctness reviews, rather than diagnosing a reported failure.
---

# Finding Bugs

Read and follow the [bug discovery checklist](references/checklist.md). It is the shared playbook for humans and agents: define coverage, start with quick relevant checks, validate leads, escalate unresolved work, and complete authorized repairs and remaining coverage.

Discover through use as well as source inspection: exercise representative workflows in scope even when no candidate defect has emerged. Observe the changed behavior and the surrounding behavior users or consumers depend on. Plausible code or passing lower-level checks do not replace that observation; record a coverage gap when the workflow was not exercised. Choose checks proportional to the task rather than launching an expensive environment for every edit.

When reproducing a candidate defect, prefer actual use first; use a faithful test as the fallback when the affected workflow is unavailable or a reasonable attempt does not reproduce it. Keep actual-use, test-only, and not-yet-reproduced evidence distinct, including when verifying a repair.

Choose the lowest-effort check that can answer the current question. Normally progress from existing evidence and focused checks to targeted sequences or replay, then expensive environment, stress, property, or history investigations only when warranted. This is an effort ladder, not a requirement to try every technique: unrelated cheap checks add no value, and low cost does not excuse weak validation or incomplete exhaustive coverage. A supported cause can proceed directly to authorized repair and verification.

Preserve the user's scope and existing work. An audit permits investigation and reversible probes within its constraints; retain product fixes or permanent test changes only when authorized. When asked to find and fix bugs, continue through repair, verification, and remaining coverage without waiting for another instruction.

For a reported failure or deeper diagnosis of a discovered defect, the [diagnosis and repair checklist](../diagnosing-bugs/references/checklist.md) is available when that sibling skill is installed. The discovery checklist includes a local repair path, so this skill also works independently.

Read additional references only when needed:

- [Coverage](references/coverage.md): choosing meaningful boundaries, state sequences, and behavioral oracles; tracing replacements, skipped evaluation, shared eligibility rules, and actual consumers.
- [Validation](references/validation.md): ambiguous evidence, review/history clues, consumer-level assertions, revision and scope limits, difficult runtime cases, or temporary probes.
- [Provenance](references/provenance.md): source rationale, further study, or evaluating the skill itself.

A dedicated security scan or product readiness audit needs its relevant workflow; this checklist can support correctness investigation without replacing that scope.
