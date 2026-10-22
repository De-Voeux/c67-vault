---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis.ingestion_run

Catatan satu proses ingestion beserta identitas request, versi adapter, waktu, status dan penanda sintetis. Menjadi akar lineage data yang masuk.

- Jenis: tabel PostgreSQL. Schema: `seagis`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | Tidak | `gen_random_uuid()` | Identitas baris; lihat PK/default dan constraint khusus tabel. |
| `dataset_key` | `text` | Tidak | — | Identitas dataset dalam registri Seagis. |
| `request_key` | `text` | Tidak | — | Kunci idempotensi request ingestion per dataset. |
| `adapter_version` | `text` | Tidak | — | Versi adapter ingestion. |
| `started_at` | `timestamp with time zone` | Tidak | — | Waktu mulai proses/percobaan. |
| `completed_at` | `timestamp with time zone` | Ya | — | Waktu selesai; boleh NULL selama running. |
| `status` | `text` | Tidak | — | Status siklus hidup; lihat pilihan pada CHECK. |
| `is_synthetic` | `boolean` | Tidak | — | Penanda data/identitas sintetis; tidak disamakan dengan data lapangan. |
| `error_code` | `text` | Ya | — | Kode kegagalan bila ada. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `ingestion_run_check`

```sql
CHECK (completed_at IS NULL OR completed_at >= started_at)
```

- `ingestion_run_check1`

```sql
CHECK ((status = 'running'::text) = (completed_at IS NULL))
```

- `ingestion_run_dataset_key_request_key_key`

```sql
UNIQUE (dataset_key, request_key)
```

- `ingestion_run_id_dataset_key_is_synthetic_key`

```sql
UNIQUE (id, dataset_key, is_synthetic)
```

- `ingestion_run_pkey`

```sql
PRIMARY KEY (id)
```

- `ingestion_run_status_check`

```sql
CHECK (status = ANY (ARRAY['running'::text, 'succeeded'::text, 'partial'::text, 'failed'::text]))
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis.ingestion_run]] (dataset_key) | [[Supabase - seagis.dataset]] (dataset_key) | Wajib; 0..N anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (dataset_key) REFERENCES seagis.dataset(dataset_key);
```

## Relasi masuk

- [[Supabase - seagis.quality_event]]: `(ingestion_run_id, dataset_key, is_synthetic)` → `(id, dataset_key, is_synthetic)`.
- [[Supabase - seagis_api.packet_receipt]]: `(ingestion_run_id)` → `(id)`.
- [[Supabase - seagis_raw.raw_payload]]: `(ingestion_run_id, dataset_key, is_synthetic)` → `(id, dataset_key, is_synthetic)`.

## Indeks

```sql
CREATE UNIQUE INDEX ingestion_run_dataset_key_request_key_key ON seagis.ingestion_run USING btree (dataset_key, request_key);
CREATE UNIQUE INDEX ingestion_run_id_dataset_key_is_synthetic_key ON seagis.ingestion_run USING btree (id, dataset_key, is_synthetic);
CREATE UNIQUE INDEX ingestion_run_pkey ON seagis.ingestion_run USING btree (id);
```

## Trigger dan batas mutasi

```sql
CREATE TRIGGER guard_ingestion BEFORE INSERT OR UPDATE ON seagis.ingestion_run FOR EACH ROW EXECUTE FUNCTION seagis.guard_ingestion();
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
