# Source rationale and limits

Sources inspected on 2026-10-22. These references inform the method; they are not evidence that this skill improves LLM performance. The instructions are original synthesis rather than copied skill text.

| Source | Role in the skill | Limits |
|---|---|---|
| John Regehr, [How to Debug](https://blog.regehr.org/archives/199), 2010 | Establish correct behavior; isolate a faithful failure case; use experiments to connect symptoms to causes. | Expert instruction about debugging known failures, rather than comparative evidence for proactive LLM bug discovery. |
| Chris Jones, Google SRE, [Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/), 2016 | Use system knowledge, inspect evidence, test explanations, and record investigation results. | Operational troubleshooting emphasizes known incidents. Production constraints can prevent direct reproduction. |
| Hypothesis, [Stateful tests](https://hypothesis.readthedocs.io/en/latest/stateful.html), current documentation | An optional way to explore action sequences against explicit behavioral checks or a simple model. | Depends on a meaningful oracle and faithful actions. Generated examples do not establish universal correctness. |
| Sentry, [find-bugs skill](https://github.com/getsentry/skills/blob/main/skills/find-bugs/SKILL.md), inspected reference | Comparison for explicit review scope and checking candidates in surrounding context. | Primarily branch review with a web/security checklist; not adopted wholesale. |
| Trail of Bits, [variant-analysis skill](https://github.com/trailofbits/skills/blob/main/plugins/variant-analysis/skills/variant-analysis/SKILL.md), inspected reference | Comparison for searching related occurrences after a causal mechanism is known. | Starts from an existing bug and is distinct from initial discovery. No dependency on its plugin is introduced. |

The coverage dimensions, scope controls, evidence dispositions, and report shape are design choices for this user's failure mode: unstructured investigations that waste effort or leave claims unverified. They should be revised based on observed task outcomes rather than accumulating more checklist items by default.

The 2026-10-23 instruction revision used OpenAI's [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), published 2026-09-11, and the [current prompting guidance](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices), read 2026-10-23. The main skill keeps coverage and finding requirements while leaving probe selection adaptive, loading detailed guidance conditionally, and making completion of authorized fix loops explicit. It does not select a model or establish improved bug-finding performance.

To evaluate effectiveness, inspect real investigations: correctness and validity of findings, missed defects, repeated or uninformative probes, unnecessary edits, preserved protections, time/effort, and honest completion of the requested scope. Keep capability checks separate from claims about broad effectiveness.

The 2026-10-28 revision made [the human-and-agent checklist](checklist.md) the canonical working procedure. The skill entrypoint loads the same checklist, preserving the coverage and finding requirements while exposing concrete actions, evidence, and next decisions to both audiences.
