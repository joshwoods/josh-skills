# Choosing an investigation technique

Read the relevant section when the investigation needs a more specific approach. Choose techniques because they distinguish current explanations, not to complete a tool checklist.

## Intermittent, timing and concurrency failures

Record the original failure signature, input/state and failures per number of trials. Preserve failing seeds, timestamps or schedules when available. Replay recorded events, coordinate execution at suspected boundaries, or introduce load to increase useful observations. Confirm that instrumentation or stress has not replaced the original failure with a different one.

Use logs, traces and dumps even when a fast reproduction is unavailable. An observed ordering violation can be useful without a high reproduction rate. Record which causal links remain inferred. Zero failures in a finite run is limited evidence; report trial count and comparability to the failing condition instead of claiming certainty. Removing instrumentation can restore timing, so recheck the final condition where practical.

## Performance regressions

Define the symptom quantitatively: operation, input/workload, baseline, metric and relevant environment. Measure comparable runs, accounting for warm-up, caches and variability. Profile or inspect query plans to locate where time/resources go; use that observation to select an experiment. A faster reduced benchmark must be checked against the original workload, and speed must preserve correct results.

## Regressions with history

With known good and bad states and a reliable classifier, consider `git bisect` or differential execution. Separate build/environment failures from the target behavior. For `git bisect run`, exit 0 is good, an appropriate nonzero exit is bad, and 125 skips an untestable revision; inspect the command's own exit behavior before automating it. Preserve the user's checkout and changes by using an appropriate isolated checkout when needed.

Confirm the candidate boundary in comparable conditions. A first bad commit narrows where to investigate; it is not by itself a causal explanation. Skipped revisions, dependencies and unrelated failures can leave an ambiguous result. Official reference: <https://git-scm.com/docs/git-bisect>.

## Large inputs or change sets

Reduce one part and classify the result using the same failure signature. Treat invalid inputs, setup errors, or different exceptions as unresolved rather than preserved failures. Syntax-aware reduction or component-level removal may be more useful than arbitrary text deletion. Stop when further reduction costs more than the diagnostic value it offers. A case where no single deletion preserves failure need not be the globally smallest case.

## UI, lifecycle and multi-component failures

Drive the relevant runtime and record observable output/state and errors at meaningful boundaries. Preserve the ordering of navigation, background work, cancellation, persistence and restart where those are part of the trigger. A passing isolated function call cannot establish that the real interaction works. If only static inspection or a partial runtime is available, state that limit.

## Unknown triggering input

Where the intended behavior admits meaningful properties, use a reference implementation, roundtrip, idempotence or state invariant to search for counterexamples. Verify the property is required and the generator reaches relevant valid inputs. For stateful failures, generate sequences of actions and retain the failing sequence. A bounded search with no counterexample does not establish absence of bugs.

## Active incidents

Prioritize authorized mitigation while preserving useful evidence. A rollback or workaround can restore service without establishing the causal explanation. Track mitigation and diagnosis separately, and continue the investigation within the requested scope.

## Human-assisted reproduction

When an indispensable interaction is unavailable to the agent, ask for the specific observation needed and continue independent investigation. The optional [interaction template](../scripts/hitl-loop.template.sh) can collect observations if the user has access to the interactive terminal running it. Adapt its example steps before use; its printed responses are observations to interpret, not an automated pass/fail verdict or a structured data protocol.
