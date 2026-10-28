# DATA_LIFECYCLE

Version: 1.0.0 | Date: 2026-10-27

[Complete document](../DATABASE_DOCUMENTATION.md) | [README](../../README.md)

Creation: callers or SQL supply UUIDs as specified in the dictionary; registry natural keys are pinned in seed/config. Raw data, measurements, forecasts, QC and snapshots have mutation guards. Dataset changes are restricted to certain operational gates; semantic changes to dataset, parameter or grid identities require new versions. Location/depth changes require a new sensor deployment; active can be disabled.

Ingestion transitions from running to succeeded/failed/partial under checks and guards. Regional attempts transition from running to succeeded/duplicate/failed/abandoned. An expired lease is marked abandoned on the next claim. Feature snapshots transition draft → sealed; the input manifest must match and a parent row lock prevents races during sealing. A3 snapshots are immutable immediately after insertion. Credentials are revoked using revoked_at or expire through expires_at; neither deletes observations.

A0 initially allowed closing effective_until on mappings. Migration 0005 adds recorded_at and an immutable_alignment_mapping trigger before UPDATE/DELETE. Therefore older instructions to close mappings through UPDATE no longer apply after the full migration chain. New interval resolution requires a design that preserves history without silently bypassing guards.

No age-based cleanup/retention job, general soft delete, tested backup/restore, cross-database replication or iOS-cloud synchronization was found. A2 metadata_only is a raw-content policy, not a TTL for all tables. Foreign keys without explicit ON DELETE/UPDATE use NO ACTION; cascade deletion must not be assumed. Prototype FarmStore deletes farmers and their plots in memory; it does not issue backend SQL DELETE statements.

Migration sequence: 0001 initial, 0002 temperature API, 0003 regional ingestion, 0004 provider_updating, 0005 quality alignment. SQL migrations are forward-only; rollback/down scripts were NOT FOUND. Deployment scripts use administrator access for provisioning and worker-role setup; none was run during this audit. Migration adoption should include backups, empty-schema tests and upgrade tests; these are recommendations, not session test results.

Security: migrations enable RLS on application tables; FORCE RLS=false in the historical snapshot. PUBLIC/anon/authenticated access is restricted; gateway/workers receive selected EXECUTE permissions using SECURITY DEFINER and search_path=pg_catalog. A2/A3 use TLS verify-full with a pinned CA hash. Original tokens are not printed; credentials store hashes. Active administrator privileges, role membership, bucket policies, encryption at rest, actual rotation, production backup and recovery remain UNVERIFIED. Rate-limit logs, attempts, QC events and hashes provide partial auditing; no dead-letter queue or configured external alerting was found on these paths.

Main implementation evidence: `Seagis-Model/supabase/migrations/0001_initial_schema.sql:1`; `Seagis-Model/supabase/migrations/0002_temperature_api.sql:1`; `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:1`; `Seagis-Model/supabase/migrations/0004_provider_update_status.sql:1`; `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:1`.

Main implementation evidence: `Seagis-Model/scripts/environmental/store.py:1`; `Seagis-Model/scripts/quality/store.py:1`; `Seagis-Model/supabase/functions/temperature/connection.ts:1`.

