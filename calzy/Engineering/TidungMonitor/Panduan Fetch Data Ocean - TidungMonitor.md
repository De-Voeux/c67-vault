---
type: runbook
project: "[[Challenge Final]]"
created: 2026-10-19
updated: 2026-10-19
status: implemented-poc
tags: [challenge-final, tidungmonitor, python, nasa, pipeline]
---

# Panduan Fetch Data Ocean - TidungMonitor

Satu command untuk menyiapkan Python, mengambil data NASA ocean, memeriksa kualitas, lalu memperbarui bundle TidungMonitor. Panduan ini merupakan snapshot implementasi **19 Oktober 2026**. Kode berada di proyek terpisah; vault menyimpan dokumentasi, bukan salinan aplikasi.

Riwayat dan keputusan proyek: [[Riwayat Pengembangan POC - TidungMonitor]]. Brief sumber: [[Arsip Pengembangan TidungMonitor - 19 Oktober 2026]].

## 1. Mulai dari sini

Buka Terminal, lalu jalankan:

```bash
cd "/Users/cindyram/Documents/Apple/POCApp"
python3 fetch_ocean.py --days 7
```

Default: **tujuh hari kalender sampai hari ini UTC**, seluruh sumber MUR + VIIRS + PACE, semua granule yang ditemukan. Ini rentang permintaan, bukan jaminan tujuh hari mempunyai data valid. Tidak ada jeda delapan hari warisan POWER.

Pemanggilan pertama membuat `.venv-ocean` dan memasang dependency yang dipin. Pemanggilan berikutnya memakai environment yang sama; tidak perlu mengaktifkan venv manual. Requirements dipasang ulang jika fingerprint file requirements berubah. Cache hasil ekstraksi digunakan kembali jika granule/revision, versi produk, seri, konfigurasi dan versi processor cocok.

Jika login Earthdata lokal sudah tersimpan, command memakainya. Jika belum ada, Terminal meminta login. Login ulang secara eksplisit:

```bash
python3 fetch_ocean.py --login --days 7
```

Kredensial tetap lokal; jangan menaruh password/token dalam command, chat, vault, JSON atau Xcode. Login bukan autentikasi di aplikasi iOS. Pemanggilan non-interaktif berhenti jika login belum tersedia.

## 2. Prasyarat

| Kebutuhan | Catatan |
| --- | --- |
| Proyek | `/Users/cindyram/Documents/Apple/POCApp` |
| Python | Versi yang diuji: **3.14**; cek dengan `python3 --version` |
| Internet | Diperlukan untuk pemasangan dependency awal, login, discovery CMR dan pengambilan granule; cache tidak membuat pipeline sepenuhnya offline |
| Earthdata | Akun dan login lokal yang dapat mengakses produk NASA terpilih |
| App iOS | Buka `TidungMonitor.xcodeproj`, scheme **TidungMonitor**, setelah data siap |
| XcodeGen | Untuk perubahan struktur/config Xcode; tidak diperlukan setiap kali isi JSON existing berubah |

Dependency ada di `Tools/ocean/requirements.txt`: earthaccess, xarray, h5netcdf, netCDF4, numpy, pandas, pyarrow, requests, scipy dan h5py. `.venv-ocean`, cache dan kredensial lokal diabaikan Git.

## 3. Contoh pemakaian

**Lihat rencana tanpa network, login, atau setup:**

```bash
python3 fetch_ocean.py --days 7 --dry-run
```

**Sampel cepat satu hari, MUR saja:**

```bash
python3 fetch_ocean.py --start 2025-08-01 --end 2025-08-01 --sources mur --max-granules 1
```

**Backfill satu bulan, semua sumber:**

```bash
python3 fetch_ocean.py --start 2025-08-01 --end 2025-08-31
```

**VIIRS dan PACE untuk rentang terbaru:**

```bash
python3 fetch_ocean.py --days 7 --sources viirs,pace
```

**Coba di output terpisah tanpa memperbarui bundle app:**

```bash
python3 fetch_ocean.py --start 2025-08-01 --end 2025-08-01 --sources mur --max-granules 1 --output /private/tmp/tidung-ocean-trial.json
```

Jika file output terpisah itu sudah ada, default tetap merge dengan riwayat file tersebut. Tidak otomatis digabungkan ke bundle app.

**Bantuan:**

```bash
python3 fetch_ocean.py --help
```

Backfill semua granule dapat lama. Pembatas `--max-granules` berguna untuk uji awal, tetapi hasilnya harus disebut **sampel**, bukan backfill lengkap.

## 4. Seluruh opsi untuk pengguna

| Opsi | Default / fungsi |
| --- | --- |
| `--days N` | Default 7 bila tanggal tidak diberikan; 1–366 hari, berakhir hari ini UTC |
| `--start YYYY-MM-DD` | Awal rentang; wajib bersama `--end` |
| `--end YYYY-MM-DD` | Akhir rentang inklusif; tidak boleh melewati hari ini UTC |
| `--sources all` | Semua collection; ini default |
| `--sources mur` | MUR SST |
| `--sources viirs` | VIIRS SNPP chlorophyll-a, Kd490 dan Rrs443 |
| `--sources pace` | Kedua collection PACE: BGC dan AOP |
| `--sources pace_bgc` | PACE chlorophyll-a saja |
| `--sources pace_aop` | PACE Rrs sekitar 443 nm saja |
| `--sources mur,viirs` | Gabungkan pilihan dengan koma; `all` dipakai sendiri |
| `--max-granules N` | Batas **per collection**, bukan per hari atau per lahan; 0 = semua, default 0 |
| `--login` | Login interaktif lokal sebelum fetch; setelah login, fetch tetap berjalan |
| `--output PATH` | Default bundle app; path relatif dihitung dari direktori Terminal saat command dijalankan |
| `--replace` | Ganti output dengan rentang/sumber run ini, tanpa merge; backup existing tetap dibuat |
| `--dry-run` | Cetak rencana saja, tanpa perubahan environment/data dan tanpa network |
| `--help` / `-h` | Tampilkan bantuan, lalu berhenti |

Gunakan **`--days` atau pasangan `--start` + `--end`**. Jangan mencampur keduanya. Rentang maksimum 366 hari. Flag `--worker` adalah mekanisme internal bootstrap dan bukan opsi pemakaian normal.

## 5. Yang dikerjakan otomatis

1. Validasi argumen tanggal, sumber dan output.
2. Siapkan/reuse `.venv-ocean`; pemasangan dependency diserialkan agar dua proses tidak memasang ke environment yang sama bersamaan.
3. Ambil lock pipeline lokal. Pipeline fetch kedua ditolak selama proses pertama masih berjalan.
4. Pakai login Earthdata tersimpan atau minta login lokal di Terminal.
5. Baca koordinat dan sumber dari `Config/ocean_plots.json` serta `Config/ocean_sources.json`.
6. Temukan collection dan granule lewat CMR; buka science NetCDF melalui earthaccess atau pakai cache ekstraksi yang cocok.
7. Subset bbox, terapkan QA laut, pilih piksel valid terdekat dalam radius, konversi unit, dan simpan provenance.
8. Validasi schema, produk/versi, unit, waktu, koordinat, jarak, metode dan QA sekali lagi sebelum publikasi.
9. Gabungkan hasil dengan riwayat existing, kecuali `--replace` dipilih. Periksa apakah output berubah dari proses lain selama fetch.
10. Simpan backup, lalu tulis output secara atomik. Cetak lokasi report dan ringkasan hasil.

Fetch/discovery/schema/metadata-QA error menghentikan publikasi seluruh run, walaupun sebagian sumber sempat berhasil. Run tanpa satu pun granule science terproses tidak menimpa output. Piksel yang benar-benar diparsing tetapi tertolak QA adalah **missing yang sah**: pipeline dapat berhasil meskipun tidak menghasilkan nilai valid baru.

## 6. Output, cache dan backup

| Lokasi relatif terhadap root POCApp | Isi |
| --- | --- |
| `TidungMonitor/Resources/ocean_observations.json` | Bundle JSON yang dibaca app; default output |
| `.venv-ocean/` | Environment Python khusus pipeline |
| `.ocean-cache/<hash>.json` | Hasil ekstraksi per granule dan konfigurasi |
| `.ocean-cache/runs/<run-id>/fetch.json` | Hasil fetch run ini sebelum merge |
| `.ocean-cache/runs/<run-id>/report.json` | Discovery, collection, granule, jumlah terproses, nilai valid dan error per sumber |
| `.ocean-cache/runs/<run-id>/candidate.json` | Kandidat output yang sudah divalidasi; berguna jika output ternyata berubah saat fetch |
| `.ocean-cache/runs/<run-id>/previous.json` | Backup output sebelum publikasi; ada jika output sebelumnya tersedia dan run mencapai tahap backup |
| `.ocean-cache/runs/<run-id>/result.json` | Ringkasan sukses: output, fetched_valid, total_valid, total_records, report dan backup |
| `.ocean-cache/setup.lock`, `pipeline.lock` | File lock OS lokal; tidak perlu dihapus setelah proses selesai |

Jika fetch berhenti lebih awal, tidak semua file per-run terbentuk. Lihat lokasi run yang dicetak di Terminal. **`fetched_valid` bukan jumlah observasi biologis baru**: bisa termasuk record dari cache yang pernah diunduh. `total_valid` adalah jumlah record valid di output setelah merge, bukan jumlah hari unik atau farm independen.

Waktu perlu dibedakan: `observed_at` = waktu akuisisi/analisis sumber; `retrieved_at` = waktu record diambil/diproses; `generated_at` = waktu ekspor disusun. Cache mempertahankan provenance record. Tanggal ekspor baru tidak membuat pengamatan lama menjadi kondisi sekarang.

## 7. Riwayat dan reset yang disengaja

Default merge mempertahankan record sumber lain serta tanggal yang sudah tersimpan. Merge berulang menjaga jendela ekspor tetap terpisah dan tidak mengisi bulan/tanggal yang belum diambil. Record dari VIIRS tidak dijadikan pengganti PACE. Pembaruan record untuk granule yang sama tidak menggandakan record tersebut.

Jika koordinat plot atau versi dataset berubah, merge dapat berhenti karena konfigurasi konflik. Tinjau konfigurasi dan kontrak Swift terlebih dahulu; jangan menempelkan data lokasi lama ke koordinat baru hanya karena ID sama.

Untuk reset yang memang diinginkan:

```bash
python3 fetch_ocean.py --start 2025-08-01 --end 2025-08-31 --sources mur --replace
```

Contoh tersebut mengganti output dengan **MUR pada rentang itu saja**. Riwayat/sumber lain tidak ikut dipertahankan di output baru. Backup tetap tersedia di run folder. Untuk memulihkan, pilih `previous.json` dari run yang benar, periksa isi dan provenance-nya, lalu salin kembali ke path output setelah memastikan tidak ada pipeline berjalan. Pemulihan backup tidak menjalankan fetch NASA.

## 8. Membaca hasil di app

Setelah command sukses, **build/run ulang app lewat Xcode**. Bundle terpasang di iPhone/simulator tidak berubah hanya karena file di Mac diperbarui.

Alur: peta → kelompok → lahan → **Inspeksi** → **Sumber data** → pilih parameter. Mode NASA membaca data ocean; mode **Placeholder** hanya nilai kosong. Tombol **Muat ulang** membaca ulang bundle yang terpasang atau endpoint bila dikonfigurasi, bukan menjalankan Python/NASA dari telepon.

Mengubah isi resource JSON yang sudah terdaftar tidak memerlukan XcodeGen. Jika mengubah target, scheme, dependency atau struktur/config:

```bash
xcodegen generate
```

Buka `TidungMonitor.xcodeproj`, bukan starter `POCApp.xcodeproj`. Rentang default **app** 90 hari; ini berbeda dari default **command fetch** 7 hari. Data historis Agustus 2025 perlu dipilih melalui rentang tanggal di app atau launch argument pengujian `--live --reference-august`.

## 9. Makna data dan nilai kosong

MUR adalah analisis SST harian dengan pengisian celah, bukan pengukuran di tali. VIIRS dan PACE merupakan sumber terpisah. Kd490 adalah koefisien atenuasi/proksi kejernihan, bukan NTU. Rrs juga bukan NTU; chlorophyll-a bukan biomassa rumput laut atau diagnosis ice-ice.

Pemilihan saat ini: piksel laut valid terdekat, maksimum **2.000 m** dari titik konfigurasi. Radius ini keputusan ekstraksi engineering, bukan ambang biologis atau jaminan akurasi. Farm/batas contoh belum diverifikasi. QA membatasi penggunaan piksel; tidak membuktikan seluruh kontaminasi pesisir telah hilang.

| Alasan kosong | Arti operasional |
| --- | --- |
| `cloud` | Kandidat tidak lolos mask awan/ice sumber |
| `land_mask` | Tidak ada kandidat laut yang diterima oleh mask |
| `shallow_water` | Kandidat tertolak kebijakan shallow-water/COASTZ |
| `qa_rejected` | Tidak ada piksel yang lolos QA lain |
| `no_nearby_pixel` | Tidak ada piksel yang dapat dipakai dalam radius |
| `no_swath` | Tidak ada cakupan yang tersedia pada hasil pencarian/ekstraksi untuk slot tersebut |
| `not_processed` | Belum diproses karena pembatasan sampel granule |
| `variable_unavailable` | Variabel yang diminta tidak tersedia pada granule |
| `authentication_required` | Akses autentikasi gagal; command utama menghentikan publish |
| `dependency_missing` / `unsupported_product` | Dependency, schema, unit atau produk belum dapat dipakai |
| `discovery_error` / `network_error` | Discovery atau akses gagal; bukan bukti laut tidak mempunyai data |
| `outside_export` | Slot yang diminta app tidak ada di ekspor; dibuat sebagai missing oleh service iOS |
| `placeholder` | Mode placeholder di app, bukan observasi NASA |

Nilai kosong tidak menjadi nol dan tidak diinterpolasi untuk menutup gap. Status lahan tetap **Belum dinilai**; keberhasilan fetch bukan validasi risiko penyakit.

## 10. Troubleshooting

| Gejala | Langkah |
| --- | --- |
| `can't open file fetch_ocean.py` | Pindah ke root POCApp atau panggil script dengan path absolut |
| Setup/pip gagal | Cek internet dan `python3 --version`; versi teruji 3.14, detail dependency di requirements |
| HTTP 401/403 atau login diminta | Jalankan command dengan `--login` di Terminal lokal; periksa report akses |
| Command sukses, nilai valid nol | Cek `science_parsed` dan alasan missing. Semua piksel dapat gagal QA, terutama optik pesisir |
| Belum ada science granule diparsing | Output existing dipertahankan; periksa sumber, tanggal, discovery dan report |
| Sebagian sumber gagal | Publish seluruh run dibatalkan; report dan cache sumber yang sempat diproses tersedia untuk diagnosis/retry |
| Proses lama | Banyak granule/akses NetCDF dapat lama. Mulai dengan satu hari, satu sumber, `--max-granules 1` |
| Pipeline lain sedang berjalan | Tunggu proses itu selesai. Menghapus file lock tidak membebaskan lock OS dan dapat merusak koordinasi |
| Output berubah saat fetch | Bundle tidak ditimpa; tinjau candidate dan perubahan dari proses lain sebelum retry |
| Konflik koordinat/versi saat merge | Tinjau konfigurasi dan kontrak app; gunakan `--replace` hanya untuk reset yang sengaja dipilih |
| App masih menampilkan data lama | Build/run ulang app; pastikan rentang, parameter dan mode NASA yang dipilih sesuai |
| Dibatalkan dengan Ctrl-C | Periksa report run terakhir dan file output sebelum retry; interupsi bisa terjadi pada tahap yang berbeda |

Exit code command utama: **0** sukses/help/dry-run; **1** kegagalan pipeline/setup; **2** argumen tidak valid; **130** interupsi. Jangan menyamakan exit code dengan status lingkungan.

## 11. Pengujian dan batas snapshot

```bash
.venv-ocean/bin/python -m unittest discover -s Tools/ocean/tests -v
```

Pada 19 Oktober 2026, **16 test Python lulus**: delapan test adapter dan delapan test pipeline. Cakupan pipeline mencakup fetch gagal, QA salah, missing sah, merge/backup, output diubah proses lain, lock dan jendela ekspor berulang.

Command satu pintu diuji dua kali untuk MUR 1 Agustus 2025, melalui CMR dan cache NASA terverifikasi. Output terpisah berisi enam record valid dan tidak berganda pada rerun. Ini bukan enam observasi baru; SHA-256 bundle app tetap sama. Snapshot bundle app saat pendokumentasian: 33 valid dari sampel 17 granule unik; rincian di [[Riwayat Pengembangan POC - TidungMonitor]].

## 12. Kode dan dokumentasi sumber

Root kode: `/Users/cindyram/Documents/Apple/POCApp`. Snapshot Git: `be4e9e1` ditambah perubahan working tree pipeline yang belum di-commit saat catatan ini dibuat.

- [Command utama](/Users/cindyram/Documents/Apple/POCApp/fetch_ocean.py)
- [Orkestrasi dan validasi pipeline](/Users/cindyram/Documents/Apple/POCApp/Tools/ocean/pipeline.py)
- [Exporter](/Users/cindyram/Documents/Apple/POCApp/Tools/ocean/export.py)
- [Adapter science/QA](/Users/cindyram/Documents/Apple/POCApp/Tools/ocean/adapters.py)
- [Merge ekspor](/Users/cindyram/Documents/Apple/POCApp/Tools/ocean/merge_exports.py)
- [Konfigurasi lahan](/Users/cindyram/Documents/Apple/POCApp/Config/ocean_plots.json)
- [Konfigurasi sumber](/Users/cindyram/Documents/Apple/POCApp/Config/ocean_sources.json)
- [Requirements](/Users/cindyram/Documents/Apple/POCApp/Tools/ocean/requirements.txt)
- [Runbook proyek, termasuk exporter/Parquet tingkat lanjut](/Users/cindyram/Documents/Apple/POCApp/docs/runbook.md)
- [[Indeks - Engineering]] · [[Indeks - Metode dan Rencana]]

Panduan ini mendokumentasikan perilaku implementasi saat itu. Perubahan CLI, konfigurasi, dataset atau kontrak app setelah snapshot perlu dicatat kembali; vault tidak tersinkron otomatis dengan repo kode.
