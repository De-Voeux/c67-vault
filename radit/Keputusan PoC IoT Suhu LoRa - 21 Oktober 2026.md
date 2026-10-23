---
type: decision-note
created: 2026-10-21
updated: 2026-10-23
status: current-requirements
tags: [radit, iot, lora, suhu, poc]
---

# Keputusan PoC IoT Suhu LoRa — 21 Oktober 2026

> **Pembaruan 23 Oktober 2026:** baca [[Status PoC IoT Suhu SEAGIS - 23 Oktober 2026]] terlebih dahulu. Pilihan terbaru adalah Ra-02 433 MHz (SPI), 2G/GPRS diperbolehkan, dan asumsi tiap node ke hub sekitar 100 m. Radius cakupan suhu probe belum tervalidasi. Wiring UART E32/920 MHz, kewajiban 4G, dan harga lama di bawah merupakan riwayat; bukan daftar rakit/pembelian final.

Catatan ini mencatat klarifikasi terbaru Radit dan menjadi acuan kebutuhan saat menilai catatan riset awal [[Riset Arsitektur IoT LoRa - 21 Oktober 2026]]. Rancangan komponen dan anggaran belum final.

## Kebutuhan yang sudah diputuskan

- Salinitas dikeluarkan dari PoC sekarang. Dua node hanya mengukur suhu air dengan satu DS18B20 per node.
- Setiap node berisi microcontroller, DS18B20, modul LoRa, antena, dan baterai.
- Satu hub berisi microcontroller, modul LoRa, antena, baterai, microSD, serta modem seluler dengan SIM. Hub di darat lebih disukai jika kedua node terjangkau.
- Lokasi uji Pulau Tidung. Radit sudah menguji bahwa ada akses internet melalui SIM; operator, band, dan kecocokan modem tertentu belum diuji.
- Target operasi awal **3 hari terus terpasang (72 jam)** sebelum baterai diganti/diisi. Hub menerima data tiap satu jam dan mengunggah kumpulan data ke server setiap 24 jam. Untuk rancangan awal, asumsi kerja ialah satu pengukuran suhu per node per jam; bila sampling diubah, perhitungan data dan daya ikut berubah.
- Batas biaya **Rp2 juta untuk dua node dan satu hub secara keseluruhan**. Ini batas target, bukan bukti BOM sudah cukup.

Pada asumsi satu sampel per jam, dua node menghasilkan 48 rekaman per hari atau 144 rekaman selama 72 jam. Aplikasi/server baru menerima pembaruan sekitar satu kali per hari. Hub menyimpan ke microSD sebelum unggah; firmware perlu mengakui paket, menghindari duplikasi, dan mengantre data saat LoRa atau seluler terputus. Ini usulan engineering, belum implementasi.

## Dampak ke keranjang lama

Sensor konduktivitas Depoinovasi+DMS, ADS1115, serta resistor 10kΩ dan 15kΩ untuk pembagi tegangan kanal EC tidak dipakai pada rancangan baru. ESP32 yang sudah dipilih tetap kandidat untuk salah satu dari tiga microcontroller; satu DS18B20 di keranjang baru memenuhi satu dari dua node. Dibutuhkan dua pull-up 4,7kΩ, satu untuk tiap DS18B20. Kabel probe dipakai untuk menempatkan sensor di air, sedangkan radio dan antena berada di atas air.

## Gerbang verifikasi komponen sebelum dipilih final

Setiap SKU yang direkomendasikan harus cocok dengan identitas, pin, tegangan, daya, frekuensi, konektor antena, dan kondisi kerja dalam **datasheet produsen**. Spesifikasi chip mentah tidak otomatis menjadi spesifikasi board toko; bila skema/datasheet board tidak tersedia, tandai board tersebut belum tervalidasi dan ukur sebelum perakitan. Foto toko hanya membuktikan varian yang diiklankan, bukan performa 72 jam atau jangkauan di Pulau Tidung.

| Kandidat | Yang sudah didukung sumber primer | Yang belum terkunci |
|---|---|---|
| ESP32-WROOM-32 | [Datasheet Espressif](https://documentation.espressif.com/esp32-wroom-32_datasheet_en.html) menunjukkan suplai modul 3,0–3,6V, SPI, UART, GPIO, dan mode daya rendah. | Arus **DevKit CP2102 lengkap** saat aktif/tidur, regulator pada board, jumlah board yang dibeli. Angka deep sleep chip tidak boleh dipakai langsung sebagai angka board. |
| DS18B20 | [Datasheet Analog Devices](https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf) menunjukkan suplai 3,0–5,5V, 1-Wire, dan pull-up 4,7kΩ. | Mutu seal probe Shopee untuk air laut dan hasil uji 72 jam. |
| HopeRF RFM95W 868/915 | [Datasheet HopeRF](https://www.hoperf.com/uploads/RFM95W-V2.0_1695351437.pdf) menyebut modul 868/915MHz, suplai 2,4–3,7V, dan antarmuka SPI. | SKU/versi RF persis dari toko, kemampuan praktis di 920–923MHz, antena dan konektor yang sesuai, jangkauan nyata. Butuh **tiga** transceiver dengan pengaturan radio sama. |
| SIMCom A7670C 4G Cat-1 | [Dokumen seri A7670 dari SIMCom](https://www.simcom.com/product/A7670X.html) tersedia untuk menguji band, suplai, antarmuka, dan arus modem. | SKU board/modul final, skema catu dan level UART board tersebut, operator/band di lokasi, dan uji unggah nyata. Harga toko belum membuktikan kecocokan. |

Regulasi LPWAN Indonesia dan batas EIRP/duty cycle perlu dicocokkan saat band radio dan daya pancar dipilih: [Permen Komdigi 2/2025](https://www.postel.go.id/downloads/40/20250208094700-permen_2025-02_perubahan_PM_Izin_Kelas_BN.pdf). Uji jangkauan dilakukan dengan casing/antena aktual, hub di darat pada posisi terbuka, dua node pada lokasi pemasangan, lalu catat penerimaan paket dan RSSI/SNR selama pasang-surut. Angka jarak belum bisa dijanjikan dari datasheet saja.

## Penentu belanja berikutnya

Hitung baterai dari **arus perangkat lengkap yang diukur** pada mode tidur, terima LoRa, kirim LoRa, dan unggah seluler selama siklus 72 jam. Hub berpotensi membutuhkan baterai lebih besar karena harus siap menerima tiap jam. Finalisasi modem, modul LoRa, antena, baterai, regulator, charger/proteksi, microSD, housing, konektor, kabel, dan alat rakit setelah masing-masing SKU dan datasheet/skema board diperiksa. Buat RAB lengkap termasuk ongkir dan cadangan sebelum menyatakan batas Rp2 juta tercapai.
