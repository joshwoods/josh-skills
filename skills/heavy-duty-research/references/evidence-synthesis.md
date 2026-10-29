# Evidence Synthesis And Confidence Reference

Use this note when a research task needs systematic-review discipline, transparent inclusion/exclusion, evidence tables, or confidence grading.

This note is an example layer for the broader concepts in `research-concepts.md`, especially evidence fit, search transparency, structured synthesis, and confidence calibration. Teach those concepts first; use the named sources here as concrete illustrations.

## Source Cards

### PRISMA 2020

- Organization: PRISMA Executive / PRISMA Statement
- Source type: Reporting guideline for systematic reviews and meta-analyses
- URL: https://www.prisma-statement.org/prisma-2020
- Key paper: Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al. "The PRISMA 2020 statement: an updated guideline for reporting systematic reviews." BMJ 2021;372:n71.
- Credibility: PRISMA is a canonical reporting standard for systematic reviews. The 2020 site provides statement paper, 27-item checklist, expanded checklist, abstract checklist, explanation/elaboration paper, and flow diagrams.
- Limitations: PRISMA is primarily a reporting guideline. It improves transparency but does not by itself guarantee that search strategy, bias assessment, or synthesis decisions were valid.

Core substance:

- Use a checklist to report title, abstract, rationale, objectives, eligibility criteria, information sources, search strategy, selection process, data collection, data items, risk-of-bias assessment, synthesis methods, certainty assessment, results, discussion, registration, protocol, support, competing interests, and data availability.
- Use a flow diagram to track records identified, screened, excluded, included, and reasons for exclusions.
- Read the statement together with the explanation and elaboration paper when implementing the checklist.
- Use PRISMA-style artifacts even for lighter research when transparency matters: search log, screening log, source counts, exclusion reasons, and synthesis table.

### Cochrane Handbook For Systematic Reviews Of Interventions

- Organization: Cochrane
- Source type: Detailed methodology handbook
- URL: https://training.cochrane.org/handbook/current
- Version: 6.5, 2024 on the current-version landing page; some chapters have later updates, including Chapter 4 updated March 2025.
- Senior editors: Julian Higgins and James Thomas
- Credibility: Cochrane is a leading institution for evidence synthesis in health research. The handbook is a detailed methods authority for review scope, eligibility, search, selection, extraction, bias, synthesis, GRADE, and interpretation.
- Limitations: Written for intervention reviews, especially health. Adapt its methods carefully for software, business, market, policy, or legal research.

Core substance:

- Start with a well-formulated, decision-relevant question. Cochrane emphasizes questions that fill important knowledge gaps and matter to review users.
- Define scope and question using PICO when appropriate: population, intervention, comparison, outcome.
- Predefine objectives and eligibility criteria before screening.
- Plan how different populations, interventions, outcomes, and study designs will be grouped for synthesis.
- Search comprehensively enough to minimize bias; in formal reviews, involve information specialists and search multiple databases/registers.
- Aim for sensitive searches where missing relevant evidence would distort the conclusion.
- Document search dates, databases, strategies, selection process, and reasons for exclusion.
- Distinguish studies from reports of studies. Multiple articles may describe the same underlying study.
- Extract structured data and study characteristics before synthesis.
- Assess bias and conflicts of interest, then interpret findings in light of those limitations.
- Use "Summary of findings" tables for key outcomes, effect sizes, quantity of evidence, and certainty.
- Use GRADE certainty levels: high, moderate, low, very low.
- Downgrade certainty for risk of bias, inconsistency, indirectness, imprecision, and publication bias.
- Upgrade some non-randomized evidence only in unusual circumstances, such as very large effects, dose-response gradients, or plausible confounding that would reduce rather than explain the observed effect.

### Oxford CEBM Levels Of Evidence

- Organization: Oxford Centre for Evidence-Based Medicine, University of Oxford
- Source type: Evidence hierarchy and rapid appraisal heuristic
- URL: https://www.cebm.ox.ac.uk/resources/levels-of-evidence/ocebm-levels-of-evidence
- Version: OCEBM Levels of Evidence 2.1 / 2011 table and explanatory documents
- Credibility: Developed by an evidence-based medicine working group including Jeremy Howick, Iain Chalmers, Paul Glasziou, Trish Greenhalgh, Carl Heneghan, Alessandro Liberati, Ivan Moschetti, Bob Phillips, Hazel Thornton, Olive Goddard, and Mary Hodgkinson.
- Limitations: It is a heuristic for finding likely best evidence, not a definitive judgment or recommendation engine. The introductory document explicitly warns that no ranking system replaces judgment.

Core substance:

- Evidence type should match question type. Prevalence, diagnosis, prognosis, treatment benefit, common harm, rare harm, and screening have different best evidence.
- Systematic reviews are generally better than individual studies, except some local-prevalence questions where current local surveys can be ideal.
- Study level can be downgraded for quality, imprecision, indirectness, inconsistency, or very small absolute effect size.
- Evidence can sometimes be upgraded for large or very large effects.
- The levels do not produce recommendations. Decision-making still requires applicability, benefit-harm balance, alternative options, values, and circumstances.

## Practical Synthesis Workflow

Use this workflow for a heavy-duty research brief. Scale the rigor to the stakes.

1. Protocol/scope
   - Write the exact question.
   - State intended decision, user, time horizon, geography, and domain.
   - Define inclusion/exclusion criteria before reading deeply.
   - Decide whether PICO or another frame fits.
2. Search plan
   - List databases, official sources, repositories, search engines, queries, and date searched.
   - Include primary sources and dissenting/negative sources.
   - For current topics, verify recency explicitly.
3. Screening
   - Track records found, screened, kept, rejected, and reason for rejection.
   - Deduplicate multiple reports of the same underlying study or event.
   - Keep a "maybe" pile only briefly; resolve it before synthesis.
4. Extraction
   - For each kept source, capture title, author/institution, date, source type, method, population, key data, claim, limitation, and use in answer.
   - Separate raw findings from interpretation.
5. Bias and limitation assessment
   - Check study design, confounding, selection effects, measurement quality, missing data, selective reporting, incentives, conflicts, and publication bias.
   - For non-academic sources, check commercial, political, legal, or reputational incentives.
6. Synthesis
   - Group sources by claim, method, population, time, jurisdiction, or evidence type.
   - Identify consensus, disagreement, trend over time, and outliers.
   - Do not average incompatible evidence just because it is available.
7. Confidence statement
   - Assign confidence per finding, not just per source.
   - Explain what would change the conclusion.
   - Label inference and speculation.
8. Reporting
   - Provide bottom line, findings table, evidence review, counterarguments, unknowns, educational references, and next research moves.
   - For systematic-style tasks, include a compact PRISMA-like search/screening note.

## PRISMA-Lite Search Record

Use this for heavy-duty briefs that are not formal systematic reviews:

```markdown
### Search Record

- Question:
- Date searched:
- Databases/search engines:
- Official sources:
- Search strings:
- Records found:
- Records screened:
- Sources included:
- Sources excluded with reasons:
- Known gaps:
- Last recency check:
```

## Extraction Table

```markdown
| Source | Type | Date | Method/Data | Claim Used | Bias/Limitations | Use In Synthesis |
|---|---|---:|---|---|---|---|
| ... | Primary / Paper / Data / Filing / News / Docs | ... | ... | ... | ... | ... |
```

## Confidence Grading

Use this pragmatic grading for general research. It is inspired by GRADE and OCEBM but adapted beyond medicine.

### High Confidence

Use when:

- Multiple strong sources converge.
- Primary evidence is available and directly answers the question.
- Methods are transparent and fit the claim.
- Evidence is current enough.
- Bias risks are low or do not plausibly explain the finding.
- Dissent is weak, explained, or limited to edge cases.

Typical evidence:

- Official records plus independent confirmation.
- Systematic review or meta-analysis with low major limitations.
- Reproducible dataset/code with clear methods.
- Audited financial filing for financial facts.
- Current statute/regulation/court decision for legal status, with jurisdiction confirmed.

### Medium Confidence

Use when:

- Evidence is credible but incomplete.
- Sources agree on the broad direction but differ in magnitude, population, or mechanism.
- Primary evidence exists but needs interpretation.
- Some bias, indirectness, or recency concerns remain.

Typical evidence:

- Several reputable secondary sources and one partial primary source.
- Good observational studies without decisive causal identification.
- Company documentation corroborated by user reports or independent tests.
- Trade data with known sampling or reporting limitations.

### Low Confidence

Use when:

- Evidence is sparse, indirect, stale, or highly conflicted.
- Findings rely on a single source.
- Methods are unclear.
- Claims are plausible but not corroborated.
- The conclusion is mostly inference.

Typical evidence:

- Unsourced social posts.
- Marketing claims without independent validation.
- Small case reports or anecdotes.
- Expert opinion without data.
- Early preprints without replication.

## Downgrading Factors

Downgrade a finding when any of these materially affect the claim:

- Risk of bias: weak design, confounding, selective reporting, missing data, poor controls, conflicts.
- Inconsistency: credible sources point in different directions and the difference is not explained.
- Indirectness: evidence studies a different population, jurisdiction, setting, product version, outcome, or timeframe.
- Imprecision: wide uncertainty, small sample, rare events, fuzzy definitions, or unstable estimates.
- Publication/reporting bias: likely missing negative results, survivorship bias, vendor-selected benchmarks, or SEO-driven visibility.
- Staleness: the source predates major legal, technical, market, or scientific changes.
- Applicability gap: the evidence may be true generally but not for the user's specific use case.

## Upgrading Factors

Upgrade cautiously when:

- A large effect is hard to explain away by bias.
- There is a dose-response or exposure-response relationship.
- Plausible confounding would reduce the observed effect, not create it.
- Independent primary sources converge despite different incentives.
- A direct observation verifies the claim in the user's environment.

## Adapting Systematic Review Rigor Outside Medicine

### Software

- PICO equivalent: user/context, intervention/tool, comparator/baseline, outcome metric.
- Strong evidence: reproducible benchmarks, source code, issue history, security advisories, official docs, independent tests.
- Bias risks: cherry-picked benchmarks, version drift, synthetic workloads, undisclosed hardware, vendor incentives.
- Confidence example:
  - High: official docs plus reproducible benchmark and independent replication on current versions.
  - Medium: official docs plus credible user reports, but no independent benchmark.
  - Low: announcement post with no docs, code, or measurable results.

### Business And Market

- PICO equivalent: segment, product/business model, comparator, outcome such as adoption, margin, retention, willingness to pay.
- Strong evidence: audited filings, transaction data, pricing pages, procurement records, customer interviews with method notes, reputable datasets.
- Bias risks: survivorship, self-reported revenue, analyst incentives, tiny samples, outdated market definitions.
- Confidence example:
  - High: public filings and multiple independent datasets agree.
  - Medium: credible estimates and primary artifacts agree directionally.
  - Low: founder claims and press coverage repeat the same unsourced number.

### Policy And Law

- PICO equivalent: jurisdiction/population, rule/intervention, prior rule/comparator, outcome/obligation/risk.
- Strong evidence: enacted statute, regulation, agency guidance, court opinion, official docket, legislative text.
- Bias risks: outdated summaries, nonbinding guidance treated as law, wrong jurisdiction, pending bill treated as enacted.
- Confidence example:
  - High: current official code/regulation and agency guidance align.
  - Medium: primary law exists but interpretation depends on unresolved cases.
  - Low: law-firm blog without citations or currentness checks.

### Medicine And Health

- Use Cochrane/GRADE more directly.
- Strong evidence depends on question type: systematic reviews of randomized trials for treatment benefits, appropriately designed diagnostic studies for test accuracy, cohort evidence for prognosis, and sufficiently powered evidence for harms.
- Always separate treatment benefits, common harms, rare harms, and applicability to a specific patient or population.

## Educational Explanation

Evidence is not strong because it sounds scientific or comes from a prestigious place. It is strong when the study design, data, method, and context fit the exact question. The best evidence for "does this treatment help?" is not necessarily the best evidence for "is this rare harm possible?" or "how common is this locally?" This is why OCEBM organizes evidence by question type and why Cochrane/GRADE judge certainty per outcome.

Systematic discipline protects against accidental cherry-picking. PRISMA makes the search and reporting transparent. Cochrane methods show how to predefine scope, screen sources, extract data, assess bias, and summarize findings. GRADE-style confidence keeps the answer honest by saying not only what the evidence suggests, but how much trust the evidence deserves.

## Output Pattern

```markdown
Confidence: Medium.

Reason: The finding is supported by two primary sources and three credible secondary analyses, but the evidence is indirect for the user's exact segment and all quantitative estimates are more than 18 months old. I downgraded for indirectness and staleness. A current dataset or direct customer sample would move this toward high confidence.
```
