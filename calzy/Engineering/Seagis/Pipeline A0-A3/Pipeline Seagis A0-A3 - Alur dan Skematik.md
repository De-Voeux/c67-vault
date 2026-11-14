---
type: engineering-guide
project: "[[Challenge Final]]"
created: 2026-10-22
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, pipeline, a0, a1, a2, a3]
source_repo: /Users/cindyram/Documents/Apple/Seagis-Model
source_commit: e93a005c95d746e6e33a6adad12760e94eb8a6cf
---

# Pipeline Seagis A0-A3 - Alur dan Skematik

Panduan membaca sistem yang sudah dibuat sampai A3. Diagram menggambarkan aliran implementasi, lokasi proses dan hubungan penyimpanan; diagram lineage merupakan ringkasan, bukan seluruh foreign key database.

PDF: [[Seagis - Pipeline A0-A3.pdf]]. Semua gambar SVG pada catatan ini juga digunakan sebagai diagram vektor dalam PDF. Sumber generator: `build_pipeline_pdf.py` di folder yang sama. Diagram dan dokumen dapat diperbarui bersama tanpa mengubah kode pipeline.

## 01 - Gambaran besar

Seagis sampai A3 mengumpulkan suhu dari jalur IoT dan keluaran model regional, mempertahankan asal serta waktunya, lalu menyusun konteks per jam untuk pemeriksaan kualitas. Hasil akhirnya adalah snapshot review yang dapat ditelusuri ke input aslinya.

![[01-overview.svg]]

| Fase | Yang dikerjakan | Hasil utama |
| --- | --- | --- |
| A0 | Menetapkan identitas, kontrak, satuan, waktu dan penyimpanan | Registry, schema, constraint, fixture sintetis dan fondasi lineage |
| A1 | Menerima satu paket suhu melalui HTTPS | Observasi per sensor/plot, receipt idempotent, QC awal dan API history/status |
| A2 | Mengambil empat dataset regional dengan adapter Python | Grid, vintage/run, nilai model, manifest dan status ingestion |
| A3 | Memilih input yang diketahui pada setiap cutoff dan memeriksa kualitas | Konteks UTC per jam, quality report dan snapshot append-only |

Status dokumen: menjelaskan implementasi pada commit `e93a005`. Bukti isi data berasal dari pemeriksaan 22 Oktober 2026 pukul 13:22 WIB; struktur database dari catalog pukul 17:43 WIB. Angka di panduan ini adalah snapshot bukti tersebut, bukan monitoring live saat PDF dibuka.

Plot A/B dan pembacaan IoT masih sintetis. Data Copernicus/Open-Meteo adalah keluaran model regional asli yang dipetakan ke koordinat contoh belum disurvei. Semua hasil A3 membawa `training_authorized=false`. Training, prakiraan suhu Seagis dan integrasi inferensi iOS belum dilaksanakan sampai A3.

## 02 - Di mana proses berjalan dan data tinggal

Satu project Supabase, **seagis-model-database** (`kibztbeviortyvbedogg`), berada di organisasi **Seagis**. Beberapa schema privat di dalam satu PostgreSQL memisahkan tanggung jawab. Schema `public` dapat kosong meskipun data aplikasi tersimpan.

| Komponen | Lokasi runtime | Pemicu dan akses |
| --- | --- | --- |
| Simulator A1 / receiver IoT kelak | Simulator di Mac; receiver pada hardware kelak | Mengirim HTTPS saat ada paket; device token terikat sensor |
| Edge Function `temperature` dan SQL API A1 | Supabase cloud | Aktif ketika request HTTP masuk; login gateway terbatas |
| Dispatcher dan adapter A2 | Python di Mac | LaunchAgent setiap 15 menit mengecek apakah dataset sudah due |
| State jadwal A2 | PostgreSQL Supabase | Menyimpan lease, next attempt dan status; tabel ini tidak mengeksekusi Python |
| Builder QC/alignment A3 | Python di Mac, on demand | Command operator membaca bundle dan membangun dokumen |
| Guard, lineage dan snapshot A3 | PostgreSQL Supabase | Tiga fungsi privat untuk baca sumber, simpan dan readback |

| Schema aplikasi | Isi | Objek pada catalog 22 Oktober |
| --- | --- | --- |
| `seagis` | Registry, plot/sensor, ingestion, observasi, model, grid/mapping dan QC | 13 tabel |
| `seagis_raw` | Manifest raw, hash, metadata dan mode retensi | 1 tabel |
| `seagis_api` | Credential, reader scope, receipt, request event dan policy suhu | 5 tabel |
| `seagis_environment` | Policy, attempt, schedule state, mapping demo dan turunan arus | 4 tabel + 1 view |
| `seagis_quality` | Policy A3, dokumen alignment dan relasi input | 3 tabel |
| `seagis_features` | Kontrak snapshot fitur dan relasi input untuk fase selanjutnya | 2 tabel |

Repo kode, konfigurasi, fixture dan hasil ekspor lokal berada di `/Users/cindyram/Documents/Apple/Seagis-Model`. Folder `data/` adalah artefak lokal yang diabaikan Git. Vault ini menyimpan penjelasan, diagram dan salinan laporan terpilih; ia bukan database operasional. Retensi regional A2 adalah `metadata_only`: tidak ada bucket raw yang otomatis menyimpan semua respons provider.

## 03 - A0: fondasi kontrak dan lineage

A0 menetapkan cara setiap fase menyebut sumber, parameter, lokasi dan waktu. Adapter harus cocok dengan registry dataset: unit asli, unit normalisasi, kode konversi, cadence dan versi. Nilai asli dipertahankan bersama hasil normalisasi.

![[02-lineage.svg]]

Identitas sensor terikat ke plot dan dataset. Identitas grid terikat ke dataset, versi dan kedalaman. Nilai sensor masuk `observation`; nilai model regional masuk `forecast_value` milik sebuah `forecast_run`. Banyak plot dapat memakai konteks dari satu sel grid tanpa menggandakan nilai model menjadi observasi lokal.

Setiap ingestion mempunyai `ingestion_run` dan manifest `raw_payload`. Manifest menyimpan digest, receipt, metadata dan lisensi. Mode `inline` dipakai untuk JSON sintetis; mode `metadata_only` menyimpan provenance tanpa payload lengkap. Mode referensi objek tersedia dalam fondasi, tetapi bucket raw belum dibuat dalam implementasi sampai A3.

| Jaminan | Cara kerja |
| --- | --- |
| Identitas dan satuan konsisten | Foreign key gabungan, CHECK dan kontrak JSON mengikat dataset, unit, asal dan penanda sintetis |
| Retry dapat diaudit | Kunci stabil dan hash membedakan replay identik, konflik paket dan revisi vintage |
| Histori sumber terpelihara | Raw, observasi dan vintage tidak diperbaiki dengan overwrite biasa; hasil baru memakai identitas/versi yang sesuai |
| Snapshot dapat ditelusuri | Relasi input menunjuk observation atau forecast value asli; FK dan hash mengikat manifest |

Tabel `seagis_features.feature_snapshot` dan `feature_input` sudah dibuat sebagai fondasi A4. Keluaran A3 memakai `seagis_quality`, sehingga keberadaan tabel fitur belum berarti fitur lag/rolling atau model sudah dibangun. Tabel state/config tertentu tetap mutable; append-only tidak berlaku otomatis untuk seluruh database.

## 04 - A1: dari paket IoT sampai observasi

Simulator menguji jalur HTTP yang sama dengan receiver IoT kelak. Perangkat mencatat waktu pengukuran UTC, membuat identitas paket dan mengirim satu pembacaan per request. Penetapan plot, dataset dan status sintetis dilakukan server dari sensor terdaftar.

![[03-iot.svg]]

Base URL development: `https://kibztbeviortyvbedogg.supabase.co/functions/v1/temperature`.

| Route setelah base URL | Pemakai | Hasil |
| --- | --- | --- |
| `POST /v1/ingest` | Device token satu sensor | Menyimpan satu paket beserta observasi, QC dan receipt |
| `GET /v1/plots/{plot_id}/temperature` | Reader token dengan izin plot | History, flags, coverage dan pagination; query `from`/`to` UTC |
| `GET /v1/status` | Reader token | Data terakhir, umur/stale dan ringkasan ingestion |
| `GET /health` | Tanpa token | Liveness proses; bukan pemeriksaan kesehatan database |

Contoh paket untuk sensor yang sudah didaftarkan, bukan data lapangan:

```json
{"schema_version":"1.0.0",
 "sensor_id":"<REGISTERED_SENSOR_UUID>",
 "boot_id":"receiver-boot-7b3b3f86","sequence":42,
 "observed_at":"2026-10-22T01:00:00Z",
 "water_temperature":29.2,"unit":"degC",
 "value_status":"present"}
```

Delapan field wajib; field tambahan ditolak. Body maksimal 8.192 byte, `Content-Type: application/json`, dengan `Authorization: Bearer <device-token>`. Null dipakai hanya bersama status `missing` ketika alat eksplisit gagal membaca. Satu jam tanpa paket menjadi gap. Receiver perlu antrean persisten; mekanisme itu adalah persyaratan firmware dan belum diuji pada hardware fisik.

## 05 - A1: transaksi, QC dan pemulihan

Edge Function memvalidasi route/body lalu memanggil SQL privat melalui `seagis_iot_gateway`. SQL memeriksa hash token, expiry/revocation, sensor binding, status deployment dan rate limit. Gateway hanya mempunyai EXECUTE pada `ingest`, `history` dan `status`, tanpa akses tabel langsung. TLS memverifikasi CA dan hostname database.

Satu transaksi menyimpan ingestion, raw manifest, observation, quality event dan packet receipt. Lock transaksi dan unique key melindungi request bersamaan. Identitas paket adalah sensor + boot ID + sequence. Retry tetap memakai identitas dan isi yang sama; reboot baru memakai boot ID baru, sementara paket antrean lama mempertahankan identitas asalnya.

| Respons | Tindakan receiver |
| --- | --- |
| `201 stored` | Terima acknowledgement, simpan ID, lalu keluarkan paket dari antrean; periksa flags QC |
| `200 duplicate` | Acknowledge replay identik; ID observasi tetap sama |
| `409 packet_conflict` | Karantina paket; key sama memiliki isi berbeda dan sumber lama tidak ditimpa |
| `400/413/415/422` | Koreksi format, ukuran, tipe atau nilai yang melanggar kontrak |
| `401/403` | Periksa token, hak akses, sensor dan masa berlaku |
| `429` | Tunggu `Retry-After`; backoff sebelum mencoba lagi |
| Timeout atau gangguan `5xx` | Retry paket sama dengan backoff/jitter; `commissioning_disabled` memerlukan tindakan operator |

QC A1 `pilot-qc-1` menandai suhu di luar -5 sampai 60 degC sebagai rejected; perubahan >3 degC dalam <=2 jam sebagai suspect; timestamp >300 detik di depan sebagai rejected; keterlambatan >7.200 detik sebagai suspect. Clock sedikit maju, missing, gap dan out-of-order juga dibawa sebagai flags. Angka ini envelope engineering pilot, bukan ambang biologis rumput laut.

Paket dengan nilai yang ditolak QC tetap dapat disimpan sebagai observasi audit dan mendapat `201`. Paket malformed atau akses ditolak tidak dibuat menjadi observasi palsu. Database rollback bila transaksi gagal. Log request database tidak mencakup semua trafik: request tanpa autentikasi/rate-limit tertentu hanya muncul di Edge log.

History A1 dapat menghitung nilai present accepted/suspect sebagai usable untuk ringkasan API. A3 lebih ketat: sumber suspect/rejected memblokir `usable_context`. Kedua istilah usable tersebut memiliki tujuan berbeda dan tidak menjadi izin training.

## 06 - A2: sumber, cadence dan jadwal

Empat dataset regional diambil melalui adapter Python. Copernicus menggunakan STAC/Marine Toolbox; Open-Meteo memakai model eksplisit `gfs_global`. Registry/config mengunci identitas, versi yang tersedia, variabel, satuan dan cadence agar perubahan provider tidak bergeser tanpa review.

| Dataset | Isi dan satuan normalisasi | Cadence nilai |
| --- | --- | --- |
| `cmems_salinity_6h` | `so` menjadi salinity, `1e-3`; depth sekitar 0,494 m | Instantaneous 6 jam |
| `cmems_currents_6h` | `uo`/`vo` menjadi komponen timur/utara, `m/s`; depth sekitar 0,494 m | Instantaneous 6 jam |
| `cmems_nutrients_daily` | Nitrate/phosphate, `mmol/m3`; depth sekitar 0,494 m | Mean harian; batas interval belum diketahui |
| `open_meteo_gfs` | Hujan mm, angin 10 m m/s/degree, cloud percent, UV tanpa dimensi, suhu udara 2 m degC | Hourly; hujan adalah sum satu jam sebelumnya |

Salinitas tidak diubah menjadi PSU/ppt. Nutrien tidak otomatis diubah menjadi mg/L. Suhu udara 2 m tidak menjadi suhu air. View `current_speed` menghitung `sqrt(uo^2 + vo^2)` hanya pada run/grid/valid time sama dan mempertahankan referensi dua komponen; A3 saat ini memilih komponen sumber secara terpisah.

| Provider | Slot fetch nominal UTC | WIB | Batas umur vintage |
| --- | --- | --- | --- |
| Copernicus PHY | 08:30 setiap hari | 15:30 | 48 jam |
| Copernicus BGC | 12:30 setiap hari | 19:30 | 48 jam |
| GFS | 04:30 / 10:30 / 16:30 / 22:30 | 11:30 / 17:30 / 23:30 / 05:30 berikutnya | 12 jam |

Dispatcher bangun setiap 15 menit, tetapi fetch hanya ketika due. Cadence nilai, jadwal fetch dan waktu publication berbeda. State jadwal berada di Supabase, sedangkan proses yang mengeksekusinya masih LaunchAgent Mac `org.seagis.environment-ingestion`. Mac harus aktif dan user login. Setelah bangun, worker mengambil window terbaru; vintage yang terlewat tidak otomatis dapat dipulihkan.

## 07 - A2: fetch, persist, vintage dan mapping

![[04-regional.svg]]

Dispatcher mengklaim lease per dataset sebelum network. Lease 20 menit mencegah dua worker memproses dataset sama bersamaan. Adapter melakukan fetch, parse, normalize, validate, lalu persist lewat fungsi privat `claim`, `finish_failure`, `persist`, `status` dan `preview`. Worker tidak diberi akses tabel langsung.

Run key berasal dari identitas semantik, nilai/status/unit, parameter request dan revisi katalog yang relevan. Respons identik menunjuk vintage pertama; perubahan isi atau revisi membentuk vintage baru. Waktu fetch tidak dipakai untuk membuat duplikat baru. `ingested_at` berasal dari server DB saat transaksi dan tidak di-backdate ke valid time.

Raw A2 memakai `metadata_only`: checksum, ukuran, request, metadata katalog, depth, credit dan lisensi. Normalized values tetap tersimpan. Hash Open-Meteo berasal dari bytes JSON respons; hash Copernicus berasal dari ekstrak JSON kanonik Toolbox, bukan bytes transfer NetCDF/Zarr asli. Full raw payload tidak otomatis tersedia untuk replay.

Untuk Copernicus, satu sel geometris terdekat ke titik referensi demo dijaga antartimestamp. Sel termask menjadi missing; tidak berpindah sel diam-diam. Open-Meteo meminta koordinat contoh A/B; bila grid sama, nilai disimpan sekali. `demo_grid_mapping` menghubungkan plot sintetis dengan grid nyata secara eksplisit. Mapping operasional memakai `plot_grid_mapping` dan memerlukan lokasi yang diverifikasi.

Gangguan network/429/5xx dicoba ulang maksimal tiga kali dengan jitter/backoff. `provider_updating`, masalah unit/metadata, lisensi atau autentikasi tidak dipaksa menjadi data baru. Failure persisten menunda retry 15 menit sampai empat jam. Lease proses mati dapat diklaim setelah kedaluwarsa dan attempt lama menjadi abandoned. Kegagalan satu dataset tidak menghentikan dataset lain.

Saat fetch gagal, vintage sebelumnya tetap memiliki umur asli. Preview dapat memberi `cached_after_failure` lalu `stale_unusable`; tidak membuat nilai nol atau timestamp baru. Issued/init time yang tidak terverifikasi tetap null dengan basis unknown. Revisi katalog dan durasi pembuatan respons bukan issue time.

## 08 - A3: QC dan alignment per jam

![[05-alignment.svg]]

Operator menjalankan `scripts/curate_environment.py` untuk satu plot dan rentang `[from,to)` dengan jam UTC utuh, maksimal 168 jam. Plot sintetis wajib `--demo`. `source_bundle()` mengembalikan sumber, registry unit, metadata sensor, mapping dan event QC. Histori 72 jam sebelum awal ditambah satu observasi lama terakhir per sensor membantu mengenali outage; bundle dibatasi 20.000 record/12 MB.

Builder `scripts/quality/alignment.py` memakai bundle, kebijakan `pilot-quality-2` dan kode `a3-alignment-1.0.1` untuk menghasilkan satu baris per jam. Setiap baris hanya memakai input yang tersedia pada cutoff-nya. Registry sumber, attribution, sensor metadata, status nilai, umur, flags, spatial metadata dan referensi input dibawa ke dokumen.

Tanpa `--persist`, command membaca dan membangun hasil untuk operator. Dengan `--persist`, `save_snapshot()` mengambil ulang bundle dan memeriksa source hash, versi policy/kode, nilai, satuan, metadata, mapping, waktu dan semua referensi input termasuk pembanding QC. Perubahan sumber saat proses berjalan meminta rebuild, bukan mengganti hash secara manual.

| Penyimpanan A3 | Peran |
| --- | --- |
| `policy` | Versi definisi QA serta hash policy/kode builder |
| `alignment_snapshot` | Body JSON, hourly rows, report, registry dan source/body/manifest hash |
| `snapshot_input` | FK ke observation atau forecast value asli pada tiap jam; termasuk referensi QC |

Snapshot dan relasi input append-only. Replay identik menghasilkan ID sama; key sumber/versi sama dengan isi berbeda ditolak. Hash adalah identitas/reproduksibilitas, bukan bukti bahwa Python dijalankan pada mesin tepercaya. Worker `seagis_quality_worker` hanya mengeksekusi `source_bundle`, `save_snapshot` dan `snapshot`; runtime ini belum mempunyai endpoint publik iOS atau scheduler cloud.

## 09 - Cutoff dan waktu ketersediaan

![[06-cutoff.svg]]

Contoh ilustratif: suhu diukur 09:00 WIB dan tiba 09:05 WIB. Pada cutoff 09:00 paket belum diketahui, sehingga baris 09:00 tidak boleh memakainya. Pada cutoff 10:00 paket sudah diketahui, tetapi pemakaiannya masih harus lolos umur, cadence dan QC; umur 60 menit dapat diberi `carried_sensor_context`. Upload terlambat tidak mengubah histori pengetahuan sistem.

| Waktu | Arti |
| --- | --- |
| `observed_at` / `valid_at` | Waktu pengukuran sensor / waktu representatif nilai model |
| `received_at` / `available_at` / `ingested_at` | Receipt sumber serta waktu tersedia/tersimpan pada jalur terkait |
| `issued_at` / `model_initialized_at` | Publication dan inisialisasi model, hanya bila terverifikasi |
| Mapping `recorded_at` / `created_at` | Kapan mapping operasional/demo mulai diketahui sistem |
| `as_of` / cutoff baris `t` | Batas informasi yang diizinkan untuk keputusan pada jam tersebut |

A3 saat ini menyusun konteks pada jam t, sehingga source/valid time harus <=t; waktu availability, receipt/ingest, issue/init yang diketahui dan pencatatan mapping juga harus <=t. Mapping harus efektif pada t. Setelah mapping dipilih, builder memilih vintage tersedia terbaru yang memiliki titik untuk parameter/waktu itu, lalu valid time terbaru yang tidak melampaui t. Missing pada vintage terbaru tetap missing.

Forecast dengan valid time sesudah t tetap tersimpan di A2. Forecast yang sudah tersedia pada t dapat dipakai untuk horizon masa depan dalam desain fitur selanjutnya; A3 belum mendefinisikan fitur horizon tersebut. Mengambil arsip hari ini tidak membuktikan arsip itu sudah diketahui sistem kemarin.

Semua waktu database/kontrak memakai UTC; contoh WIB hanya membantu pembaca. Akhir window eksklusif: `[07:00,10:00)` menghasilkan baris 07:00, 08:00 dan 09:00. Cutoff baris terakhir harus sudah berlalu.

## 10 - QC, cadence dan batas spasial

Kualitas nilai sumber, ketersediaan pada cutoff dan kelayakan konteks dibaca bersama. Nilai dapat terlihat dalam audit namun mempunyai `usable_context=false`. A3 tidak menginterpolasi untuk menutup gap dan tidak mengubah nilai tidak tersedia menjadi nol.

| Kasus | Perlakuan A3 |
| --- | --- |
| `present` bernilai 0 | Tetap nol; dibedakan sebagai measured/modelled zero |
| `missing` / `not_available` | Null dengan alasan berbeda; missing sumber berbeda dari sumber/mapping belum tersedia |
| `below_detection_limit` | Null dengan detection limit; tidak diganti nol |
| Unit, konversi, angka atau domain tidak konsisten | Flag teknis dan blokir konteks; source suspect/rejected juga memblokir |
| Sensor lewat satu cadence | `missing_hour`; umur >=7.200 detik menjadi stale; nilai audit tetap terlihat |
| Salinitas/arus 6 jam | Konteks terakhir dapat dirujuk sampai sebelum native step berikutnya, dengan umur/flag |
| Nutrien harian | Input yang sama dapat dirujuk beberapa jam; `daily_context_reused`, interval unknown tetap eksplisit |
| Hujan sum | Hanya dipakai pada akhir interval native yang sesuai; tidak dibawa sebagai hujan baru ke jam berikut |

Rapid-change suhu memakai delta >3 degC pada <=2 jam. Flatline candidate memerlukan >=12 timestamp berbeda, span >=11 jam dalam window 12 jam dan rentang <=0,01 degC. Pembanding QC juga harus valid unit/konversi/domain dan tidak konflik. Kandidat flatline belum membuktikan sensor rusak; drift kalibrasi belum dapat dinilai tanpa referensi terkalibrasi di lokasi sama.

Perbandingan spasial membawa grid, koordinat, jarak, kedalaman, metode sampling dan resolusi bila diketahui. Warning pilot: jarak >10 km, resolusi >1 km dan beda depth >1 m. Land mask memblokir; koordinat contoh, unknown depth/plot size dan representativeness belum terverifikasi tetap diberi flag. Tinggi variabel atmosfer tidak dianggap depth air. Resolusi native GFS belum dikunci; koordinat respons bukan bukti resolusi.

Coverage adalah jumlah/proporsi konteks per jam yang lolos QA, bukan akurasi model, probabilitas penyakit atau jumlah observasi independen. Dua jam yang memakai satu nitrate record tetap satu input native. Envelope QA tidak menyatakan rentang biologis aman.

## 11 - Hasil yang sudah ada dan cara memeriksa

Bukti A3 diperiksa 22 Oktober 2026 sekitar 13:22 WIB; angka berikut tidak diperbarui otomatis. Snapshot catalog terpisah pukul 17:43 WIB mendokumentasikan 28 tabel dan 1 view dalam enam schema aplikasi.

| Bukti tersimpan | Hasil saat inspeksi A3 |
| --- | --- |
| IoT | 136 observasi sintetis, 0 pembacaan sensor nyata |
| Regional A2 | 479 normalized values dalam empat vintages, termasuk 13 salinitas |
| Window A3 terbaru | 21 Okt 07:00 sampai 22 Okt 07:00 UTC, akhir eksklusif; 24 baris per plot |
| Policy 2 per plot | 20 sel konteks parameter-jam regional usable pada cutoff 05:00/06:00 UTC; 23 relasi input |
| Arsip A3 | Empat snapshot keseluruhan; dua policy 1 dan dua policy 2; 48 relasi input |
| Sensor pada snapshot | Nilai historis dummy yang terlihat tetap stale/suspect; 0 konteks sensor usable |

20 sel konteks per plot berarti 10 parameter regional x 2 jam. Salinitas belum masuk snapshot itu: receipt 06:09 UTC terjadi setelah cutoff terakhir 06:00 UTC. Nitrate/phosphate masing-masing tetap merujuk satu record native harian. Snapshot awal policy 1 mempunyai coverage nol karena data/mapping belum tersedia pada cutoff-nya; hasil lama tetap disimpan.

Snapshot policy 2: Plot A `9e47755b-87c1-42cb-ad1f-d2b27ac70293`; Plot B `a8af375a-f39b-43b0-9fef-4a9159242b11`. Buka schema `seagis_quality` di Table Editor atau SQL Editor operator untuk readback. `seagis.observation` dan `seagis.forecast_value` menyimpan sumber; bukan schema `public`.

Bukti pengujian A3 mencatat 94 Python tests, 7 Deno tests, kontrak/lint, offline CLI dan integrasi HTTP Deno dengan PostgreSQL disposable lulus. Pemeriksaan cloud mencakup persist/readback/idempotence dan akses terbatas. Ini hasil yang terdokumentasi pada fase A3; tugas pembuatan panduan ini hanya memeriksa dokumen, diagram dan PDF, tanpa menjalankan ulang ingestion maupun suite kode.

Detail row, hash dan hasil per parameter: [[quality_report_20261022.json]]. Struktur/FK tiap tabel: [[Peta Database Supabase Seagis]]. Pembatasan izin snapshot selalu `training_authorized=false`.

## 12 - Operasi, akses dan handover berikutnya

Jalankan command dari `/Users/cindyram/Documents/Apple/Seagis-Model`. Dua command pertama membaca status/preview A2 yang tersimpan; keduanya tidak memaksa fetch provider.

```sh
uv run --frozen --group environment python scripts/ingest_environment.py status
uv run --frozen --group environment python scripts/ingest_environment.py preview --plot a
```

Contoh membangun dan menyimpan snapshot demo untuk window bukti historis. `--persist` menulis snapshot baru bila kombinasi sumber/versi belum tersimpan; gunakan tanpa flag itu untuk review saja.

```sh
uv run --frozen python scripts/curate_environment.py \
  --plot-id 00000000-0000-4000-8000-000000000001 \
  --from 2026-10-21T07:00:00Z --to 2026-10-22T07:00:00Z \
  --demo --persist --out data/a3/plot-a-report.json \
  --document-out data/a3/plot-a-alignment.json
```

Mode offline memakai `fixtures/a3/synthetic_bundle.json` dengan `--offline ... --demo`. Fixture berisi 12 record sintetis dari database disposable; mode itu tidak dapat melakukan persist cloud. Hasil ekspor di `data/a3/` adalah file lokal, sementara snapshot persist berada di Supabase.

Device hanya menerima URL, sensor ID, device token dan expiry. Reader backend menerima izin plot. `.env.a1.gateway`, `.env.a2.worker`, `.env.a3.worker` adalah credential backend lokal yang diabaikan Git, bukan untuk receiver/iOS/vault. PAT administrator digunakan untuk deployment/registrasi; runtime A1/A2/A3 memakai role terbatas. Tidak ada secret aktual dalam panduan ini.

Untuk memasang IoT nyata: survei koordinat/depth dan kalibrasi alat; buat plot/deployment sensor nyata baru; aktifkan ingestion nyata khusus dataset sensor; provision token sensor; implementasikan antrean, UTC dan boot/sequence; uji koneksi putus/retry/reboot/token dicabut. Dataset regional sudah aktif pada A2; pernyataan nonaktif di handover A1 adalah status historis fase A1. Plot A/B sintetis tidak diubah menjadi identitas lapangan.

A4 selanjutnya dapat membangun fitur dari input dengan cutoff dan lineage yang jelas. Prakiraan suhu memerlukan data lapangan, definisi target dan evaluasi tersendiri. Operasi 24 jam tanpa Mac memerlukan migrasi worker/scheduler ke host cloud; menyimpan state atau menambahkan cron saja belum memindahkan proses Python. Sampai A3, Edge API IoT dan database berada di Supabase, A2 terjadwal di Mac, A3 dijalankan on demand.

## 13 - Sumber implementasi dan navigasi

Panduan ini menyintesis kode dan handover engineering, bukan review literatur atau validasi biologis. Basis implementasi adalah commit `e93a005c95d746e6e33a6adad12760e94eb8a6cf` pada repo Seagis-Model. Tidak dilakukan fetch provider, pembacaan row cloud baru atau perubahan deployment dalam tugas dokumentasi ini.

| Bagian | Source implementasi dalam repo |
| --- | --- |
| A0 | `docs/architecture.md`, `docs/data_contracts.md`, `docs/data_dictionary.md`; `contracts/`; migrasi `0001_initial_schema.sql` |
| A1 | `supabase/functions/temperature/`, `contracts/iot-packet.schema.json`, `scripts/simulate_temperature.py`, `scripts/provision_a1.py`; migrasi `0002_temperature_api.sql` |
| A2 | `scripts/ingest_environment.py`, `scripts/environmental/`, `scripts/install_a2_scheduler.py`, `config/a2_sources.json`; migrasi 0003/0004 |
| A3 | `scripts/curate_environment.py`, `scripts/quality/alignment.py`, `scripts/quality/store.py`, `config/a3_quality.json`, `contracts/alignment.schema.json`; migrasi `0005_quality_alignment.sql` |
| Bukti A3 | `docs/a3/review.md` dan `docs/a3/quality_report_20261022.json` |
| Metadata DB | Salinan catalog read-only `schema-metadata-20261022.json` di folder Database vault |

Jalur baca vault:

- [[Handover A1 - Arsitektur Data dan Akses IoT]] dan [[Operasi A1 - Simulator dan Credentials]].
- [[Handover A2 - Ingestion Lingkungan dan Grid]], [[Operasi A2 - Adapter dan Scheduler]] dan [[Lisensi A2 - Atribusi dan Retention]].
- [[Handover A3 - Kualitas dan Alignment Data]], [[Operasi A3 - Snapshot dan Quality Report]] dan [[Review A3 - Hasil dan Batas Validasi]].
- [[Peta Database Supabase Seagis]] untuk seluruh tabel, kolom dan 47 foreign key pada snapshot catalog.
- [[Indeks - Engineering]] untuk navigasi engineering proyek.

Istilah: **cadence** adalah interval native nilai sumber; **vintage** adalah versi capture/run model yang dipertahankan; **cutoff** membatasi informasi yang sudah diketahui; **lineage** adalah jejak hasil ke input; **QC** memeriksa kualitas teknis; **usable context** menyatakan lolos aturan konteks tertentu, bukan izin training atau diagnosis.

Untuk memperbarui panduan, cocokkan dulu implementasi dan bukti terbaru, ubah catatan ini serta generator bila diagram berubah, lalu bangun ulang PDF/SVG dan periksa hasil render. PDF adalah salinan baca; catatan Markdown merupakan sumber teks yang dapat diedit.
