# Configuration decisions and rollout diagnosis

Use this when a symptom depends on configuration, substituted defaults, migration routing, or rollback. Start with available request evidence and focused source/configuration reads. Escalate only to resolve a remaining question; this is not a required audit for every bug.

## Keep reports separate until the mechanism connects them

For materially different reports, keep a compact row with relevant facts:

| Time / request | Account or device context | Build / configuration revision | Actual producer | Observed result | Candidate mechanism and evidence |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

Similar output can arise from different causes. A report before activation, from an unaffected population, or with a distinct override challenges an explanation based only on the rollout. It does not automatically disprove that explanation for other reports. Preserve unknowns and use only the identity detail needed to distinguish cases; do not copy sensitive identifiers into shared writeups unnecessarily.

## Collect supplied correlation evidence

Use supplied request/trace IDs through supported sources early. An empty result means that lookup returned no evidence under its source, time range, and filters; it does not establish that the request has no useful logs. Where available and authorized, check correlated logs or request records before asking for information they may already contain.

Use the returned identity, effective configuration, producer, and output to guide the focused tracing below; leave unavailable fields unknown.

## Resolve the decision's origin and consumer

- Identify the authoritative configuration system, namespace, configuration type, deployment scope, and effective revision. A not-found lookup in one system does not prove deletion or non-use. A repository configuration file is not necessarily the deployed configuration.
- Distinguish an evaluated rule result, explicit account/device override, gate-imposed replacement, missing/error fallback, and cached value. Record the matched rule and configuration revision when available. A returned value alone does not establish why it was selected; unavailable provenance remains a missing premise.
- Treat a default as executable behavior. `control`, `false`, empty, null, and “not evaluated” can select different consumer branches, trigger another configuration lookup, or skip work. Trace the actual replacement through those effects to the user or downstream consumer. For example, a default export format might load encoder settings, while an absent format might skip export entirely. Neither behavior is inherently defective; judge it against the supported contract.
- Separate assignment, routing, fallback, shadow execution, and the implementation producing the response. Before treating a legacy dependency as irrelevant, establish whether that path still runs for the affected request through partial migration or fallback. A shadow invocation need not produce the served result.
- For bulk gates or wrappers, inspect the actual reachable readers and consumers, including inherited/indirect reads and framework-created dependencies. Metadata, class names, or lifecycle labels can locate leads but cannot establish preserved behavior. Use the relevant consumer contract to interpret unknown or missing eligibility values, rather than assuming they belong in the enabled population.

Prefer the affected actual workflow for evidence. If it is unavailable, a faithful check at the consumer boundary can distinguish the suspected paths. A test asserting that a lookup was skipped or a fallback value was returned establishes that mechanism, not preservation of the consumer's output or side effects. Label static conclusions and unexercised boundaries explicitly.

## Interpret correlated observations

For each potentially relevant exception, follow the catch/fallback/retry behavior to the disputed output. An error that is handled without changing that decision can be a separate problem; its presence in the same trace is not proof it caused this symptom.

Inspect account/device targeting and explicit overrides alongside freshness when a report differs from broad recovery. Refreshing or reinstalling a client does not establish that server-side rules or overrides were removed; check whether the targeting identity or attributes changed. Preserve the failing state and available decision evidence [before resetting it](techniques.md#preserve-failing-state-before-resetting-it), then compare the effective identity, configuration, and result afterward. A cache explanation needs a supported layer, key, lifetime, and invalidation path that accounts for the observation; do not choose it solely because the output looks stale or a reset made it disappear.

## Trace what rollback actually reverses

Identify the precise branch and values restored by switch-off or rollback. It may resume ordinary rule evaluation rather than force a particular result. Check effective propagation where relevant, then inspect other reachable paths to the symptom: explicit overrides, fallback routing, retained state, or a separate mechanism. A remaining report alone does not prove that rollback failed.

Verify recovery for the affected population and workflow, separately from explaining the cause. Keep already-affected data or queued effects in scope where authorized; restored routing does not necessarily repair those effects. Record what was restored, what remains unexplained, and what recovery has actually been observed.

## Keep validation attached to the conditions it exercised

Record the code and configuration revisions, effective scope, population, executed branch, actual producer, and consumer assertion needed to interpret a check. Gate-off results do not establish gate-on behavior; a shadow path does not establish the serving result. Broader targeting or a newly affected consumer requires reassessing the corresponding evidence, without repeating unrelated checks.

For a relevant investigation, an inline decision record is sufficient; combine it with existing notes rather than maintaining a second report:

```text
Expected invariant and reachable input/request:
Code/configuration revisions and effective scope:
Assignment / actual serving implementation:
Decision value / origin / matched rule:
Downstream observable result:
Supporting and contradicting evidence, with original source:
Disposition: validated / unresolved / disproved
Validation: actual workflow / isolated test / static
```

Omit irrelevant fields for simple bugs and leave unavailable facts unknown. Do not add product logging merely to fill this record. Choose additional instrumentation only when it can answer a necessary unresolved question.

Distinguish original observations from summaries, reposts, and quoted assistant conclusions. Multiple copies of one conclusion remain one evidence lineage. If explaining change history, separate configuration ownership, recorded change actors, authors, reviewers, and mergers; those roles and empty approval text do not establish intent or review depth. Use [review and correction history](regression-history.md#use-reviews-as-investigative-leads) for source-backed hypotheses, not unsupported blame.
