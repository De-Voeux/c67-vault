# Kontrak data v0.1.0

Kontrak A0 memisahkan payload provider dari representasi normalized. JSON Schema Draft 2020-12 berada di [source schema](../contracts/source.schema.json) dan [normalized schema](../contracts/normalized.schema.json). `scripts/validate_contracts.py` menambahkan pemeriksaan lintas field: unit, finite numbers, hash, urutan waktu, dukungan temporal, identitas sumber, grid/kedalaman, dan kesesuaian contoh dengan sumbernya. Ini validator kontrak/fixture, bukan adapter ingestion production.

## Contoh per sumber

Semua contoh di bawah memiliki `is_synthetic=true`. Sensor ID, grid, waktu, dan angka contoh tidak menyatakan deployment/peristiwa nyata di Pulau Tidung.

| Dataset | Payload sumber lengkap | Representasi normalized lengkap |
| --- | --- | --- |
| Sensor suhu lokal | [sensor.json](../fixtures/source/sensor.json) | [sensor normalized](../fixtures/normalized/sensor.json) |
| Copernicus salinitas | [salinity.json](../fixtures/source/copernicus_salinity.json) | [salinity normalized](../fixtures/normalized/copernicus_salinity.json) |
| Copernicus komponen arus | [currents.json](../fixtures/source/copernicus_currents.json) | [currents normalized](../fixtures/normalized/copernicus_currents.json) |
| Copernicus nutrien | [nutrients.json](../fixtures/source/copernicus_nutrients.json) | [nutrients normalized](../fixtures/normalized/copernicus_nutrients.json) |
| Open-Meteo | [open_meteo.json](../fixtures/source/open_meteo.json) | [weather normalized](../fixtures/normalized/open_meteo.json) |

Sensor mengirim satu pembacaan per packet, dengan `boot_id` dan sequence monoton dalam satu boot untuk idempotensi. Potongan `payload` dari fixture:

```json
{
  "sensor_id": "00000000-0000-4000-8000-000000000101",
  "boot_id": "synthetic-boot-a",
  "sequence": 1,
  "observed_at": "2026-10-21T12:00:00Z",
  "water_temperature": 29.2,
  "unit": "degC",
  "value_status": "present",
  "detection_limit": null
}
```

Token perangkat, autentikasi, format hardware final, batas payload, clock-skew policy, dan HTTP response A1 belum diimplementasikan. Jangan menerima `is_synthetic` dari perangkat sebagai dasar trust; endpoint nanti menetapkannya dari identitas sensor/simulator yang terdaftar.

Copernicus memberi data NetCDF/Zarr. File `.json` di fixture adalah **representasi logical extract satu sel** untuk review kontrak, bukan klaim wire format resmi. Fixture membawa koordinat time/depth/lat/lon, unit dan fill value tiap variabel, serta values. Adapter A2 harus membaca atribut CF asli (`units`, calendar, scale/offset, fill/mask, time bounds), menyimpan byte asli bila diizinkan, lalu memilih sel/layer yang terdokumentasi. Native integer packing harus didekode sebelum nilai fisik masuk normalized; scale/offset asal tetap dicatat pada metadata. Tidak ada full NetCDF download/parsing dalam A0.

Open-Meteo menggunakan struktur JSON `hourly_units` dan array sejajar `hourly`. Respons contoh hanya memuat satu jam. Request model/unit/timezone masuk envelope `provider_metadata.request_parameters`, bukan ditambahkan seolah field bawaan API. String waktu API tanpa suffix zona ditafsirkan sebagai UTC **hanya setelah** `utc_offset_seconds=0` dan timezone UTC/GMT diverifikasi. `generationtime_ms` dipertahankan sebagai durasi respons; tidak dipakai untuk mengisi `issued_at`.

## Envelope sumber dan normalized

Source envelope membawa `schema_version`, `source_type`, `dataset_key`, `is_synthetic`, `received_at`, `provider_metadata`, dan `payload`. Envelope ini membungkus data; tidak mengubah provenance provider. Raw JSON fixture menggunakan hash atas objek `payload` saja. Metadata disimpan tersendiri dan immutable dalam `seagis_raw.raw_payload.provider_metadata`.

Normalized envelope umum berisi:

| Bagian | Kebutuhan |
| --- | --- |
| `schema_version`, `dataset_key` | Versi kontrak serta key dataset terdaftar |
| `ingestion_run` | UUID, request key, adapter version, start/end/status, flag sintetis |
| `raw_payload` | UUID, SHA-256, receipt, format, snapshot keterangan lisensi |
| `forecast_run` | Null untuk sensor; metadata capture/issue/init terpisah untuk model regional |
| `source_grid` | Null untuk sensor; satu identitas sel/layer untuk envelope regional |
| `measurements[]` | Item bertipe `observation` atau `forecast_value` dengan unit native dan normalized |

Potongan representasi measurement umum pada dua origin:

```json
[
  {
    "kind": "observation",
    "parameter_code": "water_temperature",
    "native_value": 29.2,
    "native_unit": "degC",
    "value": 29.2,
    "unit": "degC",
    "value_status": "present",
    "observed_at": "2026-10-21T12:00:00Z"
  },
  {
    "kind": "forecast_value",
    "parameter_code": "nitrate",
    "native_value": 0.0,
    "native_unit": "mmol m-3",
    "value": 0.0,
    "unit": "mmol/m3",
    "value_status": "present",
    "valid_at": "2026-10-22T00:00:00Z",
    "temporal_support": "mean",
    "interval_status": "unknown",
    "period_start_at": null,
    "period_end_at": null
  }
]
```

Potongan ini menjelaskan field dan bukan envelope lengkap yang lolos schema; seluruh UUID/FK, metadata run/grid, timestamps ingestion, quality, dan konversi ada di fixture lengkap. Nilai nitrate nol tetap modelled zero; phosphate null dalam fixture yang sama berstatus missing. Daily mean tidak berubah menjadi 24 sampel hourly.

## Aturan yang harus dipertahankan adapter

1. Scope ditentukan dataset dan identitas asal. Sensor lokal harus memiliki plot+sensor yang cocok; model regional harus memiliki run+grid yang cocok. Kolom plot tidak ditambahkan pada `forecast_value` untuk menggandakan satu sel bagi banyak plot.
2. Semua normalized timestamps berzona UTC. Availability sistem adalah `ingested_at`, bukan `valid_at`. Field `issued_at` hanya berisi metadata penerbitan yang dapat ditelusuri; `model_initialized_at` tidak otomatis publication time. Unknown tetap null, dengan missing-context flag saat feature/assessment dibuat.
3. `native_value` dan native unit tidak ditimpa saat normalisasi. A0 hanya mengubah notasi beberapa unit, tanpa konversi angka. Unit lain memerlukan registry/kontrak versi baru. `so` dipertahankan dalam `1e-3`; tidak relabel PSU/ppt tanpa dasar tambahan.
4. NaN, infinity, fill value, dan masked cells tidak boleh menjadi measurement present. Null harus membawa alasan `missing`, `not_available`, atau batas deteksi yang diketahui. Rentang domain/QC sensor penuh adalah A1/A3.
5. Retry identik tidak menambah reading. Konflik identity dengan konten berbeda harus dicatat dan ditangani eksplisit. Revisi forecast menjadi run/capture baru. `provider_run_id`, hash capture, versi produk, model, source grid, native cadence, dan metode sampling tetap ditelusuri lewat row/metadata.
6. Presipitasi adalah total `(valid_at − 1 jam, valid_at]`; simpan awal/akhir interval. Mean yang time bounds-nya belum diketahui membawa interval unknown. Jangan mengisi bounds dari tebakan.
7. API key, password, Authorization header, dan signed download URL tidak masuk raw metadata atau error log. URI Storage adalah referensi privat stabil; lifecycle dan akses bucket baru ditetapkan jika bucket diperlukan.

## Menjalankan validasi

```sh
uv run --frozen python scripts/validate_contracts.py
uv run --frozen python scripts/check_a0.py
```

Pemeriksaan pertama memvalidasi lima pasangan fixture; yang kedua juga memasukkan contoh ke database kosong untuk memeriksa FK, unit registry, lineage, revision, RLS, dan cutoff. Menambah source/dataset harus disertai perubahan schema/registry, contoh positif dan negatif, serta dokumentasi versi. Perubahan breaking memerlukan versi kontrak baru.
