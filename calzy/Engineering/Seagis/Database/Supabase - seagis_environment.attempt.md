---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis_environment.attempt

Riwayat satu percobaan ingestion regional, beserta waktu, hasil/error dan run yang dihasilkan bila ada. ID juga digunakan dalam mekanisme lease worker.

- Jenis: tabel PostgreSQL. Schema: `seagis_environment`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | Tidak | — | Identitas baris; lihat PK/default dan constraint khusus tabel. |
| `dataset_key` | `text` | Tidak | — | Identitas dataset dalam registri Seagis. |
| `started_at` | `timestamp with time zone` | Tidak | — | Waktu mulai proses/percobaan. |
| `completed_at` | `timestamp with time zone` | Ya | — | Waktu selesai; boleh NULL selama running. |
| `status` | `text` | Tidak | — | Status siklus hidup; lihat pilihan pada CHECK. |
| `error_code` | `text` | Ya | — | Kode kegagalan bila ada. |
| `forecast_run_id` | `uuid` | Ya | — | Identitas vintage/run regional. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `attempt_check`

```sql
CHECK ((completed_at IS NULL) = (status = 'running'::text))
```

- `attempt_pkey`

```sql
PRIMARY KEY (id)
```

- `attempt_status_check`

```sql
CHECK (status = ANY (ARRAY['running'::text, 'succeeded'::text, 'duplicate'::text, 'failed'::text, 'abandoned'::text]))
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis_environment.attempt]] (dataset_key) | [[Supabase - seagis_environment.policy]] (dataset_key) | Wajib; 0..N anak per induk |
| [[Supabase - seagis_environment.attempt]] (forecast_run_id) | [[Supabase - seagis.forecast_run]] (id) | Opsional / MATCH SIMPLE; 0..N anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (dataset_key) REFERENCES seagis_environment.policy(dataset_key);
FOREIGN KEY (forecast_run_id) REFERENCES seagis.forecast_run(id);
```

## Relasi masuk

Tidak ada FK dari tabel lain menuju objek ini.

## Indeks

```sql
CREATE UNIQUE INDEX attempt_pkey ON seagis_environment.attempt USING btree (id);
```

## Trigger dan batas mutasi

Tidak ada user trigger pada objek ini dalam snapshot catalog. Pembatasan akses dan rutin API tetap dapat membatasi penulisan.

## Akses

RLS: **aktif**. FORCE RLS: **tidak aktif**. RLS aktif tidak berarti semua role boleh membaca tabel; owner/role dengan bypass memiliki perilaku tersendiri. Snapshot ini tidak mengekspor daftar role membership maupun seluruh privilege.

Tidak ada policy RLS tercatat untuk tabel ini. Role biasa yang terkena RLS tidak mendapat izin row melalui policy; jalur runtime menggunakan routine privat sesuai dokumentasi A1/A2/A3.

## Sumber dan batas snapshot

Metadata: [schema-metadata-20261022.json](schema-metadata-20261022.json), diambil melalui SELECT catalog dalam transaksi READ ONLY; tidak menyalin isi tabel.

Source implementasi: [migrasi Seagis-Model](https://github.com/De-Voeux/Seagis-Model/tree/e93a005c95d746e6e33a6adad12760e94eb8a6cf/supabase/migrations), commit `e93a005c95d746e6e33a6adad12760e94eb8a6cf`. Penjelasan fungsi tabel diturunkan dari migrasi dan handover A0–A3; definisi kolom/constraint mengikuti catalog live. Snapshot tidak otomatis diperbarui bila database berubah.
