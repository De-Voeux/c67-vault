---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis_raw.raw_payload

Manifest sumber raw: hash, waktu penerimaan, lisensi, metadata dan pilihan penyimpanan. Payload bisa inline, object reference, atau metadata_only; tidak selalu menyimpan bytes asli.

- Jenis: tabel PostgreSQL. Schema: `seagis_raw`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Cara membaca

hash_basis yang berlaku mengikuti constraint live A2, bukan hanya definisi awal A0. metadata_only tidak membuktikan bytes sumber dapat direkonstruksi; periksa hash_basis dan provider_metadata.

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | Tidak | `gen_random_uuid()` | Identitas baris; lihat PK/default dan constraint khusus tabel. |
| `ingestion_run_id` | `uuid` | Tidak | — | Identitas proses ingestion asal. |
| `dataset_key` | `text` | Tidak | — | Identitas dataset dalam registri Seagis. |
| `is_synthetic` | `boolean` | Tidak | — | Penanda data/identitas sintetis; tidak disamakan dengan data lapangan. |
| `sha256` | `text` | Tidak | — | Digest SHA-256 sumber sesuai hash_basis. |
| `hash_basis` | `text` | Tidak | `'source_bytes'::text` | Dasar bytes/serialisasi yang dipakai menghitung hash. |
| `received_at` | `timestamp with time zone` | Tidak | — | Waktu penerimaan sumber raw. |
| `storage_mode` | `text` | Tidak | — | Cara retensi: inline, object atau metadata_only. |
| `payload` | `jsonb` | Ya | — | JSON payload inline bila diizinkan constraint. |
| `object_uri` | `text` | Ya | — | Referensi objek Storage bila memakai mode object. |
| `byte_size` | `bigint` | Tidak | — | Ukuran sumber yang dicatat, bytes. |
| `format` | `text` | Tidak | — | Format payload yang dicatat. |
| `licence_snapshot` | `text` | Tidak | — | Catatan lisensi pada waktu ingestion. |
| `provider_metadata` | `jsonb` | Tidak | `'{}'::jsonb` | Metadata provider dalam objek JSON. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `raw_payload_byte_size_check`

```sql
CHECK (byte_size >= 0)
```

- `raw_payload_check`

```sql
CHECK (storage_mode = 'inline'::text AND payload IS NOT NULL AND object_uri IS NULL OR storage_mode = 'object'::text AND payload IS NULL AND object_uri IS NOT NULL AND object_uri ~~ 'storage://%'::text OR storage_mode = 'metadata_only'::text AND payload IS NULL AND object_uri IS NULL)
```

- `raw_payload_hash_basis_v3`

```sql
CHECK (hash_basis = ANY (ARRAY['source_bytes'::text, 'synthetic_json_canonical_v1'::text, 'jsonb_utf8_v1'::text, 'toolbox_subset_json_v1'::text]))
```

- `raw_payload_id_ingestion_run_id_dataset_key_is_synthetic_key`

```sql
UNIQUE (id, ingestion_run_id, dataset_key, is_synthetic)
```

- `raw_payload_ingestion_run_id_sha256_key`

```sql
UNIQUE (ingestion_run_id, sha256)
```

- `raw_payload_inline_synthetic_v2`

```sql
CHECK (storage_mode <> 'inline'::text OR is_synthetic AND (hash_basis = ANY (ARRAY['synthetic_json_canonical_v1'::text, 'jsonb_utf8_v1'::text])))
```

- `raw_payload_pkey`

```sql
PRIMARY KEY (id)
```

- `raw_payload_provider_metadata_check`

```sql
CHECK (jsonb_typeof(provider_metadata) = 'object'::text)
```

- `raw_payload_sha256_check`

```sql
CHECK (sha256 ~ '^[0-9a-f]{64}$'::text)
```

- `raw_payload_storage_mode_check`

```sql
CHECK (storage_mode = ANY (ARRAY['inline'::text, 'object'::text, 'metadata_only'::text]))
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis_raw.raw_payload]] (ingestion_run_id, dataset_key, is_synthetic) | [[Supabase - seagis.ingestion_run]] (id, dataset_key, is_synthetic) | Wajib; 0..N anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.ingestion_run(id, dataset_key, is_synthetic);
```

## Relasi masuk

- [[Supabase - seagis.forecast_run]]: `(raw_payload_id, ingestion_run_id, dataset_key, is_synthetic)` → `(id, ingestion_run_id, dataset_key, is_synthetic)`.
- [[Supabase - seagis.observation]]: `(raw_payload_id, ingestion_run_id, dataset_key, is_synthetic)` → `(id, ingestion_run_id, dataset_key, is_synthetic)`.

## Indeks

```sql
CREATE UNIQUE INDEX raw_payload_id_ingestion_run_id_dataset_key_is_synthetic_key ON seagis_raw.raw_payload USING btree (id, ingestion_run_id, dataset_key, is_synthetic);
CREATE UNIQUE INDEX raw_payload_ingestion_run_id_sha256_key ON seagis_raw.raw_payload USING btree (ingestion_run_id, sha256);
CREATE UNIQUE INDEX raw_payload_pkey ON seagis_raw.raw_payload USING btree (id);
```

## Trigger dan batas mutasi

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis_raw.raw_payload FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
CREATE TRIGGER guard_raw BEFORE INSERT ON seagis_raw.raw_payload FOR EACH ROW EXECUTE FUNCTION seagis.guard_raw();
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
