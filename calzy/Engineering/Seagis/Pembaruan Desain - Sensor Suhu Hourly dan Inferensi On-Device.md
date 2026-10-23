---
type: design-update
project: "[[Challenge Final]]"
created: 2026-10-21
updated: 2026-10-21
status: concept-not-validated
tags: [challenge-final, seagis, iot, suhu, machine-learning]
---

# Pembaruan Desain - Sensor Suhu Hourly dan Inferensi On-Device

Sumber: keputusan arah tim yang disampaikan langsung oleh pengguna dalam chat pada **21 Oktober 2026**, lalu diminta untuk dicatat. Ini pembaruan desain setelah konsolidasi [[Konteks Progres Seagis - 21 Oktober 2026]], bukan bukti implementasi hardware, backend, atau model.

## Arah yang dikonfirmasi pengguna

- Tim melanjutkan dengan **sensor suhu saja**; salinitas tidak termasuk parameter sensor pada arah desain ini.
- **Alasan perubahan besar desain:** menurut klarifikasi pengguna, sensor salinitas yang dapat diperoleh tim terkendala **harga dan kualitas pengukurannya**. Karena itu tim menyederhanakan rencana menjadi pemantauan suhu. Ini alasan keputusan tim, bukan klaim bahwa semua sensor salinitas tidak akurat atau terlalu mahal.
- **Satu sensor per tambak**, ditinggalkan di lokasi untuk merekam suhu **setiap jam (hourly)**.
- Data sensor dikirim ke **receiver berbasis ESP32**, masih konsep sementara. Pengguna menulis “EPS32”; catatan menggunakan ESP32 sesuai konteks percakapan.
- Receiver direncanakan memakai **kartu SIM untuk akses internet**, lalu mengirim data hourly ke server backend.
- Data dari backend digunakan oleh aplikasi. Model ML untuk **forecast dan classifier (nantinya)** disimpan di dalam aplikasi untuk pemrosesan **on-device**.

Alur konsep: **sensor suhu menetap → receiver ESP32 + konektivitas seluler → backend → aplikasi dengan inferensi model lokal**.

Istilah “tambak” mengikuti pesan pengguna; belum menjadi konfirmasi perpindahan dari budidaya laut Pulau Tidung ke tambak darat. Jumlah receiver dan hubungan satu receiver dengan satu/beberapa tambak belum ditetapkan. Model/jenis sensor belum dipilih; pembahasan BLE-9909 sebelumnya bukan keputusan menggunakan alat itu.

## Perubahan terhadap rancangan sebelumnya

[[Seagis_Master_Research_Context_2026-10-21]] memuat rancangan sesi suhu/salinitas 24 jam, sensor diambil lalu disinkronkan, dengan transmisi otomatis pada tahap berikutnya. **Arah terbaru mengganti konsep pengumpulan tersebut dengan sensor suhu menetap dan alur pengiriman hourly.** Arsip master dipertahankan sebagai riwayat; penamaan ulang tahap V1–V3 belum diputuskan.

[[Rencana Pengukuran IoT Kondisi Laut - Diskusi Mas Ricky]] tetap menyimpan alternatif dari diskusi mentor, bukan spesifikasi hardware yang kini telah dipilih. Forecast/classifier dan inferensi on-device adalah rencana; belum dilatih, diintegrasikan, atau divalidasi melalui pembaruan ini.

## Usulan engineering dari pembahasan — belum keputusan tim

- Receiver memerlukan modem seluler yang sesuai untuk menggunakan kartu SIM.
- Rekaman sebaiknya memiliki identitas sensor/lokasi, suhu beserta satuan, waktu pengukuran dan waktu penerimaan. Penyimpanan lokal serta retry diusulkan agar gangguan jaringan tidak langsung menghilangkan data.
- Bedakan interval pengukuran, penyimpanan, dan pengiriman. Target pengguna adalah data hourly; belum ditentukan apakah satu bacaan tiap jam atau agregasi sampel lebih rapat.

## Keputusan terbuka dan validasi

- [ ] Tentukan komunikasi sensor–receiver: kabel atau nirkabel, jarak dan topologi, serta jumlah tambak per receiver.
- [ ] Pilih probe, akurasi, kalibrasi/pembanding, kedalaman dan titik pemasangan. Satu titik ukur belum terbukti mewakili seluruh tambak.
- [ ] Tentukan catu daya, durasi operasi, housing, pemeliharaan dan ketahanan perendaman.
- [ ] Rancang penyimpanan, sinkronisasi waktu, penanganan data hilang/lama, retry dan pengiriman ulang tanpa duplikasi.
- [ ] Tetapkan modem/operator serta uji jangkauan jaringan di lokasi.
- [ ] Definisikan target dan horizon forecast serta kelas/label classifier; pengguna belum menetapkan rincian ini.
- [ ] Tentukan lokasi training dan distribusi/versi model. Inferensi direncanakan di app; mekanisme pengambilan data dan operasi ketika app tidak aktif belum ditentukan.

**Batas interpretasi:** pencatatan suhu, prakiraan suhu, klasifikasi kondisi lingkungan, dan prediksi/diagnosis ice-ice adalah target berbeda. Suhu saja belum dibuktikan cukup untuk klasifikasi ice-ice. Jika classifier ditujukan pada outcome biologis, label lapangan dan evaluasi yang sesuai tetap diperlukan. Ini batas riset, bukan perubahan atas keputusan tim menggunakan sensor suhu.

## Navigasi

[[Indeks - Engineering]] · [[Konteks Progres Seagis - 21 Oktober 2026]] · [[Challenge Final]]
