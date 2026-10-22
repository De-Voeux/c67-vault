# SEAGIS — TRACK A: DATA & ML ENGINEERING

**Status:** Implementation instructions v0.1  
**Audience:** Coding / data-engineering agent  
**Language:** Indonesian for documentation; English for identifiers and code.  
**Goal:** Build a reproducible, testable data foundation and environmental forecasting workflow for seaweed cultivation plots around Pulau Tidung. **Do not start with model training.**

## 0. Non-negotiable scope and assumptions

1. **Primary backend:** Supabase PostgreSQL, Supabase Storage if needed, and Edge Functions/Cron for lightweight orchestration. Long-running or Python-heavy ingestion/training may run in an external scheduled worker; do not force all jobs into Edge Functions.
2. **Local observations:** One submerged **water-temperature sensor per cultivation plot**, intended to report approximately hourly. ESP32/cellular transport is being developed separately. In development, use clearly labeled simulated records.
3. **Oceanographic context:** Copernicus Marine, including salinity (`so`), current components (`uo`, `vo`), nitrate (`no3`), phosphate (`po4`). Check exact product/dataset IDs, variable availability, depths, cadence, and license from current catalog before implementation. Candidate products: `GLOBAL_ANALYSISFORECAST_PHY_001_024` and `GLOBAL_ANALYSISFORECAST_BGC_001_028`.
4. **Atmospheric context:** Open-Meteo API for ingestion and ML: hourly `precipitation`, `wind_speed_10m`, `wind_direction_10m`, `cloud_cover`, `uv_index`, `temperature_2m`. Confirm API model, geographic grid, data license, attribution, and usage tier before deployment. Do not assume free noncommercial access permits a commercial product.
5. **WeatherKit:** Excluded from Track A ingestion/storage/training. It may later power **live weather display directly in iOS**. Do not silently replace Open-Meteo with WeatherKit.
6. **Primary custom ML target:** Local **water-temperature forecasting** per plot, initially 1h/3h/6h ahead. Longer horizons (24h/3d/7d) are optional experiments gated by validation; monthly is research-only until enough data exist. Environmental warning is distinct from ice-ice disease prediction.
7. **Geographic fidelity:** A Copernicus or atmospheric grid cell can cover multiple plots. Never present coarse regional values as independent plot-level observations. Preserve source-grid identity and sampling method.
8. **Scientific integrity:** Do not invent ice-ice probability, universal safe ranges, causal weights, or biological thresholds. Missing or low-quality inputs must be explicit.
9. **Engineering priority:** Working vertical slice > premature microservices, dashboards, or complex ML.

## 1. Execution order / milestones

### Phase A0 — Architecture & data contracts (START HERE)

**Tasks**
- Inventory each source, variable, unit, spatial resolution, temporal cadence, issue/valid time semantics, API/auth, provenance, retention/license constraints, and missing-data behavior.
- Define `plot`, `sensor`, `observation`, `forecast_run`, `forecast_value`, `source_grid`, `ingestion_run`, `quality_event`, and `feature_snapshot` entities. Use separate source-appropriate tables or carefully normalized tables; avoid a single table that loses forecast-run identity.
- Design a **raw → normalized → curated/features** data lifecycle. Raw payloads are immutable where licensing permits; normalized rows carry provenance; curated features are reproducible.
- Distinguish `observed_at`, `valid_at`, `issued_at`, `ingested_at` (UTC), plus `source_timezone` when applicable. Never equate issuance time with forecast valid time.
- Decide uniqueness/idempotency keys, indexes, retention policies, role-based access, API authorization, and migrations.
- Record units **at field level**, including salinity PSU/ppt conventions, nitrate/phosphate units, precipitation accumulation period, wind-speed units, and sea-water versus air temperature.

**Required deliverables**
- `docs/architecture.md` with one architecture diagram.
- `docs/source_registry.md` and `docs/data_dictionary.md`.
- `docs/data_contracts.md` (example payloads for each source and one common normalized representation).
- `supabase/migrations/0001_initial_schema.sql` plus seed data for two sample plots.
- `docs/decisions/ADR-001-data-storage.md` documenting tradeoffs and assumptions.

**Acceptance criteria**
- Each measurement can be traced to provider, grid/sensor, time, unit, and ingestion run.
- Forecast revisions are preserved as separate `forecast_run`s, not overwritten.
- A reviewer can tell which readings are **local** versus **regional**.
- Schema and sample payloads validate, migrations run on a clean database, and basic queries work.

### Phase A1 — Temperature vertical slice

**Tasks**
- Implement authenticated ingestion endpoint for sensor readings; design retry-safe, idempotent writes. Use simulator until hardware exists.
- Generate sample hourly series for Plot A/B with documented synthetic provenance, normal fluctuations, missing hours, duplicate packets, and outliers.
- Store accepted readings and QC flags; preserve original payloads where appropriate.
- Implement `GET /plots/{plot_id}/temperature?from=...&to=...` or equivalent secured API.
- Add ingestion run logs, structured errors, retry policy, and simple operational monitoring.

**Acceptance criteria**
- Duplicates do not create double measurements; delayed packets retain original observation times.
- Gaps, impossible values, and stale readings are flagged rather than silently replaced.
- Plot A/B historical temperature can be queried reliably and independently.

### Phase A2 — Copernicus + Open-Meteo ingestion

**Tasks**
- Build separate source adapters behind a common interface (`fetch`, `parse`, `normalize`, `validate`, `persist`).
- Copernicus: obtain exact dataset metadata and selected depth; persist grid-cell identity and grid-to-plot mapping. Derive current speed from `uo`/`vo`, retaining original vector components.
- Open-Meteo: ingest forecast hourly variables at documented coordinates; explicitly select model or preserve model metadata, unit parameters, timezone UTC, and forecast issuance metadata when available.
- Preserve historical forecast **vintages** (issued forecast versus actual observed outcomes) where source terms allow; do not train on later revisions as if known at prediction time.
- Schedule ingestion based on each provider's update cadence, not an arbitrary uniform hourly refresh.
- Use retry with backoff, deduplication, rate-limit handling, provider-outage fallback, and monitoring.

**Acceptance criteria**
- Sample end-to-end fetch works for one regional grid and two plots.
- Neighboring plots mapped to the same regional cell share a grid record, not falsely distinct measurements.
- Each forecast point retains valid time and associated forecast run/issuance time.
- Source attribution, license, and retention rules are documented and enforced.

### Phase A3 — Data quality & temporal/spatial alignment

**Tasks**
- Implement unit validation, plausible-domain checks, null/NaN handling, outlier flags, sensor drift checks when possible, duplicate detection, stale-data detection, and coverage reporting.
- Distinguish **missing**, **below detection limit**, **measured zero**, **modeled zero**, and **not available**. Especially important for nitrate/phosphate.
- Define deterministic alignment to hourly sensor timestamps. Daily nitrate/phosphate must not be fabricated into new independent hourly observations; if carried forward for contextual features, label age and native cadence.
- Implement as-of joins: a training row at time `t` may only use observations and forecast vintages available by `t`.
- Track spatial grid distance, depth, and representativeness; make warnings when data resolution is coarse relative to plot size.

**Acceptance criteria**
- QC tests cover missing/duplicate/stale/out-of-order/outlier and mismatched-unit cases.
- Leakage test confirms no future-issued forecast appears in earlier training rows.
- Quality report summarizes coverage per source/parameter/plot/time range.

### Phase A4 — Feature engineering

**Tasks**
- Build deterministic temperature features: lagged temperatures, `delta_temperature_1h`, rolling mean/min/max/std over 6/24/72h, diurnal features, deviations from a defensible plot-specific historical baseline, and missingness indicators.
- Atmospheric features: rolling precipitation totals, wind vector components or circular encoding, cloud cover, UV index, air temperature; retain original values and units.
- Ocean features: salinity, nitrate, phosphate, current vector/speed, source age, regional grid identifiers, QC flags.
- Make feature generation repeatable in both offline training and online inference; define feature version and schema.
- Keep raw values, derived values, and model predictions in distinct namespaces.

**Acceptance criteria**
- Identical source snapshot + feature version produces identical feature outputs.
- No target leakage, no cross-plot leakage, no fabricated interpolation without explicit policy.
- Feature tables are queryable and include lineage.

### Phase A5 — Modelling and evaluation

**Tasks**
- Begin with persistence/seasonal-naive baselines, then simple statistical/ML regressors. Add multivariate variables only after demonstrating incremental value.
- Evaluate by **time-ordered walk-forward splits** and separate plots/seasons when data permit; never random-split adjacent hourly observations.
- Report MAE/RMSE (°C), bias, coverage, performance by horizon (1h/3h/6h initially), and failure cases. Compare against baselines.
- Where uncertainty estimates are possible, calibrate and report them; do not imply precise confidence without evidence.
- Export to Core ML only if supported and beneficial; otherwise define an inference interface. Document model version, training cutoff, features, evaluation, and rollback.
- Build a deterministic warning engine based on **observed anomalies and forecasted changes** with explicitly documented provisional operational triggers. Do not label it a validated ice-ice classifier.

**Acceptance criteria**
- Reproducible training run, recorded metrics, saved artifacts, baseline comparison, and model card.
- Model fails safely when input features are missing or stale.
- Warnings state the observed/forecast basis and confidence/quality limitations.

### Phase A6 — Integration handoff

**Tasks**
- Expose secured endpoints for latest plot observations, history, aligned environmental context, forecast values, and **structured assessment packet**.
- Produce `assessment_packet` contract consumed by Track B and iOS; include only traceable claims and evidence IDs for numeric findings.
- Provide mock fixtures for app and Foundation Models development before live data is available.

**Acceptance criteria**
- Track B can consume the packet without accessing raw provider APIs.
- App can display values even if the LLM is unavailable.
- Tests verify backward compatibility of assessment schema.

## 2. Shared `assessment_packet` contract (A → B)

Illustrative structure (all values below are **synthetic**, not biological thresholds):

```json
{
  "schema_version": "0.1.0",
  "assessment_id": "demo-assessment-001",
  "plot_id": "plot-a",
  "generated_at": "2026-10-21T12:00:00Z",
  "measurements": [
    {"evidence_id": "M-001", "parameter": "water_temperature", "value": 33.0, "unit": "degC", "scope": "local_sensor", "observed_at": "2026-10-21T11:00:00Z", "quality": "synthetic"},
    {"evidence_id": "M-002", "parameter": "salinity", "value": 38.0, "unit": "psu", "scope": "regional_model", "valid_at": "2026-10-21T12:00:00Z", "quality": "synthetic"},
    {"evidence_id": "M-003", "parameter": "nitrate", "value": 0.0, "unit": "mmol/m3", "scope": "regional_model", "valid_at": "2026-10-21T12:00:00Z", "quality": "synthetic"},
    {"evidence_id": "M-004", "parameter": "phosphate", "value": 0.5, "unit": "mmol/m3", "scope": "regional_model", "valid_at": "2026-10-21T12:00:00Z", "quality": "synthetic"}
  ],
  "computed_findings": [],
  "forecast_findings": [],
  "missing_context": ["plot_baseline_not_available", "no_field_health_observation"],
  "data_quality_summary": "synthetic_demo_only"
}
```

Production packets must additionally preserve source dataset/run/grid metadata and native cadence. **Do not infer stress severity or ice-ice risk from this sample alone.**

## 3. Engineering standards

- Maintain typed contracts, SQL migrations, test fixtures, linting, CI, and versioned docs.
- Use least-privilege service credentials, row-level security, secrets management, and protected ingestion endpoints; never embed provider secrets in iOS.
- Store timestamps in UTC, retain raw provider units and normalized units with explicit conversion provenance.
- Avoid silent imputation, silent overwrite, and mixing modeled regional values with local sensor observations.
- Use a local development environment and sample fixtures so contributors can run the pipeline without production credentials.
- Keep the initial solution simple: one database, one coherent ingestion layer, one reproducible feature pipeline.

## 4. Agent execution protocol

1. **First response:** inspect existing repo, report relevant existing components, propose A0 schema/architecture, and list assumptions requiring confirmation. Do not overwrite existing work.
2. Implement **A0 only**, with migrations, docs, and tests. Stop for review before A1 unless explicitly authorized to continue.
3. At each phase, provide changed files, commands to run, tests executed, unresolved blockers, and acceptance-criteria checklist.
4. Do not claim real-data ingestion, ML performance, or scientific validation until demonstrated with corresponding evidence.
