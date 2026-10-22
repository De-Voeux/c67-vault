---
type: project
status: active
started: 2026-09-29
tags: [type/project, status/active, challenge-final, akuakultur]
---

# Challenge Final

## Pembaruan arah desain — 21 Oktober 2026

[[Pembaruan Desain - Sensor Suhu Hourly dan Inferensi On-Device]] — keputusan terbaru tim: **sensor suhu saja, satu per tambak dan ditinggalkan untuk pencatatan hourly**. Data mengalir ke receiver ESP32 (konsep sementara) dengan konektivitas seluler/SIM, lalu backend dan aplikasi. Model forecast serta classifier nantinya berada di app untuk inferensi on-device. Perubahan besar ke suhu saja didorong keterbatasan harga dan kualitas pengukuran sensor salinitas yang dapat diperoleh tim. Menggantikan konsep sesi suhu/salinitas yang diambil kembali untuk sinkronisasi; belum implementasi hardware atau prediksi ice-ice tervalidasi.

## Konteks progres terbaru — 21 Oktober 2026

[[Konteks Progres Seagis - 21 Oktober 2026]] — konteks terkonsolidasi terbaru: assessment perubahan lingkungan untuk penyuluh Pulau Tidung, hasil audit Copernicus, kontrak data, roadmap V1–V3, hipotesis transfer learning coral–seaweed dan pekerjaan yang belum selesai. V1 dalam master berupa laporan setelah sesi sensor 24 jam; belum sistem prediksi ice-ice tervalidasi atau bukti bahwa seluruh rancangan telah diimplementasikan.

Sumber lengkap: [[Seagis_Master_Research_Context_2026-10-21]] · asal, checksum dan batas verifikasi: [[Provenance Import Konteks Seagis 2026-10-21]]. Snapshot implementasi POC 19 Oktober dan konteks 14 Oktober di bawah dipertahankan sebagai riwayat.

## Progres implementasi POC — 19 Oktober 2026

TidungMonitor sudah mempunyai alur native iOS peta → lahan → Inspeksi, data ocean NASA terverifikasi pada sampel terbatas, serta pipeline Python satu command. Snapshot bundle: 33 record valid dari 17 granule unik yang diparsing; belum model penyakit atau validasi kondisi farm. Eksperimen solar sebelumnya telah diarsipkan dari target app aktif.

- [[Riwayat Pengembangan POC - TidungMonitor]] — keputusan, arsitektur, perubahan scope, hasil data/test dan pekerjaan yang masih terbuka.
- [[Panduan Fetch Data Ocean - TidungMonitor]] — instruksi pemakaian fetch, update bundle, backup dan troubleshooting.
- [[Arsip Pengembangan TidungMonitor - 19 Oktober 2026]] — brief dan wireframe sumber.

## Challenge Response tim — 14 Oktober 2026

[[Challenge Response - Seaweed Ice-Ice]] — proposal saat ini: membantu community advocates dalam budidaya rumput laut mengenali peringatan lingkungan awal terkait ice-ice dan membuat keputusan tanam, dengan data satelit, cuaca, serta IoT; menggunakan MapKit dan Core ML pada iOS. Wording asli tersimpan di catatan tersebut.

## Konteks riset terkonsolidasi — 14 Oktober 2026

[[Konteks Riset Rumput Laut - 14 Oktober 2026]] — indeks konteks percakapan 3–14 Oktober: laporan lapangan, empat variabel lingkungan, batas kuantifikasi, register paper, keterbatasan data satelit, ide produk, dan agenda riset. Lampiran diarsipkan utuh; pemetaan PDF yang berbeda dari matriks bukti dicatat eksplisit.

## Challenge

> Help Aquaculture Farmers in improving production.

Brief ini masih luas. Percakapan riset pada [chat yang dibagikan](https://chatgpt.com/share/6abcc469-3808-83ec-a644-fd8bf05939e6) mengerucut ke **budidaya rumput laut di Kepulauan Seribu**, terutama hubungan antara kondisi perairan, cuaca, kerentanan bibit, keputusan pembudidaya, dan hasil satu siklus. Ini **arah eksplorasi**, belum problem statement atau solusi yang divalidasi.

## Mulai dari sini

- [[Peta Lingkungan]] — peta dasar lingkungan alami, buatan, dan sosial budaya dari sketsa awal.
- [[Framing Produksi Akuakultur]] — segmen, kemungkinan masalah, dan arti “improving”.
- [[Rumput Laut Kepulauan Seribu]] — bukti lokal, pembanding daerah lain, dan batas klaim iklim.
- [[Siklus dan Titik Rawan Budidaya]] — sembilan tahap dan perbedaan risiko menurut tahap.
- [[Strategi Pembudidaya]] — cara keputusan dibuat, pilihan adaptasi, dan celah informasi.
- [[Guiding Questions Akuakultur]] — pertanyaan untuk memperluas pemahaman topik, bukan skrip wawancara.
- [[Register Sumber Akuakultur]] — asal klaim dan tautan yang disebut dalam chat.

## Interview masuk — 30 September 2026

- [[Interview - Ganesha Danu Enastika (eFishery)]] — perspektif sistem internal eFishery, pakan/feeder, akses pasar dan modal kerja, serta adopsi teknologi. Konteks terutama lele dan sebagian udang; belum memvalidasi masalah rumput laut Kepulauan Seribu.
- Narasumber: [[Ganesha Danu Enastika]] · Organisasi: [[eFishery]]. Klaim/opini dalam interview belum diverifikasi secara independen.
- Indeks riset: [[MOC - Challenge Final]].

## Posisi riset — diperbarui 21 Oktober 2026

Fokus saat ini adalah rumput laut Pulau Tidung, perubahan kondisi perairan dekat pantai, dan hubungan dengan gejala ice-ice. Suhu, salinitas, cahaya dan sirkulasi merupakan variabel prioritas; mekanisme kejadian setempat belum terkonfirmasi. Ambang universal, bobot kontribusi kausal, dan probabilitas penyakit belum ditetapkan.

Arah terbaru dan prioritas tindak lanjut berada di [[Konteks Progres Seagis - 21 Oktober 2026]]: mulai dari assessment lingkungan, bangun transmisi/peringatan pada V2, dan uji prediksi biologis hanya setelah label serta validasi tersedia. [[Sintesis Penyebab Ice-Ice]] dan [[Matriks Bukti Ice-Ice]] menyimpan bukti PDF; [[Konteks Riset Rumput Laut - 14 Oktober 2026]] menyimpan konteks percakapan terdahulu. Proposal tim berada di [[Challenge Response - Seaweed Ice-Ice]]. Wawancara ikan/udang dan tambak Bekasi dipertahankan sebagai pembanding, bukan bukti langsung untuk Tidung.

## Langkah riset berikutnya

- [ ] Pastikan segmen dan sistem: lokasi, jenis rumput laut, metode tali/patok, skala usaha, serta siapa yang membuat keputusan.
- [ ] Petakan satu siklus nyata dari bibit sampai penjualan; bedakan tahapan, kejadian, dan keputusan.
- [ ] Sebagai awal eksplorasi, temui sekitar 5–8 pembudidaya dari segmen yang sama (termasuk yang berhasil dan pernah rugi); cocokkan cerita dengan penyuluh/teknisi, pemasok bibit, dan pembeli bila relevan. Ini bukan sampel representatif wilayah.
- [ ] Bandingkan catatan hasil 2–3 siklus bila tersedia: bibit awal, kehilangan, hasil basah/kering, mutu, biaya, harga, dan cuaca/air.
- [ ] Bedakan **gejala → dugaan pelaku → bukti pengukuran → penjelasan alternatif** untuk tiap kejadian.
- [ ] Pilih satu masalah berdasarkan dampak, pengulangan, kemampuan pembudidaya bertindak, dan kemampuan tim mengukur perbaikan.

## Research dump diproses — 1 Oktober 2026

- [[Ekosistem dan Segmen Akuakultur]] — komoditas/sistem, pelaku, rantai pasok, dan pemilihan segmen.
- [[Hipotesis Peringatan Dini Kesehatan Budidaya]] — hipotesis kondisi lingkungan, kehilangan, dan kemungkinan tindakan; belum tervalidasi.
- [[Data Lingkungan ke Tindakan]] — kerangka data, keputusan, kemampuan, serta koordinasi.
- [[Register Klaim Research Dump]] — klaim/angka/tautan yang belum diverifikasi.
- Arsip: [[2026-10-01 Research Dump - Akuakultur, Lingkungan, dan NASA]]. GQ, framing, strategi, dan register sumber yang sudah ada turut diperbarui.

## Interview masuk — 2 Oktober 2026

- [[Interview - Maulidya Shalia (Penginderaan Jauh dan SIG)]] — pengalaman penginderaan jauh dan SIG pesisir. Membantu memeriksa cakupan sensor, validasi, serta hubungan peta dengan keputusan; belum memvalidasi kebutuhan pembudidaya atau prediksi penyakit.
- Catatan metode: [[Penginderaan Jauh dan SIG Pesisir]].

## Perspektif pembudidaya — Pak Madnung (Pak Nunung), Samudrajaya

[[Interview - Pak Madnung (Rumput Laut Tambak Bekasi)]] menambah konteks **rumput laut tambak darat Bekasi**, berbeda dari sistem budidaya laut yang sebelumnya dieksplorasi. Kendala yang paling beliau tekankan adalah harga/pemasaran, bukan permintaan alat peringatan dini. Ini sinyal untuk menelusuri hasil layak jual, penyerapan pasar, dan margin bersama kehilangan biologis; belum diagnosis seluruh pembudidaya atau keputusan solusi. Lihat [[Rumput Laut Tambak Bekasi]].

**Pak Madnung dan Pak Nunung adalah orang yang sama**, dikonfirmasi pengguna pada 8 Oktober 2026. Catatan chat yang diimpor 2 Oktober dan rangkuman dua rekaman Samudrajaya yang diimpor 7 Oktober disatukan dalam catatan interview tersebut. Rangkuman rekaman memuat timestamp, praktik tambak, ekonomi panen, fungsi pengepul, pengolahan, serta aspirasi kelompok petani. Pembeli masih ada, tetapi harga rendah mengurangi alasan untuk memanen. Transkrip otomatis belum diperiksa dengan mendengarkan; tanggal kunjungan dan angka penting masih perlu dikonfirmasi. Kedua materi ini adalah sumber dari satu narasumber, bukan dua kesaksian independen.

## Related

- [[Peta Lingkungan]]
- [[Framing Produksi Akuakultur]]
- [[Rumput Laut Kepulauan Seribu]]

## Materi tambahan — diimpor 7 Oktober 2026

- [[Interview - Pak Dahlan (Rumput Laut Pulau Tidung)]] — usaha musiman, siklus tali, modal, penampungan dan penahanan stok, diversifikasi, regenerasi, serta hubungan dengan peneliti. Dua lampiran identik menjadi satu catatan; nama dan tanggal wawancara belum tersedia.
- [[Interview - Pak Unin (Rumput Laut dan Akses Pembeli)]] — sumber mencantumkan rekaman 6 Oktober 2026; petani paruh waktu sekaligus pemulung. Penampung rutin sulit ditemukan, sementara pesanan lokal kecil masih ada. Gejala “air kotor” dan pemutihan dicatat terpisah dari dugaan diagnosis maupun hipotesis satelit tim.
- [[Panel ISF - Blue Economy, Hilirisasi, dan Pembiayaan]] — perspektif industri, kebijakan, kemitraan, dan pembiayaan: pasokan bermutu/konsisten, pembeli, pengolahan, serta kesiapan usaha. Koreksi afiliasi Babcock dipertahankan; angka/program belum diverifikasi dan kebutuhan metrik bank belum terjawab.

Perbandingan awal: **Samudrajaya menekankan harga yang tidak sebanding dengan pekerjaan; Pak Unin menekankan akses penampung; pelaku usaha Tidung menggambarkan kemampuan menahan stok dan diversifikasi; panel ISF menekankan kesiapan rantai pasok dan pembiayaan.** Ini perspektif berbeda, belum satu masalah/solusi yang tervalidasi. Empat lampiran diarsipkan utuh di `08-Sumber dan Arsip/Sources/Arsip Import 2026-10-07/`, beserta asal dan pemeriksaan duplikat.

## Perspektif marine science dan sosial — Aryo Damar

[[Interview - Aryo Damar Sadono (Marine Science dan Masyarakat Pesisir)]] memperluas pertanyaan ke seluruh rantai pasok, insentif, modal, serta keberlanjutan manfaat bagi masyarakat pesisir. Rumput laut disebut memiliki jalur masalah penyakit, pengeringan, logistik, dan pasar; sebagian cerita bersifat anekdotal/lokasi belum pasti. [[Masyarakat Pesisir dan Rantai Pasok]] menyimpan kerangka tindak lanjut, belum keputusan masalah/solusi.

## Perspektif air tawar — Nico Jaya

[[Interview - Nico Jaya (Pembibitan Ikan Air Tawar)]] menambahkan jalur pembibitan, pengelolaan air/pakan, serta penjualan langsung ke pembeli. Peran Nico dan lingkup usaha ayah/abang belum dikonfirmasi; cerita pembibitan versus ikan konsumsi juga perlu dipisahkan. [[Pembibitan Air Tawar dan Penjualan Langsung]] menyimpan pertanyaan tentang biaya, hasil, dan fungsi distribusi perantara. Ini belum pemilihan segmen atau rekomendasi praktik budidaya.

## Rencana riset rumput laut — 2 Oktober 2026

- [[Guiding Questions Rumput Laut per Aktivitas]] — pertanyaan dalam 10 cluster, dipasangkan dengan desk research, interview, dan observation; bukan hasil interview.
- [[Rencana Desk Research Rumput Laut Pulau Tidung]] — **prioritas desk research sebelum interview lanjutan**, dengan enam tujuan: market, sains/lingkungan, crop health, remote monitoring, solusi yang ada, serta prevention/treatment. Status masih rencana.


## Perspektif penyuluh Pulau Tidung — diimpor 5 Oktober 2026

- [[Interview - Fauzi (Penyuluh Rumput Laut Pulau Tidung)]] — riwayat budidaya, patok dasar, stok bibit, rescue berparanet, pasar, serta kendala biaya/ruang.
- [[Fauzi]] · [[Pak Dahlan]] · [[Dinas KKP Jakarta]] — konteks narasumber, pelaku yang diceritakan, dan label afiliasi yang perlu dikonfirmasi.
- Sinyal riset: tindakan rescue sudah ada, tetapi waktu respons dan kapasitasnya perlu ditelusuri bersama kebutuhan volume pasar. Catatan belum menetapkan penyebab kematian atau memilih solusi peringatan dini.

## Identifikasi air busuk — brief 5 Oktober 2026

- [[Air Busuk Pulau Tidung - Hipotesis dan Langkah Identifikasi]] — bukti lokal, lima kandidat mekanisme, serta urutan tindak lanjut sebelum memilih data/sensor/solusi.

## Strategi KKP dari podcast AQUA — diimpor 5 Oktober 2026

- [[Strategi KKP untuk Budidaya Rumput Laut Indonesia]] — sumber bibit unggul melalui UPT/laboratorium, perbanyakan lewat kebun bibit pemda/swasta, peningkatan produksi kampung budidaya, serta modeling sekitar 50 ha yang dikelola koperasi. Intervensi modeling yang dijelaskan sampai pengeringan; hilirisasi industri menjadi arah lebih luas.
- Relevansi Tidung: hubungkan akses dan kontinuitas bibit dengan rescue, mutu hasil, serta kecocokan volume pasar. Program/angka adalah penuturan Nono Hartanto dalam podcast yang tanggalnya belum tersedia; bukan konfirmasi kebijakan terkini.

## Perspektif budidaya udang dan limbah — diimpor 8 Oktober 2026

- [[Interview - Narasumber KKP (Budidaya Udang dan Pengolahan Limbah)]] — pendidikan akuakultur dan PKL udang vaname; kualitas air, kerja teknisi, contoh panen, limbah, serta biaya/lahan IPAL. Nama dan tanggal wawancara belum disebutkan; teks lampiran dipertahankan utuh.
- [[Limbah Budidaya, Biosecurity, dan IPAL]] — alur air masuk/keluar dan pertanyaan kelayakan pengolahan. Pengamatan air hijau kekuningan dekat tambak belum terhubung dengan air busuk Tidung atau diagnosis ice-ice.
- [[Kementerian Kelautan dan Perikanan]] — afiliasi menurut sumber. KNMP/tengkulak dibahas dalam konteks nelayan tangkap; status program dan angka lokasi adalah penuturan saat wawancara, bukan kebijakan terkini yang diverifikasi.


## Navigasi seluruh catatan

[[Peta Catatan - Challenge Final]] · [[Indeks - Navigasi]]


## Mentoring IoT — diimpor 15 Oktober 2026

[[Diskusi - Mas Ricky (Mentoring IoT dan Pengukuran Kondisi Laut)]] dengan [[Mas Ricky]], mentor [[Apple Developer Academy UC Surabaya]]. Pembahasan memusatkan kebutuhan data sebelum sensor, alternatif alat portabel versus node LoRa, serta energi/housing. Tanggal pertemuan belum disebutkan; keputusan dan klaim teknis belum tervalidasi. Rencana pencatatan: [[Rencana Pengukuran IoT Kondisi Laut - Diskusi Mas Ricky]].


## Diskusi Professor Roleda — diimpor 20 Oktober 2026

[[Diskusi - Professor Roleda (Ice-Ice, Threshold, dan Validasi Lapangan)]] bersama [[Michael Y. Roleda]] menekankan interaksi suhu/salinitas dengan nutrisi, cahaya dan kondisi tanaman; time series lingkungan perlu dipasangkan dengan observasi biologis. Rentang angka dalam meeting dicatat bersyarat, bukan pengesahan threshold alarm. Lokasi, nama tim dan afiliasi Academy telah dikoreksi pengguna; istilah lainnya dibiarkan sebagaimana dicatat. Sumber utuh diarsipkan.
