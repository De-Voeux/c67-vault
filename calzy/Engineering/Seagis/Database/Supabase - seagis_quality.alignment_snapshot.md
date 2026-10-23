---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis_quality.alignment_snapshot

Hasil QC dan alignment A3 per plot, mode dan rentang waktu. Body JSON menyimpan hasil review/coverage; berbeda dari feature_snapshot dan belum merupakan diagnosis atau prediksi penyakit.

- Jenis: tabel PostgreSQL. Schema: `seagis_quality`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Cara membaca

Mode demo_review dapat memakai konteks demo dengan provenance eksplisit. Hasil quality/alignment engineering tidak memberikan probabilitas penyakit atau izin training secara otomatis. Periksa isi body dan kebijakan sebelum memakai hasil.

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | Tidak | `gen_random_uuid()` | Identitas baris; lihat PK/default dan constraint khusus tabel. |
| `plot_id` | `uuid` | Tidak | — | Identitas plot budidaya terkait. |
| `mode` | `text` | Tidak | — | Mode demo_review atau operational_review. |
| `start_at` | `timestamp with time zone` | Tidak | — | Awal jendela alignment. |
| `end_at` | `timestamp with time zone` | Tidak | — | Akhir jendela alignment; lebih besar dari start_at dan maksimal tujuh hari. |
| `policy_version` | `text` | Tidak | — | Versi kebijakan QC/alignment yang digunakan. |
| `source_sha256` | `text` | Tidak | — | Hash bundle sumber untuk reproducibility/idempotensi. |
| `input_manifest_sha256` | `text` | Tidak | — | Hash manifest lineage input. |
| `body` | `jsonb` | Tidak | — | Objek JSON hasil QC dan alignment. |
| `body_sha256` | `text` | Ya | `GENERATED ALWAYS AS (seagis.jsonb_sha256(body)) STORED` | Hash body yang dihitung database secara otomatis. |
| `created_at` | `timestamp with time zone` | Tidak | `clock_timestamp()` | Waktu pembuatan/pencatatan baris. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `alignment_snapshot_body_check`

```sql
CHECK (jsonb_typeof(body) = 'object'::text)
```

- `alignment_snapshot_check`

```sql
CHECK (end_at > start_at AND (end_at - start_at) <= '7 days'::interval)
```

- `alignment_snapshot_input_manifest_sha256_check`

```sql
CHECK (input_manifest_sha256 ~ '^[0-9a-f]{64}$'::text)
```

- `alignment_snapshot_mode_check`

```sql
CHECK (mode = ANY (ARRAY['demo_review'::text, 'operational_review'::text]))
```

- `alignment_snapshot_pkey`

```sql
PRIMARY KEY (id)
```

- `alignment_snapshot_plot_id_mode_start_at_end_at_policy_vers_key`

```sql
UNIQUE (plot_id, mode, start_at, end_at, policy_version, source_sha256)
```

- `alignment_snapshot_source_sha256_check`

```sql
CHECK (source_sha256 ~ '^[0-9a-f]{64}$'::text)
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis_quality.alignment_snapshot]] (plot_id) | [[Supabase - seagis.plot]] (id) | Wajib; 0..N anak per induk |
| [[Supabase - seagis_quality.alignment_snapshot]] (policy_version) | [[Supabase - seagis_quality.policy]] (version) | Wajib; 0..N anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (plot_id) REFERENCES seagis.plot(id);
FOREIGN KEY (policy_version) REFERENCES seagis_quality.policy(version);
```

## Relasi masuk

- [[Supabase - seagis_quality.snapshot_input]]: `(snapshot_id)` → `(id)`.

## Indeks

```sql
CREATE UNIQUE INDEX alignment_snapshot_pkey ON seagis_quality.alignment_snapshot USING btree (id);
CREATE UNIQUE INDEX alignment_snapshot_plot_id_mode_start_at_end_at_policy_vers_key ON seagis_quality.alignment_snapshot USING btree (plot_id, mode, start_at, end_at, policy_version, source_sha256);
```

## Trigger dan batas mutasi

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis_quality.alignment_snapshot FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
```

Definisi di atas menunjukkan routine guard yang dipanggil. Isi routine selengkapnya berada pada migrasi source; CHECK/FK saja tidak menggambarkan semua guard lintas tabel.

## Akses

RLS: **aktif**. FORCE RLS: **tidak aktif**. RLS aktif tidak berarti semua role boleh membaca tabel; owner/role dengan bypass memiliki perilaku tersendiri. Snapshot ini tidak mengekspor daftar role membership maupun seluruh privilege.

Tidak ada policy RLS tercatat untuk tabel ini. Role biasa yang terkena RLS tidak mendapat izin row melalui policy; jalur runtime menggunakan routine privat sesuai dokumentasi A1/A2/A3.

## Sumber dan batas snapshot

Metadata: [schema-metadata-20261022.json](schema-metadata-20261022.json), diambil melalui SELECT catalog dalam transaksi READ ONLY; tidak menyalin isi tabel.

Source implementasi: [migrasi Seagis-Model](https://github.com/De-Voeux/Seagis-Model/tree/e93a005c95d746e6e33a6adad12760e94eb8a6cf/supabase/migrations), commit `e93a005c95d746e6e33a6adad12760e94eb8a6cf`. Penjelasan fungsi tabel diturunkan dari migrasi dan handover A0–A3; definisi kolom/constraint mengikuti catalog live. Snapshot tidak otomatis diperbarui bila database berubah.
