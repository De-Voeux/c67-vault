---
type: project-status
created: 2026-11-06
updated: 2026-11-06
status: current-working-context
supersedes: "[[Status PoC IoT Suhu SEAGIS - 5 November 2026]]"
tags: [radit, iot, lora, suhu, poc]
---

# Status PoC IoT Suhu SEAGIS — 6 November 2026

Catatan status dari sesi kerja 5 November malam sampai 6 November 2026, menggantikan [[Status PoC IoT Suhu SEAGIS - 5 November 2026]]. Ini status **uji meja sebagian, bukan bukti lulus uji meja penuh atau uji laut**. Jalur node → hub → server sudah berjalan otomatis di meja, tetapi uji hub dari baterai saja baru 6 menit.

Isi catatan ini adalah klaim agent dari sesi kerja (keluaran serial dan log), kecuali yang ditandai diverifikasi, pernyataan, atau hasil ukur pengguna.

## Posisi terakhir

Hub menerima paket dua node lewat LoRa dan mengunggahnya ke server lewat SIM800L. Uji 30 menit dengan hub murni dari baterai (S1) dimulai malam hari, tetapi dihentikan di menit ke-5 karena hub tidak mendapat daya dari baterai (CUTOFF). Pengguna lalu mengatakan semuanya normal dan hub kini dari baterai; hasil akhirnya belum tercatat.

## Yang berubah sejak 5 November

- **Upload lewat SIM800L berhasil.** Koreksi atas catatan 5 November ("belum pernah jalan"). Penyebab TLS gagal: driver salah membaca respons `CIPRXGET`. APN operator juga butuh user dan sandi bawaan operator, dan `CGATT` harus menunggu registrasi data. Sinyal ikut naik saat uji berhasil pertama, jadi pengaruh sinyal lemah (kondisi lapangan) belum terpisahkan.
- **Node A dan B dirakit dengan DevKit** dan memakai firmware yang sama dengan hub; peran dipilih lewat perintah. Satu DevKit rusak (flash tidak terbaca) dan tidak dipakai.
- **Radio dua arah node ↔ hub terbukti di jarak meja**: hub dari baterai membalas ACK ke kedua node. Jarak sekitar 100 m dan posisi antena di air belum diuji.
- **Node A dari baterai** mengirim stabil selama lima dan sekitar dua puluh menit (antrean node kosong saat dibaca lagi lewat USB).
- **Unggah hub macet** pada koneksi kedua dalam satu sesi modem. Solusi yang terbukti bekerja: restart radio modem di antara potongan, kirim tanpa menunggu konfirmasi per potongan, ulang sampai tiga kali, potongan 3000 byte (diverifikasi di `config.h`). Dengan itu 20 potongan berturut-turut lolos dan backlog 200-an record habis. **Akar masalah belum diketahui.**
- **Telemetri hub sudah ada di server** (waktu unggah terakhir, baterai, status jam). Dokumen lama menyebut belum ada.
- **Halaman pemantauan live** sudah terbit di Cloudflare Pages dan menampilkan data asli. Halaman publik, tanpa Cloudflare Access. Token baca terbatas pada dua plot node PoC dan berlaku sampai 28 November 2026.
- **Dokumen uji meja** `iot/POC_BENCH_TEST.md` (diverifikasi ada) memuat sepuluh skenario S1–S10.

## Hasil uji meja

| Skenario | Hasil | Asal bukti |
|---|---|---|
| Upload SIM800L 10 dari 10 (program uji, sinyal kuat) | HTTP 201 | keluaran serial |
| LoRa node ↔ hub, hub dari baterai | ACK diterima kedua node | keluaran serial |
| Node A dari baterai 5 dan sekitar 20 menit | antrean node kosong | keluaran serial |
| S1 hub dari baterai, 6 menit (bukan 30) | unggah terakhir berhasil, Node A dan B masing-masing 6 titik di server | pembacaan server |
| S1 penuh 30 menit | **dihentikan di menit ke-5, belum lulus** | - |
| S6 backlog dikuras | lulus di USB + baterai, 20 potongan | keluaran serial |
| S2–S5, S7–S10 | **belum dijalankan** | - |

## Batas bukti dan data uji

- **Data di server masih uji**: ditandai `simulated=true`, dengan baterai Node B palsu (penanda 5555 mV, node B masih lewat USB) dan bacaan lama dari tes. Probe belum dibandingkan di wadah yang sama; selisih sekitar 1 °C antar node dilaporkan.
- **Bacaan baterai 0 menyebabkan CUTOFF 444 mV** setiap kali saklar baterai mati, karena firmware menilai baterai dari tegangan input pembagi, bukan dari USB. Ambang `NODE_POWER` dan `HUB_POWER` masih placeholder dan belum dikalibrasi.
- **Hub tanpa jam** pernah melewatkan 27 dari 48 record pada unggah pertama; firmware tidak mengirim ulang record itu.
- **Regresi simulasi belum diulang** setelah perubahan firmware, dan firmware rilis (unggah tiap jam) belum diuji di board; board masih memakai build uji siklus 1 menit yang boros baterai.
- `xiao-node-1/depok_fw/modem.cpp` tertimpa dan belum diuji di board.
- Sinyal di meja kuat (CSQ 22–31); kondisi Pulau Tidung belum diuji.

## Pekerjaan berikutnya

1. S1 penuh (30 menit, hub dan Node A dari baterai) lalu S2–S5 satu gangguan per skenario.
2. Pasang baterai Node B, kalibrasi bacaan baterai dengan multimeter, ganti ambang placeholder.
3. Pasang firmware rilis di tiga board dan uji minimal dua siklus satu jam.
4. Ukur arus tidur hub dan node; putuskan jadwal unggah dan baterai (target 72 jam belum terbukti).
5. Cari akar masalah koneksi kedua modem; uji unggah di sinyal lemah.
6. Pilih kartu lapangan dengan adaptor asli, cek data 2G di Tidung; solder jalur daya modem dan buat housing.
7. Putuskan apakah halaman pemantauan publik diberi Cloudflare Access; naikkan batas "tertinggal" untuk jadwal satu jam.
8. Butir lama: batas EIRP 433 MHz, jalur koordinat, pembersihan record uji, perpanjangan token hub (kedaluwarsa akhir November), dan sensor nyata dari backend; `WIRING.md` dan diagram Wokwi.

## Sumber dan batas bukti

- Catatan sesi di second-brain pribadi (tidak ada di repo ini). Hasil ukur berasal dari pengguna; angka modem, radio, dan baterai node berasal dari log serial yang dilaporkan agent.
- Catatan ini sengaja tidak memuat token, ID, ref proyek, alamat MAC, nama akun, atau alamat deploy.
