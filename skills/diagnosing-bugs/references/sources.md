# Method sources and limits

This workflow adapts established debugging methods into instructions for an agent. The summaries are original paraphrases; linked articles and skill packages are not bundled. Source fit does not establish that these instructions improve an LLM's behavior.

| Source | Contribution | Limit |
|---|---|---|
| John Regehr, [How to Debug](https://blog.regehr.org/archives/199), 2010-07-04 | Establish correct behavior; isolate failures; choose informative experiments; verify, clean up and check related defects. | Expert teaching/practice, not a controlled evaluation of LLM skills. |
| Chris Jones, Google SRE, [Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/), 2016 | Domain knowledge, discriminating experiments, notes, operational mitigation and uncertain causal evidence. | Operational systems may resist safe deterministic reproduction; the method needs judgment. |
| MIT 6.031, [Debugging](https://web.mit.edu/6.031/www/fa21/classes/13-debugging/), 2021 | Reproduction, hypothesis testing, smaller inputs, then confirmation against the original input. | Teaching material; examples are simpler than many production systems. |
| Andreas Zeller, [Introduction to Debugging](https://www.debuggingbook.org/html/Intro_Debugging.html) and [Reducing Failure-Inducing Inputs](https://www.debuggingbook.org/html/DeltaDebugger.html), living executable textbook | Causal explanations, failure-preserving reduction, separate valid verdicts from unresolved experiments. | Reduced inputs can be locally minimal without being globally smallest; examples do not establish agent efficacy. |
| Julia Evans, [A debugging manifesto](https://jvns.ca/blog/2022/12/08/a-debugging-manifesto/), 2022-12-08 | Runtime observation, assumption checks, tools and fresh perspective. | Practitioner habits complement a procedure rather than replace it. |
| Hypothesis authors, [Stateful tests](https://hypothesis.readthedocs.io/en/latest/stateful.html), living documentation | Generate operation sequences against meaningful invariants or a reference model. | Properties and models must be valid; finite passing searches offer bounded evidence. |
| [Superpowers systematic-debugging](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md), public skill inspected 2026-10-22 | Practical agent-oriented reference for phased investigation, boundary tracing and verification. | Instruction content and small behavioral scenarios are not controlled proof of broad improvement. |

The earlier local skill supplied the reproduction/checking emphasis. The 2026-10-22 revision replaced fixed hypothesis counts and reproduction prerequisites with evidence-sensitive decisions, added an investigation record, and distinguished diagnosis, mitigation and verified repair.

## Prompt migration guidance

The 2026-10-23 revision used OpenAI's [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), published 2026-09-11, and the [current prompting guidance](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices), read 2026-10-23. It shortened discovery text, made the checklist adaptive, moved conditional techniques out of the main path, and clarified authorized completion and proportionate verification. The debugging evidence requirements remain. This is an instruction migration, not evidence of a performance gain; the skill does not select a model or require Astra.

## Evaluating changes to this skill

The 2026-10-28 revision made [the human-and-agent checklist](checklist.md) the canonical working procedure. The skill entrypoint now loads that procedure, so both audiences use the same decision points and evidence requirements. This changes presentation and routing; it does not establish a debugging performance improvement.

Target the actual failure mode: speculative edits, repeated low-information probes, wrong nearby repairs, or premature completion. Improvement means correct causal diagnoses and repairs with preserved behavior, fewer unnecessary changes, and reasonable time/cost.

Use ordinary historical bug requests where available. Freeze tasks, starting states and held-out checks before inspecting outcomes; keep the solution out of participant context. Record exact model/settings when exposed, instruction files, visible skills and actual reads, tools, hooks, permissions, environment and initial changes. The baseline includes existing guidance and must not be described as instruction-free.

Use fresh sessions and matched conditions; repeat trials when drawing a comparison. Inspect executed behavior, diffs, original and neighboring checks, unnecessary changes, and any weakened tests or protections. Preserve infrastructure failures and unsuccessful runs. Skill-format validation and small isolated examples are capability checks; neither proves reduced debugging time or general effectiveness. Near-ceiling outcomes call for harder representative tasks, not an uplift claim.

For evaluation design background: Anthropic, [Demystifying evals for AI agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents), 2026-01-09. This is engineering guidance rather than validation of this particular skill.
