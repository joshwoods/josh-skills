# Josh’s Skills

Reusable debugging and correctness-review skills for coding agents.

| Skill | Use it for |
| --- | --- |
| [Diagnosing Bugs](skills/diagnosing-bugs/SKILL.md) | Investigating a reported failure or performance regression, and completing requested repairs. |
| [Finding Bugs](skills/finding-bugs/SKILL.md) | Proactive bug hunts and correctness reviews with explicit coverage and validated findings. |

Both folders include their supporting references and agent metadata. Diagnosing Bugs also includes an optional human-assisted reproduction template.

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
