---
type: knowledge-transfer
created: 2026-10-21
updated: 2026-10-23
status: working-understanding
tags: [radit, iot, lora, suhu, poc, shopee]
---

# Transfer Knowledge — PoC IoT suhu LoRa

> **Pembaruan 23 Oktober 2026:** baca [[Status PoC IoT Suhu SEAGIS - 23 Oktober 2026]] terlebih dahulu. Pilihan terbaru adalah Ra-02 433 MHz (SPI), 2G/GPRS diperbolehkan, dan asumsi tiap node ke hub sekitar 100 m. Radius cakupan suhu probe belum tervalidasi. Wiring UART E32/920 MHz, kewajiban 4G, dan harga lama di bawah merupakan riwayat; bukan daftar rakit/pembelian final.

Catatan handoff sesi 21–22 Oktober 2026. Baca bersama [[Keputusan PoC IoT Suhu LoRa - 21 Oktober 2026]], [[Riset Arsitektur IoT LoRa - 21 Oktober 2026]], dan [[Rancangan Alat PoC Suhu LoRa - 21 Oktober 2026]]. Rancangan ini belum menjadi spesifikasi elektronik final dan belum diuji dengan perangkat fisik. Keputusan baterai AA tanggal 22 Oktober di bawah menggantikan usulan Li-ion untuk node yang sempat muncul pada sesi sebelumnya.

## Keputusan pengguna

- **Dua node di air**, masing-masing memakai satu probe suhu DS18B20, microcontroller, radio LoRa, antena, dan baterai. Salinitas/konduktivitas **dikeluarkan dari PoC ini**.
- **Satu hub** menerima LoRa, menyimpan data ke microSD, lalu mengirimkannya ke server melalui modem seluler dan SIM. Hub di darat lebih disukai bila kedua node terjangkau.
- Lokasi uji **Pulau Tidung**. Radit sudah menguji adanya internet seluler di lokasi; operator, pita LTE yang dipakai, dan modem kandidat belum dicocokkan.
- Perangkat terus terpasang selama **72 jam**. Asumsi kerja: tiap node mengukur dan mengirim **satu data per jam**; hub mengunggah kumpulan data **setiap 24 jam**. Ini memberi 48 data per hari atau 144 data dari dua node selama 72 jam.
- **Dua node memakai baterai AA alkaline yang diganti manual**, agar pengguna tidak perlu mengisi ulang sel 18650. Jumlah AA dan regulator final belum diputuskan; empat AA seri per node adalah kandidat awal untuk diuji, bukan daftar belanja final.
- **Hub juga wajib memakai baterai**, tetapi jenis, jumlah, dan kapasitasnya belum dipilih. Jangan menganggap pengguna menyetujui power bank ataupun AA untuk hub.
- Batas target **Rp2 juta untuk elektronik dua node dan satu hub** belum dibuktikan. **Casing/housing adalah hal yang sama; anggarannya dipisahkan dan pembeliannya ditunda**, tetapi tetap wajib tersedia dan diuji sebelum pemasangan di laut.
- Pengguna meminta agar komponen yang dicari dicocokkan dengan **datasheet produsen**. Kecocokan chip belum otomatis membuktikan kecocokan breakout board dari toko.

Alur rancangan: `2 node suhu → LoRa privat → hub → microSD → 4G Cat-1/SIM → server`. Ini bukan gateway LoRaWAN. BLE dan pola ambil alat setelah lima jam dalam catatan 20 Oktober adalah **riwayat rancangan lama**. Wokwi saat ini juga mewakili rancangan lama dan belum membuktikan jangkauan, daya, atau ketahanan laut.

## Arti pengukuran dan data

DS18B20 membaca **suhu air di titik dan kedalaman probe**, bukan salinitas, arus, diagnosis ice-ice, ataupun forecast yang sudah tervalidasi. Hub sebaiknya menyimpan `node_id`, nomor urut, suhu °C, waktu terima, status kualitas, dan status pengiriman. Node mengirim pada slot berbeda; ACK diberikan setelah record tersimpan. Unggah ulang harus aman dari duplikasi, dan data lokal baru dihapus setelah server mengakui penerimaan. Ini **usulan firmware**, belum diimplementasikan.

ESP32 DevKit tidak memiliki slot microSD bawaan. Hub membutuhkan pembaca microSD terpisah. Untuk versi hemat, waktu kalender dapat diperoleh dari jaringan seluler saat hub menyala; jika hub reboot saat jaringan tidak tersedia, timestamp perlu ditandai belum sinkron. RTC tambahan belum masuk RAB.

## Koreksi daftar belanja Shopee

**Daftar tautan dan total Rp1.900.829 yang pernah diberikan tidak layak dipakai untuk belanja.** Plugin Shopee hanya mengembalikan ID dan ringkasan hasil pencarian. Codex menyusun sendiri URL `shopee.co.id/product/<shopid>/<itemid>` tanpa memverifikasi halaman produknya. Radit melaporkan produk pada tautan itu tidak ada; pada pencarian ulang, ID TP4056 dan MT3608 yang sebelumnya dicantumkan juga tidak muncul. Kesalahan ini ada pada rekomendasi tautan, bukan bukti bahwa jenis komponen TP4056 atau MT3608 tidak ada di pasaran. Jangan menganggap harga hasil pencarian sebagai harga varian yang benar.

Daftar **kebutuhan fungsional**, tanpa mengklaim SKU atau penjual tertentu:

| Bagian | Kebutuhan sementara | Yang harus dipastikan sebelum membeli |
|---|---|---|
| Dua node | 2 microcontroller, 2 DS18B20, 2 resistor pull-up 4,7 kΩ, 2 radio LoRa yang sama, 2 antena yang cocok | Pin/tegangan, varian frekuensi 920–923 MHz, konektor antena, dan kualitas probe untuk air asin |
| Daya dua node | Dua paket AA alkaline, holder **AA**, saklar, regulator yang sesuai, dan sel pengganti | Jumlah sel, rentang tegangan paket, efisiensi/arus diam regulator, arus puncak, konsumsi saat tidur, dan daya tahan 72 jam |
| Hub | 1 microcontroller, 1 radio LoRa kompatibel, 1 antena LoRa, 1 pembaca microSD dan kartu, 1 modem 4G Cat-1 dengan SIM dan antena LTE yang cocok | Skema board modem, tegangan dan level UART, pita operator, kebutuhan arus puncak, serta integritas pencatatan data |
| Daya hub | Paket baterai yang dipilih khusus untuk hub; **kimia dan jumlah sel masih terbuka** | Energi yang cukup untuk penerimaan LoRa dan modem 4G, catu tahan lonjakan arus, serta uji 72 jam |
| Perakitan | Kabel, PCB prototipe, konektor, komponen pasif, multimeter, dan solder bila belum tersedia | Jumlah dan biaya setelah skema listrik dipilih |

**Koreksi daya node:** holder 3-slot 18650 dan BMS 1S di keranjang tidak sesuai dengan keputusan AA. Node AA tidak memerlukan TP4056, charger Li-ion, atau BMS 1S; baterai alkaline biasa **tidak diisi ulang**. Kandidat empat AA seri mulai sekitar 6 V saat baru dan turun saat digunakan. Karena itu paket tersebut tidak boleh langsung ke pin 5 V ESP32; regulator harus menjaga keluaran sesuai spesifikasi sepanjang rentang baterai. MT3608 hanya menaikkan tegangan dan **bukan satu-satunya regulator yang cocok** untuk kandidat empat AA. Modul regulator spesifik belum lolos pemeriksaan skema/datasheet dan uji fisik.

**Alasan dan batas pilihan AA:** pengguna mengutamakan penggantian sel yang mudah ditemukan daripada proses pengisian 18650. AA memberi energi lebih besar daripada AAA pada beban sebanding menurut [datasheet Energizer E91 AA](https://data.energizer.com/pdfs/e91.pdf) dan [E92 AAA](https://data.energizer.com/pdfs/e92_ap.pdf), tetapi tetap menghasilkan limbah dan biaya penggantian berulang. Empat AA seri **menambah energi total dan tegangan**, bukan kapasitas Ah paket; jumlah akhir tidak boleh ditentukan hanya dari hitungan kapasitas di label. Estimasi pada rancangan menempatkan batas beban rata-rata sekitar **17–21 mA pada 5 V** untuk kandidat empat AA agar mencapai 72 jam dengan asumsi efisiensi dan cadangan tertentu. Ini belum hasil ukur dan bukan janji umur baterai.

**Status anggaran kembali terbuka.** Total lama Rp1.732.680 dari daftar Claude juga tidak berlaku setelah pilihan daya node berubah ke AA. Batas elektronik Rp2 juta tetap kebutuhan pengguna, tetapi belum ada RAB tervalidasi untuk SKU aktif, varian tepat, ongkir, SIM/paket data, baterai dan regulator hub, holder/stok AA node, serta alat rakit. Housing dihitung terpisah tetapi tetap diperlukan untuk uji laut. Sensor Depoinovasi+DMS, ADS1115, serta pembagi 10k/15k dari keranjang lama tidak masuk rancangan sekarang.

## Crosscheck teknis: apa yang sudah dan belum

| Komponen | Dasar datasheet produsen | Status SKU toko |
|---|---|---|
| ESP32-WROOM-32 | [Espressif](https://documentation.espressif.com/esp32-wroom-32_datasheet_en.html): GPIO, UART, SPI, mode tidur, logika 3,3 V. | Konsumsi **DevKit lengkap** saat aktif/tidur dan regulator board belum diukur. |
| DS18B20 | [Analog Devices](https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf): 1-Wire, catu 3,0–5,5 V, pull-up data 4,7 kΩ. | Seal dan material probe toko belum terbukti tahan air asin 72 jam. |
| E32-900T20D | [Manual Ebyte](https://www.ebyte.com/Uploadfiles/Files/2024-4-3/2024431610567020.pdf): modul UART pada pita 862–930 MHz dan konektor antena SMA-K. | Pastikan tiga unit varian yang sama; antena harus cocok pada frekuensi operasi Indonesia. Jangkauan ke darat belum diuji. |
| SIMCom A7670C | [Dokumen seri A7670](https://www.simcom.com/product/A7670X.html) / [hardware design](https://files.waveshare.com/wiki/A7670E-Cat-1-GNSS-HAT/A7672X_A7670X_Series_Hardware_Design_V1.03.pdf): catu, level UART modul mentah, pita LTE, dan kebutuhan arus puncak. | **Papan Shopee belum tervalidasi**: perlu skema/pinout input daya, level UART ke ESP32, slot SIM, antena termasuk atau tidak, serta kecocokan pita operator di lokasi. Jangan memberi daya modem dari pin 3V3 ESP32. |
| AA node, regulator, baterai hub, microSD | Datasheet [Energizer E91](https://data.energizer.com/pdfs/e91.pdf) memberi tegangan nominal AA 1,5 V dan kurva kapasitas menurut arus. Itu tidak membuktikan umur rakitan. | Modul regulator node, paket daya hub, dan pembaca microSD memerlukan skema/datasheet varian tepat serta uji pada unit fisik. **Judul listing belum membuktikan kecocokan board.** |

Untuk pita LPWAN 920–923 MHz, cek batas EIRP dan duty cycle pada [Permen Komdigi 2/2025](https://www.postel.go.id/downloads/40/20250208094700-permen_2025-02_perubahan_PM_Izin_Kelas_BN.pdf). Daya radio harus disetel dengan memperhitungkan gain antena. Angka jangkauan iklan bukan jaminan hubungan dua node ke hub di Pulau Tidung.

## Gerbang sebelum belanja final dan uji lapangan

1. Dapatkan skema/foto pinout **board A7670C** dan modul daya yang tepat; pastikan catu modem, regulator paket AA node, rancangan baterai hub, konektor antena, serta opsi 4G operator yang dipakai. Pastikan pilihan varian probe 3 m dan antena LoRa 915 MHz beserta harga sebenarnya.
2. Rakit satu node dan satu hub di meja. Ukur tegangan serta arus pada mode tidur, bangun, kirim LoRa, terima LoRa, tulis SD, dan unggah 4G. Uji kapasitas sel/microSD aktual. Baru dari hasil ini hitung ulang apakah baterai mampu **72 jam** dengan cadangan.
3. Uji dua node bersamaan dengan hub darat pada posisi dan tinggi antena yang realistis. Catat paket berhasil, retry, RSSI/SNR, dan perubahan saat pasang surut. Letakkan radio/antena di atas air; probe terendam pada kedalaman yang ditentukan.
4. Setelah housing dipilih, uji seal, kondensasi, korosi, strain relief kabel probe, dan operasi 72 jam. **Belum ada bukti PoC lapangan siap dilakukan** sebelum langkah ini.
5. Revisi firmware/Wokwi untuk dua node, pengiriman LoRa, penyimpanan/ACK hub, dan unggah seluler. Wokwi hanya membantu logika; radio fisik, konsumsi daya, modem, dan ketahanan laut harus diuji pada hardware.

Jangan memindahkan ambang suhu PoC atau data dari dua titik ini langsung menjadi prediksi ice-ice. Model di `ModelPOC` masih inisiasi, bukan patokan tervalidasi.
