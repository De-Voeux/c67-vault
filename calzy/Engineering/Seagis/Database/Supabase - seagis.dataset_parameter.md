---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis.dataset_parameter

Penghubung dataset dan parameter; menyimpan nama variabel provider serta aturan konversi nilai/satuan ke kontrak Seagis.

- Jenis: tabel PostgreSQL. Schema: `seagis`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `dataset_key` | `text` | Tidak | — | Identitas dataset dalam registri Seagis. |
| `parameter_code` | `text` | Tidak | — | Kode parameter lingkungan. |
| `source_variable` | `text` | Tidak | — | Nama variabel sumber/provider. |
| `native_unit` | `text` | Tidak | — | Satuan asli sumber. |
| `unit` | `text` | Tidak | — | Satuan nilai normalisasi. |
| `conversion_code` | `text` | Tidak | — | Identitas aturan konversi. |
| `conversion_factor` | `seagis.finite_float` | Tidak | `1` | Faktor konversi linear. |
| `conversion_offset` | `seagis.finite_float` | Tidak | `0` | Offset konversi linear. |
| `temporal_support` | `text` | Tidak | — | Makna temporal: instantaneous, mean atau sum. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `dataset_parameter_conversion_factor_check`

```sql
CHECK (conversion_factor::double precision <> 0::double precision)
```

- `dataset_parameter_dataset_key_parameter_code_native_unit_un_key`

```sql
UNIQUE (dataset_key, parameter_code, native_unit, unit, conversion_code)
```

- `dataset_parameter_pkey`

```sql
PRIMARY KEY (dataset_key, parameter_code)
```

- `dataset_parameter_temporal_support_check`

```sql
CHECK (temporal_support = ANY (ARRAY['instantaneous'::text, 'mean'::text, 'sum'::text]))
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis.dataset_parameter]] (dataset_key) | [[Supabase - seagis.dataset]] (dataset_key) | Wajib; 0..N anak per induk |
| [[Supabase - seagis.dataset_parameter]] (parameter_code, unit) | [[Supabase - seagis.parameter]] (parameter_code, unit) | Wajib; 0..N anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (dataset_key) REFERENCES seagis.dataset(dataset_key);
FOREIGN KEY (parameter_code, unit) REFERENCES seagis.parameter(parameter_code, unit);
```

## Relasi masuk

- [[Supabase - seagis.forecast_value]]: `(dataset_key, parameter_code, native_unit, unit, conversion_code)` → `(dataset_key, parameter_code, native_unit, unit, conversion_code)`.
- [[Supabase - seagis.observation]]: `(dataset_key, parameter_code, native_unit, unit, conversion_code)` → `(dataset_key, parameter_code, native_unit, unit, conversion_code)`.
- [[Supabase - seagis.sensor]]: `(dataset_key, parameter_code)` → `(dataset_key, parameter_code)`.

## Indeks

```sql
CREATE UNIQUE INDEX dataset_parameter_dataset_key_parameter_code_native_unit_un_key ON seagis.dataset_parameter USING btree (dataset_key, parameter_code, native_unit, unit, conversion_code);
CREATE UNIQUE INDEX dataset_parameter_pkey ON seagis.dataset_parameter USING btree (dataset_key, parameter_code);
```

## Trigger dan batas mutasi

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis.dataset_parameter FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
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
