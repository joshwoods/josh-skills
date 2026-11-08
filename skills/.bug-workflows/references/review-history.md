# Use review and history as clues

Read this when prior changes, reviews, or corrections can inform the current question. A focused search does not require known good/bad endpoints and does not justify reading every discussion before trying the affected workflow.

Extract the invariant behind a warning and turn it into a prediction about the current revision, effective configuration, and request. Compare the recorded scope with the actual callers and consumers. History supplies hypotheses; a suspicious patch, approval, or thread status is not a verdict.

| Historical clue | What to check now |
| --- | --- |
| Unsafe replacement or missing safeguard | Other reachable consumers that depend on the same invariant. |
| A correction handles named exceptions | Whether it restores the invariant or leaves equivalent cases reachable. Validate a new occurrence separately; do not report a corrected historical example as still defective. |
| Behavior depends on another change | Whether the dependency is actually present in the tested environment and deployed or initialized in the required order. Merging or planning a release does not establish that. |
| Validation is deferred or pending | Whether later evidence closes that exact gap. Missing evidence means unverified, not proof testing never occurred. |
| A later change expands an abstraction | Whether prior assumptions and checks cover newly affected consumers, configurations, and populations. |
| Approval predates consequential edits | The intervening changes and later review or validation of the final behavior. |
| Configuration history adds an override | Its recorded purpose, effective scope, and whether removal actually took effect. |
| A thread is resolved, outdated, open, or labeled fixed | Correction commits, subsequent edits, and final downstream behavior. Metadata proves neither remediation nor persistence. |

Distinguish an **explicit warning about the exact failure**, a **related warning about its mechanism or invariant**, and a **hindsight inference**. A related concern does not establish that someone anticipated and ignored this exact bug.

For consequential ambiguity, keep a short clue record in existing notes:

`clue + original source/revision → invariant → recorded response/correction → current applicability and predicted failure → explicit/related/hindsight → checked result or pending evidence`

Use only fields needed for the investigation; no separate ledger is required. Unknown prerequisites remain unknown. Preserve evidence lineage: summaries or reposts of one analysis are not independent confirmations. Distinguish recorded configuration ownership, change actors, authors, reviewers, and mergers from inferred intent or review depth; a role label or approval does not establish what someone inspected or understood.
