# SEAGIS — TRACK B: SCIENTIFIC KNOWLEDGE VAULT & FOUNDATION MODELS

**Status:** Implementation instructions v0.1  
**Audience:** Research / scientific-evidence / iOS agent  
**Language:** Indonesian for product outputs and documentation; English for structured identifiers.  
**Goal:** Create a traceable, verified scientific evidence vault and use it to generate **cautious environmental interpretations**, not disease diagnoses.

## 0. Scope and boundaries

- Target context: seaweed aquaculture around Pulau Tidung, especially *Kappaphycus alvarezii* where evidence exists.
- Core environmental variables: **water temperature, salinity, nitrate, phosphate**; extend to currents, precipitation, wind, cloud cover, UV/solar exposure when research warrants.
- **Track B can start in parallel with Track A.** Use synthetic `assessment_packet` fixtures until Track A's real data contract is ready.
- Apple Foundation Models is an **interpretation layer**: it must not calculate authoritative anomaly scores, assign invented biological risk probabilities, or diagnose ice-ice disease.
- A literature claim is not automatically a universal threshold. Distinguish experimental response, correlation, mechanistic hypothesis, and field observation.
- Do not use model-generated citations as evidence. Every knowledge entry must point to an actual accessible source and precise supporting passage/table/figure before being marked verified.
- Use a small **JSON/SQL vault with tag-based retrieval** for v0.1; do not introduce embeddings/vector databases or fine-tuning without demonstrated need.

## 1. Workstreams and order

### Phase B0 — Research scope, taxonomy, and schema (START HERE)

**Tasks**
- Write explicit research questions:
  1. What physiological or growth effects are reported for each variable?
  2. What interactions between variables have been directly tested?
  3. Which results apply to *K. alvarezii*, other eucheumatoids, or other organisms only?
  4. Under which exposure duration, life stage, salinity/nutrient unit, and experimental conditions were findings observed?
  5. What can and cannot be inferred about ice-ice susceptibility?
- Define a controlled taxonomy for `parameter_tags`, `species`, `outcome`, `evidence_type`, `experimental_setting`, `verification_status`, `applicability`, and `limitation_tags`.
- Design source and claim schemas. **One atomic claim per entry**; one paper may produce multiple claims. Keep claims separate from source metadata.
- Establish review states: `candidate` → `extracted` → `needs_review` → `verified` / `rejected` / `superseded`.

**Required deliverables**
- `docs/research_questions.md`.
- `docs/evidence_taxonomy.md`.
- `schemas/source.schema.json`, `schemas/knowledge_entry.schema.json`.
- `vault/sources.jsonl`, `vault/entries.jsonl` (or equivalent SQL tables).
- `docs/review_protocol.md` with citation and evidence-verification rules.

**Acceptance criteria**
- Schema can represent single-variable effects, parameter interactions, non-significant results, and conflicting findings.
- An entry cannot become `verified` without source location, reviewer identity/date, and checked units/context.

### Phase B1 — Literature discovery and source registry

**Tasks**
- Start with a curated seed set of **5–8 relevant studies**. Previously discussed candidate DOIs: `10.1111/jpy.70044` (salinity–nutrient interaction) and `10.1111/jpy.70148` (light-related physiological response). Verify bibliographic metadata and full-text availability before extraction.
- Search by species and topic, not merely `ice-ice`: `Kappaphycus alvarezii temperature salinity`, `eucheumatoid nutrient limitation nitrate phosphate`, `combined stress temperature salinity`, etc.
- Include field studies, controlled experiments, and reviews, but tag their evidence types separately.
- Capture title, authors, year, DOI/URL, species, location, design, outcomes, and full-text access status.
- Avoid extrapolating coral-bleaching thresholds or mechanisms to seaweed as established fact. Cross-organism literature can be tagged `hypothesis_only`.

**Acceptance criteria**
- Each source has a stable identifier and a verifiable bibliographic record.
- Copyright and source access are respected; store metadata, short evidence snippets, and references rather than copying entire copyrighted papers into a distributable vault.

### Phase B2 — AI-assisted evidence extraction

**Tasks**
- Extract candidate atomic claims from each accessible paper, preferably from Methods, Results, tables, and figures, not just the abstract.
- For each candidate capture:
  - exact parameter names, values, **units**, experimental ranges, exposure durations, species, sample size (when available);
  - outcome measured (growth, bleaching, photosynthesis, stress markers, disease incidence, etc.);
  - direction of effect, uncertainty/statistical significance if reported;
  - type of evidence (`controlled_experiment`, `observational_association`, `mechanistic_hypothesis`, `review_synthesis`);
  - page/section/table/figure and brief supporting excerpt;
  - limitations and whether the claim generalizes to Pulau Tidung.
- Record **null or non-significant findings**, not only positive associations.
- Keep extraction status `needs_review`. The AI must not self-approve evidence.

**Acceptance criteria**
- Every extracted numerical claim preserves its original units and exposure context.
- Each candidate can be traced to a precise source location or remains unverified.

### Phase B3 — Human verification and vault curation

**Tasks**
- Reviewer checks source passage/table/figure against the candidate entry, including units, species, exposure, direction, significance, and interpretation.
- Reject unsupported causal language, invented thresholds, missing citation locations, or cross-species generalizations presented as proven.
- If papers disagree, retain both with context; do not collapse conflicting findings into a fabricated consensus.
- Record `verified_by`, `verified_at`, `review_notes`, and optional second-reviewer status.
- Target first milestone: **10–15 verified atomic claims** spanning single parameters and at least some interactions, if supported by literature.

**Acceptance criteria**
- Spot-check of verified entries matches source evidence exactly.
- Every entry has an explicit `limitations` field; unsupported threshold values are absent.

### Phase B4 — Retrieval and scientific context packets

**Tasks**
- Build deterministic retrieval by `parameter_tags`, `species`, `evidence_type`, `applicability`, and `verification_status`.
- Retrieve **only verified** entries for production explanations. Rank same-species direct evidence above related-species or mechanism-only evidence; make ranking rules explicit.
- Return a compact context packet with IDs, concise findings, evidence type, limitations, and citations. Include conflicting findings when material.
- Enforce token budget. Start with top 3–5 relevant entries, not whole papers.
- Define `knowledge_version` so generated explanations are reproducible and auditable.

**Acceptance criteria**
- Given a four-variable scenario, retriever returns relevant verified evidence and indicates missing evidence.
- No fabricated source IDs, no unverified entry promoted silently.

### Phase B5 — Apple Foundation Models interpretation

**Tasks**
- Integrate Apple's `FoundationModels` framework on supported iOS versions/devices, checking model availability and language support at runtime. Confirm current SDK/API compatibility in Xcode before coding.
- Use concise system instructions to require: Indonesian; measured vs forecast separation; local vs regional separation; evidence-only claims; no invented units/thresholds/probabilities; explicit uncertainty and data limitations.
- Use `@Generable` for structured output. Suggested fields: `headline`, `observedFindings`, `combinedImplication`, `suggestedInspection`, `citedMeasurementIDs`, `citedKnowledgeIDs`, `limitations`.
- Generate from **Track A assessment packet + retrieved scientific context**, never from raw numbers without units, provenance, and relevant baseline/quality metadata.
- Validate generated output: cited IDs must exist; no numerical claims without source; unsupported disease diagnoses and fabricated thresholds must be blocked. Prefer deterministic fallback when model unavailable or validation fails.
- Optionally add tool calling for plot-history/knowledge retrieval later; start with app-controlled retrieval and explicit prompt context for easier audit.
- Do not assume fine-tuning/adapters are available or needed on iOS 27; check current Apple support before making such a dependency.

**Acceptance criteria**
- Structured outputs render in SwiftUI and can be validated against input IDs.
- The app remains usable without Apple Intelligence availability.
- Tests demonstrate the model explicitly refuses unsupported biological certainty.

### Phase B6 — Evaluation and scientific QA

**Tasks**
- Build a fixed evaluation set with examples: missing nutrient units, zero versus below detection, conflicting evidence, coarse regional grid, normal local baseline versus unusual reading, stale forecasts, incomplete data, and multiple interacting parameters.
- Evaluate factual grounding, unit fidelity, correct evidence citations, hallucination rate, unsupported causal claims, appropriate uncertainty, and action usefulness.
- Have a human reviewer assess a sample of generated explanations; log prompt/knowledge/model versions and test outcomes.
- Keep warning severity determined by Track A's deterministic engine, not by LLM phrasing.

**Acceptance criteria**
- Critical tests pass: no invented disease probability, no fabricated source, no claim that coarse ocean grid measures a specific tambak, and no interpretation of nutrient zero without quality context.

## 2. Canonical knowledge-entry example

**Illustrative placeholder; NOT a verified scientific claim.**

```json
{
  "id": "TEMP-SAL-001",
  "schema_version": "0.1.0",
  "species": ["Kappaphycus alvarezii"],
  "parameter_tags": ["water_temperature", "salinity"],
  "relationship_type": "interaction",
  "finding": null,
  "evidence_type": "controlled_experiment",
  "outcome": null,
  "experimental_conditions": {
    "temperature": null,
    "salinity": null,
    "exposure_duration": null
  },
  "source_id": null,
  "source_location": null,
  "limitations": [],
  "applicability": "unassessed",
  "verification_status": "candidate",
  "verified_by": null,
  "verified_at": null
}
```

## 3. Integration contract (Track A ↔ Track B)

**Input:** `assessment_packet` from Track A, including `schema_version`, `assessment_id`, `plot_id`, timestamp, measured/forecast values with units, source scope, QC, computed findings, missing context, and numeric evidence IDs.

**Retrieval:** `getRelevantKnowledge(parameterTags, species, constraints) → knowledge_context` with verified IDs, concise claims, citations, limitations, and `knowledge_version`.

**Output:** `environmental_insight` with structured text, `citedMeasurementIDs`, `citedKnowledgeIDs`, caveats, and generation metadata. Do not store invented biological labels or treat LLM output as scientific ground truth.

**Test fixture:** `33°C water temperature / 38 PSU salinity / NO3 0 mmol/m³ / PO4 0.5 mmol/m³` with explicitly synthetic provenance. The expected response distinguishes high-level context from verified site-specific risk and recognizes that a modeled zero and a missing observation are not interchangeable.

## 4. Minimal project structure

```text
seagis/
  docs/
    research_questions.md
    evidence_taxonomy.md
    review_protocol.md
  schemas/
    source.schema.json
    knowledge_entry.schema.json
  vault/
    sources.jsonl
    entries.jsonl
  extraction/
    extract_candidates.py
    validate_schema.py
  retrieval/
    retrieve_knowledge.py
  evaluation/
    cases.jsonl
    expected_behaviors.md
  ios/
    ScientificInsightGenerator.swift
    EnvironmentalInsight.swift
```

## 5. Agent execution protocol

1. **First response:** inspect repo, propose taxonomy and JSON schemas for B0, identify existing research files and exact access limitations. Do not invent paper findings.
2. Implement **B0 only** and provide sample **unverified** entry and tests. Stop for review before bulk extraction unless authorized.
3. Use AI to accelerate extraction, but require **human verification** before `verified` status. Never self-certify.
4. At each phase, report changed files, evidence/source coverage, pending verifications, test results, and next blockers.
5. Keep Foundation Models integration independent from Track A's forecasting training so both tracks can progress concurrently.
