# ADR-001 — PostgreSQL dengan provenance dan forecast vintages

Status: diterapkan pada artefak A0; peninjauan tim sebelum A1. Tanggal: 21 Oktober 2026.

## Konteks

SEAGIS memerlukan pembacaan suhu sensor per plot dan konteks atmosfer/laut yang berasal dari grid model regional. Horizon awal forecasting suhu air adalah 1/3/6 jam. Dataset dapat berbeda satuan, spatial footprint, temporal support, dan waktu tersedia. Materi proposal tidak membuktikan prediksi penyakit atau ambang biologis. Repo awal belum memiliki data atau model.

## Keputusan

Gunakan satu database Supabase PostgreSQL 17. Pisahkan raw manifest, data normalized, serta curated snapshot melalui schema `seagis_raw`, `seagis`, `seagis_features`. Raw bytes nyata berada di Storage privat bila diizinkan lisensi; registry raw selalu mempertahankan hash dan metadata. A0 hanya menguji JSON sintetis inline. Belum perlu database time-series terpisah, feature store eksternal, atau microservices.

Observasi lokal dan nilai model regional memakai tabel berbeda. Dataset menautkan provider, dataset/version, cadence, licence/attribution, dan parameter registry. Composite FK memastikan dataset, sensor–plot, grid, serta flag sintetis cocok. Measurement menyimpan nilai native dan normalized dengan satuan per field.

Forecast disimpan append-only per `forecast_run` dan `forecast_value`. Capture baru yang berbeda tidak menimpa forecast lama. Waktu issue boleh tidak diketahui; initialisation, valid, receipt, dan ingest disimpan terpisah. Regional grid dibagikan oleh banyak plot melalui mapping, sehingga data coarse tidak terlihat sebagai observasi independen per plot.

Snapshot fitur menyimpan versi, cutoff, hash features, serta daftar input FK. Proses draft→sealed mencegah perubahan hasil/lineage setelah dibekukan. Guard availability adalah fondasi anti-leakage; pembuktian perhitungan fitur dan backtest tetap perlu A3–A5.

Semua tabel private dengan RLS, tanpa schema/table/function grants kepada client. A0 mengizinkan backend `service_role` tepercaya. Role/credential worker yang lebih sempit dan autentikasi perangkat diputuskan sebelum endpoint A1 berjalan. iOS nanti mengakses endpoint yang memeriksa otorisasi plot. Tidak ada credential baru yang ditanam di kode.

## Alternatif dan tradeoff

| Alternatif | Penilaian |
| --- | --- |
| Satu tabel generik untuk sensor dan seluruh forecast | Mudah memulai, tetapi rawan kehilangan run identity, time semantics, dan locality. Tidak dipilih |
| Satu kolom per seluruh variabel provider | Query sederhana, tetapi field baru mengubah schema dan unit/cadence antar sumber mudah tersamarkan |
| Relational long-form + parameter registry terbatas | Dipilih; lebih banyak join, tetapi unit, lineage, dan uniqueness dapat ditegakkan oleh database |
| JSONB untuk seluruh normalized data | Fleksibel, tetapi unit/FK/idempotensi sukar diperiksa. JSONB dipakai untuk raw sintetis, metadata, details, dan fitur saja |
| Timescale / database kedua / feature-store service | Belum ada volume, query, atau evaluasi yang menuntutnya. Indeks PostgreSQL biasa cukup untuk fondasi pilot |
| Satu refresh hourly untuk semua provider | Tidak mengikuti cadence asli dan dapat menggandakan daily context. Fetch mengikuti update provider pada A2 |

## Retensi dan reproduksibilitas

Retensi pilot di source registry masih usulan. Jangan mengaktifkan raw retention nyata sebelum terms, kebutuhan arsip forecast, attribution, dan batas redistribusi ditinjau. Deletion/purge perlu proses maintenance yang mengoordinasikan raw object, digest, dan artefak model yang bergantung padanya. A0 belum menjadwalkan deletion dan tidak membuat bucket.

Hash raw fixture memakai canonical JSON sintetis; hash object nyata harus memakai source bytes. Hash features memakai JSONB text UTF-8 pada PostgreSQL 17 dan tidak otomatis identik dengan canonical JSON aplikasi. Hash manifest input memakai algoritma eksplisit pada kamus data. Reproduksibilitas training memerlukan kode/lingkungan/feature version selain hash input; belum diklaim tercapai oleh A0.

## Migrasi dan pengujian

File awal bernama `0001_initial_schema.sql`, mengikuti deliverable Track A. Versi itu harus sama dengan riwayat saat diterapkan ke cloud. Jangan menerapkan via API yang otomatis menghasilkan versi timestamp tanpa rencana penyelarasan; perintah CLI migration standar tetap menjadi jalur deployment ketika koneksi PostgreSQL/pooler tersedia. Migrasi berikutnya harus append-only; jangan mengubah file yang telah diterapkan pada database bersama.

Pengujian A0 berjalan pada cluster PostgreSQL 17 sementara dengan role Supabase minimal yang diemulasikan. Runner menolak database remote dan schema yang sudah ada. Ini menguji migrasi dari bersih, seed repeatability, FK, RLS, dan kontrak; tidak menggantikan pengujian seluruh stack Supabase/Auth atau sensor fisik.

## Konsekuensi dan keputusan terbuka

- Query assessment akan melakukan join, tetapi setiap angka dapat ditelusuri ke sensor/grid, unit, raw, run, dan availability.
- Revisi dan raw manifest memakai lebih banyak storage; volume subset dan retensi harus diawasi saat ada data nyata.
- Model `gfs_global`, layer sekitar 0,494 m, dan sel dekat plot masih pilihan awal yang perlu diuji.
- Lisensi penuh Copernicus dan entitlement API Open-Meteo belum selesai. A0 menjaga semua ingestion nyata nonaktif.
- Fase berikutnya dimulai dengan temperature vertical slice bersumber simulator. Tidak ada keputusan A0 yang mengizinkan pelabelan hasil sebagai classifier ice-ice tervalidasi.
