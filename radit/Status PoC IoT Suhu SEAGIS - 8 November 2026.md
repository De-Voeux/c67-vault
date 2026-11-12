---
type: project-status
created: 2026-11-08
updated: 2026-11-12
status: superseded
superseded_by: "[[Status PoC IoT Suhu SEAGIS - 12 November 2026]]"
supersedes: "[[Status PoC IoT Suhu SEAGIS - 6 November 2026]]"
tags: [radit, iot, lora, suhu, poc]
---

# Status PoC IoT Suhu SEAGIS — 8 November 2026

Catatan status dari sesi kerja 6 November malam sampai 8 November 2026 (sampai sekitar pukul 20:10 WIB), menggantikan [[Status PoC IoT Suhu SEAGIS - 6 November 2026]]. Ini status **uji meja hampir selesai, bukan bukti uji laut**. Hampir semua skenario meja sudah dijalankan; yang tersisa adalah pengukuran dengan alat ukur, firmware rilis penuh, dan syarat lapangan.

Isi catatan ini adalah klaim agent dari sesi kerja (log serial dan pembacaan server), kecuali yang ditandai diverifikasi, pernyataan, atau hasil ukur pengguna.

## Posisi terakhir

Hub dan dua node berjalan di meja: node mengirim lewat LoRa ke hub, hub menulis ke microSD lalu mengunggah ke server lewat SIM800L. Uji firmware rilis (siklus satu jam) sudah dua dari tiga siklus; pengguna menjeda pemantauan sebelum siklus ketiga dinilai. Perbaikan firmware hub yang ditulis malam itu sudah lolos kompilasi tetapi **belum dipasang di board dan belum diuji**.

## Yang berubah sejak 6 November

- **Hasil uji meja (build uji, siklus 1 menit kecuali S7):** hub dan Node A dari baterai 30 menit lulus (cakupan data 96% dan 93%); hub dimatikan 3 menit lulus (data tertunda masuk dengan jam asli, tanpa duplikat); node restart lulus (terjadi tanpa sengaja karena kabel goyang); probe dilepas lulus (nilai kosong ber-flag, bukan 0 °C); backlog unggah lulus. Jaringan putus (S4) awalnya **gagal**, lalu lulus setelah perbaikan di bawah. Firmware rilis siklus 1 jam: siklus 1 dan 2 lulus, siklus 3 belum dinilai.
- **Kelemahan firmware yang ditemukan:**
  1. Hub yang reset (misalnya daya putus) sebelum bisa sinkron jam menandai record tanpa jam dan tidak pernah mengunggahnya. Datanya masih di microSD. Diperbaiki dengan memperkirakan jam dari urutan `seq` node (ditandai `time_basis = hub_rx`); 239 record dipulihkan. Tiga menit Node A pada uji itu belum terjelaskan.
  2. Unggah yang lama (sinyal lemah) bisa menghabiskan jendela dengar. Kini unggah dijeda sebelum jendela berikutnya.
  3. Radio E32 hub pernah macet (pin AUX tetap rendah) dua kali setelah node mengirim antrean panjang beruntun. Reset dari firmware tidak memulihkan; hanya memutus daya E32. Jeda 800 ms antarpaket diduga membantu (satu kali uji), **penyebab belum terbukti**.
- **Penyebab kegagalan terbanyak adalah fisik:** satu kabel GND pada pembagi baterai Node A hilang (membuat bacaan baterai palsu), kabel daya Node A goyang beberapa kali sampai node mati sebentar, dan kabel daya modem yang dicabut ikut mereset hub. Solder atau terminal sekrup untuk jalur daya kini prioritas pertama.
- **Backend mengirim kontrak API untuk hub physical** (identitas hub dan token baru, `hub.simulated=false`). Firmware diubah agar mode ikut token, `400 invalid_batch` tidak lagi membuang data, dan backlog uji tidak terkirim sebagai data physical. Perubahan belum dipasang di board. **Token hub physical belum dimiliki**; harus diminta ke operator backend lewat kanal privat.
- **Dua probe di satu wadah air** membaca berbeda paling banyak 0,06 °C (satu langkah resolusi sensor). Akurasi mutlak belum terbukti; pengguna belum punya termometer acuan (usulan agent: uji air es ±0 °C).
- **Pembacaan baterai Node A** kini wajar (±4,8–5,4 V) tetapi belum dicocokkan dengan multimeter.

## Batas bukti dan data uji

- Data di server masih campuran data uji (`simulated=true`), baterai Node B palsu (penanda 5555 mV, Node B masih lewat USB), dan bacaan dari tes.
- Penyebab boot karena watchdog pada hub dan sebab E32 macet belum diketahui.
- Regresi simulasi belum diulang setelah banyak perubahan firmware.
- Arus tidur belum diukur; target baterai 72 jam belum terbukti.
- Radio baru diuji di atas meja; jarak sekitar 100 m belum. SIM800L gagal di sinyal lemah (CSQ 13) dan lolos di sinyal kuat (CSQ 24–29); kondisi Pulau Tidung belum dicek.

## Pekerjaan berikutnya

1. Solder atau pasang terminal sekrup pada jalur daya hub dan node.
2. Nilai siklus 3 firmware rilis; regresi simulasi; pasang firmware terbaru di ketiga board.
3. Dapatkan token hub physical dari operator backend; pasang baterai asli di Node B; kirim satu pembacaan aktual per node dan cocokkan dengan riwayat server.
4. Uji dengan alat ukur: kalibrasi baterai (multimeter), akurasi probe (air es atau termometer acuan), arus tidur hub dan node.
5. Uji jarak sekitar 100 m, cek sinyal 2G di lokasi, siapkan kartu SIM lapangan.
6. Pertimbangkan pemutusan daya E32 dari firmware; selidiki sebab E32 macet dan boot watchdog.
7. Butir lama: batas EIRP 433 MHz, jalur koordinat, pembersihan record uji, keputusan akses halaman pemantauan, `WIRING.md` dan diagram Wokwi.

## Sumber dan batas bukti

- Catatan sesi di second-brain pribadi (tidak ada di repo ini). Hasil ukur berasal dari pengguna; angka uji, radio, modem, dan baterai berasal dari log serial dan pembacaan server yang dilaporkan agent.
- Catatan ini sengaja tidak memuat token, ID, ref proyek, alamat MAC, nama akun, atau alamat deploy.
