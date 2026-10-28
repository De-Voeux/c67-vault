# ENTITY_RELATIONSHIPS

Version: 1.0.0 | Date: 2026-10-27

[Complete document](../DATABASE_DOCUMENTATION.md) | [README](../../README.md)

All relationships below are physical foreign keys from the historical catalog and migrations. A parent has 0..N children unless the child join key is unique, limiting it to 0..1; a child references exactly one parent when all columns are NOT NULL, or 0..1 when nullable under MATCH SIMPLE. Composite foreign keys bind dataset/synthetic flags to prevent lineage mixing. A foreign key does not require a parent to have children.

### FK1 `seagis.source` → `seagis.dataset`

| Attribute | Definition |
| --- | --- |
| Constraint | dataset_source_key_fkey |
| Join | (source_key) → (source_key) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Dataset identity, version, cadence, licence and ingestion gates. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:17` |


```sql
FOREIGN KEY (source_key) REFERENCES seagis.source(source_key);
```

### FK2 `seagis.dataset` → `seagis.dataset_parameter`

| Attribute | Definition |
| --- | --- |
| Constraint | dataset_parameter_dataset_key_fkey |
| Join | (dataset_key) → (dataset_key) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Source-variable to parameter contract and conversion rules. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:43` |


```sql
FOREIGN KEY (dataset_key) REFERENCES seagis.dataset(dataset_key);
```

### FK3 `seagis.parameter` → `seagis.dataset_parameter`

| Attribute | Definition |
| --- | --- |
| Constraint | dataset_parameter_parameter_code_unit_fkey |
| Join | (parameter_code,unit) → (parameter_code,unit) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Source-variable to parameter contract and conversion rules. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:43` |


```sql
FOREIGN KEY (parameter_code, unit) REFERENCES seagis.parameter(parameter_code, unit);
```

### FK4 `seagis.dataset` → `seagis.forecast_run`

| Attribute | Definition |
| --- | --- |
| Constraint | forecast_run_dataset_key_scope_fkey |
| Join | (dataset_key,scope) → (dataset_key,scope) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Regional model capture/vintage; unknown publication time remains null. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:216` |


```sql
FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset(dataset_key, scope);
```

### FK5 `seagis_raw.raw_payload` → `seagis.forecast_run`

| Attribute | Definition |
| --- | --- |
| Constraint | forecast_run_raw_payload_id_ingestion_run_id_dataset_key_i_fkey |
| Join | (raw_payload_id,ingestion_run_id,dataset_key,is_synthetic) → (id,ingestion_run_id,dataset_key,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Regional model capture/vintage; unknown publication time remains null. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:216` |


```sql
FOREIGN KEY (raw_payload_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis_raw.raw_payload(id, ingestion_run_id, dataset_key, is_synthetic);
```

### FK6 `seagis.dataset_parameter` → `seagis.forecast_value`

| Attribute | Definition |
| --- | --- |
| Constraint | forecast_value_dataset_key_parameter_code_native_unit_unit_fkey |
| Join | (dataset_key,parameter_code,native_unit,unit,conversion_code) → (dataset_key,parameter_code,native_unit,unit,conversion_code) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Parameter value per run, grid and valid time; not duplicated per plot. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241` |


```sql
FOREIGN KEY (dataset_key, parameter_code, native_unit, unit, conversion_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code, native_unit, unit, conversion_code);
```

### FK7 `seagis.forecast_run` → `seagis.forecast_value`

| Attribute | Definition |
| --- | --- |
| Constraint | forecast_value_forecast_run_id_dataset_key_is_synthetic_fkey |
| Join | (forecast_run_id,dataset_key,is_synthetic) → (id,dataset_key,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Parameter value per run, grid and valid time; not duplicated per plot. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241` |


```sql
FOREIGN KEY (forecast_run_id, dataset_key, is_synthetic) REFERENCES seagis.forecast_run(id, dataset_key, is_synthetic);
```

### FK8 `seagis.source_grid` → `seagis.forecast_value`

| Attribute | Definition |
| --- | --- |
| Constraint | forecast_value_source_grid_id_dataset_key_is_synthetic_fkey |
| Join | (source_grid_id,dataset_key,is_synthetic) → (id,dataset_key,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Parameter value per run, grid and valid time; not duplicated per plot. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241` |


```sql
FOREIGN KEY (source_grid_id, dataset_key, is_synthetic) REFERENCES seagis.source_grid(id, dataset_key, is_synthetic);
```

### FK9 `seagis.dataset` → `seagis.ingestion_run`

| Attribute | Definition |
| --- | --- |
| Constraint | ingestion_run_dataset_key_fkey |
| Join | (dataset_key) → (dataset_key) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Audit of a logical ingestion and its completion state. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:94` |


```sql
FOREIGN KEY (dataset_key) REFERENCES seagis.dataset(dataset_key);
```

### FK10 `seagis.dataset_parameter` → `seagis.observation`

| Attribute | Definition |
| --- | --- |
| Constraint | observation_dataset_key_parameter_code_native_unit_unit_co_fkey |
| Join | (dataset_key,parameter_code,native_unit,unit,conversion_code) → (dataset_key,parameter_code,native_unit,unit,conversion_code) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Local sensor water-temperature readings, retaining native values, QC and raw lineage. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184` |


```sql
FOREIGN KEY (dataset_key, parameter_code, native_unit, unit, conversion_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code, native_unit, unit, conversion_code);
```

### FK11 `seagis_raw.raw_payload` → `seagis.observation`

| Attribute | Definition |
| --- | --- |
| Constraint | observation_raw_payload_id_ingestion_run_id_dataset_key_is_fkey |
| Join | (raw_payload_id,ingestion_run_id,dataset_key,is_synthetic) → (id,ingestion_run_id,dataset_key,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Local sensor water-temperature readings, retaining native values, QC and raw lineage. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184` |


```sql
FOREIGN KEY (raw_payload_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis_raw.raw_payload(id, ingestion_run_id, dataset_key, is_synthetic);
```

### FK12 `seagis.sensor` → `seagis.observation`

| Attribute | Definition |
| --- | --- |
| Constraint | observation_sensor_id_plot_id_dataset_key_is_synthetic_fkey |
| Join | (sensor_id,plot_id,dataset_key,is_synthetic) → (id,plot_id,dataset_key,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Local sensor water-temperature readings, retaining native values, QC and raw lineage. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184` |


```sql
FOREIGN KEY (sensor_id, plot_id, dataset_key, is_synthetic) REFERENCES seagis.sensor(id, plot_id, dataset_key, is_synthetic);
```

### FK13 `seagis.plot` → `seagis.plot_grid_mapping`

| Attribute | Definition |
| --- | --- |
| Constraint | plot_grid_mapping_plot_id_is_synthetic_fkey |
| Join | (plot_id,is_synthetic) → (id,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Operational plot-to-grid mapping with effective and recorded times. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:152` |


```sql
FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot(id, is_synthetic);
```

### FK14 `seagis.source_grid` → `seagis.plot_grid_mapping`

| Attribute | Definition |
| --- | --- |
| Constraint | plot_grid_mapping_source_grid_id_fkey |
| Join | (source_grid_id) → (id) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Operational plot-to-grid mapping with effective and recorded times. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:152` |


```sql
FOREIGN KEY (source_grid_id) REFERENCES seagis.source_grid(id);
```

### FK15 `seagis.forecast_value` → `seagis.quality_event`

| Attribute | Definition |
| --- | --- |
| Constraint | quality_event_forecast_value_id_dataset_key_is_synthetic_fkey |
| Join | (forecast_value_id,dataset_key,is_synthetic) → (id,dataset_key,is_synthetic) |
| Cardinality | 1:0..N; child → parent 0..1 |
| Optional | true |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Append-only QC log for ingestion or one measurement. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:273` |


```sql
FOREIGN KEY (forecast_value_id, dataset_key, is_synthetic) REFERENCES seagis.forecast_value(id, dataset_key, is_synthetic);
```

### FK16 `seagis.ingestion_run` → `seagis.quality_event`

| Attribute | Definition |
| --- | --- |
| Constraint | quality_event_ingestion_run_id_dataset_key_is_synthetic_fkey |
| Join | (ingestion_run_id,dataset_key,is_synthetic) → (id,dataset_key,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Append-only QC log for ingestion or one measurement. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:273` |


```sql
FOREIGN KEY (ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.ingestion_run(id, dataset_key, is_synthetic);
```

### FK17 `seagis.observation` → `seagis.quality_event`

| Attribute | Definition |
| --- | --- |
| Constraint | quality_event_observation_id_ingestion_run_id_dataset_key__fkey |
| Join | (observation_id,ingestion_run_id,dataset_key,is_synthetic) → (id,ingestion_run_id,dataset_key,is_synthetic) |
| Cardinality | 1:0..N; child → parent 0..1 |
| Optional | true |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Append-only QC log for ingestion or one measurement. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:273` |


```sql
FOREIGN KEY (observation_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.observation(id, ingestion_run_id, dataset_key, is_synthetic);
```

### FK18 `seagis.dataset_parameter` → `seagis.sensor`

| Attribute | Definition |
| --- | --- |
| Constraint | sensor_dataset_key_parameter_code_fkey |
| Join | (dataset_key,parameter_code) → (dataset_key,parameter_code) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Temperature sensor deployment identity, plot, depth and active state. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:73` |


```sql
FOREIGN KEY (dataset_key, parameter_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code);
```

### FK19 `seagis.dataset` → `seagis.sensor`

| Attribute | Definition |
| --- | --- |
| Constraint | sensor_dataset_key_scope_fkey |
| Join | (dataset_key,scope) → (dataset_key,scope) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Temperature sensor deployment identity, plot, depth and active state. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:73` |


```sql
FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset(dataset_key, scope);
```

### FK20 `seagis.plot` → `seagis.sensor`

| Attribute | Definition |
| --- | --- |
| Constraint | sensor_plot_id_is_synthetic_fkey |
| Join | (plot_id,is_synthetic) → (id,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Temperature sensor deployment identity, plot, depth and active state. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:73` |


```sql
FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot(id, is_synthetic);
```

### FK21 `seagis.dataset` → `seagis.source_grid`

| Attribute | Definition |
| --- | --- |
| Constraint | source_grid_dataset_key_scope_fkey |
| Join | (dataset_key,scope) → (dataset_key,scope) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Regional cell and depth-layer identity; distinct from cultivation plots. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:135` |


```sql
FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset(dataset_key, scope);
```

### FK22 `seagis.sensor` → `seagis_api.credential`

| Attribute | Definition |
| --- | --- |
| Constraint | credential_sensor_id_fkey |
| Join | (sensor_id) → (id) |
| Cardinality | 1:0..N; child → parent 0..1 |
| Optional | true |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | API actor identity using token hashes, expiry and revocation. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:27` |


```sql
FOREIGN KEY (sensor_id) REFERENCES seagis.sensor(id);
```

### FK23 `seagis.ingestion_run` → `seagis_api.packet_receipt`

| Attribute | Definition |
| --- | --- |
| Constraint | packet_receipt_ingestion_run_id_fkey |
| Join | (ingestion_run_id) → (id) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Sensor-packet idempotency key and semantic digest. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:53` |


```sql
FOREIGN KEY (ingestion_run_id) REFERENCES seagis.ingestion_run(id);
```

### FK24 `seagis.observation` → `seagis_api.packet_receipt`

| Attribute | Definition |
| --- | --- |
| Constraint | packet_receipt_observation_id_fkey |
| Join | (observation_id) → (id) |
| Cardinality | 1:0..1; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Sensor-packet idempotency key and semantic digest. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:53` |


```sql
FOREIGN KEY (observation_id) REFERENCES seagis.observation(id);
```

### FK25 `seagis.sensor` → `seagis_api.packet_receipt`

| Attribute | Definition |
| --- | --- |
| Constraint | packet_receipt_sensor_id_fkey |
| Join | (sensor_id) → (id) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Sensor-packet idempotency key and semantic digest. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:53` |


```sql
FOREIGN KEY (sensor_id) REFERENCES seagis.sensor(id);
```

### FK26 `seagis_api.credential` → `seagis_api.reader_plot`

| Attribute | Definition |
| --- | --- |
| Constraint | reader_plot_credential_id_fkey |
| Join | (credential_id) → (id) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Plot allowlist for a reader credential. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:39` |


```sql
FOREIGN KEY (credential_id) REFERENCES seagis_api.credential(id);
```

### FK27 `seagis.plot` → `seagis_api.reader_plot`

| Attribute | Definition |
| --- | --- |
| Constraint | reader_plot_plot_id_fkey |
| Join | (plot_id) → (id) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Plot allowlist for a reader credential. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:39` |


```sql
FOREIGN KEY (plot_id) REFERENCES seagis.plot(id);
```

### FK28 `seagis_api.credential` → `seagis_api.request_event`

| Attribute | Definition |
| --- | --- |
| Constraint | request_event_credential_id_fkey |
| Join | (credential_id) → (id) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Authenticated API response audit and rate-limit basis. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:44` |


```sql
FOREIGN KEY (credential_id) REFERENCES seagis_api.credential(id);
```

### FK29 `seagis.sensor` → `seagis_api.request_event`

| Attribute | Definition |
| --- | --- |
| Constraint | request_event_sensor_id_fkey |
| Join | (sensor_id) → (id) |
| Cardinality | 1:0..N; child → parent 0..1 |
| Optional | true |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Authenticated API response audit and rate-limit basis. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:44` |


```sql
FOREIGN KEY (sensor_id) REFERENCES seagis.sensor(id);
```

### FK30 `seagis_environment.policy` → `seagis_environment.attempt`

| Attribute | Definition |
| --- | --- |
| Constraint | attempt_dataset_key_fkey |
| Join | (dataset_key) → (dataset_key) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Audit of a fetch attempt, including duplicate and abandoned outcomes. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:57` |


```sql
FOREIGN KEY (dataset_key) REFERENCES seagis_environment.policy(dataset_key);
```

### FK31 `seagis.forecast_run` → `seagis_environment.attempt`

| Attribute | Definition |
| --- | --- |
| Constraint | attempt_forecast_run_id_fkey |
| Join | (forecast_run_id) → (id) |
| Cardinality | 1:0..N; child → parent 0..1 |
| Optional | true |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Audit of a fetch attempt, including duplicate and abandoned outcomes. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:57` |


```sql
FOREIGN KEY (forecast_run_id) REFERENCES seagis.forecast_run(id);
```

### FK32 `seagis_environment.policy` → `seagis_environment.demo_grid_mapping`

| Attribute | Definition |
| --- | --- |
| Constraint | demo_grid_mapping_dataset_key_fkey |
| Join | (dataset_key) → (dataset_key) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Bridge from two fictional plots to real grids for preview, not training authorization. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:69` |


```sql
FOREIGN KEY (dataset_key) REFERENCES seagis_environment.policy(dataset_key);
```

### FK33 `seagis.plot` → `seagis_environment.demo_grid_mapping`

| Attribute | Definition |
| --- | --- |
| Constraint | demo_grid_mapping_plot_id_plot_is_synthetic_fkey |
| Join | (plot_id,plot_is_synthetic) → (id,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Bridge from two fictional plots to real grids for preview, not training authorization. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:69` |


```sql
FOREIGN KEY (plot_id, plot_is_synthetic) REFERENCES seagis.plot(id, is_synthetic);
```

### FK34 `seagis.source_grid` → `seagis_environment.demo_grid_mapping`

| Attribute | Definition |
| --- | --- |
| Constraint | demo_grid_mapping_source_grid_id_dataset_key_grid_is_synth_fkey |
| Join | (source_grid_id,dataset_key,grid_is_synthetic) → (id,dataset_key,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Bridge from two fictional plots to real grids for preview, not training authorization. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:69` |


```sql
FOREIGN KEY (source_grid_id, dataset_key, grid_is_synthetic) REFERENCES seagis.source_grid(id, dataset_key, is_synthetic);
```

### FK35 `seagis.dataset` → `seagis_environment.policy`

| Attribute | Definition |
| --- | --- |
| Constraint | policy_dataset_key_fkey |
| Join | (dataset_key) → (dataset_key) |
| Cardinality | 1:0..1; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Regional fetch, licence, scheduler cadence, staleness and retention policy. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:16` |


```sql
FOREIGN KEY (dataset_key) REFERENCES seagis.dataset(dataset_key);
```

### FK36 `seagis_environment.policy` → `seagis_environment.schedule_state`

| Attribute | Definition |
| --- | --- |
| Constraint | schedule_state_dataset_key_fkey |
| Join | (dataset_key) → (dataset_key) |
| Cardinality | 1:0..1; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Mutable lease, due time, backoff and last-success state. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:45` |


```sql
FOREIGN KEY (dataset_key) REFERENCES seagis_environment.policy(dataset_key);
```

### FK37 `seagis.forecast_run` → `seagis_environment.schedule_state`

| Attribute | Definition |
| --- | --- |
| Constraint | schedule_state_last_forecast_run_id_fkey |
| Join | (last_forecast_run_id) → (id) |
| Cardinality | 1:0..N; child → parent 0..1 |
| Optional | true |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Mutable lease, due time, backoff and last-success state. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:45` |


```sql
FOREIGN KEY (last_forecast_run_id) REFERENCES seagis.forecast_run(id);
```

### FK38 `seagis.forecast_value` → `seagis_features.feature_input`

| Attribute | Definition |
| --- | --- |
| Constraint | feature_input_forecast_value_id_fkey |
| Join | (forecast_value_id) → (id) |
| Cardinality | 1:0..N; child → parent 0..1 |
| Optional | true |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Foreign-key input lineage and cutoff guards for feature snapshots. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:320` |


```sql
FOREIGN KEY (forecast_value_id) REFERENCES seagis.forecast_value(id);
```

### FK39 `seagis.observation` → `seagis_features.feature_input`

| Attribute | Definition |
| --- | --- |
| Constraint | feature_input_observation_id_fkey |
| Join | (observation_id) → (id) |
| Cardinality | 1:0..N; child → parent 0..1 |
| Optional | true |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Foreign-key input lineage and cutoff guards for feature snapshots. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:320` |


```sql
FOREIGN KEY (observation_id) REFERENCES seagis.observation(id);
```

### FK40 `seagis_features.feature_snapshot` → `seagis_features.feature_input`

| Attribute | Definition |
| --- | --- |
| Constraint | feature_input_snapshot_id_fkey |
| Join | (snapshot_id) → (id) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Foreign-key input lineage and cutoff guards for feature snapshots. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:320` |


```sql
FOREIGN KEY (snapshot_id) REFERENCES seagis_features.feature_snapshot(id);
```

### FK41 `seagis.plot` → `seagis_features.feature_snapshot`

| Attribute | Definition |
| --- | --- |
| Constraint | feature_snapshot_plot_id_is_synthetic_fkey |
| Join | (plot_id,is_synthetic) → (id,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Draft/sealed feature container with cutoff and hashes; no production builder found. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:301` |


```sql
FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot(id, is_synthetic);
```

### FK42 `seagis.plot` → `seagis_quality.alignment_snapshot`

| Attribute | Definition |
| --- | --- |
| Constraint | alignment_snapshot_plot_id_fkey |
| Join | (plot_id) → (id) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Immutable hourly QC/alignment document; always training_authorized=false. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:21` |


```sql
FOREIGN KEY (plot_id) REFERENCES seagis.plot(id);
```

### FK43 `seagis_quality.policy` → `seagis_quality.alignment_snapshot`

| Attribute | Definition |
| --- | --- |
| Constraint | alignment_snapshot_policy_version_fkey |
| Join | (policy_version) → (version) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Immutable hourly QC/alignment document; always training_authorized=false. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:21` |


```sql
FOREIGN KEY (policy_version) REFERENCES seagis_quality.policy(version);
```

### FK44 `seagis.forecast_value` → `seagis_quality.snapshot_input`

| Attribute | Definition |
| --- | --- |
| Constraint | snapshot_input_forecast_value_id_fkey |
| Join | (forecast_value_id) → (id) |
| Cardinality | 1:0..N; child → parent 0..1 |
| Optional | true |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Per-hour measurement lineage of an alignment snapshot. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:35` |


```sql
FOREIGN KEY (forecast_value_id) REFERENCES seagis.forecast_value(id);
```

### FK45 `seagis.observation` → `seagis_quality.snapshot_input`

| Attribute | Definition |
| --- | --- |
| Constraint | snapshot_input_observation_id_fkey |
| Join | (observation_id) → (id) |
| Cardinality | 1:0..N; child → parent 0..1 |
| Optional | true |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Per-hour measurement lineage of an alignment snapshot. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:35` |


```sql
FOREIGN KEY (observation_id) REFERENCES seagis.observation(id);
```

### FK46 `seagis_quality.alignment_snapshot` → `seagis_quality.snapshot_input`

| Attribute | Definition |
| --- | --- |
| Constraint | snapshot_input_snapshot_id_fkey |
| Join | (snapshot_id) → (id) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Per-hour measurement lineage of an alignment snapshot. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:35` |


```sql
FOREIGN KEY (snapshot_id) REFERENCES seagis_quality.alignment_snapshot(id);
```

### FK47 `seagis.ingestion_run` → `seagis_raw.raw_payload`

| Attribute | Definition |
| --- | --- |
| Constraint | raw_payload_ingestion_run_id_dataset_key_is_synthetic_fkey |
| Join | (ingestion_run_id,dataset_key,is_synthetic) → (id,dataset_key,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Immutable raw manifest: digest, hash basis, licence and retention mode. |
| Integrity risk | FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:110` |


```sql
FOREIGN KEY (ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.ingestion_run(id, dataset_key, is_synthetic);
```

Additional logical relationships: two forecast_value aliases in current_speed join on forecast_run_id, source_grid_id and valid_at; parameter_code distinguishes u/v. This is a view join, not a new FK. source_ref uses typed prefixes, a CHECK and two alternative FKs; no invented FK targets a polymorphic string. No self-referencing FK was found. reader_plot, dataset_parameter, feature_input and snapshot_input act as association/lineage entities, with composite keys/uniqueness recorded in the dictionary. AppPOC Farmer→CultivationPlot is an in-memory relationship and is excluded from the 47 PostgreSQL FKs.

Full and per-schema ERDs are in architecture/ERD.md.

