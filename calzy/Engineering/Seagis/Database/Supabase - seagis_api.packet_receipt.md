---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis_api.packet_receipt

Bukti penerimaan paket sensor dan hash semantiknya, untuk idempotensi/deteksi konflik serta hubungan ke observation dan ingestion_run.

- Jenis: tabel PostgreSQL. Schema: `seagis_api`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `sensor_id` | `uuid` | Tidak | — | Identitas sensor terkait. |
| `source_record_key` | `text` | Tidak | — | Identitas record/paket sumber per sensor. |
| `semantic_sha256` | `text` | Tidak | — | Hash makna paket untuk pemeriksaan replay/konflik. |
| `observation_id` | `uuid` | Tidak | — | Identitas observasi sensor sumber. |
| `ingestion_run_id` | `uuid` | Tidak | — | Identitas proses ingestion asal. |
| `flags` | `text[]` | Tidak | — | Daftar flag QC paket. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `packet_receipt_observation_id_key`

```sql
UNIQUE (observation_id)
```

- `packet_receipt_pkey`

```sql
PRIMARY KEY (sensor_id, source_record_key)
```

- `packet_receipt_semantic_sha256_check`

```sql
CHECK (semantic_sha256 ~ '^[0-9a-f]{64}$'::text)
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis_api.packet_receipt]] (ingestion_run_id) | [[Supabase - seagis.ingestion_run]] (id) | Wajib; 0..N anak per induk |
| [[Supabase - seagis_api.packet_receipt]] (observation_id) | [[Supabase - seagis.observation]] (id) | Wajib; maksimal 1 anak per induk |
| [[Supabase - seagis_api.packet_receipt]] (sensor_id) | [[Supabase - seagis.sensor]] (id) | Wajib; 0..N anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (ingestion_run_id) REFERENCES seagis.ingestion_run(id);
FOREIGN KEY (observation_id) REFERENCES seagis.observation(id);
FOREIGN KEY (sensor_id) REFERENCES seagis.sensor(id);
```

## Relasi masuk

Tidak ada FK dari tabel lain menuju objek ini.

## Indeks

```sql
CREATE UNIQUE INDEX packet_receipt_observation_id_key ON seagis_api.packet_receipt USING btree (observation_id);
CREATE UNIQUE INDEX packet_receipt_pkey ON seagis_api.packet_receipt USING btree (sensor_id, source_record_key);
```

## Trigger dan batas mutasi

```sql
CREATE TRIGGER receipt_append_only BEFORE DELETE OR UPDATE ON seagis_api.packet_receipt FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
```

Definisi di atas menunjukkan routine guard yang dipanggil. Isi routine selengkapnya berada pada migrasi source; CHECK/FK saja tidak menggambarkan semua guard lintas tabel.

## Akses

RLS: **aktif**. FORCE RLS: **tidak aktif**. RLS aktif tidak berarti semua role boleh membaca tabel; owner/role dengan bypass memiliki perilaku tersendiri. Snapshot ini tidak mengekspor daftar role membership maupun seluruh privilege.

Tidak ada policy RLS tercatat untuk tabel ini. Role biasa yang terkena RLS tidak mendapat izin row melalui policy; jalur runtime menggunakan routine privat sesuai dokumentasi A1/A2/A3.

## Sumber dan batas snapshot

Metadata: [schema-metadata-20261022.json](schema-metadata-20261022.json), diambil melalui SELECT catalog dalam transaksi READ ONLY; tidak menyalin isi tabel.

Source implementasi: [migrasi Seagis-Model](https://github.com/De-Voeux/Seagis-Model/tree/e93a005c95d746e6e33a6adad12760e94eb8a6cf/supabase/migrations), commit `e93a005c95d746e6e33a6adad12760e94eb8a6cf`. Penjelasan fungsi tabel diturunkan dari migrasi dan handover A0–A3; definisi kolom/constraint mengikuti catalog live. Snapshot tidak otomatis diperbarui bila database berubah.
