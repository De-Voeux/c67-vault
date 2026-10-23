---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis.plot_grid_mapping

Pemetaan operasional plot ke grid regional, dengan masa berlaku dan waktu pencatatan. Kelayakan kecocokan nyata/sintetis diperiksa lebih lanjut oleh guard aplikasi.

- Jenis: tabel PostgreSQL. Schema: `seagis`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Cara membaca

recorded_at ditambahkan pada migrasi 0005. Waktu efektif suatu mapping berbeda dari waktu sistem mengetahui mapping tersebut; keduanya penting agar alignment historis tidak memakai pengetahuan masa depan.

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | Tidak | `gen_random_uuid()` | Identitas baris; lihat PK/default dan constraint khusus tabel. |
| `plot_id` | `uuid` | Tidak | — | Identitas plot budidaya terkait. |
| `source_grid_id` | `uuid` | Tidak | — | Identitas sel/titik grid sumber. |
| `is_synthetic` | `boolean` | Tidak | — | Penanda data/identitas sintetis; tidak disamakan dengan data lapangan. |
| `sampling_method` | `text` | Tidak | — | Metode memilih/mengaitkan grid. |
| `distance_m` | `seagis.finite_float` | Ya | — | Jarak mapping dalam meter. |
| `representativeness` | `text` | Tidak | — | Penilaian representativitas mapping. |
| `effective_from` | `timestamp with time zone` | Tidak | — | Awal masa berlaku mapping. |
| `effective_until` | `timestamp with time zone` | Ya | — | Akhir masa berlaku; NULL jika terbuka. |
| `recorded_at` | `timestamp with time zone` | Tidak | `clock_timestamp()` | Waktu mapping diketahui/dicatat oleh sistem. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `plot_grid_mapping_check`

```sql
CHECK (effective_until IS NULL OR effective_until > effective_from)
```

- `plot_grid_mapping_distance_m_check`

```sql
CHECK (distance_m::double precision >= 0::double precision)
```

- `plot_grid_mapping_pkey`

```sql
PRIMARY KEY (id)
```

- `plot_grid_mapping_plot_id_source_grid_id_effective_from_key`

```sql
UNIQUE (plot_id, source_grid_id, effective_from)
```

- `plot_grid_mapping_representativeness_check`

```sql
CHECK (representativeness = ANY (ARRAY['unverified'::text, 'regional_only'::text, 'land_mask_issue'::text]))
```

- `plot_grid_mapping_sampling_method_check`

```sql
CHECK (sampling_method = ANY (ARRAY['nearest_wet_cell'::text, 'nearest_cell'::text, 'provider_returned_coordinate'::text, 'synthetic'::text]))
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis.plot_grid_mapping]] (plot_id, is_synthetic) | [[Supabase - seagis.plot]] (id, is_synthetic) | Wajib; 0..N anak per induk |
| [[Supabase - seagis.plot_grid_mapping]] (source_grid_id) | [[Supabase - seagis.source_grid]] (id) | Wajib; 0..N anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot(id, is_synthetic);
FOREIGN KEY (source_grid_id) REFERENCES seagis.source_grid(id);
```

## Relasi masuk

Tidak ada FK dari tabel lain menuju objek ini.

## Indeks

```sql
CREATE INDEX mapping_grid_plot ON seagis.plot_grid_mapping USING btree (source_grid_id, plot_id);
CREATE UNIQUE INDEX plot_grid_mapping_pkey ON seagis.plot_grid_mapping USING btree (id);
CREATE UNIQUE INDEX plot_grid_mapping_plot_id_source_grid_id_effective_from_key ON seagis.plot_grid_mapping USING btree (plot_id, source_grid_id, effective_from);
```

## Trigger dan batas mutasi

```sql
CREATE TRIGGER guard_mapping BEFORE INSERT OR UPDATE ON seagis.plot_grid_mapping FOR EACH ROW EXECUTE FUNCTION seagis.guard_mapping();
CREATE TRIGGER immutable_alignment_mapping BEFORE DELETE OR UPDATE ON seagis.plot_grid_mapping FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
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
