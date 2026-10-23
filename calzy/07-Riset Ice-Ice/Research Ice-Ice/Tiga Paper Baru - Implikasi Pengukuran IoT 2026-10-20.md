---
type: evidence-synthesis
project: "[[Challenge Final]]"
created: 2026-10-20
status: paper-comparison-pilot-not-validated
species_reported_by_user: Eucheuma cottonii
sensors_reported_by_user: [temperature, salinity]
tags: [challenge-final, ice-ice, literature, iot, salinity, temperature]
---

# Tiga Paper Baru - Implikasi Pengukuran IoT 2026-10-20

**Jawaban utama:** ketiga paper menambah konteks biologis dan angka eksperimen, tetapi belum menetapkan cutoff suhu/salinitas, durasi sebelum alarm, atau probabilitas ice-ice untuk perangkat lapangan. Dua sensor yang sudah ada dapat dipakai untuk merekam paparan dan mendukung inspeksi. Membaca suhu/salinitas dalam suatu rentang belum menyatakan tanaman sehat.

Pengguna mengonfirmasi: **“Eucheuma cottonii, sensornya baru temperatur dan salinitas.”** Dalam perdagangan, cottonii umumnya merujuk *Kappaphycus alvarezii*, sehingga paper pada spesies itu relevan sebagai pijakan. Nama dagang bukan identifikasi varietas/haplotipe pada farm; jangan menyamakan seluruh cottonii dengan delapan strain liar atau kultivar tambalang yang diuji. [FAO, nomenklatur komoditas](https://www.fao.org/4/y4765e/y4765e09.htm).

## Sumber dan apa yang baru bagi vault

| PDF | Artikel dan DOI | Kontribusi dibanding catatan sebelumnya |
|---|---|---|
| P22 | Tabonda-Nabor et al. (2026), *Light stress regulates pigment concentrations, growth, and gene expression in hatchery-cultivated Kappaphycus alvarezii (Solieriaceae, Rhodophyta)*. Journal of Phycology 62:568–588. [DOI](https://doi.org/10.1111/jpy.70148) | Bukti langsung tambahan tentang cahaya rendah/tinggi, aklimasi, perubahan pigmen dan ekspresi gen. |
| P23 | Aguilar, Paras & Roleda (2026), *The ice-ice disease black box: a disease complex triggered by bacterial associations in an ex situ milieu of biobanked Kappaphycus alvarezii*. FEMS Microbiology Letters 373:fnag080. [DOI](https://doi.org/10.1093/femsle/fnag080) | Pengamatan kultur gene bank sehat/sakit dalam kondisi terkendali; asosiasi jaringan–mikroba, bukan challenge kausal. |
| P24 | Gacura et al. (2025), *To plant or not to plant? Nutrient uptake, growth, and biochemistry of eucheumatoids under low salinity as influenced by nutrient-rich freshwater outflow*. Journal of Phycology 61:911–925. [DOI](https://doi.org/10.1111/jpy.70044) | **Sudah ada sebagai W04** di [[Literatur Tambahan - Indikator Warning]], dahulu cakupan abstract. Sekarang metode, hasil dan tabel PDF tersedia; ini pendalaman studi yang sama, bukan replikasi independen. |

Salinan PDF: [[Daftar PDF Paper]]. Nama P22–P24 mengikuti konvensi vault. Metadata, path asal, checksum, cakupan baca dan lokasi angka tersimpan pada `Manifest Tiga Paper Baru 2026-10-20.json` di folder catatan ini. Manifest S01–S21 dan ID W04 tidak diganti.

## 1. Tabonda-Nabor: cahaya tinggi tidak otomatis berarti kerusakan

**WHY:** menelusuri respons fisiologi, pigmen dan regulasi gen terhadap perubahan cahaya agar strategi hatchery mempunyai dasar biologis.

**HOW:** delapan strain *K. alvarezii* asal Guiuan, Samar, dipelihara di hatchery darat Bolinao, Filipina. Empat berfenotipe cokelat dan empat progeni hijau. Sebelumnya diaklimasikan pada cahaya medium setidaknya satu tahun. Perlakuan low/high berlangsung 28 hari dalam akuarium berair laut tersaring mengalir dan beraerasi; n=8 per perlakuan untuk analisis yang dilaporkan. Suhu air sekitar 31°C; irradiance diukur di permukaan dengan light meter bersensor cosine. Angka bukan rekaman PAR tepat di jaringan tanaman laut Tidung. [P22, PDF hlm. 2–4 / jurnal 569–571.]

| Kondisi cahaya | Intensitas dilaporkan, µmol photons m⁻² s⁻¹ | DGR, % per hari, mean ± SD |
|---|---:|---:|
| Low | 203 ± 6 | 1,88 ± 1,38 |
| Medium/control, kondisi aklimasi | 627 ± 64 | 4,94 ± 1,55 |
| High | 910 ± 23 | 6,03 ± 1,86 |

**WHAT:** mean pertumbuhan tertinggi pada high light; tidak berbeda signifikan dari medium menurut narasi hasil (p=0,23). Low versus high berbeda signifikan dalam narasi dan pengelompokan tabel. Di low light thallus menjadi lebih gelap/tipis, dan beberapa mengalami pelunakan serta deteriorasi; phycoerythrin meningkat menjadi 6,52 ± 2,52 µg/g fresh weight. Jadi warna lebih gelap bukan bukti tanaman lebih sehat, dan perubahan warna yang lebih terang pada pertumbuhan baru bukan diagnosis ice-ice. [P22, PDF hlm. 5–7, Tabel 1/Fig. 1–3; Discussion PDF hlm. 15.]

High light disertai perubahan transkripsi gen yang berhubungan dengan photoprotection/antioxidant dan perbaikan DNA; low light memperlihatkan pola penggunaan cadangan serta degradasi polisakarida. Lectin KAA merupakan kandidat respons pertahanan, **bukan biomarker lapangan atau perlindungan terhadap infeksi yang sudah diuji di sini**. Kuantifikasi biokimia karaginan tidak dilakukan; ekspresi gen tidak langsung menjadi yield karaginan. [P22, Results dan Discussion, terutama PDF hlm. 17–18.]

**Batas metode yang menentukan interpretasi:**

- Medium untuk RNA dan pigmen diambil pada awal/Day 0, low/high sesudah 28 hari; perbandingan ekspresi terhadap medium dapat mencampurkan efek waktu dan perlakuan. Ini inferensi pembaca yang belum diuji ulang; tidak diterapkan otomatis pada semua pengukuran pertumbuhan karena paper menyatakan fisiologi juga dipantau lintas waktu. [reader-inferred; Methods PDF hlm. 3–4.]
- Tabel 1 memberi huruf a/ab/b untuk DGR, sedangkan narasi menyebut low–medium signifikan p=0,001. Keduanya tidak konsisten untuk pasangan tersebut. Angka mean dipertahankan, tetapi tidak dipakai untuk menetapkan transisi/cutoff medium. [reader-inferred; PDF hlm. 5–6, tabel diperiksa visual.]
- Data berasal dari hatchery dengan flow/aerasi dan strain teraklimasi; jika langsung dipindahkan ke farm tanpa konteks tersebut, angka 910 dapat salah dianggap batas aman. [reader-inferred; Methods PDF hlm. 3.]
- Fungsi beberapa gen masih kandidat berdasarkan homologi; penulis menyebut perlunya konfirmasi pola dan pengukuran karaginan langsung. [author-acknowledged; Discussion PDF hlm. 17.]

**Implikasi untuk dua sensor sekarang:** suhu dan salinitas belum menjelaskan cahaya aktual yang diterima tanaman. Paper mendukung perlunya konteks cahaya/naungan/kedalaman saat membaca hasil sensor, tetapi tidak mewajibkan menambah UV sensor. Studi memakai satuan photon irradiance/PAR, bukan UV index; 203 atau 910 tidak dapat dikonversi menjadi alarm UV. Angka “low” relatif terhadap aklimasi/eksperimen ini, bukan batas penyakit universal.

## 2. Aguilar: kondisi stabil tidak cukup untuk menandai tanaman aman

**WHY:** memahami mengapa sebagian stok *K. alvarezii* gene bank mengalami gejala IID meskipun dipelihara dalam kondisi terkontrol.

**HOW:** satu kultur sehat dan satu sakit dari strain yang sama dipilih sebagai snapshot. Jaringan serta bulk water masing-masing menghasilkan empat tipe sampel. Isolasi kultur pada Nutrient Agar, sekuensing 16S, dan uji aktivitas pemecahan agar/karaginan menghasilkan 31 isolat, mewakili enam taksa. **31 isolat bukan 31 tanaman atau 31 ulangan penyakit.** [P23, Methods PDF hlm. 2–4; Tabel 1–2.]

Kondisi pemeliharaan yang dilaporkan: **23 ± 2°C, salinitas 34 ppt, irradiance 45–50 µmol photons m⁻² s⁻¹, fotoperiode 12:12 jam**. Kultur sehat dan sakit tersedia pada sistem pemeliharaan tersebut. Angka ±2°C bukan spesifikasi akurasi thermometer, dan 34 ppt bukan threshold aman yang diturunkan dari studi. [P23, Fig. 5 dan Discussion PDF hlm. 11.]

**WHAT:** jaringan sehat menghasilkan *Rossellomorea aquimaris*; jaringan sakit menghasilkan *Vibrio* dan *Photobacterium*. Taksa yang pulih dari jaringan berbeda dari air sekitarnya. Satu isolat *Photobacterium* dari jaringan sakit dan satu *Vibrio* dari air kultur sakit menunjukkan aktivitas agarolytic/carrageenanolytic. Ini hubungan fungsional dengan potensi degradasi jaringan, **belum membuktikan inisiasi penyakit oleh isolat tersebut**. [P23, Results PDF hlm. 4–8; Discussion/Conclusion hlm. 9–12.]

Penulis mengusulkan bahwa cahaya rendah yang menetap, kondisi host, mikroabrasi ketika pembersihan, dan mikroba oportunistik dapat berinteraksi. Penyebab itu tidak dipisahkan secara eksperimental. Rendah/stabilnya suhu tidak berarti semua bentuk stres ditiadakan. [P23, Discussion PDF hlm. 11–12.]

**Batas metode:** snapshot satu sehat–satu sakit tidak memberikan prevalensi atau efek kausal; kultur bakteri hanya mencakup bagian mikrobioma yang dapat ditumbuhkan pada medium tersebut; baseline fisiologi/mikrobioma dan challenge pathogenicity belum tersedia. Penulis sendiri menyatakan batas-batas ini. [author-acknowledged; Methods hlm. 3, Results hlm. 8, Conclusion hlm. 12.]

**Implikasi IoT:** tanpa pemicu suhu/salinitas, label yang dapat dipertanggungjawabkan adalah “belum ada anomali terukur pada dua parameter”, bukan “bebas ice-ice”. Foto/inspeksi, tanggal pertama gejala, luka/perawatan dan batch bibit tetap dicatat. Sensor EC/suhu tidak menjadi alat deteksi *Vibrio* atau profil mikrobioma.

## 3. Gacura: salinitas rendah harus dibaca bersama nutrisi dan spesies

**WHY:** menguji apakah air tawar alami yang kaya nutrisi dapat mengimbangi efek salinitas rendah; banyak percobaan lama mengencerkan air laut dengan air murni yang sekaligus mengurangi nutrisi.

**HOW:** *K. alvarezii* tambalang, *K. striatus* sacol-green dan *E. denticulatum* spinosum; enam treatment gabungan sumber air–nutrisi–salinitas, n=4 per spesies/treatment, total 72 flask. Salinitas **34, 30, 27, 24** dibuat dengan air laut dan mata air alami. Eksperimen 10 hari pada **29 ± 0,25°C**, cahaya **198 ± 12 µmol photons m⁻² s⁻¹**, fotoperiode 12:12 jam; medium diganti tiap 24 jam dan flask digerakkan pada orbital shaker 200 rpm. Salinitas diperiksa dengan refraktometer terkalibrasi. [P24, Methods PDF hlm. 3–6.]

Contoh dua treatment yang memperjelas konteks, **bukan dua target dosing farm**:

| Treatment | Salinitas dilaporkan | Total inorganic N, µM | PO₄³⁻, µM | NH₄⁺, µM | NO₃⁻, µM |
|---|---:|---:|---:|---:|---:|
| O-LN-34, offshore | 34 | 2,35 | 0,60 ± 0,04 | 1,45 ± 0,24 | 0,72 ± 0,11 |
| N-HN-24, nearshore + mata air | 24 | 14,56 | 1,61 ± 0,24 | 5,44 ± 0,14 | 8,76 ± 1,94 |

Nilai nutrien mean ± SE; total N merupakan total inorganic nitrogen yang dijelaskan metode. [P24, Tabel 1, PDF hlm. 4 / jurnal 914; diperiksa visual.]

**WHAT:** pada *K. alvarezii*, DGR hari 3 tertinggi 6,33%/hari pada N-HN-24; pertumbuhan hari 10 juga mendukung treatment nutrisi tinggi/salinitas rendah tertentu. Pada *K. striatus*, perbedaan pertumbuhan antar-treatment hari 10 tidak signifikan (p=0,0861); jangan meratakan hasil semua spesies. Uptake NH₄⁺ sekitar 86–100% dalam uji 24 jam, bukan threshold konsentrasi atau bukti keharusan memberi pupuk. [P24, Results PDF hlm. 7; Fig. 4 PDF hlm. 9.]

**Batas metode:**

- Salinitas, nutrisi dan sumber air berubah bersama; tidak ada susunan faktorial lengkap yang memisahkan efek salinitas dari efek nutrisi pada semua level. Karena itu “salinitas 24 meningkatkan pertumbuhan dengan sendirinya” bukan kesimpulan yang terisolasi. [reader-inferred; Methods/Tabel 1 PDF hlm. 3–5.]
- Endpoint yang diperiksa adalah uptake, pertumbuhan dan biokimia selama 10 hari; Methods/Results yang diperiksa tidak memuat estimasi risiko/onset IID atau akurasi alarm. Pertumbuhan yang baik tidak menetapkan kebebasan penyakit sepanjang siklus farm. [reader-inferred; cakupan Methods/Results PDF hlm. 3–10.]
- Penulis menyatakan field trial masih diperlukan karena cahaya, suhu dan faktor lapangan lain dapat mengubah respons. [author-acknowledged; Discussion PDF hlm. 12 / jurnal 922.]

**Implikasi IoT:** jangan membuat aturan otomatis `S < 30 → ice-ice`, atau `S = 24 → aman`. Dua angka itu menjadi konteks paparan yang membutuhkan inspeksi dan konteks sumber air/nutrisi. Sensor salinitas tidak memberi konsentrasi nitrat/ammonium; nutrient sampling terpisah dapat menjadi substudi, belum alasan menambah dosing otomatis.

## Sintesis lintas paper dan perubahan pemahaman

**WHY bersama:** ketahanan dan hasil tanaman bergantung pada hubungan paparan–host–kondisi pemeliharaan; sebuah angka lingkungan tidak memiliki arti biologis yang selalu sama.

**HOW berbeda:** P22 memanipulasi cahaya dan membaca fisiologi/transkriptom; P23 memotret asosiasi bakteri pada dua kultur; P24 memanipulasi gabungan salinitas/nutrisi dan membaca pertumbuhan/biokimia. Ketiganya tidak boleh dihitung sebagai tiga pengujian prediksi IID yang setara.

**WHAT paling kuat untuk keputusan saat ini:** ada bukti eksperimen bahwa low light dapat membatasi pertumbuhan pada strain teraklimasi dan bahwa low salinity dengan nutrisi cukup dapat mendukung pertumbuhan. Bukti P23 lebih terbatas secara kausal, tetapi mengingatkan bahwa suhu/salinitas terkendali tidak mengklasifikasikan kesehatan semua kultur.

Hubungan dengan [[Kajian Indikator Warning Ice-Ice - Uji Asumsi Fitur]]: simpulan “belum ada cutoff universal” bertahan. W04 kini mempunyai angka/metode full text; ini pendalaman, bukan temuan yang meniadakan kajian lama. P22 memberi counterexample terhadap narasi “semakin tinggi cahaya selalu semakin buruk”; P23 menambah konteks gene bank terhadap jalur host–mikroba pada [[Sintesis Penyebab Ice-Ice]].

Perbedaan 203 sebagai low pada P22 versus 45–50 pada P23 bukan dua cutoff yang berlawanan: riwayat aklimasi, strain, sistem dan outcome berbeda. P22 melaporkan irradiance permukaan; jangan menyebutnya paparan terintegrasi 24 jam atau mengalikan 910 dengan panjang siang untuk mengklaim DLI penelitian. P24 tidak menguji salinitas di bawah 24, sehingga tidak menjawab apa yang terjadi pada 20 atau 18 untuk cottonii farm kalian.

**Gap bersama:** Methods/Results ketiganya tidak menguji model prospective berbasis dua sensor, horizon notifikasi, sensitivity/false alarm, batas durasi penyakit, atau manfaat tindakan pada farm Pulau Tidung. Tidak ada dasar dari tiga paper ini untuk mengesahkan horizon tiga hari dalam [[Flow Model Proyek - Indikasi Risiko Ice-Ice]]. Ini klaim absence terbatas pada tiga PDF yang diperiksa.

## Angka yang bisa dan tidak bisa dipakai untuk setup

| Angka dari paper | Kegunaan yang sah | Penggunaan yang tidak didukung |
|---|---|---|
| P24: 24/27/30/34 salinitas; 29 ± 0,25°C | Menentukan titik pembanding dalam pembacaan studi; menunjukkan kebutuhan mencakup kondisi lebih tawar dan air laut | Threshold aman/bahaya, spesifikasi akurasi ±0,25°C, rekomendasi menurunkan salinitas |
| P23: 23 ± 2°C dan 34 ppt pada kultur sehat/sakit | Contoh keterbatasan klasifikasi kesehatan dari suhu/salinitas | “23°C menyebabkan IID”, atau “34 ppt pasti aman” |
| P22: 203/627/910 µmol photons m⁻² s⁻¹ | Memahami perlakuan cahaya dan aklimasi | Cutoff UV, rentang optimum pasti untuk farm, diagnosis IID |
| P23: <20 ppt dan 33–35°C di Discussion | Jejak ke studi klasik yang dikutip penulis | Hasil threshold baru dari eksperimen Aguilar; jangan menghitungnya sebagai replikasi |
| 10 hari P24 / 28 hari P22 | Durasi observasi masing-masing studi | Waktu minimum sebelum alarm atau lead time sebelum gejala |

Jika ingin menilai kandidat suhu 32°C dari literatur terdahulu, lihat [[Kajian Indikator Warning Ice-Ice - Uji Asumsi Fitur]] dan P11. Itu bukan threshold yang ditemukan ketiga paper baru. Tidak ada tier 32→33→36 atau cutoff penurunan salinitas tertentu yang divalidasi ulang di sini.

## Usulan pilot dengan sensor temperatur dan salinitas yang sudah ada

**Seluruh angka pada bagian ini adalah rancangan engineering untuk pengumpulan data, bukan hasil tiga paper atau threshold penyakit.** Model sensor, datasheet, konsumsi energi, response time dan metode salinitas belum diberikan; konfigurasi firmware final belum dapat disahkan.

| Bagian | Konfigurasi awal yang dapat diuji | Alasan dan batas |
|---|---|---|
| Lokasi ukur | Suhu dan salinitas pada kedalaman aktual thallus, berdekatan dan selalu terendam selama pengamatan | Hindari suhu udara/pelampung dibandingkan dengan air tanaman. Catat perubahan kedalaman saat pasang; 1 m bukan syarat universal. |
| Target kemampuan instrumen | Sebagai target evaluasi awal: thermometer mencakup 0–50°C dengan ketidakpastian terverifikasi ≤±0,2°C; salinitas mencakup air tawar–laut 0–42 dengan ketidakpastian ≤±0,5 pada rentang kerja farm | Ini kriteria engineering usulan, bukan syarat biologis atau akurasi yang ditetapkan paper. Jangan mengeklaim alat existing memenuhi tanpa kalibrasi dan spesifikasi. Kemampuan baca rentang penuh tidak sama dengan akurasi penuh. |
| Sampling lokal | Kandidat satu pasangan pembacaan tiap 60 detik **jika response/settling time dan energi mendukung** | Pilihan pilot untuk melihat variasi singkat; belum terbukti cadence optimal IID. Jika tidak layak, gunakan cadence lebih lambat yang tercatat, bukan interpolasi seolah sampel nyata. |
| Penyimpanan/ringkasan | Simpan reading asli dan QA; buat ringkasan 5 menit yang menyertakan min/max/mean/jumlah sampel valid | Ringkasan tidak menggantikan data asli; clock, gap dan dropout tetap disimpan. |
| Pengiriman | Dapat dibatch, misalnya tiap 15 menit; timestamp pengukuran dipisahkan dari pengiriman | Cadence komunikasi bukan cadence sampling dan bukan horizon prediksi. Nilai ini belum hasil perhitungan energi/jangkauan. |
| Fitur analisis | Maks/min, perubahan terhadap reading sebelumnya dan 1 jam lalu, serta paparan dalam window 1/6/24 jam | Window ini kandidat analisis, belum duration threshold biologis. Jangan mengisi gap sebagai nol atau “normal”. |
| Outcome pembanding | Inspeksi tanaman terjadwal, misalnya pagi dan sore, serta saat kejadian; foto, waktu pertama gejala dan jumlah diperiksa/terdampak | Frekuensi ini usulan operasional, bukan hasil studi. Tetap inspeksi saat tidak ada alert agar false negative terlihat. |

Flow model 19 Oktober menyebut logger 10–30 menit sebagai target awal. Angka 60 detik di sini adalah **alternatif pilot yang lebih rapat untuk dievaluasi**, bukan perubahan requirement yang sudah disepakati. Dokumen flow dan kode perangkat tidak diubah.

**EC dan salinitas:** jika sensor bekerja melalui conductivity, simpan raw EC, suhu, satuan, versi konversi, pressure/depth bila digunakan, serta nilai salinitas yang diturunkan. Gunakan konversi seawater yang sesuai alat, bukan faktor TDS tetap. GSW `SP_from_C` menerima conductivity **mS/cm**, suhu **°C** dan sea pressure **dbar**, menghasilkan Practical Salinity yang tidak berdimensi (sering ditampilkan sebagai PSU). Jangan mencampurkan Practical Salinity dengan Absolute Salinity g/kg atau label ppt instrumen tanpa mengetahui definisinya; hindari kompensasi suhu ganda bila alat sudah melakukannya. Rentang valid perhitungan juga harus mengikuti algoritma/datasheet. [Dokumentasi resmi TEOS-10/GSW](https://teos-10.org/pubs/gsw/html/gsw_SP_from_C.html).

Panas dapat mengubah conductivity, tetapi kenaikan suhu tidak dengan sendirinya membuktikan jumlah garam meningkat. Karena itu, pernyataan diskusi lama “semakin panas salinitas meningkat” pada [[Diskusi - Mas Ricky (Mentoring IoT dan Pengukuran Kondisi Laut)]] tetap merupakan klaim yang perlu dibedakan dari konversi EC berbasis suhu. Catatan mentoring asli tidak diubah.

**Aturan keluaran pilot:** data tidak valid → “belum dapat dinilai”; perubahan lingkungan → tugas cek/inspeksi menurut aturan eksperimen yang diberi versi; gejala dilaporkan → inspeksi kondisi tanaman meskipun dua sensor normal. Jangan menampilkan persen risiko IID, label aman, atau mengendalikan pemupukan/salinitas otomatis berdasarkan tabel paper ini. Nilai trigger untuk perubahan/durasi masih perlu dipilih bersama ahli, diuji pada data kejadian dan non-kejadian, kemudian dinilai false alarm/kejadian terlewat serta kegunaannya.

## Catatan pemeriksaan metode

Checklist tetap memakai enam kriteria empirical research; status di bawah menyatakan apakah **kelemahan relevan** ditemukan dalam teks yang diperiksa, bukan skor kualitas paper. “none found” tidak membuktikan tidak ada kelemahan lain.

| Kriteria | P22 | P23 | P24 |
|---|---|---|---|
| Research hypothesis clarity | checked: none found | checked: none found | checked: none found |
| Variable operational definitions | checked: found — surface light vs paparan tanaman | checked: found — hanya fraksi culturable | checked: none found |
| Internal validity | checked: found — medium Day 0 vs Day 28 untuk RNA/pigmen | checked: found — snapshot tidak menentukan urutan host/mikroba | checked: found — salinitas/nutrisi/sumber air tergabung |
| External validity | checked: found — strain/hatchery/aklimasi bukan farm Tidung | checked: found — dua kultur dalam satu gene bank | checked: found — 10 hari laboratorium bukan satu siklus lapangan |
| Statistical reporting completeness | checked: found — huruf Tabel 1 vs narasi low–medium | checked: none found — analisis dinyatakan deskriptif, bukan inferensial | not checked — tidak mengaudit ulang data/CI/model statistik |
| Conclusion conservatism | checked: found — karaginan langsung belum diukur | checked: none found — causality/representativeness dibatasi penulis | checked: none found — penulis meminta field trial |

Locator serta label author-acknowledged/reader-inferred untuk isu relevan ada pada tiap ringkasan. Tidak dilakukan reanalisis RNA-seq, statistik data mentah, supplementary material, systematic review atau independent expert review.

## Jejak penelusuran dan batas hasil

Pada 20 Oktober 2026, PDF pengguna diekstrak dengan `pdftotext -layout`; cakupan pembacaan: abstract, metode, hasil dan pembahasan/kesimpulan yang relevan. Tabel/gambar dan angka utama diperiksa visual pada P22 PDF hlm. 3/5/6, P23 hlm. 3/11/12 dan P24 hlm. 4/7/9. Tidak mengklaim menelaah setiap referensi primer yang dikutip ketiganya.

Metadata dicocokkan dengan penerbit melalui DOI/halaman OUP dan Wiley. Query: tiga DOI persis, nomenklatur cottonii pada FAO, serta dokumentasi resmi GSW `SP_from_C`. Halaman Wiley Gacura utama sempat gagal dibuka; PDF terindeks penerbit cocok DOI/judul/penulis. Tanggal Aguilar mengikuti PDF dan OUP (10 Juli 2026), bukan rekaman PubMed yang menampilkan tanggal berbeda. Penelusuran hanya untuk identitas dan definisi ukur, bukan pencarian literatur yang menyeluruh atau audit retraction/indexing.

Analisis dibantu AI. Tidak ada pengukuran lapangan baru, rekomendasi produk/pembelian, perubahan firmware/app, training model, atau validasi prediksi penyakit. Pertanyaan yang tetap terbuka: strain cottonii pada farm, kedalaman tanaman, model/akurasi/response time sensor, profil salinitas setelah hujan, nutrisi air dan outcome penyakit berwaktu.

## Terhubung

[[Indeks - Riset Ice-Ice]] · [[Daftar PDF Paper]] · [[Kajian Indikator Warning Ice-Ice - Uji Asumsi Fitur]] · [[Rencana Pengukuran IoT Kondisi Laut - Diskusi Mas Ricky]] · [[Flow Model Proyek - Indikasi Risiko Ice-Ice]] · [[Sintesis Penyebab Ice-Ice]] · [[Matriks Bukti Ice-Ice]] · [[Peta Catatan - Challenge Final]]
