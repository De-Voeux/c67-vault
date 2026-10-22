---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis.source_grid

Identitas sel/titik grid milik dataset regional, lengkap dengan koordinat, kedalaman, versi dan dasar identitas grid.

- Jenis: tabel PostgreSQL. Schema: `seagis`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | Tidak | `gen_random_uuid()` | Identitas baris; lihat PK/default dan constraint khusus tabel. |
| `dataset_key` | `text` | Tidak | — | Identitas dataset dalam registri Seagis. |
| `scope` | `text` | Tidak | `'regional_model'::text` | Lingkup data: sensor lokal atau model regional sesuai CHECK. |
| `grid_key` | `text` | Tidak | — | Identitas grid per dataset. |
| `grid_version` | `text` | Tidak | — | Versi identitas/grid. |
| `identity_basis` | `text` | Tidak | — | Dasar identitas sel/koordinat provider atau sintetis. |
| `latitude` | `seagis.finite_float` | Tidak | — | Lintang lokasi, derajat. |
| `longitude` | `seagis.finite_float` | Tidak | — | Bujur lokasi, derajat. |
| `depth_m` | `seagis.finite_float` | Tidak | — | Kedalaman dalam meter. |
| `is_synthetic` | `boolean` | Tidak | — | Penanda data/identitas sintetis; tidak disamakan dengan data lapangan. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `source_grid_check`

```sql
CHECK (identity_basis <> 'synthetic'::text OR is_synthetic)
```

- `source_grid_dataset_key_grid_key_is_synthetic_key`

```sql
UNIQUE (dataset_key, grid_key, is_synthetic)
```

- `source_grid_depth_m_check`

```sql
CHECK (depth_m::double precision >= 0::double precision)
```

- `source_grid_id_dataset_key_is_synthetic_key`

```sql
UNIQUE (id, dataset_key, is_synthetic)
```

- `source_grid_identity_basis_check`

```sql
CHECK (identity_basis = ANY (ARRAY['provider_cell'::text, 'provider_returned_coordinate'::text, 'synthetic'::text]))
```

- `source_grid_latitude_check`

```sql
CHECK (latitude::double precision >= '-90'::integer::double precision AND latitude::double precision <= 90::double precision)
```

- `source_grid_longitude_check`

```sql
CHECK (longitude::double precision >= '-180'::integer::double precision AND longitude::double precision <= 180::double precision)
```

- `source_grid_pkey`

```sql
PRIMARY KEY (id)
```

- `source_grid_scope_check`

```sql
CHECK (scope = 'regional_model'::text)
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis.source_grid]] (dataset_key, scope) | [[Supabase - seagis.dataset]] (dataset_key, scope) | Wajib; 0..N anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset(dataset_key, scope);
```

## Relasi masuk

- [[Supabase - seagis.forecast_value]]: `(source_grid_id, dataset_key, is_synthetic)` → `(id, dataset_key, is_synthetic)`.
- [[Supabase - seagis.plot_grid_mapping]]: `(source_grid_id)` → `(id)`.
- [[Supabase - seagis_environment.demo_grid_mapping]]: `(source_grid_id, dataset_key, grid_is_synthetic)` → `(id, dataset_key, is_synthetic)`.

## Indeks

```sql
CREATE UNIQUE INDEX source_grid_dataset_key_grid_key_is_synthetic_key ON seagis.source_grid USING btree (dataset_key, grid_key, is_synthetic);
CREATE UNIQUE INDEX source_grid_id_dataset_key_is_synthetic_key ON seagis.source_grid USING btree (id, dataset_key, is_synthetic);
CREATE UNIQUE INDEX source_grid_pkey ON seagis.source_grid USING btree (id);
```

## Trigger dan batas mutasi

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis.source_grid FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
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
