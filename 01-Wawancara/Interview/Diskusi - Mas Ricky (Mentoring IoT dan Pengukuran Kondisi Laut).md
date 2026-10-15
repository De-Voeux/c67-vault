---
type: interview
project: "[[Challenge Final]]"
imported: 2026-10-15
status: discussion-notes
tags: [challenge-final, iot, mentoring]
---

# Diskusi - Mas Ricky (Mentoring IoT dan Pengukuran Kondisi Laut)

## Asal dan batas catatan

Catatan diskusi dengan [[Mas Ricky]], **Mentor Apple Developer Academy UC Surabaya**, menurut keterangan pengguna. Tanggal diskusi belum disebutkan; 15 Oktober 2026 adalah tanggal import. Lampiran berupa poin diskusi, bukan transkrip verbatim. Nama lengkap dan rincian afiliasi belum tersedia. Karena pergantian pembicara tidak ditandai, pemisahan pertanyaan tim dan saran mentor di bawah mengikuti konteks kalimat, bukan atribusi kutipan pasti.

Sumber utuh dan checksum: [[Provenance Diskusi Mas Ricky - 15 Oktober 2026]]. Penjelasan teknis dan biologis dalam diskusi belum diverifikasi secara independen.

## Konteks yang dibawa tim

- Tim membingkai pekerjaan berat petani/penyuluh sebagai menjaga agar ice-ice tidak menyebar. Ini framing diskusi tim; belum hasil validasi beban kerja atau diagnosis kejadian lapangan.
- Sasaran pengamatan adalah **kondisi laut**, bukan pengamatan langsung seaweed.
- Parameter yang disebut: salinitas, suhu, ombak/arus, dan paparan sinar matahari/UV. Istilah-istilah tersebut masih perlu didefinisikan sebagai besaran pengukuran.
- Tim mempertimbangkan satu sensor yang dipakai untuk pengecekan berkala. Lampiran menyebut dua opsi dan kecenderungan ke opsi kedua, tetapi tidak menjabarkan pasangan opsi itu secara lengkap; jangan menetapkannya sebagai keputusan final.
- Kekhawatiran: transfer data ke aplikasi, kebutuhan internet atau kedekatan Bluetooth, daya baterai, serta paparan korosif air laut.

## Saran dan opsi teknis yang tercatat

### Salinitas dan suhu

EC (*electrical conductivity*) dibahas sebagai jalur pengukuran salinitas; rentang dan kualitas sensor beragam. Diskusi menekankan alat yang dapat terpapar air laut terus-menerus dan menyebut model ujung seperti kaca, tanpa model/produk yang teridentifikasi. Suhu dapat diukur bersama atau berdekatan dengan sensor salinitas. Rentang suhu ekstrem seperti minus hingga mendidih dianggap tidak perlu untuk skenario ini.

Contoh penempatan yang disebut adalah sekitar **1 m di bawah permukaan**, sebagai opsi pemasangan, bukan kedalaman tervalidasi. Klaim dalam lampiran bahwa air makin panas berarti salinitas meningkat disimpan sebagai pernyataan diskusi yang perlu diperiksa; belum dipakai sebagai aturan konversi atau hubungan sebab-akibat.

### Ombak, gerakan pelampung dan arus

- Opsi akselerometer 3D pada pelampung untuk merekam gerak naik-turun/intensitas gelombang, disebut sebagai opsi murah dalam diskusi; belum ada perbandingan biaya.
- Alternatif paddle/baling-baling untuk aliran air dibahas dengan beban mekanis yang lebih berat.
- Sensor pada pelampung dianggap lebih mudah dirakit. Pengamatan ombak disebut perlu menyala terus; kebutuhan sampling aktual belum dihitung.
- Diskusi mengaitkan sirkulasi dengan pasokan nutrien/oksigen dan kondisi pertumbuhan, serta stagnasi dengan ice-ice. Hubungan lokal dan besarnya pengaruh belum diuji.

Catatan metodologis: lampiran bergeser antara ombak dan kecepatan arus. Belum ada kalibrasi yang membenarkan keluaran akselerometer sebagai ukuran kecepatan arus; kedua target pengukuran dicatat terpisah dalam [[Rencana Pengukuran IoT Kondisi Laut - Diskusi Mas Ricky]].

### Cahaya dan UV

Mentoring mengangkat kebutuhan menentukan UV-A/UV-B atau rentang panjang gelombang yang relevan sebelum memilih sensor. Opsi pemasangan sensor di atas permukaan disebut. Paparan matahari, UV dan cahaya di kedalaman tanam belum dijadikan satu definisi pengukuran.

### Komunikasi dan daya

**Opsi stasiun mandiri:** node sensor memakai panel surya dan baterai backup; LoRa mengirim ke receiver/stasiun darat, lalu koneksi seluler meneruskan data. Contoh skala 5–10 sensor/node dibicarakan, bukan jumlah yang sudah dipilih. Stasiun darat dapat memakai listrik kabel, atau baterai dan panel surya; pemasangan tinggi dibahas, termasuk contoh di atas pohon, tanpa survei lokasi/jangkauan.

**Opsi alat dibawa petani:** sensor, Arduino, baterai dan penyimpanan lokal; data diambil setelah kembali ke darat. Opsi ini dibahas tanpa keharusan LoRa/panel surya sebagai percobaan kelayakan awal. Metode transfer data akhir belum ditentukan.

Interval 30 detik atau 1 menit disebut sebagai contoh. Kebutuhan daya sensor, Arduino dan radio/modem perlu dihitung terhadap lama operasi, sampling dan pengiriman sebelum memilih kapasitas baterai serta panel. Tidak ada anggaran energi atau kapasitas final dalam lampiran.

### Housing

Pipa paralon/PVC dan lem yang baik disebut sebagai bahan murah untuk percobaan. Setelah uji awal, housing perlu mempertimbangkan akses buka-tutup, air laut dan sinar matahari. Belum ada spesifikasi kedap air, ketahanan korosi, umur pakai atau hasil uji deployment.

## Inti mentoring dan hal yang belum diputuskan

Mulai dari satu titik, tentukan data yang diperlukan, dan jelaskan cara mengukurnya secara manual terlebih dahulu; IoT membantu pengambilan data. Lampiran menyebut *mental model* dan kemungkinan meminta masukan Kak Keke. Ini tindak lanjut yang disebut dalam diskusi, bukan kontak yang sudah dilakukan.

Belum ada keputusan sensor, pemasok, harga, jumlah node, kedalaman final, LoRa vs alat portabel, interval sampling, atau rancangan daya. “Good starting point” dan kelayakan yang dibicarakan adalah umpan balik mentoring, bukan validasi ilmiah atau keberhasilan prototipe.

## Terkait

- [[Rencana Pengukuran IoT Kondisi Laut - Diskusi Mas Ricky]] — parameter, alternatif arsitektur dan pertanyaan tindak lanjut.
- [[Empat Variabel Lingkungan dan Batas Kuantifikasi Ice-Ice]]
- [[Data Pengamatan Bumi dan Eksplorasi Produk Rumput Laut]]
- [[Field Kit Kunjungan Pulau Tidung]]
- [[Air Busuk Pulau Tidung - Hipotesis dan Langkah Identifikasi]]
- [[Challenge Response - Seaweed Ice-Ice]]


## Navigasi kategori

[[Indeks - Wawancara]] · [[Peta Catatan - Challenge Final]]
