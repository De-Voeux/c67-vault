---
type: project-status
created: 2026-10-29
updated: 2026-10-31
status: current-working-context
supersedes: "[[Status PoC IoT Suhu SEAGIS - 28 Oktober 2026]]"
tags: [radit, iot, lora, suhu, poc]
---

# Status PoC IoT Suhu SEAGIS — 29 Oktober 2026

Catatan status dari sesi kerja 28–29 Oktober 2026, menggantikan [[Status PoC IoT Suhu SEAGIS - 28 Oktober 2026]]. Ini status rancangan, firmware **dalam simulasi**, dan part yang mulai tiba, **bukan bukti perangkat lulus uji meja atau uji laut**. Radio LoRa antar board, DS18B20 asli, microSD asli, modem 4G, dan HTTPS ke server **belum pernah dijalankan**.

Dokumen kerja aktif ada di repo `De-Voeux/wokwiPOC`: `README.md`, `WIRING.md`, `firmware/depok_fw/`, empat diagram Wokwi, dan `tools/`. Semuanya sudah di `main` lewat PR #8 (`5e74082`).

## Pembaruan 29 Oktober siang–malam (uji meja pertama)

Klaim agent dari sesi kerja, kecuali yang ditandai pernyataan pengguna. Belum diukur dengan alat ukur.

- **Probe DS18B20 asli terbaca** di DevKit dan merespons panas/dingin (13 °C di air dingin, naik saat digenggam). Akurasinya belum dibandingkan dengan termometer lain. Probe kedua belum dites.
- **Satu DevKit rusak.** Menurut pengguna, 4×AA (±6 V) tersambung langsung ke rel breadboard yang terhubung ke pin 3V3. Hasilnya chip flash tidak terbaca dan board tidak bisa di-flash lagi. Probe yang ikut tersambung selamat.
  - **Aturan daya:** baterai hanya lewat XL6009 yang sudah disetel 5,0 V ke pin VIN. Rel breadboard hanya dari 3V3 board. Baterai dan USB tidak dipakai bersamaan.
- **Dua modul Ra-02 belum pernah menjawab** (register versi tidak terbaca) setelah header disolder sendiri, baik di DevKit maupun di XIAO. Pemindaian semua kombinasi pin hasilnya nol. Daya sampai ke header (tes buzzer) dan kabel tersambung. Dugaan: sambungan daya ke kaki modul atau chip rusak saat penyolderan. Saran: Ra-02 baru dengan header tersolder pabrik dan multimeter. **Radio antar board belum pernah jalan.**
- **Backend:** tim backend mengaktifkan `POST /v1/hub/ingest` di Supabase **development** untuk data sintetis dan menyiapkan hub serta sensor uji.
  - Firmware disesuaikan dengan kontrak resmi: `simulated=true`, chunk ≤7000 byte, penanganan 429/413/4xx.
  - Chunk keluaran firmware diterima (201 `stored`, replay terhitung duplikat) saat dikirim **dari laptop**. HTTPS dari ESP32/Air780E belum ada.
- **Board:** saran agent, hub memakai DevKit (butuh pin tambahan untuk pemutus daya modem) dan XIAO menjadi node. Tersisa 1 DevKit sehat dan 1 XIAO, jadi perlu DevKit pengganti.
- **Modul seluler terbuka lagi.** Pengguna menulis ingin modul 3G. Agent menyebut jaringan 3G operator besar di Indonesia sudah dimatikan; **klaim ini belum diverifikasi**. Keputusan 4G (Air780E) belum diubah atau dikonfirmasi ulang.
- **Usulan belanja tambahan:** DevKit pengganti, breadboard half size ×4, kabel jumper termasuk female-female, multimeter, dioda 1N5819 untuk proteksi input baterai, dan Ra-02 baru.

## Yang berubah sejak 28 Oktober

| Topik | 28 Oktober | 29 Oktober |
|---|---|---|
| Part fisik | Belum ada yang dikonfirmasi tiba | Pengguna menyatakan **2 probe suhu, resistor 4,7 kΩ, 2 modul LoRa, dan 2 ESP32** sudah tiba (28 Okt malam); XIAO ESP32-S3 sudah dimiliki. Ra-02 hanya 2 dari 3 yang dibeli (kedatangan yang ketiga belum jelas). Belanja 28 Okt (microSD, XL6009, lithium AA, dll.) belum dikonfirmasi. |
| Firmware | Draf `node/` dan `hub/` untuk DevKit, belum dikompilasi | **Firmware v2** satu basis kode untuk node A/B dan hub: jendela dengar terjadwal, ACK setelah simpan, dedup, antrean NVS, cutoff baterai, unggah harian. Dikompilasi dan dijalankan di XIAO ESP32-S3 dan ESP32 DevKit **dalam mode simulasi** (sensor, radio, microSD, modem disimulasikan). |
| Jadwal unggah | Tiap 24 jam | **Harian 06:00 WIB**; gagal → retry tiap 3 jam. Data tiba di server berumur 0–24 jam (disengaja demi baterai hub). |
| Health | Belum ada | Alat mengirim angka mentah (baterai, antrean, reboot, sinyal LoRa/4G, dll.); **server** memberi label `ok` / `warn` / `critical` / `no_news`. Ambang masih placeholder. |
| Backend | Konteks dari pull `main` | Hit read-only: `POST /v1/hub/ingest` **belum ada** (404); penerimaan data nyata masih nonaktif; data di backend sintetis. Kontrak usulan sudah ditulis untuk tim backend. **Keputusan: menunggu backend.** |
| Wokwi | Hanya ESP32+DS18B20 dan ESP32+microSD | Empat diagram (`devkit-node`, `devkit-hub`, `xiao-node`, `xiao-hub`) dengan rute kabel dicek pemeriksa otomatis; pin dipindah dari rancangan lama (lihat di bawah). |

Tidak berubah: 2 node → LoRa → 1 hub → microSD → modem → server; target 72 jam; 1 bacaan/node/jam; keputusan 4G (Air780E, SKU/antena/SIM belum dipilih); radius representatif probe belum tervalidasi; data hilang bukan 0 °C.

## Pin yang berubah (perlu diketahui sebelum merakit)

Pindahan pin ini ada di `WIRING.md` pada cabang `wokwi-firmware-v2-diagrams`; **ikuti tabel itu, bukan `WIRING.md` 27 Okt**. Papan fisik yang sudah di-flash masih memakai pin lama sampai di-flash ulang.

- **DevKit:** DIO0 Ra-02 GPIO2 → 21 (GPIO2 adalah strapping pin sekaligus LED bawaan), RST → 4, DS18B20 → 32, SD CS → 22, UART modem 16/17 → 25/26, PWRKEY → 27. SPI tetap VSPI default (keputusan pengguna).
- **XIAO ESP32-S3:** pin dikelompokkan per sisi board: sisi kiri untuk ADC, modem, kontrol LoRa; sisi kanan untuk SPI dan DS18B20 (node) atau SD CS (hub).
- Pemeriksa agent menyatakan ke-44 sambungan di empat diagram cocok dengan `config.h` kedua target; diagram hub masih punya 2–3 kabel bersilang tegak lurus (dibiarkan).

## Yang sudah dijalankan (simulasi) dan yang belum

Sudah, **hanya di simulasi pada board nyata**: boot dan peran tersimpan di NVS; jadwal slot A/B; ACK setelah simpan; antrean node; unggah ke server **simulasi** dengan potongan JSON, dedup, retry, dan label health; uji restart mandiri 40 kali tanpa macet di XIAO.

Belum terbukti: radio LoRa antar board (belum ada breadboard dan header Ra-02 belum disolder), DS18B20 asli, microSD asli, modem 4G, HTTPS+SNI ke domain backend, jam jaringan (NITZ) di Pulau Tidung, deep sleep dan drift jam nyata, arus baterai, jangkauan di lapangan, dan firmware di dalam Wokwi (baru kompilasi dan kecocokan pin).

## Perakitan akhir (saran agent, bukan keputusan)

- Meja uji: breadboard + jumper. Rakitan untuk laut: **PCB lubang yang disolder** dengan female header untuk board dan terminal blok untuk baterai/probe, karena breadboard mudah longgar dan berkarat di udara asin. PCB custom pabrik tidak diperlukan untuk PoC ini.
- Ukuran PCB lubang dari ukuran modul umum (belum diukur): node ±7×9 cm, hub ±9×15 cm. Ukuran Air780E belum diketahui, jadi ukuran hub sementara.

## Checklist pembelian

Tercentang berarti pengguna menyatakan barang sudah **tiba** (bukan sekadar checkout).

- [x] 2 probe DS18B20 waterproof 2 m (jumlah dari pengguna; panjang 2 m belum dicek cukup untuk kedalaman dan pasang-surut).
- [x] Resistor 4,7 kΩ.
- [x] 2 modul Ra-02 SX1278 433 MHz + antena. Header belum disolder. Pasang antena sebelum memancar.
- [x] 2 ESP32 DevKit (cek label modul: harus WROOM, bukan WROVER) dan 1 XIAO ESP32-S3.
- [ ] Ra-02 ke-3 (dibeli 3, tiba 2): cek apakah masih di jalan.
- [ ] Belanja 28 Okt: 3 XL6009, 4 Energizer Lithium AA, holder 4×AA, resistor 100 kΩ/47 kΩ, 2 reader + 1 kartu microSD. Kedatangan belum dikonfirmasi.
- [ ] Breadboard + kabel jumper (m-m dan f-m), PCB lubang, female header, terminal blok sekrup, multimeter.
- [ ] AA alkaline untuk 2 node; 2× elco low-ESR 1000 µF ≥16 V + keramik 100 nF.
- [ ] Modem Air780E + antena LTE + SIM/paket data; housing kedap air, cable gland probe, penambat/pelampung.

## Pekerjaan berikutnya

1. Konfirmasi kedatangan barang; pastikan jumlah Ra-02 dan WROOM vs WROVER dari label modul.
2. Breadboard + solder header Ra-02, lalu uji LoRa node ↔ hub dan DS18B20 asli; flash ulang papan dengan pin baru.
3. Ganti Ra-02 (atau ukur dengan multimeter) dan beli DevKit pengganti sebelum uji radio.
4. Putuskan SKU Air780E, antena, SIM/operator; uji band dan jam jaringan di Tidung.
5. Sepakati lebar jendela dengar hub (usulan pengguna ±20 menit/jam vs perhitungan agent 10 menit/jam) dan ukur arus tidur.
6. Menunggu backend: endpoint `/v1/hub/ingest`, kredensial hub, plot/sensor nyata, retensi payload mentah, dan kebijakan data basi yang tidak bentrok dengan unggah harian.

## Sumber dan batas bukti

- Repo `wokwiPOC` @ `5e74082` (`main`, termasuk PR #8); dicek langsung di git.
- Catatan sesi di second-brain pribadi (tidak ada di repo ini). Hasil uji, pin baru, dan ukuran PCB adalah klaim agent dari sesi tersebut; kedatangan part adalah pernyataan pengguna. Tidak satu pun diukur atau diuji pada rakitan lengkap.
- Angka daya, ESR, ambang label, dan perilaku jaringan seluler tetap estimasi/placeholder (lihat catatan 28 Okt).
