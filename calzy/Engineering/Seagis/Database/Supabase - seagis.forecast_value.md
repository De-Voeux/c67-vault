---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis.forecast_value

Nilai parameter pada grid dan waktu berlaku dari satu run regional. Nilai ini merupakan konteks model regional; bukan pengukuran langsung di tambak.

- Jenis: tabel PostgreSQL. Schema: `seagis`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Cara membaca

valid_at adalah waktu kondisi model berlaku; ingested_at adalah waktu nilai masuk sistem. period_start_at/period_end_at dan temporal_support membedakan nilai sesaat, rerata dan akumulasi. NULL mengikuti value_status, bukan diubah menjadi angka nol.

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | Tidak | `gen_random_uuid()` | Identitas baris; lihat PK/default dan constraint khusus tabel. |
| `forecast_run_id` | `uuid` | Tidak | — | Identitas vintage/run regional. |
| `source_grid_id` | `uuid` | Tidak | — | Identitas sel/titik grid sumber. |
| `dataset_key` | `text` | Tidak | — | Identitas dataset dalam registri Seagis. |
| `is_synthetic` | `boolean` | Tidak | — | Penanda data/identitas sintetis; tidak disamakan dengan data lapangan. |
| `parameter_code` | `text` | Tidak | — | Kode parameter lingkungan. |
| `native_value` | `seagis.finite_float` | Ya | — | Nilai dalam satuan asli. |
| `native_unit` | `text` | Tidak | — | Satuan asli sumber. |
| `value` | `seagis.finite_float` | Ya | — | Nilai hasil normalisasi; NULL mengikuti value_status. |
| `unit` | `text` | Tidak | — | Satuan nilai normalisasi. |
| `conversion_code` | `text` | Tidak | — | Identitas aturan konversi. |
| `value_status` | `text` | Tidak | — | Status nilai: present, missing, not_available atau below_detection_limit menurut guard. |
| `detection_limit` | `seagis.finite_float` | Ya | — | Batas deteksi bila value_status menggunakannya. |
| `valid_at` | `timestamp with time zone` | Tidak | — | Waktu nilai model berlaku. |
| `ingested_at` | `timestamp with time zone` | Tidak | — | Waktu data masuk sistem. |
| `temporal_support` | `text` | Tidak | — | Makna temporal: instantaneous, mean atau sum. |
| `interval_status` | `text` | Tidak | — | Apakah interval agregasi diketahui, tidak diketahui atau tidak relevan. |
| `period_start_at` | `timestamp with time zone` | Ya | — | Awal interval agregasi bila diketahui. |
| `period_end_at` | `timestamp with time zone` | Ya | — | Akhir interval agregasi bila diketahui. |
| `quality_status` | `text` | Tidak | — | Status QC data, bukan status kesehatan rumput laut. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `forecast_value_check`

```sql
CHECK (seagis.valid_value(value::double precision, native_value::double precision, value_status, detection_limit::double precision))
```

- `forecast_value_check1`

```sql
CHECK (seagis.valid_support(valid_at, temporal_support, interval_status, period_start_at, period_end_at))
```

- `forecast_value_forecast_run_id_source_grid_id_parameter_cod_key`

```sql
UNIQUE (forecast_run_id, source_grid_id, parameter_code, valid_at)
```

- `forecast_value_id_dataset_key_is_synthetic_key`

```sql
UNIQUE (id, dataset_key, is_synthetic)
```

- `forecast_value_pkey`

```sql
PRIMARY KEY (id)
```

- `forecast_value_quality_status_check`

```sql
CHECK (quality_status = ANY (ARRAY['unreviewed'::text, 'accepted'::text, 'suspect'::text, 'rejected'::text]))
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis.forecast_value]] (dataset_key, parameter_code, native_unit, unit, conversion_code) | [[Supabase - seagis.dataset_parameter]] (dataset_key, parameter_code, native_unit, unit, conversion_code) | Wajib; 0..N anak per induk |
| [[Supabase - seagis.forecast_value]] (forecast_run_id, dataset_key, is_synthetic) | [[Supabase - seagis.forecast_run]] (id, dataset_key, is_synthetic) | Wajib; 0..N anak per induk |
| [[Supabase - seagis.forecast_value]] (source_grid_id, dataset_key, is_synthetic) | [[Supabase - seagis.source_grid]] (id, dataset_key, is_synthetic) | Wajib; 0..N anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (dataset_key, parameter_code, native_unit, unit, conversion_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code, native_unit, unit, conversion_code);
FOREIGN KEY (forecast_run_id, dataset_key, is_synthetic) REFERENCES seagis.forecast_run(id, dataset_key, is_synthetic);
FOREIGN KEY (source_grid_id, dataset_key, is_synthetic) REFERENCES seagis.source_grid(id, dataset_key, is_synthetic);
```

## Relasi masuk

- [[Supabase - seagis.quality_event]]: `(forecast_value_id, dataset_key, is_synthetic)` → `(id, dataset_key, is_synthetic)`.
- [[Supabase - seagis_features.feature_input]]: `(forecast_value_id)` → `(id)`.
- [[Supabase - seagis_quality.snapshot_input]]: `(forecast_value_id)` → `(id)`.

## Indeks

```sql
CREATE INDEX forecast_grid_time ON seagis.forecast_value USING btree (source_grid_id, parameter_code, valid_at DESC);
CREATE UNIQUE INDEX forecast_value_forecast_run_id_source_grid_id_parameter_cod_key ON seagis.forecast_value USING btree (forecast_run_id, source_grid_id, parameter_code, valid_at);
CREATE UNIQUE INDEX forecast_value_id_dataset_key_is_synthetic_key ON seagis.forecast_value USING btree (id, dataset_key, is_synthetic);
CREATE UNIQUE INDEX forecast_value_pkey ON seagis.forecast_value USING btree (id);
```

## Trigger dan batas mutasi

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis.forecast_value FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
CREATE TRIGGER guard_forecast_value BEFORE INSERT ON seagis.forecast_value FOR EACH ROW EXECUTE FUNCTION seagis.guard_measurement();
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
