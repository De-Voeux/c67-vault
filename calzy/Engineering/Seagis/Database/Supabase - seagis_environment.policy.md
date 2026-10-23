---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis_environment.policy

Kebijakan ingestion per dataset regional: izin prototype, lisensi, atribusi, jadwal pembaruan, stale dan retention metadata_only.

- Jenis: tabel PostgreSQL. Schema: `seagis_environment`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `dataset_key` | `text` | Tidak | — | Identitas dataset dalam registri Seagis. |
| `enabled` | `boolean` | Tidak | `true` | Flag kebijakan ingestion aktif. |
| `purpose` | `text` | Tidak | — | Tujuan penggunaan yang diizinkan kebijakan. |
| `licence_url` | `text` | Tidak | — | URL ketentuan lisensi. |
| `terms_review` | `text` | Tidak | — | Identitas/catatan peninjauan ketentuan provider. |
| `attribution` | `text` | Tidak | — | Teks atribusi penyedia. |
| `update_seconds` | `integer` | Tidak | — | Periode pembaruan provider untuk scheduling, detik. |
| `release_offset_seconds` | `integer` | Tidak | — | Offset jadwal rilis dalam periode, detik. |
| `stale_seconds` | `integer` | Tidak | — | Batas stale dataset regional, detik. |
| `retention_mode` | `text` | Tidak | `'metadata_only'::text` | Kebijakan retensi raw operasional. |
| `reviewed_at` | `timestamp with time zone` | Tidak | `now()` | Waktu peninjauan kebijakan. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `policy_check`

```sql
CHECK (release_offset_seconds >= 0 AND release_offset_seconds < update_seconds)
```

- `policy_check1`

```sql
CHECK (stale_seconds >= update_seconds)
```

- `policy_pkey`

```sql
PRIMARY KEY (dataset_key)
```

- `policy_purpose_check`

```sql
CHECK (purpose = 'noncommercial_educational_prototype'::text)
```

- `policy_retention_mode_check`

```sql
CHECK (retention_mode = 'metadata_only'::text)
```

- `policy_update_seconds_check`

```sql
CHECK (update_seconds >= 21600)
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis_environment.policy]] (dataset_key) | [[Supabase - seagis.dataset]] (dataset_key) | Wajib; maksimal 1 anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (dataset_key) REFERENCES seagis.dataset(dataset_key);
```

## Relasi masuk

- [[Supabase - seagis_environment.attempt]]: `(dataset_key)` → `(dataset_key)`.
- [[Supabase - seagis_environment.demo_grid_mapping]]: `(dataset_key)` → `(dataset_key)`.
- [[Supabase - seagis_environment.schedule_state]]: `(dataset_key)` → `(dataset_key)`.

## Indeks

```sql
CREATE UNIQUE INDEX policy_pkey ON seagis_environment.policy USING btree (dataset_key);
```

## Trigger dan batas mutasi

Tidak ada user trigger pada objek ini dalam snapshot catalog. Pembatasan akses dan rutin API tetap dapat membatasi penulisan.

## Akses

RLS: **aktif**. FORCE RLS: **tidak aktif**. RLS aktif tidak berarti semua role boleh membaca tabel; owner/role dengan bypass memiliki perilaku tersendiri. Snapshot ini tidak mengekspor daftar role membership maupun seluruh privilege.

Tidak ada policy RLS tercatat untuk tabel ini. Role biasa yang terkena RLS tidak mendapat izin row melalui policy; jalur runtime menggunakan routine privat sesuai dokumentasi A1/A2/A3.

## Sumber dan batas snapshot

Metadata: [schema-metadata-20261022.json](schema-metadata-20261022.json), diambil melalui SELECT catalog dalam transaksi READ ONLY; tidak menyalin isi tabel.

Source implementasi: [migrasi Seagis-Model](https://github.com/De-Voeux/Seagis-Model/tree/e93a005c95d746e6e33a6adad12760e94eb8a6cf/supabase/migrations), commit `e93a005c95d746e6e33a6adad12760e94eb8a6cf`. Penjelasan fungsi tabel diturunkan dari migrasi dan handover A0–A3; definisi kolom/constraint mengikuti catalog live. Snapshot tidak otomatis diperbarui bila database berubah.
