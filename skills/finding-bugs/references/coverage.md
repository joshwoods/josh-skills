# Choosing useful coverage

Read this when a hunt spans several workflows, boundaries, or stateful operations. A coverage map tracks what was examined; it is not a proof that all defects have been found.

## Derive checks from contracts

For each public operation or user workflow, identify what enters, which state it reads or changes, what it returns or exposes, and the assumptions made by downstream consumers. Use those relationships to choose checks. When intent is ambiguous, seek an authoritative contract or state the uncertainty.

For change reviews, connect modified behavior to callers and observable consequences. For product workflows, map actual actions and transitions, including prerequisites. A list of files alone does not describe workflow coverage.

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
