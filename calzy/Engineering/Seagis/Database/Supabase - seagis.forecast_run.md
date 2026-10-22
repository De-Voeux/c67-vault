---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis.forecast_run

Satu vintage/run model regional berikut asal ingestion/raw, jenis run dan waktu penerbitan yang diketahui. Nama forecast juga mencakup analysis dan analysis_forecast_unspecified.

- Jenis: tabel PostgreSQL. Schema: `seagis`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Cara membaca

issued_at boleh NULL ketika issue_time_basis=unknown. Waktu fetch/ingestion tidak boleh diklaim sebagai waktu penerbitan model.

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | Tidak | `gen_random_uuid()` | Identitas baris; lihat PK/default dan constraint khusus tabel. |
| `dataset_key` | `text` | Tidak | — | Identitas dataset dalam registri Seagis. |
| `scope` | `text` | Tidak | `'regional_model'::text` | Lingkup data: sensor lokal atau model regional sesuai CHECK. |
| `ingestion_run_id` | `uuid` | Tidak | — | Identitas proses ingestion asal. |
| `raw_payload_id` | `uuid` | Tidak | — | Identitas manifest raw asal. |
| `is_synthetic` | `boolean` | Tidak | — | Penanda data/identitas sintetis; tidak disamakan dengan data lapangan. |
| `run_key` | `text` | Tidak | — | Kunci unik run per dataset. |
| `run_kind` | `text` | Tidak | — | Jenis run: forecast, analysis atau belum dibedakan provider. |
| `provider_run_id` | `text` | Ya | — | ID run dari provider bila tersedia. |
| `model_initialized_at` | `timestamp with time zone` | Ya | — | Waktu inisialisasi model bila diketahui. |
| `issued_at` | `timestamp with time zone` | Ya | — | Waktu penerbitan model bila terverifikasi. |
| `issue_time_basis` | `text` | Tidak | — | Apakah waktu terbit terverifikasi atau unknown. |
| `ingested_at` | `timestamp with time zone` | Tidak | — | Waktu data masuk sistem. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `forecast_run_check`

```sql
CHECK ((issue_time_basis = 'unknown'::text) = (issued_at IS NULL))
```

- `forecast_run_check1`

```sql
CHECK (issued_at IS NULL OR issued_at <= ingested_at)
```

- `forecast_run_check2`

```sql
CHECK (model_initialized_at IS NULL OR model_initialized_at <= ingested_at)
```

- `forecast_run_dataset_key_run_key_key`

```sql
UNIQUE (dataset_key, run_key)
```

- `forecast_run_id_dataset_key_is_synthetic_key`

```sql
UNIQUE (id, dataset_key, is_synthetic)
```

- `forecast_run_issue_time_basis_check`

```sql
CHECK (issue_time_basis = ANY (ARRAY['provider_verified'::text, 'unknown'::text]))
```

- `forecast_run_pkey`

```sql
PRIMARY KEY (id)
```

- `forecast_run_run_kind_check`

```sql
CHECK (run_kind = ANY (ARRAY['forecast'::text, 'analysis'::text, 'analysis_forecast_unspecified'::text]))
```

- `forecast_run_scope_check`

```sql
CHECK (scope = 'regional_model'::text)
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis.forecast_run]] (dataset_key, scope) | [[Supabase - seagis.dataset]] (dataset_key, scope) | Wajib; 0..N anak per induk |
| [[Supabase - seagis.forecast_run]] (raw_payload_id, ingestion_run_id, dataset_key, is_synthetic) | [[Supabase - seagis_raw.raw_payload]] (id, ingestion_run_id, dataset_key, is_synthetic) | Wajib; 0..N anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset(dataset_key, scope);
FOREIGN KEY (raw_payload_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis_raw.raw_payload(id, ingestion_run_id, dataset_key, is_synthetic);
```

## Relasi masuk

- [[Supabase - seagis.forecast_value]]: `(forecast_run_id, dataset_key, is_synthetic)` → `(id, dataset_key, is_synthetic)`.
- [[Supabase - seagis_environment.attempt]]: `(forecast_run_id)` → `(id)`.
- [[Supabase - seagis_environment.schedule_state]]: `(last_forecast_run_id)` → `(id)`.

## Indeks

```sql
CREATE INDEX forecast_run_asof ON seagis.forecast_run USING btree (dataset_key, ingested_at DESC);
CREATE UNIQUE INDEX forecast_run_dataset_key_run_key_key ON seagis.forecast_run USING btree (dataset_key, run_key);
CREATE UNIQUE INDEX forecast_run_id_dataset_key_is_synthetic_key ON seagis.forecast_run USING btree (id, dataset_key, is_synthetic);
CREATE UNIQUE INDEX forecast_run_pkey ON seagis.forecast_run USING btree (id);
```

## Trigger dan batas mutasi

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis.forecast_run FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
CREATE TRIGGER guard_run BEFORE INSERT ON seagis.forecast_run FOR EACH ROW EXECUTE FUNCTION seagis.guard_run();
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
