---
type: project-status
created: 2026-11-12
updated: 2026-11-13
status: superseded
superseded_by: "[[Status PoC IoT Suhu SEAGIS - 13 November 2026]]"
supersedes: "[[Status PoC IoT Suhu SEAGIS - 8 November 2026]]"
tags: [radit, iot, lora, suhu, poc]
---

# Status PoC IoT Suhu SEAGIS — 12 November 2026

> [!warning] Riwayat
> Catatan ini sudah digantikan oleh [[Status PoC IoT Suhu SEAGIS - 13 November 2026]] (alat ditempatkan di laut, Node A tidak terdengar, Node B mengirim data lama, belum ada jalur perbaikan jarak jauh).

Catatan status dari sesi kerja 9 sampai 12 November 2026 (sampai sekitar pukul 21:45 WIB), menggantikan [[Status PoC IoT Suhu SEAGIS - 8 November 2026]]. Ini status **tes akhir di meja dan di dalam housing, bukan bukti uji laut**. Firmware, radio, modem, dan server sudah terbukti bekerja; yang belum siap adalah sambungan fisik.

Isi catatan ini adalah klaim agent dari sesi kerja (log serial dan pembacaan server), kecuali yang ditandai diverifikasi, pernyataan, atau hasil ukur pengguna.

## Posisi terakhir

Tes akhir sebelum lapangan sudah dijalankan pada 12 November. **Hub lolos**: radio, microSD, sinkron jam lewat jaringan, dan unggah tiap jam dari baterai. **Node A lolos dengan catatan**, dan **Node B gagal lalu pulih** di akhir sesi. Setelah ketiga board dimasukkan ke housing tertutup, Node B masuk satu siklus lalu hilang lagi, dan Node A sempat mati lalu probenya lepas lagi. Semua kegagalan hari itu berasal dari **kontak breadboard yang longgar**. Rekomendasi agent: **jangan berangkat ke lapangan dengan breadboard**; solder ketiga board, lalu ulang tes akhir dan tes semalam di housing.

## Yang berubah sejak 8 November

- **Token hub physical terpasang (9 Nov).** Data kini masuk sebagai data physical (`simulated=false`); record uji lama tidak ikut terbawa.
- **Firmware rilis siklus 1 jam (S7)** lulus tiga siklus berturut-turut untuk hub dan Node B pada 9 Nov malam. Node A gagal di uji itu karena sambungan daya.
- **Unggah dan sinyal:** di lokasi uji dengan sinyal 2G lemah (CSQ 5–11, pendaftaran jaringan ditolak), semua unggah semalam gagal **tanpa data hilang**; record menunggu di microSD. Di lokasi dengan CSQ 14, 93 record tertahan terkirim dalam sekitar 4 menit. Pada 12 Nov CSQ 30–31.
- **Hub dari baterai saja** terbukti mengunggah tiap jam (10 dan 12 Nov). Tegangan baterai hub turun sekitar 50–130 mV per jam, belum cukup untuk target 72 jam.
- **Penyebab radio hub "macet"** (sampah 1 byte setelah paket pertama, dicari sejak 8 Nov) akhirnya terbukti **kabel E32 hub yang longgar**, bukan modul, firmware, atau jarak antar-board. Memutus daya E32 tidak memulihkan; menekan ulang ketujuh kabelnya memulihkan. Setelah itu Node A menguras 12 bacaan yang tertahan sekitar dua hari.
- **Node B:** baterai habis (3,7 V) dan masuk mode CUTOFF; radio gagal berulang. Menukar modul E32 dengan milik Node A tetap gagal, jadi modulnya sehat. Firmware scan pin sementara menunjukkan pin 3V3 tidak tersambung ke rel dan tiga pin sinyal di satu sisi papan mengambang (dugaan: kaki papan atau lubang breadboard aus). Modul E32 Node A dan Node B kini tertukar; keduanya sehat.
- **Node A:** probe sempat terbaca gagal dua kali karena kabel lepas; hanya satu bacaan per bangun yang di-ACK, sehingga antrean tidak terkuras. Penyebabnya belum diselidiki.
- **Daftar uji:** 97 test case disusun dalam 11 kelompok (10 Nov). Skenario S1, S2, S3, S5, S6 lulus; S4 dan S7 sebagian; S8–S10 (akurasi probe, kalibrasi baterai, arus tidur) belum.
- **Housing:** kotak ABS 25 × 15 × 11,8 cm dengan pelampung foam closed-cell di tengah dan pemberat di dasar; hub sebaiknya di tiang atau darat. Ukuran dan daya apung masih perkiraan agent.

## Batas bukti dan data uji

- Sinyal 2G di lokasi lapangan belum diketahui; unggah gagal di CSQ 5–13 dan lolos di CSQ 14 ke atas.
- Belum pernah ada uji tanpa disentuh lebih dari beberapa jam; uji 72 jam belum dijalankan.
- Arus tidur belum diukur; ukuran baterai untuk 72 jam belum dihitung.
- Akurasi probe belum dicek dengan acuan; pembacaan baterai belum dikalibrasi dengan multimeter.
- Radio baru diuji dalam jarak beberapa meter; uji sekitar 100 m belum.
- Banjir output serial berulang di hub saat tercolok USB belum dijelaskan.

## Pekerjaan berikutnya

1. Solder ketiga board ke PCB berlubang: 3V3/GND, tujuh kabel E32, probe, dan jalur daya (termasuk jalur daya modem).
2. Ganti baterai baru di ketiga board; hitung kebutuhan baterai untuk 72 jam (baterai hub kemungkinan perlu lebih besar).
3. Ulang tes akhir yang sama, lalu tes semalam di dalam housing tanpa disentuh.
4. Selidiki satu-bacaan-per-bangun di Node A.
5. Uji dengan alat ukur (S8–S10), uji jarak sekitar 100 m, cek sinyal 2G di lokasi, siapkan kartu SIM lapangan.
6. Usulan untuk backend: tampilkan kejadian radio hub di status supaya diagnosis bisa dilakukan tanpa USB.
7. Butir lama: batas EIRP 433 MHz, jalur koordinat, pembersihan record uji, keputusan akses halaman pemantauan, `WIRING.md` dan diagram Wokwi.

## Sumber dan batas bukti

- Catatan sesi di second-brain pribadi (tidak ada di repo ini). Hasil ukur berasal dari pengguna; angka uji, radio, modem, dan baterai berasal dari log serial dan pembacaan server yang dilaporkan agent.
- Catatan ini sengaja tidak memuat token, ID, ref proyek, alamat MAC, nama akun, atau alamat deploy.
