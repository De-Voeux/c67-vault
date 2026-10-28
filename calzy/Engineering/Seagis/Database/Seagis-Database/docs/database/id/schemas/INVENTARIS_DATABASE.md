# INVENTARIS_DATABASE

Version: 1.0.0 | Date: 2026-10-27

[Dokumen lengkap](../DOKUMENTASI_DATABASE.md) | [README](../../README.md)

PostgreSQL/Supabase adalah persistence backend yang didefinisikan kode. Schema `seagis` berisi registri, observasi, forecast dan provenance; `seagis_raw` menyimpan manifest raw; `seagis_api` membatasi IoT gateway; `seagis_environment` mengatur worker regional; `seagis_quality` menyimpan review QC; `seagis_features` menyediakan container fitur yang belum dihubungkan ke builder produksi. Schema internal Supabase seperti auth/storage tidak diinventaris sebagai milik aplikasi: akses catalog terkini tidak tersedia dan tidak boleh diasumsikan kosong.

Python melakukan pengambilan provider di luar database. Worker A2/A3 memanggil stored function lewat psycopg; TS handler memanggil hanya fungsi ingest/history/status. Tidak ada ORM yang ditemukan pada jalur ini. Transaksi mutasi berada di fungsi SQL; claim fetch merupakan transaksi terpisah dari persistence agar panggilan jaringan tidak menahan transaksi database.

Diagram memperlihatkan dua komponen yang terputus: mock iOS tidak memiliki edge ke backend. Integrasi masa depan tetap UNVERIFIED. Core ML, cache terdistribusi, warehouse, queue dan search index produksi NOT FOUND dalam file implementasi yang diinspeksi; ini bukan bukti bahwa layanan di luar checkout tidak ada.

| Store | Evidence status | Tujuan/lingkungan | Owner | Scope | Access | Otoritas | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PostgreSQL / Supabase | VERIFIED (repository + historical catalog) | Backend; lingkungan deployment terkini UNVERIFIED | Seagis-Model | Registri, sensor, regional, QC, fitur | read/write via stored functions | Otoritatif untuk record yang tersimpan; bukan diagnosis | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:1` |
| Supabase Storage | configured / UNVERIFIED usage | Storage enabled lokal; object_uri didukung, bucket aplikasi NOT FOUND | Supabase | objects / metadata_only | configured | Tidak dibuktikan sebagai penyimpan raw aktif | `Seagis-Model/supabase/config.toml:116` |
| UserDefaults / launch arguments | VERIFIED code | Akses preferensi/debug UI; bukan penyimpan plot | AppPOC | initialPlot / initialFarmer / skipCaptureSteps / detailDay | read preference/argument values | Tidak otoritatif untuk data backend | `AppPOC/POCApp/Features/FarmMap/ViewModels/FarmMapViewModel.swift:1` |
| legacy AR files | VERIFIED cleanup code | File ar-site.json/ar-site.worldmap hanya dihapus saat sesi AR baru | AppPOC | legacy local AR files | best-effort delete; active writer NOT FOUND | Bukan persistence aktif | `AppPOC/POCApp/Features/PlotCapture/ViewModels/ARCaptureViewModel.swift:1` |
| JSON / CSV files | VERIFIED code | Fixture sintetis, policy, export eksperimen dan manifest | Python scripts | fixtures/config/export | file read/write | Hanya otoritatif untuk capture/fixture versinya | `Seagis-Model/scripts/export_experiment_csv.py:1` |
| in-memory Swift arrays | VERIFIED code | State prototype; hilang saat proses berakhir | AppPOC | Farmer / CultivationPlot | array append/remove | State demo lokal | `AppPOC/POCApp/Shared/Data/FarmStore.swift:1` |

Default layanan Supabase auth, vector dan analytics tercantum dalam config lokal, tetapi bucket/index/dataset aplikasi aktif tidak dibuktikan. Ini konfigurasi layanan, bukan database aplikasi tambahan. Jumlah baris seluruh tabel: UNVERIFIED; tidak diestimasi dari fixture.

| Schema | Objek | Tables | Views | Batas akses |
| --- | --- | --- | --- | --- |
| seagis | dataset, dataset_parameter, forecast_run, forecast_value, ingestion_run, observation, parameter, plot, plot_grid_mapping, quality_event, sensor, source, source_grid | 13 | 0 | Akses melalui routine backend; membership live UNVERIFIED |
| seagis_api | credential, packet_receipt, reader_plot, request_event, temperature_policy | 5 | 0 | Akses melalui routine backend; membership live UNVERIFIED |
| seagis_environment | attempt, current_speed, demo_grid_mapping, policy, schedule_state | 4 | 1 | Akses melalui routine backend; membership live UNVERIFIED |
| seagis_features | feature_input, feature_snapshot | 2 | 0 | Akses melalui routine backend; membership live UNVERIFIED |
| seagis_quality | alignment_snapshot, policy, snapshot_input | 3 | 0 | Akses melalui routine backend; membership live UNVERIFIED |
| seagis_raw | raw_payload | 1 | 0 | Akses melalui routine backend; membership live UNVERIFIED |

| Objek fisik | Fungsi | Kolom | Evidence |
| --- | --- | --- | --- |
| seagis.dataset | Identitas dataset, versi, cadence, lisensi dan gate ingestion. | 15 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:17` |
| seagis.dataset_parameter | Kontrak variabel sumber ke parameter dan aturan konversi. | 9 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:43` |
| seagis.forecast_run | Capture/vintage model regional; waktu publikasi yang tidak diketahui tetap null. | 13 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:216` |
| seagis.forecast_value | Nilai parameter per run, grid dan valid time; tidak diduplikasi per plot. | 20 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:241` |
| seagis.ingestion_run | Audit satu ingestion logis beserta status penyelesaian. | 9 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:94` |
| seagis.observation | Pembacaan suhu air sensor lokal, dengan nilai native, QC dan lineage raw. | 19 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:184` |
| seagis.parameter | Registri parameter dan satuan normalisasi. | 3 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:36` |
| seagis.plot | Identitas plot dan status survei; koordinat nullable bukan bukti lokasi lapangan. | 8 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:58` |
| seagis.plot_grid_mapping | Pemetaan operasional plot ke grid dengan waktu efektif dan waktu tercatat. | 10 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:152` |
| seagis.quality_event | Log QC append-only untuk ingestion atau satu measurement. | 11 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:273` |
| seagis.sensor | Identitas deployment sensor suhu, plot, kedalaman dan status aktif. | 10 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:73` |
| seagis.source | Registri penyedia asal dataset. | 3 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:11` |
| seagis.source_grid | Identitas sel regional dan layer kedalaman; bukan plot budidaya. | 10 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:135` |
| seagis_api.credential | Identitas aktor API berupa hash token, masa berlaku dan pencabutan. | 8 | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:27` |
| seagis_api.packet_receipt | Kunci idempotensi paket sensor dan digest semantik. | 6 | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:53` |
| seagis_api.reader_plot | Daftar plot yang boleh dibaca satu credential reader. | 2 | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:39` |
| seagis_api.request_event | Audit respons API terautentikasi dan dasar rate limit. | 6 | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:44` |
| seagis_api.temperature_policy | Konfigurasi QC engineering pilot dan batas request; bukan ambang penyakit. | 8 | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:67` |
| seagis_environment.attempt | Audit satu upaya fetch termasuk duplicate dan abandoned. | 7 | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:57` |
| seagis_environment.current_speed | View magnitude arus dari pasangan komponen dengan run/grid/waktu yang sama. | 9 | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:89` |
| seagis_environment.demo_grid_mapping | Bridge khusus dua plot fiktif ke grid nyata untuk preview, bukan otorisasi training. | 11 | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:69` |
| seagis_environment.policy | Kebijakan fetch, lisensi, cadence scheduler, staleness dan retensi regional. | 11 | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:16` |
| seagis_environment.schedule_state | State mutable lease, due time, backoff dan keberhasilan terakhir. | 9 | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:45` |
| seagis_features.feature_input | Lineage FK input feature snapshot dan guard cutoff. | 4 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:320` |
| seagis_features.feature_snapshot | Container fitur draft/sealed dengan cutoff dan hash; builder produksi belum ditemukan. | 12 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:301` |
| seagis_quality.alignment_snapshot | Dokumen QC/alignment hourly immutable; selalu training_authorized=false. | 11 | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:21` |
| seagis_quality.policy | Registri versi kebijakan QC dan hash kode builder yang immutable. | 5 | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:14` |
| seagis_quality.snapshot_input | Lineage measurement per jam alignment snapshot. | 5 | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:35` |
| seagis_raw.raw_payload | Manifest raw immutable: digest, basis hash, lisensi dan mode retensi. | 14 | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:110` |

