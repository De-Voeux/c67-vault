---
type: engineering-design
created: 2026-10-21
updated: 2026-10-23
status: rancangan-lapangan-belum-tervalidasi
tags: [radit, iot, lora, suhu, poc]
---

# Rancangan alat PoC suhu LoRa

> **Pembaruan 23 Oktober 2026:** baca [[Status PoC IoT Suhu SEAGIS - 23 Oktober 2026]] terlebih dahulu. Pilihan terbaru adalah Ra-02 433 MHz (SPI), 2G/GPRS diperbolehkan, dan asumsi tiap node ke hub sekitar 100 m. Radius cakupan suhu probe belum tervalidasi. Wiring UART E32/920 MHz, kewajiban 4G, dan harga lama di bawah merupakan riwayat; bukan daftar rakit/pembelian final.

Rancangan ini menerjemahkan [[Keputusan PoC IoT Suhu LoRa - 21 Oktober 2026]] menjadi tiga perangkat untuk **MVP yang diuji langsung di lapangan, di Pulau Tidung**. Pemeriksaan singkat di meja tetap dilakukan sebelum pemasangan untuk mencegah kerusakan, tetapi tidak dihitung sebagai MVP tersendiri. Ini belum skema listrik final atau bukti daya tahan/jangkauan. Nomor pin dan catu breakout baru boleh dikunci setelah modul fisik dan skemanya cocok dengan datasheet produsen.

## Hasil yang harus dicapai

- Dua node mengukur **suhu air** pada dua titik dengan satu DS18B20 per node. Tidak ada sensor salinitas pada PoC ini.
- Setiap node mengirim satu pengukuran per jam ke satu hub melalui LoRa privat. Node A dan B memakai slot kirim berbeda agar tidak bertabrakan.
- Hub di darat jika uji jangkauan berhasil. Hub menyimpan pengukuran ke microSD, lalu mengunggah kumpulannya melalui 4G/SIM ke server setiap 24 jam. Server harus menerima ulang tanpa membuat duplikat.
- Ketiganya beroperasi terus selama 72 jam. Batas RAB elektronik target Rp2 juta untuk dua node dan satu hub **belum terbukti terpenuhi**. Housing dicatat sebagai **anggaran terpisah di luar RAB elektronik saat ini**, tetapi dua housing node dan perlindungan hub tetap diperlukan sebelum MVP dipasang di lapangan.

```text
AIR:   probe A ─ node A + antena di atas air ─┐
                                              ├─ LoRa 920–923 MHz ─ hub di darat ─ microSD
       probe B ─ node B + antena di atas air ─┘                     └─ 4G/SIM ─ server/app
```

Ini sambungan radio langsung antarperangkat, **bukan LoRaWAN**. Aplikasi memperoleh data setelah unggah harian, sehingga belum dapat memberi peringatan waktu nyata per jam.

## Komponen per perangkat

| Bagian | Node A | Node B | Hub | Alasan dan status |
| --- | ---: | ---: | ---: | --- |
| ESP32-WROOM-32 DevKit 30 pin | 1 | 1 | 1 | MCU dengan GPIO/UART/SPI. Board toko dan arus tidur keseluruhan belum diverifikasi. |
| Probe DS18B20 + resistor pull-up 4,7 kΩ | 1 + 1 | 1 + 1 | – | Sensor suhu digital 1-Wire; pull-up diperlukan pada jalur data. Kualitas selubung probe terhadap air asin belum terbukti. |
| Ebyte E32-900T20D atau **tiga radio UART identik yang tervalidasi** | 1 | 1 | 1 | Mengirim paket LoRa. Varian 862–930 MHz dapat dikaji untuk pita Indonesia; konfigurasi kanal, daya, dan tegangan board harus dipastikan. |
| Antena LoRa yang sesuai radio, konektor, dan frekuensi kerja | 1 | 1 | 1 | Antena adalah bagian dari sistem radio; antena 433 MHz tidak dipasang untuk rancangan 920–923 MHz. |
| Baterai AA alkaline, holder AA, saklar, regulator | 1 set | 1 set | – | **Keputusan terbaru: baterai node diganti manual, bukan diisi ulang.** Kandidat awal empat AA seri per node; jumlah akhir dan regulator dipastikan lewat pengukuran rakitan 72 jam. Holder 18650, BMS 1S, TP4056, dan charger Li-ion tidak diperlukan untuk node AA. |
| Pembaca microSD SPI 3,3 V + kartu microSD | – | – | 1 + 1 | Penyimpanan lokal sebelum unggah. ESP32 DevKit tidak memiliki slot microSD bawaan. |
| Modem 4G Cat-1 breakout + antena LTE + SIM aktif | – | – | 1 set | Kandidat keluarga SIMCom A7670; varian band, skema breakout, level UART, dan suplai belum terkunci. |
| Paket baterai hub berkapasitas lebih besar + proteksi/regulator sesuai kimia dan modem | – | – | 1 set | **Wajib untuk target 72 jam.** Jenis dan jumlah sel belum dipilih; jangan mengasumsikan power bank. Tentukan dari arus hub lengkap serta lonjakan modem. Daftar Claude hanya memuat dua sel 18650 untuk node, belum baterai hub. |
| PCB prototipe, kabel, konektor, penyekat, alat ukur/rakit | sesuai kebutuhan | sesuai kebutuhan | sesuai kebutuhan | Jumlah ditentukan setelah skema dan lokasi pemasangan dipilih. |

**Total fungsi minimal dalam RAB elektronik saat ini:** tiga MCU, dua probe, dua resistor 4,7 kΩ, tiga radio, tiga antena LoRa, satu pembaca+kartu microSD, satu modem 4G+antena LTE+SIM/paket data, dua paket baterai AA node beserta regulator dan stok penggantinya, serta satu paket baterai hub dengan catu/proteksi sesuai pilihan akhirnya. Siapkan kabel data USB, multimeter, alat solder, serta termometer pembanding. Tidak ada ADS1115, sensor EC, atau pembagi tegangan EC 10k/15k dalam rancangan baru.

**Di luar RAB elektronik saat ini, tetapi wajib sebelum pemasangan:** dua housing kedap air untuk node, gland kabel, penambat/pelampung, serta perlindungan cuaca/air dan dudukan antena hub di darat. Biayanya dicatat dalam RAB housing terpisah; komponen ini tidak dianggap selesai hanya karena belum dibeli.

## Sambungan listrik awal

**Node (dua perangkat dengan wiring sama):** DS18B20 merah → 3,3 V, hitam → GND, data → GPIO27; resistor 4,7 kΩ di antara data dan 3,3 V. Radio UART TXD → RX ESP32 GPIO16, RXD ← TX ESP32 GPIO17; M0 → GPIO25, M1 → GPIO26, AUX → GPIO34 (input). Semua GND disatukan. Antena sesuai konektor dipasang **sebelum mengirim**. GPIO35/ADC1 dapat dipakai mengukur tegangan paket AA melalui pembagi yang dirancang dan diuji; paket baterai tidak boleh langsung ke GPIO.

**Hub:** radio menggunakan GPIO16/17/25/26/34 seperti node. microSD SPI: SCK GPIO18, MISO GPIO19, MOSI GPIO23, CS GPIO13. UART modem sementara menggunakan RX ESP32 GPIO32 dan TX GPIO33; sambungannya **belum boleh dilakukan** sebelum tahu level UART pada breakout. Modul SIMCom mentah memakai UART 1,8 V; breakout tertentu mungkin menambah pengubah level. ESP32 3,3 V **bukan** sumber daya modem. Tombol daya modem/PWRKEY dihubungkan hanya menurut skema breakout yang tepat.

Pin di atas ialah alokasi ESP32 untuk prototipe, bukan klaim pinout papan Shopee. Periksa label fisik, arah TX/RX, kebutuhan level shifter, dan regulator modul. Radio, microSD, modem, serta ESP32 harus berbagi GND jika memakai catu terpisah. Pilih pembaca microSD yang benar-benar berlogika 3,3 V; jangan mengandalkan tulisan “5 V” pada listing tanpa skema.

### Jalur daya yang diusulkan

```text
Node: paket AA alkaline ─ saklar ─ regulator 5 V terukur ─ ESP32 DevKit
                                    └─ catu radio sesuai spesifikasi modul
      setelah masa operasi, sel AA diganti di darat dengan sel baru.

Hub: paket baterai + proteksi ─ regulator/rel yang sanggup menahan lonjakan modem
                               ├─ ESP32 + breakout modem sesuai spesifikasi board
                               └─ catu radio + pembaca microSD sesuai spesifikasi modul
```

Empat AA alkaline seri menghasilkan sekitar 6 V saat baru dan tegangannya turun selama pemakaian. Karena itu **jangan hubungkan paket AA langsung ke pin 5 V**. Rancangan kandidat membutuhkan regulator 5 V yang bisa menurunkan *dan* menaikkan tegangan (buck-boost) sepanjang rentang pakai baterai; MT3608 hanya penaik tegangan, sehingga tidak cocok sebagai satu-satunya regulator untuk empat AA. Pilih modul regulator setelah skema, batas tegangan masuk, arus puncak, arus diam, dan efisiensinya diperiksa. Jangan menyuplai radio dari pin 3V3 DevKit sampai cadangan arus regulator board terbukti cukup. Modem memerlukan jalur daya tersendiri sesuai board yang dipilih dan lonjakan arusnya. **BMS 1S serta TP4056 adalah untuk Li-ion, bukan baterai AA alkaline.** Jangan mengisi ulang AA alkaline biasa.

## Alur kerja firmware

1. Hub memperoleh waktu UTC dari jaringan saat tersedia, memasang radio sebagai penerima, membuka microSD, lalu menunggu paket. Modem mati atau masuk mode hemat daya di luar jendela unggah **hanya jika board mendukung kendali daya yang teruji**.
2. Node A bangun setiap jam pada menit yang ditetapkan; node B beberapa menit sesudahnya. Node membaca suhu, memeriksa nilai tidak valid, memberi `node_id`, `boot_id`, dan `seq`, lalu mengirim paket. Setelah ACK diterima, node tidur lagi dengan ESP32 dan radio di mode hemat daya.
3. Hub memeriksa checksum/CRC, menyimpan rekaman ke microSD, melakukan flush, **baru mengirim ACK**. Jika ACK tidak datang, node menyimpan paket belum diakui dalam antrean kecil flash dan mencoba ulang dengan batas percobaan. Pengiriman ulang dengan identitas sama tidak menjadi baris ganda.
4. Tiap 24 jam hub menyalakan koneksi 4G, mengunggah batch dengan HTTPS, memeriksa balasan server, lalu menandai rekaman yang sudah diterima. Bila internet gagal, backlog tetap di kartu dan dicoba lagi. Jangan menghapus data hanya karena request sudah terkirim.

Contoh isi rekaman: `node_id`, `boot_id`, `seq`, `temp_c_x100`, `battery_mv`, `received_at_utc`, `time_valid`, `quality_flags`, `upload_status`. Kunci deduplikasi server adalah `(node_id, boot_id, seq)`. Waktu terima hub berbeda dari waktu ukur, terutama setelah retry. Jika hub tidak punya waktu valid saat reboot, beri tanda `time_valid=false`; jangan mengarang timestamp. Untuk rekonstruksi waktu ukur yang presisi setelah gangguan radio lama, tambahkan sinkronisasi waktu node atau RTC—belum masuk rancangan biaya ini.

## Perhitungan awal baterai, bukan janji 72 jam

- **Estimasi kandidat empat AA seri per node:** andaikan tiap sel memberi 2–2,5 Ah pada tegangan kerja rata-rata sekitar 1,2 V, energi paket sekitar **9,6–12 Wh**. Setelah asumsi efisiensi catu 80% dan cadangan 20%, untuk 72 jam daya rata-rata maksimum sekitar **0,085–0,107 W**, setara **17–21 mA pada 5 V**. Ini perhitungan ilustratif, bukan kapasitas terjamin: [datasheet Energizer E91](https://data.energizer.com/pdfs/e91.pdf) menunjukkan kapasitas berubah mengikuti arus dan batas tegangan akhir. Cutoff regulator, pulsa radio, serta arus tidur **DevKit lengkap + regulator + radio** menentukan hasil nyata.
- Contoh kebutuhan hub: bila paket baterai memiliki energi nominal **74 Wh** dan hanya 80% sampai ke beban, rata-rata batas sekitar **0,82 W atau 164 mA pada 5 V** selama 72 jam; dengan cadangan 20%, sekitar **132 mA**. Ini contoh energi, **bukan** pilihan jenis baterai atau kapasitas yang sudah disetujui. Beban puncak modem harus diuji terpisah dari rata-rata.

Kedua angka hanya **batas desain berdasarkan kapasitas nominal dan asumsi rugi**. Ukur konsumsi rakitan utuh pada tidur, bangun, LoRa TX/RX, menulis SD, modem mencari jaringan, dan unggah. Jika hasil melampaui batas, ubah board/daya sebelum mengklaim 72 jam; jangan sekadar menambah kapasitas tertulis di listing.

### Keputusan AA alkaline untuk node

AA dipilih untuk **dua node** agar pengguna cukup mengganti baterai habis dengan sel baru. Pilih holder **AA**, bukan AAA atau 18650. Empat AA seri adalah kandidat awal yang perlu diuji bersama regulator; jumlah itu belum menjamin 72 jam. **Susunan seri menaikkan tegangan, bukan kapasitas Ah;** energi total naik karena ada lebih banyak sel. Jangan menambah sel tanpa mengecek batas tegangan seluruh rangkaian. Gunakan sel alkaline baru dengan merek/tipe sama dalam satu holder; jangan mencampur sel lama dan baru.

Holder **3 slot 18650** dan tiga BMS 1S dalam screenshot keranjang harus dikeluarkan dari daftar belanja **node**. Pilihan baterai hub tetap terpisah: pengguna meminta hub memakai baterai, tetapi belum memutuskan apakah hub juga AA. Radio hub menerima terus dan modem memiliki lonjakan arus, sehingga paket daya hub harus dihitung dari beban aktual.

## Radio dan penempatan

Rencanakan satu kanal yang legal dalam **920–923 MHz**, bandwidth dan duty cycle sesuai [Permen Komdigi 2/2025](https://www.postel.go.id/downloads/40/20250208094700-permen_2025-02_perubahan_PM_Izin_Kelas_BN.pdf). Ketiga radio harus memiliki kanal, modulasi, laju, dan format paket yang sama; firmware memberi ID tiap node. Daya pancar harus dihitung sebagai EIRP termasuk gain antena. Radio “915 MHz” belum otomatis siap untuk kanal Indonesia; cek tabel kanal dan kemampuan antenanya. Jangkauan ke pantai tidak dapat dipastikan dari datasheet saja.

Probe ditempatkan pada kedalaman budidaya yang konsisten. Elektronik dan antena node berada **di atas permukaan air**; hub di darat pada tempat lebih tinggi dan terbuka jika uji sambungan dari **kedua** node lolos. Setelah housing dipilih, periksa gland kabel, seal, strain relief, kondensasi, korosi, penambatan, serta pengaruh pasang-surut. Tanpa housing yang diuji, rancangan ini hanya layak untuk meja/lab, belum perendaman 72 jam.

## Urutan pembuktian dan syarat lolos MVP lapangan

1. **Identitas komponen:** dapatkan varian persis dan skema/datasheet untuk tiga board radio, tiga antena, modem breakout, pembaca microSD, serta modul daya. Cocokkan catu, logika pin, band, konektor, dan arus puncak. Cek band operator SIM yang benar-benar dipakai di Pulau Tidung. Harga/SKU belum divalidasi; jangan memakai tautan Shopee atau total Rp1.900.829 dari daftar lama.
2. **Pemeriksaan sebelum berangkat:** rakit kedua node dan hub, uji suhu terhadap termometer pembanding, LoRa dua arah, ACK setelah SD tersimpan, restart/pemulihan data, dan unggah HTTPS sungguhan lewat SIM. Periksa catu modem saat mengirim, serta ukur arus mode tidur, terima, dan unggah. Ini pemeriksaan keselamatan fungsi, bukan MVP terpisah.
3. **Housing:** pasang dan uji kebocoran kedua node serta perlindungan hub. Pastikan baterai, MCU, radio, dan sambungan tetap kering; kabel probe dan antena tidak menarik seal saat pelampung bergerak.
4. **Jangkauan di lokasi:** tempatkan hub di darat dan dua node pada posisi budidaya yang direncanakan. Catat paket diterima, retry, RSSI/SNR, dan pasang-surut; ubah tinggi/posisi antena bila salah satu jalur gagal.
5. **MVP 72 jam di lapangan:** jalankan semua perangkat dengan sumber daya final. Pastikan hub menyimpan tiap jam dan server menerima unggahan harian melalui 4G. Cocokkan 144 rekaman yang diharapkan dari dua node dengan microSD dan server; periksa tegangan akhir, reboot, kebocoran, kekosongan, dan duplikasi.

## Batas Wokwi dan anggaran

Simulasi Wokwi lama masih menggambarkan rancangan lima jam dengan kanal sensor yang kini dikeluarkan. Versi baru perlu logika dua node dan satu hub, ACK, antrean, penulisan SD, serta unggah harian yang dapat dimock. Wokwi berguna untuk alur kode, **bukan** bukti jangkauan radio, daya baterai, kompatibilitas breakout 4G, atau ketahanan air laut.

RAB elektronik yang sah baru bisa dibuat setelah SKU dan harga aktif dicek untuk **seluruh** komponen, ongkir, SIM/paket data, **paket baterai hub**, holder dan stok AA node, regulator yang cocok, serta alat rakit. **Housing mempunyai RAB terpisah** dan tidak dihitung dalam cap elektronik Rp2 juta saat ini, tetapi tetap perlu sebelum uji laut. Estimasi lama Rp1.732.680 dari daftar Claude **tidak lagi berlaku** setelah perubahan daya node ke AA; selain itu SKU/tautan belum seluruhnya diverifikasi dan baterai hub belum dihitung. Hitung ulang dari awal. Jika rancangan elektronik yang benar melampaui Rp2 juta, laporkan selisihnya; jangan menghilangkan 4G atau catu yang aman untuk membuat angka tampak cocok.

## Dasar spesifikasi yang sudah diperiksa dan batasnya

- [Espressif ESP32-WROOM-32](https://documentation.espressif.com/esp32-wroom-32_datasheet_en.html): modul 3,0–3,6 V, GPIO/UART/SPI; bukan arus lengkap DevKit toko.
- [Analog Devices DS18B20](https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf): 3,0–5,5 V, 1-Wire, pull-up 4,7 kΩ; bukan sertifikat seal probe toko.
- [Ebyte E32-900T20D](https://www.ebyte.com/Uploadfiles/Files/2024-4-3/2024431610567020.pdf): kandidat modul LoRa UART; cek varian dan tabel kanal modul yang benar sebelum membeli/menyambung.
- [Energizer E91 AA alkaline](https://data.energizer.com/pdfs/e91.pdf): 1,5 V nominal per sel; kapasitas bergantung arus dan batas tegangan akhir. Angka 72 jam di atas tetap harus dibuktikan pada rakitan utuh.
- [SIMCom A7670 series](https://www.simcom.com/product/A7670X.html) dan [hardware design](https://files.waveshare.com/wiki/A7670E-Cat-1-GNSS-HAT/A7672X_A7670X_Series_Hardware_Design_V1.03.pdf): rujukan modem mentah; board toko memerlukan verifikasi skema tersendiri.
- [Dokumentasi sleep ESP32](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/sleep_modes.html) dan [NVS](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/storage/nvs_flash.html): kemampuan firmware, bukan hasil uji daya/umur flash pada perangkat jadi.
