# Regression history: when did it stop working?

Use this when behavior previously worked or reports cluster around a release. Compare the failing and working states while tracing the current failure. History narrows the explanation; a suspicious commit message does not establish a cause.

**Effort order:** First try the ordinary reproduction and quick evidence checks. Collect version facts cheaply, then inspect a focused history summary or diff. Rebuilding old versions and bisecting come later when cheaper checks have not answered the question and the expected information justifies the setup. Skip unnecessary history work once you have enough evidence to repair and verify, unless the requested outcome also includes the introduction boundary or affected releases; complete those questions too.

## 1. Establish the interval

- [ ] Record the last **observed working** and first **observed failing** versions, with the same scenario and evidence for each. Treat “it worked last month” as a lead until verified. A release with no reports is not automatically good.
- [ ] Map app version/build, release tag, deployed artifact, and source SHA using build or deployment records. Record client and server versions separately when independently deployed. Check rollout cohort and cached assets where relevant; a tag or commit timestamp alone does not prove what the user ran.
- [ ] Record what else changed: flags/configuration, dependency lockfiles, toolchain/runtime, infrastructure, API/schema, migrations, and data. Separate **introduced in code**, **activated/deployed**, and **first detected**. A new input can expose an older latent bug.

| Observation | Version / artifact / SHA | Relevant context | Scenario and evidence |
| --- | --- | --- | --- |
| Last observed good | | | |
| First observed bad | | | |

**Next:** If no good version is known, first check existing release, CI, telemetry, or archived evidence for a supported endpoint. Defer execution or rebuilding of older versions until escalation is warranted. Continue ordinary diagnosis if no endpoint is available; do not invent a good endpoint for bisect.

## 2. Compare what changed

- [ ] Inspect changes between the verified endpoints, including callers, dependencies, configuration, and migrations. Start with an interval-wide summary, then focus on evidence-relevant patches; filtering immediately to the visibly failing component can hide the actual cause.
- [ ] Read relevant patches and issue/PR rationale, and compare their predictions with the observed failure. Trace changed fields or logic backward when helpful. A last-edited line identifies history to inspect, not a guilty author or sufficient causal evidence.

Replace the example refs and paths below. These commands inspect history without changing the checkout:

```sh
regression_good='VERIFIED_GOOD_SHA'
regression_bad='VERIFIED_BAD_SHA'
git log --oneline --decorate "${regression_good}..${regression_bad}"
git diff --stat "$regression_good" "$regression_bad"
git diff "$regression_good" "$regression_bad" -- path/to/relevant/code
git log -p "${regression_good}..${regression_bad}" -- path/to/relevant/code
```

For focused searches, `git log -S 'fieldName' "${regression_good}..${regression_bad}"` finds changes to its occurrence count; `git log -G 'pattern' "${regression_good}..${regression_bad}"` searches matching added/removed lines. `git log --follow -p "$regression_bad" -- path/to/file` follows one file backward from the failing ref across renames. Keep these searches subordinate to the observed path. See [git-log](https://git-scm.com/docs/git-log).

## 3. Separate code from context

- [ ] Rerun the same failure check on the proposed good and bad endpoints in comparable conditions. An old build failing against today's incompatible API or migrated database is not proof it was always broken. A checkout change must actually rebuild/relaunch the tested artifact, not leave a newer process or cached bundle running.
- [ ] Where feasible, compare old/new code with old/current context using isolated, compatible fixtures. Record only combinations actually tested:

| | Earlier context | Current context |
| --- | --- | --- |
| Earlier code | Result + evidence | Result + evidence |
| Current code | Result + evidence | Result + evidence |

Hold relevant inputs, state, and check semantics constant. Reproduce each revision's recorded dependency/toolchain requirements when they are part of the change; record that difference rather than quietly substituting today's dependencies. Do not run old migration code against live data to fill the matrix.

**Next:** A code-dependent result supports source-history investigation; a context-dependent result points toward data, flags, infrastructure, or dependencies. A combination may reveal an interaction. These are leads to test, not automatic diagnoses. Unavailable combinations remain unknown.

## 4. Narrow a large interval with bisect

- [ ] Escalate to bisect when the reproduction is classified reliably and quick error, boundary, and focused history checks have not localized the regression. Estimate build/run time and the availability of old artifacts; an expensive search needs a useful question to answer.
- [ ] Use a stable check that exercises the target failure on both endpoints. Qualify its PASS / FAIL / UNRESOLVED decisions before automating; a setup error must not masquerade as this regression.
- [ ] Work in a separate checkout to preserve ongoing edits. Use the environment's managed-worktree support when available, or a detached worktree in an unused location. Git supports [multiple worktrees](https://git-scm.com/docs/git-worktree) sharing the repository while retaining separate checkout state.

Example setup, using verified refs from above and a new path:

```sh
git worktree add --detach ../regression-investigation "$regression_bad"
cd ../regression-investigation
git bisect start "$regression_bad" "$regression_good" --
```

At each selected revision, build/run the same check, record the SHA and evidence, then issue **one** verdict:

| Observation | Command |
| --- | --- |
| Target behavior exercised correctly | `git bisect good` |
| Same target failure observed | `git bisect bad` |
| Revision cannot be classified | `git bisect skip` |

For automation, supply a task-specific classifier outside the bisected tree: `git bisect run /absolute/path/to/classifier`. Use 0 for pass, 1 for target failure, 125 for an untestable revision, and a fatal status such as 128 to stop on a broken harness. Git also interprets 126/127 as bad, so a missing command must not leak through as a regression verdict. Save `git bisect log` outside the checkout, then use `git bisect reset` to exit. These semantics are documented in [git-bisect](https://git-scm.com/docs/git-bisect).

**Limits:** Skips can leave several candidates. Flaky checks need comparable trials or controlled ordering before labeling revisions. If a bug was fixed and reintroduced, choose the relevant interval; do not claim the first occurrence ever. Start without a path restriction unless evidence supports it. A first-parent search can locate the integration merge rather than the originating branch change; state which question you tested.

## 5. Confirm and explain the boundary

- [ ] Recheck the candidate bad revision and the relevant preceding good revision under the recorded conditions. For merges, distinguish the tested integration parent from branch history. If you cannot test the neighbor, report the remaining candidate range rather than an exact introduction.
- [ ] Inspect the boundary diff and connect it to the trigger, changed behavior, and observed failure. A focused local revert or reapplication can strengthen the account when safe and meaningful; dependencies or interaction effects can make a revert inconclusive.
- [ ] Map the supported boundary back to released/deployed artifacts. Report the first affected release only when release/deployment evidence supports it; a source commit or first error timestamp alone cannot establish that mapping.
- [ ] Preserve endpoint evidence, verdict log, skipped revisions, candidate SHA/range, environment limits, and causal explanation. Exit bisect, retain useful evidence outside its checkout, and clean up the disposable checkout without discarding user work.

Return to the [main checklist](checklist.md) to repair and verify the original workflow. Finding the introducing change is localization, not completion of the repair.
