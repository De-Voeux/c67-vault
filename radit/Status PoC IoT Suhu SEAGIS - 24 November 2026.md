---
type: project-status
created: 2026-11-24
updated: 2026-11-24
status: current-working-context
supersedes: "[[Status PoC IoT Suhu SEAGIS - 13 November 2026]]"
tags: [radit, iot, lora, suhu, poc]
---

# Status PoC IoT Suhu SEAGIS — 24 November 2026

Catatan status dari sesi kerja 23 sampai 24 November 2026, menggantikan [[Status PoC IoT Suhu SEAGIS - 13 November 2026]]. **Alat sudah diangkat dari laut pada 24 November** (pengguna: dijemput sekitar 11:55 WIB). Data yang tersisa di perangkat sudah disalin, dan bacaan suhu laut pertama sudah masuk ke server.

Isi catatan ini adalah klaim agent dari sesi kerja (salinan flash perangkat, log kartu microSD, dan pembacaan server), kecuali yang ditandai sebagai pernyataan pengguna.

## Apa yang terjadi selama di laut

- **Ketiga perangkat mati karena baterai** dalam satu sampai dua hari setelah penempatan 13 November. Node A hanya merekam sekitar 2,5 jam. Node B merekam sekitar 25 jam, sampai sekitar 14:04 WIB 14 November. Hub mati sekitar 03:56 WIB 14 November.
- **Tidak ada bacaan laut yang sampai ke hub.** Hub hanya menerima sisa antrean bacaan meja dari Node B, satu per jam dan yang tertua dulu, sehingga antrean tidak pernah mencapai bacaan laut. Node A tidak pernah terdengar oleh hub.
- Kedua node berhenti pada tegangan baterai yang sama (sekitar 4,03 V). Dugaan sementara: ambang pemutusan di firmware, bukan baterai yang benar-benar kosong.

## Penyelamatan data (24 November)

- Isi flash ketiga board disalin tanpa menjalankan firmware, ditambah berkas log dari kartu microSD hub. Salinan disimpan privat, karena salinan hub memuat kredensial perangkat.
- Hub sempat tidak bisa dibaca lewat USB sampai semua modulnya dilepas; salah satu modul mengganggu jalur serial. Modul mana belum dipastikan.
- Waktu bacaan direkonstruksi karena jam node mulai dari nol setiap boot. Untuk Node B, waktunya dihitung dari penghitung antrean yang tercatat di log hub. Untuk Node A, patokannya hanya akhir log USB, jadi waktunya lebih kasar.
- **Unggahan rescue:** 53 bacaan laut (4 dari Node A, 49 dari Node B, 13 November 13:21 WIB sampai 14 November 14:04 WIB) dan 34 catatan kesehatan hub. Pengguna menetapkan batas masuk air pukul 13:15 WIB. Semua bacaan laut ditandai **perlu verifikasi** oleh QC server, karena waktunya hasil rekonstruksi dan datang terlambat.

## Yang belum

- Data rescue belum tampil di app iOS. Build app sekarang hanya meminta tujuh hari terakhir dan hanya menampilkan data yang sudah diterima QC. Pengguna mengusulkan menampilkannya lewat riwayat kalender laporan.
- Satu node disiapkan untuk demo 25 November lewat kabel USB ke komputer, terpisah dari data lapangan. Ini **bukan** data laut.
- Analisis crash yang tercatat di Node A, modul yang mengganggu serial hub, dan ambang baterai belum dikerjakan.

## Batas bukti

- Bacaan laut yang masuk hanya mencakup sekitar satu hari, dari satu lokasi, dengan waktu hasil rekonstruksi. Data ini belum cukup untuk menilai pola suhu, apalagi hubungan dengan ice-ice.
- Server belum punya laporan ice-ice untuk 13 sampai 14 November; laporan paling awal tercatat 16 November.

## Pekerjaan berikutnya

1. Daya: cari tahu mengapa ketiga perangkat berhenti di ambang baterai dalam satu sampai dua hari, dan apakah ambang firmware perlu diubah.
2. Radio: antrean node harus mengirim bacaan terbaru lebih dulu, supaya bacaan meja lama tidak menghalangi data laut.
3. Firmware v3 (log internal, jalur servis, perintah jarak jauh) dan solder wajib sebelum penempatan berikutnya. Tanggal penempatan berikutnya belum ditetapkan.
4. Tampilkan data rescue di app dengan label "perlu verifikasi", tanpa mengubah status QC di server.
