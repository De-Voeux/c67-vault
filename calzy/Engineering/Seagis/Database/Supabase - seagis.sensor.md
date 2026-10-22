---
type: reference
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, supabase]
---

# seagis.sensor

Perangkat sensor suhu yang terikat ke plot, dataset dan parameter. Indeks parsial membatasi satu sensor suhu aktif per plot.

- Jenis: tabel PostgreSQL. Schema: `seagis`.
- Database/project: `seagis-model-database` / `kibztbeviortyvbedogg`.
- Snapshot metadata live: `2026-10-22T10:42:58.974431+00:00`. Migrasi terpasang: `0001`–`0005`.
- Navigasi: [[Peta Database Supabase Seagis]].

## Kolom

| Kolom | Tipe PostgreSQL | NULL diizinkan | Default / generated | Arti |
| --- | --- | --- | --- | --- |
| `id` | `uuid` | Tidak | `gen_random_uuid()` | Identitas baris; lihat PK/default dan constraint khusus tabel. |
| `sensor_code` | `text` | Tidak | — | Kode sensor yang unik. |
| `plot_id` | `uuid` | Tidak | — | Identitas plot budidaya terkait. |
| `dataset_key` | `text` | Tidak | — | Identitas dataset dalam registri Seagis. |
| `scope` | `text` | Tidak | `'local_sensor'::text` | Lingkup data: sensor lokal atau model regional sesuai CHECK. |
| `parameter_code` | `text` | Tidak | `'water_temperature'::text` | Kode parameter lingkungan. |
| `depth_m` | `seagis.finite_float` | Ya | — | Kedalaman dalam meter. |
| `depth_status` | `text` | Tidak | — | Status pengetahuan kedalaman. |
| `is_synthetic` | `boolean` | Tidak | — | Penanda data/identitas sintetis; tidak disamakan dengan data lapangan. |
| `active` | `boolean` | Tidak | `true` | Flag sensor aktif. |

Tipe `seagis.finite_float` adalah domain double precision yang menolak NaN dan ±Infinity; NULL tetap mengikuti nullability kolom. Timestamp `timestamp with time zone` menyimpan instan waktu; tampilan zona waktu mengikuti session.

## Primary key, unique dan pemeriksaan nilai

- `sensor_check`

```sql
CHECK (depth_status <> 'unknown'::text OR depth_m IS NULL)
```

- `sensor_check1`

```sql
CHECK (depth_status = 'unknown'::text OR depth_m IS NOT NULL)
```

- `sensor_check2`

```sql
CHECK (depth_status <> 'synthetic'::text OR is_synthetic)
```

- `sensor_depth_m_check`

```sql
CHECK (depth_m::double precision >= 0::double precision)
```

- `sensor_depth_status_check`

```sql
CHECK (depth_status = ANY (ARRAY['unknown'::text, 'measured'::text, 'synthetic'::text]))
```

- `sensor_id_plot_id_dataset_key_is_synthetic_key`

```sql
UNIQUE (id, plot_id, dataset_key, is_synthetic)
```

- `sensor_parameter_code_check`

```sql
CHECK (parameter_code = 'water_temperature'::text)
```

- `sensor_pkey`

```sql
PRIMARY KEY (id)
```

- `sensor_scope_check`

```sql
CHECK (scope = 'local_sensor'::text)
```

- `sensor_sensor_code_key`

```sql
UNIQUE (sensor_code)
```

## Relasi keluar

| Anak dan kolom FK | Induk dan kolom tujuan | Kewajiban / kardinalitas maksimum |
| --- | --- | --- |
| [[Supabase - seagis.sensor]] (dataset_key, parameter_code) | [[Supabase - seagis.dataset_parameter]] (dataset_key, parameter_code) | Wajib; 0..N anak per induk |
| [[Supabase - seagis.sensor]] (dataset_key, scope) | [[Supabase - seagis.dataset]] (dataset_key, scope) | Wajib; 0..N anak per induk |
| [[Supabase - seagis.sensor]] (plot_id, is_synthetic) | [[Supabase - seagis.plot]] (id, is_synthetic) | Wajib; 0..N anak per induk |

Definisi FK persis dari database:

```sql
FOREIGN KEY (dataset_key, parameter_code) REFERENCES seagis.dataset_parameter(dataset_key, parameter_code);
FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset(dataset_key, scope);
FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot(id, is_synthetic);
```

## Relasi masuk

- [[Supabase - seagis.observation]]: `(sensor_id, plot_id, dataset_key, is_synthetic)` → `(id, plot_id, dataset_key, is_synthetic)`.
- [[Supabase - seagis_api.credential]]: `(sensor_id)` → `(id)`.
- [[Supabase - seagis_api.packet_receipt]]: `(sensor_id)` → `(id)`.
- [[Supabase - seagis_api.request_event]]: `(sensor_id)` → `(id)`.

## Indeks

```sql
CREATE UNIQUE INDEX one_active_temperature_sensor_per_plot ON seagis.sensor USING btree (plot_id) WHERE active;
CREATE UNIQUE INDEX sensor_id_plot_id_dataset_key_is_synthetic_key ON seagis.sensor USING btree (id, plot_id, dataset_key, is_synthetic);
CREATE UNIQUE INDEX sensor_pkey ON seagis.sensor USING btree (id);
CREATE UNIQUE INDEX sensor_sensor_code_key ON seagis.sensor USING btree (sensor_code);
```

## Trigger dan batas mutasi

```sql
CREATE TRIGGER guard_sensor_deployment BEFORE UPDATE ON seagis.sensor FOR EACH ROW EXECUTE FUNCTION seagis.guard_sensor_deployment();
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
