# Registri sumber

Diperiksa: **21 Oktober 2026**. Ini inventaris metadata serta keputusan engineering A0. Angka lingkungan pada fixture adalah sintetis. Salinan ringkas metadata katalog publik, URL, waktu retrieval, dan SHA-256 respons asal berada di [snapshot katalog](metadata/source_catalogue_20261021.json). Metadata tersebut bukan hasil unduhan pengukuran dan bukan bukti akurasi lokal.

## Dataset yang dipilih

| Key SEAGIS | Product / dataset provider | Variabel, native unit | Resolusi / cadence native | Update provider / rencana fetch |
| --- | --- | --- | --- | --- |
| `sensor_temperature_v1` | `seagis-water-temperature`, kontrak `v1` | `water_temperature`, `degC` | Satu sensor terendam/plot; target sekitar 1 jam | Paket push A1; retry mempertahankan observed time |
| `cmems_salinity_6h` | `GLOBAL_ANALYSISFORECAST_PHY_001_024`; `cmems_mod_glo_phy-so_anfc_0.083deg_PT6H-i`, versi `202406` | `so`, `1e-3` | ~1/12°; instantaneous 6 jam | Produk fisik harian; satu fetch per pembaruan terdeteksi |
| `cmems_currents_6h` | Product fisik sama; `cmems_mod_glo_phy-cur_anfc_0.083deg_PT6H-i`, versi `202406` | `uo`, `vo`, `m s-1` | ~1/12°; instantaneous 6 jam | Mengikuti publikasi fisik, bukan polling hourly seragam |
| `cmems_nutrients_daily` | `GLOBAL_ANALYSISFORECAST_BGC_001_028`; `cmems_mod_glo_bgc-nut_anfc_0.25deg_P1D-m`, versi `202311` | `no3`, `po4`, `mmol m-3` | 0,25°; mean harian | Mengikuti pembaruan BGC harian |
| `open_meteo_gfs` | Forecast API, request model `gfs_global` | Enam field pada tabel di bawah | API hourly; cadence dan grid native dapat berbeda antarfield/horizon | Siklus model sekitar 6 jam; cek metadata availability terlebih dahulu |

Katalog [fisik/data access](https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_PHY_001_024/services) dan [nutrien/data access](https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_BGC_001_028/services) memberi dataset ID. Jenis waktu, unit, fill value, versi, dan layer teratas dicek langsung melalui STAC yang URL-nya ada dalam snapshot. [Keterangan produk fisik](https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_PHY_001_024/description) dan [BGC](https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_BGC_001_028/description) menjadi konteks update; waktu update katalog tidak dipakai sebagai `issued_at` forecast.

Layer teratas STAC fisik memiliki elevasi `-0.49402499198913574 m`; usulan depth positif ke bawah `0.49402499198913574 m`. Untuk nutrien nilainya `0.4940253794193268 m`. Sel di dekat Pulau Tidung belum dipilih dari wet mask. Jangan membulatkan lalu menganggap layer sama dengan kedalaman sensor. Katalog adalah deret yang dapat diperbarui; A2 harus menyimpan capture/vintage sendiri ketika hak akses mengizinkan. Retrieval baru tidak merekonstruksi apa yang tersedia pada cutoff lama.

## Field atmosfer

| Field Open-Meteo | Field normalisasi | Native unit yang diminta | Normalized unit | Dukungan waktu |
| --- | --- | --- | --- | --- |
| `precipitation` | `precipitation` | `mm` | `mm` | Jumlah selama satu jam sebelumnya; simpan batas interval |
| `wind_speed_10m` | `wind_speed_10m` | `m/s` | `m/s` | Instantaneous |
| `wind_direction_10m` | `wind_direction_10m` | `°` | `degree` | Instantaneous; arah meteorologis **dari** |
| `cloud_cover` | `cloud_cover` | `%` | `percent` | Instantaneous |
| `uv_index` | `uv_index` | string kosong dari API | `1` | Instantaneous; tanpa dimensi |
| `temperature_2m` | `air_temperature_2m` | `°C` | `degC` | Instantaneous; berbeda dari suhu air |

Definisi field dan unit: [dokumentasi GFS](https://open-meteo.com/en/docs/gfs-api). Parameter usulan: `models=gfs_global`, `timezone=UTC`, `wind_speed_unit=ms`, `temperature_unit=celsius`, `precipitation_unit=mm`, `cell_selection=nearest`, `elevation=nan`. Menonaktifkan koreksi elevasi adalah keputusan engineering untuk konteks laut yang akan diuji A2.

Dokumentasi GFS menyebut grid global sekitar 13 km dan grid sebagian field sekitar 0,25°; step setelah horizon tertentu dapat diinterpolasi menjadi hourly. Oleh sebab itu A0 tidak mengisi satu resolusi atmosfer yang seolah berlaku untuk semua field. Koordinat respons API disimpan sebagai `provider_returned_coordinate`, dengan grid native/perfield masih perlu diverifikasi. Jika API mengganti model atau geometri, buat versi dataset/grid baru. Banyak plot dengan sel yang sama harus memakai record grid yang sama.

## Waktu, missingness, dan autentikasi

| Sumber | Semantik issue/valid | Missing-data behavior | API / auth |
| --- | --- | --- | --- |
| Sensor | `observed_at` dari perangkat; `ingested_at` dari worker | Jam tanpa paket adalah gap; bukan pengukuran nol. Nilai null membawa status eksplisit | Endpoint berautentikasi perangkat dibangun A1; simulator tanpa kredensial production |
| Copernicus | `valid_at` mempertahankan CF time asli; publication time hanya diisi bila metadata benar-benar menyediakannya | `_FillValue`, mask daratan, NaN → null + alasan/QC. Metadata mencatat sentinel `9.969209968386869e36`; bukan angka lingkungan | Toolbox `subset/get`; akun Copernicus Marine server-side. Metadata STAC publik tidak membutuhkan akun |
| Open-Meteo | Time response adalah valid time. `generationtime_ms` adalah durasi respons, bukan issue time | `null`, field hilang, array tidak selaras, atau HTTP failure tidak boleh menjadi nol | Free API tanpa key hanya bila noncommercial sesuai terms; customer API menggunakan key server-side |

Referensi auth Copernicus: [credentials configuration](https://help.marine.copernicus.eu/en/articles/8185007-copernicus-marine-toolbox-credentials-configuration). Untuk Open-Meteo, [metadata model](https://open-meteo.com/en/docs/model-updates) membedakan inisialisasi, modifikasi, dan availability; metadata itu tidak otomatis mengikat setiap field respons seamless ke satu vintage. A2 harus menguji request model eksplisit/Single Runs dan metadata yang benar-benar kembali. Saat belum terbukti, simpan `issued_at=null`, basis `unknown`, serta digest snapshot dan receipt.

## Lisensi, retensi, dan deployment gate

| Sumber | Dasar dan batas yang diketahui | Keputusan A0 |
| --- | --- | --- |
| Sensor | Data proyek; hak penggunaan dan persetujuan lokasi/data lapangan belum dicatat | Hanya simulator; semua flag ingestion nyata mati |
| Copernicus | [Tautan lisensi resmi](https://marine.copernicus.eu/user-corner/service-commitments-and-licence), [panduan sitasi](https://help.marine.copernicus.eu/en/articles/4444611-citing-copernicus-marine-products-and-services); STAC product memakai label `proprietary` | Halaman lisensi penuh mengembalikan HTTP 403 dalam pemeriksaan ini; hak arsip/redistribusi belum dinyatakan selesai. Jangan menafsirkannya sebagai CC-BY atau larangan umum. Attribution dan DOI disimpan; raw retention nyata belum diaktifkan |
| Open-Meteo | [Terms](https://open-meteo.com/en/terms): data CC BY 4.0, akses Free API khusus noncommercial; lisensi data dan entitlement API adalah dua hal berbeda | Status bisnis/plan belum diputuskan; tidak ada subscription atau fetch data nyata di A0 |

Usulan engineering setelah lisensi dipastikan: raw object berumur 30 hari pada pilot, normalized dan vintage pilot 12 bulan, metadata/digest serta manifest input selama artefak model yang bergantung padanya masih disimpan. Angka ini **usulan retensi**, bukan persyaratan provider atau job yang sudah berjalan. Sebelum mengaktifkan raw nyata, tentukan apakah retensi tersebut kompatibel dengan kontrak sumber dan kebutuhan reproduksibilitas; turunkan/ubah kebijakan jika diperlukan. A0 tidak menjalankan purge, Cron, atau membuat bucket. Penghapusan raw yang diwajibkan hukum/kontrak memerlukan prosedur maintenance terkontrol; trigger append-only bukan izin mengabaikan kewajiban penghapusan.

**WeatherKit tidak digunakan** untuk ingestion, storage, atau training Track A. Penelitian akurasi lokal dan validasi penyakit belum dilakukan.
