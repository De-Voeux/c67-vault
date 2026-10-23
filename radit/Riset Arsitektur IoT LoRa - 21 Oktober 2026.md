---
type: research-note
created: 2026-10-21
updated: 2026-10-21
status: provisional-architecture
tags: [radit, iot, lora, suhu, poc]
---

# Riset Arsitektur IoT LoRa — 21 Oktober 2026

Catatan keputusan terbaru dari percakapan Radit dan pemeriksaan sumber primer. Ini rancangan sementara, belum daftar belanja final, jaminan jangkauan, atau hasil uji alat. Riwayat sebelumnya ada di [[Transfer Knowledge - IoT Rumput Laut - 15 Oktober 2026]].

## Keputusan Radit

- Salinitas dikeluarkan dari PoC.
- Dua node, masing-masing microcontroller, satu DS18B20, LoRa beserta antena, dan baterai.
- Satu hub: microcontroller, LoRa beserta antena, baterai, microSD, modem seluler, dan SIM untuk mengirim ke server.
- Hub sebaiknya di darat jika jangkauan memungkinkan; lokasi aktual belum ditetapkan.
- Dipasang 24 jam; data diterima hub per satu jam; data dikirim ke server per 24 jam.
- Ada akses internet lewat SIM, tetapi operator, teknologi jaringan, dan band belum dikonfirmasi.
- Batas total dua node dan satu hub Rp2 juta. Kecukupan anggaran belum terbukti oleh BOM lengkap.

Yang belum dipastikan: apakah 24 jam berarti satu sesi lalu diambil/diisi ulang atau operasi terus-menerus berhari-hari; interval baca suhu sebelum pengiriman per jam; jarak node ke pantai; lokasi dan operator. Jangan menganggap kata GPRS sebagai konfirmasi jaringan2G.

## Dampak ke keranjang dan arti data

Sensor EC Depoinovasi+DMS, ADS1115, dan pembagi tegangan10k/15k untuk kanal EC tidak diperlukan dalam versi ini. Tetap gunakan dua DS18B20 dan dua resistor pull-up4,7kΩ, satu set per node. DS18B20 membaca suhu secara digital; rangkaian pull-up tercantum di [datasheet Analog Devices, halaman7](https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf). Kualitas selubung probe Shopee untuk perendaman laut tetap harus diuji.

Dua lokasi suhu memberikan pengamatan suhu pada dua titik. Data tersebut tidak mengukur salinitas dan belum membuktikan model forecast/ice-ice. Jangan meneruskan asumsi masukan salinitas ke model tanpa perubahan eksplisit.

## Usulan alur engineering

`Node1 dan Node2 → LoRa privat → hub darat → microSD → modem seluler → server`

Gunakan LoRa privat dengan dua node mengirim ke satu hub sebagai kandidat paling sederhana. Ini belum keputusan memakai jaringan LoRaWAN; hub transceiver biasa tidak otomatis menjadi gateway LoRaWAN penuh.

- Jika satu bacaan dikirim per jam, targetnya24 bacaan per node per24jam atau48 bacaan gabungan. Jika sampling lebih sering, jumlahnya berbeda.
- Node mengirim pada slot berbeda dan menunggu ACK. Hub baru memberi ACK setelah record tersimpan. Node menyimpan record belum diakui dalam flash internal dengan batas kapasitas yang jelas, kemudian mencoba ulang. Ini usulan firmware, belum implementasi.
- Setiap record memiliki node_id, nomor urut, waktu ukur, suhu, dan status kualitas. Hub menyimpan waktu terima secara terpisah; server menerima ID unik agar retry tidak menggandakan data.
- microSD menampung backlog bila koneksi seluler gagal. Pengiriman harian berarti server/app mendapat pembaruan harian, bukan peringatan langsung setiap jam. Data lokal tidak dihapus hanya karena permintaan upload sudah dikirim; tunggu pengakuan server.
- Jam pengukuran harus tetap terlacak setelah sleep/reboot. Sinkronisasi waktu dan kebutuhan RTC hub perlu dipilih pada rancangan detail.

ESP32 mendukung timer wakeup dari deep sleep; tetapi arus board lengkap dan modem tetap harus diukur. [Dokumentasi sleep Espressif](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/sleep_modes.html). Flash internal dapat menyimpan nilai kecil secara nonvolatile melalui NVS; kapasitas antrean, wear, dan pemulihan setelah listrik putus perlu dirancang. [Dokumentasi NVS Espressif](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/storage/nvs_flash.html).

## LoRa: frekuensi dan cakupan

Sumber resmi yang ditemukan adalah [Permen Komdigi2/2025, lampiranII, halamanPDF12](https://www.postel.go.id/downloads/40/20250208094700-permen_2025-02_perubahan_PM_Izin_Kelas_BN.pdf):

| Pita LPWAN | Batas yang relevan |
|---|---|
|433,05–434,79MHz|EIRP maksimum12,15dBm; bandwidth maksimum125kHz; duty cycle tidak diatur pada tabel ini|
|920–923MHz|End node maksimum20dBm EIRP; gateway26dBm EIRP; bandwidth maksimum250kHz; uplink/downlink duty cycle1%|

Jadi433MHz tidak otomatis terlarang. Modul433MHz dapat dievaluasi sebagai opsi biaya, tetapi jangan memakai daya maksimum bawaan20dBm bila melampaui batas EIRP. EIRP memperhitungkan antena dan rugi kabel. Ketentuan standar/perangkat lain tetap perlu diperiksa pada produk final.

SX1278 hanya mencakup137–525MHz, sehingga tidak dapat disetel ke920–923MHz. SX1276 mencakup137–1020MHz pada level chip, tetapi versi modul, rangkaian RF, dan antena harus mendukung band yang dipilih. Ketiga radio harus kompatibel dan dikonfigurasi sama. [Tabel resmi Semtech](https://www.semtech.com/products/wireless-rf/lora-connect).

Tidak ada radius pasti yang dapat dijanjikan hanya dari nama LoRa. Daya legal, antena, sensitivitas, dan kondisi propagasi menentukan sambungan; [penjelasan teknis Semtech](https://blog.semtech.com/long-range-with-lora). Penelitian primer *Experimental Study of LoRa Transmission over Seawater* menunjukkan skenario dekat permukaan laut dapat mengubah karakteristik antena dan menurunkan penerimaan paket; hasil jarak eksperimen lain tidak menjadi jaminan lokasi ini. [Artikel penelitian2018](https://www.mdpi.com/1424-8220/18/9/2853) — bagian relevan ditemukan melalui indeks pencarian; halaman penuh PMC terhalang pemeriksaan browser pada sesi ini.

Usulan pengujian: hub di darat pada posisi cukup tinggi dan terbuka; probe terendam sedangkan elektronik/antena tetap di atas air. Uji bertahap100,300,500meter jika lokasi memungkinkan, memakai posisi dan housing yang benar-benar akan dipasang. Angka ini jarak uji usulan, bukan cakupan terjamin. Catat keberhasilan paket, retry, RSSI/SNR, tinggi antena, pasang surut, dan orientasi node; uji kedua node bersamaan selama24jam. Hub darat dipilih setelah kedua sambungan memenuhi target penerimaan yang ditentukan tim.

## Modem dan daya

Internet pada ponsel belum membuktikan kompatibilitas modem tertentu. Cocokkan operator dan band lokasi dengan varian modem; kandidat4G Cat1 layak diperiksa, tetapi model dan breakout belum dipilih.

Sebagai contoh persyaratan, [SIMCom A7672X/A7670X Hardware DesignV1.03](https://files.waveshare.com/wiki/A7670E-Cat-1-GNSS-HAT/A7672X_A7670X_Series_Hardware_Design_V1.03.pdf), halamanPDF26–28, menyebut lonjakan hingga2A pada transmisiGSM dan kebutuhan catu yang memadai; halamanPDF19/33 mencantumkan UART1,8V pada modul mentah. Breakout dapat menambahkan regulator dan konversi level, jadi jangan menyamakan spesifikasi chip dengan pin board yang dijual atau memberi daya modem dari pin3V3ESP32.

Usulan hemat daya: node tidur di antara jadwal ukur/kirim; modem hub dinyalakan pada jadwal unggah dan retry terbatas. Hub perlu tetap bisa menerima slot node, baik dengan radio aktif terus maupun penjadwalan yang teruji. Hitung baterai dari arus terukur seluruh sistem, lama aktif, efisiensi regulator, dan cadangan; belum ada bukti kapasitas tertentu cukup24jam. Harga komponen, alat rakit, casing, konektor, baterai, charger/proteksi, dan ongkir harus masuk pemeriksaan anggaran; paket data merupakan biaya berulang.

## Batas hasil

Belum ada firmware baru, wiring final, simulasi radio, pembuktian baterai24jam, atau hasil uji lapangan. Catatan lama tidak dihapus; keputusan salinitas/5jam/BLE di sana merupakan riwayat yang diganti oleh keputusan percakapan21 Oktober di catatan ini.
