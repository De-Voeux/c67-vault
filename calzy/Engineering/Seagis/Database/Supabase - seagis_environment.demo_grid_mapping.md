---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis_environment.demo_grid_mapping

Jembatan preview khusus plot A/B sintetis ke grid regional nyata dengan koordinat contoh belum disurvei. Terpisah dari mapping operasional agar konteks demo tidak berubah menjadi data lapangan.

- Jenis: tabel PostgreSQL. Schema: `seagis_environment`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Cara membaca

Constraint mengikat plot sintetis dan grid non-sintetis serta membatasi plot ke dua ID demo. Ini bukan hasil survei lapangan atau bukti representativitas grid untuk lokasi budidaya.

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `plot_id` | `uuid` | Tidak | — | Identitas plot budidaya terkait. |
| `plot_is_synthetic` | `boolean` | Tidak | `true` | Flag plot sintetis yang diperiksa FK gabungan. |
| `source_grid_id` | `uuid` | Tidak | — | Identitas sel/titik grid sumber. |
| `dataset_key` | `text` | Tidak | — | Identitas dataset dalam registri Seagis. |
| `grid_is_synthetic` | `boolean` | Tidak | `false` | Flag grid sintetis; demo mapping mewajibkan false. |
| `example_latitude` | `seagis.finite_float` | Tidak | — | Lintang contoh demo, bukan koordinat survei. |
| `example_longitude` | `seagis.finite_float` | Tidak | — | Bujur contoh demo, bukan koordinat survei. |
| `coordinate_status` | `text` | Tidak | — | Status koordinat contoh belum disurvei. |
| `distance_m` | `seagis.finite_float` | Tidak | — | Jarak mapping dalam meter. |
| `sampling_method` | `text` | Tidak | — | Metode memilih/mengaitkan grid. |
| `created_at` | `timestamp with time zone` | Tidak | `now()` | Waktu pembuatan/pencatatan baris. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `demo_grid_mapping_coordinate_status_check`

```sql
CHECK (coordinate_status = 'example_not_surveyed'::text)
```

- `demo_grid_mapping_distance_m_check`

```sql
CHECK (distance_m::double precision >= 0::double precision AND distance_m::double precision <= 30000::double precision)
```

- `demo_grid_mapping_example_latitude_check`

```sql
CHECK (example_latitude::double precision >= '-90'::integer::double precision AND example_latitude::double precision <= 90::double precision)
```

- `demo_grid_mapping_example_longitude_check`

```sql
CHECK (example_longitude::double precision >= '-180'::integer::double precision AND example_longitude::double precision <= 180::double precision)
```

- `demo_grid_mapping_grid_is_synthetic_check`

```sql
CHECK (NOT grid_is_synthetic)
```

- `demo_grid_mapping_pkey`

```sql
PRIMARY KEY (plot_id, source_grid_id)
```

- `demo_grid_mapping_plot_id_check`

```sql
CHECK (plot_id = ANY (ARRAY['00000000-0000-4000-8000-000000000001'::uuid, '00000000-0000-4000-8000-000000000002'::uuid]))
```

- `demo_grid_mapping_plot_is_synthetic_check`

```sql
CHECK (plot_is_synthetic)
```

- `demo_grid_mapping_sampling_method_check`

```sql
CHECK (sampling_method = ANY (ARRAY['nearest_cell'::text, 'provider_returned_coordinate'::text]))
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis_environment.demo_grid_mapping]] (dataset_key) | [[Supabase - seagis_environment.policy]] (dataset_key) | Wajib; 0..N anak per induk |
| [[Supabase - seagis_environment.demo_grid_mapping]] (plot_id, plot_is_synthetic) | [[Supabase - seagis.plot]] (id, is_synthetic) | Wajib; 0..N anak per induk |
| [[Supabase - seagis_environment.demo_grid_mapping]] (source_grid_id, dataset_key, grid_is_synthetic) | [[Supabase - seagis.source_grid]] (id, dataset_key, is_synthetic) | Wajib; 0..N anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (dataset_key) REFERENCES seagis_environment.policy(dataset_key);
FOREIGN KEY (plot_id, plot_is_synthetic) REFERENCES seagis.plot(id, is_synthetic);
FOREIGN KEY (source_grid_id, dataset_key, grid_is_synthetic) REFERENCES seagis.source_grid(id, dataset_key, is_synthetic);
```

## Relasi masuk

Tidak ada FK dari tabel lain menuju objek ini.

## Indeks

```sql
CREATE UNIQUE INDEX demo_grid_mapping_pkey ON seagis_environment.demo_grid_mapping USING btree (plot_id, source_grid_id);
```

## Trigger dan batas mutasi

```sql
CREATE TRIGGER immutable_demo_mapping BEFORE DELETE OR UPDATE ON seagis_environment.demo_grid_mapping FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
```

Definisi di atas menunjukkan routine guard yang dipanggil. Isi routine selengkapnya berada pada migrasi source; CHECK/FK saja tidak menggambarkan semua guard lintas tabel.

## Akses

RLS: **aktif**. FORCE RLS: **tidak aktif**. RLS aktif tidak berarti semua role boleh membaca tabel; owner/role dengan bypass memiliki perilaku tersendiri. Snapshot ini tidak mengekspor daftar role membership maupun seluruh privilege.

Tidak ada policy RLS tercatat untuk tabel ini. Role biasa yang terkena RLS tidak mendapat izin row melalui policy; jalur runtime menggunakan routine privat sesuai dokumentasi A1/A2/A3.

## Sumber dan batas snapshot

Metadata: [schema-metadata-20261022.json](schema-metadata-20261022.json), diambil melalui SELECT catalog dalam transaksi READ ONLY; tidak menyalin isi tabel.

Source implementasi: [migrasi Seagis-Model](https://github.com/De-Voeux/Seagis-Model/tree/e93a005c95d746e6e33a6adad12760e94eb8a6cf/supabase/migrations), commit `e93a005c95d746e6e33a6adad12760e94eb8a6cf`. Penjelasan fungsi tabel diturunkan dari migrasi dan handover A0–A3; definisi kolom/constraint mengikuti catalog live. Snapshot tidak otomatis diperbarui bila database berubah.
