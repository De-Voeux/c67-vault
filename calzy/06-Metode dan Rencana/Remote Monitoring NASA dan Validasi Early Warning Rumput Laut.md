---
type: research-brief
project: "[[Challenge Final]]"
created: 2026-10-03
updated: 2026-10-05
status: desk-research-complete-local-validation-needed
scope: "Paket 4 — remote monitoring dan validasi rantai early warning"
tags: [challenge-final, nasa, earth-observation, seaweed, ice-ice, early-warning]
---

# Remote Monitoring NASA dan Validasi Early Warning Rumput Laut

**Jawaban utama:** NASA/EO dapat membantu mendeteksi kondisi lingkungan yang berpotensi meningkatkan risiko sebelum kerusakan tanaman terlihat. Kandidat paling masuk akal untuk diuji adalah **anomali suhu permukaan laut dan hujan yang sudah terjadi**. Namun, sumber yang diperiksa belum menunjukkan bahwa sinyal tersebut menghasilkan peringatan penyakit dengan lead time tertentu atau mengurangi kehilangan di farm dangkal tropis. Ini kesimpulan sintesis, bukan hasil uji sistem lokal. Bukti mekanisme stres tersedia pada eksperimen [Kumar et al., 2020](https://doi.org/10.1371/journal.pone.0239097) dan [Li et al., 2026](https://doi.org/10.1016/j.algal.2025.104474).

Fokus biologis laporan adalah *Kappaphycus* dan *Eucheuma*, terutama sindrom *ice-ice*. Hasilnya tidak otomatis berlaku untuk *Gracilaria* di tambak. Studi dari Filipina, Malaysia, Sulawesi, dan Tanzania juga belum memvalidasi kondisi Pulau Tidung. Pertanyaan yang dijawab: parameter apa tersedia, seberapa dekat dengan kondisi tanaman, dan apakah waktu pengamatan dapat membantu keputusan sebelum kehilangan terjadi?

## 1. Tabel parameter: kemampuan dan batasnya

**Cara membaca:** hubungan biologis dengan kesehatan bukan bukti bahwa parameter satelit itu sudah menjadi prediktor penyakit. Resolusi spasial, interval pengamatan, dan latensi publikasi adalah tiga hal berbeda. Angka di bawah merupakan spesifikasi produk, bukan akurasi yang sudah diuji di Tidung. “NASA/EO” mencakup produk NASA yang memakai satelit mitra, termasuk VIIRS NOAA dan Landsat NASA–USGS.

| Parameter | Hubungan dengan kesehatan/penyakit | NASA/EO yang tersedia | Resolusi dan waktu | Batas di farm dangkal; nilai untuk early warning |
| --- | --- | --- | --- | --- |
| **Suhu / SST dan anomalinya** | Bukti eksperimen kuat bahwa suhu tinggi dapat menurunkan fungsi fisiologis, pertumbuhan, serta mutu. [Kumar](https://doi.org/10.1371/journal.pone.0239097). Hasil lapangan yang membatasi generalisasi dijelaskan di bagian 2. | MODIS L2 SST; VIIRS L2 SST yang didistribusikan NASA. Anomali/durasi paparan dihitung dari seri waktunya. | MODIS sekitar **1 km**, VIIRS sekitar **750 m** di nadir; cakupan nominal sekitar harian–2 hari. L2 NRT biasanya **3–8 jam setelah akuisisi**, menurut [OB.DAAC](https://forum.earthdata.nasa.gov/viewtopic.php?t=5237). [Spesifikasi VIIRS](https://podaac.jpl.nasa.gov/dataset/VIIRS_N20-NAVO-L2P-v3.0). | Awan, piksel campuran daratan–air, dan suhu permukaan yang berbeda dari kedalaman tanaman. Definisi suhu juga bergantung produk: NAVO VIIRS melaporkan estimasi pada 1 m; jangan menyebut semua SST sebagai skin temperature. **Prioritas untuk diuji sebagai sinyal regional**, dipasangkan dengan logger di farm. |
| **Curah hujan** | Jalur tidak langsung: hujan/air tawar dapat mengubah salinitas dan membawa sedimen. Bukti korelasi lapangan dijelaskan di bagian 2. | GPM **IMERG Early V07**, produk gabungan multi-satelit NASA–JAXA/mitra. | Grid **0,1° ≈ 11 km** dekat ekuator; estimasi **30 menit**; Early sekitar **4 jam**. [NASA GPM](https://gpm.nasa.gov/data/imerg), [resolusi](https://gpm.nasa.gov/data/faq). | **Observasi/estimasi hujan, bukan prakiraan.** Tidak mengukur salinitas atau volume air tawar yang tiba di farm. Banyak slot 30 menit diisi estimasi antar-overpass. **Prioritas kedua**, untuk memicu pengukuran salinitas; manfaat waktunya harus diuji. |
| **Salinitas** | Sangat relevan: eksperimen menunjukkan hiposalinitas dapat menyebabkan gangguan fotosintesis sebelum gejala terlihat. [Li et al.](https://doi.org/10.1016/j.algal.2025.104474). | SMAP sea-surface salinity. | RSS: resolusi efektif **40/70 km**, pada grid **0,25°**; JPL memakai grid 25 km dengan footprint sekitar 60 km. [RSS](https://salinity.oceansciences.org/data-smap-v5.htm), [JPL](https://podaac.jpl.nasa.gov/dataset/SMAP_JPL_L2B_NRT2_SSS_CAP_V5). | Grid bukan ukuran detail independen. Kontaminasi daratan membuat pengamatan dekat pantai bermasalah. **Lemah untuk salinitas farm kecil**; gunakan pengukuran lapangan untuk pulsa air tawar. [Batas pesisir](https://salinity.oceansciences.org/data-salinity-05b.htm). |
| **Klorofil-a perairan** | Menunjukkan fitoplankton dan konteks ekosistem. Dalam penelusuran ini belum ditemukan validasi sebagai prediktor *ice-ice* sebelum gejala. | MODIS/VIIRS ocean colour; PACE OCI. | VIIRS L2 **750 m**, MODIS L2 sekitar **1 km**; L3 sering **4/9 km**. PACE OCI footprint **1,2 km** di pusat scan. [OBPG](https://oceancolor.gsfc.nasa.gov/docs/obpg_dmp.pdf), [PACE](https://pace.oceansciences.org/oci.cgi). | **Bukan pengukuran klorofil jaringan rumput laut.** Sedimen, CDOM, pantulan dasar, awan, dan daratan sekitar memengaruhi retrieval. **Parameter pendukung**, tanpa ambang penyakit yang telah tervalidasi. [NASA water quality](https://terra.nasa.gov/citizen-science/water-quality/earth-observation). |
| **Kekeruhan / TSS / plume sedimen** | Relevan terhadap cahaya dan deposisi pada tanaman; hubungan langsung dengan kejadian *ice-ice* perlu dibuktikan per lokasi. | Reflektansi Landsat OLI dapat dipakai untuk estimasi melalui algoritme perairan. | **30 m optik**; Landsat 8 dan 9 masing-masing 16 hari, gabungan nominal **8 hari**. [USGS](https://www.usgs.gov/landsat-missions/landsat-8). | Resolusi bagus untuk pemetaan, tetapi awan dan revisit dapat melewatkan pulsa singkat. Nilai NTU/TSS perlu kalibrasi; kekeruhan tidak mengidentifikasi jenis pencemar. **Pendukung untuk paparan sedimen**, bukan alarm cepat tunggal. [NASA contoh kalibrasi](https://science.nasa.gov/blogs/notes-from-the-field/2019/06/03/on-the-ground-in-belize-to-improve-how-satellites-see-water-quality-from-space/). |
| **Cahaya / PAR / kejernihan Kd490** | Cahaya rendah dapat berinteraksi dengan stres lain dalam pembentukan *ice-ice*. [Largo et al., 1995](https://doi.org/10.1007/BF00003940). | Produk PAR dan koefisien atenuasi Kd490 dari ocean colour. | VIIRS L2 sekitar **750 m**; produk L3 umumnya kilometer dan komposit. [OBPG](https://oceancolor.gsfc.nasa.gov/docs/obpg_dmp.pdf). | PAR permukaan dan Kd490 tidak langsung memberi dosis cahaya yang diterima tanaman. Kedalaman, pasang, dan shading harus diketahui. **Pendukung**, perlu sensor/catatan kedalaman. |
| **Arus / pertukaran air** | Relevan terhadap kondisi budidaya; hubungan lapangan dijelaskan di bagian 2. | NASA-funded OSCAR: analisis arus dari SSH, angin, dan SST melalui model fisik. | Grid **0,25° ≈ 28 km**, rata-rata harian; NRT sekitar **2 hari**. [PO.DAAC OSCAR](https://podaac.jpl.nasa.gov/dataset/oscar_l4_oc_nrt_v2.0). | Analisis mixed layer atas sekitar 30 m; tidak menyelesaikan arus pasang-surut, kanal, atau flushing laguna kecil. **Konteks regional**, bukan kecepatan arus pada tali budidaya. |
| **DO / oksigen terlarut** | Relevan untuk metabolisme dan kualitas air; belum terbukti sebagai indikator awal spesifik *ice-ice* dalam sumber yang diperiksa. | **Tidak diukur langsung** oleh produk satelit tersebut; model dapat mengestimasi. | Tidak ada resolusi pengukuran langsung yang sesuai untuk farm. | DO tidak mengubah sifat optik air secara langsung. Gunakan probe dan pengukuran pada waktu/kedalaman relevan. [NASA ARSET Q8](https://appliedsciences.nasa.gov/sites/default/files/2025-03/Waterborne_Part1_QA.pdf). |
| **pH** | Parameter kualitas air; hubungan lapangan dijelaskan di bagian 2. | Tidak ada pengukuran langsung operasional satelit untuk pH farm; inferensi model mungkin tersedia. | — | Sensor/sampel lapangan dibutuhkan. Estimasi statistik tidak setara pengukuran pH. [NASA](https://science.gsfc.nasa.gov/610/applied-sciences/images/WaterQuality_8-5-2019.pdf). |
| **Nutrien: amonium, nitrat, fosfat** | Penting bagi pertumbuhan; amonium berkorelasi negatif dengan intensitas lesi pada studi 2024. Ini tidak membenarkan pemupukan universal. [Tahiluddin & Terzi](https://doi.org/10.3390/plants13152157). | Tidak langsung; klorofil/ocean colour hanya proksi yang membutuhkan model dan validasi. | — | Klorofil tinggi tidak otomatis nutrien berlebih; klorofil rendah tidak mendiagnosis kekurangan nutrien rumput laut. Gunakan analisis air. [NASA](https://science.gsfc.nasa.gov/610/applied-sciences/images/WaterQuality_8-5-2019.pdf). |
| **Patogen / mikrobioma** | Bakteri oportunistik dapat mempercepat pemutihan pada tanaman stres. [Largo et al., 1995](https://doi.org/10.1007/BF00003941). | Tidak ada diagnosis patogen *ice-ice* langsung dari satelit. | — | Uji kultur/molekuler dan pemeriksaan tanaman diperlukan; kondisi cocok untuk bakteri belum membuktikan infeksi. [NASA batas mikroba](https://science.gsfc.nasa.gov/610/applied-sciences/images/WaterQuality_8-5-2019.pdf). |
| **Epifit, luka, mutu bibit, kesehatan jaringan** | Penting dan dapat menyebabkan perbedaan penyakit meski kondisi air serupa. [Kambey et al., 2021](https://doi.org/10.1007/s10811-021-02530-z). | Belum ada produk NASA operasional untuk diagnosis tersebut pada individu/tali farm. Sensor dekat tanaman dapat membantu deteksi perubahan warna. | Tidak tersedia resolusi diagnostik farm dari produk di atas. | Tetap perlu inspeksi. Studi proximal sensing menggunakan spektrometer dan kamera multispektral pada jarak **1,5 m** dari sampel; hasilnya bukan bukti satelit mendeteksi penyakit sebelum gejala. [Alevizos et al., 2024](https://doi.org/10.3390/rs16183502). |

**Tambahan suhu:** Landsat thermal mempunyai resolusi asli **100 m**, walaupun keluaran sering di-resample menjadi 30 m; resampling tidak menciptakan detail termal 30 m. NASA JPL **MUR** menyediakan analisis SST harian pada grid sekitar 1 km, menggabungkan sensor dan pengamatan lapangan serta mengisi celah. Peta lengkap saat berawan tidak berarti setiap farm diukur hari itu. [USGS Landsat](https://www.usgs.gov/landsat-missions/landsat-8), [NASA MUR](https://podaac.jpl.nasa.gov/MEaSUREs-MUR?sections=data).

## 2. Apakah rantai hipotesis nyata?

**Verdict: didukung sebagian, belum tervalidasi sebagai satu rantai utuh.** Tabel berikut memisahkan mekanisme biologis, perilaku petani, dan keberhasilan informasi.

| Mata rantai | Bukti data | Status dan batas kesimpulan |
| --- | --- | --- |
| Perubahan lingkungan sulit diamati petani | Survei/wawancara **96 petani Sibutu** menunjukkan pengetahuan tentang suhu, hujan, salinitas, arus dan tanda awal penyakit. [Tahiluddin & Eldani-Tahiluddin, 2024](https://doi.org/10.1080/09670262.2024.2383623). | **Perlu diperhalus.** Tidak tepat mengasumsikan petani tidak tahu. Gap yang perlu diuji adalah kemampuan mengukur besar, kecepatan perubahan, dan durasi paparan secara rutin. |
| Perubahan lingkungan → risiko kesehatan meningkat | Eksperimen termal dan hiposalinitas menunjukkan gangguan fisiologi; eksperimen bakteri menunjukkan interaksi host–stres–mikroba. [Kumar](https://doi.org/10.1371/journal.pone.0239097), [Li](https://doi.org/10.1016/j.algal.2025.104474), [Largo](https://doi.org/10.1007/BF00003941). | **Didukung secara mekanistik.** Belum menjadi aturan deterministik atau ambang universal untuk semua strain/farm. |
| Stres → gejala nyata muncul kemudian | Pada eksperimen hiposalinitas *E. denticulatum*, penurunan fungsi fotosistem II mendahului gejala; perlakuan **18 psu selama 12–60 jam** menimbulkan gangguan dan pemutihan. [Li](https://doi.org/10.1016/j.algal.2025.104474). | **Didukung.** Jeda bergantung paparan/host. Interval percobaan bukan lead time satelit atau tenggat tindakan. |
| Gejala muncul → petani baru mengenali masalah | Petani Sibutu mengenali pucat serta epifit/debris sebagai tanda awal. [Survei 2024](https://doi.org/10.1080/09670262.2024.2383623). | **Delay pengenalan belum terukur.** Pengamatan awal memang bisa terjadi; diperlukan waktu kejadian–inspeksi–pengenalan di lokasi target. |
| Setelah dikenali, waktu tindakan terbatas | Studi tiga farm *E. denticulatum* Nain menggambarkan progresi jaringan melemah menuju fragmentasi dalam hitungan hari. Sampling penyakit dua mingguan dan narasi onset tidak konsisten. [Sondak et al., 2025](https://doi.org/10.1007/s44289-025-00065-6). | **Didukung secara kualitatif.** Belum ada jumlah hari universal. Akses farm, tenaga kerja dan kemampuan tindakan juga membatasi respons. |
| Penyakit → kehilangan produksi/mutu | Studi Sabah membandingkan farm dengan paket biosecurity dan tanpa paket tersebut: insidensi rata-rata *K. alvarezii* **4,5% vs 11,5%**; perbandingan thallus terinfeksi/tidak dibersihkan dengan sehat menunjukkan yield karagenan lebih rendah **10–14%**, gel strength **16–45%**. [Kambey et al., 2021](https://doi.org/10.1007/s10811-021-02530-z). | **Didukung**, tetapi hanya satu farm per perlakuan dan tindakan digabung; persentase bukan estimasi efek alarm NASA. |
| Peringatan NASA → waktu tambahan → kehilangan berkurang | Studi EO Bone Bay 2026 memetakan aktivitas/luas budidaya serta hubungannya dengan MODIS SST dan CHIRPS rainfall. Outcome tersebut berbeda dari diagnosis penyakit dan waktu gejala. [Hardiana et al., 2026](https://doi.org/10.1080/01431161.2026.2648101). | **Belum dibuktikan oleh studi yang diperiksa.** Tidak ditemukan pengujian prospektif peringatan NASA dengan lead time, false alarm, dan kehilangan yang berhasil dicegah. |

Ada dua bukti yang menahan generalisasi. Pada **12 farm selama 12 bulan** di Tawi-Tawi, suhu air *in situ*, salinitas, pH, arus, dan angin tidak berkorelasi signifikan dengan *ice-ice*. Hujan berkorelasi lemah dengan panjang lesi (**r=0,232; p=0,005**), tetapi tidak dengan prevalensi (**r=0,002; p=0,982**). Pengukuran air bulanan dapat melewatkan perubahan singkat; hasil ini tidak membatalkan eksperimen, tetapi melemahkan klaim bahwa satu variabel dapat langsung memprediksi penyakit. [Tahiluddin & Terzi, 2024, Tabel 2 dan Discussion](https://doi.org/10.3390/plants13152157).

Di Sulawesi Selatan, fase monsun basah menunjukkan *ice-ice*, tetapi juga menghasilkan pertumbuhan dan produksi tertinggi dari tiga siklus yang diamati. **Peningkatan risiko tidak otomatis berarti hasil total lebih rendah**, karena perubahan lingkungan juga dapat meningkatkan suplai nutrien/pertumbuhan. [Barillé et al., 2025](https://doi.org/10.1016/j.aqrep.2024.102557).

Rantai yang lebih sesuai bukti:

> Perubahan paparan lingkungan + kerentanan bibit/host + mikroba/epifit/praktik → stres fisiologis → kemungkinan gejala dan kerusakan → keputusan serta kemampuan respons → hasil produksi/mutu.

Ini kerangka sintesis untuk diuji. NASA terutama mengisi bagian **paparan lingkungan regional**; inspeksi dan sensor farm mengisi bagian kondisi lokal dan kesehatan tanaman.

## 3. Bagian mana dapat memberi useful head start?

**Peringkat berikut adalah penilaian sintesis terhadap kemampuan produk dan bukti biologis, bukan skor performa sistem yang sudah diuji.**

1. **Anomali SST, perubahan, dan durasinya:** kandidat utama untuk mengidentifikasi paparan panas regional yang sedang berkembang sebelum pemutihan. Periksa kesesuaian dengan suhu pada kedalaman tanaman dan ketersediaan piksel berkualitas. Nilai absolut seperti 30°C tidak cukup menjadi alarm universal. [Kumar](https://doi.org/10.1371/journal.pone.0239097), [batas VIIRS](https://podaac.jpl.nasa.gov/dataset/VIIRS_N20-NAVO-L2P-v3.0).
2. **Hujan yang sudah terjadi:** dapat menjadi pemicu pemeriksaan salinitas dan tanaman, terutama jika jalur air tawar diketahui. Waktu tambahan sebelum stres lokal atau sebelum gejala bergantung proses setempat; kejadian salinitas cepat bisa berlangsung sebelum IMERG Early diterima. [NASA IMERG](https://gpm.nasa.gov/data/imerg), [eksperimen hiposalinitas](https://doi.org/10.1016/j.algal.2025.104474).
3. **Plume sedimen/kejernihan dan klorofil:** dapat membantu menjelaskan paparan dan memprioritaskan lokasi inspeksi, bila retrieval perairan dangkal telah divalidasi. Belum cukup untuk memberi label “penyakit akan muncul”. [NASA kalibrasi pesisir](https://science.nasa.gov/blogs/notes-from-the-field/2019/06/03/on-the-ground-in-belize-to-improve-how-satellites-see-water-quality-from-space/).

Data observasi menunjukkan kondisi yang sudah terjadi. Untuk pemberitahuan **sebelum hujan atau panas terjadi**, perlu komponen prakiraan tersendiri. Latensi produk tidak sama dengan lead time: IMERG empat jam tidak berarti empat jam sebelum penyakit. Demikian juga waktu antara perubahan fotosintesis dan kerusakan di laboratorium tidak sama dengan waktu berguna di farm.

Definisi operasional yang diusulkan untuk uji lokal:

> **Waktu tersisa untuk tindakan = waktu batas tindakan masih bermanfaat − waktu petani benar-benar menerima peringatan.**

Laporkan pula waktu peringatan relatif terhadap **gejala pertama** dan terhadap **pengenalan petani dengan praktik biasa**. Ketiganya berbeda. Ini rancangan evaluasi, bukan hasil penelitian yang telah tersedia.

Validasi minimum yang disarankan: koordinat/poligon farm, spesies dan strain, kedalaman, logger suhu–salinitas, log/foto gejala berwaktu, waktu inspeksi/pengenalan, waktu dan jenis respons, serta biomassa/mutu panen. Uji alert dengan data yang **benar-benar sudah tersedia pada saat alert**, termasuk cloud gap dan latensi. Bandingkan dengan inspeksi biasa; laporkan false alarm, kejadian terlewat, distribusi waktu tambahan, biaya tindakan, dan kehilangan. Tindakan seperti menunda tanam, menambah inspeksi, atau menyesuaikan kedalaman harus diperiksa kelayakannya bersama petani/penyuluh; keberhasilan paket biosecurity tidak membuktikan tiap tindakan efektif secara terpisah. [Kambey et al., 2021](https://doi.org/10.1007/s10811-021-02530-z).

**Framing yang dapat dipakai:** “NASA membantu mendeteksi paparan lingkungan berisiko agar pemeriksaan dan pengambilan keputusan dapat dilakukan lebih awal.” Klaim “memprediksi *ice-ice* 5–7 hari sebelum muncul” masih memerlukan pembuktian lokal.

## 4. Jejak bukti dan batas penelusuran

Penelusuran terarah melalui web dilaksanakan **3 Oktober 2026**, memakai ARS `deep-research` quick mode. Kelompok query: `(Kappaphycus OR Eucheuma) AND (ice-ice OR disease) AND (temperature OR salinity OR rainfall OR light)`; `ice-ice AND (farmer recognition OR response time OR satellite OR early warning OR lead time)`; serta dokumentasi resmi NASA/USGS untuk MODIS, VIIRS, IMERG, SMAP, PACE, Landsat dan OSCAR. Studi primer dipilih untuk mekanisme, data lapangan, pengenalan petani dan kehilangan; dokumentasi institusi dipilih untuk spesifikasi produk. Review, media, dan studi Sargassum hanyut tidak dipakai sebagai bukti prediksi penyakit tanaman budidaya.

Ini bukan systematic review/PRISMA dan tidak memiliki hitungan hasil database yang lengkap. Tidak ada ekstraksi piksel Tidung, uji sensor lokal, model prediksi, atau pengukuran avoided loss. Sebagian artikel hanya dapat dibaca melalui abstrak atau cache teks penerbit; hal itu membatasi penilaian metode. DOI dan identitas publikasi dicocokkan, tetapi audit retraction dan indeks jurnal menyeluruh belum dilakukan. Konsentrasi geografis bukti pada Asia Tenggara mengikuti komoditas target; cakupan dan generalisasi tetap terbatas.

| Sumber ilmiah inti | Jenis bukti dan cakupan baca | Apa yang dapat dibuktikan |
| --- | --- | --- |
| [Kumar et al. (2020), PLOS ONE 15, e0239097](https://doi.org/10.1371/journal.pone.0239097) | Eksperimen satu strain; lima replikasi per suhu. Methods, Results, dan bagian Discussion dibaca. | Respons fisiologis terhadap panas, kerusakan dan mutu; bukan performa prediktor farm. |
| [Li et al. (2026), Algal Research 93, 104474](https://doi.org/10.1016/j.algal.2025.104474) | Eksperimen hiposalinitas *E. denticulatum*; abstrak/highlights dibaca. Kelemahan metode tidak dinilai dari abstrak. | Gangguan fotosintesis mendahului gejala; interval peringatan operasional belum ditentukan. |
| [Largo et al. (1995), Journal of Applied Phycology 7, 539–543](https://doi.org/10.1007/BF00003940) | Eksperimen pemicu lingkungan; abstrak penerbit dibaca. | Mekanisme stres dan pemutihan; tidak dipakai untuk angka onset/ambang salinitas karena teks HTML bermasalah. |
| [Largo et al. (1995), Journal of Applied Phycology 7, 545–554](https://doi.org/10.1007/BF00003941) | Isolasi/challenge bakteri; abstrak penerbit dibaca. | Peran mikroba oportunistik dalam kondisi stres. |
| [Tahiluddin & Terzi (2024), Plants 13, 2157](https://doi.org/10.3390/plants13152157) | Observasional 12 farm/12 bulan; Methods, Results/Tabel 2, Discussion dibaca. | Korelasi lapangan dan hasil negatif; pengukuran bulanan dapat melewatkan pulsa singkat. |
| [Tahiluddin & Eldani-Tahiluddin (2024), European Journal of Phycology 59, 423–435](https://doi.org/10.1080/09670262.2024.2383623) | Mixed methods 96 wawancara dan focus groups; abstrak/highlights penerbit dibaca. | Pengetahuan/tanda awal menurut petani; bukan kronologi paparan yang diukur independen. |
| [Kambey et al. (2021), Journal of Applied Phycology 33, 3179–3197](https://doi.org/10.1007/s10811-021-02530-z) | Perbandingan dua farm, paket biosecurity; Methods/Results/Discussion relevan dibaca. | Manfaat pengelolaan serta kehilangan mutu; satu farm/perlakuan membatasi isolasi efek dan generalisasi (interpretasi pembaca). |
| [Sondak et al. (2025), Discover Oceans 2, 27](https://doi.org/10.1007/s44289-025-00065-6) | Tiga farm Nain; Methods/Results/Discussion relevan dibaca. | Progresi dan hasil pengelolaan; sampling dua mingguan tidak menetapkan tenggat respons yang presisi (interpretasi pembaca). |
| [Barillé et al. (2025), Aquaculture Reports 40, 102557](https://doi.org/10.1016/j.aqrep.2024.102557) | Tiga siklus monsun; abstrak/highlights dan bagian Results/Discussion tersedia melalui salinan artikel. | Penyakit dan pertumbuhan tinggi dapat bersamaan; hubungan kausal tunggal belum ditetapkan. |
| [Hardiana et al. (2026), International Journal of Remote Sensing 47, 4254–4281](https://doi.org/10.1080/01431161.2026.2648101) | EO observasional 2022–2024; abstrak dan bagian Methods/Discussion/Conclusions diperiksa. | Pemetaan aktivitas budidaya dan asosiasi lingkungan; tidak mengukur lead time diagnosis penyakit atau manfaat alert. |
| [Alevizos et al. (2024), Remote Sensing 16, 3502](https://doi.org/10.3390/rs16183502) | Spektroskopi sampel dan imaging dekat tanaman; abstrak, Methods, Results/Discussion diperiksa. | Identifikasi kondisi/depigmentasi; bukan kemampuan satelit mendeteksi stres tanpa gejala. |

**Catatan operasional:** gunakan produk NRT untuk layanan cepat dan pisahkan dari produk refined/komposit untuk analisis historis. Periksa kontinuitas platform dan granule aktual sebelum implementasi; jangan bergantung pada satu sensor. NASA menyampaikan perubahan usia operasi Terra/Aqua, sedangkan produk VIIRS NOAA dapat menjadi bagian kelanjutan pengamatan. [NASA pembaruan misi](https://science.nasa.gov/science-research/earth-science/terra-the-end-of-an-era/), [daftar produk NASA](https://oceandata.sci.gsfc.nasa.gov/file_search/file_search_help/).

**AI disclosure:** Penelusuran, pemeriksaan sumber, dan penyusunan brief dibantu AI. Pernyataan dikaitkan dengan sumber yang tercantum; interpretasi dan kebutuhan validasi dibedakan dari hasil studi. Brief belum direview manusia sebagai laporan final penelitian lapangan.

## Related

- [[Rencana Desk Research Rumput Laut Pulau Tidung]]
- [[Hipotesis Peringatan Dini Kesehatan Budidaya]]
- [[Penginderaan Jauh dan SIG Pesisir]]
- [[Data Lingkungan ke Tindakan]]

## 5. Implementasi eksploratif air busuk Tidung — 5 Oktober 2026

### Tujuan produk

[[Air Busuk Pulau Tidung - Hipotesis dan Langkah Identifikasi]] mendefinisikan air busuk sebagai kondisi air hangat/keruh menurut [[Fauzi]], belum identitas zat atau diagnosis. Kesempatan produk: membantu pelaku mengenali **perubahan kondisi lingkungan yang perlu diperiksa** dan menilai apakah stok bibit perlu dijaga. Nilai tindakan masih harus diperiksa bersama pembudidaya; bukan otomatis perintah rescue atau prediksi ice-ice.

NASA memberi cakupan regional dan seri waktu permukaan. Lapisan partikel bawah laut yang tidak memberi sinyal optik dekat permukaan dapat tidak terdeteksi; tidak ada kedalaman penetrasi tetap yang berlaku untuk semua kondisi air. SST bukan profil suhu 0–50 m. Suhu permukaan normal juga bukan bukti bahwa semua lapisan air aman.

### Data inti dan fungsi

| Data | Fungsi implementasi | Batas |
|---|---|---|
| [MUR SST](https://podaac.jpl.nasa.gov/MEaSUREs-MUR) | Seri waktu suhu permukaan/anomali; grid sekitar 1 km, harian. Simpan uncertainty dan land mask. | Analisis gabungan/interpolasi; setiap grid harian tidak berarti ada observasi langsung harian pada petak. Belum mewakili suhu tanaman atau perubahan singkat. |
| [PACE OCI](https://pace.oceansciences.org/oci.htm) dan [chlorophyll maps](https://pace.oceansciences.org/recentmapdata_daily.htm) | Konteks plankton/warna air dekat permukaan; footprint OCI sekitar 1,2 km di pusat scan. | Klorofil perairan bukan klorofil tanaman, bukan diagnosis pembusukan atau harmful bloom. Produk regional/coarse belum bisa memisahkan petak kecil. |
| [Landsat aquatic reflectance](https://www.usgs.gov/landsat-missions/landsat-provisional-aquatic-reflectance) | Pendalaman pola optik spasial sekitar pulau; gunakan produk/processing untuk perairan. | Produk provisional; algoritme turbidity/TSS harus diperiksa dan dikalibrasi lokal. Jangan menyebut warna sebagai nilai NTU tanpa kalibrasi. Landsat 8/9 masing-masing 16 hari dengan offset 8 hari: [USGS](https://landsat.usgs.gov/landsat_acq). Awan dapat memperpanjang jeda. |
| [IMERG Early](https://gpm.nasa.gov/data/imerg) | Konteks hujan yang sudah terjadi; grid sekitar 11 km, interval 30 menit, latensi sekitar 4 jam. | Bukan prakiraan hujan dan bukan salinitas lokasi. |

Catatan optik dangkal: pasir, lamun, kedalaman/pasang, dan sunglint dapat mengubah warna meski kualitas air tidak memburuk. [NASA interpretasi citra](https://science.nasa.gov/earth/earth-observatory/how-to-interpret-a-satellite-image/). Terapkan [quality flags Ocean Color](https://oceandata.sci.gsfc.nasa.gov/ocl2flags/): mask awan, daratan, glint dan processing failure sesuai produk; shallow/coastal flags memerlukan penanganan tersendiri. Jangan membuang semua piksel turbid secara otomatis karena kekeruhan adalah kandidat sinyal.

### Tahap A — buktikan sinyal dapat diamati

1. Buat GIS titik budidaya, rescue, dan lokasi air busuk menurut ingatan pelaku. Bedakan zona farm dangkal dengan zona selatan lepas pantai; tentukan geometri dari lokasi nyata, jangan menggambar farm fiktif. Zona yang lebih kecil dari satu piksel tidak memberi data independen antarpetak.
2. Pilih rentang historis 6–12 bulan sebagai percobaan awal, dengan tanggal kejadian yang tersedia. Ketepatan tanggal menurut ingatan dicatat sebagai rentang, bukan waktu pasti.
3. Gunakan [Worldview](https://worldview.earthdata.nasa.gov/) untuk melihat pola dan [Earthdata Search](https://search.earthdata.nasa.gov/) untuk memilih granule. Periksa apakah ada piksel laut valid dan berapa banyak hari yang hilang sebelum menyusun model.
4. Bandingkan hari kejadian, hari biasa, dan area pembanding. Cek suhu, optik/klorofil, hujan serta perubahan pasang/kedalaman bila tersedia. Bila laporan tidak punya tanggal cukup spesifik, mulai catatan prospektif; jangan memaksakan pencocokan historis.

### Tahap B — pipeline dan tampilan MVP

Rancangan: Earthdata/OB.DAAC/PO.DAAC → Python ingest dan quality control → ekstraksi nilai per zona → seri waktu dan fitur anomali → API JSON → peta dan catatan kejadian.

Stack yang disarankan sebagai pilihan implementasi: Python dengan earthaccess, xarray untuk NetCDF, dan GeoPandas/rasterio untuk spasial; SQLite untuk prototype kecil; FastAPI untuk API; MapKit/SwiftUI bila output iOS. Ini rancangan, belum kode yang dijalankan. [earthaccess](https://earthaccess.readthedocs.io/en/latest/user/explanation/search/) mendukung pencarian NASA Earthdata; unduhan dapat membutuhkan Earthdata Login. Kredensial tidak disimpan dalam vault.

Simpan per zona dan waktu: observation_time, published/available_time bila tersedia, source_product, processing_version, spatial_resolution, valid_pixel_count, coverage_fraction, nilai, uncertainty, serta alasan data tidak tersedia. Jam observasi dan jam data tersedia dibedakan. L2 swath dan raster L3/analisis membutuhkan ekstraksi spasial berbeda; jangan menganggap semuanya raster reguler.

Fitur awal: selisih SST terhadap baseline musiman lokal, perubahan/penyimpangan klorofil atau reflektansi, serta akumulasi hujan. Baseline memakai data sebelum waktu evaluasi; bila riwayat pendek, beri label baseline sementara dan jangan klaim anomali klimatologis. Jangan menggabungkan piksel berukuran berbeda melalui resampling lalu menganggap resolusinya meningkat.

Tampilan awal menampilkan **data cukup / anomali perlu dicek / data belum cukup**, masing-masing dengan alasan, waktu, sumber, cakupan, dan tingkat dukungan data. Ambang anomali adalah parameter eksplorasi, belum ambang ice-ice. Contoh pesan konseptual: “Suhu permukaan zona ini di atas baseline; perubahan warna air juga terlihat pada pengamatan valid terakhir. Periksa kondisi tanaman.” Jangan menampilkan probabilitas penyakit tanpa model terkalibrasi.

### Tahap C — verifikasi manfaat

Cocokkan sinyal satelit dengan laporan kejadian dan inspeksi biasa; bila tim memiliki alat, prioritaskan suhu/salinitas/DO/kekeruhan pada kedalaman tanaman sesuai hipotesis. Tidak meminta Fauzi mengukur saat spearfishing. Untuk menjelaskan lapisan bawah laut, diperlukan data profil yang sudah ada atau pengambilan oleh tim teknis; sensor permukaan saja tidak menyelesaikan pertanyaan itu.

Evaluasi: cakupan data valid, kejadian terlewat, false alarm, waktu tambahan dibanding inspeksi biasa, tindakan yang berubah, biaya, dan stok/hasil yang bertahan. Sinyal bersamaan dengan kerusakan berarti monitoring; untuk early warning harus terbukti mendahului pengenalan/kerusakan dan masih memberi waktu tindakan. Sedikit kejadian cukup untuk studi kasus, belum untuk akurasi model yang bisa digeneralisasi. Jika satelit tidak menangkap kejadian bawah laut, hasil tersebut menentukan kebutuhan pengamatan lokal.

**Posisi implementasi:** monitoring anomali permukaan/regional adalah tahap awal yang dapat diuji. Deteksi identitas air busuk, prakiraan keberadaannya, dan prediksi ice-ice adalah tiga tahap berbeda yang belum tervalidasi di Tidung. Tidak ada ekstraksi piksel atau prototype baru yang dijalankan dalam pembaruan ini.


## Navigasi kategori

[[Indeks - Metode dan Rencana]] · [[Peta Catatan - Challenge Final]]
