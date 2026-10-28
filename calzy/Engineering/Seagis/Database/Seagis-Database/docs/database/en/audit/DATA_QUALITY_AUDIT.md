# DATA_QUALITY_AUDIT

Version: 1.0.0 | Date: 2026-10-27

[Complete document](../DATABASE_DOCUMENTATION.md) | [README](../../README.md)

Read-only audit of code and historical metadata; severity expresses potential impact within the prototype scope, not a measured production incident. No application/schema changes were applied.

### F01 iOS assessment is not connected to backend

| Attribute | Finding |
| --- | --- |
| Severity / category | High / Contract / integration |
| Status | VERIFIED |
| Description / impact | The mock returns synthetic_fixture; no assessment API adapter was found. New consumers must not treat the domain model as a wire contract. |
| Affected | Seagis/Seagis/Repositories/Shared/MockAssessmentRepository.swift, Seagis/Seagis/Models/Shared/Assessment.swift |
| Evidence | `Seagis/Seagis/Repositories/Shared/MockAssessmentRepository.swift:1`; `Seagis/Seagis/Models/Shared/Assessment.swift:1` |
| Recommendation | Agree an executable contract and provenance/error mapping before integration. |

### F02 Mapping immutability after 0005 changes the old closing procedure

| Attribute | Finding |
| --- | --- |
| Severity / category | Medium / Lifecycle |
| Status | VERIFIED |
| Description / impact | A0 guard_mapping permits interval closure; the 0005 trigger rejects all UPDATE/DELETE. A0 architecture instructions for closing mappings can fail on the complete schema. |
| Affected | supabase/migrations/0001_initial_schema.sql, supabase/migrations/0005_quality_alignment.sql, docs/architecture.md |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:1`; `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:1`; `Seagis-Model/docs/architecture.md:1` |
| Recommendation | Define append-only supersession and test interval overlap/cutoff. |

### F03 History grows without a discovered retention job

| Attribute | Finding |
| --- | --- |
| Severity / category | Medium / Governance / retention |
| Status | INFERRED |
| Description / impact | request_event, observations, forecasts and snapshots are append-only; scheduled TTL/cleanup and recovery tests were not found in the checkouts. Capacity risk is inferred, not benchmarked. |
| Affected | supabase/migrations/0001_initial_schema.sql, supabase/migrations/0002_temperature_api.sql, supabase/migrations/0005_quality_alignment.sql |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:1`; `Seagis-Model/supabase/migrations/0002_temperature_api.sql:1`; `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:1` |
| Recommendation | Set domain retention, archival, backups and restore drills before production scale. |

### F04 A3 SQL checks lineage but does not recompute all QC

| Attribute | Finding |
| --- | --- |
| Severity / category | Medium / Validation boundary |
| Status | VERIFIED |
| Description / impact | save_snapshot verifies policy/code hashes and source values, but usable_context/flags/blocking_flags decisions are not recomputed through Python inside the DB. The worker role remains a trust boundary. |
| Affected | supabase/migrations/0005_quality_alignment.sql, scripts/quality/alignment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:1`; `Seagis-Model/scripts/quality/alignment.py:1` |
| Recommendation | Document worker trust; add deterministic QC verification and payload-tampering tests where required. |

### F05 Metadata-only limits raw reproducibility

| Attribute | Finding |
| --- | --- |
| Severity / category | Medium / Data provenance |
| Status | VERIFIED |
| Description / impact | A2 retains no raw content. A Toolbox subset hash is not an original NetCDF/Zarr byte hash; refetching a provider aggregate does not guarantee the same vintage. |
| Affected | scripts/environmental/copernicus.py, supabase/migrations/0003_environment_ingestion.sql |
| Evidence | `Seagis-Model/scripts/environmental/copernicus.py:1`; `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:1` |
| Recommendation | Preserve hash_basis; if licence and cost allow, propose immutable versioned subset/object retention. |

### F06 Capture CSV is not a historical backtest

| Attribute | Finding |
| --- | --- |
| Severity / category | High / Analytics semantics |
| Status | VERIFIED |
| Description / impact | The exporter selects latest_available_at_capture; A3 uses a per-hour cutoff. Treating the CSV as historical availability risks leakage; code explicitly sets training_authorized=false. |
| Affected | scripts/export_experiment_csv.py, scripts/quality/alignment.py |
| Evidence | `Seagis-Model/scripts/export_experiment_csv.py:1`; `Seagis-Model/scripts/quality/alignment.py:1` |
| Recommendation | Use all-vintage source bundles and explicit cutoffs when designing backtests; retain the training gate until validation. |

### F07 A0 documentation predates A1–A3 implementation

| Attribute | Finding |
| --- | --- |
| Severity / category | Low / Documentation drift |
| Status | VERIFIED |
| Description / impact | docs/architecture.md says ingestion/scheduler/QC are not implemented, while subsequent migrations and workers exist. Statements require phase/date context. |
| Affected | docs/architecture.md, scripts/ingest_environment.py, scripts/curate_environment.py |
| Evidence | `Seagis-Model/docs/architecture.md:1`; `Seagis-Model/scripts/ingest_environment.py:1`; `Seagis-Model/scripts/curate_environment.py:1` |
| Recommendation | Use a phase-status index and source manifest for documentation updates. |

### F08 Catalog snapshot is five days old

| Attribute | Finding |
| --- | --- |
| Severity / category | Medium / Runtime verification |
| Status | UNVERIFIED |
| Description / impact | The 22 October snapshot is not a 27 October runtime audit. Grants, row counts, active schedules and current cloud migrations were not reverified. |
| Affected | runtime catalog |
| Evidence | schema-metadata-20261022.json inspected_at |
| Recommendation | Run a read-only catalog diff and grants review before production decisions. |

Priority: P1 agree integration/contracts and prevent leakage (F01/F06); P2 address trust, retention, mapping lifecycle and raw reproducibility (F02–F05); P3 refresh documentation status/catalog (F07/F08). Index/performance evaluation needs EXPLAIN and actual workloads: no missing-index or slow-query claim is established merely from column names.

