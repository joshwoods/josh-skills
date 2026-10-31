# Choosing an investigation technique

Read the relevant section when the investigation needs a more specific approach. Choose techniques because they distinguish current explanations, not to complete a tool checklist.

## Preserve failing state before resetting it

A currently failing instance may be the only reproduction available. Before recommending or performing refresh, restart, reinstall, sign-out, cache clearing, data reset, or a retry that may overwrite the failing state or evidence, preserve as much relevant evidence as is safely available:

- Record the visible or consumer-observed failure, exact action order and inputs, timestamps, request/trace IDs, and matching responses or errors. Save existing logs before they rotate or disappear.
- Record build/environment, effective configuration and overrides, account/session/device or installation identity, and relevant persisted, cached, or in-process state. Prefer supported exports or snapshots when feasible; capture evidence without exposing credentials or unrelated personal data.
- Keep the failing instance intact when safe and practical. Use a copy, snapshot, or separate fresh instance to test a clean start instead of destroying the only failing state. Note any properties the copy cannot preserve, such as timing or live connections.
- Record the reset performed and compare the result, identity, configuration, and state before and after. A reset can erase the trigger or change targeting inputs; disappearance of the symptom alone neither establishes a cache cause nor verifies a repair.

Keep capture proportional to the risk of losing the reproduction; do not require an exhaustive dump or new logging infrastructure. During urgent authorized mitigation, collect what is practical without delaying necessary recovery, then state what changed and what evidence could not be retained. If state was already reset, use remaining evidence and disclose the lost reproduction rather than claiming it never occurred.

## Intermittent, timing and concurrency failures

Record the original failure signature, input/state and failures per number of trials. Preserve failing seeds, timestamps or schedules when available. Replay recorded events, coordinate execution at suspected boundaries, or introduce load to increase useful observations. Confirm that instrumentation or stress has not replaced the original failure with a different one.

Use logs, traces and dumps even when a fast reproduction is unavailable. An observed ordering violation can be useful without a high reproduction rate. Record which causal links remain inferred. Zero failures in a finite run is limited evidence; report trial count and comparability to the failing condition instead of claiming certainty. Removing instrumentation can restore timing, so recheck the final condition where practical.

## Performance regressions

Define the symptom quantitatively: operation, input/workload, baseline, metric and relevant environment. Measure comparable runs, accounting for warm-up, caches and variability. Profile or inspect query plans to locate where time/resources go; use that observation to select an experiment. A faster reduced benchmark must be checked against the original workload, and speed must preserve correct results.

## Regressions with history

Use the [regression history checklist](regression-history.md) when a last-known-good version or release window can narrow the investigation. It covers establishing endpoints, mapping app/deployment versions to commits, comparing code and context, reviewing history, manual or automated bisect, and confirming the resulting boundary. Use it alongside current-path diagnosis; a first bad commit does not by itself explain the mechanism or verify a repair.

## Large inputs or change sets

Reduce one part and classify the result using the same failure signature. Treat invalid inputs, setup errors, or different exceptions as unresolved rather than preserved failures. Syntax-aware reduction or component-level removal may be more useful than arbitrary text deletion. Stop when further reduction costs more than the diagnostic value it offers. A case where no single deletion preserves failure need not be the globally smallest case.

## UI, lifecycle and multi-component failures

Drive the relevant runtime and record observable output/state and errors at meaningful boundaries. Preserve the ordering of navigation, background work, cancellation, persistence and restart where those are part of the trigger. A passing isolated function call cannot establish that the real interaction works. If only static inspection or a partial runtime is available, state that limit.

## Unknown triggering input

Where the intended behavior admits meaningful properties, use a reference implementation, roundtrip, idempotence or state invariant to search for counterexamples. Verify the property is required and the generator reaches relevant valid inputs. For stateful failures, generate sequences of actions and retain the failing sequence. A bounded search with no counterexample does not establish absence of bugs.

## Active incidents

Assess ongoing harm and fragile evidence immediately. Capture what is practical, perform authorized mitigation without waiting for a fresh reproduction or complete diagnosis, and verify recovery in the affected workflow and population. Record remaining damaged state or queued effects that need recovery. A rollback or workaround can restore service without establishing the causal explanation or repairing prior damage. Track mitigation and diagnosis separately, and continue the investigation within the requested scope.

For configuration-driven symptoms, use the [configuration and rollout guide](configuration-and-rollouts.md) to separate reports, identify decision origins and the actual producer, and trace exactly what rollback restores. Use available correlation evidence early; do not merge causes solely because reports look alike or share a trace.

## Human-assisted reproduction

When an indispensable interaction is unavailable to the agent, ask for the specific observation needed and continue independent investigation. The optional [interaction template](../scripts/hitl-loop.template.sh) can collect observations if the user has access to the interactive terminal running it. Adapt its example steps before use; its printed responses are observations to interpret, not an automated pass/fail verdict or a structured data protocol.
