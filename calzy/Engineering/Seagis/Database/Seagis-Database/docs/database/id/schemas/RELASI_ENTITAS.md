# RELASI_ENTITAS

Version: 1.0.0 | Date: 2026-10-27

[Dokumen lengkap](../DOKUMENTASI_DATABASE.md) | [README](../../README.md)

Semua relasi di bawah adalah FK fisik dari catalog lama dan migrasi. Parent memiliki 0..N child kecuali child join key unik, yang membatasi 0..1 child; child merujuk tepat satu parent bila seluruh kolom NOT NULL, atau 0..1 bila nullable dengan MATCH SIMPLE. FK composite mengikat dataset/flag sintetis agar lineage tidak tercampur. Keberadaan FK tidak membuktikan parent wajib mempunyai child.

### FK1 `seagis.source` → `seagis.dataset`

| Atribut | Definisi |
| --- | --- |
| Constraint | dataset_source_key_fkey |
| Join | (source_key) → (source_key) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Identitas dataset, versi, cadence, lisensi dan gate ingestion. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:17` |


```sql
FOREIGN KEY (source_key) REFERENCES seagis.source(source_key);
```

### FK2 `seagis.dataset` → `seagis.dataset_parameter`

| Atribut | Definisi |
| --- | --- |
| Constraint | dataset_parameter_dataset_key_fkey |
| Join | (dataset_key) → (dataset_key) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Kontrak variabel sumber ke parameter dan aturan konversi. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:43` |


```sql
FOREIGN KEY (dataset_key) REFERENCES seagis.dataset(dataset_key);
```

### FK3 `seagis.parameter` → `seagis.dataset_parameter`

| Atribut | Definisi |
| --- | --- |
| Constraint | dataset_parameter_parameter_code_unit_fkey |
| Join | (parameter_code,unit) → (parameter_code,unit) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Kontrak variabel sumber ke parameter dan aturan konversi. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:43` |


```sql
FOREIGN KEY (parameter_code, unit) REFERENCES seagis.parameter(parameter_code, unit);
```

### FK4 `seagis.dataset` → `seagis.forecast_run`

| Atribut | Definisi |
| --- | --- |
| Constraint | forecast_run_dataset_key_scope_fkey |
| Join | (dataset_key,scope) → (dataset_key,scope) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Capture/vintage model regional; waktu publikasi yang tidak diketahui tetap null. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:216` |


```sql
FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset(dataset_key, scope);
```

### FK5 `seagis_raw.raw_payload` → `seagis.forecast_run`

| Atribut | Definisi |
| --- | --- |
| Constraint | forecast_run_raw_payload_id_ingestion_run_id_dataset_key_i_fkey |
| Join | (raw_payload_id,ingestion_run_id,dataset_key,is_synthetic) → (id,ingestion_run_id,dataset_key,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Capture/vintage model regional; waktu publikasi yang tidak diketahui tetap null. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:216` |


```sql
FOREIGN KEY (raw_payload_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis_raw.raw_payload(id, ingestion_run_id, dataset_key, is_synthetic);
```

### FK6 `seagis.dataset_parameter` → `seagis.forecast_value`

| Atribut | Definisi |
| --- | --- |
| Constraint | forecast_value_dataset_key_parameter_code_native_unit_unit_fkey |
| Join | (dataset_key,parameter_code,native_unit,unit,conversion_code) → (dataset_key,parameter_code,native_unit,unit,conversion_code) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Nilai parameter per run, grid dan valid time; tidak diduplikasi per plot. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241` |


```sql
FOREIGN KEY (dataset_key, parameter_code, native_unit, unit, conversion_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code, native_unit, unit, conversion_code);
```

### FK7 `seagis.forecast_run` → `seagis.forecast_value`

| Atribut | Definisi |
| --- | --- |
| Constraint | forecast_value_forecast_run_id_dataset_key_is_synthetic_fkey |
| Join | (forecast_run_id,dataset_key,is_synthetic) → (id,dataset_key,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Nilai parameter per run, grid dan valid time; tidak diduplikasi per plot. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241` |


```sql
FOREIGN KEY (forecast_run_id, dataset_key, is_synthetic) REFERENCES seagis.forecast_run(id, dataset_key, is_synthetic);
```

### FK8 `seagis.source_grid` → `seagis.forecast_value`

| Atribut | Definisi |
| --- | --- |
| Constraint | forecast_value_source_grid_id_dataset_key_is_synthetic_fkey |
| Join | (source_grid_id,dataset_key,is_synthetic) → (id,dataset_key,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Nilai parameter per run, grid dan valid time; tidak diduplikasi per plot. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241` |


```sql
FOREIGN KEY (source_grid_id, dataset_key, is_synthetic) REFERENCES seagis.source_grid(id, dataset_key, is_synthetic);
```

### FK9 `seagis.dataset` → `seagis.ingestion_run`

| Atribut | Definisi |
| --- | --- |
| Constraint | ingestion_run_dataset_key_fkey |
| Join | (dataset_key) → (dataset_key) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Audit satu ingestion logis beserta status penyelesaian. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:94` |


```sql
FOREIGN KEY (dataset_key) REFERENCES seagis.dataset(dataset_key);
```

### FK10 `seagis.dataset_parameter` → `seagis.observation`

| Atribut | Definisi |
| --- | --- |
| Constraint | observation_dataset_key_parameter_code_native_unit_unit_co_fkey |
| Join | (dataset_key,parameter_code,native_unit,unit,conversion_code) → (dataset_key,parameter_code,native_unit,unit,conversion_code) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Pembacaan suhu air sensor lokal, dengan nilai native, QC dan lineage raw. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184` |


```sql
FOREIGN KEY (dataset_key, parameter_code, native_unit, unit, conversion_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code, native_unit, unit, conversion_code);
```

### FK11 `seagis_raw.raw_payload` → `seagis.observation`

| Atribut | Definisi |
| --- | --- |
| Constraint | observation_raw_payload_id_ingestion_run_id_dataset_key_is_fkey |
| Join | (raw_payload_id,ingestion_run_id,dataset_key,is_synthetic) → (id,ingestion_run_id,dataset_key,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Pembacaan suhu air sensor lokal, dengan nilai native, QC dan lineage raw. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184` |


```sql
FOREIGN KEY (raw_payload_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis_raw.raw_payload(id, ingestion_run_id, dataset_key, is_synthetic);
```

### FK12 `seagis.sensor` → `seagis.observation`

| Atribut | Definisi |
| --- | --- |
| Constraint | observation_sensor_id_plot_id_dataset_key_is_synthetic_fkey |
| Join | (sensor_id,plot_id,dataset_key,is_synthetic) → (id,plot_id,dataset_key,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Pembacaan suhu air sensor lokal, dengan nilai native, QC dan lineage raw. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184` |


```sql
FOREIGN KEY (sensor_id, plot_id, dataset_key, is_synthetic) REFERENCES seagis.sensor(id, plot_id, dataset_key, is_synthetic);
```

### FK13 `seagis.plot` → `seagis.plot_grid_mapping`

| Atribut | Definisi |
| --- | --- |
| Constraint | plot_grid_mapping_plot_id_is_synthetic_fkey |
| Join | (plot_id,is_synthetic) → (id,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Pemetaan operasional plot ke grid dengan waktu efektif dan waktu tercatat. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:152` |


```sql
FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot(id, is_synthetic);
```

### FK14 `seagis.source_grid` → `seagis.plot_grid_mapping`

| Atribut | Definisi |
| --- | --- |
| Constraint | plot_grid_mapping_source_grid_id_fkey |
| Join | (source_grid_id) → (id) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Pemetaan operasional plot ke grid dengan waktu efektif dan waktu tercatat. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:152` |


```sql
FOREIGN KEY (source_grid_id) REFERENCES seagis.source_grid(id);
```

### FK15 `seagis.forecast_value` → `seagis.quality_event`

| Atribut | Definisi |
| --- | --- |
| Constraint | quality_event_forecast_value_id_dataset_key_is_synthetic_fkey |
| Join | (forecast_value_id,dataset_key,is_synthetic) → (id,dataset_key,is_synthetic) |
| Cardinality | 1:0..N; child → parent 0..1 |
| Optional | true |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Log QC append-only untuk ingestion atau satu measurement. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:273` |


```sql
FOREIGN KEY (forecast_value_id, dataset_key, is_synthetic) REFERENCES seagis.forecast_value(id, dataset_key, is_synthetic);
```

### FK16 `seagis.ingestion_run` → `seagis.quality_event`

| Atribut | Definisi |
| --- | --- |
| Constraint | quality_event_ingestion_run_id_dataset_key_is_synthetic_fkey |
| Join | (ingestion_run_id,dataset_key,is_synthetic) → (id,dataset_key,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Log QC append-only untuk ingestion atau satu measurement. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:273` |


```sql
FOREIGN KEY (ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.ingestion_run(id, dataset_key, is_synthetic);
```

### FK17 `seagis.observation` → `seagis.quality_event`

| Atribut | Definisi |
| --- | --- |
| Constraint | quality_event_observation_id_ingestion_run_id_dataset_key__fkey |
| Join | (observation_id,ingestion_run_id,dataset_key,is_synthetic) → (id,ingestion_run_id,dataset_key,is_synthetic) |
| Cardinality | 1:0..N; child → parent 0..1 |
| Optional | true |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Log QC append-only untuk ingestion atau satu measurement. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:273` |


```sql
FOREIGN KEY (observation_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.observation(id, ingestion_run_id, dataset_key, is_synthetic);
```

### FK18 `seagis.dataset_parameter` → `seagis.sensor`

| Atribut | Definisi |
| --- | --- |
| Constraint | sensor_dataset_key_parameter_code_fkey |
| Join | (dataset_key,parameter_code) → (dataset_key,parameter_code) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Identitas deployment sensor suhu, plot, kedalaman dan status aktif. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:73` |


```sql
FOREIGN KEY (dataset_key, parameter_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code);
```

### FK19 `seagis.dataset` → `seagis.sensor`

| Atribut | Definisi |
| --- | --- |
| Constraint | sensor_dataset_key_scope_fkey |
| Join | (dataset_key,scope) → (dataset_key,scope) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Identitas deployment sensor suhu, plot, kedalaman dan status aktif. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:73` |


```sql
FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset(dataset_key, scope);
```

### FK20 `seagis.plot` → `seagis.sensor`

| Atribut | Definisi |
| --- | --- |
| Constraint | sensor_plot_id_is_synthetic_fkey |
| Join | (plot_id,is_synthetic) → (id,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Identitas deployment sensor suhu, plot, kedalaman dan status aktif. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:73` |


```sql
FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot(id, is_synthetic);
```

### FK21 `seagis.dataset` → `seagis.source_grid`

| Atribut | Definisi |
| --- | --- |
| Constraint | source_grid_dataset_key_scope_fkey |
| Join | (dataset_key,scope) → (dataset_key,scope) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Identitas sel regional dan layer kedalaman; bukan plot budidaya. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:135` |


```sql
FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset(dataset_key, scope);
```

### FK22 `seagis.sensor` → `seagis_api.credential`

| Atribut | Definisi |
| --- | --- |
| Constraint | credential_sensor_id_fkey |
| Join | (sensor_id) → (id) |
| Cardinality | 1:0..N; child → parent 0..1 |
| Optional | true |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Identitas aktor API berupa hash token, masa berlaku dan pencabutan. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:27` |


```sql
FOREIGN KEY (sensor_id) REFERENCES seagis.sensor(id);
```

### FK23 `seagis.ingestion_run` → `seagis_api.packet_receipt`

| Atribut | Definisi |
| --- | --- |
| Constraint | packet_receipt_ingestion_run_id_fkey |
| Join | (ingestion_run_id) → (id) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Kunci idempotensi paket sensor dan digest semantik. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:53` |


```sql
FOREIGN KEY (ingestion_run_id) REFERENCES seagis.ingestion_run(id);
```

### FK24 `seagis.observation` → `seagis_api.packet_receipt`

| Atribut | Definisi |
| --- | --- |
| Constraint | packet_receipt_observation_id_fkey |
| Join | (observation_id) → (id) |
| Cardinality | 1:0..1; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Kunci idempotensi paket sensor dan digest semantik. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:53` |


```sql
FOREIGN KEY (observation_id) REFERENCES seagis.observation(id);
```

### FK25 `seagis.sensor` → `seagis_api.packet_receipt`

| Atribut | Definisi |
| --- | --- |
| Constraint | packet_receipt_sensor_id_fkey |
| Join | (sensor_id) → (id) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Kunci idempotensi paket sensor dan digest semantik. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:53` |


```sql
FOREIGN KEY (sensor_id) REFERENCES seagis.sensor(id);
```

### FK26 `seagis_api.credential` → `seagis_api.reader_plot`

| Atribut | Definisi |
| --- | --- |
| Constraint | reader_plot_credential_id_fkey |
| Join | (credential_id) → (id) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Daftar plot yang boleh dibaca satu credential reader. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:39` |


```sql
FOREIGN KEY (credential_id) REFERENCES seagis_api.credential(id);
```

### FK27 `seagis.plot` → `seagis_api.reader_plot`

| Atribut | Definisi |
| --- | --- |
| Constraint | reader_plot_plot_id_fkey |
| Join | (plot_id) → (id) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Daftar plot yang boleh dibaca satu credential reader. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:39` |


```sql
FOREIGN KEY (plot_id) REFERENCES seagis.plot(id);
```

### FK28 `seagis_api.credential` → `seagis_api.request_event`

| Atribut | Definisi |
| --- | --- |
| Constraint | request_event_credential_id_fkey |
| Join | (credential_id) → (id) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Audit respons API terautentikasi dan dasar rate limit. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:44` |


```sql
FOREIGN KEY (credential_id) REFERENCES seagis_api.credential(id);
```

### FK29 `seagis.sensor` → `seagis_api.request_event`

| Atribut | Definisi |
| --- | --- |
| Constraint | request_event_sensor_id_fkey |
| Join | (sensor_id) → (id) |
| Cardinality | 1:0..N; child → parent 0..1 |
| Optional | true |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Audit respons API terautentikasi dan dasar rate limit. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:44` |


```sql
FOREIGN KEY (sensor_id) REFERENCES seagis.sensor(id);
```

### FK30 `seagis_environment.policy` → `seagis_environment.attempt`

| Atribut | Definisi |
| --- | --- |
| Constraint | attempt_dataset_key_fkey |
| Join | (dataset_key) → (dataset_key) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Audit satu upaya fetch termasuk duplicate dan abandoned. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:57` |


```sql
FOREIGN KEY (dataset_key) REFERENCES seagis_environment.policy(dataset_key);
```

### FK31 `seagis.forecast_run` → `seagis_environment.attempt`

| Atribut | Definisi |
| --- | --- |
| Constraint | attempt_forecast_run_id_fkey |
| Join | (forecast_run_id) → (id) |
| Cardinality | 1:0..N; child → parent 0..1 |
| Optional | true |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Audit satu upaya fetch termasuk duplicate dan abandoned. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:57` |


```sql
FOREIGN KEY (forecast_run_id) REFERENCES seagis.forecast_run(id);
```

### FK32 `seagis_environment.policy` → `seagis_environment.demo_grid_mapping`

| Atribut | Definisi |
| --- | --- |
| Constraint | demo_grid_mapping_dataset_key_fkey |
| Join | (dataset_key) → (dataset_key) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Bridge khusus dua plot fiktif ke grid nyata untuk preview, bukan otorisasi training. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:69` |


```sql
FOREIGN KEY (dataset_key) REFERENCES seagis_environment.policy(dataset_key);
```

### FK33 `seagis.plot` → `seagis_environment.demo_grid_mapping`

| Atribut | Definisi |
| --- | --- |
| Constraint | demo_grid_mapping_plot_id_plot_is_synthetic_fkey |
| Join | (plot_id,plot_is_synthetic) → (id,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Bridge khusus dua plot fiktif ke grid nyata untuk preview, bukan otorisasi training. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:69` |


```sql
FOREIGN KEY (plot_id, plot_is_synthetic) REFERENCES seagis.plot(id, is_synthetic);
```

### FK34 `seagis.source_grid` → `seagis_environment.demo_grid_mapping`

| Atribut | Definisi |
| --- | --- |
| Constraint | demo_grid_mapping_source_grid_id_dataset_key_grid_is_synth_fkey |
| Join | (source_grid_id,dataset_key,grid_is_synthetic) → (id,dataset_key,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Bridge khusus dua plot fiktif ke grid nyata untuk preview, bukan otorisasi training. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:69` |


```sql
FOREIGN KEY (source_grid_id, dataset_key, grid_is_synthetic) REFERENCES seagis.source_grid(id, dataset_key, is_synthetic);
```

### FK35 `seagis.dataset` → `seagis_environment.policy`

| Atribut | Definisi |
| --- | --- |
| Constraint | policy_dataset_key_fkey |
| Join | (dataset_key) → (dataset_key) |
| Cardinality | 1:0..1; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Kebijakan fetch, lisensi, cadence scheduler, staleness dan retensi regional. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:16` |


```sql
FOREIGN KEY (dataset_key) REFERENCES seagis.dataset(dataset_key);
```

### FK36 `seagis_environment.policy` → `seagis_environment.schedule_state`

| Atribut | Definisi |
| --- | --- |
| Constraint | schedule_state_dataset_key_fkey |
| Join | (dataset_key) → (dataset_key) |
| Cardinality | 1:0..1; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | State mutable lease, due time, backoff dan keberhasilan terakhir. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:45` |


```sql
FOREIGN KEY (dataset_key) REFERENCES seagis_environment.policy(dataset_key);
```

### FK37 `seagis.forecast_run` → `seagis_environment.schedule_state`

| Atribut | Definisi |
| --- | --- |
| Constraint | schedule_state_last_forecast_run_id_fkey |
| Join | (last_forecast_run_id) → (id) |
| Cardinality | 1:0..N; child → parent 0..1 |
| Optional | true |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | State mutable lease, due time, backoff dan keberhasilan terakhir. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:45` |


```sql
FOREIGN KEY (last_forecast_run_id) REFERENCES seagis.forecast_run(id);
```

### FK38 `seagis.forecast_value` → `seagis_features.feature_input`

| Atribut | Definisi |
| --- | --- |
| Constraint | feature_input_forecast_value_id_fkey |
| Join | (forecast_value_id) → (id) |
| Cardinality | 1:0..N; child → parent 0..1 |
| Optional | true |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Lineage FK input feature snapshot dan guard cutoff. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:320` |


```sql
FOREIGN KEY (forecast_value_id) REFERENCES seagis.forecast_value(id);
```

### FK39 `seagis.observation` → `seagis_features.feature_input`

| Atribut | Definisi |
| --- | --- |
| Constraint | feature_input_observation_id_fkey |
| Join | (observation_id) → (id) |
| Cardinality | 1:0..N; child → parent 0..1 |
| Optional | true |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Lineage FK input feature snapshot dan guard cutoff. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:320` |


```sql
FOREIGN KEY (observation_id) REFERENCES seagis.observation(id);
```

### FK40 `seagis_features.feature_snapshot` → `seagis_features.feature_input`

| Atribut | Definisi |
| --- | --- |
| Constraint | feature_input_snapshot_id_fkey |
| Join | (snapshot_id) → (id) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Lineage FK input feature snapshot dan guard cutoff. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:320` |


```sql
FOREIGN KEY (snapshot_id) REFERENCES seagis_features.feature_snapshot(id);
```

### FK41 `seagis.plot` → `seagis_features.feature_snapshot`

| Atribut | Definisi |
| --- | --- |
| Constraint | feature_snapshot_plot_id_is_synthetic_fkey |
| Join | (plot_id,is_synthetic) → (id,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Container fitur draft/sealed dengan cutoff dan hash; builder produksi belum ditemukan. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:301` |


```sql
FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot(id, is_synthetic);
```

### FK42 `seagis.plot` → `seagis_quality.alignment_snapshot`

| Atribut | Definisi |
| --- | --- |
| Constraint | alignment_snapshot_plot_id_fkey |
| Join | (plot_id) → (id) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Dokumen QC/alignment hourly immutable; selalu training_authorized=false. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:21` |


```sql
FOREIGN KEY (plot_id) REFERENCES seagis.plot(id);
```

### FK43 `seagis_quality.policy` → `seagis_quality.alignment_snapshot`

| Atribut | Definisi |
| --- | --- |
| Constraint | alignment_snapshot_policy_version_fkey |
| Join | (policy_version) → (version) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Dokumen QC/alignment hourly immutable; selalu training_authorized=false. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:21` |


```sql
FOREIGN KEY (policy_version) REFERENCES seagis_quality.policy(version);
```

### FK44 `seagis.forecast_value` → `seagis_quality.snapshot_input`

| Atribut | Definisi |
| --- | --- |
| Constraint | snapshot_input_forecast_value_id_fkey |
| Join | (forecast_value_id) → (id) |
| Cardinality | 1:0..N; child → parent 0..1 |
| Optional | true |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Lineage measurement per jam alignment snapshot. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:35` |


```sql
FOREIGN KEY (forecast_value_id) REFERENCES seagis.forecast_value(id);
```

### FK45 `seagis.observation` → `seagis_quality.snapshot_input`

| Atribut | Definisi |
| --- | --- |
| Constraint | snapshot_input_observation_id_fkey |
| Join | (observation_id) → (id) |
| Cardinality | 1:0..N; child → parent 0..1 |
| Optional | true |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Lineage measurement per jam alignment snapshot. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:35` |


```sql
FOREIGN KEY (observation_id) REFERENCES seagis.observation(id);
```

### FK46 `seagis_quality.alignment_snapshot` → `seagis_quality.snapshot_input`

| Atribut | Definisi |
| --- | --- |
| Constraint | snapshot_input_snapshot_id_fkey |
| Join | (snapshot_id) → (id) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Lineage measurement per jam alignment snapshot. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:35` |


```sql
FOREIGN KEY (snapshot_id) REFERENCES seagis_quality.alignment_snapshot(id);
```

### FK47 `seagis.ingestion_run` → `seagis_raw.raw_payload`

| Atribut | Definisi |
| --- | --- |
| Constraint | raw_payload_ingestion_run_id_dataset_key_is_synthetic_fkey |
| Join | (ingestion_run_id,dataset_key,is_synthetic) → (id,dataset_key,is_synthetic) |
| Cardinality | 1:0..N; child → parent 1 |
| Optional | false |
| ON DELETE / ON UPDATE | NO ACTION / NO ACTION (default) |
| Meaning | Manifest raw immutable: digest, basis hash, lisensi dan mode retensi. |
| Risiko integritas | FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan. |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:110` |


```sql
FOREIGN KEY (ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.ingestion_run(id, dataset_key, is_synthetic);
```

Relasi logis tambahan: dua alias forecast_value di current_speed bergabung pada forecast_run_id, source_grid_id, valid_at; parameter_code membedakan u/v. Ini join view, bukan FK baru. source_ref memakai prefix typed dan CHECK serta dua FK alternatif; tidak dibuat FK ke string polimorfik. Tidak ditemukan self-reference FK. reader_plot, dataset_parameter, feature_input dan snapshot_input berperan sebagai association/lineage, dengan composite key/unique yang tercantum pada dictionary. Relasi Farmer→CultivationPlot berada di memori AppPOC dan tidak masuk 47 FK PostgreSQL.

ERD lengkap dan per schema terdapat pada modul architecture/ERD.md.

