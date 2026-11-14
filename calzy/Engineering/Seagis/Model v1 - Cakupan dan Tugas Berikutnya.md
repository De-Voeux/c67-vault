---
type: plan
project: "[[Challenge Final]]"
updated: 2026-10-28
tags: [challenge-final, seagis, engineering, ai-ml, planning]
---

# Model v1 — Progress dan Rencana Saya

Saya sedang menyiapkan fondasi data untuk Model v1 pada [issue #2 — Refine Pipeline Model](https://github.com/De-Voeux/Seagis-Backend/issues/2). **Untuk sekarang, saya menahan pengembangan dan training model** sambil mengecek ketersediaan data IoT dan menyiapkan cara membandingkan hasil model saya dengan forecast Copernicus.

## Yang sudah saya kerjakan

Berikut pekerjaan yang sudah ada dalam pipeline dan bisa saya gunakan untuk tahap ML:

- **Fondasi database dan kontrak:** menyusun schema PostgreSQL, registri sumber/parameter, kontrak data dan penyimpanan lineage. Struktur feature snapshot dan input sudah tersedia sebagai fondasi, tetapi feature builder Model v1 belum dibuat.
- **Ingestion suhu IoT:** menyiapkan API untuk menerima paket suhu, validasi sensor dan kualitas, penanganan paket duplikat, serta akses history/status. Data suhu yang tersedia pada contoh masih berasal dari simulator.
- **Data lingkungan regional:** menyiapkan ingestion Copernicus dan Open-Meteo dengan informasi sumber, unit, grid, waktu, cadence dan versi data. Copernicus yang terkonfigurasi saat ini mencakup **salinitas, komponen arus dan nutrien**.
- **Quality dan alignment A3:** menyiapkan pemeriksaan missing, stale, unit, data terlambat dan kualitas, lalu menyelaraskan konteks per jam berdasarkan data yang tersedia pada cutoff. Sumber input tetap dapat ditelusuri.
- **Data eksperimen:** mengekspor 13 CSV per fitur dari capture contoh: suhu sintetis untuk dua plot serta data regional. Capture, alignment dan manifest disimpan untuk pemeriksaan ulang. Detailnya ada di [[CSV Forecast - Data dan Cara Pakai]].
- **Pengujian dan dokumentasi:** menyiapkan fixture serta tes untuk kontrak dan A0–A3, lalu merangkum database, alur data dan kontrak dalam [dokumentasi bilingual](https://github.com/De-Voeux/Seagis-Backend/blob/64043b11fb72724ae9860cd3245b42dbab978fe0/docs/database/README.md).

Semua ini adalah fondasi data. **Saya belum menyelesaikan feature engineering Model v1, training, evaluasi, artefak model, inference, atau output assessment untuk app.**

## Keputusan saya untuk sekarang

1. **Data IoT dulu.** Saya perlu data suhu nyata dari IoT. Kalau belum tersedia, saya akan menggunakan data dummy yang sudah ada untuk simulasi dan menguji alur terlebih dahulu; hasil simulasi tetap diberi label sintetis dan bukan bukti performa lapangan.
2. **Bandingkan dengan Copernicus.** Copernicus sudah menyediakan data model regional/forecast. Saya ingin membandingkannya dengan hasil model yang nanti saya buat, setelah variabel, lokasi/grid, unit, horizon dan waktu yang dibandingkan cocok. Ini masih rencana; model saya dan hasil perbandingannya belum ada.
3. **Feature engineering berjalan seiring development A4.** Saya akan menentukan dan membangun fitur bersama perkembangan A4, dengan menjaga kualitas, cutoff, lineage dan versi input.
4. **A5: CI di development setelah data terhubung ke frontend.** Saya akan membahas dan mengerjakan CI pada environment development setelah koneksi data ke frontend tersedia. CI untuk kontrak dan pipeline A0–A3 sudah ada; yang dimaksud di sini adalah langkah CI A5 sesuai rencana saya, bukan klaim bahwa integrasi frontend sudah selesai.

Output A3 dan ekspor saat ini masih bertanda `training_authorized=false`. Saya belum menetapkan dataset yang disetujui untuk training model nyata. Data regional tidak otomatis mewakili pengukuran di plot, dan prediksi suhu tidak sama dengan diagnosis atau probabilitas ice-ice.

**Catatan perbandingan:** konfigurasi Copernicus saat ini belum memuat suhu air. Jika target model saya adalah suhu air, saya perlu memastikan apakah ada sumber forecast Copernicus yang sesuai dan tersedia sebelum membandingkannya; saya tidak akan menyamakan salinitas/arus/nutrien dengan suhu.

## Rencana Kamis, 29 Oktober 2026

Saya akan mengerjakan dua hal berikut pada Kamis; hasilnya akan dicatat sebagai keputusan berikutnya, bukan diasumsikan sudah selesai:

- [ ] **Cek data IoT:** pastikan apakah data suhu nyata sudah tersedia dan dapat dipakai. Jika belum, siapkan simulasi dari dummy yang ada, pertahankan label sintetis, dan catat batas kualitas/cakupannya.
- [ ] **Siapkan perbandingan Copernicus:** cek data model/forecast dan pilih apa yang bisa dibandingkan dengan rencana model saya. Catat variabel, unit, grid/lokasi, cadence, horizon dan ketersediaan data; tentukan gap jika belum ada pasangan yang sebanding.

Untuk evaluasi nantinya, saya perlu memakai data yang tersedia pada setiap cutoff historis. CSV regional saat ini memilih vintage terbaru saat capture, sehingga tidak langsung dipakai sebagai backtest as-of tanpa pemeriksaan ulang.

## Setelah Kamis

- [ ] Lanjutkan **feature engineering bersama development A4** berdasarkan keputusan target, fitur dan data yang tersedia.
- [ ] Saat model dan data pembanding sudah siap, buat evaluasi kronologis yang membandingkan hasil model saya dengan baseline/forecast yang sepadan; catat metrik, kualitas input dan keterbatasannya.
- [ ] Setelah **data terhubung ke frontend**, lanjutkan **A5: CI di development** sesuai kontrak integrasi yang disepakati.
- [ ] Tutup issue #2 hanya setelah pipeline reproduktif, tes, artefak berversi, lineage dan review tim memenuhi kriteria issue.

## Referensi

- [Issue #2](https://github.com/De-Voeux/Seagis-Backend/issues/2) dan [arsitektur A3](https://github.com/De-Voeux/Seagis-Backend/blob/64043b11fb72724ae9860cd3245b42dbab978fe0/docs/a3/architecture.md).
- [Konfigurasi sumber A2](https://github.com/De-Voeux/Seagis-Backend/blob/64043b11fb72724ae9860cd3245b42dbab978fe0/config/a2_sources.json) dan [[CSV Forecast - Data dan Cara Pakai]].
- [[Rencana Track A v0.2 - Pembaruan A0 sampai A3]] — konteks pekerjaan A0–A3 dan batas integrasi lanjutan.

Basis teknis: `main` Seagis-Backend pada [commit 64043b11](https://github.com/De-Voeux/Seagis-Backend/commit/64043b11fb72724ae9860cd3245b42dbab978fe0). Kondisi runtime cloud dan ketersediaan data terbaru belum diperiksa ulang.
