---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis_features.feature_input

Lineage setiap input yang dipakai feature_snapshot: tepat satu observasi atau satu forecast_value per baris.

- Jenis: tabel PostgreSQL. Schema: `seagis_features`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | Tidak | `gen_random_uuid()` | Identitas baris; lihat PK/default dan constraint khusus tabel. |
| `snapshot_id` | `uuid` | Tidak | — | Identitas snapshot induk. |
| `observation_id` | `uuid` | Ya | — | Identitas observasi sensor sumber. |
| `forecast_value_id` | `uuid` | Ya | — | Identitas nilai regional sumber. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `feature_input_check`

```sql
CHECK (num_nonnulls(observation_id, forecast_value_id) = 1)
```

- `feature_input_pkey`

```sql
PRIMARY KEY (id)
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis_features.feature_input]] (forecast_value_id) | [[Supabase - seagis.forecast_value]] (id) | Opsional / MATCH SIMPLE; 0..N anak per induk |
| [[Supabase - seagis_features.feature_input]] (observation_id) | [[Supabase - seagis.observation]] (id) | Opsional / MATCH SIMPLE; 0..N anak per induk |
| [[Supabase - seagis_features.feature_input]] (snapshot_id) | [[Supabase - seagis_features.feature_snapshot]] (id) | Wajib; 0..N anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (forecast_value_id) REFERENCES seagis.forecast_value(id);
FOREIGN KEY (observation_id) REFERENCES seagis.observation(id);
FOREIGN KEY (snapshot_id) REFERENCES seagis_features.feature_snapshot(id);
```

## Relasi masuk

Tidak ada FK dari tabel lain menuju objek ini.

## Indeks

```sql
CREATE UNIQUE INDEX feature_input_forecast ON seagis_features.feature_input USING btree (snapshot_id, forecast_value_id) WHERE (forecast_value_id IS NOT NULL);
CREATE UNIQUE INDEX feature_input_observation ON seagis_features.feature_input USING btree (snapshot_id, observation_id) WHERE (observation_id IS NOT NULL);
CREATE UNIQUE INDEX feature_input_pkey ON seagis_features.feature_input USING btree (id);
```

## Trigger dan batas mutasi

```sql
CREATE TRIGGER append_only BEFORE DELETE OR UPDATE ON seagis_features.feature_input FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
CREATE TRIGGER guard_feature_input BEFORE INSERT ON seagis_features.feature_input FOR EACH ROW EXECUTE FUNCTION seagis_features.guard_input();
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
