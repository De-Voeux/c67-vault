---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis_features.feature_snapshot

Kontrak penyimpanan fitur per plot dan cutoff as_of, dengan versi, status draft/sealed dan hash lineage. Keberadaan tabel tidak berarti pipeline fitur/model A4 sudah dijalankan.

- Jenis: tabel PostgreSQL. Schema: `seagis_features`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Cara membaca

Fitur statistik/model lanjutan tidak dibuktikan hanya dengan keberadaan schema ini. A3 menyimpan hasilnya di seagis_quality; jangan menganggap body QC A3 sebagai features A4.

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | Tidak | `gen_random_uuid()` | Identitas baris; lihat PK/default dan constraint khusus tabel. |
| `plot_id` | `uuid` | Tidak | — | Identitas plot budidaya terkait. |
| `is_synthetic` | `boolean` | Tidak | — | Penanda data/identitas sintetis; tidak disamakan dengan data lapangan. |
| `as_of` | `timestamp with time zone` | Tidak | — | Cutoff ketersediaan data untuk fitur. |
| `generated_at` | `timestamp with time zone` | Tidak | — | Waktu snapshot fitur dibuat. |
| `feature_version` | `text` | Tidak | — | Versi definisi/perhitungan fitur. |
| `feature_schema_version` | `text` | Tidak | — | Versi struktur payload fitur. |
| `features` | `jsonb` | Tidak | — | Objek JSON fitur. |
| `missing_context` | `text[]` | Tidak | `'{}'::text[]` | Daftar konteks yang belum tersedia. |
| `status` | `text` | Tidak | `'draft'::text` | Status siklus hidup; lihat pilihan pada CHECK. |
| `input_manifest_sha256` | `text` | Ya | — | Hash manifest lineage input. |
| `features_sha256` | `text` | Ya | `GENERATED ALWAYS AS (seagis.jsonb_sha256(features)) STORED` | Hash features yang dihitung database secara otomatis. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `feature_snapshot_check`

```sql
CHECK (generated_at >= as_of)
```

- `feature_snapshot_check1`

```sql
CHECK ((status = 'draft'::text) = (input_manifest_sha256 IS NULL))
```

- `feature_snapshot_features_check`

```sql
CHECK (jsonb_typeof(features) = 'object'::text)
```

- `feature_snapshot_input_manifest_sha256_check`

```sql
CHECK (input_manifest_sha256 ~ '^[0-9a-f]{64}$'::text)
```

- `feature_snapshot_pkey`

```sql
PRIMARY KEY (id)
```

- `feature_snapshot_plot_id_as_of_feature_version_input_manife_key`

```sql
UNIQUE (plot_id, as_of, feature_version, input_manifest_sha256)
```

- `feature_snapshot_status_check`

```sql
CHECK (status = ANY (ARRAY['draft'::text, 'sealed'::text]))
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis_features.feature_snapshot]] (plot_id, is_synthetic) | [[Supabase - seagis.plot]] (id, is_synthetic) | Wajib; 0..N anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot(id, is_synthetic);
```

## Relasi masuk

- [[Supabase - seagis_features.feature_input]]: `(snapshot_id)` → `(id)`.

## Indeks

```sql
CREATE UNIQUE INDEX feature_snapshot_pkey ON seagis_features.feature_snapshot USING btree (id);
CREATE UNIQUE INDEX feature_snapshot_plot_id_as_of_feature_version_input_manife_key ON seagis_features.feature_snapshot USING btree (plot_id, as_of, feature_version, input_manifest_sha256);
```

## Trigger dan batas mutasi

```sql
CREATE TRIGGER guard_snapshot BEFORE INSERT OR UPDATE ON seagis_features.feature_snapshot FOR EACH ROW EXECUTE FUNCTION seagis_features.guard_snapshot();
CREATE TRIGGER no_snapshot_delete BEFORE DELETE ON seagis_features.feature_snapshot FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
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
