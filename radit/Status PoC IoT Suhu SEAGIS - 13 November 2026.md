---
type: project-status
created: 2026-11-13
updated: 2026-11-13
status: current-working-context
supersedes: "[[Status PoC IoT Suhu SEAGIS - 12 November 2026]]"
tags: [radit, iot, lora, suhu, poc]
---

# Status PoC IoT Suhu SEAGIS — 13 November 2026

Catatan status dari sesi kerja 12 sampai 13 November 2026 (sampai sekitar pukul 21:50 WIB), menggantikan [[Status PoC IoT Suhu SEAGIS - 12 November 2026]]. **Alat sudah ditutup** (pengguna: "semua node ku tutup skrg, full battery") dan dianggap sudah di laut, karena pengguna lalu menanyakan data air laut. Hasilnya **belum menjadi data suhu laut yang bisa dipakai**.

Isi catatan ini adalah klaim agent dari sesi kerja (log serial dan pembacaan server), kecuali yang ditandai diverifikasi atau pernyataan pengguna.

## Posisi terakhir

- **Hub** berjalan dari baterai dan mengunggah tiap jam. Tegangan baterainya stabil sekitar 5,3 V sejak siang 13 November, lebih baik dari perkiraan turun sekitar 55 mV per jam.
- **Node A** tidak terdengar sejak sekitar 11:46 WIB, tepat sebelum kotak ditutup. Dugaan: kabel radio lepas lagi saat kotak ditutup, atau mati; dari server keduanya tampak sama.
- **Node B** masih terdengar tetapi hanya mengirim 1–2 bacaan per jam dari antrean penuh (48). Karena antrean dikirim dari yang tertua, **yang sampai ke server adalah bacaan lama dari meja**, bukan suhu laut. Semua baris Node B pada 13 November bertanda waktu terima di hub (`time_basis=hub_rx`) dan nilainya cocok dengan log pengukuran di meja.

## Yang berubah sejak 12 November

- **Firmware node mengukur tiap 30 menit** dan tetap mengirim sekali per jam (dua bacaan per slot). Di-flash ke kedua node pada 13 November siang. Hanya terbukti di simulasi dan satu unggahan Node B; belum teruji lama.
- **Penyebab gangguan berulang di meja** tetap kontak kabel: kabel 3V3 ke rel dan kabel sinyal E32 yang lepas setiap kali kabel USB dicabut.
- **Tidak ada jalur perbaikan jarak jauh** pada firmware yang berjalan sekarang: hub tidak membaca perintah dari respons server, ACK ke node berformat tetap, modem tidak punya jalur masuk, dan tidak ada pembaruan lewat internet (OTA). Pengguna menyatakan tidak bisa kembali ke lokasi. Cara menghubungi alat dari jauh belum ditemukan.
- **Backend:** server menerima unggahan dan menandai data Node B sebagai kurang tepercaya karena waktu. Agent menulis jawaban rinci untuk tim backend tentang perilaku firmware dan pola waktu data.
- **Pemantauan:** pemindahan dashboard ke hosting lain belum selesai; alamat dashboard khusus sedang tidak aktif. Lihat catatan tim monitoring untuk status terbarunya.

## Batas bukti dan data uji

- Belum ada satu pun bacaan suhu laut yang terbukti masuk ke server.
- Posisi dan waktu penempatan tidak tercatat di sesi ini.
- Perkiraan sisa baterai (hub sampai batas rendah sekitar 8 jam menurut laju lama; node sekitar satu hari) kasar dan sudah terbukti terlalu pesimistis untuk hub.
- Uji 72 jam, arus tidur, akurasi probe, dan jangkauan radio sekitar 100 m masih seperti pada catatan 12 November.

## Pekerjaan berikutnya

1. Tentukan cara menghadapi alat yang sudah di laut: menunggu baterai habis lalu mengambil, atau merencanakan kunjungan.
2. Pisahkan data meja dan data laut di server (tandai atau bersihkan bacaan lama dengan `time_basis=hub_rx`).
3. Pasang jalur perintah dari server ke hub ke node (downlink) di versi firmware berikutnya, supaya alat bisa diperbaiki tanpa kunjungan.
4. Selesaikan butir lama: soldering ke PCB lubang, tes semalam dalam housing, batas EIRP 433 MHz, jalur koordinat, dan `WIRING.md` serta diagram Wokwi.
