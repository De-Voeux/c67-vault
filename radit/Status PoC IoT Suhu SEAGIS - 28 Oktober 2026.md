---
type: project-status
created: 2026-10-28
updated: 2026-10-28
status: current-working-context
supersedes: "[[Status PoC IoT Suhu SEAGIS - 23 Oktober 2026]]"
tags: [radit, iot, lora, suhu, poc]
---

# Status PoC IoT Suhu SEAGIS — 28 Oktober 2026

Catatan keputusan percakapan 27–28 Oktober 2026, menggantikan [[Status PoC IoT Suhu SEAGIS - 23 Oktober 2026]]. Ini status rancangan, pembelian, dan draf firmware, **bukan bukti perangkat telah lulus uji meja atau uji laut**. Firmware `node/` dan `hub/` belum pernah dikompilasi ke papan fisik.

Dokumen kerja aktif sekarang ada di repo `De-Voeux/wokwiPOC` (commit `7a3977d`, 28 Okt 00:47): `README.md`, `WIRING.md`, `node/`, `hub/`. Berkas lokal: `/Users/radityaaydin/repos/depok/wokwiPOC/`. `sealiit-poc-v3/` dan `sketch.ino` di root `wokwiPOC` adalah simulasi lama satu alat/5 jam.

## Yang berubah sejak 23 Oktober

| Topik | 23 Oktober | 28 Oktober |
|---|---|---|
| Seluler | 2G/GPRS boleh; kandidat SIM800L | **Pengguna memutuskan 4G** (27 Okt). Arah modem **Air780E** (Cat-1). SIM800L/2G tidak dipakai lagi. SKU board, antena LTE, dan SIM/operator **belum dipilih/dibeli**. |
| Daya | Node AA alkaline; baterai/regulator hub belum dipilih | Node: 4×AA alkaline. Hub: 4×**Energizer Ultimate Lithium AA**. Ketiga alat lewat buck-boost **XL6009** disetel 5,0 V. MT3608 ditolak karena hanya step-up. |
| Firmware | Belum ada firmware dua node–hub; pin belum dibuat | Draf `node/` dan `hub/` + pinout `WIRING.md` ada. Wokwi hanya menyimulasikan ESP32+DS18B20 (node) dan ESP32+microSD (hub); LoRa dan modem hanya digambar. |
| Radio | Ra-02 dipilih untuk checkout | **3 set Ra-02 SX1278 + antena 433 MHz sudah checkout** (24 Okt, Rp126.000/set, listing berbeda dari kandidat 23 Okt). Kedatangan belum dikonfirmasi. |
| Anggaran | Sementara Rp488.030 | Sementara **±Rp840.930**, sisa ±Rp1.159.070 dari cap Rp2.000.000. Harga listing, sebelum ongkir/voucher; bukan RAB final. |

Tidak berubah: 2 node → LoRa → 1 hub → microSD → modem → server; target 72 jam, 1 bacaan/node/jam, unggah tiap 24 jam (144 slot); asumsi jarak ±100 m tiap node ke hub; radius representatif probe belum tervalidasi; QoS (ACK setelah tulis SD, identitas paket tetap saat retry, data hilang bukan 0 °C).

## Rancangan daya (estimasi, belum diukur)

- Hub mendengar LoRa **terjadwal**, bukan terus-menerus: mendengar terus memakan ±97% energi hub, unggah modem ±3%.
- Modem dimatikan penuh di luar jadwal unggah.
- Firmware wajib punya **software cutoff** baterai lewat pembagi 100 kΩ/47 kΩ ke GPIO34 di ketiga alat.
- Estimasi hub ±11–15 Wh untuk 72 jam vs ±18 Wh dari 4 sel lithium: **margin tipis**. Ketidakpastian terbesar adalah arus deep sleep DevKit (±5–15 mA); wajib diukur.
- Lebar jendela dengar hub **belum disepakati**: usulan pengguna ±20 menit/jam vs perhitungan agent 10 menit/jam.
- Buffer lonjakan modem: 2× elco low-ESR 1000 µF ≥16 V + 100 nF di pin daya modem. Supercap koin 1F ditolak karena ESR ±30 Ω.

## Temuan crosscheck yang belum diperbaiki di firmware

- `LORA_FREQUENCY_HZ = 433000000` di node dan hub berada di bawah awal pita LPWAN 433,05–434,79 MHz ([Permen Komdigi 2/2025](https://www.postel.go.id/downloads/40/20250208094700-permen_2025-02_perubahan_PM_Izin_Kelas_BN.pdf)). Usulan: tengah pita (mis. 433,5 MHz), kanal ≤125 kHz.
- TX power 14 dBm ditambah gain antena berisiko melewati EIRP 12,15 dBm. Turunkan setelah gain antena diketahui.
- Node belum deep sleep; antrean retry masih di RAM, perlu dipindah ke NVS.
- Hub belum punya jendela dengar terjadwal yang menunggu kedua node; `modemHttpPostBatch()` masih kosong sampai manual AT Air780E dibaca.
- Node membaca ADC baterai mentah; konversi rasio 100k/47k dan cutoff belum ada. Komentar `node/sketch.ino` masih menyebut pembagi "belum didesain".
- Pin DS18B20: firmware **GPIO4**, catatan lama **GPIO27**. Belum direkonsiliasi.
- GPIO16/17 dipakai UART modem; papan harus **WROOM**, bukan WROVER (PSRAM). Cek fisik saat barang datang.
- Ra-02 dan microSD berbagi bus SPI (CS GPIO5 vs GPIO13). Perlu uji meja tulis SD lalu kirim/terima LoRa bergantian.

## Checklist pembelian

Tercentang berarti checkout selesai menurut pengguna; kedatangan barang belum dikonfirmasi.

- [x] 3 ESP32 DevKit 30 pin (1 dari @adityadaniel, 2 checkout).
- [x] 10 resistor 4,7 kΩ; 2 probe DS18B20 2 m.
- [x] 3 set Ra-02 SX1278 433 MHz + antena IPEX (24 Okt).
- [x] 3 holder 4×AA + tutup + saklar (2 node 24 Okt, 1 hub 28 Okt). Tidak tahan air.
- [x] 4 Energizer Ultimate Lithium AA untuk hub (28 Okt).
- [x] 3 XL6009 auto buck-boost (28 Okt). Setel 5,0 V dengan multimeter **sebelum** disambung.
- [x] Resistor 100 kΩ ×10 + 47 kΩ ×10 (28 Okt).
- [x] 2 reader microSD 3,3 V + 1 kartu microSD 2 GB (28 Okt).
- [ ] AA alkaline untuk 2 node.
- [ ] 2× elco low-ESR 1000 µF ≥16 V + 1 keramik 100 nF.
- [ ] Modem 4G Air780E + antena LTE 700–2700 MHz + SIM/paket data. Cek konektor (IPEX/SMA) dan input 5 V.
- [ ] Housing kedap air (kemungkinan 3D print, bukan logam), cable gland probe, penambat/pelampung.

## Pekerjaan berikutnya

1. Putuskan SKU Air780E, antena, dan SIM/operator; uji band di Tidung. Ponsel menangkap 5G di lokasi, tetapi band Air780E vs operator belum diuji.
2. Sepakati jendela dengar hub dan jadwal slot node A/B.
3. Perbaiki firmware sesuai daftar crosscheck di atas, lalu kompilasi ke papan fisik.
4. Ukur arus deep sleep dan konsumsi rakitan lengkap sebelum memakai angka daya sebagai dasar.
5. Uji meja QoS: paket/ACK hilang, reboot, SD gagal, jaringan putus.

## Sumber

- Repo `wokwiPOC` @ `7a3977d`: `README.md` (kebutuhan, QoS, rancangan daya, checklist, crosscheck 28 Okt), `WIRING.md`, `node/sketch.ino`, `hub/sketch.ino`.
- second-brain: `sources/SEAGIS PoC IoT suhu/Sesi keputusan IoT - 27-28 Oktober 2026.md` (keputusan pengguna vs klaim agent) dan `projects/SEAGIS PoC IoT suhu/Konteks kerja dan keputusan terkini.md`.
- Angka daya, ESR, dan perilaku jaringan seluler adalah estimasi/klaim agent, bukan hasil ukur. Harga dari listing dan tempelan pengguna, bukan bukti pembayaran.
