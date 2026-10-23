---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis_environment.schedule_state

State mutable scheduler per dataset: lease, jadwal percobaan berikut, sukses terakhir, error dan hitungan kegagalan. Tabel ini bukan scheduler cloud yang berjalan sendiri.

- Jenis: tabel PostgreSQL. Schema: `seagis_environment`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `dataset_key` | `text` | Tidak | — | Identitas dataset dalam registri Seagis. |
| `lease_id` | `uuid` | Ya | — | Identitas klaim eksklusif worker. |
| `lease_until` | `timestamp with time zone` | Ya | — | Batas waktu lease worker. |
| `next_attempt_at` | `timestamp with time zone` | Tidak | `'-infinity'::timestamp with time zone` | Waktu paling awal percobaan berikutnya. |
| `last_success_at` | `timestamp with time zone` | Ya | — | Waktu sukses ingestion terakhir. |
| `last_attempt_at` | `timestamp with time zone` | Ya | — | Waktu percobaan terakhir. |
| `last_error_code` | `text` | Ya | — | Kode error terakhir. |
| `failures` | `integer` | Tidak | `0` | Jumlah kegagalan untuk backoff. |
| `last_forecast_run_id` | `uuid` | Ya | — | Run regional terakhir yang dicatat state scheduler. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `schedule_state_failures_check`

```sql
CHECK (failures >= 0)
```

- `schedule_state_pkey`

```sql
PRIMARY KEY (dataset_key)
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis_environment.schedule_state]] (dataset_key) | [[Supabase - seagis_environment.policy]] (dataset_key) | Wajib; maksimal 1 anak per induk |
| [[Supabase - seagis_environment.schedule_state]] (last_forecast_run_id) | [[Supabase - seagis.forecast_run]] (id) | Opsional / MATCH SIMPLE; 0..N anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (dataset_key) REFERENCES seagis_environment.policy(dataset_key);
FOREIGN KEY (last_forecast_run_id) REFERENCES seagis.forecast_run(id);
```

## Relasi masuk

Tidak ada FK dari tabel lain menuju objek ini.

## Indeks

```sql
CREATE UNIQUE INDEX schedule_state_pkey ON seagis_environment.schedule_state USING btree (dataset_key);
```

## Trigger dan batas mutasi

Tidak ada user trigger pada objek ini dalam snapshot catalog. Pembatasan akses dan rutin API tetap dapat membatasi penulisan.

## Akses

RLS: **aktif**. FORCE RLS: **tidak aktif**. RLS aktif tidak berarti semua role boleh membaca tabel; owner/role dengan bypass memiliki perilaku tersendiri. Snapshot ini tidak mengekspor daftar role membership maupun seluruh privilege.

Tidak ada policy RLS tercatat untuk tabel ini. Role biasa yang terkena RLS tidak mendapat izin row melalui policy; jalur runtime menggunakan routine privat sesuai dokumentasi A1/A2/A3.

## Sumber dan batas snapshot

Metadata: [schema-metadata-20261022.json](schema-metadata-20261022.json), diambil melalui SELECT catalog dalam transaksi READ ONLY; tidak menyalin isi tabel.

Source implementasi: [migrasi Seagis-Model](https://github.com/De-Voeux/Seagis-Model/tree/e93a005c95d746e6e33a6adad12760e94eb8a6cf/supabase/migrations), commit `e93a005c95d746e6e33a6adad12760e94eb8a6cf`. Penjelasan fungsi tabel diturunkan dari migrasi dan handover A0–A3; definisi kolom/constraint mengikuti catalog live. Snapshot tidak otomatis diperbarui bila database berubah.
