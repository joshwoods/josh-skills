---
name: heavy-duty-research
description: Use when the user wants deep, evidence-backed research with explicit source quality checks, competing hypotheses, synthesis, and educational references for learning the topic. Best for market research, technical research, policy/legal/regulatory scans, product strategy, literature reviews, and due diligence where correctness and decision usefulness matter more than speed.
---

# Heavy-Duty Research

Use this skill to turn a broad research question into a rigorous, source-backed brief with a learning trail the user can follow afterward.

## Core Principles

- Optimize for decision quality, not volume.
- Separate facts, source claims, analysis, and speculation.
- Prefer primary sources: official docs, original papers, filings, standards, datasets, source code, transcripts, court records, regulatory text, and first-party announcements.
- Use secondary sources to discover leads, context, and dissenting interpretations, then verify against primary material.
- Track uncertainty explicitly. If a claim is not well-supported, label it as tentative.
- Compare alternatives and incentives. Strong research explains why reasonable people disagree.
- Include educational references that help the user understand the field, not only sources that support the answer.

Use local reference notes before falling back to live links:

- Read `references/research-concepts.md` when teaching or applying transferable research concepts.
- Read `references/source-evaluation.md` when evaluating credibility, checking web claims, or teaching source hygiene.
- Read `references/literature-discovery.md` when searching academic literature, reading papers, or entering a new domain.
- Read `references/evidence-synthesis.md` when running a systematic, high-rigor, or confidence-graded review.
- Read `references/educational-references.md` for routing guidance across the education/reference pack.

Treat the local research-method references as scaffolding, not as topic evidence:

- Teach the concepts, not the brand names of the example sources.
- Use the named references as examples of broader principles: context recovery, source-role matching, claim tracing, literature graph navigation, structured synthesis, and confidence calibration.
- Cite or summarize them only when the user asks about research methodology, source quality, evidence grading, or how to learn the research process.
- In topical briefs, the evidence table and findings should be driven by domain-specific primary and secondary sources.
- Educational references should usually teach the user's topic, not the skill's methodology.

## Research Workflow

### 1. Frame The Question

Start by rewriting the user's request as:

- Research objective
- Intended decision or output
- Scope boundaries
- Time horizon
- Geography or jurisdiction, if relevant
- Required depth
- Known constraints

If the user provided a link, paper, thread, repository, dataset, or artifact, retrieve and summarize it before broadening the search. If it cannot be retrieved, ask for the missing content or proceed only with a clearly labeled assumption.

### 2. Build A Source Map

Create a source plan before synthesis:

- Primary sources that can directly answer the question
- Authoritative secondary sources for context
- Data sources or benchmarks
- Dissenting or negative sources
- Educational references for topic fundamentals

For current facts, browse or otherwise verify recency. Do not rely on memory for laws, prices, product capabilities, rankings, benchmarks, APIs, companies, or public figures.

### 3. Collect Evidence

For every important source, capture:

- Title
- Author or institution
- Date
- URL or local path
- Source type
- Key claim or data point
- Why it is credible
- Known limitations or bias

Prefer exact numbers, dates, definitions, and directly attributable claims. Avoid long quotations unless the wording itself matters.

### 4. Evaluate Source Quality

Classify sources by confidence:

- High: primary source, official record, peer-reviewed paper, reproducible dataset, source code, or directly observed artifact.
- Medium: reputable expert analysis, trade publication with named sources, well-cited technical writing, or transparent methodology.
- Low: unsourced posts, marketing copy, anonymous commentary, SEO summaries, or claims that cannot be corroborated.

For controversial or high-stakes claims, require at least two independent confirmations or explain why only one source exists.

### 5. Synthesize

Do not produce a pile of notes. Convert evidence into a usable answer:

- Bottom line
- Key findings
- Evidence table
- Competing interpretations
- Risks and unknowns
- Practical implications
- Recommended next steps
- Educational references

When useful, include a confidence level for each major finding.

### 6. Teach The Topic

Add an educational section that helps the user become more capable:

- Foundational concepts
- Recommended reading order
- Glossary of important terms
- Canonical books, papers, docs, talks, or courses
- Exercises or prompts the user can use to test understanding

Educational references should be chosen for clarity, durability, and authority within the user's topic. Separate beginner, intermediate, and advanced resources when the topic is broad.

When recommending a research-method reference, summarize the relevant local note and explain how to apply it to the user's topic. Do not provide only a bare link list.

## Output Format

Use this structure unless the user asks for another format:

```markdown
## Bottom Line

One to three paragraphs answering the question directly.

## Scope

- Objective:
- Time horizon:
- Geography/jurisdiction:
- Included:
- Excluded:

## Findings

| Finding | Confidence | Evidence |
|---|---:|---|
| ... | High/Medium/Low | ... |

## Evidence Review

| Source | Type | Date | Credibility | Key Use |
|---|---|---:|---|---|
| ... | Primary/Secondary/Data | ... | High/Medium/Low | ... |

## Analysis

Reasoned synthesis, tradeoffs, and implications.

## Counterarguments

Strongest opposing views or reasons the conclusion may be wrong.

## Unknowns

Gaps, stale data risks, inaccessible sources, and assumptions.

## Educational References

Topic-specific learning references. Omit or keep brief unless the user asked to learn the topic.

### Beginner
- ...

### Intermediate
- ...

### Advanced
- ...

## Next Research Moves

1. ...
2. ...
3. ...
```

## Quality Bar

Before finalizing, verify:

- The answer directly serves the user's decision or learning goal.
- Current claims were checked against current sources.
- Primary sources are preferred where available.
- Important dates are absolute, not only relative.
- Every major claim has support or is labeled as inference.
- The strongest counterargument is represented fairly.
- Educational references are not filler and do not crowd out the answer; each one teaches a useful layer of the topic.
- Research-method references are not presented as evidence for topical claims unless the topic is research methodology itself.
- Research concepts are explained in transferable language rather than as allegiance to a particular framework.
- The final answer is concise enough to use, with deeper evidence organized below it.

## Research Modes

Use one of these modes depending on the request:

- Fast scan: 5-10 sources, concise synthesis, clear caveats.
- Standard brief: 10-25 sources, evidence table, counterarguments, educational trail.
- Deep dossier: 25+ sources, source map, chronology, data review, expert landscape, open questions, and a recommended validation plan.

If the user asks for "heavy duty," default to Standard brief unless the stakes justify Deep dossier.
