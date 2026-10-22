---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis.quality_event

Catatan event kualitas engineering pada ingestion, observasi atau nilai regional. Severity warning bukan label bahaya ice-ice.

- Jenis: tabel PostgreSQL. Schema: `seagis`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | Tidak | `gen_random_uuid()` | Identitas baris; lihat PK/default dan constraint khusus tabel. |
| `ingestion_run_id` | `uuid` | Tidak | — | Identitas proses ingestion asal. |
| `dataset_key` | `text` | Tidak | — | Identitas dataset dalam registri Seagis. |
| `is_synthetic` | `boolean` | Tidak | — | Penanda data/identitas sintetis; tidak disamakan dengan data lapangan. |
| `event_key` | `text` | Tidak | — | Kunci event kualitas per ingestion. |
| `observation_id` | `uuid` | Ya | — | Identitas observasi sensor sumber. |
| `forecast_value_id` | `uuid` | Ya | — | Identitas nilai regional sumber. |
| `event_code` | `text` | Tidak | — | Kode temuan QC. |
| `severity` | `text` | Tidak | — | Tingkat event engineering: info, warning atau error. |
| `details` | `jsonb` | Tidak | `'{}'::jsonb` | Rincian event dalam objek JSON. |
| `created_at` | `timestamp with time zone` | Tidak | `now()` | Waktu pembuatan/pencatatan baris. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `quality_event_check`

```sql
CHECK (num_nonnulls(observation_id, forecast_value_id) <= 1)
```

- `quality_event_details_check`

```sql
CHECK (jsonb_typeof(details) = 'object'::text)
```

- `quality_event_ingestion_run_id_event_key_key`

```sql
UNIQUE (ingestion_run_id, event_key)
```

- `quality_event_pkey`

```sql
PRIMARY KEY (id)
```

- `quality_event_severity_check`

```sql
CHECK (severity = ANY (ARRAY['info'::text, 'warning'::text, 'error'::text]))
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis.quality_event]] (forecast_value_id, dataset_key, is_synthetic) | [[Supabase - seagis.forecast_value]] (id, dataset_key, is_synthetic) | Opsional / MATCH SIMPLE; 0..N anak per induk |
| [[Supabase - seagis.quality_event]] (ingestion_run_id, dataset_key, is_synthetic) | [[Supabase - seagis.ingestion_run]] (id, dataset_key, is_synthetic) | Wajib; 0..N anak per induk |
| [[Supabase - seagis.quality_event]] (observation_id, ingestion_run_id, dataset_key, is_synthetic) | [[Supabase - seagis.observation]] (id, ingestion_run_id, dataset_key, is_synthetic) | Opsional / MATCH SIMPLE; 0..N anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (forecast_value_id, dataset_key, is_synthetic) REFERENCES seagis.forecast_value(id, dataset_key, is_synthetic);
FOREIGN KEY (ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.ingestion_run(id, dataset_key, is_synthetic);
FOREIGN KEY (observation_id, ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.observation(id, ingestion_run_id, dataset_key, is_synthetic);
```

## Relasi masuk

Tidak ada FK dari tabel lain menuju objek ini.

## Indeks

```sql
CREATE INDEX quality_event_forecast ON seagis.quality_event USING btree (forecast_value_id) WHERE (forecast_value_id IS NOT NULL);
CREATE UNIQUE INDEX quality_event_ingestion_run_id_event_key_key ON seagis.quality_event USING btree (ingestion_run_id, event_key);
CREATE INDEX quality_event_observation ON seagis.quality_event USING btree (observation_id) WHERE (observation_id IS NOT NULL);
CREATE UNIQUE INDEX quality_event_pkey ON seagis.quality_event USING btree (id);
```

## Trigger dan batas mutasi

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis.quality_event FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
CREATE TRIGGER guard_quality BEFORE INSERT ON seagis.quality_event FOR EACH ROW EXECUTE FUNCTION seagis.guard_quality_event();
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
