---
type: project-status
created: 2026-11-04
updated: 2026-11-04
status: current-working-context
supersedes: "[[Status PoC IoT Suhu SEAGIS - 29 Oktober 2026]]"
tags: [radit, iot, lora, suhu, poc]
---

# Status PoC IoT Suhu SEAGIS — 4 November 2026

Catatan status dari sesi kerja 3–4 November 2026, menggantikan [[Status PoC IoT Suhu SEAGIS - 29 Oktober 2026]]. Ini status **uji meja sebagian, bukan bukti perangkat lulus uji meja penuh atau uji laut**. Radio antar board belum pernah jalan, dan firmware belum ditulis ulang untuk part baru.

Isi catatan ini adalah klaim agent dari sesi kerja, kecuali yang ditandai keputusan, pernyataan, atau hasil ukur pengguna.

## Yang berubah

- **Radio (keputusan pengguna):** Ra-02 diganti **E32-433T20D** untuk ketiga alat, karena modul Ra-02 yang dirakit sendiri tidak pernah menjawab. E32 tidak bisa berbicara dengan Ra-02. Rencana kanal 434 MHz dan daya 10 dBm.
- **Seluler (keputusan pengguna):** 4G Air780E diganti **SIM800L V2 5V (2G)** untuk hub karena harga. 3G sudah dimatikan, sedangkan 2G masih aktif per sumber berita Oktober 2026, tanpa jaminan jangka panjang.
- **HTTPS:** pengguna menolak server perantara. Rencananya TLS 1.2 dikerjakan ESP32 lewat koneksi TCP modem. **Belum diuji.**
- **Pembelian:** menurut pengguna sudah checkout. E32 belum sampai per 4 November.
- **Koordinat (keputusan pengguna):** tanpa modul baru, cukup satu koordinat dari hub yang diisi manual. Jalur sampai ke server belum diputuskan.

## Hasil uji meja 4 November

Rakitan sementara di tiga breadboard half size, gabungan bagian node dan hub.

| Bagian | Hasil | Asal bukti |
|---|---|---|
| Baterai ke XL6009 ke VIN | VIN 4,8 V, 3V3 3,32 V | ukur pengguna |
| Rel breadboard | 3,32 V | ukur pengguna |
| Pembagi baterai 100k/47k | 1,67 V saat masukan sekitar 5,1 V | ukur pengguna |
| Probe DS18B20 | terbaca 23,88–24,94 °C | keluaran serial |
| microSD 3,3 V | tulis dan baca lolos | keluaran serial |

- Uji fungsi memakai **program tes lewat USB, bukan firmware v2**.
- Menurut pengguna probe dicelup ke air suhu ruang. Uji di air yang jelas beda suhunya dan perbandingan dengan termometer lain belum dilakukan.
- **ESP belum terbukti menjalankan program dari baterai,** dan pembacaan baterai oleh firmware belum diuji.
- Tegangan XL6009 dan rel diukur tanpa beban E32 maupun modem.
- Sempat terjadi salah pasang resistor sehingga pin ADC terbaca 3,92 V, di board yang sudah rusak. Sudah dibetulkan.

## Pekerjaan berikutnya

1. Tunggu E32, lalu tulis ulang driver radio dari SPI ke UART dan uji kirim antar board.
2. Rakit SIM800L dan uji sinyal, jam jaringan, serta TLS di ESP32. Modem butuh elco 1000 µF ×2 + 100 nF, dan 5 V langsung dari XL6009.
3. Cek sinyal 2G di Tidung dengan HP mode 2G dan SIM yang akan dipakai.
4. Perbarui pin firmware, diagram Wokwi, dan `WIRING.md` untuk part baru.
5. Uji ESP dari baterai, ukur arus, dan solder sambungan sebelum masuk housing.
6. Verifikasi batas EIRP 433 MHz ke regulasi: 10 dBm + antena 3 dBi sekitar 13 dBm, sedangkan angka 12,15 dBm di README belum diverifikasi.
7. Tentukan jalur koordinat bersama backend, dan tunggu endpoint serta sensor nyata dari backend.

## Sumber dan batas bukti

- Catatan sesi di second-brain pribadi (tidak ada di repo ini). Hasil ukur berasal dari pengguna dan tidak diulang dengan alat lain.
- Spesifikasi E32 dan status jaringan berasal dari sumber web yang dibaca agent, perlu dicek ulang saat keputusan final.
- Firmware dan diagram di repo `De-Voeux/wokwiPOC` **masih untuk Ra-02 dan Air780E**.
