---
type: knowledge-transfer
project: "[[Challenge Final]]"
created: 2026-10-15
updated: 2026-10-20
status: working-understanding
tags: [challenge-final, radit, iot, rumput-laut, ice-ice, poc, fusion]
---

# Transfer Knowledge — IoT Rumput Laut

Pemahaman Codex berdasarkan percakapan dengan Radit sampai 15 Oktober 2026, catatan kelayakan teknis yang diberikan Radit, serta percakapan Claude yang ditempelkan Radit. Catatan ini merupakan handoff untuk melanjutkan riset dan PoC; bukan spesifikasi final atau hasil validasi lapangan.

**Pembaruan keputusan per 20 Oktober 2026:** variabel inti yang dipahami Radit adalah **salinitas dan suhu air**. Alat dipasang selama **5 jam**, kemudian diangkat dan data disinkronkan ke app melalui **BLE**. Batas biaya total **Rp1–2 juta**; tim tidak memiliki alat ukur untuk dipinjam dan bersedia belajar merakit board. Rincian di bawah yang menyebut variabel atau komunikasi masih terbuka menggambarkan pembahasan hingga 15 Oktober; lihat bagian pembaruan terbaru di akhir catatan.

**Arah pada catatan 15 Oktober:** alat low budget yang merekam kondisi selama dipasang di kebun, kemudian diambil kembali untuk membaca data. Radit sudah mengonfirmasi bahwa tali rumput laut menggantung dekat permukaan dengan pelampung. Pada tanggal itu, jadwal pengambilan, metode transfer, aturan risiko, serta hardware final masih terbuka; pembaruan 20 Oktober di atas menggantikan status jadwal dan transfer.

## 1. Tujuan dan konteks

- Membantu memahami kondisi lingkungan di sekitar rumput laut dan mengeksplorasi tanda peringatan terkait ice-ice serta pertimbangan keputusan tanam.
- Empat variabel yang dibahas: suhu air, salinitas, paparan matahari, dan gerak air. Definisi pengukuran untuk dua variabel terakhir belum final.
- Lokasi yang diceritakan berupa perairan pesisir dangkal, kira-kira sedalam pinggang remaja. Itu perkiraan verbal, bukan ukuran kedalaman atau data pasang surut.
- Low budget merupakan kebutuhan eksplisit. Satu node menjadi skala kerja PoC; jumlah perangkat produksi belum ditentukan.
- App iOS menjadi konteks integrasi dalam catatan mentoring dan diskusi produk. Implementasi app/backend belum dibuat dalam sesi Codex ini.
- Pengukuran lingkungan belum sama dengan diagnosis ice-ice, probabilitas penyakit, atau rekomendasi tanam yang tervalidasi.

Dua pembuktian perlu dipisahkan: **alat mengukur dan menyimpan data dengan benar**, serta **informasinya membantu pengguna mengambil keputusan**. Keberhasilan salah satunya belum membuktikan yang lain.

## 2. Status keputusan: jangan menyamakan usulan dengan konfirmasi

| Topik | Status terbaru | Implikasi |
|---|---|---|
| Tali dekat permukaan dengan pelampung | **Dikonfirmasi Radit**, menjawab pilihan (a) Claude | Rancang pemasangan relatif terhadap lapisan tanaman dekat permukaan |
| Alat diambil-pasang | **Arah yang sangat mungkin** menurut Radit | Bedakan dari node permanen dan alat handheld yang hanya dicelup sebentar |
| Diambil setiap hari | **Belum terkunci**; Radit juga membuka durasi yang dirasa cukup untuk PoC | Durasi rekam dan kebutuhan baterai belum dapat ditetapkan |
| Bluetooth | **Masih dipertimbangkan** | Jangan menyatakan BLE sudah menjadi spesifikasi final |
| Tanpa LoRa/gateway | Usulan penyederhanaan pada rangkuman Claude; cocok dengan arah pengambilan berkala | Dua opsi komunikasi pernah diminta sebelumnya; LoRa belum dinyatakan dibatalkan secara eksplisit oleh Radit |
| Tanpa panel surya | Rekomendasi Claude untuk skenario ambil-pasang | Layak dievaluasi berdasarkan kebutuhan energi, bukan dianggap otomatis cukup |
| Aturan if-else | **Asumsi yang perlu diperiksa**, ditegaskan Radit | Jangan memakai ambang sebagai aturan risiko tervalidasi |
| Pengaruh tanggal tanam | **Belum diketahui**, ditegaskan Radit | Boleh dipertimbangkan sebagai metadata; belum dasar ranking atau skor |
| Alert harian retrospektif | Usulan produk Claude | Konsekuensi alur offline: evaluasi baru tersedia setelah sinkron, frekuensinya mengikuti pengambilan |
| Radius node di peta | Ide produk, makna belum ditetapkan | Radius bukan bukti cakupan pengukuran atau keseragaman kondisi kebun |
| Posisi dari ponsel/titik tetap, tanpa GPS node | Usulan Claude | Perlu konfirmasi alur pencatatan lokasi saat pemasangan |

**Catatan penting:** jawaban (a) Radit menjawab *posisi vertikal tali*, bukan mengonfirmasi bahwa alat akan diikat langsung ke tali. Cara memasang alat masih perlu ditentukan.

Keterangan tali mengambang ini berlaku untuk skenario yang sedang dibahas Radit. Jangan langsung menggantikan semua catatan budidaya di vault yang mungkin membahas patok dasar, blok, atau lokasi lain.

## 3. Penempatan dan arti sensor

Konsep fisik yang disarankan adalah **hybrid**: badan mengambang dengan elektronik kering; probe air terendam; sensor paparan permukaan menghadap ke atas. Ini rekomendasi desain awal, bukan satu-satunya konfigurasi yang mungkin.

| Variabel | Pendekatan awal | Penempatan | Batas interpretasi |
|---|---|---|---|
| Suhu air | Probe tahan air | Sejajar lapisan tanaman, dekat EC | Bukan suhu udara atau suhu dalam housing; akurasi dan respons perlu dibandingkan dengan alat referensi |
| Salinitas | EC + suhu, menggunakan metode konversi yang sesuai | Berdekatan dengan suhu dan terendam sesuai petunjuk probe | Perlu sensor dengan rentang air laut, kalibrasi, kompensasi suhu, serta satuan/metode yang jelas |
| Paparan matahari | Kandidat UV, lux, atau PAR; **belum dipilih** | Di atas permukaan jika yang diukur paparan datang | Bacaan permukaan belum otomatis mewakili paparan tanaman di dalam air |
| Gerak air | Kandidat IMU seperti MPU6050 | Terpasang kokoh pada badan yang gerakannya ingin direkam | Mengukur gerak badan alat; belum merupakan kecepatan arus atau tinggi ombak |

Hal yang harus dijaga dalam interpretasi:

- EC dan suhu perlu mewakili kondisi air yang sama. Kedekatan fisik membantu, tetapi perbedaan waktu respons sensor juga perlu diperhatikan.
- Tali dan alat yang sama-sama mengapung membuat pengaturan kedalaman lebih mudah; tidak menjamin jarak probe ke tanaman selalu konstan. Beban tanaman, lendutan tali, ombak, dan pengikat dapat mengubah posisi relatifnya.
- Panjang kabel/dudukan probe sebaiknya dapat disetel setelah kedalaman tali diukur. Contoh 1 meter dari mentoring dan 25–30 cm pada CAD bukan ketentuan lapangan.
- UV, lux, dan PAR mengukur hal berbeda. Cocokkan variabel dan satuannya dengan pertanyaan riset sebelum membeli sensor atau mengadopsi ambang.
- Sensor cahaya bawah air memungkinkan dengan perangkat dan koreksi yang sesuai. Penempatan di permukaan merupakan kompromi desain yang harus diberi label jelas.
- Jendela housing yang tampak bening belum tentu meneruskan UV yang hendak diukur; karakteristik bahan penutup harus diperiksa.
- Gerak akibat pengikatan, penanganan, dan tarikan tali dapat masuk ke data IMU. Gunakan istilah **indeks gerak alat pada konfigurasi pemasangan tertentu** sampai hubungannya dengan kondisi air divalidasi.
- Belum diketahui apakah tanaman/probe pernah keluar dari air saat surut terendah atau gelombang.

## 4. Pengambilan data dan komunikasi

### Arah terbaru: dipasang untuk merekam, lalu diambil

`Sensor → controller → penyimpanan lokal → alat diambil → transfer dekat ponsel → app → backend bila diperlukan`

- microSD pernah diminta Radit sebagai opsi penyimpanan tanpa LoRa. Kapasitas, format file, serta hardware final belum dipilih.
- Jika transfer memakai BLE di darat, kebutuhan jangkauan BLE dari pantai ke pelampung tidak lagi menjadi masalah utama.
- Alat harus merekam sepanjang periode terpasang. Mencelupkan alat sebentar saat kunjungan hanya menghasilkan pengamatan sesaat dan tidak cukup untuk analisis durasi kondisi di antara kunjungan.
- Evaluasi aturan di app/backend setelah sinkron merupakan rekomendasi yang masuk akal agar aturan dapat diperbarui tanpa mengganti firmware.
- Konsekuensinya, peringatan baru dapat muncul setelah data dibaca. Jangan menjanjikan peringatan langsung ketika alat masih di laut tanpa jalur komunikasi yang mendukungnya.
- Kebutuhan backend belum final. Analisis lokal di app dan unggahan setelah internet tersedia merupakan pilihan desain, bukan implementasi yang sudah ada.

### Alternatif yang pernah dibahas: LoRa

`Sensor → controller → LoRa → penerima di darat → internet seluler → backend → app iOS`

LoRa tidak menyediakan internet secara langsung. Stasiun darat membutuhkan penerima, daya, dan koneksi internet. LoRa titik-ke-titik atau LoRaWAN belum dipilih, jangkauan belum diuji, dan gateway belum dimodelkan dalam Fusion. Opsi ini tetap menjadi riwayat alternatif sampai diputuskan apakah diperlukan.

## 5. Data, aturan, dan peta

Rekomendasi dasar pencatatan untuk dibahas, **belum kontrak data yang disepakati**:

- Identitas node dan sesi pemasangan; waktu mulai/selesai dan timestamp bacaan yang dapat dipercaya.
- Lokasi pemasangan beserta sumbernya: ponsel, titik tetap, atau input manual; kedalaman probe dan cara pemasangan.
- Bacaan asli sensor beserta satuan, identitas/versi kalibrasi, serta cara menghitung nilai turunan seperti salinitas.
- Status baterai, penyimpanan, dan kualitas data; penanda masa alat dibawa, dibersihkan, tidak terendam, atau pembacaan belum stabil.
- Riwayat pengambilan/sinkron agar data tidak hilang atau terduplikasi.
- Catatan kondisi tanaman/kejadian ice-ice sebagai pembanding; tanggal tanam jika dinilai berguna untuk dikumpulkan.

Cara menentukan terendam/tidak terendam masih terbuka. Kebutuhan menandai data tidak valid tidak otomatis berarti harus menambahkan satu sensor khusus; pendekatan yang dipilih perlu diuji. Status manual sesi saja mungkin tidak menangkap probe yang sesekali keluar dari air.

IMU membutuhkan rancangan frekuensi dan durasi sampling tersendiri. Menyimpan semua bacaan mentah dapat memperbesar kebutuhan memori dan waktu transfer; pilih strategi yang mempertahankan data yang dibutuhkan untuk validasi. Interval 30 detik/satu menit terdahulu hanyalah contoh, bukan spesifikasi untuk semua sensor.

**Angka penurunan salinitas 3 ppt dan suhu 32/35°C muncul dalam teks Claude, tetapi belum diverifikasi dalam proyek.** Telusuri spesies, satuan, durasi, kedalaman pengukuran, kondisi eksperimen, dan penerapannya di lokasi sebelum mengubahnya menjadi aturan. Versikan aturan jika nanti diterapkan, sehingga hasil analisis bisa ditelusuri ulang.

Pada peta, bedakan lokasi pengamatan, area kebun yang ditandai pengguna, dan area yang benar-benar terwakili oleh pengukuran. Satu node tidak otomatis mewakili seluruh kebun. Radius belum boleh dibaca sebagai batas aman/berisiko atau jangkauan sensor.

## 6. Daya dan housing sebagai bagian produk

Untuk skenario ambil-pasang, baterai tanpa panel surya layak menjadi kandidat awal. Klaim “cukup 18650” belum bisa dibuat sebelum durasi pemasangan dan konsumsi komponen diketahui. Paket 2×18650 dalam CAD hanyalah bentuk pengganti; susunan listrik, kapasitas, dan rangkaian pengisian belum dipilih.

Urutan sizing: pilih komponen → tetapkan pola sampling/transfer → ukur konsumsi aktif dan sleep → hitung Wh per sesi serta cadangan → tentukan baterai/pengisian → evaluasi apakah solar diperlukan. Perekaman IMU dapat membatasi peluang sleep.

Kegunaan housing perlu diuji dari aktivitas pengguna:

- Mudah dipasang dan diambil, dengan pengikat yang konsisten dan tidak mengganggu tali/tanaman.
- EC dan suhu berdekatan, kedalamannya bisa diatur, mudah dibersihkan dan dikalibrasi.
- Sinkron tanpa perlu membuka ruang elektronik jika BLE dipilih.
- Akses pengisian/ganti baterai yang praktis dengan sambungan dan seal yang sesuai.
- Indikator rekam, baterai, dan memori sebagai kandidat fitur; bentuk LED/buzzer belum dipilih.
- Daya apung, kestabilan, jalur kabel, perlindungan air asin/matahari, dan perawatan harus diuji.

Pengambilan harian memudahkan inspeksi, tetapi tidak otomatis menyelesaikan kebocoran, biofouling, atau kebutuhan pembersihan. Beban kerja ambil-pasang juga perlu dinilai bersama pengguna.

## 7. Yang benar-benar sudah dibuat di Autodesk Fusion

Fusion MCP lokal berhasil dikonfigurasi dan digunakan untuk membuat draft mekanis. Pada pemeriksaan terakhir dalam sesi pembuatan, dokumen bernama **Untitled**, berisi **19 komponen / 23 body**, berstatus modified dan belum disimpan. Ini status historis, bukan pemeriksaan langsung saat dokumen handoff ini ditulis. Belum ada ekspor `.f3d` atau STEP yang diserahkan dalam percakapan ini.

| No. | Komponen draft |
|---|---|
| 01 | Pelampung cincin |
| 02 | Dasar dan dinding kotak elektronik; target tahan air |
| 03 | Tutup kotak semi transparan untuk melihat susunan |
| 04 | Ruang paket baterai 2×18650 + proteksi |
| 05 | ESP32 / BLE |
| 06 | MPU6050 / indeks gerak |
| 07 | Modul pengisian solar dan regulator |
| 08 | Opsi A: modul LoRa |
| 09 | Opsi B: modul microSD, BLE melalui ESP32 |
| 10 | Panel surya |
| 11 | Empat penyangga panel |
| 12 | Tiang sensor UV |
| 13 | Kepala sensor UV |
| 14 | Opsi A: antena LoRa |
| 15 | Kabel probe suhu |
| 16 | Probe suhu |
| 17 | Kabel probe EC |
| 18 | Probe EC / salinitas |
| 19 | Ilustrasi tali tambat |

Ukuran CAD dibuat untuk menyusun bentuk: pelampung OD 260 mm, ID 155 mm, tebal 50 mm; tapak kotak 120 × 96 mm, tinggi dinding 58 mm; tutup 126 × 102 × 5 mm; panel 130 × 85 mm. Ujung probe suhu/EC sekitar 255/300 mm di bawah bidang referensi model yang dipakai sebagai ilustrasi permukaan air. Garis air aktual belum dihitung dari massa dan daya apung.

**Draft ini mendahului arah ambil-pasang terbaru.** Solar, LoRa, dan microSD masih terlihat bersama sebagai alternatif. Hardware berbentuk blok/cylinder sederhana, bukan model barang yang telah dipilih. Tidak ada PCB/wiring yang selesai, bukti IP67, perhitungan daya apung, atau hasil simulasi sensor. Label enclosure telah diubah menjadi target tahan air agar tidak terkesan tersertifikasi.

Kekurangan yang sudah diketahui: EC dan suhu terpisah sekitar **210 mm horizontal**. Keduanya perlu didekatkan dalam revisi. Kedalaman probe harus disesuaikan dengan tali; pengait lepas-pasang serta dudukan probe yang bisa disetel belum dibuat. Penghapusan solar/LoRa dari varian PoC juga belum dilakukan.

Fusion digunakan untuk CAD mekanis. Visual yang terlihat lengkap tidak berarti spesifikasi elektronik, aturan analisis, dan kesiapan produksi sudah lengkap.

## 8. Langkah berikutnya yang disarankan

1. Pastikan titik/kebun uji, kedalaman tali dari permukaan, serta kondisi saat surut terendah. Periksa apakah tanaman atau probe dapat terpapar udara.
2. Tentukan pemasangan fisik: ke tali/rangka yang sama atau tambatan terpisah. Catat bagaimana pemasangan memengaruhi gerak IMU.
3. Tetapkan lama satu sesi pemasangan yang realistis untuk PoC dan cara mengambil data. Keputusan ini menentukan daya, memori, dan waktu hasil tersedia.
4. Definisikan besaran paparan matahari dan gerak air; pilih kandidat EC/suhu yang sesuai air laut, metode kalibrasi, dan alat pembanding.
5. Uji satu rangkaian pencatat dengan timestamp, kemudian bandingkan data terhadap pengukuran referensi. Eksperimen dua kedalaman suhu dapat dipertimbangkan jika ingin mengetahui pentingnya kedalaman, bukan menjadi kewajiban hardware final.
6. Perbarui CAD menggunakan ukuran komponen nyata; dekatkan EC/suhu, buat pengaturan kedalaman dan pengait, serta evaluasi varian baterai tanpa solar/LoRa.
7. Kembangkan sinkron dan ringkasan sesi. Uji aturan kandidat hanya setelah sumbernya diperiksa dan kualitas data diketahui; bandingkan dengan catatan kondisi tanaman.

## 9. Sumber dan hubungan ke vault

Sumber keputusan pengguna: percakapan langsung Radit–Codex dan kutipan percakapan Radit–Claude yang diberikan Radit. Pendapat Claude/Codex dicatat sebagai usulan atau interpretasi bila belum dikonfirmasi; bukan bukti lapangan tambahan.

Catatan repo yang relevan:

- [[Challenge Final]] — konteks proyek dan posisi riset tim.
- [[Rencana Pengukuran IoT Kondisi Laut - Diskusi Mas Ricky]] — alternatif sensor, komunikasi, energi, dan pekerjaan validasi.
- [[Diskusi - Mas Ricky (Mentoring IoT dan Pengukuran Kondisi Laut)]] — sumber mentoring.
- [[Konteks Riset Rumput Laut - 14 Oktober 2026]] — konteks riset terdahulu.
- [[Matriks Bukti Ice-Ice]] dan [[Sintesis Penyebab Ice-Ice]] — titik awal menelusuri bukti; bukan pernyataan bahwa ambangnya telah diverifikasi dalam handoff ini.

Rujukan teknis yang dibaca saat menilai transfer Claude pada 15 Oktober 2026:

- [Sea-Bird — faktor yang memengaruhi akurasi salinitas](https://www.seabird.com/faqs/1824): perhitungan salinitas, galat sensor, fouling, dan respons dinamis.
- [Apogee — pengukuran PAR bawah air](https://www.apogeeinstruments.com/underwater-par-measurements/): efek perendaman dan kebutuhan koreksi yang sesuai sensor.
- [Apogee — manual sensor UV](https://www.apogeeinstruments.com/content/UVS_webmanual.pdf): bahan transparan dapat menyaring UV; jangan menyamakan bening dengan transmisi UV yang sesuai.
- [Datawell — FAQ](https://datawell.nl/faq/): konfigurasi tambatan buoy bergantung pada kondisi pengukuran. Ini referensi prinsip, bukan validasi MPU6050 atau housing draft kita.

Dokumen transfer awal dibuat sebelum tambahan konteks Claude. Catatan ini menjadi versi pemahaman yang lebih baru untuk diteruskan di folder `radit`; keputusan yang masih terbuka sengaja dipertahankan sebagai terbuka.

## 10. Pembaruan kebutuhan dan audit komponen — 20 Oktober 2026

Bagian ini memperbarui status kebutuhan setelah diskusi dan pencarian komponen. Keputusan pengguna mengenai kebutuhan variabel dan alur kerja menjadi acuan terkini; saran komponen tetap berstatus kandidat sampai spesifikasi dan uji alat mendukungnya.

### Kebutuhan yang dikonfirmasi

- Dua variabel inti: **salinitas** dan **suhu air**.
- Satu alat merekam selama **5 jam**, lalu diambil dan disinkronkan ke app iOS melalui **BLE**.
- Anggaran total satu PoC: **Rp1–2 juta**. Tidak tersedia alat ukur pinjaman; tim bersedia belajar merakit dan menyolder.
- Cahaya dan gerak/arus tidak termasuk variabel inti saat ini. Keduanya pernah dibahas sebelumnya, tetapi tidak perlu dimasukkan ke BOM inti.

### Arti pengukuran salinitas

Salinitas dapat diturunkan dari konduktivitas listrik (EC) dengan kompensasi suhu dan metode yang sesuai. Karena itu sistem sebaiknya menyimpan **bacaan EC mentah, suhu air, dan nilai salinitas hasil perhitungan** secara terpisah, beserta satuan, waktu, status kalibrasi, dan versi rumus. EC sendiri bukan pengukuran nutrien tertentu atau diagnosis ice-ice.

### Kandidat biaya rendah yang ditemukan

[Sensor Konduktivitas / TDS / Kadar Garam Depoinovasi](https://depoinovasi.co.id/sensor-konduktivitas-tds-kadar-garam/) tercantum **Rp150.000** saat diperiksa. Halaman menyebut catu 5 V, keluaran analog 0–5 V, dan elektroda stainless di dalam pipa PVC. Namun halaman itu tidak menyatakan rentang EC, akurasi, grade stainless, kompensasi suhu, metode konversi salinitas, atau batas perendaman. Jadi ini **kandidat uji**, bukan pilihan sensor laut yang tervalidasi. Keluaran 0–5 V juga tidak boleh langsung masuk ke pin ESP32; batas input dan rangkaian harus diperiksa dahulu.

Probe DS18B20 waterproof lokal tercantum sekitar **Rp21.000** di [Jogjarobotika](https://jogjarobotika.com/produk/250/sensor-suhu-water-proof-ds18b20/). Itu harga chip/probe generik, bukan bukti bahwa seal dan selubungnya tahan air asin. Gunakan hanya setelah materi probe dan kemasan pada unit aktual diperiksa serta diuji. Pull-up data ke 3,3 V diperlukan untuk ESP32.

Referensi alternatif yang lebih terdokumentasi seperti Atlas EC-KIT berharga jauh di atas porsi wajar dari cap proyek. DFRobot DFR0300-H punya rentang EC yang relevan tetapi produsennya memperingatkan agar elektrodanya tidak direndam lama, sehingga belum dipilih untuk sesi 5 jam. [Panduan produsen](https://wiki.dfrobot.com/dfr0300-h/docs/20395).

### Anggaran dan batas keputusan

Audit belum membuktikan bahwa semua bagian alat laut dapat dibeli dan divalidasi dalam Rp2 juta. Tabel anggaran pada dokumen audit adalah **batas alokasi awal**, bukan penawaran harga per SKU. Pengendali, RTC, kartu SD, daya, casing, konektor, alat rakit, larutan standar dan pemeriksaan pembanding harus dihitung bersama sensor. Jangan menetapkan kandidat EC sebagai sensor utama hanya karena harganya cocok.

Tahap berikut yang paling mengurangi risiko adalah meminta spesifikasi teknis kandidat lokal atau menguji satu sampel pada larutan standar dengan nilai EC diketahui, lalu memeriksa apakah bacaannya mencakup kondisi air laut dan tetap stabil selama 5 jam. Keberhasilan uji meja masih perlu diikuti pemeriksaan selubung, sambungan kabel, dan uji terkontrol air asin. Pembelian sampel, jika dilakukan, adalah eksperimen dan mungkin gagal memenuhi kebutuhan.

### Dampak pada Wokwi dan firmware

- Pertahankan ESP32, microSD, sesi 5 jam dan metadata waktu sebagai arah dasar. Jam kalender memerlukan RTC atau sumber waktu yang disetel sebelum pemasangan.
- Ganti potensiometer simulasi dengan pembaca EC dan probe yang akhirnya lolos uji. Tambahkan perhitungan salinitas yang menggunakan suhu dan simpan EC serta suhu mentah.
- Ganti sensor suhu hanya setelah komponen fisiknya diputuskan. Driver DS18B20 tidak akan cocok bila pilihan akhir berupa PT1000 + pembaca RTD.
- Hapus LDR dan MPU6050 dari konfigurasi PoC inti untuk menjaga biaya dan pekerjaan tetap pada dua kebutuhan yang disepakati.
- Implementasikan BLE nyata di ESP32 dan penerima iOS; transfer Serial saat ini belum menguji koneksi BLE. Perlu potongan data, konfirmasi penyimpanan di app, retry/resume, dan pemeriksaan file utuh.
- Tambahkan daya, casing kering, seal kabel, dudukan probe, dan pengikat. Uji konsumsi selama 5 jam ditambah waktu transfer.

Wokwi membantu memeriksa alur kode, tetapi tidak membuktikan ketahanan laut, akurasi EC/salinitas, segel casing, masa baterai, ataupun transfer BLE ke app. Revisi firmware yang dibahas sebelumnya telah dikompilasi dan diuji dengan mock lokal, namun belum dijalankan pada ESP32 fisik atau diverifikasi di UI Wokwi.

Catatan pendukung audit: `/Users/radityaaydin/repos/depok/iot-hardware-review/README.md`, `BUDGET_OPTIONS.md`, dan `SENSOR_RESEARCH.md` (di luar vault). Sumber vendor di atas diperiksa 20 Oktober 2026; harga/stok dapat berubah.
