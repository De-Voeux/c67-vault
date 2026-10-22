---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis_api.request_event

Log request API yang dicatat rutin API: credential, sensor bila ada, HTTP status dan kode hasil. Bukan jaminan audit seluruh trafik karena ada cabang yang tidak dicatat.

- Jenis: tabel PostgreSQL. Schema: `seagis_api`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | Tidak | `gen_random_uuid()` | Identitas baris; lihat PK/default dan constraint khusus tabel. |
| `credential_id` | `uuid` | Tidak | — | Identitas credential yang diberi akses/membuat request. |
| `sensor_id` | `uuid` | Ya | — | Identitas sensor terkait. |
| `http_status` | `integer` | Tidak | — | HTTP status hasil API. |
| `code` | `text` | Tidak | — | Kode hasil API. |
| `created_at` | `timestamp with time zone` | Tidak | `clock_timestamp()` | Waktu pembuatan/pencatatan baris. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `request_event_pkey`

```sql
PRIMARY KEY (id)
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis_api.request_event]] (credential_id) | [[Supabase - seagis_api.credential]] (id) | Wajib; 0..N anak per induk |
| [[Supabase - seagis_api.request_event]] (sensor_id) | [[Supabase - seagis.sensor]] (id) | Opsional / MATCH SIMPLE; 0..N anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (credential_id) REFERENCES seagis_api.credential(id);
FOREIGN KEY (sensor_id) REFERENCES seagis.sensor(id);
```

## Relasi masuk

Tidak ada FK dari tabel lain menuju objek ini.

## Indeks

```sql
CREATE INDEX request_event_actor_time ON seagis_api.request_event USING btree (credential_id, created_at DESC);
CREATE UNIQUE INDEX request_event_pkey ON seagis_api.request_event USING btree (id);
```

## Trigger dan batas mutasi

```sql
CREATE TRIGGER request_event_append_only BEFORE DELETE OR UPDATE ON seagis_api.request_event FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
```

Definisi di atas menunjukkan routine guard yang dipanggil. Isi routine selengkapnya berada pada migrasi source; CHECK/FK saja tidak menggambarkan semua guard lintas tabel.

## Akses

RLS: **aktif**. FORCE RLS: **tidak aktif**. RLS aktif tidak berarti semua role boleh membaca tabel; owner/role dengan bypass memiliki perilaku tersendiri. Snapshot ini tidak mengekspor daftar role membership maupun seluruh privilege.

Tidak ada policy RLS tercatat untuk tabel ini. Role biasa yang terkena RLS tidak mendapat izin row melalui policy; jalur runtime menggunakan routine privat sesuai dokumentasi A1/A2/A3.

## Sumber dan batas snapshot

Metadata: [schema-metadata-20261022.json](schema-metadata-20261022.json), diambil melalui SELECT catalog dalam transaksi READ ONLY; tidak menyalin isi tabel.

Source implementasi: [migrasi Seagis-Model](https://github.com/De-Voeux/Seagis-Model/tree/e93a005c95d746e6e33a6adad12760e94eb8a6cf/supabase/migrations), commit `e93a005c95d746e6e33a6adad12760e94eb8a6cf`. Penjelasan fungsi tabel diturunkan dari migrasi dan handover A0–A3; definisi kolom/constraint mengikuti catalog live. Snapshot tidak otomatis diperbarui bila database berubah.
