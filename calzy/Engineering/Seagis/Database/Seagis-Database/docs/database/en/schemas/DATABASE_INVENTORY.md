# DATABASE_INVENTORY

Version: 1.0.0 | Date: 2026-10-27

[Complete document](../DATABASE_DOCUMENTATION.md) | [README](../../README.md)

PostgreSQL/Supabase is the backend persistence defined by code. Schema `seagis` owns registries, observations, forecasts and provenance; `seagis_raw` holds raw manifests; `seagis_api` bounds the IoT gateway; `seagis_environment` manages regional workers; `seagis_quality` stores QC reviews; `seagis_features` supplies containers not connected to a production feature builder. Supabase internal schemas such as auth/storage are not inventoried as application-owned: current catalog access is unavailable and they must not be assumed empty.

Python retrieves provider data outside the database. A2/A3 workers call stored functions through psycopg; the TypeScript handler invokes only ingest/history/status functions. No ORM was found on these paths. Mutation transactions live in SQL functions; fetch claiming is a separate transaction from persistence so network calls do not hold a database transaction.

The diagram contains disconnected components: the iOS mock has no backend edge. Future integration remains UNVERIFIED. Production Core ML, distributed caches, warehouses, queues and search indexes were NOT FOUND in inspected implementation files; that does not establish absence of services outside these checkouts.

| Store | Evidence status | Purpose/environment | Owner | Scope | Access | Authority | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PostgreSQL / Supabase | VERIFIED (repository + historical catalog) | Backend; current deployment environment UNVERIFIED | Seagis-Model | Registry, sensor, regional, QC, features | read/write via stored functions | Authoritative for persisted records; not a diagnosis | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:1` |
| Supabase Storage | configured / UNVERIFIED usage | Local storage enabled; object_uri supported, application bucket NOT FOUND | Supabase | objects / metadata_only | configured | Not proven to be active raw storage | `Seagis-Model/supabase/config.toml:116` |
| UserDefaults / launch arguments | VERIFIED code | Preference/debug UI access; not plot persistence | AppPOC | initialPlot / initialFarmer / skipCaptureSteps / detailDay | read preference/argument values | Not authoritative for backend data | `AppPOC/POCApp/Features/FarmMap/ViewModels/FarmMapViewModel.swift:1` |
| legacy AR files | VERIFIED cleanup code | ar-site.json/ar-site.worldmap are only deleted at new AR session start | AppPOC | legacy local AR files | best-effort delete; active writer NOT FOUND | Not active persistence | `AppPOC/POCApp/Features/PlotCapture/ViewModels/ARCaptureViewModel.swift:1` |
| JSON / CSV files | VERIFIED code | Synthetic fixtures, policies, experimental exports and manifests | Python scripts | fixtures/config/export | file read/write | Authoritative only for that capture/fixture version | `Seagis-Model/scripts/export_experiment_csv.py:1` |
| in-memory Swift arrays | VERIFIED code | Prototype state; lost at process termination | AppPOC | Farmer / CultivationPlot | array append/remove | Local demo state | `AppPOC/POCApp/Shared/Data/FarmStore.swift:1` |

Supabase auth, vector and analytics service defaults appear in local configuration, but active application buckets/indexes/datasets are not established. These are service settings, not additional application databases. All table row counts are UNVERIFIED; fixtures are not used as runtime estimates.

| Schema | Objects | Tables | Views | Access boundary |
| --- | --- | --- | --- | --- |
| seagis | dataset, dataset_parameter, forecast_run, forecast_value, ingestion_run, observation, parameter, plot, plot_grid_mapping, quality_event, sensor, source, source_grid | 13 | 0 | Access through backend routines; live membership UNVERIFIED |
| seagis_api | credential, packet_receipt, reader_plot, request_event, temperature_policy | 5 | 0 | Access through backend routines; live membership UNVERIFIED |
| seagis_environment | attempt, current_speed, demo_grid_mapping, policy, schedule_state | 4 | 1 | Access through backend routines; live membership UNVERIFIED |
| seagis_features | feature_input, feature_snapshot | 2 | 0 | Access through backend routines; live membership UNVERIFIED |
| seagis_quality | alignment_snapshot, policy, snapshot_input | 3 | 0 | Access through backend routines; live membership UNVERIFIED |
| seagis_raw | raw_payload | 1 | 0 | Access through backend routines; live membership UNVERIFIED |

| Physical object | Purpose | Columns | Evidence |
| --- | --- | --- | --- |
| seagis.dataset | Dataset identity, version, cadence, licence and ingestion gates. | 15 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:17` |
| seagis.dataset_parameter | Source-variable to parameter contract and conversion rules. | 9 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:43` |
| seagis.forecast_run | Regional model capture/vintage; unknown publication time remains null. | 13 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:216` |
| seagis.forecast_value | Parameter value per run, grid and valid time; not duplicated per plot. | 20 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241` |
| seagis.ingestion_run | Audit of a logical ingestion and its completion state. | 9 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:94` |
| seagis.observation | Local sensor water-temperature readings, retaining native values, QC and raw lineage. | 19 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184` |
| seagis.parameter | Registry of parameters and normalized units. | 3 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:36` |
| seagis.plot | Plot identity and survey status; nullable coordinates are not evidence of a surveyed location. | 8 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:58` |
| seagis.plot_grid_mapping | Operational plot-to-grid mapping with effective and recorded times. | 10 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:152` |
| seagis.quality_event | Append-only QC log for ingestion or one measurement. | 11 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:273` |
| seagis.sensor | Temperature sensor deployment identity, plot, depth and active state. | 10 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:73` |
| seagis.source | Registry of dataset providers. | 3 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:11` |
| seagis.source_grid | Regional cell and depth-layer identity; distinct from cultivation plots. | 10 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:135` |
| seagis_api.credential | API actor identity using token hashes, expiry and revocation. | 8 | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:27` |
| seagis_api.packet_receipt | Sensor-packet idempotency key and semantic digest. | 6 | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:53` |
| seagis_api.reader_plot | Plot allowlist for a reader credential. | 2 | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:39` |
| seagis_api.request_event | Authenticated API response audit and rate-limit basis. | 6 | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:44` |
| seagis_api.temperature_policy | Pilot engineering QC settings and request limit; not disease thresholds. | 8 | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:67` |
| seagis_environment.attempt | Audit of a fetch attempt, including duplicate and abandoned outcomes. | 7 | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:57` |
| seagis_environment.current_speed | Current-magnitude view joining components from the same run, grid and time. | 9 | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:89` |
| seagis_environment.demo_grid_mapping | Bridge from two fictional plots to real grids for preview, not training authorization. | 11 | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:69` |
| seagis_environment.policy | Regional fetch, licence, scheduler cadence, staleness and retention policy. | 11 | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:16` |
| seagis_environment.schedule_state | Mutable lease, due time, backoff and last-success state. | 9 | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:45` |
| seagis_features.feature_input | Foreign-key input lineage and cutoff guards for feature snapshots. | 4 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:320` |
| seagis_features.feature_snapshot | Draft/sealed feature container with cutoff and hashes; no production builder found. | 12 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:301` |
| seagis_quality.alignment_snapshot | Immutable hourly QC/alignment document; always training_authorized=false. | 11 | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:21` |
| seagis_quality.policy | Immutable registry of QC policy versions and builder code hashes. | 5 | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:14` |
| seagis_quality.snapshot_input | Per-hour measurement lineage of an alignment snapshot. | 5 | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:35` |
| seagis_raw.raw_payload | Immutable raw manifest: digest, hash basis, licence and retention mode. | 14 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:110` |

