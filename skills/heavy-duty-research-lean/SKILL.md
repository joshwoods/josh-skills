---
name: heavy-duty-research-lean
description: Use when the user asks for deep, evidence-backed research with source-quality checks, uncertainty, counterarguments, and recommendations. Best for due diligence, market, technical, policy, legal, regulatory, product, or literature briefs. Avoid for quick lookups, simple summaries, and ordinary link finding.
---

# Heavy-Duty Research Lean

Turn a broad question into a rigorous, source-backed brief without loading unnecessary methodology text.

## Activation Boundary

Use this skill only when the request needs at least two of:

- A decision or recommendation that depends on evidence quality.
- Multiple source types, competing interpretations, or uncertainty.
- Primary-source verification, citations, or direct source attribution.
- A learning trail, glossary, or educational reading path.
- High-stakes current information such as law, regulation, pricing, benchmarks, product capabilities, companies, or public figures.

For simple summaries, quick facts, brainstorming, or one-source questions, answer normally and do not expand into this workflow.

## Mode Selection

Choose the lightest mode that satisfies the user:

- **Fast scan**: 5-10 sources, concise caveats, no long evidence table unless useful.
- **Standard brief**: 10-25 sources, findings table, evidence review, counterarguments, unknowns.
- **Deep dossier**: 25+ sources, chronology or data review, expert landscape, confidence grading, validation plan.

Default to Standard brief only when the user asks for "heavy duty," due diligence, a serious recommendation, or a learning-oriented research brief. Ask only when scope is ambiguous and the wrong mode would waste substantial time or tokens.

## Source Rules

- Prefer primary sources: official docs, filings, standards, source code, papers, datasets, transcripts, court or regulatory records, and first-party announcements.
- Use secondary sources for leads, context, and dissenting views; verify important claims against primary material where feasible.
- For current facts, browse or otherwise verify recency. Do not rely on memory for laws, prices, rankings, APIs, product specs, companies, public figures, or standards.
- If browsing is unavailable or out of scope, do not invent current facts. Produce a research plan and identify the sources needed.
- Separate facts, source claims, analysis, and speculation. Label weak or tentative claims.
- For controversial or high-stakes claims, seek two independent confirmations or explain why only one source is available.

## Reference Loading

Do not load methodology references by default. Read `references/research-method-checklists.md` only when one of these is true:

- The user asks how to research, evaluate sources, grade evidence, or learn a domain.
- The task involves academic literature discovery, systematic review, or explicit confidence grading.
- You need a compact checklist for source credibility, synthesis, or educational-reference selection.

Treat the reference as scaffolding, not topical evidence. Topic-specific evidence must come from sources for the user's actual question.

## Workflow

1. **Frame the question**: state objective, intended decision/output, scope, time horizon, geography/jurisdiction, depth, and constraints.
2. **Map sources**: identify primary sources, authoritative secondary sources, data/benchmarks, dissenting sources, and educational references.
3. **Collect evidence**: capture title, author/institution, date, URL/path, source type, key claim, credibility reason, and limitation for important sources.
4. **Evaluate quality**: classify each important source as High, Medium, or Low confidence.
5. **Synthesize**: answer the question directly, then explain tradeoffs, implications, counterarguments, and unknowns.
6. **Teach only when useful**: include educational references when the user asked to learn, when the domain is unfamiliar, or when the research decision depends on understanding the field.

## Output Shape

Use this structure for Standard and Deep work. For Fast scans, keep the same order but compress sections that would be empty or repetitive.

```markdown
## Bottom Line

## Scope

- Objective:
- Time horizon:
- Geography/jurisdiction:
- Included:
- Excluded:

## Findings

| Finding | Confidence | Evidence |
|---|---:|---|

## Evidence Review

| Source | Type | Date | Credibility | Key Use |
|---|---|---:|---|---|

## Analysis

## Counterarguments

## Unknowns

## Educational References

## Next Research Moves
```

## Quality Bar

Before finalizing, verify:

- The answer serves the user's decision or learning goal.
- Current claims were checked against current sources or clearly bounded.
- Primary sources are preferred where available.
- Dates are absolute when recency matters.
- Major claims have support or are labeled as inference.
- The strongest counterargument is represented fairly.
- Educational references are useful and not filler.
- The final answer is concise enough to use, with evidence organized below.
