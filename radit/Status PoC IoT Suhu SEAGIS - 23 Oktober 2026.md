---
type: project-status
created: 2026-10-23
updated: 2026-10-23
status: current-working-context
tags: [radit, iot, lora, suhu, poc]
---

# Status PoC IoT Suhu SEAGIS — 23 Oktober 2026

Catatan keputusan percakapan 22–23 Oktober 2026. Ini status rancangan dan pembelian, **bukan bukti perangkat telah lulus uji laut**. Ringkasan lama yang bertentangan harus dibaca sebagai riwayat.

## Rancangan terkini

| Topik | Keputusan dan batasnya |
|---|---|
| Sistem | 2 node ESP32 + DS18B20 → LoRa privat → 1 hub → microSD → modem/SIM → server/aplikasi. Salinitas dikeluarkan. |
| Radio | **3 set Ra-02 SX1278 433 MHz + antena 433 MHz dipilih untuk checkout**. Menggantikan kandidat E32-900T20D/920–923 MHz. Ra-02 memakai **SPI dan catu 3,3 V**; wiring UART E32 lama tidak berlaku. Alokasi pin final belum dibuat. |
| Jarak | Asumsi terbaru **masing-masing node sekitar 100 m dari hub**; belum hasil pengukuran lokasi dan bukan jaminan jangkauan. |
| Pemasangan | Pengguna menegaskan perangkat untuk **pemasangan nyata di laut**, dengan waktu terbatas untuk merakit ulang. Probe di air; elektronik/antena tetap di atas air. Hub tepi laut hanya bila kedua sambungan lolos uji. |
| Housing/antena | Antena bawaan dapat dicoba di dalam **housing plastik kedap air**. Ini pilihan pemasangan yang masih perlu uji sinyal, seal, embun, percikan asin, dan pasang-surut; bukan bukti antena bawaan tahan laut bila dipasang terbuka. |
| Jadwal | Target operasi 72 jam. Rencana 1 observasi per node per jam dan unggah batch tiap 24 jam → **144 slot target**, belum jadwal firmware final. |
| Seluler | Pengguna membolehkan **2G/GPRS**, jadi 4G tidak wajib. SIM800L hanya kandidat jika registrasi dan unggah 2G nyata berhasil di lokasi hub. |
| Daya | Dua node memakai AA alkaline yang diganti manual. Jumlah sel/regulator dan baterai hub belum dipilih; daya 72 jam belum terukur. |
| Probe | 5 m habis; 2 m tersedia. Kedalaman dan rute kabel belum pasti; panjang 2 m belum dinyatakan cukup. |

## Cakupan data lokal probe

**Radius wilayah yang diwakili satu probe belum diketahui dan belum tervalidasi.** DS18B20 membaca suhu di lokasi dan kedalaman ujung probe. Jarak radio 100 m atau jarak antar-node tidak menentukan cakupan suhu.

Catat observasi sebagai **titik koordinat + kedalaman + waktu**. Jika skema memerlukan `coverage_radius_m`, usulan engineering adalah membiarkannya kosong/null dengan status belum tervalidasi, bukan angka 0 m atau radius tebakan. Nama field ini belum menjadi kontrak API yang disepakati.

Untuk menetapkan radius representatif, tim perlu menentukan toleransi selisih suhu dan mengukur titik pembanding pada beberapa jarak, arah, waktu, serta kedalaman yang sebanding. Hasil hanya berlaku pada lokasi/kondisi yang diuji; tidak ada radius universal dari spesifikasi DS18B20.

## Data dan QoS yang harus dibangun

- Identitas paket `(node_id, boot_id, sequence)` tetap sama saat retry; kedua node memakai giliran kirim berbeda.
- Hub memberi **ACK setelah data tersimpan aman terhadap restart di microSD**. Node menyimpan paket belum diakui dan mencoba lagi; batas retry/antrean belum ditetapkan.
- Paket/ACK hilang, tabrakan, reboot, atau SD gagal harus menghasilkan data pulih atau gap yang terlihat. Data hilang bukan suhu 0 °C.
- Internet/server putus: data tetap dalam antrean SD. Hub menandai terkirim hanya setelah server mengakui; server mencegah duplikat.
- Bedakan waktu ukur, terima hub, dan masuk server; jam belum sinkron diberi status tidak pasti. Pisahkan kualitas pengukuran dari status pengiriman.
- Laporkan 144 slot target, valid/diragukan/hilang, retry, duplikat, keterlambatan, dan kecocokan SD–server. Batas lolos numerik packet loss/latensi belum disepakati.

## Checklist pembelian

Tercentang berarti sudah dimiliki menurut pengguna. Belum tercentang berarti belum ada konfirmasi pesanan selesai; screenshot keranjang masih di tahap **Buat Pesanan**.

- [x] 1 ESP32 sudah dimiliki.
- [ ] [2 ESP32 DevKit 30 pin](https://id.shp.ee/WaTYdyw6).
- [ ] [10 resistor 4,7 kΩ](https://id.shp.ee/JCgnZjMD), 2 dipakai untuk dua probe.
- [ ] [2 probe DS18B20](https://id.shp.ee/kRFTkd7f), panjang kabel final menunggu kedalaman/rute.
- [ ] [3 Ra-02 433 MHz + antena](https://id.shp.ee/SRvGS13x), dipilih untuk checkout; screenshot Rp101.850/set. [Listing alternatif pengguna](https://id.shp.ee/jEEA1gJ6) Rp100.800, tetapi frekuensi/varian antenanya belum dipastikan dari screenshot.
- [ ] Modem/antena/SIM: kandidat [SIM800L V2](https://shopee.co.id/Sim800l-V2-V.2-V2.0-5V-GSM-GPRS-module-antena-antenna-micro-sim-card-i.1555409167.54960841730), belum final.
- [ ] Pembaca dan kartu microSD; AA/holder; baterai hub; regulator; kabel, konektor, komponen solder; housing, seal, dudukan, dan penambat.

**Anggaran:** cap target Rp2.000.000. Jika keranjang awal Rp182.480 dan 3 radio Rp305.550, total sementara **Rp488.030**, sisa **Rp1.511.970** sebelum belanja lainnya/ongkir radio. Ini bukan RAB lengkap atau total yang sudah dibayar. Housing sebelumnya dipisahkan dari anggaran elektronik, tetapi tetap wajib.

## Sumber dan pekerjaan lanjutan

Keputusan/stok/harga berasal dari percakapan dan screenshot pengguna; harga bukan verifikasi pasar terbaru. Sumber teknis yang dirujuk dalam sesi:

- [Ai-Thinker Ra-02](https://docs.ai-thinker.com/en/Ra-02/index.html): SPI, 3,3 V, 410–525 MHz; spesifikasi chip/modul tidak menjamin kualitas SKU toko.
- [Permen Komdigi 2/2025](https://www.postel.go.id/downloads/40/20250208094700-permen_2025-02_perubahan_PM_Izin_Kelas_BN.pdf): LPWAN 433,05–434,79 MHz, lebar kanal maksimal 125 kHz, EIRP maksimal 16,4 mW/12,15 dBm termasuk pengaruh antena. Daya maksimum iklan 20 dBm bukan setelan yang boleh langsung dipakai.
- [Datasheet DS18B20](https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf): spesifikasi suhu dan kelistrikan, tanpa radius representatif area laut.
- [Analog Devices: probe pihak ketiga](https://ez.analog.com/dsp/otherdsp/a/documents/do19739/can-the-ds18b20-be-submerged-in-water): mutu seal bukan jaminan produsen chip.
- [NOAA: deskripsi pengukuran](https://www.ndbc.noaa.gov/faq/measdes.shtml): pengukuran laut disertai kedalaman; tidak menetapkan radius untuk probe ini.

README kerja telah diringkas menjadi **tabel kebutuhan → alur sensor–server → QoS → checklist belanja**, tanpa tautan wajib ke dokumen requirements terpisah. Berkas asli: `/Users/radityaaydin/repos/depok/sealiit-poc-v3/README.md` dan `IOT_TECHNICAL_REQUIREMENTS.md`. Kode Wokwi tetap simulasi lama satu alat/5 jam; belum ada firmware dua node–hub, bukti daya 72 jam, atau hasil uji laut. Tugas berikut: finalisasi kedalaman/rute, daya, posisi alat, SKU modem, API/waktu/antrean, dan gerbang uji sebelum pemasangan.
