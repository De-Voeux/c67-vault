# Kamus data A0

Sumber definisi executable: [migrasi 0001](../supabase/migrations/0001_initial_schema.sql). Versi kontrak `0.1.0`. Nama field mengikuti SQL; tabel berikut mengelompokkan field tanpa menyembunyikan provenance. Kolom nullable ditandai `null`; yang lain wajib, dengan default bila ditentukan SQL.

## Tipe dan aturan lintas tabel

- `uuid`: primary key atau foreign key. `id` default `gen_random_uuid()` kecuali fixture memakai ID stabil.
- `timestamptz`: instan waktu; API kontrak wajib UTC `Z`. PostgreSQL menyimpan instannya dan menampilkan sesuai timezone session. Gunakan session UTC untuk export. Input tanpa zona ditolak validator kontrak.
- `finite_float`: double precision yang menolak NaN dan ±Infinity. Ini batas representasi data, bukan ambang biologis atau QC rentang alamiah.
- `is_synthetic`: boolean wajib, diwariskan dari ingestion/plot. Composite FK mencegah pencampuran baris nyata dan sintetis. Status ini terpisah dari `quality_status`.
- `value_status`: `present`, `missing`, `below_detection_limit`, `not_available`. Present mensyaratkan nilai native dan normalized non-null. Selain present, keduanya null. Batas deteksi wajib hanya untuk `below_detection_limit`, dinyatakan pada unit normalized.
- `quality_status`: `unreviewed`, `accepted`, `suspect`, `rejected`. Tidak berarti diagnosis penyakit; A0 belum menjalankan QC otomatis.

Nilai `0` dengan status `present` adalah **measured zero** pada `observation`, **modeled zero** pada `forecast_value`; null tidak sama dengan nol. Paket sensor yang sama sekali tidak datang adalah gap, bukan baris observasi nol.

## Referensi sumber, parameter, dan plot — schema `seagis`

| Tabel | Field | Arti / constraint |
| --- | --- | --- |
| `source` | `source_key` PK, `provider`, `documentation_url` | Identitas provider yang dirujuk dataset |
| `dataset` | `dataset_key` PK, `source_key` FK | Identitas versi kontrak; sumber dapat memiliki beberapa dataset |
| | `provider_product_id` null, `provider_dataset_id`, `dataset_version` | Product dan dataset asli serta versi eksplisit |
| | `scope`, `native_cadence_seconds` | `local_sensor` atau `regional_model`; cadence >0 detik, bukan interval scheduler |
| | `resolution_lat_deg`, `resolution_lon_deg` null | Step geografis diketahui dalam derajat; null jika bervariasi/belum diverifikasi |
| | `source_timezone` default UTC | Zona asal bila relevan |
| | `licence_url`, `attribution`, `metadata_checked_at` | Bukti metadata serta wording attribution |
| | `raw_storage_permitted`, `real_ingestion_enabled` default false | Gate operasional A0; metadata identitas lain tidak boleh ditulis ulang |
| `parameter` | `parameter_code` PK, `unit`, `description` | Daftar parameter terbatas; UNIQUE `(parameter_code,unit)` |
| `dataset_parameter` | `dataset_key`, `parameter_code` PK gabungan | Field yang diizinkan untuk dataset itu |
| | `source_variable`, `native_unit`, `unit`, `conversion_code` | Nama asli dan unit per field; gabungan ini direferensikan measurement |
| | `conversion_factor` default 1, `conversion_offset` default 0 | `value = native_value × factor + offset`; diperiksa trigger dengan toleransi numerik 1e-8 relatif |
| | `temporal_support` | `instantaneous`, `mean`, `sum`; metadata immutable |
| `plot` | `id` PK, `plot_code` UNIQUE, `name` | Identitas plot, bukan nama grid |
| | `latitude`, `longitude` null | Derajat WGS84; keduanya terisi atau keduanya null |
| | `is_synthetic`, `location_status`, `created_at` | Status `synthetic`, `not_surveyed`, `surveyed`; surveyed membutuhkan koordinat |
| `sensor` | `id` PK, `sensor_code` UNIQUE, `plot_id`, `dataset_key`, `scope` | Deployment sensor suhu lokal; FK mengunci pasangan sensor–plot–dataset–synthetic |
| | `parameter_code`, `depth_m` null, `depth_status` | A0 hanya `water_temperature`; kedalaman positif ke bawah dalam **meter**, null jika unknown |
| | `is_synthetic`, `active` default true | Satu deployment suhu aktif per plot; deaktifkan sebelum deployment baru. Perubahan plot/kedalaman membuat deployment baru |

## Unit per field

| Parameter | Native pada dataset terpilih | Normalized | Konversi A0 |
| --- | --- | --- | --- |
| `water_temperature` | `degC` | `degC` | Identity; suhu air terendam |
| `salinity` | `1e-3` | `1e-3` | Identity; konvensi provider dipertahankan. Tidak otomatis menjadi PSU, ppt, atau g/kg |
| `current_eastward`, `current_northward` | `m s-1` | `m/s` | Notasi unit; komponen asli tetap disimpan |
| `nitrate`, `phosphate` | `mmol m-3` | `mmol/m3` | Notasi unit; konversi ke mg/L memerlukan basis spesies kimia yang belum dipilih |
| `precipitation` | `mm` | `mm` | Total satu jam sebelumnya; bukan intensitas mm/jam tanpa interval |
| `wind_speed_10m` | `m/s` diminta eksplisit | `m/s` | Identity; jangan menerima default km/h pada kontrak ini |
| `wind_direction_10m` | `°` | `degree` | Notasi; arah **dari**, searah jarum jam dari utara |
| `cloud_cover` | `%` | `percent` | Notasi; 60 berarti 60%, bukan 0,60 |
| `uv_index` | string unit kosong | `1` | Notasi tanpa dimensi |
| `air_temperature_2m` | `°C` | `degC` | Notasi; suhu udara pada 2 m, tidak disamakan dengan sensor air |

## Ingestion dan raw

| Tabel | Field | Arti / constraint |
| --- | --- | --- |
| `seagis.ingestion_run` | `id`, `dataset_key`, `request_key`, `adapter_version` | UNIQUE dataset+request key; identitas ingestion tetap |
| | `started_at`, `completed_at` null, `status` | Status `running` hanya bila belum selesai; selain itu end ≥ start |
| | `is_synthetic`, `error_code` null | Jangan memasukkan token, URL bertanda tangan, atau payload rahasia ke kode error |
| `seagis_raw.raw_payload` | `id`, `ingestion_run_id`, `dataset_key`, `is_synthetic` | Composite FK ke ingestion yang sama |
| | `sha256`, `hash_basis`, `byte_size`, `format` | SHA-256 lower-case 64 hex; ukuran bytes ≥0. Hash basis `source_bytes` atau `synthetic_json_canonical_v1` |
| | `received_at`, `licence_snapshot`, `provider_metadata` JSONB object | Timestamp receipt, keterangan lisensi saat capture, metadata response/request tanpa secrets |
| | `storage_mode`, `payload` null, `object_uri` null | `inline`: JSON sintetis + canonical hash; `object`: URI privat `storage://...` dan raw bytes disimpan apa adanya; `metadata_only`: kedua konten null, digest tetap ada |

Raw immutable. Untuk fixture, byte size/hash dihitung dari payload JSON dengan key urut leksikografis, separator tanpa spasi, UTF-8, dan `allow_nan=False`. Representasi JSONB di disk bukan sumber byte hash fixture. Nilai real harus memakai byte asli/object privat atau metadata-only; tidak memakai serialisasi ulang JSONB sebagai raw bytes. Validator aplikasi memeriksa kecocokan hash fixture; CHECK SQL hanya memeriksa bentuk digest, bukan menghitung ulang bytes object eksternal.

## Grid, observasi, dan forecast

| Tabel | Field | Arti / constraint |
| --- | --- | --- |
| `source_grid` | `id`, `dataset_key`, `scope`, `grid_key`, `grid_version` | Dataset regional saja; key mencakup sel/layer/versi. Identitas grid immutable |
| | `identity_basis` | `provider_cell`, `provider_returned_coordinate`, atau `synthetic`; returned coordinate tidak menjamin native cell asli |
| | `latitude`, `longitude`, `depth_m`, `is_synthetic` | Derajat dan meter; untuk atmosfer gunakan depth 0 sebagai sumbu permukaan, tinggi variabel tetap pada definisi field |
| `plot_grid_mapping` | `id`, `plot_id`, `source_grid_id`, `is_synthetic` | Banyak plot boleh memakai sel yang sama; tidak menggandakan forecast |
| | `sampling_method`, `distance_m` null, `representativeness` | Metode `nearest_wet_cell`, `nearest_cell`, `provider_returned_coordinate`, `synthetic`; meter; status `unverified`, `regional_only`, `land_mask_issue` |
| | `effective_from`, `effective_until` null | Rentang setengah terbuka `[from,until)`; end > start; pemilihan/penutupan mapping konsisten masih tanggung jawab adapter A2 |
| `observation` | `id`, `plot_id`, `sensor_id`, `dataset_key`, `ingestion_run_id`, `raw_payload_id`, `is_synthetic` | Provenance sensor lokal; dataset/plot/flag harus cocok melalui FK |
| | `source_record_key`, `parameter_code` | Boot ID + sequence dari packet; parameter A0 suhu air saja |
| | `native_value`, `native_unit`, `value`, `unit`, `conversion_code` | Nilai finite atau null sesuai status; FK ke dataset_parameter memeriksa satuan |
| | `value_status`, `detection_limit` null, `quality_status` | Missing dan kualitas terpisah dari nilai numerik |
| | `observed_at`, `ingested_at` | Waktu pengukuran asli dan waktu tersedia; ingest ≥ receipt raw. Clock skew/future observation dicatat QC pada A1/A3 |
| `forecast_run` | `id`, `dataset_key`, `scope`, `ingestion_run_id`, `raw_payload_id`, `is_synthetic` | Satu capture/revisi regional dengan raw dan ingestion yang sama |
| | `run_key`, `run_kind`, `provider_run_id` null | Key capture immutable; kind `forecast`/`analysis`; source run ID hanya jika tersedia |
| | `model_initialized_at` null, `issued_at` null, `issue_time_basis`, `ingested_at` | Unknown issue ↔ null; known issue dan initialization tidak boleh sesudah ingest |
| `forecast_value` | `id`, `forecast_run_id`, `source_grid_id`, `dataset_key`, `is_synthetic` | FK mengunci dataset/synthetic untuk run dan grid yang sama |
| | `parameter_code`, `native_value`, `native_unit`, `value`, `unit`, `conversion_code`, `value_status`, `detection_limit` null, `quality_status` | Aturan field sama dengan observasi; row berorigin model, bukan sensor |
| | `valid_at`, `ingested_at`, `temporal_support`, `interval_status`, `period_start_at` null, `period_end_at` null | Instantaneous: interval tidak berlaku. Mean/sum: interval known atau unknown dengan batas null. Presipitasi wajib interval known tepat satu jam berakhir di valid_at |

Untuk daily mean nutrien, cadence 86400 detik tetap native. Batas mean tidak dibuat dari tebakan tanggal; fixture mempertahankan `interval_status=unknown`. Tidak ada penggandaan menjadi 24 observasi independen. Kecepatan arus turunan `sqrt(uo²+vo²)` adalah pekerjaan A4, bukan parameter asli yang sudah dihitung A0.

## Kualitas dan fitur

| Tabel | Field | Arti / constraint |
| --- | --- | --- |
| `seagis.quality_event` | `id`, `ingestion_run_id`, `dataset_key`, `is_synthetic`, `event_key` | Log append-only; UNIQUE ingestion+event key |
| | `observation_id` null, `forecast_value_id` null | Maksimal satu target; keduanya null berarti kejadian tingkat ingestion. Dataset/ingestion harus konsisten |
| | `event_code`, `severity`, `details`, `created_at` | Kode stabil seperti `missing`, `stale`, `duplicate_conflict`; severity info/warning/error. Rincian JSON tanpa secrets |
| `seagis_features.feature_snapshot` | `id`, `plot_id`, `is_synthetic`, `as_of`, `generated_at` | Snapshot pada cutoff; generated ≥ as_of |
| | `feature_version`, `feature_schema_version`, `features`, `missing_context` | Versi builder/schema, JSON object, daftar indikator konteks yang tidak tersedia |
| | `status`, `input_manifest_sha256`, `features_sha256` | Draft tanpa manifest hash; sealed membutuhkan hash manifest nonempty. Features hash dihasilkan SQL dari JSONB text UTF-8 pada PostgreSQL 17 |
| `seagis_features.feature_input` | `id`, `snapshot_id`, `observation_id` null, `forecast_value_id` null | Tepat satu input FK; UNIQUE per snapshot+input. Guard menolak input masa depan, plot salah, flag salah, atau grid tak terpetakan pada cutoff |

Hash manifest adalah SHA-256 UTF-8 atas baris `observation:<uuid>` atau `forecast_value:<uuid>` yang diurutkan leksikografis dan dipisahkan newline, tanpa newline terakhir. Semua input ditambahkan dalam transaksi yang sama dengan pembuatan dan sealing snapshot. Guard mengambil row lock induk untuk menghindari perlombaan dengan sealing.

Contoh sealing setelah input lengkap:

```sql
UPDATE seagis_features.feature_snapshot
SET status = 'sealed', input_manifest_sha256 = seagis_features.manifest_hash(id)
WHERE id = :snapshot_id AND status = 'draft';
```

Table ini menegakkan lineage/cutoff, tetapi belum membuktikan isi fitur dihitung benar. Builder deterministik, versi kode, kebijakan QC, pemilihan vintage, dan kesamaan offline/online tetap harus dibangun serta diuji pada A3/A4.
