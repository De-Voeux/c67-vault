---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis.plot

Identitas lokasi budidaya. Memisahkan lokasi contoh sintetis, belum disurvei, dan hasil survei; koordinat boleh belum diketahui.

- Jenis: tabel PostgreSQL. Schema: `seagis`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | Tidak | `gen_random_uuid()` | Identitas baris; lihat PK/default dan constraint khusus tabel. |
| `plot_code` | `text` | Tidak | — | Kode plot yang unik. |
| `name` | `text` | Tidak | — | Nama plot. |
| `latitude` | `seagis.finite_float` | Ya | — | Lintang lokasi, derajat. |
| `longitude` | `seagis.finite_float` | Ya | — | Bujur lokasi, derajat. |
| `is_synthetic` | `boolean` | Tidak | — | Penanda data/identitas sintetis; tidak disamakan dengan data lapangan. |
| `location_status` | `text` | Tidak | — | Status koordinat: belum disurvei, disurvei, atau sintetis. |
| `created_at` | `timestamp with time zone` | Tidak | `now()` | Waktu pembuatan/pencatatan baris. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `plot_check`

```sql
CHECK ((latitude IS NULL) = (longitude IS NULL))
```

- `plot_check1`

```sql
CHECK ((location_status = 'synthetic'::text) = is_synthetic)
```

- `plot_check2`

```sql
CHECK (location_status <> 'surveyed'::text OR latitude IS NOT NULL)
```

- `plot_id_is_synthetic_key`

```sql
UNIQUE (id, is_synthetic)
```

- `plot_latitude_check`

```sql
CHECK (latitude::double precision >= '-90'::integer::double precision AND latitude::double precision <= 90::double precision)
```

- `plot_location_status_check`

```sql
CHECK (location_status = ANY (ARRAY['not_surveyed'::text, 'surveyed'::text, 'synthetic'::text]))
```

- `plot_longitude_check`

```sql
CHECK (longitude::double precision >= '-180'::integer::double precision AND longitude::double precision <= 180::double precision)
```

- `plot_pkey`

```sql
PRIMARY KEY (id)
```

- `plot_plot_code_key`

```sql
UNIQUE (plot_code)
```

## Relasi keluar

Tidak ada foreign key yang dideklarasikan.

## Relasi masuk

- [[Supabase - seagis.plot_grid_mapping]]: `(plot_id, is_synthetic)` → `(id, is_synthetic)`.
- [[Supabase - seagis.sensor]]: `(plot_id, is_synthetic)` → `(id, is_synthetic)`.
- [[Supabase - seagis_api.reader_plot]]: `(plot_id)` → `(id)`.
- [[Supabase - seagis_environment.demo_grid_mapping]]: `(plot_id, plot_is_synthetic)` → `(id, is_synthetic)`.
- [[Supabase - seagis_features.feature_snapshot]]: `(plot_id, is_synthetic)` → `(id, is_synthetic)`.
- [[Supabase - seagis_quality.alignment_snapshot]]: `(plot_id)` → `(id)`.

## Indeks

```sql
CREATE UNIQUE INDEX plot_id_is_synthetic_key ON seagis.plot USING btree (id, is_synthetic);
CREATE UNIQUE INDEX plot_pkey ON seagis.plot USING btree (id);
CREATE UNIQUE INDEX plot_plot_code_key ON seagis.plot USING btree (plot_code);
```

## Trigger dan batas mutasi

Tidak ada user trigger pada objek ini dalam snapshot catalog. Pembatasan akses dan rutin API tetap dapat membatasi penulisan.

## Akses

RLS: **aktif**. FORCE RLS: **tidak aktif**. RLS aktif tidak berarti semua role boleh membaca tabel; owner/role dengan bypass memiliki perilaku tersendiri. Snapshot ini tidak mengekspor daftar role membership maupun seluruh privilege.

| Policy | Role | Command | USING | WITH CHECK |
| --- | --- | --- | --- | --- |
| `backend_only` | `service_role` | `ALL` | `true` | `true` |

## Sumber dan batas snapshot

Metadata: [schema-metadata-20261022.json](schema-metadata-20261022.json), diambil melalui SELECT catalog dalam transaksi READ ONLY; tidak menyalin isi tabel.

Source implementasi: [migrasi Seagis-Model](https://github.com/De-Voeux/Seagis-Model/tree/e93a005c95d746e6e33a6adad12760e94eb8a6cf/supabase/migrations), commit `e93a005c95d746e6e33a6adad12760e94eb8a6cf`. Penjelasan fungsi tabel diturunkan dari migrasi dan handover A0–A3; definisi kolom/constraint mengikuti catalog live. Snapshot tidak otomatis diperbarui bila database berubah.
