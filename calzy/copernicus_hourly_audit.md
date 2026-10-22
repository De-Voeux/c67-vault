---
title: Copernicus Hourly Feasibility Test
tags: [tidungmonitor, copernicus, data-audit]
updated: 2026-10-20
---

# Copernicus Hourly Feasibility Test

**Tanggal sampel:** 18 Oktober 2026, pukul 00–23 UTC, diambil 20 Oktober 2026. Koordinat enam titik dibaca dari `Config/ocean_plots.json`; semuanya masih `verified: false`. Fetch menggunakan Copernicus Marine Toolbox 2.5.0. Masing-masing subset disimpan sebagai NetCDF di `/private/tmp`; ukuran berikut adalah ukuran file lokal hasil subset, bukan ukuran byte transfer jaringan.

## Dataset dan kelengkapan

| Data | Product / dataset ID (versi) | Variabel dan unit | Resolusi; kedalaman | Dimensi; grid; valid | Ukuran NetCDF |
|---|---|---|---|---|---:|
| Arus per jam | `GLOBAL_ANALYSISFORECAST_PHY_001_024` / `cmems_mod_glo_phy_anfc_0.083deg_PT1H-m` (`202406`) | `uo`, `vo` — m s⁻¹ | 0,08333° ≈ 9,3 km; 0,494025 m | `time=24 × depth=1 × lat=6 × lon=7`; 42 sel/timestamp. Masing-masing variabel 984/1.008 nilai valid di subset; pada sel plot: **24/24** valid untuk `uo` dan `vo`. | 34.648 byte = 34,6 kB (33,8 KiB) |
| Arus harian pembanding | `GLOBAL_ANALYSISFORECAST_PHY_001_024` / `cmems_mod_glo_phy-cur_anfc_0.083deg_P1D-m` (`202406`) | `uo`, `vo` — m s⁻¹ | 0,08333° ≈ 9,3 km; 0,494025 m | `time=1 × depth=1 × lat=6 × lon=7`; 42 sel; 41 nilai valid per variabel. Sel plot valid. | 26.365 byte = 26,4 kB (25,7 KiB) |
| Nutrien harian | `GLOBAL_ANALYSISFORECAST_BGC_001_028` / `cmems_mod_glo_bgc-nut_anfc_0.25deg_P1D-m` (`202311`) | `no3`, `po4` — mmol m⁻³ | 0,25° ≈ 27,8 km; 0,494025 m | `time=1 × depth=1 × lat=2 × lon=3`; 6 sel; 6/6 nilai valid per variabel. Satu nilai harian, **bukan** 24 nilai per jam. | 26.509 byte = 26,5 kB (25,9 KiB) |

Judul metadata hourly menyebut “hourly mean fields”; dataset pembanding harian dan nutrien juga menyebut “daily mean fields”. `time_bnds` tidak ada pada ketiga subset, jadi awal/akhir interval rerata tidak dapat dipastikan dari berkas. Koordinat data hourly aktual adalah setiap jam tepat dari `2026-10-18T00:00:00Z` sampai `2026-10-18T23:00:00Z`. WIB (UTC+7) berjalan dari **18 Okt 07:00** sampai **19 Okt 06:00**. Data harian untuk arus dan nutrien berlabel `2026-10-18T00:00:00Z` = 18 Okt 07:00 WIB; label tersebut tidak menjadikan nilai rerata harian sebuah pengamatan seketika.

## Nilai hourly aktual — sel bersama plot

Untuk `a1`, sel arus valid terdekat yang lengkap sepanjang 24 jam adalah **(-5,833328°, 106,500000°)**, berjarak 4,46 km dari koordinat a1. Kelima plot lain dan titik referensi memilih sel yang sama. Speed dihitung sebagai `sqrt(uo² + vo²)`; arah adalah `atan2(uo, vo)` dalam derajat searah jarum jam dari utara. Arah menunjukkan arah aliran menuju.

| UTC | WIB | uo (m/s) | vo (m/s) | speed (m/s) | arah (°) |
|---|---|---:|---:|---:|---:|
| 18 Okt 00Z | 18 Okt 07 | -0.409688 | 0.025067 | 0.410454 | 273.50 |
| 18 Okt 01Z | 18 Okt 08 | -0.429519 | 0.029636 | 0.430540 | 273.95 |
| 18 Okt 02Z | 18 Okt 09 | -0.459033 | 0.030707 | 0.460059 | 273.83 |
| 18 Okt 03Z | 18 Okt 10 | -0.484069 | 0.022856 | 0.484608 | 272.70 |
| 18 Okt 04Z | 18 Okt 11 | -0.506343 | 0.007501 | 0.506399 | 270.85 |
| 18 Okt 05Z | 18 Okt 12 | -0.530242 | -0.016556 | 0.530500 | 268.21 |
| 18 Okt 06Z | 18 Okt 13 | -0.537216 | -0.043570 | 0.538980 | 265.36 |
| 18 Okt 07Z | 18 Okt 14 | -0.528529 | -0.062020 | 0.532156 | 263.31 |
| 18 Okt 08Z | 18 Okt 15 | -0.524618 | -0.064364 | 0.528552 | 263.01 |
| 18 Okt 09Z | 18 Okt 16 | -0.519688 | -0.054211 | 0.522508 | 264.04 |
| 18 Okt 10Z | 18 Okt 17 | -0.507966 | -0.038202 | 0.509400 | 265.70 |
| 18 Okt 11Z | 18 Okt 18 | -0.494051 | -0.021797 | 0.494531 | 267.47 |
| 18 Okt 12Z | 18 Okt 19 | -0.483065 | -0.006931 | 0.483115 | 269.18 |
| 18 Okt 13Z | 18 Okt 20 | -0.476290 | 0.003435 | 0.476303 | 270.41 |
| 18 Okt 14Z | 18 Okt 21 | -0.476627 | 0.007121 | 0.476680 | 270.86 |
| 18 Okt 15Z | 18 Okt 22 | -0.477552 | 0.008589 | 0.477630 | 271.03 |
| 18 Okt 16Z | 18 Okt 23 | -0.478109 | 0.010478 | 0.478224 | 271.26 |
| 18 Okt 17Z | 19 Okt 00 | -0.478745 | 0.011133 | 0.478875 | 271.33 |
| 18 Okt 18Z | 19 Okt 01 | -0.480338 | 0.010024 | 0.480442 | 271.20 |
| 18 Okt 19Z | 19 Okt 02 | -0.477506 | 0.011243 | 0.477638 | 271.35 |
| 18 Okt 20Z | 19 Okt 03 | -0.472459 | 0.013876 | 0.472663 | 271.68 |
| 18 Okt 21Z | 19 Okt 04 | -0.467345 | 0.014772 | 0.467579 | 271.81 |
| 18 Okt 22Z | 19 Okt 05 | -0.463504 | 0.014554 | 0.463732 | 271.80 |
| 18 Okt 23Z | 19 Okt 06 | -0.461493 | 0.015291 | 0.461746 | 271.90 |

Sel itu memiliki seluruh 24 timestamp; **tidak ada jam hilang** untuk `uo` maupun `vo`. Di subset spasial, 41 dari 42 sel valid per variabel per jam; satu sel grid termask, bukan satu jam yang hilang.

Nutrien harian pada tanggal yang sama di sel BGC **(-5,750000°, 106,500000°)** adalah `no3=0.009114 mmol m⁻³` dan `po4=0.116639 mmol m⁻³`, dengan timestamp label 18 Okt 00Z (07 WIB). Data BGC tetap satu nilai harian—tidak digandakan atau diinterpolasi menjadi observasi hourly.

## Perbandingan terhadap rerata arus harian

Perbandingan menggunakan sel PHY yang sama (-5,833328°, 106,500000°). Rerata komponen dari 24 record hourly: `uo=-0.484333 m/s`, `vo=-0.002974 m/s`. Nilai dataset daily mean pada tanggal tersebut: `uo=-0.491590 m/s`, `vo=0.000089 m/s`.

| Ringkasan | Dari 24 hourly | Daily mean dataset |
|---|---:|---:|
| Rerata speed hourly / speed dari komponen daily | 0.485138 m/s | 0.491590 m/s |
| Arah vektor rerata / arah dari komponen daily | 269.65° | 270.01° |
| Kisaran hourly | speed 0.410–0.539 m/s; arah 263.01–273.95° | Satu nilai rerata harian |

Rerata komponen hourly berbeda dari komponen daily sebesar +0.007257 m/s pada `uo` dan -0.003062 m/s pada `vo`. Rerata speed hourly 0.006452 m/s (sekitar 1,3%) di bawah speed yang dihitung dari komponen daily; arah vektor rerata berbeda sekitar -0,36°. Speed rata-rata dan magnitude vektor rata-rata bukan operasi yang identik, sehingga keduanya diberi label terpisah.

## Grid plot dan rekomendasi

- Untuk keenam titik, sel hourly/daily currents yang dipilih sama: **(-5,833328°, 106,500000°)**. Jarak dari koordinat plot berkisar 3,52–4,46 km. Dengan demikian, enam plot tidak memperoleh enam seri arus yang independen; semuanya melihat sel regional yang sama.
- Sel BGC nutrien adalah **(-5,750000°, 106,500000°)** untuk keenam titik, berbeda karena gridnya lebih kasar (≈28 km). Nutrien hanya tersedia harian.
- Konfigurasi pipeline saat ini mendaftarkan dataset arus P1D; dataset `PT1H-m` belum terdaftar sebagai sumber aktif. Fetch ini menguji ketersediaan langsung lewat klien Copernicus Marine dengan koordinat pipeline yang sama, bukan integrasi atau ekspor pipeline.
- **Rekomendasi Seagis:** hourly currents layak menambah konteks waktu dalam hari. Pada sampel ini speed berubah 0,410–0,539 m/s dan arah sekitar 11°, variasi yang hilang pada satu rerata harian. Gunakan sebagai ringkasan perubahan subharian (mis. rentang/variabilitas speed dan perubahan komponen/arah) jika keputusan pengguna memang sensitif pada waktu dalam hari. Untuk ringkasan harian, hourly mean components dan daily mean cukup berdekatan pada satu tanggal ini.
- Nilai tambahnya bersifat **temporal regional**, bukan detail lokal antarplot: resolusi sekitar 9 km membuat keenam plot satu sel. Satu tanggal saja belum cukup untuk menetapkan nilai guna operasional; verifikasi lintas tanggal dan diskusi dengan advocate masih diperlukan. Jangan membuat data nutrien hourly dari data harian.

**Batas audit:** ukuran berkas adalah ukuran NetCDF subset lokal, bukan transfer jaringan. `time_bnds` tidak tersedia. Koordinat plot belum terverifikasi dan sampel adalah keluaran model, bukan pengukuran in-situ atau prediksi tervalidasi untuk ice-ice. Tidak ada kode produksi yang diubah dan tidak ada test kode yang dijalankan.
