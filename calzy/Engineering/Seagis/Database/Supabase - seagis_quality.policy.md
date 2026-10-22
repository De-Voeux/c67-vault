---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis_quality.policy

Registri versi kebijakan QC/alignment A3, definisi JSON dan hash kebijakan/kode. Memungkinkan hasil ditelusuri ke versi pemeriksaannya.

- Jenis: tabel PostgreSQL. Schema: `seagis_quality`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `version` | `text` | Tidak | — | Identitas versi kebijakan. |
| `definition` | `jsonb` | Tidak | — | Objek JSON definisi kebijakan QC/alignment. |
| `policy_sha256` | `text` | Tidak | — | Hash definisi kebijakan. |
| `code_sha256` | `text` | Tidak | — | Hash kode pemrosesan yang didaftarkan. |
| `registered_at` | `timestamp with time zone` | Tidak | `clock_timestamp()` | Waktu versi kebijakan diregistrasikan. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `policy_code_sha256_check`

```sql
CHECK (code_sha256 ~ '^[0-9a-f]{64}$'::text)
```

- `policy_definition_check`

```sql
CHECK (jsonb_typeof(definition) = 'object'::text)
```

- `policy_pkey`

```sql
PRIMARY KEY (version)
```

- `policy_policy_sha256_check`

```sql
CHECK (policy_sha256 ~ '^[0-9a-f]{64}$'::text)
```

## Relasi keluar

Tidak ada foreign key yang dideklarasikan.

## Relasi masuk

- [[Supabase - seagis_quality.alignment_snapshot]]: `(policy_version)` → `(version)`.

## Indeks

```sql
CREATE UNIQUE INDEX policy_pkey ON seagis_quality.policy USING btree (version);
```

## Trigger dan batas mutasi

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis_quality.policy FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
```

Definisi di atas menunjukkan routine guard yang dipanggil. Isi routine selengkapnya berada pada migrasi source; CHECK/FK saja tidak menggambarkan semua guard lintas tabel.

## Akses

RLS: **aktif**. FORCE RLS: **tidak aktif**. RLS aktif tidak berarti semua role boleh membaca tabel; owner/role dengan bypass memiliki perilaku tersendiri. Snapshot ini tidak mengekspor daftar role membership maupun seluruh privilege.

Tidak ada policy RLS tercatat untuk tabel ini. Role biasa yang terkena RLS tidak mendapat izin row melalui policy; jalur runtime menggunakan routine privat sesuai dokumentasi A1/A2/A3.

## Sumber dan batas snapshot

Metadata: [schema-metadata-20261022.json](schema-metadata-20261022.json), diambil melalui SELECT catalog dalam transaksi READ ONLY; tidak menyalin isi tabel.

Source implementasi: [migrasi Seagis-Model](https://github.com/De-Voeux/Seagis-Model/tree/e93a005c95d746e6e33a6adad12760e94eb8a6cf/supabase/migrations), commit `e93a005c95d746e6e33a6adad12760e94eb8a6cf`. Penjelasan fungsi tabel diturunkan dari migrasi dan handover A0–A3; definisi kolom/constraint mengikuti catalog live. Snapshot tidak otomatis diperbarui bila database berubah.
