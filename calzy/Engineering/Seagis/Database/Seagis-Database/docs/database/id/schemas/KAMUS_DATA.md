# KAMUS_DATA

Version: 1.0.0 | Date: 2026-10-27

[Dokumen lengkap](../DOKUMENTASI_DATABASE.md) | [README](../../README.md)

Domain seagis.finite_float adalah double precision yang menolak NaN dan infinity; NULL tetap diatur kolom. value_status present memerlukan angka; status nonpresent memerlukan null; valid_value/valid_support serta guard SQL menetapkan aturan lintas field. Presipitasi mm adalah total satu jam, salinitas 1e-3 tidak otomatis PSU/ppt, wind direction adalah arah dari dalam derajat. Metadata tipe/null/default/constraint/index berasal dari snapshot catalog 22 Oktober; definisi SQL diverifikasi terhadap rantai migrasi lokal 0001–0005. Baris view tidak memiliki PK/FK fisik walaupun field-nya berasal dari measurement. Contoh adalah ilustrasi sintetis dan belum tentu satu row INSERT yang valid. NOT APPLICABLE berarti atribut tidak relevan; UNVERIFIED berarti semantik atau derivasi spesifik belum dibuktikan.

### 4.1 `seagis.dataset`

Identitas dataset, versi, cadence, lisensi dan gate ingestion.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis |
| Kind | table |
| Primary key | PRIMARY KEY (dataset_key) |
| Unique | UNIQUE (dataset_key, scope) |
| Rows | UNVERIFIED |
| Writer | supabase/seed.sql; scripts/provision_a1.py; scripts/deploy_a2.py |
| Reader | A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:17` |

#### `seagis.dataset.dataset_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Kunci dataset terdaftar |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:511` → `'sensor_temperature_v1'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:17`; catalog seagis.dataset.dataset_key |

#### `seagis.dataset.source_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (source_key) REFERENCES seagis.source(source_key) |
| Arti bisnis / teknis | Kunci penyedia sumber |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:511` → `'sensor'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:17`; catalog seagis.dataset.source_key |

#### `seagis.dataset.provider_product_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas produk penyedia bila tersedia |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:511` → `NULL` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:17`; catalog seagis.dataset.provider_product_id |

#### `seagis.dataset.provider_dataset_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas dataset asli penyedia |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:511` → `'seagis-water-temperature'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:17`; catalog seagis.dataset.provider_dataset_id |

#### `seagis.dataset.dataset_version`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Versi dataset yang dipin |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:511` → `'v1'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:17`; catalog seagis.dataset.dataset_version |

#### `seagis.dataset.scope`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Asal local_sensor atau regional_model |
| Valid values / checks | CHECK (scope = ANY (ARRAY['local_sensor'::text, 'regional_model'::text])) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:511` → `'local_sensor'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:17`; catalog seagis.dataset.scope |

#### `seagis.dataset.native_cadence_seconds`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `integer` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Jarak waktu asli sampel, bukan interval fetch |
| Valid values / checks | CHECK (native_cadence_seconds > 0) |
| Units / time | s; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:511` → `3600` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:17`; catalog seagis.dataset.native_cadence_seconds |

#### `seagis.dataset.resolution_lat_deg`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `seagis.finite_float` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Resolusi latitude dalam derajat bila diketahui |
| Valid values / checks | CHECK (resolution_lat_deg::double precision > 0::double precision) |
| Units / time | degree; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:511` → `NULL` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:17`; catalog seagis.dataset.resolution_lat_deg |

#### `seagis.dataset.resolution_lon_deg`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `seagis.finite_float` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Resolusi longitude dalam derajat bila diketahui |
| Valid values / checks | CHECK (resolution_lon_deg::double precision > 0::double precision) |
| Units / time | degree; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:511` → `NULL` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:17`; catalog seagis.dataset.resolution_lon_deg |

#### `seagis.dataset.source_timezone`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | `'UTC'::text` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Konteks zona waktu asal |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | caller / SQL default → `'UTC'::text` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:17`; catalog seagis.dataset.source_timezone |

#### `seagis.dataset.licence_url`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Referensi lisensi sumber |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:511` → `'project-owned://sensor-data'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:17`; catalog seagis.dataset.licence_url |

#### `seagis.dataset.attribution`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Teks atribusi yang harus dipertahankan |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:511` → `'SEAGIS; simulated until hardware commissioning'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:17`; catalog seagis.dataset.attribution |

#### `seagis.dataset.raw_storage_permitted`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `boolean` / false |
| Default / generated | `false` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Gate izin menyimpan raw, bukan jaminan objek telah disimpan |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | true |
| Asal / transformasi | caller / SQL default → `false` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:17`; catalog seagis.dataset.raw_storage_permitted |

#### `seagis.dataset.real_ingestion_enabled`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `boolean` / false |
| Default / generated | `false` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Gate ingestion data nonsintetis |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | true |
| Asal / transformasi | caller / SQL default → `false` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:17`; catalog seagis.dataset.real_ingestion_enabled |

#### `seagis.dataset.metadata_checked_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Waktu metadata sumber diperiksa |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:511` → `'2026-10-21T00:00:00Z'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:17`; catalog seagis.dataset.metadata_checked_at |

#### Constraint, indeks dan trigger

**constraints**

```sql
UNIQUE (dataset_key, scope);
CHECK (native_cadence_seconds > 0);
PRIMARY KEY (dataset_key);
CHECK (resolution_lat_deg::double precision > 0::double precision);
CHECK (resolution_lon_deg::double precision > 0::double precision);
CHECK (scope = ANY (ARRAY['local_sensor'::text, 'regional_model'::text]));
FOREIGN KEY (source_key) REFERENCES seagis.source(source_key);
```

**indexes**

```sql
CREATE UNIQUE INDEX dataset_dataset_key_scope_key ON seagis.dataset USING btree (dataset_key, scope);
CREATE UNIQUE INDEX dataset_pkey ON seagis.dataset USING btree (dataset_key);
```

**triggers**

```sql
CREATE TRIGGER guard_dataset_identity BEFORE UPDATE ON seagis.dataset FOR EACH ROW EXECUTE FUNCTION seagis.guard_dataset_identity();
```

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.2 `seagis.dataset_parameter`

Kontrak variabel sumber ke parameter dan aturan konversi.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis |
| Kind | table |
| Primary key | PRIMARY KEY (dataset_key, parameter_code) |
| Unique | UNIQUE (dataset_key, parameter_code, native_unit, unit, conversion_code) |
| Rows | UNVERIFIED |
| Writer | supabase/seed.sql; scripts/provision_a1.py; scripts/deploy_a2.py |
| Reader | A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:43` |

#### `seagis.dataset_parameter.dataset_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | true / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key) REFERENCES seagis.dataset(dataset_key) |
| Arti bisnis / teknis | Kunci dataset terdaftar |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:532` → `'sensor_temperature_v1'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:43`; catalog seagis.dataset_parameter.dataset_key |

#### `seagis.dataset_parameter.parameter_code`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | true / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (parameter_code, unit) REFERENCES seagis.parameter(parameter_code, unit) |
| Arti bisnis / teknis | Identitas parameter lingkungan |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:532` → `'water_temperature'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:43`; catalog seagis.dataset_parameter.parameter_code |

#### `seagis.dataset_parameter.source_variable`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Nama variabel asli provider |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:532` → `'water_temperature'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:43`; catalog seagis.dataset_parameter.source_variable |

#### `seagis.dataset_parameter.native_unit`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Satuan asli sebelum normalisasi |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:532` → `'degC'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:43`; catalog seagis.dataset_parameter.native_unit |

#### `seagis.dataset_parameter.unit`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (parameter_code, unit) REFERENCES seagis.parameter(parameter_code, unit) |
| Arti bisnis / teknis | Satuan nilai normalisasi menurut registri |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:532` → `'degC'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:43`; catalog seagis.dataset_parameter.unit |

#### `seagis.dataset_parameter.conversion_code`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas metode konversi satuan |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:532` → `'identity'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:43`; catalog seagis.dataset_parameter.conversion_code |

#### `seagis.dataset_parameter.conversion_factor`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `seagis.finite_float` / false |
| Default / generated | `1` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Pengali pada value=native_value*factor+offset |
| Valid values / checks | CHECK (conversion_factor::double precision <> 0::double precision) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | caller / SQL default → `1` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:43`; catalog seagis.dataset_parameter.conversion_factor |

#### `seagis.dataset_parameter.conversion_offset`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `seagis.finite_float` / false |
| Default / generated | `0` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Offset setelah perkalian faktor |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | caller / SQL default → `0` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:43`; catalog seagis.dataset_parameter.conversion_offset |

#### `seagis.dataset_parameter.temporal_support`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Dukungan waktu instantaneous, mean atau sum |
| Valid values / checks | CHECK (temporal_support = ANY (ARRAY['instantaneous'::text, 'mean'::text, 'sum'::text])) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:532` → `'instantaneous'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:43`; catalog seagis.dataset_parameter.temporal_support |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK (conversion_factor::double precision <> 0::double precision);
FOREIGN KEY (dataset_key) REFERENCES seagis.dataset(dataset_key);
UNIQUE (dataset_key, parameter_code, native_unit, unit, conversion_code);
FOREIGN KEY (parameter_code, unit) REFERENCES seagis.parameter(parameter_code, unit);
PRIMARY KEY (dataset_key, parameter_code);
CHECK (temporal_support = ANY (ARRAY['instantaneous'::text, 'mean'::text, 'sum'::text]));
```

**indexes**

```sql
CREATE UNIQUE INDEX dataset_parameter_dataset_key_parameter_code_native_unit_un_key ON seagis.dataset_parameter USING btree (dataset_key, parameter_code, native_unit, unit, conversion_code);
CREATE UNIQUE INDEX dataset_parameter_pkey ON seagis.dataset_parameter USING btree (dataset_key, parameter_code);
```

**triggers**

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis.dataset_parameter FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
```

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.3 `seagis.forecast_run`

Capture/vintage model regional; waktu publikasi yang tidak diketahui tetap null.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis |
| Kind | table |
| Primary key | PRIMARY KEY (id) |
| Unique | UNIQUE (dataset_key, run_key); UNIQUE (id, dataset_key, is_synthetic) |
| Rows | UNVERIFIED |
| Writer | seagis_environment.persist; A0 fixtures |
| Reader | seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:216` |

#### `seagis.forecast_run.id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | `gen_random_uuid()` |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas baris menurut PK tabel |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | DB default / explicit UUID → `gen_random_uuid()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:216`; catalog seagis.forecast_run.id |

#### `seagis.forecast_run.dataset_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset(dataset_key, scope); FOREIGN KEY (raw_payload_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis_raw.raw_payload(id, ingestion_run_id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Kunci dataset terdaftar |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:168` → `s.dataset_key` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:216`; catalog seagis.forecast_run.dataset_key |

#### `seagis.forecast_run.scope`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | `'regional_model'::text` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset(dataset_key, scope) |
| Arti bisnis / teknis | Asal local_sensor atau regional_model |
| Valid values / checks | CHECK (scope = 'regional_model'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | caller / SQL default → `'regional_model'::text` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:216`; catalog seagis.forecast_run.scope |

#### `seagis.forecast_run.ingestion_run_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (raw_payload_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis_raw.raw_payload(id, ingestion_run_id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Referensi ingestion asal |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:168` → `ing` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:216`; catalog seagis.forecast_run.ingestion_run_id |

#### `seagis.forecast_run.raw_payload_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (raw_payload_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis_raw.raw_payload(id, ingestion_run_id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Referensi manifest raw asal |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:168` → `raw_id` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:216`; catalog seagis.forecast_run.raw_payload_id |

#### `seagis.forecast_run.is_synthetic`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `boolean` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (raw_payload_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis_raw.raw_payload(id, ingestion_run_id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Penanda asal sintetis, terpisah dari QC |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | true |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:168` → `false` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:216`; catalog seagis.forecast_run.is_synthetic |

#### `seagis.forecast_run.run_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas capture semantik per dataset |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:168` → `batch->>'run_key'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:216`; catalog seagis.forecast_run.run_key |

#### `seagis.forecast_run.run_kind`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | forecast, analysis atau analysis_forecast_unspecified |
| Valid values / checks | CHECK (run_kind = ANY (ARRAY['forecast'::text, 'analysis'::text, 'analysis_forecast_unspecified'::text])) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:168` → `CASE WHEN d.source_key='copernicus' THEN 'analysis_forecast_unspecified' ELSE 'forecast' END` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:216`; catalog seagis.forecast_run.run_kind |

#### `seagis.forecast_run.provider_run_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | ID run provider jika benar-benar tersedia |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | active loader omits column / nullable schema → `NULL in inspected A1/A2 path; other callers may supply under schema guards` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:216`; catalog seagis.forecast_run.provider_run_id |

#### `seagis.forecast_run.model_initialized_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan inisialisasi model jika diketahui |
| Valid values / checks | CHECK (model_initialized_at IS NULL OR model_initialized_at <= ingested_at) |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | active loader omits column / nullable schema → `NULL in inspected A1/A2 path; other callers may supply under schema guards` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:216`; catalog seagis.forecast_run.model_initialized_at |

#### `seagis.forecast_run.issued_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan publikasi provider terverifikasi; null jika tidak diketahui |
| Valid values / checks | CHECK ((issue_time_basis = 'unknown'::text) = (issued_at IS NULL)); CHECK (issued_at IS NULL OR issued_at <= ingested_at) |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | active loader omits column / nullable schema → `NULL in inspected A1/A2 path; other callers may supply under schema guards` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:216`; catalog seagis.forecast_run.issued_at |

#### `seagis.forecast_run.issue_time_basis`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Dasar known/unknown waktu publikasi |
| Valid values / checks | CHECK ((issue_time_basis = 'unknown'::text) = (issued_at IS NULL)); CHECK (issue_time_basis = ANY (ARRAY['provider_verified'::text, 'unknown'::text])) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:168` → `'unknown'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:216`; catalog seagis.forecast_run.issue_time_basis |

#### `seagis.forecast_run.ingested_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan data tersedia bagi sistem |
| Valid values / checks | CHECK (issued_at IS NULL OR issued_at <= ingested_at); CHECK (model_initialized_at IS NULL OR model_initialized_at <= ingested_at) |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:168` → `t` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:216`; catalog seagis.forecast_run.ingested_at |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK ((issue_time_basis = 'unknown'::text) = (issued_at IS NULL));
CHECK (issued_at IS NULL OR issued_at <= ingested_at);
CHECK (model_initialized_at IS NULL OR model_initialized_at <= ingested_at);
UNIQUE (dataset_key, run_key);
FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset(dataset_key, scope);
UNIQUE (id, dataset_key, is_synthetic);
CHECK (issue_time_basis = ANY (ARRAY['provider_verified'::text, 'unknown'::text]));
PRIMARY KEY (id);
FOREIGN KEY (raw_payload_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis_raw.raw_payload(id, ingestion_run_id, dataset_key, is_synthetic);
CHECK (run_kind = ANY (ARRAY['forecast'::text, 'analysis'::text, 'analysis_forecast_unspecified'::text]));
CHECK (scope = 'regional_model'::text);
```

**indexes**

```sql
CREATE INDEX forecast_run_asof ON seagis.forecast_run USING btree (dataset_key, ingested_at DESC);
CREATE UNIQUE INDEX forecast_run_dataset_key_run_key_key ON seagis.forecast_run USING btree (dataset_key, run_key);
CREATE UNIQUE INDEX forecast_run_id_dataset_key_is_synthetic_key ON seagis.forecast_run USING btree (id, dataset_key, is_synthetic);
CREATE UNIQUE INDEX forecast_run_pkey ON seagis.forecast_run USING btree (id);
```

**triggers**

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis.forecast_run FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
CREATE TRIGGER guard_run BEFORE INSERT ON seagis.forecast_run FOR EACH ROW EXECUTE FUNCTION seagis.guard_run();
```

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.4 `seagis.forecast_value`

Nilai parameter per run, grid dan valid time; tidak diduplikasi per plot.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis |
| Kind | table |
| Primary key | PRIMARY KEY (id) |
| Unique | UNIQUE (forecast_run_id, source_grid_id, parameter_code, valid_at); UNIQUE (id, dataset_key, is_synthetic) |
| Rows | UNVERIFIED |
| Writer | seagis_environment.persist; A0 fixtures |
| Reader | seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241` |

#### `seagis.forecast_value.id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | `gen_random_uuid()` |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas baris menurut PK tabel |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | DB default / explicit UUID → `gen_random_uuid()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241`; catalog seagis.forecast_value.id |

#### `seagis.forecast_value.forecast_run_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (forecast_run_id, dataset_key, is_synthetic) REFERENCES seagis.forecast_run(id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Referensi capture/vintage model regional |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | A2 adapter batch → `persist run_id` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241`; catalog seagis.forecast_value.forecast_run_id |

#### `seagis.forecast_value.source_grid_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (source_grid_id, dataset_key, is_synthetic) REFERENCES seagis.source_grid(id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Referensi sel regional dan layer |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | A2 adapter batch → `grid lookup by dataset/key/synthetic` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241`; catalog seagis.forecast_value.source_grid_id |

#### `seagis.forecast_value.dataset_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key, parameter_code, native_unit, unit, conversion_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code, native_unit, unit, conversion_code); FOREIGN KEY (forecast_run_id, dataset_key, is_synthetic) REFERENCES seagis.forecast_run(id, dataset_key, is_synthetic); FOREIGN KEY (source_grid_id, dataset_key, is_synthetic) REFERENCES seagis.source_grid(id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Kunci dataset terdaftar |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A2 adapter batch → `leased dataset` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241`; catalog seagis.forecast_value.dataset_key |

#### `seagis.forecast_value.is_synthetic`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `boolean` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (forecast_run_id, dataset_key, is_synthetic) REFERENCES seagis.forecast_run(id, dataset_key, is_synthetic); FOREIGN KEY (source_grid_id, dataset_key, is_synthetic) REFERENCES seagis.source_grid(id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Penanda asal sintetis, terpisah dari QC |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | true |
| Asal / transformasi | A2 adapter batch → `false` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241`; catalog seagis.forecast_value.is_synthetic |

#### `seagis.forecast_value.parameter_code`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key, parameter_code, native_unit, unit, conversion_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code, native_unit, unit, conversion_code) |
| Arti bisnis / teknis | Identitas parameter lingkungan |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A2 adapter batch → `batch.values[].parameter` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241`; catalog seagis.forecast_value.parameter_code |

#### `seagis.forecast_value.native_value`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `seagis.finite_float` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Nilai fisik dalam satuan sumber |
| Valid values / checks | CHECK (seagis.valid_value(value::double precision, native_value::double precision, value_status, detection_limit::double precision)) |
| Units / time | Mengikuti unit/native_unit dan dataset_parameter; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | A2 adapter batch → `batch.values[].value` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241`; catalog seagis.forecast_value.native_value |

#### `seagis.forecast_value.native_unit`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key, parameter_code, native_unit, unit, conversion_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code, native_unit, unit, conversion_code) |
| Arti bisnis / teknis | Satuan asli sebelum normalisasi |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | registered seagis.dataset_parameter par → `par.native_unit` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241`; catalog seagis.forecast_value.native_unit |

#### `seagis.forecast_value.value`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `seagis.finite_float` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Nilai normalisasi; null mengikuti value_status |
| Valid values / checks | CHECK (seagis.valid_value(value::double precision, native_value::double precision, value_status, detection_limit::double precision)) |
| Units / time | Mengikuti unit/native_unit dan dataset_parameter; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | A2 adapter batch → `batch.values[].value` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241`; catalog seagis.forecast_value.value |

#### `seagis.forecast_value.unit`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key, parameter_code, native_unit, unit, conversion_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code, native_unit, unit, conversion_code) |
| Arti bisnis / teknis | Satuan nilai normalisasi menurut registri |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | registered seagis.dataset_parameter par → `par.unit` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241`; catalog seagis.forecast_value.unit |

#### `seagis.forecast_value.conversion_code`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key, parameter_code, native_unit, unit, conversion_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code, native_unit, unit, conversion_code) |
| Arti bisnis / teknis | Identitas metode konversi satuan |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | registered seagis.dataset_parameter par → `par.conversion_code` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241`; catalog seagis.forecast_value.conversion_code |

#### `seagis.forecast_value.value_status`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Ketersediaan angka, terpisah dari kualitas |
| Valid values / checks | CHECK (seagis.valid_value(value::double precision, native_value::double precision, value_status, detection_limit::double precision)) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A2 adapter batch → `v.value_status` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241`; catalog seagis.forecast_value.value_status |

#### `seagis.forecast_value.detection_limit`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `seagis.finite_float` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Batas deteksi pada satuan normalisasi bila relevan |
| Valid values / checks | CHECK (seagis.valid_value(value::double precision, native_value::double precision, value_status, detection_limit::double precision)) |
| Units / time | Mengikuti unit/native_unit dan dataset_parameter; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | A2 adapter batch → `omitted -> SQL NULL` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241`; catalog seagis.forecast_value.detection_limit |

#### `seagis.forecast_value.valid_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Waktu representatif nilai model |
| Valid values / checks | CHECK (seagis.valid_support(valid_at, temporal_support, interval_status, period_start_at, period_end_at)) |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | A2 adapter batch → `v.valid_at::timestamptz` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241`; catalog seagis.forecast_value.valid_at |

#### `seagis.forecast_value.ingested_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan data tersedia bagi sistem |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | A2 adapter batch → `persist t = clock_timestamp()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241`; catalog seagis.forecast_value.ingested_at |

#### `seagis.forecast_value.temporal_support`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Dukungan waktu instantaneous, mean atau sum |
| Valid values / checks | CHECK (seagis.valid_support(valid_at, temporal_support, interval_status, period_start_at, period_end_at)) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | registered seagis.dataset_parameter par → `par.temporal_support` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241`; catalog seagis.forecast_value.temporal_support |

#### `seagis.forecast_value.interval_status`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | known, unknown atau not_applicable untuk interval |
| Valid values / checks | CHECK (seagis.valid_support(valid_at, temporal_support, interval_status, period_start_at, period_end_at)) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A2 adapter batch → `v.interval_status` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241`; catalog seagis.forecast_value.interval_status |

#### `seagis.forecast_value.period_start_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Awal interval mean/sum jika diketahui |
| Valid values / checks | CHECK (seagis.valid_support(valid_at, temporal_support, interval_status, period_start_at, period_end_at)) |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | A2 adapter batch → `v.period_start_at::timestamptz` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241`; catalog seagis.forecast_value.period_start_at |

#### `seagis.forecast_value.period_end_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Akhir interval mean/sum jika diketahui |
| Valid values / checks | CHECK (seagis.valid_support(valid_at, temporal_support, interval_status, period_start_at, period_end_at)) |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | A2 adapter batch → `v.period_end_at::timestamptz` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241`; catalog seagis.forecast_value.period_end_at |

#### `seagis.forecast_value.quality_status`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Status QC unreviewed, accepted, suspect atau rejected; bukan diagnosis |
| Valid values / checks | CHECK (quality_status = ANY (ARRAY['unreviewed'::text, 'accepted'::text, 'suspect'::text, 'rejected'::text])) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A2 adapter batch → `default unreviewed` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241`; catalog seagis.forecast_value.quality_status |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK (seagis.valid_value(value::double precision, native_value::double precision, value_status, detection_limit::double precision));
CHECK (seagis.valid_support(valid_at, temporal_support, interval_status, period_start_at, period_end_at));
FOREIGN KEY (dataset_key, parameter_code, native_unit, unit, conversion_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code, native_unit, unit, conversion_code);
FOREIGN KEY (forecast_run_id, dataset_key, is_synthetic) REFERENCES seagis.forecast_run(id, dataset_key, is_synthetic);
UNIQUE (forecast_run_id, source_grid_id, parameter_code, valid_at);
UNIQUE (id, dataset_key, is_synthetic);
PRIMARY KEY (id);
CHECK (quality_status = ANY (ARRAY['unreviewed'::text, 'accepted'::text, 'suspect'::text, 'rejected'::text]));
FOREIGN KEY (source_grid_id, dataset_key, is_synthetic) REFERENCES seagis.source_grid(id, dataset_key, is_synthetic);
```

**indexes**

```sql
CREATE INDEX forecast_grid_time ON seagis.forecast_value USING btree (source_grid_id, parameter_code, valid_at DESC);
CREATE UNIQUE INDEX forecast_value_forecast_run_id_source_grid_id_parameter_cod_key ON seagis.forecast_value USING btree (forecast_run_id, source_grid_id, parameter_code, valid_at);
CREATE UNIQUE INDEX forecast_value_id_dataset_key_is_synthetic_key ON seagis.forecast_value USING btree (id, dataset_key, is_synthetic);
CREATE UNIQUE INDEX forecast_value_pkey ON seagis.forecast_value USING btree (id);
```

**triggers**

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis.forecast_value FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
CREATE TRIGGER guard_forecast_value BEFORE INSERT ON seagis.forecast_value FOR EACH ROW EXECUTE FUNCTION seagis.guard_measurement();
```

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.5 `seagis.ingestion_run`

Audit satu ingestion logis beserta status penyelesaian.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis |
| Kind | table |
| Primary key | PRIMARY KEY (id) |
| Unique | UNIQUE (dataset_key, request_key); UNIQUE (id, dataset_key, is_synthetic) |
| Rows | UNVERIFIED |
| Writer | seagis_api.ingest; seagis_environment.persist; A0 fixtures |
| Reader | A3 source_bundle; provenance guards |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:94` |

#### `seagis.ingestion_run.id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | `gen_random_uuid()` |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas baris menurut PK tabel |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | DB default / explicit UUID → `gen_random_uuid()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:94`; catalog seagis.ingestion_run.id |

#### `seagis.ingestion_run.dataset_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key) REFERENCES seagis.dataset(dataset_key) |
| Arti bisnis / teknis | Kunci dataset terdaftar |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:191` → `s.dataset_key` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:94`; catalog seagis.ingestion_run.dataset_key |

#### `seagis.ingestion_run.request_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Kunci logis retry ingestion per dataset |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:191` → `'a1:'&#124;&#124;s.id&#124;&#124;':'&#124;&#124;key` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:94`; catalog seagis.ingestion_run.request_key |

#### `seagis.ingestion_run.adapter_version`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Versi implementasi adapter ingestion |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:191` → `'temperature-1.0.0'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:94`; catalog seagis.ingestion_run.adapter_version |

#### `seagis.ingestion_run.started_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan dimulainya ingestion atau attempt |
| Valid values / checks | CHECK (completed_at IS NULL OR completed_at >= started_at) |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:191` → `received` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:94`; catalog seagis.ingestion_run.started_at |

#### `seagis.ingestion_run.completed_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan selesai; null selama running |
| Valid values / checks | CHECK (completed_at IS NULL OR completed_at >= started_at); CHECK ((status = 'running'::text) = (completed_at IS NULL)) |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | owning routine / caller → `UPDATE at end of A1/A2: clock_timestamp(); NULL while running` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:94`; catalog seagis.ingestion_run.completed_at |

#### `seagis.ingestion_run.status`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | running/succeeded/failed/partial beserta completed_at |
| Valid values / checks | CHECK ((status = 'running'::text) = (completed_at IS NULL)); CHECK (status = ANY (ARRAY['running'::text, 'succeeded'::text, 'partial'::text, 'failed'::text])) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:191` → `'running'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:94`; catalog seagis.ingestion_run.status |

#### `seagis.ingestion_run.is_synthetic`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `boolean` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Penanda asal sintetis, terpisah dari QC |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | true |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:191` → `s.is_synthetic` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:94`; catalog seagis.ingestion_run.is_synthetic |

#### `seagis.ingestion_run.error_code`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Kode kegagalan tersanitasi |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | owning routine / caller → `A1/A2 successful rows omit -> NULL; failure codes tracked in environment.attempt` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:94`; catalog seagis.ingestion_run.error_code |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK (completed_at IS NULL OR completed_at >= started_at);
CHECK ((status = 'running'::text) = (completed_at IS NULL));
FOREIGN KEY (dataset_key) REFERENCES seagis.dataset(dataset_key);
UNIQUE (dataset_key, request_key);
UNIQUE (id, dataset_key, is_synthetic);
PRIMARY KEY (id);
CHECK (status = ANY (ARRAY['running'::text, 'succeeded'::text, 'partial'::text, 'failed'::text]));
```

**indexes**

```sql
CREATE UNIQUE INDEX ingestion_run_dataset_key_request_key_key ON seagis.ingestion_run USING btree (dataset_key, request_key);
CREATE UNIQUE INDEX ingestion_run_id_dataset_key_is_synthetic_key ON seagis.ingestion_run USING btree (id, dataset_key, is_synthetic);
CREATE UNIQUE INDEX ingestion_run_pkey ON seagis.ingestion_run USING btree (id);
```

**triggers**

```sql
CREATE TRIGGER guard_ingestion BEFORE INSERT OR UPDATE ON seagis.ingestion_run FOR EACH ROW EXECUTE FUNCTION seagis.guard_ingestion();
```

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.6 `seagis.observation`

Pembacaan suhu air sensor lokal, dengan nilai native, QC dan lineage raw.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis |
| Kind | table |
| Primary key | PRIMARY KEY (id) |
| Unique | UNIQUE (id, ingestion_run_id, dataset_key, is_synthetic); UNIQUE (sensor_id, parameter_code, source_record_key) |
| Rows | UNVERIFIED |
| Writer | seagis_api.ingest; A0 fixtures |
| Reader | seagis_api.history/status; A3 source_bundle; export_experiment_csv.py |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184` |

#### `seagis.observation.id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | `gen_random_uuid()` |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas baris menurut PK tabel |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | DB default / explicit UUID → `gen_random_uuid()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.history/status; A3 source_bundle; export_experiment_csv.py |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184`; catalog seagis.observation.id |

#### `seagis.observation.plot_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (sensor_id, plot_id, dataset_key, is_synthetic) REFERENCES seagis.sensor(id, plot_id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Referensi plot budidaya |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | A1 packet + registered identity + server → `registered sensor.plot_id` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.history/status; A3 source_bundle; export_experiment_csv.py |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184`; catalog seagis.observation.plot_id |

#### `seagis.observation.sensor_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (sensor_id, plot_id, dataset_key, is_synthetic) REFERENCES seagis.sensor(id, plot_id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Referensi deployment sensor |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | A1 packet + registered identity + server → `authenticated credential.sensor_id` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.history/status; A3 source_bundle; export_experiment_csv.py |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184`; catalog seagis.observation.sensor_id |

#### `seagis.observation.dataset_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key, parameter_code, native_unit, unit, conversion_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code, native_unit, unit, conversion_code); FOREIGN KEY (raw_payload_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis_raw.raw_payload(id, ingestion_run_id, dataset_key, is_synthetic); FOREIGN KEY (sensor_id, plot_id, dataset_key, is_synthetic) REFERENCES seagis.sensor(id, plot_id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Kunci dataset terdaftar |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A1 packet + registered identity + server → `registered sensor.dataset_key` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.history/status; A3 source_bundle; export_experiment_csv.py |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184`; catalog seagis.observation.dataset_key |

#### `seagis.observation.ingestion_run_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (raw_payload_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis_raw.raw_payload(id, ingestion_run_id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Referensi ingestion asal |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | A1 packet + registered identity + server → `ingest-generated run_id` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.history/status; A3 source_bundle; export_experiment_csv.py |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184`; catalog seagis.observation.ingestion_run_id |

#### `seagis.observation.raw_payload_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (raw_payload_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis_raw.raw_payload(id, ingestion_run_id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Referensi manifest raw asal |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | A1 packet + registered identity + server → `ingest-generated raw_id` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.history/status; A3 source_bundle; export_experiment_csv.py |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184`; catalog seagis.observation.raw_payload_id |

#### `seagis.observation.is_synthetic`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `boolean` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (raw_payload_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis_raw.raw_payload(id, ingestion_run_id, dataset_key, is_synthetic); FOREIGN KEY (sensor_id, plot_id, dataset_key, is_synthetic) REFERENCES seagis.sensor(id, plot_id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Penanda asal sintetis, terpisah dari QC |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | true |
| Asal / transformasi | A1 packet + registered identity + server → `registered sensor.is_synthetic` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.history/status; A3 source_bundle; export_experiment_csv.py |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184`; catalog seagis.observation.is_synthetic |

#### `seagis.observation.source_record_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | boot_id:sequence untuk paket A1 |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A1 packet + registered identity + server → `boot_id &#124;&#124; : &#124;&#124; sequence` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.history/status; A3 source_bundle; export_experiment_csv.py |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184`; catalog seagis.observation.source_record_key |

#### `seagis.observation.parameter_code`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key, parameter_code, native_unit, unit, conversion_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code, native_unit, unit, conversion_code) |
| Arti bisnis / teknis | Identitas parameter lingkungan |
| Valid values / checks | CHECK (parameter_code = 'water_temperature'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A1 packet + registered identity + server → `constant water_temperature` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.history/status; A3 source_bundle; export_experiment_csv.py |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184`; catalog seagis.observation.parameter_code |

#### `seagis.observation.native_value`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `seagis.finite_float` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Nilai fisik dalam satuan sumber |
| Valid values / checks | CHECK (seagis.valid_value(value::double precision, native_value::double precision, value_status, detection_limit::double precision)) |
| Units / time | Mengikuti unit/native_unit dan dataset_parameter; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | A1 packet + registered identity + server → `packet.water_temperature` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.history/status; A3 source_bundle; export_experiment_csv.py |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184`; catalog seagis.observation.native_value |

#### `seagis.observation.native_unit`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key, parameter_code, native_unit, unit, conversion_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code, native_unit, unit, conversion_code) |
| Arti bisnis / teknis | Satuan asli sebelum normalisasi |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A1 packet + registered identity + server → `constant degC` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.history/status; A3 source_bundle; export_experiment_csv.py |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184`; catalog seagis.observation.native_unit |

#### `seagis.observation.value`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `seagis.finite_float` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Nilai normalisasi; null mengikuti value_status |
| Valid values / checks | CHECK (seagis.valid_value(value::double precision, native_value::double precision, value_status, detection_limit::double precision)) |
| Units / time | Mengikuti unit/native_unit dan dataset_parameter; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | A1 packet + registered identity + server → `packet.water_temperature (identity)` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.history/status; A3 source_bundle; export_experiment_csv.py |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184`; catalog seagis.observation.value |

#### `seagis.observation.unit`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key, parameter_code, native_unit, unit, conversion_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code, native_unit, unit, conversion_code) |
| Arti bisnis / teknis | Satuan nilai normalisasi menurut registri |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A1 packet + registered identity + server → `constant degC` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.history/status; A3 source_bundle; export_experiment_csv.py |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184`; catalog seagis.observation.unit |

#### `seagis.observation.conversion_code`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key, parameter_code, native_unit, unit, conversion_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code, native_unit, unit, conversion_code) |
| Arti bisnis / teknis | Identitas metode konversi satuan |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A1 packet + registered identity + server → `constant identity` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.history/status; A3 source_bundle; export_experiment_csv.py |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184`; catalog seagis.observation.conversion_code |

#### `seagis.observation.value_status`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Ketersediaan angka, terpisah dari kualitas |
| Valid values / checks | CHECK (seagis.valid_value(value::double precision, native_value::double precision, value_status, detection_limit::double precision)) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A1 packet + registered identity + server → `packet.value_status` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.history/status; A3 source_bundle; export_experiment_csv.py |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184`; catalog seagis.observation.value_status |

#### `seagis.observation.detection_limit`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `seagis.finite_float` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Batas deteksi pada satuan normalisasi bila relevan |
| Valid values / checks | CHECK (seagis.valid_value(value::double precision, native_value::double precision, value_status, detection_limit::double precision)) |
| Units / time | Mengikuti unit/native_unit dan dataset_parameter; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | A1 packet + registered identity + server → `omitted -> SQL NULL` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.history/status; A3 source_bundle; export_experiment_csv.py |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184`; catalog seagis.observation.detection_limit |

#### `seagis.observation.observed_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan pengukuran sensor, bukan receipt |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | A1 packet + registered identity + server → `packet.observed_at cast timestamptz` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.history/status; A3 source_bundle; export_experiment_csv.py |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184`; catalog seagis.observation.observed_at |

#### `seagis.observation.ingested_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan data tersedia bagi sistem |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | A1 packet + registered identity + server → `server received = clock_timestamp()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.history/status; A3 source_bundle; export_experiment_csv.py |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184`; catalog seagis.observation.ingested_at |

#### `seagis.observation.quality_status`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Status QC unreviewed, accepted, suspect atau rejected; bukan diagnosis |
| Valid values / checks | CHECK (quality_status = ANY (ARRAY['unreviewed'::text, 'accepted'::text, 'suspect'::text, 'rejected'::text])) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A1 packet + registered identity + server → `pilot policy + flags` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.history/status; A3 source_bundle; export_experiment_csv.py |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184`; catalog seagis.observation.quality_status |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK (seagis.valid_value(value::double precision, native_value::double precision, value_status, detection_limit::double precision));
FOREIGN KEY (dataset_key, parameter_code, native_unit, unit, conversion_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code, native_unit, unit, conversion_code);
UNIQUE (id, ingestion_run_id, dataset_key, is_synthetic);
CHECK (parameter_code = 'water_temperature'::text);
PRIMARY KEY (id);
CHECK (quality_status = ANY (ARRAY['unreviewed'::text, 'accepted'::text, 'suspect'::text, 'rejected'::text]));
FOREIGN KEY (raw_payload_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis_raw.raw_payload(id, ingestion_run_id, dataset_key, is_synthetic);
UNIQUE (sensor_id, parameter_code, source_record_key);
FOREIGN KEY (sensor_id, plot_id, dataset_key, is_synthetic) REFERENCES seagis.sensor(id, plot_id, dataset_key, is_synthetic);
```

**indexes**

```sql
CREATE UNIQUE INDEX observation_id_ingestion_run_id_dataset_key_is_synthetic_key ON seagis.observation USING btree (id, ingestion_run_id, dataset_key, is_synthetic);
CREATE INDEX observation_ingestion ON seagis.observation USING btree (ingestion_run_id);
CREATE UNIQUE INDEX observation_pkey ON seagis.observation USING btree (id);
CREATE INDEX observation_plot_time ON seagis.observation USING btree (plot_id, parameter_code, observed_at DESC);
CREATE UNIQUE INDEX observation_sensor_id_parameter_code_source_record_key_key ON seagis.observation USING btree (sensor_id, parameter_code, source_record_key);
```

**triggers**

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis.observation FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
CREATE TRIGGER guard_observation BEFORE INSERT ON seagis.observation FOR EACH ROW EXECUTE FUNCTION seagis.guard_measurement();
```

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.7 `seagis.parameter`

Registri parameter dan satuan normalisasi.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis |
| Kind | table |
| Primary key | PRIMARY KEY (parameter_code) |
| Unique | UNIQUE (parameter_code, unit) |
| Rows | UNVERIFIED |
| Writer | supabase/seed.sql; scripts/provision_a1.py; scripts/deploy_a2.py |
| Reader | A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:36` |

#### `seagis.parameter.parameter_code`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas parameter lingkungan |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:518` → `'water_temperature'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:36`; catalog seagis.parameter.parameter_code |

#### `seagis.parameter.unit`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Satuan nilai normalisasi menurut registri |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:518` → `'degC'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:36`; catalog seagis.parameter.unit |

#### `seagis.parameter.description`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Penjelasan registri parameter |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:518` → `'Submerged local sensor temperature; distinct from air temperature'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:36`; catalog seagis.parameter.description |

#### Constraint, indeks dan trigger

**constraints**

```sql
UNIQUE (parameter_code, unit);
PRIMARY KEY (parameter_code);
```

**indexes**

```sql
CREATE UNIQUE INDEX parameter_parameter_code_unit_key ON seagis.parameter USING btree (parameter_code, unit);
CREATE UNIQUE INDEX parameter_pkey ON seagis.parameter USING btree (parameter_code);
```

**triggers**
NOT APPLICABLE / NOT FOUND

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.8 `seagis.plot`

Identitas plot dan status survei; koordinat nullable bukan bukti lokasi lapangan.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis |
| Kind | table |
| Primary key | PRIMARY KEY (id) |
| Unique | UNIQUE (id, is_synthetic); UNIQUE (plot_code) |
| Rows | UNVERIFIED |
| Writer | supabase/seed.sql; scripts/provision_a1.py; scripts/deploy_a2.py |
| Reader | A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:58` |

#### `seagis.plot.id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | `gen_random_uuid()` |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas baris menurut PK tabel |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | DB default / explicit UUID → `gen_random_uuid()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:58`; catalog seagis.plot.id |

#### `seagis.plot.plot_code`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Kode plot unik yang dapat dibaca manusia |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/seed.sql:2` → `'plot-a'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:58`; catalog seagis.plot.plot_code |

#### `seagis.plot.name`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Nama tampilan plot |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/seed.sql:2` → `'Plot A (synthetic)'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:58`; catalog seagis.plot.name |

#### `seagis.plot.latitude`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `seagis.finite_float` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Latitude WGS84 dalam derajat |
| Valid values / checks | CHECK ((latitude IS NULL) = (longitude IS NULL)); CHECK (location_status <> 'surveyed'::text OR latitude IS NOT NULL); CHECK (latitude::double precision >= '-90'::integer::double precision AND latitude::double precision <= 90::double precision) |
| Units / time | degree; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | active loader omits column / nullable schema → `NULL in inspected A1/A2 path; other callers may supply under schema guards` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:58`; catalog seagis.plot.latitude |

#### `seagis.plot.longitude`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `seagis.finite_float` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Longitude WGS84 dalam derajat |
| Valid values / checks | CHECK ((latitude IS NULL) = (longitude IS NULL)); CHECK (longitude::double precision >= '-180'::integer::double precision AND longitude::double precision <= 180::double precision) |
| Units / time | degree; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | active loader omits column / nullable schema → `NULL in inspected A1/A2 path; other callers may supply under schema guards` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:58`; catalog seagis.plot.longitude |

#### `seagis.plot.is_synthetic`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `boolean` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Penanda asal sintetis, terpisah dari QC |
| Valid values / checks | CHECK ((location_status = 'synthetic'::text) = is_synthetic) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | true |
| Asal / transformasi | `Seagis-Model/supabase/seed.sql:2` → `true` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:58`; catalog seagis.plot.is_synthetic |

#### `seagis.plot.location_status`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Status lokasi synthetic, not_surveyed atau surveyed |
| Valid values / checks | CHECK ((location_status = 'synthetic'::text) = is_synthetic); CHECK (location_status <> 'surveyed'::text OR latitude IS NOT NULL); CHECK (location_status = ANY (ARRAY['not_surveyed'::text, 'surveyed'::text, 'synthetic'::text])) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/seed.sql:2` → `'synthetic'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:58`; catalog seagis.plot.location_status |

#### `seagis.plot.created_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | `now()` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan pembuatan baris |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | caller / SQL default → `now()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:58`; catalog seagis.plot.created_at |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK ((latitude IS NULL) = (longitude IS NULL));
CHECK ((location_status = 'synthetic'::text) = is_synthetic);
CHECK (location_status <> 'surveyed'::text OR latitude IS NOT NULL);
UNIQUE (id, is_synthetic);
CHECK (latitude::double precision >= '-90'::integer::double precision AND latitude::double precision <= 90::double precision);
CHECK (location_status = ANY (ARRAY['not_surveyed'::text, 'surveyed'::text, 'synthetic'::text]));
CHECK (longitude::double precision >= '-180'::integer::double precision AND longitude::double precision <= 180::double precision);
PRIMARY KEY (id);
UNIQUE (plot_code);
```

**indexes**

```sql
CREATE UNIQUE INDEX plot_id_is_synthetic_key ON seagis.plot USING btree (id, is_synthetic);
CREATE UNIQUE INDEX plot_pkey ON seagis.plot USING btree (id);
CREATE UNIQUE INDEX plot_plot_code_key ON seagis.plot USING btree (plot_code);
```

**triggers**
NOT APPLICABLE / NOT FOUND

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.9 `seagis.plot_grid_mapping`

Pemetaan operasional plot ke grid dengan waktu efektif dan waktu tercatat.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis |
| Kind | table |
| Primary key | PRIMARY KEY (id) |
| Unique | UNIQUE (plot_id, source_grid_id, effective_from) |
| Rows | UNVERIFIED |
| Writer | A0 fixture/admin SQL |
| Reader | A3 source_bundle; feature_input guards |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:152` |

#### `seagis.plot_grid_mapping.id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | `gen_random_uuid()` |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas baris menurut PK tabel |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | DB default / explicit UUID → `gen_random_uuid()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; feature_input guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:152`; catalog seagis.plot_grid_mapping.id |

#### `seagis.plot_grid_mapping.plot_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot(id, is_synthetic) |
| Arti bisnis / teknis | Referensi plot budidaya |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | A0 fixtures/test SQL; operational creator NOT FOUND → `caller-supplied plot_id subject to FK/CHECK/guard_mapping; recorded_at SQL default` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; feature_input guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:152`; catalog seagis.plot_grid_mapping.plot_id |

#### `seagis.plot_grid_mapping.source_grid_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (source_grid_id) REFERENCES seagis.source_grid(id) |
| Arti bisnis / teknis | Referensi sel regional dan layer |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | A0 fixtures/test SQL; operational creator NOT FOUND → `caller-supplied source_grid_id subject to FK/CHECK/guard_mapping; recorded_at SQL default` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; feature_input guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:152`; catalog seagis.plot_grid_mapping.source_grid_id |

#### `seagis.plot_grid_mapping.is_synthetic`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `boolean` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot(id, is_synthetic) |
| Arti bisnis / teknis | Penanda asal sintetis, terpisah dari QC |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | true |
| Asal / transformasi | A0 fixtures/test SQL; operational creator NOT FOUND → `caller-supplied is_synthetic subject to FK/CHECK/guard_mapping; recorded_at SQL default` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; feature_input guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:152`; catalog seagis.plot_grid_mapping.is_synthetic |

#### `seagis.plot_grid_mapping.sampling_method`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Metode pemilihan grid untuk plot |
| Valid values / checks | CHECK (sampling_method = ANY (ARRAY['nearest_wet_cell'::text, 'nearest_cell'::text, 'provider_returned_coordinate'::text, 'synthetic'::text])) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A0 fixtures/test SQL; operational creator NOT FOUND → `caller-supplied sampling_method subject to FK/CHECK/guard_mapping; recorded_at SQL default` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; feature_input guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:152`; catalog seagis.plot_grid_mapping.sampling_method |

#### `seagis.plot_grid_mapping.distance_m`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `seagis.finite_float` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Jarak plot ke sel dalam meter |
| Valid values / checks | CHECK (distance_m::double precision >= 0::double precision) |
| Units / time | m; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | A0 fixtures/test SQL; operational creator NOT FOUND → `caller-supplied distance_m subject to FK/CHECK/guard_mapping; recorded_at SQL default` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; feature_input guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:152`; catalog seagis.plot_grid_mapping.distance_m |

#### `seagis.plot_grid_mapping.representativeness`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Status keterwakilan regional, bukan bukti representasi lokal |
| Valid values / checks | CHECK (representativeness = ANY (ARRAY['unverified'::text, 'regional_only'::text, 'land_mask_issue'::text])) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A0 fixtures/test SQL; operational creator NOT FOUND → `caller-supplied representativeness subject to FK/CHECK/guard_mapping; recorded_at SQL default` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; feature_input guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:152`; catalog seagis.plot_grid_mapping.representativeness |

#### `seagis.plot_grid_mapping.effective_from`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Awal inklusif rentang pemetaan |
| Valid values / checks | CHECK (effective_until IS NULL OR effective_until > effective_from) |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | A0 fixtures/test SQL; operational creator NOT FOUND → `caller-supplied effective_from subject to FK/CHECK/guard_mapping; recorded_at SQL default` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; feature_input guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:152`; catalog seagis.plot_grid_mapping.effective_from |

#### `seagis.plot_grid_mapping.effective_until`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Akhir eksklusif pemetaan; null berarti terbuka |
| Valid values / checks | CHECK (effective_until IS NULL OR effective_until > effective_from) |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | A0 fixtures/test SQL; operational creator NOT FOUND → `caller-supplied effective_until subject to FK/CHECK/guard_mapping; recorded_at SQL default` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; feature_input guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:152`; catalog seagis.plot_grid_mapping.effective_until |

#### `seagis.plot_grid_mapping.recorded_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | `clock_timestamp()` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan pemetaan pertama diketahui sistem |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | caller / SQL default → `clock_timestamp()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; feature_input guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:152`; catalog seagis.plot_grid_mapping.recorded_at |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK (effective_until IS NULL OR effective_until > effective_from);
CHECK (distance_m::double precision >= 0::double precision);
PRIMARY KEY (id);
FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot(id, is_synthetic);
UNIQUE (plot_id, source_grid_id, effective_from);
CHECK (representativeness = ANY (ARRAY['unverified'::text, 'regional_only'::text, 'land_mask_issue'::text]));
CHECK (sampling_method = ANY (ARRAY['nearest_wet_cell'::text, 'nearest_cell'::text, 'provider_returned_coordinate'::text, 'synthetic'::text]));
FOREIGN KEY (source_grid_id) REFERENCES seagis.source_grid(id);
```

**indexes**

```sql
CREATE INDEX mapping_grid_plot ON seagis.plot_grid_mapping USING btree (source_grid_id, plot_id);
CREATE UNIQUE INDEX plot_grid_mapping_pkey ON seagis.plot_grid_mapping USING btree (id);
CREATE UNIQUE INDEX plot_grid_mapping_plot_id_source_grid_id_effective_from_key ON seagis.plot_grid_mapping USING btree (plot_id, source_grid_id, effective_from);
```

**triggers**

```sql
CREATE TRIGGER guard_mapping BEFORE INSERT OR UPDATE ON seagis.plot_grid_mapping FOR EACH ROW EXECUTE FUNCTION seagis.guard_mapping();
CREATE TRIGGER immutable_alignment_mapping BEFORE DELETE OR UPDATE ON seagis.plot_grid_mapping FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
```

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.10 `seagis.quality_event`

Log QC append-only untuk ingestion atau satu measurement.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis |
| Kind | table |
| Primary key | PRIMARY KEY (id) |
| Unique | UNIQUE (ingestion_run_id, event_key) |
| Rows | UNVERIFIED |
| Writer | seagis_api.ingest; A0 fixtures |
| Reader | A3 source_bundle/alignment |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:273` |

#### `seagis.quality_event.id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | `gen_random_uuid()` |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas baris menurut PK tabel |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | DB default / explicit UUID → `gen_random_uuid()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle/alignment |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:273`; catalog seagis.quality_event.id |

#### `seagis.quality_event.ingestion_run_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.ingestion_run(id, dataset_key, is_synthetic); FOREIGN KEY (observation_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.observation(id, ingestion_run_id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Referensi ingestion asal |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:208` → `run_id` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle/alignment |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:273`; catalog seagis.quality_event.ingestion_run_id |

#### `seagis.quality_event.dataset_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (forecast_value_id, dataset_key, is_synthetic) REFERENCES seagis.forecast_value(id, dataset_key, is_synthetic); FOREIGN KEY (ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.ingestion_run(id, dataset_key, is_synthetic); FOREIGN KEY (observation_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.observation(id, ingestion_run_id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Kunci dataset terdaftar |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:208` → `s.dataset_key` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle/alignment |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:273`; catalog seagis.quality_event.dataset_key |

#### `seagis.quality_event.is_synthetic`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `boolean` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (forecast_value_id, dataset_key, is_synthetic) REFERENCES seagis.forecast_value(id, dataset_key, is_synthetic); FOREIGN KEY (ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.ingestion_run(id, dataset_key, is_synthetic); FOREIGN KEY (observation_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.observation(id, ingestion_run_id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Penanda asal sintetis, terpisah dari QC |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | true |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:208` → `s.is_synthetic` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle/alignment |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:273`; catalog seagis.quality_event.is_synthetic |

#### `seagis.quality_event.event_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas event unik per ingestion |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:208` → `flag` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle/alignment |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:273`; catalog seagis.quality_event.event_key |

#### `seagis.quality_event.observation_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (observation_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.observation(id, ingestion_run_id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Referensi pembacaan sensor lokal |
| Valid values / checks | CHECK (num_nonnulls(observation_id, forecast_value_id) <= 1) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:208` → `observation_id` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle/alignment |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:273`; catalog seagis.quality_event.observation_id |

#### `seagis.quality_event.forecast_value_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (forecast_value_id, dataset_key, is_synthetic) REFERENCES seagis.forecast_value(id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Referensi satu nilai model regional |
| Valid values / checks | CHECK (num_nonnulls(observation_id, forecast_value_id) <= 1) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | active loader omits column / nullable schema → `NULL in inspected A1/A2 path; other callers may supply under schema guards` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle/alignment |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:273`; catalog seagis.quality_event.forecast_value_id |

#### `seagis.quality_event.event_code`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Kode jenis kejadian QC |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:208` → `flag` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle/alignment |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:273`; catalog seagis.quality_event.event_code |

#### `seagis.quality_event.severity`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Tingkat kejadian info, warning atau error; bukan risiko penyakit |
| Valid values / checks | CHECK (severity = ANY (ARRAY['info'::text, 'warning'::text, 'error'::text])) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:208` → `CASE WHEN quality='rejected' THEN 'error' WHEN flag IN ('gap_before','out_of_order') THEN 'info' ELSE 'warning' END` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle/alignment |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:273`; catalog seagis.quality_event.severity |

#### `seagis.quality_event.details`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `jsonb` / false |
| Default / generated | `'{}'::jsonb` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Rincian QC JSON tanpa rahasia |
| Valid values / checks | CHECK (jsonb_typeof(details) = 'object'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | {} |
| Asal / transformasi | caller / SQL default → `'{}'::jsonb` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle/alignment |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:273`; catalog seagis.quality_event.details |

#### `seagis.quality_event.created_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | `now()` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan pembuatan baris |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | caller / SQL default → `now()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle/alignment |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:273`; catalog seagis.quality_event.created_at |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK (num_nonnulls(observation_id, forecast_value_id) <= 1);
CHECK (jsonb_typeof(details) = 'object'::text);
FOREIGN KEY (forecast_value_id, dataset_key, is_synthetic) REFERENCES seagis.forecast_value(id, dataset_key, is_synthetic);
FOREIGN KEY (ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.ingestion_run(id, dataset_key, is_synthetic);
UNIQUE (ingestion_run_id, event_key);
FOREIGN KEY (observation_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.observation(id, ingestion_run_id, dataset_key, is_synthetic);
PRIMARY KEY (id);
CHECK (severity = ANY (ARRAY['info'::text, 'warning'::text, 'error'::text]));
```

**indexes**

```sql
CREATE INDEX quality_event_forecast ON seagis.quality_event USING btree (forecast_value_id) WHERE (forecast_value_id IS NOT NULL);
CREATE UNIQUE INDEX quality_event_ingestion_run_id_event_key_key ON seagis.quality_event USING btree (ingestion_run_id, event_key);
CREATE INDEX quality_event_observation ON seagis.quality_event USING btree (observation_id) WHERE (observation_id IS NOT NULL);
CREATE UNIQUE INDEX quality_event_pkey ON seagis.quality_event USING btree (id);
```

**triggers**

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis.quality_event FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
CREATE TRIGGER guard_quality BEFORE INSERT ON seagis.quality_event FOR EACH ROW EXECUTE FUNCTION seagis.guard_quality_event();
```

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.11 `seagis.sensor`

Identitas deployment sensor suhu, plot, kedalaman dan status aktif.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis |
| Kind | table |
| Primary key | PRIMARY KEY (id) |
| Unique | UNIQUE (id, plot_id, dataset_key, is_synthetic); UNIQUE (sensor_code) |
| Rows | UNVERIFIED |
| Writer | supabase/seed.sql; scripts/provision_a1.py; scripts/deploy_a2.py |
| Reader | A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:73` |

#### `seagis.sensor.id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | `gen_random_uuid()` |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas baris menurut PK tabel |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | DB default / explicit UUID → `gen_random_uuid()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:73`; catalog seagis.sensor.id |

#### `seagis.sensor.sensor_code`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Kode deployment sensor unik |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/seed.sql:7` → `'simulator-a'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:73`; catalog seagis.sensor.sensor_code |

#### `seagis.sensor.plot_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot(id, is_synthetic) |
| Arti bisnis / teknis | Referensi plot budidaya |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | `Seagis-Model/supabase/seed.sql:7` → `'00000000-0000-4000-8000-000000000001'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:73`; catalog seagis.sensor.plot_id |

#### `seagis.sensor.dataset_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key, parameter_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code); FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset(dataset_key, scope) |
| Arti bisnis / teknis | Kunci dataset terdaftar |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/seed.sql:7` → `'sensor_temperature_v1'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:73`; catalog seagis.sensor.dataset_key |

#### `seagis.sensor.scope`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | `'local_sensor'::text` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset(dataset_key, scope) |
| Arti bisnis / teknis | Asal local_sensor atau regional_model |
| Valid values / checks | CHECK (scope = 'local_sensor'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | caller / SQL default → `'local_sensor'::text` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:73`; catalog seagis.sensor.scope |

#### `seagis.sensor.parameter_code`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | `'water_temperature'::text` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key, parameter_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code) |
| Arti bisnis / teknis | Identitas parameter lingkungan |
| Valid values / checks | CHECK (parameter_code = 'water_temperature'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | caller / SQL default → `'water_temperature'::text` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:73`; catalog seagis.sensor.parameter_code |

#### `seagis.sensor.depth_m`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `seagis.finite_float` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Kedalaman positif ke bawah dalam meter |
| Valid values / checks | CHECK (depth_status <> 'unknown'::text OR depth_m IS NULL); CHECK (depth_status = 'unknown'::text OR depth_m IS NOT NULL); CHECK (depth_m::double precision >= 0::double precision) |
| Units / time | m; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | active loader omits column / nullable schema → `NULL in inspected A1/A2 path; other callers may supply under schema guards` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:73`; catalog seagis.sensor.depth_m |

#### `seagis.sensor.depth_status`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Status pengetahuan kedalaman sensor |
| Valid values / checks | CHECK (depth_status <> 'unknown'::text OR depth_m IS NULL); CHECK (depth_status = 'unknown'::text OR depth_m IS NOT NULL); CHECK (depth_status <> 'synthetic'::text OR is_synthetic); CHECK (depth_status = ANY (ARRAY['unknown'::text, 'measured'::text, 'synthetic'::text])) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/seed.sql:7` → `'unknown'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:73`; catalog seagis.sensor.depth_status |

#### `seagis.sensor.is_synthetic`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `boolean` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot(id, is_synthetic) |
| Arti bisnis / teknis | Penanda asal sintetis, terpisah dari QC |
| Valid values / checks | CHECK (depth_status <> 'synthetic'::text OR is_synthetic) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | true |
| Asal / transformasi | `Seagis-Model/supabase/seed.sql:7` → `true` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:73`; catalog seagis.sensor.is_synthetic |

#### `seagis.sensor.active`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `boolean` / false |
| Default / generated | `true` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Apakah deployment sensor masih aktif |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | true |
| Asal / transformasi | caller / SQL default → `true` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:73`; catalog seagis.sensor.active |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK (depth_status <> 'unknown'::text OR depth_m IS NULL);
CHECK (depth_status = 'unknown'::text OR depth_m IS NOT NULL);
CHECK (depth_status <> 'synthetic'::text OR is_synthetic);
FOREIGN KEY (dataset_key, parameter_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code);
FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset(dataset_key, scope);
CHECK (depth_m::double precision >= 0::double precision);
CHECK (depth_status = ANY (ARRAY['unknown'::text, 'measured'::text, 'synthetic'::text]));
UNIQUE (id, plot_id, dataset_key, is_synthetic);
CHECK (parameter_code = 'water_temperature'::text);
PRIMARY KEY (id);
FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot(id, is_synthetic);
CHECK (scope = 'local_sensor'::text);
UNIQUE (sensor_code);
```

**indexes**

```sql
CREATE UNIQUE INDEX one_active_temperature_sensor_per_plot ON seagis.sensor USING btree (plot_id) WHERE active;
CREATE UNIQUE INDEX sensor_id_plot_id_dataset_key_is_synthetic_key ON seagis.sensor USING btree (id, plot_id, dataset_key, is_synthetic);
CREATE UNIQUE INDEX sensor_pkey ON seagis.sensor USING btree (id);
CREATE UNIQUE INDEX sensor_sensor_code_key ON seagis.sensor USING btree (sensor_code);
```

**triggers**

```sql
CREATE TRIGGER guard_sensor_deployment BEFORE UPDATE ON seagis.sensor FOR EACH ROW EXECUTE FUNCTION seagis.guard_sensor_deployment();
```

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.12 `seagis.source`

Registri penyedia asal dataset.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis |
| Kind | table |
| Primary key | PRIMARY KEY (source_key) |
| Unique | NOT FOUND |
| Rows | UNVERIFIED |
| Writer | supabase/seed.sql; scripts/provision_a1.py; scripts/deploy_a2.py |
| Reader | A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:11` |

#### `seagis.source.source_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Kunci penyedia sumber |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:506` → `'sensor'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:11`; catalog seagis.source.source_key |

#### `seagis.source.provider`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Nama penyedia dataset |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:506` → `'SEAGIS local sensor / simulator'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:11`; catalog seagis.source.provider |

#### `seagis.source.documentation_url`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | URL dokumentasi penyedia |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:506` → `'https://github.com/De-Voeux/Seagis-Model'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A1 ingest/history; A2 persist/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:11`; catalog seagis.source.documentation_url |

#### Constraint, indeks dan trigger

**constraints**

```sql
PRIMARY KEY (source_key);
```

**indexes**

```sql
CREATE UNIQUE INDEX source_pkey ON seagis.source USING btree (source_key);
```

**triggers**
NOT APPLICABLE / NOT FOUND

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.13 `seagis.source_grid`

Identitas sel regional dan layer kedalaman; bukan plot budidaya.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis |
| Kind | table |
| Primary key | PRIMARY KEY (id) |
| Unique | UNIQUE (dataset_key, grid_key, is_synthetic); UNIQUE (id, dataset_key, is_synthetic) |
| Rows | UNVERIFIED |
| Writer | seagis_environment.persist; A0 fixtures |
| Reader | seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:135` |

#### `seagis.source_grid.id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | `gen_random_uuid()` |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas baris menurut PK tabel |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | DB default / explicit UUID → `gen_random_uuid()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:135`; catalog seagis.source_grid.id |

#### `seagis.source_grid.dataset_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset(dataset_key, scope) |
| Arti bisnis / teknis | Kunci dataset terdaftar |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:173` → `s.dataset_key` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:135`; catalog seagis.source_grid.dataset_key |

#### `seagis.source_grid.scope`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | `'regional_model'::text` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset(dataset_key, scope) |
| Arti bisnis / teknis | Asal local_sensor atau regional_model |
| Valid values / checks | CHECK (scope = 'regional_model'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | caller / SQL default → `'regional_model'::text` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:135`; catalog seagis.source_grid.scope |

#### `seagis.source_grid.grid_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Kunci sel berbasis koordinat/depth atau fixture |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:173` → `g->>'key'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:135`; catalog seagis.source_grid.grid_key |

#### `seagis.source_grid.grid_version`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Versi identitas grid |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:173` → `d.dataset_version` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:135`; catalog seagis.source_grid.grid_version |

#### `seagis.source_grid.identity_basis`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Dasar identitas sel asli, koordinat respons atau sintetis |
| Valid values / checks | CHECK (identity_basis <> 'synthetic'::text OR is_synthetic); CHECK (identity_basis = ANY (ARRAY['provider_cell'::text, 'provider_returned_coordinate'::text, 'synthetic'::text])) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:173` → `g->>'identity_basis'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:135`; catalog seagis.source_grid.identity_basis |

#### `seagis.source_grid.latitude`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `seagis.finite_float` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Latitude WGS84 dalam derajat |
| Valid values / checks | CHECK (latitude::double precision >= '-90'::integer::double precision AND latitude::double precision <= 90::double precision) |
| Units / time | degree; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:173` → `(g->>'latitude')::float8` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:135`; catalog seagis.source_grid.latitude |

#### `seagis.source_grid.longitude`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `seagis.finite_float` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Longitude WGS84 dalam derajat |
| Valid values / checks | CHECK (longitude::double precision >= '-180'::integer::double precision AND longitude::double precision <= 180::double precision) |
| Units / time | degree; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:173` → `(g->>'longitude')::float8` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:135`; catalog seagis.source_grid.longitude |

#### `seagis.source_grid.depth_m`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `seagis.finite_float` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Kedalaman positif ke bawah dalam meter |
| Valid values / checks | CHECK (depth_m::double precision >= 0::double precision) |
| Units / time | m; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:173` → `(g->>'depth_m')::float8` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:135`; catalog seagis.source_grid.depth_m |

#### `seagis.source_grid.is_synthetic`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `boolean` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Penanda asal sintetis, terpisah dari QC |
| Valid values / checks | CHECK (identity_basis <> 'synthetic'::text OR is_synthetic) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | true |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:173` → `false` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:135`; catalog seagis.source_grid.is_synthetic |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK (identity_basis <> 'synthetic'::text OR is_synthetic);
UNIQUE (dataset_key, grid_key, is_synthetic);
FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset(dataset_key, scope);
CHECK (depth_m::double precision >= 0::double precision);
UNIQUE (id, dataset_key, is_synthetic);
CHECK (identity_basis = ANY (ARRAY['provider_cell'::text, 'provider_returned_coordinate'::text, 'synthetic'::text]));
CHECK (latitude::double precision >= '-90'::integer::double precision AND latitude::double precision <= 90::double precision);
CHECK (longitude::double precision >= '-180'::integer::double precision AND longitude::double precision <= 180::double precision);
PRIMARY KEY (id);
CHECK (scope = 'regional_model'::text);
```

**indexes**

```sql
CREATE UNIQUE INDEX source_grid_dataset_key_grid_key_is_synthetic_key ON seagis.source_grid USING btree (dataset_key, grid_key, is_synthetic);
CREATE UNIQUE INDEX source_grid_id_dataset_key_is_synthetic_key ON seagis.source_grid USING btree (id, dataset_key, is_synthetic);
CREATE UNIQUE INDEX source_grid_pkey ON seagis.source_grid USING btree (id);
```

**triggers**

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis.source_grid FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
```

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.14 `seagis_api.credential`

Identitas aktor API berupa hash token, masa berlaku dan pencabutan.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis_api |
| Kind | table |
| Primary key | PRIMARY KEY (id) |
| Unique | UNIQUE (token_sha256) |
| Rows | UNVERIFIED |
| Writer | scripts/provision_a1.py; migration 0002 |
| Reader | seagis_api.actor/rate_ok/ingest/history/status |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:27` |

#### `seagis_api.credential.id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | `gen_random_uuid()` |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas baris menurut PK tabel |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | DB default / explicit UUID → `gen_random_uuid()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:27`; catalog seagis_api.credential.id |

#### `seagis_api.credential.label`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Label administratif credential |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | owning routine / caller → `provision_a1.create(label) CLI --label` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:27`; catalog seagis_api.credential.label |

#### `seagis_api.credential.token_sha256`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Hash token Bearer; token asli tidak disimpan di kolom |
| Valid values / checks | CHECK (token_sha256 ~ '^[0-9a-f]{64}$'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | owning routine / caller → `sha256((sgi_ + secrets.token_urlsafe(32)).encode()).hexdigest(); original token excluded` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:27`; catalog seagis_api.credential.token_sha256 |

#### `seagis_api.credential.kind`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Jenis aktor device atau reader |
| Valid values / checks | CHECK ((kind = 'device'::text) = (sensor_id IS NOT NULL)); CHECK (kind = ANY (ARRAY['device'::text, 'reader'::text])) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | owning routine / caller → `provision_a1.create(kind), CLI device/reader` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:27`; catalog seagis_api.credential.kind |

#### `seagis_api.credential.sensor_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (sensor_id) REFERENCES seagis.sensor(id) |
| Arti bisnis / teknis | Referensi deployment sensor |
| Valid values / checks | CHECK ((kind = 'device'::text) = (sensor_id IS NOT NULL)) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | owning routine / caller → `validated CLI sensor UUID for device, NULL for reader` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:27`; catalog seagis_api.credential.sensor_id |

#### `seagis_api.credential.created_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | `now()` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan pembuatan baris |
| Valid values / checks | CHECK (expires_at > created_at) |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | caller / SQL default → `now()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:27`; catalog seagis_api.credential.created_at |

#### `seagis_api.credential.expires_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan credential tidak berlaku lagi |
| Valid values / checks | CHECK (expires_at > created_at) |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | owning routine / caller → `now()+make_interval(days=>days); CLI 1..365, default 30` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:27`; catalog seagis_api.credential.expires_at |

#### `seagis_api.credential.revoked_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan pencabutan; null bila belum dicabut |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | owning routine / caller → `NULL initially; revoke command UPDATE revoked_at=now()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:27`; catalog seagis_api.credential.revoked_at |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK ((kind = 'device'::text) = (sensor_id IS NOT NULL));
CHECK (expires_at > created_at);
CHECK (kind = ANY (ARRAY['device'::text, 'reader'::text]));
PRIMARY KEY (id);
FOREIGN KEY (sensor_id) REFERENCES seagis.sensor(id);
CHECK (token_sha256 ~ '^[0-9a-f]{64}$'::text);
UNIQUE (token_sha256);
```

**indexes**

```sql
CREATE UNIQUE INDEX credential_pkey ON seagis_api.credential USING btree (id);
CREATE UNIQUE INDEX credential_token_sha256_key ON seagis_api.credential USING btree (token_sha256);
```

**triggers**
NOT APPLICABLE / NOT FOUND

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.15 `seagis_api.packet_receipt`

Kunci idempotensi paket sensor dan digest semantik.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis_api |
| Kind | table |
| Primary key | PRIMARY KEY (sensor_id, source_record_key) |
| Unique | UNIQUE (observation_id) |
| Rows | UNVERIFIED |
| Writer | seagis_api.ingest/reply |
| Reader | seagis_api.actor/rate_ok/ingest/history/status |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:53` |

#### `seagis_api.packet_receipt.sensor_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | true / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (sensor_id) REFERENCES seagis.sensor(id) |
| Arti bisnis / teknis | Referensi deployment sensor |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:215` → `s.id` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:53`; catalog seagis_api.packet_receipt.sensor_id |

#### `seagis_api.packet_receipt.source_record_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | true / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | boot_id:sequence untuk paket A1 |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:215` → `key` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:53`; catalog seagis_api.packet_receipt.source_record_key |

#### `seagis_api.packet_receipt.semantic_sha256`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Hash paket setelah normalisasi semantik retry |
| Valid values / checks | CHECK (semantic_sha256 ~ '^[0-9a-f]{64}$'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:215` → `digest` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:53`; catalog seagis_api.packet_receipt.semantic_sha256 |

#### `seagis_api.packet_receipt.observation_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / true (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (observation_id) REFERENCES seagis.observation(id) |
| Arti bisnis / teknis | Referensi pembacaan sensor lokal |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:215` → `observation_id` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:53`; catalog seagis_api.packet_receipt.observation_id |

#### `seagis_api.packet_receipt.ingestion_run_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (ingestion_run_id) REFERENCES seagis.ingestion_run(id) |
| Arti bisnis / teknis | Referensi ingestion asal |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:215` → `run_id` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:53`; catalog seagis_api.packet_receipt.ingestion_run_id |

#### `seagis_api.packet_receipt.flags`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text[]` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Kode QC dari penerimaan paket |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | [] |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:215` → `flags` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:53`; catalog seagis_api.packet_receipt.flags |

#### Constraint, indeks dan trigger

**constraints**

```sql
FOREIGN KEY (ingestion_run_id) REFERENCES seagis.ingestion_run(id);
FOREIGN KEY (observation_id) REFERENCES seagis.observation(id);
UNIQUE (observation_id);
PRIMARY KEY (sensor_id, source_record_key);
CHECK (semantic_sha256 ~ '^[0-9a-f]{64}$'::text);
FOREIGN KEY (sensor_id) REFERENCES seagis.sensor(id);
```

**indexes**

```sql
CREATE UNIQUE INDEX packet_receipt_observation_id_key ON seagis_api.packet_receipt USING btree (observation_id);
CREATE UNIQUE INDEX packet_receipt_pkey ON seagis_api.packet_receipt USING btree (sensor_id, source_record_key);
```

**triggers**

```sql
CREATE TRIGGER receipt_append_only BEFORE DELETE OR UPDATE ON seagis_api.packet_receipt FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
```

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.16 `seagis_api.reader_plot`

Daftar plot yang boleh dibaca satu credential reader.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis_api |
| Kind | table |
| Primary key | PRIMARY KEY (credential_id, plot_id) |
| Unique | NOT FOUND |
| Rows | UNVERIFIED |
| Writer | scripts/provision_a1.py; migration 0002 |
| Reader | seagis_api.actor/rate_ok/ingest/history/status |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:39` |

#### `seagis_api.reader_plot.credential_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | true / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (credential_id) REFERENCES seagis_api.credential(id) |
| Arti bisnis / teknis | Referensi aktor API terdaftar |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | owning routine / caller → `provision_a1.create generated credential UUID` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:39`; catalog seagis_api.reader_plot.credential_id |

#### `seagis_api.reader_plot.plot_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | true / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (plot_id) REFERENCES seagis.plot(id) |
| Arti bisnis / teknis | Referensi plot budidaya |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | owning routine / caller → `CLI plots validated with UUID(), FK checked by database` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:39`; catalog seagis_api.reader_plot.plot_id |

#### Constraint, indeks dan trigger

**constraints**

```sql
FOREIGN KEY (credential_id) REFERENCES seagis_api.credential(id);
PRIMARY KEY (credential_id, plot_id);
FOREIGN KEY (plot_id) REFERENCES seagis.plot(id);
```

**indexes**

```sql
CREATE UNIQUE INDEX reader_plot_pkey ON seagis_api.reader_plot USING btree (credential_id, plot_id);
```

**triggers**
NOT APPLICABLE / NOT FOUND

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.17 `seagis_api.request_event`

Audit respons API terautentikasi dan dasar rate limit.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis_api |
| Kind | table |
| Primary key | PRIMARY KEY (id) |
| Unique | NOT FOUND |
| Rows | UNVERIFIED |
| Writer | seagis_api.ingest/reply |
| Reader | seagis_api.actor/rate_ok/ingest/history/status |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:44` |

#### `seagis_api.request_event.id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | `gen_random_uuid()` |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas baris menurut PK tabel |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | DB default / explicit UUID → `gen_random_uuid()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:44`; catalog seagis_api.request_event.id |

#### `seagis_api.request_event.credential_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (credential_id) REFERENCES seagis_api.credential(id) |
| Arti bisnis / teknis | Referensi aktor API terdaftar |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:100` → `actor_id` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:44`; catalog seagis_api.request_event.credential_id |

#### `seagis_api.request_event.sensor_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (sensor_id) REFERENCES seagis.sensor(id) |
| Arti bisnis / teknis | Referensi deployment sensor |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:100` → `sensor` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:44`; catalog seagis_api.request_event.sensor_id |

#### `seagis_api.request_event.http_status`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `integer` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Status HTTP respons yang diaudit |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:100` → `status` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:44`; catalog seagis_api.request_event.http_status |

#### `seagis_api.request_event.code`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Kode respons API |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:100` → `code` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:44`; catalog seagis_api.request_event.code |

#### `seagis_api.request_event.created_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | `clock_timestamp()` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan pembuatan baris |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | caller / SQL default → `clock_timestamp()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:44`; catalog seagis_api.request_event.created_at |

#### Constraint, indeks dan trigger

**constraints**

```sql
FOREIGN KEY (credential_id) REFERENCES seagis_api.credential(id);
PRIMARY KEY (id);
FOREIGN KEY (sensor_id) REFERENCES seagis.sensor(id);
```

**indexes**

```sql
CREATE INDEX request_event_actor_time ON seagis_api.request_event USING btree (credential_id, created_at DESC);
CREATE UNIQUE INDEX request_event_pkey ON seagis_api.request_event USING btree (id);
```

**triggers**

```sql
CREATE TRIGGER request_event_append_only BEFORE DELETE OR UPDATE ON seagis_api.request_event FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
```

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.18 `seagis_api.temperature_policy`

Konfigurasi QC engineering pilot dan batas request; bukan ambang penyakit.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis_api |
| Kind | table |
| Primary key | PRIMARY KEY (id) |
| Unique | NOT FOUND |
| Rows | UNVERIFIED |
| Writer | scripts/provision_a1.py; migration 0002 |
| Reader | seagis_api.actor/rate_ok/ingest/history/status |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:67` |

#### `seagis_api.temperature_policy.id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `boolean` / false |
| Default / generated | `true` |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Singleton boolean harus true; bukan UUID |
| Valid values / checks | CHECK (id) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | true |
| Asal / transformasi | DB default / explicit UUID → `true` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:67`; catalog seagis_api.temperature_policy.id |

#### `seagis_api.temperature_policy.version`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas versi kebijakan |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:80` → `'pilot-qc-1'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:67`; catalog seagis_api.temperature_policy.version |

#### `seagis_api.temperature_policy.min_degc`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `double precision` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Batas bawah envelope QC engineering pilot dalam degC |
| Valid values / checks | CHECK (min_degc < max_degc AND max_step_degc > 0::double precision AND future_tolerance_seconds > 0 AND stale_after_seconds > 0 AND requests_per_minute > 0) |
| Units / time | degC; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:80` → `-5` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:67`; catalog seagis_api.temperature_policy.min_degc |

#### `seagis_api.temperature_policy.max_degc`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `double precision` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Batas atas envelope QC engineering pilot dalam degC |
| Valid values / checks | CHECK (min_degc < max_degc AND max_step_degc > 0::double precision AND future_tolerance_seconds > 0 AND stale_after_seconds > 0 AND requests_per_minute > 0) |
| Units / time | degC; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:80` → `60` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:67`; catalog seagis_api.temperature_policy.max_degc |

#### `seagis_api.temperature_policy.max_step_degc`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `double precision` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Batas perubahan suhu pilot dalam degC |
| Valid values / checks | CHECK (min_degc < max_degc AND max_step_degc > 0::double precision AND future_tolerance_seconds > 0 AND stale_after_seconds > 0 AND requests_per_minute > 0) |
| Units / time | degC; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:80` → `3` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:67`; catalog seagis_api.temperature_policy.max_step_degc |

#### `seagis_api.temperature_policy.future_tolerance_seconds`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `integer` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Toleransi jam sensor ke depan dalam detik |
| Valid values / checks | CHECK (min_degc < max_degc AND max_step_degc > 0::double precision AND future_tolerance_seconds > 0 AND stale_after_seconds > 0 AND requests_per_minute > 0) |
| Units / time | s; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:80` → `300` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:67`; catalog seagis_api.temperature_policy.future_tolerance_seconds |

#### `seagis_api.temperature_policy.stale_after_seconds`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `integer` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Batas keterlambatan sensor dalam detik |
| Valid values / checks | CHECK (min_degc < max_degc AND max_step_degc > 0::double precision AND future_tolerance_seconds > 0 AND stale_after_seconds > 0 AND requests_per_minute > 0) |
| Units / time | s; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:80` → `7200` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:67`; catalog seagis_api.temperature_policy.stale_after_seconds |

#### `seagis_api.temperature_policy.requests_per_minute`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `integer` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Batas request per aktor per jendela satu menit |
| Valid values / checks | CHECK (min_degc < max_degc AND max_step_degc > 0::double precision AND future_tolerance_seconds > 0 AND stale_after_seconds > 0 AND requests_per_minute > 0) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:80` → `120` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_api.actor/rate_ok/ingest/history/status |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:67`; catalog seagis_api.temperature_policy.requests_per_minute |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK (min_degc < max_degc AND max_step_degc > 0::double precision AND future_tolerance_seconds > 0 AND stale_after_seconds > 0 AND requests_per_minute > 0);
CHECK (id);
PRIMARY KEY (id);
```

**indexes**

```sql
CREATE UNIQUE INDEX temperature_policy_pkey ON seagis_api.temperature_policy USING btree (id);
```

**triggers**
NOT APPLICABLE / NOT FOUND

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.19 `seagis_environment.attempt`

Audit satu upaya fetch termasuk duplicate dan abandoned.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis_environment |
| Kind | table |
| Primary key | PRIMARY KEY (id) |
| Unique | NOT FOUND |
| Rows | UNVERIFIED |
| Writer | seagis_environment.claim/persist/finish_failure; migration 0003 |
| Reader | A2 status/preview; A3 source_bundle |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:57` |

#### `seagis_environment.attempt.id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas baris menurut PK tabel |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:113` → `lease` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:57`; catalog seagis_environment.attempt.id |

#### `seagis_environment.attempt.dataset_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key) REFERENCES seagis_environment.policy(dataset_key) |
| Arti bisnis / teknis | Kunci dataset terdaftar |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:113` → `k` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:57`; catalog seagis_environment.attempt.dataset_key |

#### `seagis_environment.attempt.started_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan dimulainya ingestion atau attempt |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:113` → `clock_timestamp()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:57`; catalog seagis_environment.attempt.started_at |

#### `seagis_environment.attempt.completed_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan selesai; null selama running |
| Valid values / checks | CHECK ((completed_at IS NULL) = (status = 'running'::text)) |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | owning routine / caller → `clock_timestamp() at persist/failure/abandon; initially NULL` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:57`; catalog seagis_environment.attempt.completed_at |

#### `seagis_environment.attempt.status`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | running/succeeded/duplicate/failed/abandoned untuk fetch attempt |
| Valid values / checks | CHECK ((completed_at IS NULL) = (status = 'running'::text)); CHECK (status = ANY (ARRAY['running'::text, 'succeeded'::text, 'duplicate'::text, 'failed'::text, 'abandoned'::text])) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:113` → `'running'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:57`; catalog seagis_environment.attempt.status |

#### `seagis_environment.attempt.error_code`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Kode kegagalan tersanitasi |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | owning routine / caller → `finish_failure sanitized code or lease_expired on abandoned; otherwise NULL` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:57`; catalog seagis_environment.attempt.error_code |

#### `seagis_environment.attempt.forecast_run_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (forecast_run_id) REFERENCES seagis.forecast_run(id) |
| Arti bisnis / teknis | Referensi capture/vintage model regional |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | owning routine / caller → `persist run_id, also on duplicate; NULL before completion` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:57`; catalog seagis_environment.attempt.forecast_run_id |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK ((completed_at IS NULL) = (status = 'running'::text));
FOREIGN KEY (dataset_key) REFERENCES seagis_environment.policy(dataset_key);
FOREIGN KEY (forecast_run_id) REFERENCES seagis.forecast_run(id);
PRIMARY KEY (id);
CHECK (status = ANY (ARRAY['running'::text, 'succeeded'::text, 'duplicate'::text, 'failed'::text, 'abandoned'::text]));
```

**indexes**

```sql
CREATE UNIQUE INDEX attempt_pkey ON seagis_environment.attempt USING btree (id);
```

**triggers**
NOT APPLICABLE / NOT FOUND

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.20 `seagis_environment.current_speed`

View magnitude arus dari pasangan komponen dengan run/grid/waktu yang sama.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis_environment |
| Kind | view |
| Primary key | NOT APPLICABLE: view |
| Unique | NOT FOUND |
| Rows | UNVERIFIED |
| Writer | NOT APPLICABLE: view |
| Reader | A2 status/preview; A3 source_bundle |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:89` |

#### `seagis_environment.current_speed.eastward_value_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | ID komponen current_eastward pada view |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | seagis.forecast_value u/v → `u.id` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:89`; catalog seagis_environment.current_speed.eastward_value_id |

#### `seagis_environment.current_speed.northward_value_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | ID komponen current_northward pada view |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | seagis.forecast_value u/v → `v.id` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:89`; catalog seagis_environment.current_speed.northward_value_id |

#### `seagis_environment.current_speed.forecast_run_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Referensi capture/vintage model regional |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | seagis.forecast_value u/v → `u.forecast_run_id` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:89`; catalog seagis_environment.current_speed.forecast_run_id |

#### `seagis_environment.current_speed.source_grid_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Referensi sel regional dan layer |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | seagis.forecast_value u/v → `u.source_grid_id` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:89`; catalog seagis_environment.current_speed.source_grid_id |

#### `seagis_environment.current_speed.valid_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Waktu representatif nilai model |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | seagis.forecast_value u/v → `u.valid_at` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:89`; catalog seagis_environment.current_speed.valid_at |

#### `seagis_environment.current_speed.ingested_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan data tersedia bagi sistem |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | seagis.forecast_value u/v → `u.ingested_at` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:89`; catalog seagis_environment.current_speed.ingested_at |

#### `seagis_environment.current_speed.available_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Waktu konservatif ketersediaan input |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | seagis.forecast_value u/v → `greatest(u.ingested_at,v.ingested_at)` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:89`; catalog seagis_environment.current_speed.available_at |

#### `seagis_environment.current_speed.speed_m_s`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `double precision` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | sqrt(uo²+vo²), null bila salah satu komponen tidak present |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | m/s; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | seagis.forecast_value u/v → `CASE WHEN both value_status='present' THEN sqrt(u.value*u.value+v.value*v.value) END` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:89`; catalog seagis_environment.current_speed.speed_m_s |

#### `seagis_environment.current_speed.derivation`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Label formula dan versi magnitude arus |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | seagis.forecast_value u/v → `'sqrt(uo^2+vo^2); a2-vector-magnitude-v1'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:89`; catalog seagis_environment.current_speed.derivation |

#### Constraint, indeks dan trigger

**constraints**
NOT APPLICABLE / NOT FOUND

**indexes**
NOT APPLICABLE / NOT FOUND

**triggers**
NOT APPLICABLE / NOT FOUND


```sql
SELECT u.id AS eastward_value_id,
    v.id AS northward_value_id,
    u.forecast_run_id,
    u.source_grid_id,
    u.valid_at,
    u.ingested_at,
    GREATEST(u.ingested_at, v.ingested_at) AS available_at,
        CASE
            WHEN ((u.value_status = 'present'::text) AND (v.value_status = 'present'::text)) THEN sqrt((((u.value)::double precision * (u.value)::double precision) + ((v.value)::double precision * (v.value)::double precision)))
            ELSE NULL::double precision
        END AS speed_m_s,
    'sqrt(uo^2+vo^2); a2-vector-magnitude-v1'::text AS derivation
   FROM (seagis.forecast_value u
     JOIN seagis.forecast_value v ON (((u.forecast_run_id = v.forecast_run_id) AND (u.source_grid_id = v.source_grid_id) AND (u.valid_at = v.valid_at))))
  WHERE ((u.parameter_code = 'current_eastward'::text) AND (v.parameter_code = 'current_northward'::text));
```

### 4.21 `seagis_environment.demo_grid_mapping`

Bridge khusus dua plot fiktif ke grid nyata untuk preview, bukan otorisasi training.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis_environment |
| Kind | table |
| Primary key | PRIMARY KEY (plot_id, source_grid_id) |
| Unique | NOT FOUND |
| Rows | UNVERIFIED |
| Writer | seagis_environment.claim/persist/finish_failure; migration 0003 |
| Reader | A2 status/preview; A3 source_bundle |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:69` |

#### `seagis_environment.demo_grid_mapping.plot_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | true / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (plot_id, plot_is_synthetic) REFERENCES seagis.plot(id, is_synthetic) |
| Arti bisnis / teknis | Referensi plot budidaya |
| Valid values / checks | CHECK (plot_id = ANY (ARRAY['00000000-0000-4000-8000-000000000001'::uuid, '00000000-0000-4000-8000-000000000002'::uuid])) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:197` → `(m->>'plot_id')::uuid` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:69`; catalog seagis_environment.demo_grid_mapping.plot_id |

#### `seagis_environment.demo_grid_mapping.plot_is_synthetic`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `boolean` / false |
| Default / generated | `true` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (plot_id, plot_is_synthetic) REFERENCES seagis.plot(id, is_synthetic) |
| Arti bisnis / teknis | Harus true untuk bridge demo |
| Valid values / checks | CHECK (plot_is_synthetic) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | true |
| Asal / transformasi | caller / SQL default → `true` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:69`; catalog seagis_environment.demo_grid_mapping.plot_is_synthetic |

#### `seagis_environment.demo_grid_mapping.source_grid_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | true / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (source_grid_id, dataset_key, grid_is_synthetic) REFERENCES seagis.source_grid(id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Referensi sel regional dan layer |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:197` → `grid_id` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:69`; catalog seagis_environment.demo_grid_mapping.source_grid_id |

#### `seagis_environment.demo_grid_mapping.dataset_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key) REFERENCES seagis_environment.policy(dataset_key); FOREIGN KEY (source_grid_id, dataset_key, grid_is_synthetic) REFERENCES seagis.source_grid(id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Kunci dataset terdaftar |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:197` → `s.dataset_key` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:69`; catalog seagis_environment.demo_grid_mapping.dataset_key |

#### `seagis_environment.demo_grid_mapping.grid_is_synthetic`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `boolean` / false |
| Default / generated | `false` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (source_grid_id, dataset_key, grid_is_synthetic) REFERENCES seagis.source_grid(id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Harus false untuk grid nyata di bridge demo |
| Valid values / checks | CHECK (NOT grid_is_synthetic) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | true |
| Asal / transformasi | caller / SQL default → `false` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:69`; catalog seagis_environment.demo_grid_mapping.grid_is_synthetic |

#### `seagis_environment.demo_grid_mapping.example_latitude`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `seagis.finite_float` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Latitude contoh fiktif, bukan survei |
| Valid values / checks | CHECK (example_latitude::double precision >= '-90'::integer::double precision AND example_latitude::double precision <= 90::double precision) |
| Units / time | degree; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:197` → `(m->>'latitude')::float8` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:69`; catalog seagis_environment.demo_grid_mapping.example_latitude |

#### `seagis_environment.demo_grid_mapping.example_longitude`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `seagis.finite_float` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Longitude contoh fiktif, bukan survei |
| Valid values / checks | CHECK (example_longitude::double precision >= '-180'::integer::double precision AND example_longitude::double precision <= 180::double precision) |
| Units / time | degree; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:197` → `(m->>'longitude')::float8` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:69`; catalog seagis_environment.demo_grid_mapping.example_longitude |

#### `seagis_environment.demo_grid_mapping.coordinate_status`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | example_not_surveyed pada bridge demo |
| Valid values / checks | CHECK (coordinate_status = 'example_not_surveyed'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:197` → `m->>'coordinate_status'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:69`; catalog seagis_environment.demo_grid_mapping.coordinate_status |

#### `seagis_environment.demo_grid_mapping.distance_m`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `seagis.finite_float` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Jarak plot ke sel dalam meter |
| Valid values / checks | CHECK (distance_m::double precision >= 0::double precision AND distance_m::double precision <= 30000::double precision) |
| Units / time | m; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:197` → `(m->>'distance_m')::float8` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:69`; catalog seagis_environment.demo_grid_mapping.distance_m |

#### `seagis_environment.demo_grid_mapping.sampling_method`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Metode pemilihan grid untuk plot |
| Valid values / checks | CHECK (sampling_method = ANY (ARRAY['nearest_cell'::text, 'provider_returned_coordinate'::text])) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:197` → `m->>'sampling_method'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:69`; catalog seagis_environment.demo_grid_mapping.sampling_method |

#### `seagis_environment.demo_grid_mapping.created_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | `now()` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan pembuatan baris |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | caller / SQL default → `now()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:69`; catalog seagis_environment.demo_grid_mapping.created_at |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK (coordinate_status = 'example_not_surveyed'::text);
FOREIGN KEY (dataset_key) REFERENCES seagis_environment.policy(dataset_key);
CHECK (distance_m::double precision >= 0::double precision AND distance_m::double precision <= 30000::double precision);
CHECK (example_latitude::double precision >= '-90'::integer::double precision AND example_latitude::double precision <= 90::double precision);
CHECK (example_longitude::double precision >= '-180'::integer::double precision AND example_longitude::double precision <= 180::double precision);
CHECK (NOT grid_is_synthetic);
PRIMARY KEY (plot_id, source_grid_id);
CHECK (plot_id = ANY (ARRAY['00000000-0000-4000-8000-000000000001'::uuid, '00000000-0000-4000-8000-000000000002'::uuid]));
FOREIGN KEY (plot_id, plot_is_synthetic) REFERENCES seagis.plot(id, is_synthetic);
CHECK (plot_is_synthetic);
CHECK (sampling_method = ANY (ARRAY['nearest_cell'::text, 'provider_returned_coordinate'::text]));
FOREIGN KEY (source_grid_id, dataset_key, grid_is_synthetic) REFERENCES seagis.source_grid(id, dataset_key, is_synthetic);
```

**indexes**

```sql
CREATE UNIQUE INDEX demo_grid_mapping_pkey ON seagis_environment.demo_grid_mapping USING btree (plot_id, source_grid_id);
```

**triggers**

```sql
CREATE TRIGGER immutable_demo_mapping BEFORE DELETE OR UPDATE ON seagis_environment.demo_grid_mapping FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
```

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.22 `seagis_environment.policy`

Kebijakan fetch, lisensi, cadence scheduler, staleness dan retensi regional.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis_environment |
| Kind | table |
| Primary key | PRIMARY KEY (dataset_key) |
| Unique | NOT FOUND |
| Rows | UNVERIFIED |
| Writer | seagis_environment.claim/persist/finish_failure; migration 0003 |
| Reader | A2 status/preview; A3 source_bundle |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:16` |

#### `seagis_environment.policy.dataset_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key) REFERENCES seagis.dataset(dataset_key) |
| Arti bisnis / teknis | Kunci dataset terdaftar |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:30` → `dataset_key` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:16`; catalog seagis_environment.policy.dataset_key |

#### `seagis_environment.policy.enabled`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `boolean` / false |
| Default / generated | `true` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Apakah policy regional mengizinkan fetch |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | true |
| Asal / transformasi | caller / SQL default → `true` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:16`; catalog seagis_environment.policy.enabled |

#### `seagis_environment.policy.purpose`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Tujuan noncommercial_educational_prototype |
| Valid values / checks | CHECK (purpose = 'noncommercial_educational_prototype'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:30` → `'noncommercial_educational_prototype'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:16`; catalog seagis_environment.policy.purpose |

#### `seagis_environment.policy.licence_url`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Referensi lisensi sumber |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:30` → `licence_url` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:16`; catalog seagis_environment.policy.licence_url |

#### `seagis_environment.policy.terms_review`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas review ketentuan provider |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:30` → `CASE WHEN source_key='copernicus' THEN 'cmems-licence-20261022-sections-2.2-2.4-2.6' ELSE 'open-meteo-terms-20261022-noncommercial-cc-by-4.0' END` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:16`; catalog seagis_environment.policy.terms_review |

#### `seagis_environment.policy.attribution`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Teks atribusi yang harus dipertahankan |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:30` → `attribution` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:16`; catalog seagis_environment.policy.attribution |

#### `seagis_environment.policy.update_seconds`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `integer` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Interval nominal scheduler per provider dalam detik |
| Valid values / checks | CHECK (release_offset_seconds >= 0 AND release_offset_seconds < update_seconds); CHECK (stale_seconds >= update_seconds); CHECK (update_seconds >= 21600) |
| Units / time | s; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:30` → `CASE WHEN source_key='copernicus' THEN 86400 ELSE 21600 END` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:16`; catalog seagis_environment.policy.update_seconds |

#### `seagis_environment.policy.release_offset_seconds`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `integer` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Offset fase jadwal dalam detik |
| Valid values / checks | CHECK (release_offset_seconds >= 0 AND release_offset_seconds < update_seconds) |
| Units / time | s; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:30` → `CASE WHEN dataset_key='cmems_nutrients_daily' THEN 45000 WHEN source_key='copernicus' THEN 30600 ELSE 16200 END` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:16`; catalog seagis_environment.policy.release_offset_seconds |

#### `seagis_environment.policy.stale_seconds`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `integer` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Usia vintage maksimum menurut policy dalam detik |
| Valid values / checks | CHECK (stale_seconds >= update_seconds) |
| Units / time | s; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:30` → `CASE WHEN source_key='copernicus' THEN 172800 ELSE 43200 END` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:16`; catalog seagis_environment.policy.stale_seconds |

#### `seagis_environment.policy.retention_mode`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | `'metadata_only'::text` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Kebijakan metadata_only pada A2 |
| Valid values / checks | CHECK (retention_mode = 'metadata_only'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | caller / SQL default → `'metadata_only'::text` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:16`; catalog seagis_environment.policy.retention_mode |

#### `seagis_environment.policy.reviewed_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | `now()` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan review kebijakan |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | caller / SQL default → `now()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:16`; catalog seagis_environment.policy.reviewed_at |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK (release_offset_seconds >= 0 AND release_offset_seconds < update_seconds);
CHECK (stale_seconds >= update_seconds);
FOREIGN KEY (dataset_key) REFERENCES seagis.dataset(dataset_key);
PRIMARY KEY (dataset_key);
CHECK (purpose = 'noncommercial_educational_prototype'::text);
CHECK (retention_mode = 'metadata_only'::text);
CHECK (update_seconds >= 21600);
```

**indexes**

```sql
CREATE UNIQUE INDEX policy_pkey ON seagis_environment.policy USING btree (dataset_key);
```

**triggers**
NOT APPLICABLE / NOT FOUND

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.23 `seagis_environment.schedule_state`

State mutable lease, due time, backoff dan keberhasilan terakhir.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis_environment |
| Kind | table |
| Primary key | PRIMARY KEY (dataset_key) |
| Unique | NOT FOUND |
| Rows | UNVERIFIED |
| Writer | seagis_environment.claim/persist/finish_failure; migration 0003 |
| Reader | A2 status/preview; A3 source_bundle |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:45` |

#### `seagis_environment.schedule_state.dataset_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (dataset_key) REFERENCES seagis_environment.policy(dataset_key) |
| Arti bisnis / teknis | Kunci dataset terdaftar |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:56` → `dataset_key` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:45`; catalog seagis_environment.schedule_state.dataset_key |

#### `seagis_environment.schedule_state.lease_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas lease fetch aktif |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | owning routine / caller → `claim gen_random_uuid(); cleared after persist/failure` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:45`; catalog seagis_environment.schedule_state.lease_id |

#### `seagis_environment.schedule_state.lease_until`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan lease tidak lagi valid |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | owning routine / caller → `claim clock_timestamp()+interval 20 minutes; cleared after persist/failure` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:45`; catalog seagis_environment.schedule_state.lease_until |

#### `seagis_environment.schedule_state.next_attempt_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | `'-infinity'::timestamp with time zone` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Waktu fetch paling awal; dapat bernilai -infinity pada awal |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | caller / SQL default → `'-infinity'::timestamp with time zone` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:45`; catalog seagis_environment.schedule_state.next_attempt_at |

#### `seagis_environment.schedule_state.last_success_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan fetch/persist terakhir berhasil |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | owning routine / caller → `persist t=clock_timestamp()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:45`; catalog seagis_environment.schedule_state.last_success_at |

#### `seagis_environment.schedule_state.last_attempt_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan attempt terakhir dimulai |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | owning routine / caller → `claim clock_timestamp()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:45`; catalog seagis_environment.schedule_state.last_attempt_at |

#### `seagis_environment.schedule_state.last_error_code`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Kode kegagalan attempt terakhir |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | owning routine / caller → `finish_failure sanitized code; cleared on success` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:45`; catalog seagis_environment.schedule_state.last_error_code |

#### `seagis_environment.schedule_state.failures`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `integer` / false |
| Default / generated | `0` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Jumlah kegagalan untuk perhitungan backoff |
| Valid values / checks | CHECK (failures >= 0) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | caller / SQL default → `0` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:45`; catalog seagis_environment.schedule_state.failures |

#### `seagis_environment.schedule_state.last_forecast_run_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (last_forecast_run_id) REFERENCES seagis.forecast_run(id) |
| Arti bisnis / teknis | Referensi vintage terakhir berhasil |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | owning routine / caller → `persist run_id` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A2 status/preview; A3 source_bundle |
| Evidence | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:45`; catalog seagis_environment.schedule_state.last_forecast_run_id |

#### Constraint, indeks dan trigger

**constraints**

```sql
FOREIGN KEY (dataset_key) REFERENCES seagis_environment.policy(dataset_key);
CHECK (failures >= 0);
FOREIGN KEY (last_forecast_run_id) REFERENCES seagis.forecast_run(id);
PRIMARY KEY (dataset_key);
```

**indexes**

```sql
CREATE UNIQUE INDEX schedule_state_pkey ON seagis_environment.schedule_state USING btree (dataset_key);
```

**triggers**
NOT APPLICABLE / NOT FOUND

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.24 `seagis_features.feature_input`

Lineage FK input feature snapshot dan guard cutoff.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis_features |
| Kind | table |
| Primary key | PRIMARY KEY (id) |
| Unique | NOT FOUND |
| Rows | UNVERIFIED |
| Writer | A0 fixture/test inserts; production builder NOT FOUND |
| Reader | snapshot/input guards; production ML consumer NOT FOUND |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:320` |

#### `seagis_features.feature_input.id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | `gen_random_uuid()` |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas baris menurut PK tabel |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | DB default / explicit UUID → `gen_random_uuid()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; snapshot/input guards; production ML consumer NOT FOUND |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:320`; catalog seagis_features.feature_input.id |

#### `seagis_features.feature_input.snapshot_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (snapshot_id) REFERENCES seagis_features.feature_snapshot(id) |
| Arti bisnis / teknis | Referensi snapshot induk |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | A0 fixtures/tests; production builder NOT FOUND → `caller-supplied snapshot_id subject to guard_input/guard_snapshot; no production derivation claimed` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; snapshot/input guards; production ML consumer NOT FOUND |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:320`; catalog seagis_features.feature_input.snapshot_id |

#### `seagis_features.feature_input.observation_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (observation_id) REFERENCES seagis.observation(id) |
| Arti bisnis / teknis | Referensi pembacaan sensor lokal |
| Valid values / checks | CHECK (num_nonnulls(observation_id, forecast_value_id) = 1) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | A0 fixtures/tests; production builder NOT FOUND → `caller-supplied observation_id subject to guard_input/guard_snapshot; no production derivation claimed` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; snapshot/input guards; production ML consumer NOT FOUND |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:320`; catalog seagis_features.feature_input.observation_id |

#### `seagis_features.feature_input.forecast_value_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (forecast_value_id) REFERENCES seagis.forecast_value(id) |
| Arti bisnis / teknis | Referensi satu nilai model regional |
| Valid values / checks | CHECK (num_nonnulls(observation_id, forecast_value_id) = 1) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | A0 fixtures/tests; production builder NOT FOUND → `caller-supplied forecast_value_id subject to guard_input/guard_snapshot; no production derivation claimed` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; snapshot/input guards; production ML consumer NOT FOUND |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:320`; catalog seagis_features.feature_input.forecast_value_id |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK (num_nonnulls(observation_id, forecast_value_id) = 1);
FOREIGN KEY (forecast_value_id) REFERENCES seagis.forecast_value(id);
FOREIGN KEY (observation_id) REFERENCES seagis.observation(id);
PRIMARY KEY (id);
FOREIGN KEY (snapshot_id) REFERENCES seagis_features.feature_snapshot(id);
```

**indexes**

```sql
CREATE UNIQUE INDEX feature_input_forecast ON seagis_features.feature_input USING btree (snapshot_id, forecast_value_id) WHERE (forecast_value_id IS NOT NULL);
CREATE UNIQUE INDEX feature_input_observation ON seagis_features.feature_input USING btree (snapshot_id, observation_id) WHERE (observation_id IS NOT NULL);
CREATE UNIQUE INDEX feature_input_pkey ON seagis_features.feature_input USING btree (id);
```

**triggers**

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis_features.feature_input FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
CREATE TRIGGER guard_feature_input BEFORE INSERT ON seagis_features.feature_input FOR EACH ROW EXECUTE FUNCTION seagis_features.guard_input();
```

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.25 `seagis_features.feature_snapshot`

Container fitur draft/sealed dengan cutoff dan hash; builder produksi belum ditemukan.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis_features |
| Kind | table |
| Primary key | PRIMARY KEY (id) |
| Unique | UNIQUE (plot_id, as_of, feature_version, input_manifest_sha256) |
| Rows | UNVERIFIED |
| Writer | A0 fixture/test inserts; production builder NOT FOUND |
| Reader | snapshot/input guards; production ML consumer NOT FOUND |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:301` |

#### `seagis_features.feature_snapshot.id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | `gen_random_uuid()` |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas baris menurut PK tabel |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | DB default / explicit UUID → `gen_random_uuid()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; snapshot/input guards; production ML consumer NOT FOUND |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:301`; catalog seagis_features.feature_snapshot.id |

#### `seagis_features.feature_snapshot.plot_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot(id, is_synthetic) |
| Arti bisnis / teknis | Referensi plot budidaya |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | A0 fixtures/tests; production builder NOT FOUND → `caller-supplied plot_id subject to guard_input/guard_snapshot; no production derivation claimed` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; snapshot/input guards; production ML consumer NOT FOUND |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:301`; catalog seagis_features.feature_snapshot.plot_id |

#### `seagis_features.feature_snapshot.is_synthetic`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `boolean` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot(id, is_synthetic) |
| Arti bisnis / teknis | Penanda asal sintetis, terpisah dari QC |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | true |
| Asal / transformasi | A0 fixtures/tests; production builder NOT FOUND → `caller-supplied is_synthetic subject to guard_input/guard_snapshot; no production derivation claimed` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; snapshot/input guards; production ML consumer NOT FOUND |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:301`; catalog seagis_features.feature_snapshot.is_synthetic |

#### `seagis_features.feature_snapshot.as_of`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Cutoff informasi untuk feature snapshot |
| Valid values / checks | CHECK (generated_at >= as_of) |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | A0 fixtures/tests; production builder NOT FOUND → `caller-supplied as_of subject to guard_input/guard_snapshot; no production derivation claimed` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; snapshot/input guards; production ML consumer NOT FOUND |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:301`; catalog seagis_features.feature_snapshot.as_of |

#### `seagis_features.feature_snapshot.generated_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan snapshot fitur dihasilkan |
| Valid values / checks | CHECK (generated_at >= as_of) |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | A0 fixtures/tests; production builder NOT FOUND → `caller-supplied generated_at subject to guard_input/guard_snapshot; no production derivation claimed` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; snapshot/input guards; production ML consumer NOT FOUND |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:301`; catalog seagis_features.feature_snapshot.generated_at |

#### `seagis_features.feature_snapshot.feature_version`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Versi definisi/builder fitur |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A0 fixtures/tests; production builder NOT FOUND → `caller-supplied feature_version subject to guard_input/guard_snapshot; no production derivation claimed` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; snapshot/input guards; production ML consumer NOT FOUND |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:301`; catalog seagis_features.feature_snapshot.feature_version |

#### `seagis_features.feature_snapshot.feature_schema_version`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Versi struktur JSON fitur |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A0 fixtures/tests; production builder NOT FOUND → `caller-supplied feature_schema_version subject to guard_input/guard_snapshot; no production derivation claimed` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; snapshot/input guards; production ML consumer NOT FOUND |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:301`; catalog seagis_features.feature_snapshot.feature_schema_version |

#### `seagis_features.feature_snapshot.features`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `jsonb` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Objek JSON fitur; validitas perhitungan tidak dibuktikan container |
| Valid values / checks | CHECK (jsonb_typeof(features) = 'object'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | {} |
| Asal / transformasi | A0 fixtures/tests; production builder NOT FOUND → `caller-supplied features subject to guard_input/guard_snapshot; no production derivation claimed` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; snapshot/input guards; production ML consumer NOT FOUND |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:301`; catalog seagis_features.feature_snapshot.features |

#### `seagis_features.feature_snapshot.missing_context`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text[]` / false |
| Default / generated | `'{}'::text[]` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Daftar konteks yang tidak tersedia |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | [] |
| Asal / transformasi | caller / SQL default → `'{}'::text[]` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; snapshot/input guards; production ML consumer NOT FOUND |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:301`; catalog seagis_features.feature_snapshot.missing_context |

#### `seagis_features.feature_snapshot.status`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | `'draft'::text` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | draft sebelum sealing, sealed setelah manifest cocok |
| Valid values / checks | CHECK ((status = 'draft'::text) = (input_manifest_sha256 IS NULL)); CHECK (status = ANY (ARRAY['draft'::text, 'sealed'::text])) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | caller / SQL default → `'draft'::text` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; snapshot/input guards; production ML consumer NOT FOUND |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:301`; catalog seagis_features.feature_snapshot.status |

#### `seagis_features.feature_snapshot.input_manifest_sha256`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Digest daftar input lineage terurut |
| Valid values / checks | CHECK ((status = 'draft'::text) = (input_manifest_sha256 IS NULL)); CHECK (input_manifest_sha256 ~ '^[0-9a-f]{64}$'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | seagis_features.manifest_hash(snapshot) → `SHA256 sorted input references at draft -> sealed` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; snapshot/input guards; production ML consumer NOT FOUND |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:301`; catalog seagis_features.feature_snapshot.input_manifest_sha256 |

#### `seagis_features.feature_snapshot.features_sha256`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / true |
| Default / generated | `seagis.jsonb_sha256(features)` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Digest JSONB fitur menurut PostgreSQL |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | DB generated → `seagis.jsonb_sha256(features)` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; snapshot/input guards; production ML consumer NOT FOUND |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:301`; catalog seagis_features.feature_snapshot.features_sha256 |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK (generated_at >= as_of);
CHECK ((status = 'draft'::text) = (input_manifest_sha256 IS NULL));
CHECK (jsonb_typeof(features) = 'object'::text);
CHECK (input_manifest_sha256 ~ '^[0-9a-f]{64}$'::text);
PRIMARY KEY (id);
UNIQUE (plot_id, as_of, feature_version, input_manifest_sha256);
FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot(id, is_synthetic);
CHECK (status = ANY (ARRAY['draft'::text, 'sealed'::text]));
```

**indexes**

```sql
CREATE UNIQUE INDEX feature_snapshot_pkey ON seagis_features.feature_snapshot USING btree (id);
CREATE UNIQUE INDEX feature_snapshot_plot_id_as_of_feature_version_input_manife_key ON seagis_features.feature_snapshot USING btree (plot_id, as_of, feature_version, input_manifest_sha256);
```

**triggers**

```sql
CREATE TRIGGER guard_snapshot BEFORE INSERT OR UPDATE ON seagis_features.feature_snapshot FOR EACH ROW EXECUTE FUNCTION seagis_features.guard_snapshot();
CREATE TRIGGER no_snapshot_delete BEFORE DELETE ON seagis_features.feature_snapshot FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
```

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.26 `seagis_quality.alignment_snapshot`

Dokumen QC/alignment hourly immutable; selalu training_authorized=false.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis_quality |
| Kind | table |
| Primary key | PRIMARY KEY (id) |
| Unique | UNIQUE (plot_id, mode, start_at, end_at, policy_version, source_sha256) |
| Rows | UNVERIFIED |
| Writer | seagis_quality.save_snapshot |
| Reader | seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:21` |

#### `seagis_quality.alignment_snapshot.id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | `gen_random_uuid()` |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas baris menurut PK tabel |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | DB default / explicit UUID → `gen_random_uuid()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:21`; catalog seagis_quality.alignment_snapshot.id |

#### `seagis_quality.alignment_snapshot.plot_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (plot_id) REFERENCES seagis.plot(id) |
| Arti bisnis / teknis | Referensi plot budidaya |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | A3 build -> save_snapshot → `document.plot_id` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:21`; catalog seagis_quality.alignment_snapshot.plot_id |

#### `seagis_quality.alignment_snapshot.mode`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | demo_review atau operational_review sesuai asal plot |
| Valid values / checks | CHECK (mode = ANY (ARRAY['demo_review'::text, 'operational_review'::text])) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A3 build -> save_snapshot → `document.mode` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:21`; catalog seagis_quality.alignment_snapshot.mode |

#### `seagis_quality.alignment_snapshot.start_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Awal inklusif jendela alignment |
| Valid values / checks | CHECK (end_at > start_at AND (end_at - start_at) <= '7 days'::interval) |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | A3 build -> save_snapshot → `document.start_at` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:21`; catalog seagis_quality.alignment_snapshot.start_at |

#### `seagis_quality.alignment_snapshot.end_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Akhir eksklusif jendela alignment |
| Valid values / checks | CHECK (end_at > start_at AND (end_at - start_at) <= '7 days'::interval) |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | A3 build -> save_snapshot → `document.end_at` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:21`; catalog seagis_quality.alignment_snapshot.end_at |

#### `seagis_quality.alignment_snapshot.policy_version`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (policy_version) REFERENCES seagis_quality.policy(version) |
| Arti bisnis / teknis | Referensi versi policy QC |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A3 build -> save_snapshot → `registered policy.version` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:21`; catalog seagis_quality.alignment_snapshot.policy_version |

#### `seagis_quality.alignment_snapshot.source_sha256`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Digest source bundle untuk deteksi sumber berubah |
| Valid values / checks | CHECK (source_sha256 ~ '^[0-9a-f]{64}$'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A3 build -> save_snapshot → `document.source_sha256 checked against fresh source_bundle` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:21`; catalog seagis_quality.alignment_snapshot.source_sha256 |

#### `seagis_quality.alignment_snapshot.input_manifest_sha256`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Digest daftar input lineage terurut |
| Valid values / checks | CHECK (input_manifest_sha256 ~ '^[0-9a-f]{64}$'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A3 build -> save_snapshot → `SHA256 sorted distinct at&#124;source_ref lines` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:21`; catalog seagis_quality.alignment_snapshot.input_manifest_sha256 |

#### `seagis_quality.alignment_snapshot.body`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `jsonb` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Dokumen alignment lengkap, termasuk rows dan laporan QC |
| Valid values / checks | CHECK (jsonb_typeof(body) = 'object'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | {} |
| Asal / transformasi | A3 build -> save_snapshot → `document` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:21`; catalog seagis_quality.alignment_snapshot.body |

#### `seagis_quality.alignment_snapshot.body_sha256`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / true |
| Default / generated | `seagis.jsonb_sha256(body)` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Digest generated atas JSONB body |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | DB generated → `seagis.jsonb_sha256(body)` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:21`; catalog seagis_quality.alignment_snapshot.body_sha256 |

#### `seagis_quality.alignment_snapshot.created_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | `clock_timestamp()` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan pembuatan baris |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | A3 build -> save_snapshot → `SQL default clock_timestamp()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:21`; catalog seagis_quality.alignment_snapshot.created_at |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK (jsonb_typeof(body) = 'object'::text);
CHECK (end_at > start_at AND (end_at - start_at) <= '7 days'::interval);
CHECK (input_manifest_sha256 ~ '^[0-9a-f]{64}$'::text);
CHECK (mode = ANY (ARRAY['demo_review'::text, 'operational_review'::text]));
PRIMARY KEY (id);
FOREIGN KEY (plot_id) REFERENCES seagis.plot(id);
UNIQUE (plot_id, mode, start_at, end_at, policy_version, source_sha256);
FOREIGN KEY (policy_version) REFERENCES seagis_quality.policy(version);
CHECK (source_sha256 ~ '^[0-9a-f]{64}$'::text);
```

**indexes**

```sql
CREATE UNIQUE INDEX alignment_snapshot_pkey ON seagis_quality.alignment_snapshot USING btree (id);
CREATE UNIQUE INDEX alignment_snapshot_plot_id_mode_start_at_end_at_policy_vers_key ON seagis_quality.alignment_snapshot USING btree (plot_id, mode, start_at, end_at, policy_version, source_sha256);
```

**triggers**

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis_quality.alignment_snapshot FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
```

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.27 `seagis_quality.policy`

Registri versi kebijakan QC dan hash kode builder yang immutable.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis_quality |
| Kind | table |
| Primary key | PRIMARY KEY (version) |
| Unique | NOT FOUND |
| Rows | UNVERIFIED |
| Writer | scripts/quality/store.py::register_policy |
| Reader | seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:14` |

#### `seagis_quality.policy.version`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas versi kebijakan |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | owning routine / caller → `register_policy policy[version]` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:14`; catalog seagis_quality.policy.version |

#### `seagis_quality.policy.definition`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `jsonb` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Dokumen kebijakan QC yang diregistrasi |
| Valid values / checks | CHECK (jsonb_typeof(definition) = 'object'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | {} |
| Asal / transformasi | owning routine / caller → `register_policy JSON policy argument (config/a3_quality.json)` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:14`; catalog seagis_quality.policy.definition |

#### `seagis_quality.policy.policy_sha256`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Digest isi policy |
| Valid values / checks | CHECK (policy_sha256 ~ '^[0-9a-f]{64}$'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | owning routine / caller → `register_policy policy_hash from digest(policy)` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:14`; catalog seagis_quality.policy.policy_sha256 |

#### `seagis_quality.policy.code_sha256`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Digest source builder alignment |
| Valid values / checks | CHECK (code_sha256 ~ '^[0-9a-f]{64}$'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | owning routine / caller → `register_policy builder_hash from code_hash()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:14`; catalog seagis_quality.policy.code_sha256 |

#### `seagis_quality.policy.registered_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | `clock_timestamp()` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan registrasi policy immutable |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | caller / SQL default → `clock_timestamp()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:14`; catalog seagis_quality.policy.registered_at |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK (code_sha256 ~ '^[0-9a-f]{64}$'::text);
CHECK (jsonb_typeof(definition) = 'object'::text);
PRIMARY KEY (version);
CHECK (policy_sha256 ~ '^[0-9a-f]{64}$'::text);
```

**indexes**

```sql
CREATE UNIQUE INDEX policy_pkey ON seagis_quality.policy USING btree (version);
```

**triggers**

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis_quality.policy FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
```

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.28 `seagis_quality.snapshot_input`

Lineage measurement per jam alignment snapshot.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis_quality |
| Kind | table |
| Primary key | PRIMARY KEY (snapshot_id, aligned_at, source_ref) |
| Unique | NOT FOUND |
| Rows | UNVERIFIED |
| Writer | seagis_quality.save_snapshot |
| Reader | seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:35` |

#### `seagis_quality.snapshot_input.snapshot_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | true / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (snapshot_id) REFERENCES seagis_quality.alignment_snapshot(id) |
| Arti bisnis / teknis | Referensi snapshot induk |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | A3 document.rows[].cells[].lineage → `saved snapshot UUID` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:35`; catalog seagis_quality.snapshot_input.snapshot_id |

#### `seagis_quality.snapshot_input.aligned_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | NOT FOUND |
| PK / unique | true / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Jam UTC baris alignment |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | A3 document.rows[].cells[].lineage → `row.at::timestamptz` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:35`; catalog seagis_quality.snapshot_input.aligned_at |

#### `seagis_quality.snapshot_input.source_ref`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | true / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Referensi typed observation:uuid atau forecast_value:uuid |
| Valid values / checks | CHECK (source_ref =<br>CASE<br>    WHEN observation_id IS NOT NULL THEN 'observation:'::text &#124;&#124; observation_id<br>    ELSE 'forecast_value:'::text &#124;&#124; forecast_value_id<br>END) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | A3 document.rows[].cells[].lineage → `lineage ref` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:35`; catalog seagis_quality.snapshot_input.source_ref |

#### `seagis_quality.snapshot_input.observation_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (observation_id) REFERENCES seagis.observation(id) |
| Arti bisnis / teknis | Referensi pembacaan sensor lokal |
| Valid values / checks | CHECK (num_nonnulls(observation_id, forecast_value_id) = 1); CHECK (source_ref =<br>CASE<br>    WHEN observation_id IS NOT NULL THEN 'observation:'::text &#124;&#124; observation_id<br>    ELSE 'forecast_value:'::text &#124;&#124; forecast_value_id<br>END) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | A3 document.rows[].cells[].lineage → `UUID if ref prefix observation else NULL` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:35`; catalog seagis_quality.snapshot_input.observation_id |

#### `seagis_quality.snapshot_input.forecast_value_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (forecast_value_id) REFERENCES seagis.forecast_value(id) |
| Arti bisnis / teknis | Referensi satu nilai model regional |
| Valid values / checks | CHECK (num_nonnulls(observation_id, forecast_value_id) = 1); CHECK (source_ref =<br>CASE<br>    WHEN observation_id IS NOT NULL THEN 'observation:'::text &#124;&#124; observation_id<br>    ELSE 'forecast_value:'::text &#124;&#124; forecast_value_id<br>END) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | A3 document.rows[].cells[].lineage → `UUID if ref prefix forecast_value else NULL` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:35`; catalog seagis_quality.snapshot_input.forecast_value_id |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK (num_nonnulls(observation_id, forecast_value_id) = 1);
CHECK (source_ref =
CASE
    WHEN observation_id IS NOT NULL THEN 'observation:'::text || observation_id
    ELSE 'forecast_value:'::text || forecast_value_id
END);
FOREIGN KEY (forecast_value_id) REFERENCES seagis.forecast_value(id);
FOREIGN KEY (observation_id) REFERENCES seagis.observation(id);
PRIMARY KEY (snapshot_id, aligned_at, source_ref);
FOREIGN KEY (snapshot_id) REFERENCES seagis_quality.alignment_snapshot(id);
```

**indexes**

```sql
CREATE UNIQUE INDEX snapshot_input_pkey ON seagis_quality.snapshot_input USING btree (snapshot_id, aligned_at, source_ref);
```

**triggers**

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis_quality.snapshot_input FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
```

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

### 4.29 `seagis_raw.raw_payload`

Manifest raw immutable: digest, basis hash, lisensi dan mode retensi.

| Atribut | Definisi |
| --- | --- |
| Schema / domain | seagis_raw |
| Kind | table |
| Primary key | PRIMARY KEY (id) |
| Unique | UNIQUE (id, ingestion_run_id, dataset_key, is_synthetic); UNIQUE (ingestion_run_id, sha256) |
| Rows | UNVERIFIED |
| Writer | seagis_api.ingest; seagis_environment.persist; A0 fixtures |
| Reader | A3 source_bundle; provenance guards |
| Otoritas | Record domain ini; registry/config atau sumber asal tetap ditelusuri |
| Lifecycle | Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:110` |

#### `seagis_raw.raw_payload.id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | `gen_random_uuid()` |
| PK / unique | true / true (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Identitas baris menurut PK tabel |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | DB default / explicit UUID → `gen_random_uuid()` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:110`; catalog seagis_raw.raw_payload.id |

#### `seagis_raw.raw_payload.ingestion_run_id`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `uuid` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.ingestion_run(id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Referensi ingestion asal |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 00000000-0000-4000-8000-000000000001 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:193` → `run_id` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:110`; catalog seagis_raw.raw_payload.ingestion_run_id |

#### `seagis_raw.raw_payload.dataset_key`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.ingestion_run(id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Kunci dataset terdaftar |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:193` → `s.dataset_key` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:110`; catalog seagis_raw.raw_payload.dataset_key |

#### `seagis_raw.raw_payload.is_synthetic`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `boolean` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | FOREIGN KEY (ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.ingestion_run(id, dataset_key, is_synthetic) |
| Arti bisnis / teknis | Penanda asal sintetis, terpisah dari QC |
| Valid values / checks | CHECK (storage_mode <> 'inline'::text OR is_synthetic AND (hash_basis = ANY (ARRAY['synthetic_json_canonical_v1'::text, 'jsonb_utf8_v1'::text]))) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | true |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:193` → `s.is_synthetic` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:110`; catalog seagis_raw.raw_payload.is_synthetic |

#### `seagis_raw.raw_payload.sha256`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Digest raw sesuai hash_basis, bukan selalu byte jaringan |
| Valid values / checks | CHECK (sha256 ~ '^[0-9a-f]{64}$'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:193` → `CASE WHEN s.is_synthetic THEN seagis.jsonb_sha256(packet) ELSE wire_sha256 END` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:110`; catalog seagis_raw.raw_payload.sha256 |

#### `seagis_raw.raw_payload.hash_basis`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | `'source_bytes'::text` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Aturan byte/serialisasi yang di-hash |
| Valid values / checks | CHECK (hash_basis = ANY (ARRAY['source_bytes'::text, 'synthetic_json_canonical_v1'::text, 'jsonb_utf8_v1'::text, 'toolbox_subset_json_v1'::text])); CHECK (storage_mode <> 'inline'::text OR is_synthetic AND (hash_basis = ANY (ARRAY['synthetic_json_canonical_v1'::text, 'jsonb_utf8_v1'::text]))) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | caller / SQL default → `'source_bytes'::text` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:110`; catalog seagis_raw.raw_payload.hash_basis |

#### `seagis_raw.raw_payload.received_at`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `timestamp with time zone` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Instan penerimaan raw oleh worker |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity. |
| Example | 2026-10-21T12:00:00Z |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:193` → `received` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:110`; catalog seagis_raw.raw_payload.received_at |

#### `seagis_raw.raw_payload.storage_mode`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | inline, object atau metadata_only menentukan lokasi konten |
| Valid values / checks | CHECK (storage_mode = 'inline'::text AND payload IS NOT NULL AND object_uri IS NULL OR storage_mode = 'object'::text AND payload IS NULL AND object_uri IS NOT NULL AND object_uri ~~ 'storage://%'::text OR storage_mode = 'metadata_only'::text AND payload IS NULL AND object_uri IS NULL); CHECK (storage_mode <> 'inline'::text OR is_synthetic AND (hash_basis = ANY (ARRAY['synthetic_json_canonical_v1'::text, 'jsonb_utf8_v1'::text]))); CHECK (storage_mode = ANY (ARRAY['inline'::text, 'object'::text, 'metadata_only'::text])) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:193` → `CASE WHEN s.is_synthetic THEN 'inline' ELSE 'metadata_only' END` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:110`; catalog seagis_raw.raw_payload.storage_mode |

#### `seagis_raw.raw_payload.payload`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `jsonb` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Konten JSON raw sintetis bila inline |
| Valid values / checks | CHECK (storage_mode = 'inline'::text AND payload IS NOT NULL AND object_uri IS NULL OR storage_mode = 'object'::text AND payload IS NULL AND object_uri IS NOT NULL AND object_uri ~~ 'storage://%'::text OR storage_mode = 'metadata_only'::text AND payload IS NULL AND object_uri IS NULL) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | {} |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:193` → `CASE WHEN s.is_synthetic THEN packet ELSE NULL END` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:110`; catalog seagis_raw.raw_payload.payload |

#### `seagis_raw.raw_payload.object_uri`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / true |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Referensi privat objek bila mode object |
| Valid values / checks | CHECK (storage_mode = 'inline'::text AND payload IS NOT NULL AND object_uri IS NULL OR storage_mode = 'object'::text AND payload IS NULL AND object_uri IS NOT NULL AND object_uri ~~ 'storage://%'::text OR storage_mode = 'metadata_only'::text AND payload IS NULL AND object_uri IS NULL) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | active loader omits column / nullable schema → `NULL in inspected A1/A2 path; other callers may supply under schema guards` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:110`; catalog seagis_raw.raw_payload.object_uri |

#### `seagis_raw.raw_payload.byte_size`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `bigint` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Ukuran byte yang dilaporkan pada capture |
| Valid values / checks | CHECK (byte_size >= 0) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | 1 |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:193` → `wire_bytes` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:110`; catalog seagis_raw.raw_payload.byte_size |

#### `seagis_raw.raw_payload.format`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Media type/format representasi raw |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:193` → `'application/json'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:110`; catalog seagis_raw.raw_payload.format |

#### `seagis_raw.raw_payload.licence_snapshot`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `text` / false |
| Default / generated | NOT FOUND |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Keterangan lisensi saat capture |
| Valid values / checks | Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid |
| Asal / transformasi | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:193` → `'project-owned; A1 synthetic development / real retention gated'` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:110`; catalog seagis_raw.raw_payload.licence_snapshot |

#### `seagis_raw.raw_payload.provider_metadata`

| Atribut | Definisi |
| --- | --- |
| Type / nullable | `jsonb` / false |
| Default / generated | `'{}'::jsonb` |
| PK / unique | false / false (unique satu kolom; composite di bawah) |
| FK | NOT APPLICABLE |
| Arti bisnis / teknis | Metadata provider/request tersanitasi |
| Valid values / checks | CHECK (jsonb_typeof(provider_metadata) = 'object'::text) |
| Units / time | NOT APPLICABLE; NOT APPLICABLE |
| Example | {} |
| Asal / transformasi | caller / SQL default → `'{}'::jsonb` (VERIFIED) |
| Mutasi / konsumen | Mengikuti trigger/mutasi tabel, bukan asumsi mutable; A3 source_bundle; provenance guards |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:110`; catalog seagis_raw.raw_payload.provider_metadata |

#### Constraint, indeks dan trigger

**constraints**

```sql
CHECK (byte_size >= 0);
CHECK (storage_mode = 'inline'::text AND payload IS NOT NULL AND object_uri IS NULL OR storage_mode = 'object'::text AND payload IS NULL AND object_uri IS NOT NULL AND object_uri ~~ 'storage://%'::text OR storage_mode = 'metadata_only'::text AND payload IS NULL AND object_uri IS NULL);
CHECK (hash_basis = ANY (ARRAY['source_bytes'::text, 'synthetic_json_canonical_v1'::text, 'jsonb_utf8_v1'::text, 'toolbox_subset_json_v1'::text]));
UNIQUE (id, ingestion_run_id, dataset_key, is_synthetic);
FOREIGN KEY (ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.ingestion_run(id, dataset_key, is_synthetic);
UNIQUE (ingestion_run_id, sha256);
CHECK (storage_mode <> 'inline'::text OR is_synthetic AND (hash_basis = ANY (ARRAY['synthetic_json_canonical_v1'::text, 'jsonb_utf8_v1'::text])));
PRIMARY KEY (id);
CHECK (jsonb_typeof(provider_metadata) = 'object'::text);
CHECK (sha256 ~ '^[0-9a-f]{64}$'::text);
CHECK (storage_mode = ANY (ARRAY['inline'::text, 'object'::text, 'metadata_only'::text]));
```

**indexes**

```sql
CREATE UNIQUE INDEX raw_payload_id_ingestion_run_id_dataset_key_is_synthetic_key ON seagis_raw.raw_payload USING btree (id, ingestion_run_id, dataset_key, is_synthetic);
CREATE UNIQUE INDEX raw_payload_ingestion_run_id_sha256_key ON seagis_raw.raw_payload USING btree (ingestion_run_id, sha256);
CREATE UNIQUE INDEX raw_payload_pkey ON seagis_raw.raw_payload USING btree (id);
```

**triggers**

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis_raw.raw_payload FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
CREATE TRIGGER guard_raw BEFORE INSERT ON seagis_raw.raw_payload FOR EACH ROW EXECUTE FUNCTION seagis.guard_raw();
```

RLS pada snapshot: True; FORCE RLS: False. Membership/grant terkini UNVERIFIED.

