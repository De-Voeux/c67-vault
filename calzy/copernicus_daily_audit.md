---
title: Copernicus Daily Data Audit
tags: [tidungmonitor, copernicus, data-audit]
updated: 2026-10-20
---

# Copernicus Daily Data Audit

**Fetch:** 12–18 Oktober 2026 (7 hari berturut-turut), diambil 20 Oktober 2026. Sumber koordinat adalah `Config/ocean_plots.json` pada proyek TidungMonitor. Lima plot (`a1`, `a2`, `b1`, `c1`, `c2`) dan satu titik referensi dipakai; semuanya ditandai `verified: false`, sehingga koordinat plot adalah contoh dan titik referensi adalah seed pencarian, bukan lokasi budidaya terverifikasi.

Fetch memakai Copernicus Marine Toolbox 2.5.0 dan dua dataset/version yang ditemukan melalui katalog live. Data subset disimpan sebagai satu NetCDF lokal per dataset di direktori sementara. **Ukuran di bawah adalah ukuran berkas NetCDF subset yang tersimpan, bukan byte transfer jaringan.** Toolbox mengembalikan satu subset 7 hari, bukan tujuh berkas harian terpisah; ukuran transfer per hari tidak tersedia dari metadata/API yang digunakan.

## Perbandingan dataset dan hasil fetch

| Collection / dataset | Variabel mentah diminta; unit | Resolusi horizontal | Kedalaman permukaan | Temporal | Dimensi subset; grid; nilai valid | Berkas subset tersimpan |
|---|---|---|---|---|---|---|
| `GLOBAL_ANALYSISFORECAST_PHY_001_024` / `cmems_mod_glo_phy-cur_anfc_0.083deg_P1D-m` (versi `202406`) | `uo`, m s⁻¹; `vo`, m s⁻¹ | 1/12° ≈ 0,08333°; sekitar 9,3 km pada lintang Tidung | 0,494025 m | P1D; judul metadata menyatakan *daily mean fields* | per variabel: `time=7 × depth=1 × lat=6 × lon=7`; 42 sel/hari; 41 nilai valid per variabel per hari (287/294 total) | 28.706 byte = 28,7 kB (28,0 KiB); satu berkas 7 hari |
| `GLOBAL_ANALYSISFORECAST_BGC_001_028` / `cmems_mod_glo_bgc-nut_anfc_0.25deg_P1D-m` (versi `202311`) | `no3`, mmol m⁻³; `po4`, mmol m⁻³ | 0,25°; sekitar 27,8 km pada lintang Tidung | 0,494025 m | P1D; judul metadata menyatakan *daily mean fields* | per variabel: `time=7 × depth=1 × lat=2 × lon=3`; 6 sel/hari; 6 nilai valid per variabel per hari (42/42 total) | 26.677 byte = 26,7 kB (26,1 KiB); satu berkas 7 hari |

Data yang diminta berhasil diparse untuk seluruh tujuh tanggal. Banyaknya sel adalah jumlah sel grid dalam subset spasial yang diunduh; valid count dihitung per variabel setelah mask nilai hilang. Resolusi kilometer adalah konversi perkiraan dari resolusi sudut katalog, bukan akurasi lokasi plot.

## Waktu dan ketersediaan

Kedua subset memberi koordinat `time` berikut (semua pada 00:00 UTC): 12, 13, 14, 15, 16, 17, dan 18 Oktober 2026. Konversi label waktu ke WIB (UTC+7) adalah 07:00 pada tanggal yang sama. Ini label koordinat untuk field rerata harian; karena batas hari tepatnya tidak dapat diperiksa dari `time_bnds`, jangan menafsirkan nilai sebagai pengukuran seketika pada 00:00 UTC atau menganggap interval WIB 00:00–24:00. `time_bnds` tidak ada pada kedua berkas.

| Dataset | Rentang `time` pada metadata katalog | Waktu publikasi/latensi |
|---|---|---|
| PHY currents | 2022-06-01 sampai 2026-10-29 | Tidak diberikan. Rentang koordinat maksimum bukan timestamp publikasi. |
| BGC nutrients | 2021-11-01 sampai 2026-10-29 | Tidak diberikan. Label versi `202311` juga bukan waktu publikasi. |

Atribut judul berkas PHY: “daily mean fields from Global Ocean Physics Analysis and Forecast updated Daily”; atribut BGC: “daily mean fields from Global Ocean Biogeochemistry Analysis and Forecast”. Jadi label produk mendukung interpretasi sebagai rerata harian, tetapi file tidak menyertakan batas waktu (`time_bnds`) atau timestamp rilis. Koordinat `time` aktual dalam data yang terambil bertanda 00Z.

## Variabel mentah dan fitur turunan

- **Dataset PHY currents** mengekspos `uo` (eastward velocity) dan `vo` (northward velocity), keduanya m s⁻¹. Standard name katalog/data masing-masing `eastward_sea_water_velocity` dan `northward_sea_water_velocity`. Tidak ada variabel skalar bernama `sea_water_velocity` di profil pipeline maupun daftar variabel mentah dataset ini. Istilah *sea water velocity* pada standard name tidak menduplikasi fitur kecepatan skalar.
- **Dataset BGC** mengekspos `fe`, `no3`, `po4`, dan `si` (semuanya mmol m⁻³) dalam layanan katalog. Request subset ini hanya meminta dan mengunduh `no3` serta `po4`; `fe` dan `si` bukan kolom dalam berkas hasil.
- **Turunan yang dihitung dari arus:** kecepatan `speed = sqrt(uo² + vo²)` dan arah aliran `atan2(uo, vo)` dalam derajat searah jarum jam dari utara, dinormalisasi ke 0–360°. Arah ini menunjukkan arah vektor aliran menuju; definisi arah harus dipertahankan konsisten.
- Inspeksi kode konfigurasi saat ini: `ocean_sources.json` memuat sumber `cop_currents` dengan `uo`/`vo` dan resolusi nominal 9.250 m, tetapi tidak memasukkan profil BGC `no3`/`po4`. Berkas `copernicus.py` mengambil dataset berdasarkan ID sumber dan meminta variabel terdaftar. Fetch BGC audit ini memakai klien Toolbox serta ID dataset/version hasil katalog; belum merupakan fitur pipeline aktif.

## Contoh nilai aktual: plot a1

Sampel a1 dipilih pada sel grid valid terdekat per dataset dalam radius 20 km. PHY memakai sel **(-5,833328°, 106,500000°)** (jarak a1 4,46 km); BGC memakai sel **(-5,750000°, 106,500000°)** (jarak a1 5,18 km). Nilai tabel adalah angka yang dikembalikan data; speed dan arah adalah hitungan turunan.

| Waktu UTC (label; WIB +7 jam) | uo (m/s) | vo (m/s) | speed (m/s) | arah (° dari utara, clockwise) | no3 (mmol/m³) | po4 (mmol/m³) |
|---|---:|---:|---:|---:|---:|---:|
| 12 Okt 00Z (07 WIB) | -0,44019 | 0,03091 | 0,44127 | 274,02 | 0,007689 | 0,115137 |
| 13 Okt 00Z (07 WIB) | -0,40953 | 0,01868 | 0,40996 | 272,61 | 0,005953 | 0,116596 |
| 14 Okt 00Z (07 WIB) | -0,44139 | 0,02053 | 0,44186 | 272,66 | 0,006468 | 0,117300 |
| 15 Okt 00Z (07 WIB) | -0,48602 | 0,02321 | 0,48658 | 272,73 | 0,006473 | 0,117776 |
| 16 Okt 00Z (07 WIB) | -0,44223 | 0,03045 | 0,44328 | 273,94 | 0,006554 | 0,118199 |
| 17 Okt 00Z (07 WIB) | -0,32879 | 0,02813 | 0,32999 | 274,89 | 0,008527 | 0,118096 |
| 18 Okt 00Z (07 WIB) | -0,49159 | 0,00009 | 0,49159 | 270,01 | 0,009114 | 0,116639 |

Untuk sampel ini, rerata rolling tiga hari terakhir (16–18 Okt) adalah `uo=-0,42087`, `vo=0,01956` m/s; rerata speed harian `0,42162` m/s; arah vektor rerata `272,66°`; `no3=0,008065` dan `po4=0,117645` mmol/m³. Rerata tujuh hari adalah `uo=-0,43425`, `vo=0,02171` m/s; rerata speed harian `0,43493` m/s; arah vektor rerata `272,86°`; `no3=0,007254` dan `po4=0,117106` mmol/m³. Arah rerata dihitung dari komponen vektor rerata, bukan rerata aritmetika sudut.

## Kesamaan sel grid enam plot

| Dataset | Sel yang dipilih untuk a1, a2, b1, c1, c2, dan titik referensi | Kesimpulan |
|---|---|---|
| PHY `uo`/`vo` | `(-5,833328°, 106,500000°)` untuk seluruh plot dan seluruh 7 hari | Ya; enam plot berbagi sel yang sama. Jarak ke plot berkisar 3,52–4,46 km. `uo` dan `vo` selalu berpasangan pada sel dan kedalaman yang sama. |
| BGC `no3`/`po4` | `(-5,750000°, 106,500000°)` untuk seluruh plot dan seluruh 7 hari | Ya; enam plot berbagi sel yang sama. Jarak ke plot berkisar 5,12–6,15 km. |

Grid BGC lebih kasar dan memilih sel berbeda dari PHY. Seluruh enam titik terwakili oleh hanya satu sel pada masing-masing produk, sehingga nilai antarplot di sini bukan observasi independen atau pembeda kondisi antarpetak.

## Fitur lingkungan yang disarankan

| Fitur ringkas | Perhitungan / rentang | Catatan agar tidak redundan |
|---|---|---|
| Arus | Simpan `uo` dan `vo` sebagai komponen utama; turunkan speed untuk tampilan. Arah dapat diturunkan untuk tampilan dari pasangan yang sama. | Jangan masukkan `uo`, `vo`, speed, dan arah sekaligus sebagai fitur bebas ke model; itu representasi ulang informasi arus. Untuk arah dalam model, gunakan pasangan sin/cos atau komponen asli. |
| Nutrien | `no3` dan `po4` harian; pertahankan unit dan metadata sumber/kedalaman. | Keduanya fitur mentah berbeda, bukan proksi langsung diagnosis ice-ice. Karena grid BGC kasar, perlakukan sebagai konteks regional. |
| Ringkasan 3 hari | Rerata trailing 3 hari untuk `uo`, `vo`, `no3`, `po4`; speed dari vektor harian. Tambahkan perubahan awal-ke-akhir atau rentang hanya bila memang perlu mendeteksi perubahan cepat. | Syaratkan minimal 2/3 hari valid dan simpan coverage count. Jangan hitung arah dari rerata aritmetika derajat. |
| Ringkasan 7 hari | Rerata trailing 7 hari untuk empat variabel mentah; simpangan baku atau rentang per variabel untuk variabilitas, dengan jumlah hari valid. | Hindari menambahkan mean, min, max, range, dan std semuanya tanpa alasan; pilih satu statistik perubahan/variabilitas untuk mengurangi duplikasi. |

Semua agregat di atas adalah kandidat ringkasan data lingkungan untuk evaluasi/inspeksi. Ambang dan hubungannya dengan kejadian ice-ice belum divalidasi oleh audit ini.

## Batas hasil

- Koordinat lima plot dan titik referensi pada konfigurasi ditandai belum terverifikasi; jarak sel mengacu ke koordinat tersebut.
- Fetch ini membuktikan subset model tersedia dan dapat diparse di sel laut terdekat, bukan bahwa nilai merupakan pengukuran in-situ atau akurat pada skala petak. Resolusi nominal PHY sekitar 9 km dan BGC sekitar 28 km.
- Product ID yang diminta adalah collection/product; ID dataset harian spesifik PHY/BGC ada pada tabel. Pipeline aktif hanya mengonfigurasi PHY currents (serta salinitas PHY lain); BGC `no3`/`po4` tidak tampak terdaftar di `ocean_sources.json`.
- Waktu publikasi/latensi dan `time_bnds` tidak tersedia; tanggal maksimum katalog tidak dipakai sebagai waktu rilis.
- Ukuran aktual transfer per hari tidak diberikan Toolbox. Angka ukuran berkas merujuk ke NetCDF subset yang disimpan, sehingga bukan klaim ukuran payload jaringan.
- Sampel adalah hasil analisis/prakiraan model. Audit tidak mendiagnosis ice-ice dan tidak memvalidasi ambang atau kemampuan prediksi penyakit.

**Sumber implementasi yang diperiksa:** `Config/ocean_plots.json`, `Config/ocean_sources.json`, `Tools/ocean/copernicus.py`, dan `Tools/ocean/audit_environmental_coverage.py` pada proyek TidungMonitor. Tidak ada kode produksi yang diubah; tidak ada test yang dijalankan.
