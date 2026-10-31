# Choosing useful coverage

Read this when a hunt spans several workflows, boundaries, or stateful operations. A coverage map tracks what was examined; it is not a proof that all defects have been found.

## Derive checks from contracts

For each public operation or user workflow, identify what enters, which state it reads or changes, what it returns or exposes, and the assumptions made by downstream consumers. Use those relationships to choose checks. When intent is ambiguous, seek an authoritative contract or state the uncertainty.

For change reviews, connect modified behavior to callers and observable consequences. For product workflows, map actual actions and transitions, including prerequisites. A list of files alone does not describe workflow coverage.

Use representative workflows to discover defects even when source inspection raises no suspicion. Choose checks that expose the changed outcome and the surrounding contract: inspect affected UI sections and their continued usability, save and reopen a document, or run a CLI/API through its consumer. Observe what users or consumers receive, rather than treating plausible implementation or passing lower-level tests as equivalent evidence. Keep checks proportional to the requested scope and available environment; if a workflow is not exercised, record that coverage gap. This is discovery through use; validating a particular suspected bug is a separate step.

## Select relevant dimensions

These prompts are a menu. Include the dimensions that the implementation and task make plausible; explain significant omissions rather than marking unrelated categories as tested.

| Dimension | Useful questions | Evidence to seek |
|---|---|---|
| Inputs and boundaries | Do supported empty, minimal, maximum, duplicate, malformed, or unusual values expose different behavior? | Actual results at the meaningful boundary; a documented rejection where appropriate. |
| Decisions and ownership | Are preconditions enforced at the responsible layer? Can callers supply a state the callee assumes impossible? | Caller-to-callee trace with concrete reachable inputs. |
| State and sequences | What happens after retry, repeat, undo, back, reset, or a different order of valid actions? | Relevant action sequence and final state, not only individual method results. |
| Failures and recovery | What happens when an operation fails partway through? Can the user retry? | Propagated error, retained state, and subsequent successful or failed operation. |
| Cancellation and lifetime | What work survives cancellation or view/process disposal? Can a late result overwrite newer state? | Ownership and completion order, with observed state where feasible. |
| Persistence and interchange | Does save/load preserve the required meaning? Can previous or external data be read as promised? Does an upgrade or repair work with existing affected state? | Round trip, compatibility, or recovery check invoking the real storage boundary; distinguish fresh fixtures from preexisting data. |
| Concurrency and ordering | Can independently valid operations conflict, duplicate effects, or commit stale results? | Reachable interleaving and invariant violated at the relevant observation point. |
| Environment and dependencies | Which configurations, versions, permissions, or external outcomes affect the contract? | Observed or supported configuration plus dependency behavior. |

Do not invent requirements such as idempotence, order independence, or lossless round trips. Apply a property only where the contract warrants it. A failed request might still have committed a remote effect; a canceled local task does not establish that the remote operation was canceled.

## Replacements, eligibility, and actual consumers

Use this section when a change substitutes a result, returns a default, skips evaluation, or gates a shared set of operations. Start with the affected path and cheap available evidence; expand only as required to establish its effective scope.

- Trace the decision through each reachable downstream consumer to its output, further reads, and side effects. A control value, `false`, an empty value, `null`, and "not evaluated" are not inherently equivalent or safe. Determine what each consumer does with the actual state: it may perform another read, choose a different path, retain old state, or emit an effect. Judge the contract at that observation point.
- For a registry, base class, or bulk rule, enumerate the actual affected implementations and inherited/indirect callers within scope. Check dispatch and framework dependency construction, including work that occurs before the gated method runs. Skipping evaluation need not prevent dependency creation or its effects. Names, annotations, registry labels, and other metadata guide the search; confirm the reachable call/dependency paths rather than treating metadata as a complete caller inventory.
- Separate eligibility or cohort assignment from the path producing the response. Check routing overrides, fallback, and shadow execution where applicable. Record which result the consumer actually receives; a shadow result or an assigned-but-disabled branch does not establish behavior on the enabled response-producing path.

Derive decision cases from the intended contract, not from the implementation's current branches. Include eligible and ineligible cases, unknown/missing inputs, and unaffected cases where those states are supported. Do not silently equate unknown with false or ineligible. Keep a compact decision record in existing notes when several branches matter:

`case + contract → eligibility → actual route → evaluated/replaced/skipped result → consumer outcome + relevant reads/effects → evidence or unknown`

This is a local reasoning aid, not a required universal form or production logging feature. Start with representative cases that distinguish the possibilities, then cover the remaining requested cases. Keep unknown fields unknown until evidence resolves them.

Include a negative control where useful: an intentionally supported fallback can be correct even though it differs from the preferred path. Do not report fallback, a false value, or suppressed work as a defect without a reachable contract violation. Conversely, showing that evaluation was suppressed does not establish that downstream behavior remained correct.

## Choose an oracle and a method

An oracle is the rule used to judge a result. It may come from an explicit example, API contract, established invariant, simple reference model, or relationship between operations. If the oracle merely repeats the implementation's formula, it may reproduce its mistake.

- Use examples when the failure space is narrow and the expected output is clear.
- Use properties for varied inputs when a stable rule is known.
- Use stateful checks when defects depend on action sequences. Model only the behavior needed to judge the real implementation; record generated counterexamples and relevant seeds/settings.
- Use the runtime for interaction, integration, lifecycle, and presentation claims. A reduced harness can isolate a mechanism without demonstrating the whole product workflow.

Hypothesis describes generating sequences of actions and comparing implementations with a model. This is an optional technique, not a requirement to adopt Python or a new test framework. See its [stateful testing documentation](https://hypothesis.readthedocs.io/en/latest/stateful.html).

## Frontend and backend data boundaries

For a UI backed by an API, include both the user's action and the data reaching the view. Preserve the relevant route/session/cache state and match the response to the failing request. Compare `intended action → outgoing request → raw response → decoding/mapping → cache/state → view output`.

Check shape and meaning: a schema-valid response can contain the wrong record, stale values, wrong units, or incomplete results. A server may correctly answer a request the client constructed incorrectly. Contract-valid empty, null, or optional fields are different from a response violating the contract; derive client fallback/error expectations from the supported behavior.

Use captured responses and faithful isolated replay to test assumptions. Keep starting state and ordering comparable. A fabricated malformed fixture shows how the client reacts, not that production emits it. Record an upstream contract violation separately from a client failure to handle it as required; avoid forcing a single frontend/backend owner when both are defective. If only mock/replay checks ran, state the missing integration evidence.

## Record coverage honestly

Distinguish source examined, test executed, runtime exercised, and blocked. Record the scenarios and observation points actually covered. A test file's existence is not execution evidence; a green suite is not evidence that every relevant transition was asserted.

Prioritize by likely impact, changed behavior, historical failure areas, and uncovered assumptions. In an exhaustive request, prioritization changes order rather than removing planned areas. If the scope cannot be completed, report precisely what remains and why.
