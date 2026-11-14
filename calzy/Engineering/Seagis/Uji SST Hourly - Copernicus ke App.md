---
type: engineering-audit
project: "[[Challenge Final]]"
created: 2026-11-10
updated: 2026-11-10
status: feasibility-tested-not-deployed
tags: [challenge-final, seagis, engineering, sst, copernicus, hourly]
---

# Uji SST hourly — Copernicus ke App

**Hasil: akses data suhu hourly Copernicus dan jalur JSON → HTTP lokal → decoding Swift berhasil. Integrasi ke aplikasi Seagis utama, ingestion database, dan scheduler produksi belum dipasang oleh uji ini.**

Pengguna meminta fallback suhu dari sumber regional serta fetch setiap jam. Koordinat sensor riil belum tersedia; pengguna memilih **Pulau Tidung Besar -5.8211, 106.5522** sebagai titik referensi sementara. Titik ini berasal dari pengguna, bukan hasil survei/geocoding yang diverifikasi. Dua titik konfigurasi lama disertakan sebagai pembanding, bukan dianggap farm riil.

## Sumber yang benar-benar diuji

| Field | Hasil aktual |
| --- | --- |
| Provider / product | Copernicus Marine / `GLOBAL_ANALYSISFORECAST_PHY_001_024` |
| Dataset / version | `cmems_mod_glo_phy_anfc_0.083deg_PT1H-m` / `202406` |
| Variabel | `thetao`, `sea_water_potential_temperature` |
| Kedalaman nominal terpilih | 0,49402499198913574 m |
| Cadence / statistik | Native `PT1H`, hourly mean |
| Grid | 1/12°, sekitar 8–9 km; bukan resolusi farm |
| Unit | Native `degrees_C` → `degC`, hanya perubahan notasi |
| Window subset | 9 November 2026 00:00 sampai 12 November 2026 23:00 UTC, inklusif |
| Metadata update provider saat audit | 10 November 2026 03:20:24.873 UTC / 10:20:24.873 WIB |
| Cakupan akhir pada katalog saat audit | 19 November 2026 23:00 UTC; bukan seluruhnya diunduh |

Pemilihan ini memenuhi kebutuhan **nilai per jam**. Produk tersebut merupakan model analisis/forecast laut regional; penggunaan istilah SST di sini mengacu pada suhu lapisan permukaan nominalnya. Ini bukan observasi SST satelit murni atau pengukuran probe di lokasi budidaya. NASA MUR tidak diunduh dalam uji ini.

Dokumentasi resmi membedakan hourly mean surface fields dan pembaruan forecast harian: [deskripsi produk](https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_PHY_001_024/description), [dataset](https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_PHY_001_024/services). Metadata aktual disimpan dalam [catalog-before.json](SST-Hourly-Audit/evidence/catalog-before.json) dan [catalog-after.json](SST-Hourly-Audit/evidence/catalog-after.json).

## Hasil spasial dan kelengkapan

| Titik permintaan | Status lokasi | Cell terpilih lat, lon | Jarak titik–pusat cell | Nilai valid |
| --- | --- | --- | --- | --- |
| **Tidung Besar -5.8211, 106.5522** | Referensi pulau dari pengguna; belum lokasi farm | -5.833328, 106.583344 | **3,704 km** | **96/96** |
| Contoh A -5.79268, 106.48012 | `synthetic` pada konfigurasi | -5.833328, 106.500000 | 5,027 km | 96/96 |
| Contoh B -5.798, 106.494 | `example_not_surveyed` | -5.833328, 106.500000 | 3,984 km | 96/96 |

Setiap timestamp berjarak tepat 3600 detik; tidak ada slot hilang/duplikat atau nilai nonfinite pada subset ini. A dan B berbagi cell dan deret suhu yang sama. Jadi hasil mewakili **dua cell unik**, bukan tiga deret suhu farm independen.

Untuk referensi Tidung Besar, rentang 96 jam adalah **30,283–31,335 °C**. Nilai jam **10 November 2026 06:00 UTC / 13:00 WIB** adalah **30,883 °C**. Ini nilai model regional, bukan bukti suhu farm atau risiko ice-ice.

Toolbox memakai `coordinates_selection_method=nearest`, tanpa pencarian diam-diam ke cell lain ketika nilai hilang. Nilai finite membuktikan data tersedia pada cell itu; uji ini belum memeriksa coastline/land mask independen, konektivitas perairan, kedalaman perairan budidaya, atau bias terhadap probe. Titik di pulau tidak otomatis menjadi titik sensor laut.

## Uji alur ingestion dan klien

Alur yang dijalankan:

```text
Copernicus aktual (login Toolbox operator)
  → validasi metadata, unit, depth, grid dan interval native
  → subset thetao per titik, 96 jam
  → pemeriksaan metadata update sebelum/sesudah fetch
  → snapshot JSON lokal, ditulis atomik
  → HTTP sementara di 127.0.0.1
  → URLSession + JSONDecoder Swift
```

- Fetch utama tiga titik berjalan 10 November sekitar **13:07–13:08 WIB**. Durasi subset tiap titik sekitar 15 detik, belum termasuk seluruh overhead katalog. Ini bukan ukuran byte transfer jaringan atau SLA provider.
- Fetch ulang window yang sama menghasilkan `content_changed=false` dan hash konten yang sama, tanpa menambah observasi duplikat. Pengambilan ulang berjarak pendek; bukan pengujian 24 jam atau bukti jadwal publikasi harian.
- Klien Swift berhasil HTTP 200 dan decode **96 sampel untuk setiap titik**, memeriksa plot, scope, unit, interval serta pemilihan nilai jam berjalan. Plot tidak dikenal mengembalikan 404.
- Snapshot JSON tiga titik sekitar **42,9 KB**; satu respons referensi Tidung sekitar **10,4 KB**, tanpa kompresi. Ini ukuran artefak/respons lokal, bukan trafik provider.
- **10 pengujian perilaku lulus**: batas 3600 detik, clock rollback, fetch identik, revisi nilai, pergantian jam, missing, stale/umur tak diketahui, plot salah, timestamp berlubang/duplikat, serta kegagalan serialisasi yang mempertahankan cache terakhir. Fixture pengujian sintetis dipisahkan dari hasil provider aktual.
- Swift 6.4.2 berhasil mengompilasi probe Foundation. **Tidak menjalankan build Xcode, simulator iOS, atau aplikasi pada perangkat.**

Bukti: [audit.json](SST-Hourly-Audit/evidence/audit.json), [repeat-check.json](SST-Hourly-Audit/evidence/repeat-check.json), [swift-probe.json](SST-Hourly-Audit/evidence/swift-probe.json), [hourly.csv](SST-Hourly-Audit/evidence/hourly.csv), [snapshot.json](SST-Hourly-Audit/evidence/snapshot.json). [README reproduksi](SST-Hourly-Audit/README.md) dan [script](SST-Hourly-Audit/audit_sst.py) disimpan bersama bukti.

## Makna “latest” dan fetch setiap jam

Ada tiga waktu berbeda:

1. **Valid time**: jam yang diwakili nilai model. Endpoint memilih slot jam UTC berjalan, bukan forecast paling jauh di masa depan. Mean per jam tidak berarti bacaan instan saat request; time bounds numeriknya belum dibuktikan dari subset ini.
2. **Update provider / issue time**: katalog menunjukkan waktu update data, tetapi tidak membuktikan issue time run forecast tertentu. `provider_updated_at` disimpan apa adanya dan `issued_at=null`.
3. **Waktu pemeriksaan**: `last_checked_at` diperbarui setelah fetch sukses. Konten identik mempertahankan `content_first_seen_at`; refresh tidak mengubah waktu update provider.

**Rancangan yang dianjurkan:** worker backend memeriksa provider setiap 3600 detik, menyimpan window hourly dan revisinya; app mengambil data backend saat dibuka/resume dan setiap jam selama aktif. Jika run provider belum berubah, nilai forecast jam berikutnya tetap bisa disajikan dari window cache. Riwayat sukses/gagal serta umur provider harus tetap terlihat. Retry/backoff, lease worker, revision history dan monitoring perlu mengikuti pola A2, bukan memanggil Toolbox dari iPhone.

Untuk background, iOS menentukan waktu pelaksanaan `BGAppRefreshTask`; `earliestBeginDate` bukan jaminan pelaksanaan tepat waktu. Maka **app tertutup tidak bisa dijanjikan fetch tepat setiap jam**. Kontinuitas ingestion harus berada di worker backend pada host yang aktif. [Dokumentasi Apple](https://developer.apple.com/documentation/backgroundtasks/choosing-background-strategies-for-your-app), [earliestBeginDate](https://developer.apple.com/documentation/backgroundtasks/bgtaskrequest/earliestbegindate).

Probe menandai usable secara temporal hanya jika slot jam berjalan ada dan umur update katalog 0–48 jam. Batas **48 jam adalah usulan engineering pilot**, bukan standar biologis atau bukti freshness vintage model. Status spasial tetap `unverified`, `farm_fallback_authorized=false`, `training_authorized=false`. Fungsi pemilihan jam/interval diuji dengan clock fixture; belum ada scheduler terpasang atau soak test lintas jam nyata.

## Gap pada backend dan aplikasi saat ini

Pemeriksaan read-only pada backend lokal commit `c496285` dengan perubahan physical-hub yang sudah ada, dan aplikasi Seagis commit `81daf0a`:

| Komponen | Yang ditemukan | Perubahan yang dibutuhkan sebelum live |
| --- | --- | --- |
| Backend `config/a2_sources.json` | Belum mendaftarkan dataset suhu hourly | Tambah profil dataset/parameter regional terpisah dari suhu sensor dan registrasi gate/retensi sesuai kontrak |
| `scripts/environmental/copernicus.py` | Validasi cadence mengharapkan daily atau 6-hourly | Tambah dukungan metadata `PT1H`, unit `degrees_C`, statistik mean dan kedalaman sesuai dataset, disertai tes |
| Pipeline A2/A3 + endpoint app | Belum diuji menerima profil suhu baru | Integrasikan persist, revisi, lineage, mapping, cutoff, QC dan proyeksi API; jangan masukkan suhu regional sebagai observation sensor |
| App `DailyRefreshPolicy` | Refresh pada batas 06:00 WIB | Tambah policy hourly untuk jalur suhu yang relevan; perlu pemicu saat aktif/resume, bukan hanya mengganti policy |
| App `RegionalContextService` | Allowlist hanya salinitas/arus/nitrat/fosfat | Perlu kontrak parameter suhu regional + DTO/domain/service/cache/UI yang mempertahankan provenance |
| App `TemperatureService` | Endpoint observasi lokal dan guard synthetic untuk demo | Jangan masukkan SST ke kontrak ini sebagai probe riil atau data simulator; pemilihan fallback membutuhkan kontrak eksplisit |

`DailyRefreshPolicy.swift` aktual dikompilasi bersama probe kecil: setelah satu jam pada hari WIB yang sama, `shouldFetch` masih **false**. Jadi permintaan fetch hourly memang belum dipenuhi app saat ini. Validator regional juga menolak parameter suhu di luar allowlist; tidak cukup hanya mengaktifkan satu dataset di server.

Endpoint `/v1/plots/<id>/sst` dalam paket ini adalah **endpoint lokal percobaan**, bukan URL API produksi yang sudah tersedia. Seluruh checkout app/backend asli dipertahankan. Tidak ada migrasi, registrasi sensor, perubahan autentikasi, deploy, commit/push, scheduler, atau training yang dilakukan.

## Keputusan dan tindak lanjut

**Layak dilanjutkan ke integrasi teknis Copernicus hourly.** Availability berhasil pada titik referensi Tidung Besar untuk window yang diuji. Kelayakan sebagai pengganti suhu sensor farm masih memerlukan koordinat probe sebenarnya, kedalaman, dan perbandingan overlap terhadap pengukuran lokal.

Urutan integrasi: profil/registry A2 + persist dan refresh hourly → proyeksi API suhu regional dengan provenance → service/refresh hourly/cache app → UI sumber fallback → verifikasi di app dan soak test backend. Setelah tersedia koordinat sensor, ulang pemetaan cell sebelum mengaktifkan fallback per farm. Fetch provider hourly tidak menjanjikan run baru setiap jam.

Terkait: [[Kontrak Fitur A4 - Forecast Suhu Air]], [[Model v1 - Cakupan dan Tugas Berikutnya]], [[Operasi A2 - Adapter dan Scheduler]], [[Indeks - Engineering]]. Indeks bersama tidak diubah karena sudah memiliki perubahan pekerjaan lain.
