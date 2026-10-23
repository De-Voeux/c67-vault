---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis.dataset

Registri produk/dataset: identitas provider, versi, cadence, resolusi, lisensi, dan izin ingestion. Dataset lokal dan model regional dibedakan lewat scope.

- Jenis: tabel PostgreSQL. Schema: `seagis`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Kolom

| Kolom                    | Tipe PostgreSQL            | NULL diizinkan | Default / generated | Arti                                                         |
| ------------------------ | -------------------------- | -------------- | ------------------- | ------------------------------------------------------------ |
| `dataset_key`            | `text`                     | Tidak          | —                   | Identitas dataset dalam registri Seagis.                     |
| `source_key`             | `text`                     | Tidak          | —                   | Identitas penyedia sumber.                                   |
| `provider_product_id`    | `text`                     | Ya             | —                   | ID produk provider bila tersedia.                            |
| `provider_dataset_id`    | `text`                     | Tidak          | —                   | ID dataset pada provider.                                    |
| `dataset_version`        | `text`                     | Tidak          | —                   | Versi dataset yang diregistrasikan.                          |
| `scope`                  | `text`                     | Tidak          | —                   | Lingkup data: sensor lokal atau model regional sesuai CHECK. |
| `native_cadence_seconds` | `integer`                  | Tidak          | —                   | Cadence native data dalam detik; berbeda dari jadwal fetch.  |
| `resolution_lat_deg`     | `seagis.finite_float`      | Ya             | —                   | Resolusi lintang grid, derajat.                              |
| `resolution_lon_deg`     | `seagis.finite_float`      | Ya             | —                   | Resolusi bujur grid, derajat.                                |
| `source_timezone`        | `text`                     | Tidak          | `'UTC'::text`       | Zona waktu sumber yang dicatat pada registri.                |
| `licence_url`            | `text`                     | Tidak          | —                   | URL ketentuan lisensi.                                       |
| `attribution`            | `text`                     | Tidak          | —                   | Teks atribusi penyedia.                                      |
| `raw_storage_permitted`  | `boolean`                  | Tidak          | `false`             | Izin penyimpanan raw menurut registri.                       |
| `real_ingestion_enabled` | `boolean`                  | Tidak          | `false`             | Flag pengaktifan ingestion data nyata.                       |
| `metadata_checked_at`    | `timestamp with time zone` | Tidak          | —                   | Waktu pemeriksaan metadata dataset.                          |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `dataset_dataset_key_scope_key`

```sql
UNIQUE (dataset_key, scope)
```

- `dataset_native_cadence_seconds_check`

```sql
CHECK (native_cadence_seconds > 0)
```

- `dataset_pkey`

```sql
PRIMARY KEY (dataset_key)
```

- `dataset_resolution_lat_deg_check`

```sql
CHECK (resolution_lat_deg::double precision > 0::double precision)
```

- `dataset_resolution_lon_deg_check`

```sql
CHECK (resolution_lon_deg::double precision > 0::double precision)
```

- `dataset_scope_check`

```sql
CHECK (scope = ANY (ARRAY['local_sensor'::text, 'regional_model'::text]))
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis.dataset]] (source_key) | [[Supabase - seagis.source]] (source_key) | Wajib; 0..N anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (source_key) REFERENCES seagis.source(source_key);
```

## Relasi masuk

- [[Supabase - seagis.dataset_parameter]]: `(dataset_key)` → `(dataset_key)`.
- [[Supabase - seagis.forecast_run]]: `(dataset_key, scope)` → `(dataset_key, scope)`.
- [[Supabase - seagis.ingestion_run]]: `(dataset_key)` → `(dataset_key)`.
- [[Supabase - seagis.sensor]]: `(dataset_key, scope)` → `(dataset_key, scope)`.
- [[Supabase - seagis.source_grid]]: `(dataset_key, scope)` → `(dataset_key, scope)`.
- [[Supabase - seagis_environment.policy]]: `(dataset_key)` → `(dataset_key)`.

## Indeks

```sql
CREATE UNIQUE INDEX dataset_dataset_key_scope_key ON seagis.dataset USING btree (dataset_key, scope);
CREATE UNIQUE INDEX dataset_pkey ON seagis.dataset USING btree (dataset_key);
```

## Trigger dan batas mutasi

```sql
CREATE TRIGGER guard_dataset_identity BEFORE UPDATE ON seagis.dataset FOR EACH ROW EXECUTE FUNCTION seagis.guard_dataset_identity();
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
