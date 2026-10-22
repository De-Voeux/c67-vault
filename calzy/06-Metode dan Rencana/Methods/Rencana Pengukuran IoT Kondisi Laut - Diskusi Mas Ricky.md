---
type: research-plan
project: "[[Challenge Final]]"
imported: 2026-10-15
status: discussion-notes
tags: [challenge-final, iot, mentoring]
---

# Rencana Pengukuran IoT Kondisi Laut - Diskusi Mas Ricky

Sumber: [[Diskusi - Mas Ricky (Mentoring IoT dan Pengukuran Kondisi Laut)]], bersama [[Mas Ricky]]. **Status: alternatif pengukuran yang dibahas; belum spesifikasi implementasi atau hasil validasi.**

## Peta kebutuhan pengukuran

| Target | Opsi dalam diskusi | Hal yang belum jelas |
|---|---|---|
| Salinitas | Sensor EC dengan suhu; contoh kedalaman 1 m | Besaran keluaran, kompensasi suhu, rentang air laut, kalibrasi, ketahanan perendaman; hubungan panas–salinitas dalam diskusi belum diverifikasi |
| Suhu air | Sensor gabungan atau bersebelahan | Kedalaman representatif tanaman, akurasi, frekuensi dan pembanding manual |
| Gelombang/gerak pelampung | Akselerometer 3D pada pelampung | Besaran turunan yang dibutuhkan, sampling, pengaruh tambatan, kalibrasi; belum ukuran arus |
| Kecepatan arus | Paddle/baling-baling sebagai alternatif | Kompleksitas mekanis, arah arus, fouling dan perawatan; bukan otomatis keluaran akselerometer |
| UV/cahaya | Sensor dengan rentang panjang gelombang sesuai; opsi di atas permukaan | UV-A/UV-B atau besaran cahaya lain; perbedaan pengukuran di udara dan kedalaman tanaman |

## Dua alternatif pengumpulan data

1. **Node menetap:** sensor → LoRa → stasiun darat → seluler → aplikasi. Panel surya dan baterai dibahas untuk daya; contoh 5–10 node, belum keputusan.
2. **Alat dibawa petani:** sensor + Arduino + baterai → simpan lokal → ambil data setelah kembali. Cara transfer akhir belum dipilih.

Keduanya perlu dinilai berdasarkan kebutuhan data dan rutinitas pengguna. Diskusi tidak menetapkan bahwa data real-time wajib atau satu titik ukur mewakili seluruh plot.

## Pertanyaan tindak lanjut

- [ ] Tentukan keputusan/pertanyaan riset yang membutuhkan tiap parameter dan definisi besarannya.
- [ ] Jelaskan pengukuran manual pembanding sebelum otomatisasi.
- [ ] Pisahkan gelombang, arus, UV dan paparan cahaya tanaman sebagai target yang berbeda.
- [ ] Tentukan lokasi/kedalaman, durasi observasi, frekuensi sampling dan pengiriman.
- [ ] Bandingkan penggunaan alat portabel dengan stasiun menetap berdasarkan rutinitas petani/penyuluh.
- [ ] Hitung kebutuhan energi sensor, controller, radio/modem; lanjutkan ke kapasitas baterai dan panel.
- [ ] Tentukan uji housing, akses perawatan dan paparan air laut/matahari.
- [ ] Telusuri *mental model* yang dimaksud dan konteks masukan Kak Keke bila diperlukan.

Daftar ini mencatat pekerjaan terbuka dari diskusi; belum dijalankan dalam import.

## Terhubung ke riset

[[Empat Variabel Lingkungan dan Batas Kuantifikasi Ice-Ice]] · [[Field Kit Kunjungan Pulau Tidung]] · [[Penginderaan Jauh dan SIG Pesisir]] · [[Data Lingkungan ke Tindakan]]. Pengukuran kondisi laut belum merupakan diagnosis atau prediksi ice-ice tervalidasi.


## Navigasi kategori

[[Indeks - Metode dan Rencana]] · [[Peta Catatan - Challenge Final]]


## Masukan Professor Roleda — diimpor 20 Oktober 2026

[[Diskusi - Professor Roleda (Ice-Ice, Threshold, dan Validasi Lapangan)]] menambahkan konteks conductivity/cahaya, efek nutrisi, jeda paparan–gejala dan logbook biologis. Ini penuturan dalam ringkasan meeting, bukan pemilihan sensor atau pengesahan cutoff; lihat juga [[Tiga Paper Baru - Implikasi Pengukuran IoT 2026-10-20]].
