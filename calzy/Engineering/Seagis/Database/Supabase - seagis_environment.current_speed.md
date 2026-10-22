---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis_environment.current_speed

View turunan besar kecepatan arus sqrt(uo² + vo²), memasangkan komponen timur dan utara pada run, grid dan valid_at yang sama. Tidak menyimpan salinan baris hasil.

- Jenis: view turunan. Schema: `seagis_environment`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Cara membaca

Rumus hanya menghasilkan nilai saat kedua komponen berstatus present. available_at memakai waktu ingestion paling akhir dari dua komponen; kolom ingested_at pada view berasal dari komponen timur. Relasi view adalah JOIN SQL, bukan foreign key yang dideklarasikan pada view.

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `eastward_value_id` | `uuid` | Tidak dijamin NOT NULL oleh catalog view | — | ID forecast_value komponen arus timur. |
| `northward_value_id` | `uuid` | Tidak dijamin NOT NULL oleh catalog view | — | ID forecast_value komponen arus utara. |
| `forecast_run_id` | `uuid` | Tidak dijamin NOT NULL oleh catalog view | — | Identitas vintage/run regional. |
| `source_grid_id` | `uuid` | Tidak dijamin NOT NULL oleh catalog view | — | Identitas sel/titik grid sumber. |
| `valid_at` | `timestamp with time zone` | Tidak dijamin NOT NULL oleh catalog view | — | Waktu nilai model berlaku. |
| `ingested_at` | `timestamp with time zone` | Tidak dijamin NOT NULL oleh catalog view | — | Waktu data masuk sistem. |
| `available_at` | `timestamp with time zone` | Tidak dijamin NOT NULL oleh catalog view | — | Waktu ketersediaan pasangan; maksimum ingestion kedua komponen. |
| `speed_m_s` | `double precision` | Tidak dijamin NOT NULL oleh catalog view | — | Besar vektor arus hasil sqrt(u²+v²), m/s. |
| `derivation` | `text` | Tidak dijamin NOT NULL oleh catalog view | — | Rumus dan versi derivasi hasil view. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

Tidak ada PK/unique/CHECK yang dideklarasikan pada objek ini.

## Relasi keluar

Tidak ada foreign key yang dideklarasikan.

Dependensi logis: dua baris [[Supabase - seagis.forecast_value]] sebagai komponen timur dan utara; tidak ada FK fisik pada view.

## Relasi masuk

Tidak ada FK dari tabel lain menuju objek ini.

## Indeks

Tidak ada indeks fisik pada objek ini.

## Trigger dan batas mutasi

Tidak ada user trigger pada objek ini dalam snapshot catalog. Pembatasan akses dan rutin API tetap dapat membatasi penulisan.

## Akses

View memakai `security_invoker=true` pada migrasi A2; hak akses dan RLS tabel dasar berlaku untuk pemanggil.

## Sumber dan batas snapshot

Metadata: [schema-metadata-20261022.json](schema-metadata-20261022.json), diambil melalui SELECT catalog dalam transaksi READ ONLY; tidak menyalin isi tabel.

Source implementasi: [migrasi Seagis-Model](https://github.com/De-Voeux/Seagis-Model/tree/e93a005c95d746e6e33a6adad12760e94eb8a6cf/supabase/migrations), commit `e93a005c95d746e6e33a6adad12760e94eb8a6cf`. Penjelasan fungsi tabel diturunkan dari migrasi dan handover A0–A3; definisi kolom/constraint mengikuti catalog live. Snapshot tidak otomatis diperbarui bila database berubah.

## Definisi view

```sql
 SELECT u.id AS eastward_value_id,
    v.id AS northward_value_id,
    u.forecast_run_id,
    u.source_grid_id,
    u.valid_at,
    u.ingested_at,
    GREATEST(u.ingested_at, v.ingested_at) AS available_at,
        CASE
            WHEN ((u.value_status = 'present'::text) AND (v.value_status = 'present'::text)) THEN sqrt((((u.value)::double precision * (u.value)::double precision) + ((v.value)::double precision * (v.value)::double precision)))
            ELSE NULL::double precision
        END AS speed_m_s,
    'sqrt(uo^2+vo^2); a2-vector-magnitude-v1'::text AS derivation
   FROM (seagis.forecast_value u
     JOIN seagis.forecast_value v ON (((u.forecast_run_id = v.forecast_run_id) AND (u.source_grid_id = v.source_grid_id) AND (u.valid_at = v.valid_at))))
  WHERE ((u.parameter_code = 'current_eastward'::text) AND (v.parameter_code = 'current_northward'::text));
```
