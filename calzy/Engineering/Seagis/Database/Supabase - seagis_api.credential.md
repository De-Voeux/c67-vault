---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis_api.credential

Identitas akses device/reader: hash token, masa berlaku, pencabutan dan ikatan sensor untuk device. Tidak menyimpan token plaintext. Isi tabel tidak disalin ke dokumentasi.

- Jenis: tabel PostgreSQL. Schema: `seagis_api`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | Tidak | `gen_random_uuid()` | Identitas baris; lihat PK/default dan constraint khusus tabel. |
| `label` | `text` | Tidak | — | Label operasional credential. |
| `token_sha256` | `text` | Tidak | — | Hash token autentikasi; bukan token plaintext. |
| `kind` | `text` | Tidak | — | Jenis credential: device atau reader. |
| `sensor_id` | `uuid` | Ya | — | Identitas sensor terkait. |
| `created_at` | `timestamp with time zone` | Tidak | `now()` | Waktu pembuatan/pencatatan baris. |
| `expires_at` | `timestamp with time zone` | Tidak | — | Waktu credential kedaluwarsa. |
| `revoked_at` | `timestamp with time zone` | Ya | — | Waktu pencabutan; NULL bila belum dicabut. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `credential_check`

```sql
CHECK ((kind = 'device'::text) = (sensor_id IS NOT NULL))
```

- `credential_check1`

```sql
CHECK (expires_at > created_at)
```

- `credential_kind_check`

```sql
CHECK (kind = ANY (ARRAY['device'::text, 'reader'::text]))
```

- `credential_pkey`

```sql
PRIMARY KEY (id)
```

- `credential_token_sha256_check`

```sql
CHECK (token_sha256 ~ '^[0-9a-f]{64}$'::text)
```

- `credential_token_sha256_key`

```sql
UNIQUE (token_sha256)
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis_api.credential]] (sensor_id) | [[Supabase - seagis.sensor]] (id) | Opsional / MATCH SIMPLE; 0..N anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (sensor_id) REFERENCES seagis.sensor(id);
```

## Relasi masuk

- [[Supabase - seagis_api.reader_plot]]: `(credential_id)` → `(id)`.
- [[Supabase - seagis_api.request_event]]: `(credential_id)` → `(id)`.

## Indeks

```sql
CREATE UNIQUE INDEX credential_pkey ON seagis_api.credential USING btree (id);
CREATE UNIQUE INDEX credential_token_sha256_key ON seagis_api.credential USING btree (token_sha256);
```

## Trigger dan batas mutasi

Tidak ada user trigger pada objek ini dalam snapshot catalog. Pembatasan akses dan rutin API tetap dapat membatasi penulisan.

## Akses

RLS: **aktif**. FORCE RLS: **tidak aktif**. RLS aktif tidak berarti semua role boleh membaca tabel; owner/role dengan bypass memiliki perilaku tersendiri. Snapshot ini tidak mengekspor daftar role membership maupun seluruh privilege.

Tidak ada policy RLS tercatat untuk tabel ini. Role biasa yang terkena RLS tidak mendapat izin row melalui policy; jalur runtime menggunakan routine privat sesuai dokumentasi A1/A2/A3.

## Sumber dan batas snapshot

Metadata: [schema-metadata-20261022.json](schema-metadata-20261022.json), diambil melalui SELECT catalog dalam transaksi READ ONLY; tidak menyalin isi tabel.

Source implementasi: [migrasi Seagis-Model](https://github.com/De-Voeux/Seagis-Model/tree/e93a005c95d746e6e33a6adad12760e94eb8a6cf/supabase/migrations), commit `e93a005c95d746e6e33a6adad12760e94eb8a6cf`. Penjelasan fungsi tabel diturunkan dari migrasi dan handover A0–A3; definisi kolom/constraint mengikuti catalog live. Snapshot tidak otomatis diperbarui bila database berubah.
