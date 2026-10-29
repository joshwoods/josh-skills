# Literature Discovery And Paper Reading Reference

Use this note when searching scholarly literature, building a research map, reading technical papers, or helping a user enter a new domain.

This note is an example layer for the broader concepts in `research-concepts.md`, especially literature graph navigation, reading-depth control, search transparency, and structured synthesis. Teach those concepts first; use the named sources here as concrete illustrations.

## Source Cards

### Google Scholar Search Help

- Institution: Google Scholar
- Source type: Official product help and search guidance
- URL: https://scholar.google.com/intl/en/scholar/help.html
- Date: No single publication date exposed on the help page.
- Credibility: It is first-party documentation for Scholar behavior, search features, access links, alerts, citation export, and coverage caveats.
- Limitations: Google Scholar is broad but not transparent enough for reproducible systematic-review searches. It does not provide bulk access, shows limited result depth, and cannot guarantee uninterrupted coverage of any source.

Core substance:

- Results are normally sorted by relevance, not by date. Use "Since Year" for recent papers sorted by relevance and "Sort by date" for newest additions.
- Use alerts to monitor new results for a topic, author, or citations to a specific paper.
- For full text, try library links, right-side `[PDF]` or `[HTML]` links, "All versions," publisher pages, and institutional access.
- Use secondary sources to learn terminology when entering a field, then search Scholar with the field's actual terms.
- Use references to move backward to more foundational work.
- Use "Cited by" to move forward to newer work.
- Use "Related articles" to find nearby papers.
- Search by author with `author:"name"` and by exact title with quotation marks.
- Advanced search supports author, title, publication field, and date limits.
- Scholar includes many scholarly literature types: journal and conference papers, theses, dissertations, books, preprints, abstracts, technical reports, court opinions, and patents.
- Scholar coverage is broad but imperfect. Verify coverage of a source by searching a sample of exact paper titles.
- Scholar records and citation counts can lag because updates require recrawling source websites.
- Legal opinions in Scholar are informational and not a substitute for licensed legal advice.

### S. Keshav: How To Read A Paper

- Author: S. Keshav, David R. Cheriton School of Computer Science, University of Waterloo
- Source type: Short academic-method paper
- URL: https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf
- Original venue/date: ACM SIGCOMM Computer Communication Review, 2007
- Credibility: Widely circulated paper-reading method by a computer science professor; concrete, repeatable, and designed for research-paper triage and literature surveys.
- Limitations: Written from a technical/computer-science perspective. Adapt for legal, market, policy, or qualitative research rather than applying mechanically.

Core substance:

- Do not read every paper linearly from start to finish. Use up to three passes, each with a different goal.
- First pass: 5-10 minute scan to understand the category, context, correctness, contributions, and clarity. Read title, abstract, introduction, headings, conclusion, and references.
- Second pass: up to about an hour. Read more carefully while skipping deep proof details. Inspect figures, diagrams, axes, error bars, and marked references. Summarize the main argument and support.
- Third pass: for deep understanding or review. Reconstruct the work, challenge assumptions, identify hidden weaknesses, and note future work.
- Literature survey method:
  - Search an academic engine for three to five recent papers using good keywords.
  - First-pass those papers and read their related-work sections.
  - Look for survey papers.
  - Identify shared citations and repeated author names.
  - Visit key researchers' pages and top venue proceedings.
  - Iterate when the selected papers repeatedly cite a key work you missed.

## Practical Literature Discovery Workflow

1. Translate the user's topic into search concepts.
   - Plain-language topic.
   - Field-specific terms.
   - Synonyms, acronyms, older names, and adjacent disciplines.
   - Entities: authors, labs, companies, agencies, statutes, technologies, products.
2. Start broad.
   - One or two Scholar searches.
   - One domain-specific database or official repository when relevant.
   - One high-quality secondary source to learn vocabulary.
3. Find anchor papers or anchor sources.
   - Recent review paper.
   - Highly cited foundational paper.
   - Current benchmark or standard.
   - Authoritative government, legal, or standards document.
4. Expand backward and forward.
   - Backward: references and related work.
   - Forward: "Cited by," newer papers, later standards, updated guidelines.
   - Sideways: "Related articles," same authors, same venue, same dataset, same method.
5. Triage with Keshav first-pass.
   - Keep, maybe, reject.
   - Record why, not just the URL.
6. Deep-read only the highest-value items.
   - Use second or third pass when a paper becomes central to a finding.
7. Stop with a defensible boundary.
   - Record search queries, databases, dates, inclusion/exclusion criteria, and known gaps.

## Search Tactics

### Scholar Queries

- Exact title: `"A History of the China Sea"`
- Author: `author:"donald e knuth"`
- Recent relevance: use "Since Year."
- Newest additions: use "Sort by date."
- Forward citation chasing: click "Cited by."
- Similar work: click "Related articles."
- Full text: check `[PDF]`, `[HTML]`, "All versions," library links, and publisher pages.
- Coverage check: search exact titles from a journal, conference, or repository to see whether Scholar sees them.

### Query Expansion

Use this when results are sparse or noisy:

| Problem | Move |
|---|---|
| Search terms are too colloquial | Read a credible overview and harvest field terms |
| Results are too broad | Add method, population, jurisdiction, date, or venue |
| Results are too narrow | Remove implementation-specific terms and search the parent concept |
| Results are stale | Use "Since Year," alerts, proceedings, preprints, and agency updates |
| Results are low quality | Search named venues, authors, standards bodies, databases, or exact references |
| Results disagree | Build a chronology and compare methods, populations, incentives, and definitions |

## Keshav Paper-Reading Template

```markdown
### Paper: ...

- Citation:
- URL/DOI:
- Venue/date:
- Research job:
- Pass used: First / Second / Third

#### First Pass
- Category:
- Context:
- Correctness assumptions:
- Contributions:
- Clarity:
- Keep/maybe/reject:

#### Second Pass
- Main claim:
- Method:
- Data/sample:
- Figures/tables checked:
- Evidence strength:
- Important references to chase:
- Limitations:

#### Third Pass
- Reconstructed argument:
- Assumptions challenged:
- Missing citations or alternate explanations:
- Reproducibility concerns:
- Future-work ideas:
- Final use in synthesis:
```

## Literature Review Checklist For Codex

- Frame:
  - What exact question is being answered?
  - Is this exploratory, standard brief, or systematic-style review?
  - What time horizon and geography matter?
- Search:
  - What query strings were used?
  - Which databases or repositories were searched?
  - Were primary and secondary sources both considered?
  - Were newer and foundational works both checked?
- Screen:
  - What inclusion/exclusion rules were applied?
  - Were papers rejected for irrelevance, weak method, stale data, inaccessible text, or duplicate coverage?
- Extract:
  - What claim, method, population, data, and limitation does each source contribute?
  - Is the finding from one paper or a pattern across papers?
- Synthesize:
  - What is consensus?
  - What is contested?
  - What changed over time?
  - Which papers are central, and which are only background?
- Teach:
  - What should a beginner read first?
  - What should an intermediate reader read next?
  - What advanced source would let the user inspect the frontier or original method?

## Examples

### Technical Papers

1. Search Scholar with the technique name, benchmark, dataset, and canonical acronym.
2. First-pass five recent papers and one survey if available.
3. Use references to identify the original method paper and dataset paper.
4. Use "Cited by" to identify replications, critiques, and improvements.
5. Second-pass papers that directly support the answer.
6. Third-pass only papers whose claims are central or surprising.

Use in answer: separate "paper claims," "benchmark evidence," "independent replication," and "field consensus."

### Market Map

1. Search scholarly literature only for durable concepts: market structure, adoption theory, unit economics, regulation, or user behavior.
2. Combine papers with primary market artifacts: filings, pricing pages, customer docs, app store data, job postings, import/export data, procurement records.
3. Use citation chasing to find academic framing, not market share truth.
4. Treat company blogs and analyst reports as leads until corroborated.

Use in answer: explain which insights come from research literature and which come from market evidence.

### Policy Or Legal Research

1. Start with official law, regulation, agency guidance, court opinions, or bill text.
2. Use Scholar/case-law search for commentary, empirical studies, and legal scholarship.
3. Use exact-title and jurisdiction filters when available.
4. Track currentness carefully: enactment date, effective date, amended date, case status.
5. Treat academic articles as interpretation unless they quote or analyze primary legal sources.

Use in answer: do not substitute scholarship for jurisdiction-specific legal authority.

### Product Research

1. Search papers for technical feasibility, human factors, security, reliability, or behavior.
2. Search docs, changelogs, repositories, benchmarks, and issue trackers for implementation reality.
3. Use "Cited by" for methods that may have been superseded.
4. Compare lab results against field constraints such as latency, cost, privacy, deployment, maintenance, and failure modes.

Use in answer: translate research results into product implications with caveats.

## Educational Explanation

Entering a new field is mostly a vocabulary and map-building problem. Start with broad orientation, learn the field's terms, identify the anchor papers and people, then use citation trails to understand how ideas evolved. Do not deep-read everything. Triage aggressively with first passes, deepen only where the source affects the conclusion, and keep a record of what was searched and excluded.

Keshav's method prevents drowning in detail. Google Scholar's tools help move through the literature graph. Together they create a repeatable loop: search, skim, map, chase, deep-read, synthesize.

## Output Pattern

```markdown
Literature method: I started with recent Scholar searches for "..." and "...", then used references and "Cited by" links to identify the anchor papers. I first-passed 12 papers, second-passed 4, and treated 2 as central evidence. The review is not exhaustive because I did not search paywalled domain databases or non-English literature.
```
