# Evidence for bug investigations

Use the relevant section when preserving a failure, choosing a reproduction, or interpreting a check. Keep the parent workflow's scope, authorization, and completion conditions; this reference does not start a separate investigation or require a new report.

## Preserve failing state before resetting it

A currently failing instance may be the only reproduction available. Before recommending or performing refresh, restart, reinstall, sign-out, cache clearing, data reset, or a retry that may overwrite evidence:

- Capture the visible or consumer-observed failure, action order and inputs, timestamps, request/trace IDs, and matching responses or errors. Save available logs before they rotate or disappear.
- Record the build/environment, effective configuration and overrides, relevant account/session/device or installation identity, and persisted, cached, or in-process state. Prefer supported exports or snapshots; omit credentials and unrelated personal data.
- Keep the failing instance intact when safe and practical. Compare with a copy, snapshot, or separate fresh instance. Record properties the copy cannot preserve, such as timing or live connections.
- Record the reset and compare the result, identity, configuration, and state before and after. A reset can erase a trigger or change targeting inputs. A disappearing symptom alone neither establishes a cache cause nor verifies a repair.

Keep capture proportional to the risk of losing the reproduction; do not require an exhaustive dump or new logging infrastructure. During urgent authorized mitigation, capture what is practical without delaying recovery and record what evidence was lost. If state was already reset, use remaining evidence and disclose the lost reproduction rather than claiming the failure never occurred. Verify recovery separately from explaining the cause, including affected data or queued effects where authorized.

## Reproduce faithfully

Prefer the affected UI, CLI, or API workflow in a representative environment, manually or through automation. Preserve the relevant version, configuration, reachable inputs, state, action order, timing, lifecycle, and callers. Use isolated state for mutations within the task's authorization.

If actual use is unavailable or a reasonable attempt does not reproduce the failure, reuse a cheap existing check or small adaptation against the real implementation. Inspect available logs, matching exchanges, source, and focused history before investing in a new test or harness. Do not repeat uninformative attempts or require prolonged environment setup before useful static investigation.

A fallback or reduced case must preserve the supported contract and target failure signature. Copied logic, impossible state, an unrelated exception, or a defect in a mock does not reproduce the claimed bug. A substituted response or schedule must be supported by the real dependency. Keep the original scenario and reduce only while preserving what it demonstrates.

## Separate result, evidence, and conclusion

For each attempt, record the command or steps, conditions, observer/source, assertion, and observed result. Retain unsuccessful attempts even if a later fallback succeeds. Reuse applicable evidence instead of repeating work solely to satisfy a sequence.

| Dimension | Meaning |
| --- | --- |
| **PASS / FAIL / UNRESOLVED** | Relevant behavior exercised correctly / target violation observed / setup or observation prevented a verdict. Another exception is not confirmation. |
| **Actual use / test only / not yet reproduced** | Reproduction through the representative application workflow / only an isolated test or substituted boundary / no reproduction established. Automation can establish actual use when it drives and observes that workflow. |
| **Validated / unresolved / disproved** | Disposition of a candidate after checking its causal argument; independent of any single attempt's result. |

Discovery coverage separately records **actual workflow observed**, **test-only coverage**, **source examined**, or **not exercised**. Launching a product or driving steps without inspecting the relevant outcome does not establish workflow coverage.

A complete static argument can validate a deterministic defect without reproducing it; identify the method and unverified premises. Runtime, integration, timing, or visual claims need corresponding observations. Severity follows reachable impact; confidence follows evidence strength. Keep unresolved candidates distinct from established findings and avoid invented numerical confidence.

## Bind evidence to its conditions

Record the relevant code/configuration revisions, effective scope and population, branch actually exercised, and consumer assertion. Assert the consumer's result and relevant reads/effects; skipped-work counters or a returned fallback alone do not establish preserved behavior. An assigned cohort, disabled branch, or shadow run does not prove the enabled serving path. Leave an unknown producer unknown.

Reassess affected consumers and checks when code, configuration, dependencies, or scope change, including after approval. Earlier evidence covers its original conditions; retain unaffected checks and rerun those whose premises changed. Verify final conditions without temporary instrumentation wherever removal can change behavior. Report intermittent trial counts or comparable performance measurements and their limits.

A passing isolated test does not establish end-to-end repair, and fresh state does not establish recovery of existing affected state. Keep actual-use gaps and outstanding recovery explicit. Preserve original evidence and attribution: summaries, reposts, or quoted conclusions are not independent corroboration.
