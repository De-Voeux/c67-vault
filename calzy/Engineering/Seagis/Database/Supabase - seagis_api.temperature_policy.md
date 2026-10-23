---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis_api.temperature_policy

Konfigurasi tunggal QC engineering suhu dan batas operasional API: rentang nilai, langkah perubahan, toleransi waktu, stale dan rate limit. Angka ini bukan ambang biologis tervalidasi.

- Jenis: tabel PostgreSQL. Schema: `seagis_api`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Cara membaca

Tabel singleton: id boolean PRIMARY KEY dan CHECK(id) mengizinkan paling banyak satu baris true. max_step_degc adalah batas QC dalam implementasi API, bukan bukti suhu berubah sekian derajat menyebabkan ice-ice.

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `id` | `boolean` | Tidak | `true` | Identitas baris; lihat PK/default dan constraint khusus tabel. |
| `version` | `text` | Tidak | — | Identitas versi kebijakan. |
| `min_degc` | `double precision` | Tidak | — | Batas bawah QC suhu dalam °C. |
| `max_degc` | `double precision` | Tidak | — | Batas atas QC suhu dalam °C. |
| `max_step_degc` | `double precision` | Tidak | — | Batas langkah perubahan untuk QC suhu, °C. |
| `future_tolerance_seconds` | `integer` | Tidak | — | Toleransi timestamp masa depan, detik. |
| `stale_after_seconds` | `integer` | Tidak | — | Batas stale API suhu, detik. |
| `requests_per_minute` | `integer` | Tidak | — | Batas request per menit pada API. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `temperature_policy_check`

```sql
CHECK (min_degc < max_degc AND max_step_degc > 0::double precision AND future_tolerance_seconds > 0 AND stale_after_seconds > 0 AND requests_per_minute > 0)
```

- `temperature_policy_id_check`

```sql
CHECK (id)
```

- `temperature_policy_pkey`

```sql
PRIMARY KEY (id)
```

## Relasi keluar

Tidak ada foreign key yang dideklarasikan.

## Relasi masuk

Tidak ada FK dari tabel lain menuju objek ini.

## Indeks

```sql
CREATE UNIQUE INDEX temperature_policy_pkey ON seagis_api.temperature_policy USING btree (id);
```

## Trigger dan batas mutasi

Tidak ada user trigger pada objek ini dalam snapshot catalog. Pembatasan akses dan rutin API tetap dapat membatasi penulisan.

## Akses

RLS: **aktif**. FORCE RLS: **tidak aktif**. RLS aktif tidak berarti semua role boleh membaca tabel; owner/role dengan bypass memiliki perilaku tersendiri. Snapshot ini tidak mengekspor daftar role membership maupun seluruh privilege.

Tidak ada policy RLS tercatat untuk tabel ini. Role biasa yang terkena RLS tidak mendapat izin row melalui policy; jalur runtime menggunakan routine privat sesuai dokumentasi A1/A2/A3.

## Sumber dan batas snapshot

Metadata: [schema-metadata-20261022.json](schema-metadata-20261022.json), diambil melalui SELECT catalog dalam transaksi READ ONLY; tidak menyalin isi tabel.

Source implementasi: [migrasi Seagis-Model](https://github.com/De-Voeux/Seagis-Model/tree/e93a005c95d746e6e33a6adad12760e94eb8a6cf/supabase/migrations), commit `e93a005c95d746e6e33a6adad12760e94eb8a6cf`. Penjelasan fungsi tabel diturunkan dari migrasi dan handover A0–A3; definisi kolom/constraint mengikuti catalog live. Snapshot tidak otomatis diperbarui bila database berubah.
