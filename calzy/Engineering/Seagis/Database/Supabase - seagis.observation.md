---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis.observation

Nilai observasi sensor suhu air per plot dan waktu. Mempertahankan nilai asli/normalisasi, status ketersediaan, QC dan lineage raw. Tidak menyimpan kesimpulan biologis dari suhu.

- Jenis: tabel PostgreSQL. Schema: `seagis`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Cara membaca

Contoh data “sensor tambak A, 09.30, 26°C” masuk sebagai nilai suhu dengan observed_at dan identitas sensor/plot. Penyimpanan tersebut tidak otomatis berarti suhu rendah, menurun, aman atau waspada. Status quality_status adalah QC data.

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | Tidak | `gen_random_uuid()` | Identitas baris; lihat PK/default dan constraint khusus tabel. |
| `plot_id` | `uuid` | Tidak | — | Identitas plot budidaya terkait. |
| `sensor_id` | `uuid` | Tidak | — | Identitas sensor terkait. |
| `dataset_key` | `text` | Tidak | — | Identitas dataset dalam registri Seagis. |
| `ingestion_run_id` | `uuid` | Tidak | — | Identitas proses ingestion asal. |
| `raw_payload_id` | `uuid` | Tidak | — | Identitas manifest raw asal. |
| `is_synthetic` | `boolean` | Tidak | — | Penanda data/identitas sintetis; tidak disamakan dengan data lapangan. |
| `source_record_key` | `text` | Tidak | — | Identitas record/paket sumber per sensor. |
| `parameter_code` | `text` | Tidak | — | Kode parameter lingkungan. |
| `native_value` | `seagis.finite_float` | Ya | — | Nilai dalam satuan asli. |
| `native_unit` | `text` | Tidak | — | Satuan asli sumber. |
| `value` | `seagis.finite_float` | Ya | — | Nilai hasil normalisasi; NULL mengikuti value_status. |
| `unit` | `text` | Tidak | — | Satuan nilai normalisasi. |
| `conversion_code` | `text` | Tidak | — | Identitas aturan konversi. |
| `value_status` | `text` | Tidak | — | Status nilai: present, missing, not_available atau below_detection_limit menurut guard. |
| `detection_limit` | `seagis.finite_float` | Ya | — | Batas deteksi bila value_status menggunakannya. |
| `observed_at` | `timestamp with time zone` | Tidak | — | Waktu pengukuran sensor, bukan waktu diterima server. |
| `ingested_at` | `timestamp with time zone` | Tidak | — | Waktu data masuk sistem. |
| `quality_status` | `text` | Tidak | — | Status QC data, bukan status kesehatan rumput laut. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `observation_check`

```sql
CHECK (seagis.valid_value(value::double precision, native_value::double precision, value_status, detection_limit::double precision))
```

- `observation_id_ingestion_run_id_dataset_key_is_synthetic_key`

```sql
UNIQUE (id, ingestion_run_id, dataset_key, is_synthetic)
```

- `observation_parameter_code_check`

```sql
CHECK (parameter_code = 'water_temperature'::text)
```

- `observation_pkey`

```sql
PRIMARY KEY (id)
```

- `observation_quality_status_check`

```sql
CHECK (quality_status = ANY (ARRAY['unreviewed'::text, 'accepted'::text, 'suspect'::text, 'rejected'::text]))
```

- `observation_sensor_id_parameter_code_source_record_key_key`

```sql
UNIQUE (sensor_id, parameter_code, source_record_key)
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis.observation]] (dataset_key, parameter_code, native_unit, unit, conversion_code) | [[Supabase - seagis.dataset_parameter]] (dataset_key, parameter_code, native_unit, unit, conversion_code) | Wajib; 0..N anak per induk |
| [[Supabase - seagis.observation]] (raw_payload_id, ingestion_run_id, dataset_key, is_synthetic) | [[Supabase - seagis_raw.raw_payload]] (id, ingestion_run_id, dataset_key, is_synthetic) | Wajib; 0..N anak per induk |
| [[Supabase - seagis.observation]] (sensor_id, plot_id, dataset_key, is_synthetic) | [[Supabase - seagis.sensor]] (id, plot_id, dataset_key, is_synthetic) | Wajib; 0..N anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (dataset_key, parameter_code, native_unit, unit, conversion_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code, native_unit, unit, conversion_code);
FOREIGN KEY (raw_payload_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis_raw.raw_payload(id, ingestion_run_id, dataset_key, is_synthetic);
FOREIGN KEY (sensor_id, plot_id, dataset_key, is_synthetic) REFERENCES seagis.sensor(id, plot_id, dataset_key, is_synthetic);
```

## Relasi masuk

- [[Supabase - seagis.quality_event]]: `(observation_id, ingestion_run_id, dataset_key, is_synthetic)` → `(id, ingestion_run_id, dataset_key, is_synthetic)`.
- [[Supabase - seagis_api.packet_receipt]]: `(observation_id)` → `(id)`.
- [[Supabase - seagis_features.feature_input]]: `(observation_id)` → `(id)`.
- [[Supabase - seagis_quality.snapshot_input]]: `(observation_id)` → `(id)`.

## Indeks

```sql
CREATE UNIQUE INDEX observation_id_ingestion_run_id_dataset_key_is_synthetic_key ON seagis.observation USING btree (id, ingestion_run_id, dataset_key, is_synthetic);
CREATE INDEX observation_ingestion ON seagis.observation USING btree (ingestion_run_id);
CREATE UNIQUE INDEX observation_pkey ON seagis.observation USING btree (id);
CREATE INDEX observation_plot_time ON seagis.observation USING btree (plot_id, parameter_code, observed_at DESC);
CREATE UNIQUE INDEX observation_sensor_id_parameter_code_source_record_key_key ON seagis.observation USING btree (sensor_id, parameter_code, source_record_key);
```

## Trigger dan batas mutasi

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis.observation FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
CREATE TRIGGER guard_observation BEFORE INSERT ON seagis.observation FOR EACH ROW EXECUTE FUNCTION seagis.guard_measurement();
```

Definisi di atas menunjukkan routine guard yang dipanggil. Isi routine selengkapnya berada pada migrasi source; CHECK/FK saja tidak menggambarkan semua guard lintas tabel.

## Akses

RLS: **aktif**. FORCE RLS: **tidak aktif**. RLS aktif tidak berarti semua role boleh membaca tabel; owner/role dengan bypass memiliki perilaku tersendiri. Snapshot ini tidak mengekspor daftar role membership maupun seluruh privilege.

| Policy | Role | Command | USING | WITH CHECK |
| --- | --- | --- | --- | --- |
| `backend_only` | `service_role` | `ALL` | `true` | `true` |

## Sumber dan batas snapshot

Metadata: [schema-metadata-20261022.json](schema-metadata-20261022.json), diambil melalui SELECT catalog dalam transaksi READ ONLY; tidak menyalin isi tabel.

Source implementasi: [migrasi Seagis-Model](https://github.com/De-Voeux/Seagis-Model/tree/e93a005c95d746e6e33a6adad12760e94eb8a6cf/supabase/migrations), commit `e93a005c95d746e6e33a6adad12760e94eb8a6cf`. Penjelasan fungsi tabel diturunkan dari migrasi dan handover A0–A3; definisi kolom/constraint mengikuti catalog live. Snapshot tidak otomatis diperbarui bila database berubah.
