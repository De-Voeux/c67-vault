---
type: engineering-handover
project: "[[Challenge Final]]"
created: 2026-10-23
updated: 2026-10-23
tags: [challenge-final, seagis, engineering, csv, forecasting]
source_repo: /Users/cindyram/Documents/Apple/Seagis-Model
source_path: docs/experiment_csv.md
source_commit: 291b6c5fdc7c990660ea98b1dcf676f6c0b58148
---

# Ekspor CSV per fitur untuk eksperimen forecast

Layout ini menggantikan enam CSV gabungan sebelumnya sesuai permintaan pengguna. Setiap CSV hanya memuat satu parameter. Capture sumber tetap sama: **23 Oktober 2026, 08:50 WIB / 01:50 UTC**. Tidak mengambil data baru, mengubah database atau menjalankan model.

Buka `data/exports/forecast-20261023T015005Z/features/` di repo `/Users/cindyram/Documents/Apple/Seagis-Model`.

## File per fitur

| CSV dalam features/ | Parameter / sumber | Baris |
| --- | --- | --- |
| `water_temperature_plot-a.csv` | Suhu air sintetis Plot A, hourly | 72 |
| `water_temperature_plot-b.csv` | Suhu air sintetis Plot B, hourly | 72 |
| `salinity.csv` | Salinitas model regional, 1e-3, cadence 6 jam | 5 |
| `current_eastward.csv` | Komponen arus timur, m/s, cadence 6 jam | 5 |
| `current_northward.csv` | Komponen arus utara, m/s, cadence 6 jam | 5 |
| `nitrate.csv` | Nitrate model, mmol/m3, mean harian | 2 |
| `phosphate.csv` | Phosphate model, mmol/m3, mean harian | 2 |
| `precipitation.csv` | Hujan model, mm, sum satu jam sebelumnya | 26 |
| `wind_speed_10m.csv` | Kecepatan angin 10 m, m/s, hourly | 26 |
| `wind_direction_10m.csv` | Arah angin 10 m, degree, hourly | 26 |
| `cloud_cover.csv` | Tutupan awan, percent, hourly | 26 |
| `uv_index.csv` | Indeks UV, tanpa dimensi, hourly | 26 |
| `air_temperature_2m.csv` | Suhu udara 2 m, degC, hourly | 26 |

Ada **13 file** untuk 12 parameter; suhu air memakai dua file karena berbeda plot. Data regional dibagi bersama sesuai grid dan tidak digandakan menjadi data farm per plot. Suhu udara bukan suhu air. Tidak ada interpolasi, pengisian nol atau penggandaan nutrien harian menjadi sampel hourly.

CSV berformat UTF-8, delimiter koma, decimal point titik dan nilai hilang berupa field kosong. `timestamp_utc` merupakan observed time untuk sensor atau valid time untuk model. `timestamp_wib` membantu membaca waktu lokal. Kolom utama untuk eksplorasi adalah `timestamp_utc`, `value` dan `unit`.

## Suhu air sintetis

Dua seri suhu mencakup 19 Oktober 00:00 sampai 21 Oktober 23:00 UTC, inklusif. Masing-masing berisi 72 slot hourly, 68 paket asli, empat gap tanpa paket, satu paket missing dan satu nilai uji 99 degC yang rejected. Terdapat **66 value numerik dan enam kosong** per file.

`value` memakai present finite non-rejected untuk mencoba kode pada dummy; sumber suspect termasuk rapid-change masih dapat masuk. `raw_value` mempertahankan nilai present asli, termasuk 99. `qc_flags`, `quality_status`, `value_status`, `is_gap`, `observation_id` dan `available_at_utc` tetap menyertai setiap timestamp. Semua paket diunggah terlambat; tidak ada sumber accepted pada capture ini. `strict_source_qc_pass` dan `training_authorized` tetap False. Jangan menumpuk dua plot menjadi satu urutan waktu.

## Pemilihan versi data regional

CSV regional memakai **vintage terbaru yang sudah tersedia saat capture**, secara terpisah untuk setiap dataset/grid/parameter/valid time. Ranking: `available_at`, `run_ingested_at`, forecast run ID dan record ID sebagai tie-break stabil. Missing pada versi terbaru tetap missing; tidak diganti versi lama. Hasilnya 175 baris regional dari 513 record sumber dalam sembilan vintages.

Ini adalah tampilan eksplorasi berdasarkan pengetahuan saat capture. File ini tidak menerapkan cutoff pengetahuan ulang pada setiap timestamp historis. Jangan menggunakannya sebagai backtest as-of tanpa memperhatikan availability dan issue time. Semua revisi asli tetap ada di `source_bundles.json`; dokumen `plot-a_alignment.json` dan `plot-b_alignment.json` mempertahankan hasil A3 hourly as-of beserta seluruh flags dan lineage.

Setiap file regional membawa `id`, `source_grid_id`, `forecast_run_id`, `dataset_key`, unit native/normalized, status, QC, cadence, interval, attribution/license URL dan waktu availability. Field `selection_basis=latest_available_at_capture` membedakan pemilihan ini dari alignment A3. Unknown issue/init time tetap kosong. Pada capture ini setiap parameter memakai satu grid; jika ekspor selanjutnya memiliki beberapa grid, pilih satu grid/dataset sebelum membentuk seri univariat.

## Membaca satu fitur

```python
from pathlib import Path
import pandas as pd

folder = Path("data/exports/forecast-20261023T015005Z/features")
df = pd.read_csv(folder / "salinity.csv", parse_dates=["timestamp_utc"])
y = df.set_index("timestamp_utc")["value"].sort_index()
print(y)
```

Ganti nama file untuk mengeksplorasi fitur lain. Cadence tidak otomatis hourly: salinitas/arus enam jam, nutrien harian, cuaca hourly. Jangan menghapus missing lalu menganggap jarak antarsampel masih sama. Pemilihan model, seasonality, train/test dan penanganan missing ditentukan dalam eksperimen terpisah.

## Audit dan ekspor ulang

- `source_bundles.json`: capture asli 136 observasi sintetis + 513 nilai regional; kontrak, mapping, attribution dan semua vintage tetap dipertahankan.
- `plot-a_alignment.json` / `plot-b_alignment.json`: konteks A3 asli dengan cutoff. Target suhu usable A3 tetap nol karena paket masuk terlambat dan suspect/stale.
- `manifest.json`: layout `experiment-csv-2`, jumlah baris tiap CSV, units, capture time, versi A3, exporter hash dan SHA-256 file secara rekursif.

Enam CSV layout lama di root paket sudah dihapus; tidak ada lagi context CSV gabungan atau native CSV campuran. Penghapusan hanya mencakup CSV yang dibuat pada tugas ekspor sebelumnya. Source JSON dan alignment JSON tetap berada di root paket.

Ekspor ulang tanpa cloud, menggunakan output folder baru:

```sh
uv run --frozen python scripts/export_experiment_csv.py \
  --source-json data/exports/forecast-20261023T015005Z/source_bundles.json \
  --out data/exports/forecast-replay
```

Tanpa `--source-json`, exporter mengambil bundle read-only terbaru untuk dua plot demo dengan role A3 terbatas, window cutoff maksimal tujuh hari serta lookback A3. Tidak ada provider fetch atau persist database. Folder output harus baru; overwrite ditolak. Angka dalam panduan ini milik capture 08:50 WIB, bukan jaminan ekspor selanjutnya sama.

CSV dan JSON numerik tetap di `data/` yang diabaikan Git; exporter dan panduan di-commit. Seluruh data suhu masih sintetis selama tiga hari, dan regional adalah keluaran model, sehingga paket ini belum menjadi bukti akurasi forecast farm atau diagnosis ice-ice.


## Buka CSV per fitur

- [air_temperature_2m.csv](</Users/cindyram/Documents/Apple/Seagis-Model/data/exports/forecast-20261023T015005Z/features/air_temperature_2m.csv>)
- [cloud_cover.csv](</Users/cindyram/Documents/Apple/Seagis-Model/data/exports/forecast-20261023T015005Z/features/cloud_cover.csv>)
- [current_eastward.csv](</Users/cindyram/Documents/Apple/Seagis-Model/data/exports/forecast-20261023T015005Z/features/current_eastward.csv>)
- [current_northward.csv](</Users/cindyram/Documents/Apple/Seagis-Model/data/exports/forecast-20261023T015005Z/features/current_northward.csv>)
- [nitrate.csv](</Users/cindyram/Documents/Apple/Seagis-Model/data/exports/forecast-20261023T015005Z/features/nitrate.csv>)
- [phosphate.csv](</Users/cindyram/Documents/Apple/Seagis-Model/data/exports/forecast-20261023T015005Z/features/phosphate.csv>)
- [precipitation.csv](</Users/cindyram/Documents/Apple/Seagis-Model/data/exports/forecast-20261023T015005Z/features/precipitation.csv>)
- [salinity.csv](</Users/cindyram/Documents/Apple/Seagis-Model/data/exports/forecast-20261023T015005Z/features/salinity.csv>)
- [uv_index.csv](</Users/cindyram/Documents/Apple/Seagis-Model/data/exports/forecast-20261023T015005Z/features/uv_index.csv>)
- [water_temperature_plot-a.csv](</Users/cindyram/Documents/Apple/Seagis-Model/data/exports/forecast-20261023T015005Z/features/water_temperature_plot-a.csv>)
- [water_temperature_plot-b.csv](</Users/cindyram/Documents/Apple/Seagis-Model/data/exports/forecast-20261023T015005Z/features/water_temperature_plot-b.csv>)
- [wind_direction_10m.csv](</Users/cindyram/Documents/Apple/Seagis-Model/data/exports/forecast-20261023T015005Z/features/wind_direction_10m.csv>)
- [wind_speed_10m.csv](</Users/cindyram/Documents/Apple/Seagis-Model/data/exports/forecast-20261023T015005Z/features/wind_speed_10m.csv>)

Navigasi: [[Pipeline Seagis A0-A3 - Alur dan Skematik]] · [[Peta Database Supabase Seagis]] · [[Indeks - Engineering]].
