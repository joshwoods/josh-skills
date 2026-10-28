---
name: finding-bugs
description: Find and validate correctness defects in a requested code or product scope. Use for proactive bug hunts and correctness reviews, rather than diagnosing a reported failure.
---

# Finding Bugs

Read and follow the [bug discovery checklist](references/checklist.md). It is the shared playbook for humans and agents: define coverage, choose meaningful scenarios, validate candidates, complete authorized repairs, and account for the remaining scope.

Use the checklist as an investigation loop, not a requirement to try every technique. Preserve the user's scope and existing work. An audit permits investigation and reversible probes within its constraints; retain product fixes or permanent test changes only when authorized. When asked to find and fix bugs, continue through repair, verification, and remaining coverage without waiting for another instruction.

For a reported failure or deeper diagnosis of a discovered defect, the [diagnosis and repair checklist](../diagnosing-bugs/references/checklist.md) is available when that sibling skill is installed. The discovery checklist includes a local repair path, so this skill also works independently.

Read additional references only when needed:

- [Coverage](references/coverage.md): choosing meaningful boundaries, state sequences, and behavioral oracles across workflows.
- [Validation](references/validation.md): ambiguous evidence, difficult runtime cases, mocks, ordering, or temporary test/instrumentation probes.
- [Provenance](references/provenance.md): source rationale, further study, or evaluating the skill itself.

A dedicated security scan or product readiness audit needs its relevant workflow; this checklist can support correctness investigation without replacing that scope.
