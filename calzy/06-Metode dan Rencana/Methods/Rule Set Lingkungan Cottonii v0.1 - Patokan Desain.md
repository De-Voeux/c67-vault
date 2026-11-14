---
type: design-specification
project: "[[Challenge Final]]"
created: 2026-10-28
updated: 2026-10-28
status: proposed-pilot-not-biologically-validated
rule_version: cottonii-environment-v0.1
tags: [challenge-final, cottonii, rule-set, desain, monitoring]
---

# Rule Set Lingkungan Cottonii v0.1 — Patokan Desain

**Keputusan desain yang diusulkan:** gunakan aturan eksplisit untuk menentukan prioritas pemeriksaan lingkungan dan tanaman. Tim desain dapat memakai spesifikasi ini untuk wireframe, prototipe, dan pengujian pemahaman. Ini belum aturan produksi atau klasifikasi risiko penyakit yang tervalidasi.

**Makna “pasti”:** input, operator, urutan keputusan, dan keluaran ditentukan. Kepastian biologis serta ketepatan cutoff belum dibuktikan. Angka operasional di bawah diberi label **P = keputusan pilot**, bukan hasil pengukuran batas penyakit. Bukti dan alasan pemilihannya tersedia di [[Bukti dan Keputusan - Rule Set Cottonii v0.1]].

## 1. Lingkup dan keputusan produk

Cottonii dipakai sebagai nama dagang yang umumnya merujuk *Kappaphycus alvarezii*. Identitas strain farm perlu dicatat. Aturan tidak otomatis berlaku untuk spinosum, *Gracilaria*, atau tambak payau. Dasar nomenklatur dan batas generalisasi: [[Tiga Paper Baru - Implikasi Pengukuran IoT 2026-10-20]].

Konfigurasi inti mengikuti [[Pembaruan Desain - Sensor Suhu Hourly dan Inferensi On-Device]]: **satu sensor suhu per plot, target satu record per jam**. Dokumen ini tidak menambah perangkat salinitas. Data lokal, model regional, prakiraan, dan laporan tanaman menghasilkan kartu terpisah. Satu titik sensor tidak mengukur seluruh pulau.

| Elemen UI | Label yang dipakai | Makna |
|---|---|---|
| Hijau | **Tidak ada pemicu suhu** | Data suhu cukup dan aturan suhu tidak aktif; parameter lain serta kesehatan tanaman belum disimpulkan |
| Kuning | **Waspada — periksa kondisi** | Ada penyimpangan/perubahan yang perlu diperiksa |
| Merah | **Prioritas pemeriksaan tinggi** | Pembacaan panas tinggi, pengulangan paparan, atau laporan kerusakan membutuhkan prioritas |
| Abu-abu | **Belum dapat dinilai** | Data untuk cakupan tersebut kurang, lama, atau tidak valid |

Teks pendamping warna merah: **“Peringatan pilot; belum menunjukkan probabilitas ice-ice.”** Jangan memberi label “aman”, “pasti sakit”, “bahaya ice-ice”, persentase penyakit, atau rekomendasi tanam/panen otomatis. Jika desain membutuhkan istilah rendah/tinggi, gunakan **“prioritas pemeriksaan rendah/tinggi”** dan tampilkan alasan.

## 2. Syarat data sebelum menghitung aturan [P]

Seluruh angka pada bagian ini merupakan kebijakan pilot, tidak mengubah policy A3 yang sudah ada. Input harus terlebih dahulu lolos QC pipeline. Snapshot demo/sintetis boleh dipakai pada prototipe dengan banner **“Data simulasi”**, tidak sebagai penilaian farm nyata.

| Pemeriksaan | Ketentuan |
|---|---|
| Identitas | Plot, sensor, sumber, satuan °C, `observed_at`, dan `received_at` tersedia; suhu air dibedakan dari suhu udara |
| Pemasangan | Sensor terendam dan posisi/kedalaman terhadap tanaman tercatat. Jika kondisi pemasangan tidak diketahui, tampilkan angka sebagai belum terverifikasi dan status abu-abu |
| Mutu alat | Ada commissioning/cek pembanding sesuai spesifikasi alat; sensor gagal kalibrasi atau terkena flag invalid tidak dinilai. Nilai ekstrem tidak boleh dibuang hanya karena ekstrem |
| Waktu | Simpan UTC, tampilkan Asia/Jakarta. Timestamp masa depan >5 menit ditahan untuk verifikasi jam perangkat |
| Kebaruan | Reading terbaru berumur **≤90 menit** terhadap waktu penilaian; >90 menit berarti status suhu saat ini abu-abu |
| Duplikat | Retry record yang sama dihitung sekali. Konflik dua nilai untuk sensor/waktu sama ditahan sampai diselesaikan; tidak dipilih nilai yang lebih nyaman |
| Pasangan hourly | Dua reading valid dari slot jam berurutan, selisih waktu aktual **45–75 menit**, sensor dan pemasangan sama. Tidak interpolasi melewati gap |
| Data minimum hijau | Reading terbaru valid dan fresh, serta tersedia satu pasangan hourly valid. Baseline 28 hari tidak wajib untuk menjalankan batas absolut |

Jika cadence aktual adalah agregasi banyak sampel, simpan jenis agregat dan jumlah sampel. **V0.1 menilai nilai representatif per jam yang dideklarasikan**, bukan mencampur mean, maksimum, dan spot reading. Mean hourly dapat menyembunyikan puncak; tampilkan keterbatasan itu. Aturan puncak berbasis maksimum memerlukan versi tersendiri.

**Dua reading tinggi berjarak satu jam tidak membuktikan suhu tinggi terus-menerus selama satu jam.** Copy UI wajib menyebut dua pembacaan, bukan “terpapar 60 menit”. Data hilang tidak dihitung normal dan tidak menambah durasi paparan.

## 3. Tabel aturan suhu — aktif pada profil inti

`T` = reading terbaru valid/fresh. `Tprev` = pasangan hourly valid. Jalankan semua aturan yang memenuhi syarat; simpan seluruh alasan. Status pemicu mengikuti prioritas tertinggi. Semua operator menggunakan angka asli sebelum pembulatan tampilan.

| ID | Kondisi pemicu | Level | Copy inti | Dasar |
|---|---|---|---|---|
| T01 | `T < 26` atau `T > 30` | Kuning | “Suhu di luar target pantauan 26–30°C.” | Kisaran kerja tim/masukan Roleda; pemakaian sebagai trigger adalah P, bukan batas kerusakan |
| T02 | `T >= 32` dan `Tprev >= 32`, pasangan hourly sah | Merah | “Suhu ≥32°C pada dua pembacaan berurutan. Prioritaskan pemeriksaan.” | Ada pijakan stres pada perlakuan 32°C; syarat dua reading adalah P [E01] |
| T03 | `T >= 35` pada satu reading valid/fresh | Merah | “Pembacaan suhu tinggi: {T}°C. Verifikasi sensor dan kondisi tanaman.” | P untuk urgensi, diinformasikan studi panas tinggi; bukan titik biologis universal [E01–E03] |
| T04 | `abs(T − Tprev) >= 2.0°C`, pasangan hourly sah | Kuning | “Suhu berubah {delta}°C dalam {selang} menit.” | Cutoff 2°C dan window adalah P; belum ada ambang delta penyakit terverifikasi |
| T05 | `abs(T − B_h) >= 2.0°C` pada satu reading dengan baseline sah | Kuning | “Suhu {selisih}°C dari pola referensi pada jam ini.” | Baseline dan cutoff adalah P; menunjukkan ketidaklaziman, bukan kepastian stres |
| T00 | Tidak ada T01–T05; syarat data minimum hijau terpenuhi | Hijau | “Tidak ada pemicu suhu pada pembacaan yang tersedia.” | Hasil aturan, bukan temuan biologis |

**Urutan:** T03/T02 → T01/T04/T05 → T00. Jika hanya satu reading 32–<35°C tersedia, keluarkan kuning T01 + “menunggu pembacaan berikutnya”; jangan menunggu dua reading sebelum memberi perhatian awal. Satu reading 26–30°C tanpa pasangan valid belum cukup untuk hijau: abu-abu “riwayat belum cukup”, angka tetap terlihat.

Tepat 26 dan 30°C termasuk target; tepat 32°C memenuhi T02 bila berulang; tepat 35°C memenuhi T03; tepat delta 2°C memenuhi T04/T05. Suhu <26°C tetap kuning pada v0.1; tidak dibuat cutoff merah dingin dengan menyalin cutoff panas. Belum ada aturan bahwa beberapa kuning otomatis menjadi merah, atau bahwa nutrisi/arus baik menurunkan merah.

## 4. Pagi, siang, malam dan baseline [P]

**Batas absolut pada T01–T03 sama selama 24 jam.** Baseline mengikuti pola lokasi dan jam; baseline tidak dapat membatalkan batas absolut. Tidak ada angka optimum berbeda untuk pagi/siang/malam yang telah ditetapkan dari bukti yang ditelaah.

`B_h` adalah median reading pada **jam lokal yang sama**, dari maksimal 28 hari lengkap sebelum hari penilaian. Gunakan paling banyak satu nilai representatif per hari pada slot tersebut. Minimal **14 hari berbeda** dengan record valid, sensor/posisi/metode agregasi sama. Hari ini tidak masuk referensi. Data gagal QC dan periode sensor terangkat tidak masuk.

Bekukan baseline sebagai versi referensi ketika pertama kali memenuhi syarat; tinjau tiap 28 hari atau setelah perubahan pemasangan. Pembaruan hanya setelah review data, tidak otomatis menyesuaikan diri setiap kali suhu naik. Jika sensor/lokasi/metode berubah, baseline lama tidak dipakai. Referensi ini adalah **pola yang tercatat**, tidak boleh disebut “pola sehat” tanpa inspeksi berpasangan.

| Contoh sintetis | Hasil aturan |
|---|---|
| Jam 14: `B_h=29,5`, `Tprev=29,4`, `T=30,0` | Hijau jika syarat data terpenuhi; tidak ada delta/anomali ≥2 |
| Jam 02: `B_h=27,0`, `Tprev=29,2`, `T=30,0` | Kuning T05: malam lebih hangat 3°C dari referensi |
| Jam 14: `B_h=31,0`, `Tprev=32,1`, `T=32,2` | Merah T02; pola siang panas tidak menetralkan batas absolut |
| Dari 27 ke 29°C pada pasangan hourly sah | Kuning T04 meski kedua nilai masuk target; penyebab belum diketahui |

Simpan juga jumlah reading ≥32°C dalam 24 jam, minimum/maksimum teramati, dan coverage. Dengan spot reading hourly, tulis **“4 dari 20 pembacaan valid ≥32°C”**, bukan “4 jam paparan”. Jangan menyebut maksimum teramati sebagai puncak sebenarnya di antara sampel.

## 5. Parameter selain suhu

Aturan opsional hanya diaktifkan jika jenis sumber dan mutu datanya memenuhi tabel ini. Angka target bukan ambang bebas penyakit. Tidak tersedianya salinitas lokal tidak menghalangi kartu suhu, tetapi membuat cakupan salinitas lokal “belum diukur”.

| Parameter | Aturan v0.1 | Keluaran dan batas |
|---|---|---|
| Salinitas **lokal** | S01 opsional: `<28` atau `>34` pada pengukuran valid berumur ≤90 menit → kuning [P]. S02 opsional: `abs(delta)>=3` pada pasangan hourly sah dari alat/metode sama → kuning [P] | “Salinitas di luar target/perubahan cepat; ukur ulang dan periksa tanaman.” Pengukuran manual tunggal tidak menghasilkan delta atau persistensi. Tidak ada merah otomatis salinitas dalam versi ini; cutoff ekstrem perlu telaah unit/protokol dan validasi lebih lanjut [E04, E08] |
| Salinitas **regional** | RG01: `<28` atau `>34` pada nilai analysis/model non-forecast yang usable → kartu **waspada regional** [P] | Tidak mengisi S01/S02, tidak mengubah plot menjadi merah. Nilai 6-jam tidak menghasilkan delta lokal 1-jam |
| Arus **lokal** | C01 opsional: `<0,20` atau `>0,40 m/s` pada pengukuran valid → kuning [P] | Periksa sirkulasi/fouling jika lemah, kondisi tali/tanaman jika kuat; catat fase pasang. Kisaran target bukan cutoff penyakit [E07] |
| Arus **regional** | RG02: magnitude `sqrt(u²+v²)` di luar `0,20–0,40 m/s` pada analysis/model usable → kartu waspada regional [P] | Bukan kecepatan di tali atau gelombang. `0,20 m/s = 20 cm/detik`; jangan menerapkan batas pada komponen u/v secara terpisah |
| Nitrat | Konteks nutrisi, **tidak memicu warna kesehatan** pada v0.1 | Nilai, unit kimia, sumber, tanggal, dan tren terlihat. Rentang pengguna 0,9–3,5 mg/L belum disahkan sebagai cutoff [E04, E08] |
| Fosfat | Konteks nutrisi, **tidak memicu warna kesehatan** pada v0.1 | Perlakuan sama; 0,051–1,00 mg/L belum disahkan. Tidak ada saran pupuk/dosing otomatis |
| Hujan | Nilai/akumulasi observasi dan prakiraan dipisah; **tidak memicu warna kesehatan** | Copy konteks: “Hujan dapat mengubah kondisi air; cek salinitas lokal bila tersedia.” Tidak ada persamaan mm hujan → ppt farm [E06] |
| Angin | Kecepatan dan arah untuk konteks; **tidak memicu warna kesehatan** | Arah angin saja tidak mengidentifikasi “air busuk”. Peringatan keselamatan resmi, bila tersedia, tampil terpisah sesuai penerbit [I02, E06] |
| Cloud coverage | Konteks cahaya, **tidak memicu warna kesehatan** | Tidak mengonversi % awan menjadi PAR tanaman atau menganggap mendung selalu baik [E09] |
| UV Index | Konteks cuaca, **tidak memicu warna kesehatan** | UV Index bukan PAR dan bukan dosis UV di jaringan bawah air. UV nol malam tidak menjadi alarm cahaya rendah [E09, D01] |

`Usable regional` pada usulan desain ini: lolos QC/alignment sumber, unit/grid/kedalaman diketahui, jelas analysis versus forecast, sudah tersedia saat penilaian, dan timestamp valid terbaru tidak di masa depan. Batas umur valid time: **≤9 jam untuk salinitas/arus 6-jam** [P]. Lebih lama → regional abu-abu; jangan memforward-fill untuk menjalankan aturan. Jika A3 menolak lebih awal, penolakan A3 berlaku. Kontrak aktual snapshot harus dicocokkan engineering sebelum implementasi.

Forecast suhu/salinitas/arus yang melewati target tampil sebagai **“Prakiraan perlu perhatian”** beserta waktu berlaku dan penerbitan bila diketahui; tidak dihitung sebagai kejadian lokal teramati. Vintage yang tidak diketahui diberi label demikian. V0.1 tidak menetapkan lead time penyakit atau membuat merah plot dari forecast.

Untuk nutrisi Copernicus `mmol/m³`: kalikan 0,062 untuk mg/L sebagai NO₃, atau 0,014 sebagai N; fosfat kalikan 0,095 sebagai PO₄ atau 0,031 sebagai P. Koefisien dibulatkan dari massa molar; jangan bandingkan angka sebelum definisi kimianya sama. Contoh `1 mmol/m³ NO₃ = 0,062 mg/L NO₃`, bukan 1 mg/L. Practical Salinity, g/kg dan label ppt instrumen harus dipetakan menurut metadata; tidak diasumsikan identik [D02 dan [[Tiga Paper Baru - Implikasi Pengukuran IoT 2026-10-20]]].

## 6. Laporan tanaman dan pengalaman lapangan

Jalankan jalur ini **meskipun suhu hijau, tidak tersedia, atau regional terlihat normal**. Status lingkungan dan status tanaman tetap dua field terpisah; tugas inspeksi dapat berprioritas merah tanpa menyatakan air penyebabnya. Foto opsional dan input setelah pulang mengikuti keputusan 23 Oktober pada [[Flow Model Proyek - Indikasi Risiko Ice-Ice]].

| ID | Laporan | Status tugas [P] | Copy |
|---|---|---|---|
| B01 | Baru memutih/pucat; tekstur masih solid atau belum diketahui | Kuning | “Perubahan tanaman dilaporkan. Periksa tekstur, lokasi perubahan dan progresinya.” |
| B02 | Jaringan melunak/benyek, mudah putus, atau kerusakan dilaporkan meluas | Merah | “Kerusakan tanaman dilaporkan. Prioritaskan pemeriksaan bersama pendamping.” |
| B03 | Laporan air keruh/berbau/terasa panas tanpa pengukuran | Kuning | “Perubahan air dilaporkan; penyebab belum diketahui.” |
| B00 | Sudah diperiksa dan tidak menemukan gejala | Log hasil pengamatan | Berlaku pada sampel dan waktu pengamatan; bukan sertifikat bebas penyakit |

Catat waktu pengamatan terpisah dari waktu input, pengamat langsung versus cerita petani, ciri tanaman, jumlah diperiksa/terdampak jika diketahui, bagian tanaman, serta tindakan. Lokasi sumber catatan Pak Unin dan identitas catatan berjudul Pak Dahlan masih mempunyai ketidakpastian; jangan memperlakukannya sebagai pengukuran atau tiga konfirmasi independen [I01–I04].

B01/B02 adalah **laporan gejala/kerusakan**, bukan diagnosis IID. Pengamatan Fauzi tentang rescue menjadi bahan diskusi tindakan dengan pendamping, bukan instruksi otomatis memindah tanaman, menurunkan tali, memasang naungan, atau panen [I02, E07].

## 7. Gabungan status, pemulihan, dan notifikasi [P]

Simpan `temperature_status`, `regional_status`, `plant_report_status`, `data_status` dan `inspection_priority` terpisah. Kartu utama menampilkan alasan terpenting beserta sumbernya.

1. Pemicu lokal/biologis merah yang masih terbuka → prioritas tinggi. Pemicu kuning atau waspada regional → waspada. Regional tidak menurunkan pemicu lokal dan sebaliknya. Tidak ada rata-rata skor atau bobot 60:40.
2. Jika tidak ada pemicu tetapi data suhu tidak cukup → abu-abu. Jika suhu cukup dan tidak ada pemicu → hijau **untuk suhu saja**; status parameter lain tetap terlihat.
3. Setelah T02/T03 aktif, pertahankan prioritas tinggi sampai terdapat **tiga reading baru pada tiga slot hourly berurutan, setiap pasangan sah, seluruhnya <32°C**. Reading pembuka merah tidak dihitung; reading baru ≥32°C mengulang hitungan pemulihan merah dari nol. Bila sudah lolos, status minimum kuning “paparan tinggi sebelumnya”; hijau baru setelah tiga reading baru berturut-turut berada dalam 26–30°C dan T04/T05 tidak aktif pada ketiganya. Hitungan hijau kembali nol setiap kali salah satu syarat hijau gagal. Gunakan rangkaian terakhir yang memenuhi syarat, bukan hanya tiga reading pertama setelah alert.
4. Kuning suhu pulih setelah tiga reading baru berurutan dalam target dan tidak memicu T04/T05. Gap memutus rangkaian pemulihan. Baseline belum tersedia tidak diperlakukan sebagai T05 aktif.
5. Data menjadi stale/invalid saat alert terbuka → status saat ini abu-abu + **“peringatan sebelumnya belum terverifikasi pulih”**. Prioritas tugas lama dipertahankan; jangan tampilkan merah seolah pengukuran saat ini masih tinggi, atau hijau karena koneksi putus.
6. B01–B03 ditutup lewat kunjungan tindak lanjut dengan hasil tercatat oleh pengamat; kondisi suhu normal tidak menutupnya. Laporan terlambat ditampilkan sebagai riwayat berwaktu + tugas cek kondisi terkini, bukan gejala live.
7. S01/S02/C01 ditutup dengan dua pengukuran lokal baru valid dalam target dari slot hourly berurutan, tidak memicu delta opsional; jika pengukuran hanya manual sesekali, petugas menutup tugas setelah verifikasi tercatat. RG01/RG02 ditutup pada update native berikutnya yang usable dan kembali dalam target; jeda data menghasilkan unknown, bukan pulih.
8. Notifikasi hanya ketika episode baru muncul, naik level, atau ada laporan kerusakan baru. Pembacaan berulang pada episode sama memperbarui kartu tanpa push baru. Pengakuan “sudah dibaca” tidak menutup alert; satu tombol “normal” tanpa catatan tidak menyelesaikan laporan tanaman.

Waktu respons yang diusulkan: kuning diperiksa pada kesempatan kunjungan berikutnya, target dalam 24 jam; merah diverifikasi secepat akses aman memungkinkan, target dalam 6 jam. Angka ini **target layanan pilot**, bukan lead time biologis atau instruksi keluar ke laut pada malam/cuaca berbahaya. App menyampaikan tugas kepada pengguna; dokumen ini tidak mengirim notifikasi atau menghubungi siapa pun.

## 8. Anatomi kartu untuk tim desain

**Contoh sintetis:**

> **Prioritas pemeriksaan tinggi**  
> Plot A · suhu lokal 32,4°C  
> Dua pembacaan ≥32°C: 13.00 dan 14.00 WIB.  
> Data terakhir 14.00 · diterima 14.06 · dinilai 14.10.  
> Verifikasi pembacaan dan periksa kondisi tanaman bersama pendamping.  
> Salinitas lokal belum diukur. Aturan pilot v0.1.  
> **Lihat riwayat** · **Catat hasil pemeriksaan**

Setiap kartu wajib memuat plot/cakupan, level + teks, alasan dan ID aturan, nilai/satuan, sumber lokal/regional/forecast/laporan, waktu pengukuran dan umur data, kelengkapan, langkah berikutnya, dan versi aturan. Bukti ilmiah tersedia di detail “Dasar aturan”; jangan memaksa pengguna membaca paper untuk mengetahui tindakan.

Map memakai warna prioritas pemeriksaan dan ikon sumber. Beberapa plot dalam sel regional yang sama mendapatkan konteks regional yang sama; jangan membuat gradien presisi antarplot dari satu grid. Kondisi bergejala, data tidak tersedia, dan paparan panas memakai ikon/teks pembeda agar tidak bergantung pada warna.

## 9. Skenario acceptance desain

Semua contoh memakai data valid/fresh kecuali disebut lain. Ini spesifikasi expected behavior, bukan klaim implementasi telah lulus uji.

| Skenario | Hasil yang diharapkan |
|---|---|
| 29→30°C, pasangan sah, baseline selisih <2 | Hijau suhu |
| 30→30,1°C | Kuning T01; pembulatan tampilan tidak membatalkan trigger |
| 31→32°C, pasangan sah | Kuning; belum dua reading ≥32 |
| 32→32°C, pasangan sah | Merah T02 |
| Reading pertama 35°C | Merah T03 + verifikasi; tanpa klaim durasi |
| 32°C jam 12, gap jam 13, 32°C jam 14 | Kuning; tidak memenuhi pasangan T02 |
| 27→29°C dalam 60 menit | Kuning T04, meski dalam target |
| 27→29°C dalam 120 menit | T04 tidak dapat dinilai sebagai delta hourly |
| T=30°C malam, baseline jam tersebut 27°C | Kuning T05 |
| Baseline baru 7 hari, T=29°C, pasangan tanpa delta | Hijau suhu; fitur baseline “belum cukup”, tidak mengaku pola normal |
| T=29°C tetapi reading berumur 91 menit | Abu-abu suhu |
| Merah terbuka lalu data putus | Abu-abu kondisi kini + tugas prioritas tinggi belum pulih |
| Merah pada 32°C lalu 31,0→29,8→29,4→29,2°C pada jam berurutan, baseline tidak memicu | Pada 29,4°C merah turun menjadi kuning (tiga reading <32); pada 29,2°C bisa hijau (tiga reading target tanpa pemicu). Riwayat merah tersimpan |
| Suhu 29°C, tanaman benyek dilaporkan | Hijau suhu + tugas merah B02; bukan diagnosis |
| Lokal tidak memicu; salinitas regional 27 | Waspada regional, minta pengukuran lokal; bukan salinitas plot 27 |
| Arus regional u=0,15 dan v=0,15 m/s | Magnitude ≈0,212 m/s; tidak memicu RG02 |
| UV=0 malam / awan 100% / hujan terprakirakan | Konteks; tidak merah kesehatan dari variabel itu saja |

## 10. Review dan validasi berikutnya

Desain dapat dikerjakan sekarang memakai versi ini. Sebelum dipakai sebagai peringatan lapangan, review bersama penanggung jawab budidaya/ahli dan engineering: commissioning sensor, semantik record hourly, cutoff pilot, kemampuan kunjungan, serta kesesuaian unit dan cakupan regional. Angka belum diendors Professor Roleda dan belum disetujui sebagai deployment app.

Uji pada beberapa plot/siklus dengan inspeksi rutin saat ada dan tidak ada alert; simpan waktu pengamatan, outcome dan tindakan. Ukur alarm yang berujung temuan, kejadian terlewat, false alert per plot-minggu, keterlambatan data, waktu verifikasi, beban kunjungan dan manfaat tindakan. Tidak diperiksa berarti outcome tidak diketahui. Jika kelak mengklaim prediksi, tetapkan definisi kasus/horizon terlebih dahulu dan uji pada waktu serta farm yang tidak dipakai memilih cutoff.

Versi berikutnya hanya berubah setelah review hasil. Riset yang ditelaah belum mendukung akurasi, probabilitas penyakit, atau jaminan hasil panen untuk aturan ini. Penyusunan dibantu AI menggunakan alur ARS deep-research quick; bukan systematic review atau review ahli independen.

## Terhubung

[[Bukti dan Keputusan - Rule Set Cottonii v0.1]] · [[Indeks - Metode dan Rencana]] · [[Flow Model Proyek - Indikasi Risiko Ice-Ice]] · [[Kajian Indikator Warning Ice-Ice - Uji Asumsi Fitur]] · [[Diskusi - Professor Roleda (Ice-Ice, Threshold, dan Validasi Lapangan)]]
