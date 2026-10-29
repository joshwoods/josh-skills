# Josh’s Bug Playbook

Checklists and a decision flow for humans and LLMs to find, explain, and fix software bugs. Each checklist says what to do, what evidence to keep, and which step comes next.

## Start here

| Checklist | Use it when |
| --- | --- |
| [Diagnose and fix a bug](skills/diagnosing-bugs/references/checklist.md) | Something is broken, wrong, throwing, or slower than expected. |
| [Find bugs in a codebase or workflow](skills/finding-bugs/references/checklist.md) | You want to discover defects that have not been reported. |
| [Reproduce a frontend bug and locate the data mismatch](skills/diagnosing-bugs/references/frontend-boundary.md) | The UI is wrong and you need to distinguish request, backend-data, and client-handling problems. |
| [Trace a regression through versions and Git history](skills/diagnosing-bugs/references/regression-history.md) | Something used to work and you want to narrow when and how it changed, including with Git bisect. |

Start at the first unanswered question. Check boxes against actual evidence; mark inapplicable or blocked items explicitly. A small bug may need one experiment. A broader hunt needs a coverage record so finding one bug does not silently end the rest of the work.

## Work from quick checks to expensive investigations

Both checklists use this default order. Choose checks that can answer the current question; the list is not a quota to finish.

| Effort | Diagnosing a known failure | Finding unknown bugs |
| --- | --- | --- |
| Quick | Confirm basics, try the reported steps, inspect existing errors/data | Define scope, inspect relevant behavior, run available targeted checks |
| Focused | Trace the mismatch, inspect a relevant diff, test an explanation | Challenge candidates with concrete boundary or sequence checks |
| More involved | Add targeted probes or a faithful harness; compare code/context | Exercise integration, failure recovery, or stateful behavior where needed |
| Expensive | Reconstruct environments, run prolonged trials, rebuild historical versions or bisect | Run justified extended stress/property searches or version/configuration comparisons |

Stop escalating when the evidence supports the next decision. A requested fix still needs verification, and an exhaustive hunt still needs its remaining coverage even when that work is expensive. The history checklist starts with inexpensive version facts and diffs; bisect is a later branch.

## Decision flow

```mermaid
flowchart TD
    A{"Known failure?"}
    A -->|Yes| D["Define expected vs actual behavior"]
    A -->|No| S["Map scope; check the next scenario"]
    S -->|Candidate defect| D
    S -->|No candidate| M{"Other planned areas remain?"}
    D --> E["Reproduce or collect available evidence"]
    E --> H["Trace the path; test explanations"]
    H -->|Useful next experiment| E
    H -->|Cause supported| F{"Fix included in the task?"}
    H -->|Candidate disproved or evidence blocked| O["Record outcome and evidence limits"]
    F -->|No| O
    F -->|Yes| R["Repair; verify the original failure"]
    R -->|Failure or regression| E
    R -->|Checks pass: verified| O
    R -->|Unavailable or inconclusive: unverified| O
    O --> M
    M -->|Yes| N["Return to the next planned scenario"]
    N --> S
    M -->|No| Z["Report findings, changes, and coverage"]
```

The detailed checklists distinguish a failed check from a setup failure, a supported diagnosis from a hypothesis, and a verified repair from a workaround. During an incident, authorized mitigation can come first; preserve evidence and resume diagnosis afterward. When no useful next check is possible, record the blocker and continue independent work within scope.

## Use with a human or an LLM

Copy the relevant checklist into your issue or working notes. A short instruction is enough:

> Follow the linked checklist for this task. Record evidence beside completed steps and explain any blocked or inapplicable items. Continue through the requested scope, including repair and verification when asked.

The checklists are the method. The installable skills below are small adapters that load those same documents for a coding agent.

Each skill folder includes its checklist, supporting references, and agent metadata. Diagnosing Bugs also includes an optional human-assisted reproduction template.

## Install in Codex

On another machine, sign in to GitHub with an account that can access this repository (`gh auth login`), then clone it:

```sh
gh repo clone joshwoods/josh-skills
cd josh-skills
```

Copy both skill folders into your Codex skills directory. Back up any existing copies before replacing them.

```sh
skill_destination="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$skill_destination"
cp -R skills/diagnosing-bugs skills/finding-bugs "$skill_destination/"
```

In a new session, invoke `$diagnosing-bugs` for a known failure or `$finding-bugs` for a proactive review. For example:

- “Use $diagnosing-bugs to investigate and fix this crash: …”
- “Use $finding-bugs to review the import workflow for correctness defects.”

## Use with other agents

Copy the complete folders into the agent’s supported skill location, or provide the relevant `SKILL.md` and its linked references as task context. Keep both folders as siblings so their cross-references continue to work. Adapt installation to the receiving tool; the methods do not require a particular model.

## Sources and validation

Research sources and limitations are recorded in [diagnosis sources](skills/diagnosing-bugs/references/sources.md) and [discovery provenance](skills/finding-bugs/references/provenance.md).

The instructions were revised using OpenAI’s [GPT-6 Astra skill guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra). Format checks and editorial review do not establish improved debugging performance; effectiveness requires evaluation on representative tasks.
