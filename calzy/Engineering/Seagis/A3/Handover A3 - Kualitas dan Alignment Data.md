---
type: engineering-handover
project: "[[Challenge Final]]"
created: 2026-10-22
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, a3]
source_repo: /Users/cindyram/Documents/Apple/Seagis-Model
source_path: docs/a3/architecture.md
source_commit: e93a005c95d746e6e33a6adad12760e94eb8a6cf
---

# A3 — Kualitas dan alignment data

A3 menghasilkan konteks per jam untuk review kualitas, dengan waktu ketersediaan, identitas input dan keterbatasan spasial yang eksplisit. Nilai sumber tetap berada pada tabel A1/A2. Fitur lag/rolling, training dan evaluasi model berada pada fase selanjutnya.

## Alur dan hasil

1. `seagis_quality.source_bundle()` membaca normalized observations, forecast vintages, kontrak unit, sensor dan mapping untuk satu plot serta rentang maksimal tujuh hari. Histori 72 jam sebelum awal ikut dibaca untuk QC; satu observasi lama terakhir per sensor dipertahankan untuk mengenali outage panjang. Maksimum 20.000 record dan 12 MB.
2. `scripts/quality/alignment.py` membentuk konteks pada setiap jam UTC `[from,to)`. Perhitungan hanya memakai bundle, kebijakan dan kode yang teridentifikasi hash; urutan input tidak mengubah hasil.
3. `seagis_quality.save_snapshot()` memeriksa ulang hash sumber, versi kebijakan/kode, jam, parameter, nilai, metadata, mapping dan cutoff setiap input, termasuk referensi QC. Snapshot serta relasi input disimpan append-only. Input yang berubah sejak pembacaan menyebabkan permintaan rebuild.

| Penyimpanan Supabase | Isi |
|---|---|
| `seagis_quality.policy` | Kebijakan QA, hash JSON kanonik Python, hash kode builder, waktu registrasi |
| `seagis_quality.alignment_snapshot` | Dokumen per jam, report, registry sumber/atribusi, metadata sensor, source/body/manifest hash |
| `seagis_quality.snapshot_input` | FK observasi atau forecast value untuk tiap jam; termasuk input pembanding QC |

`contracts/alignment.schema.json` mendefinisikan dokumen keluaran. `seagis_features.feature_snapshot` tetap fondasi untuk A4; A3 memakai namespace kualitas tersendiri. Seluruh dokumen A3 memiliki `training_authorized=false`. Mode `demo_review` wajib untuk plot sintetis; mode `operational_review` diperuntukkan plot nyata yang kelak diprovisikan.

## Waktu dan pemilihan sumber

Untuk baris pada jam `t`, waktu pengukuran/valid yang mewakili konteks saat itu harus ≤ `t`. Observasi juga harus sudah di-ingest dan diterima pada `t`; forecast harus sudah diterima, di-ingest pada tingkat run maupun value, dan sudah terbit/diinisialisasi bila waktunya diketahui. `issued_at=null` tetap null: receipt/ingest menjadi batas konservatif pengetahuan sistem. Arsip yang diambil hari ini tidak merekonstruksi ketersediaan historis sebelum hari ini.

Mapping harus efektif **dan tercatat** pada cutoff. Migrasi 0005 menambahkan `recorded_at` pada mapping operasional. Mapping lama memperoleh waktu migrasi, sehingga tidak otomatis dianggap sudah diketahui sebelumnya. Mapping menjadi append-only; perubahan menggunakan record baru dengan periode efektif eksplisit. Bridge demo A2 menggunakan `created_at` dan tetap membawa koordinat `example_not_surveyed`.

Observasi dipilih menurut waktu pengukuran terbaru yang tersedia; tie diurutkan menurut availability dan ID. Identitas sensor dan plot tetap dibawa. Forecast dipilih pada mapping yang diketahui, mengutamakan mapping operasional lalu jarak terdekat dan key stabil. Pada grid itu dipilih vintage tersedia terbaru yang memiliki titik untuk parameter dan waktu konteks, lalu valid time terbaru ≤ `t`. Titik missing pada vintage terbaru dipertahankan sebagai missing; tidak diganti diam-diam dengan nilai vintage lama.

Forecast dengan valid time sesudah `t` tetap tersimpan pada A2. Keluaran A3 ini khusus konteks pada jam `t`; penggunaan forecast untuk horizon masa depan membutuhkan definisi fitur/horizon tersendiri pada A4. Valid time masa depan tidak dengan sendirinya berarti leakage bila forecast sudah tersedia pada cutoff.

## Cadence dan missingness

- Sensor: sampel terakhir sampai satu cadence native, termasuk batas tepat satu jam, dapat menjadi konteks dengan `source_time`, umur dan flag `carried_sensor_context`. Umur lebih dari satu cadence menghasilkan `missing_hour`; umur ≥ 7.200 detik menghasilkan `stale_sensor`. Nilai sumber tetap terlihat untuk audit, dengan `usable_context=false` ketika diblokir. Tidak ada observasi baru atau interpolasi yang dibuat.
- Arus/salinitas: titik sebelumnya dapat menjadi konteks sampai sebelum cadence native berikutnya, dengan `carried_context`. Setelah itu `native_step_expired`.
- Nitrate/phosphate harian: satu record sumber dapat dirujuk beberapa baris konteks, dengan `age_seconds`, cadence 86.400 detik dan `daily_context_reused`. Jumlah baris konteks tidak menjadi jumlah observasi independen. Batas interval mean yang belum diketahui tetap `interval_unknown`.
- Presipitasi sum: hanya sesuai dengan akhir interval native pada jam `t`; total jam sebelumnya tidak dipakai sebagai hujan baru pada jam berikutnya.
- Umur vintage memakai batas operasional A2: Copernicus 172.800 detik; Open-Meteo 43.200 detik. Batas ini pemeriksaan kesegaran data, bukan akurasi atau validitas biologis.

`present` dengan nol tetap nol dan ditandai `measured_zero` atau `modeled_zero` sesuai sumber. `missing`, `not_available` dan `below_detection_limit` tetap berbeda. Nilai below detection limit tetap null dengan limit yang diketahui; tidak diganti nol. Payload offline malformed dengan NaN/nonfinite menghasilkan nilai curated null dan flag penolakan, sambil mempertahankan status yang diklaim sumber; normalized database sendiri sudah menolak nonfinite.

## Pemeriksaan kualitas

Kebijakan `pilot-quality-2` pada `config/a3_quality.json` memeriksa pasangan unit native/normalized, kode dan hasil konversi, status/nilai/limit yang konsisten, angka finite, temporal support, interval, duplicate/conflict, stale dan nilai di luar envelope engineering. Identitas forecast yang berbeda adalah vintage, bukan duplikat. Duplikat sensor dengan nilai sama diberi flag; nilai berbeda pada identitas waktu yang sama memblokir konteks. Baseline pembanding rapid-change/flatline juga harus memiliki unit, konversi dan envelope yang valid serta bebas duplikat konflik.

Suhu memakai envelope pilot A1 −5 sampai 60 °C dan perubahan >3 °C terhadap sampel sebelumnya dalam ≤2 jam sebagai flag review engineering. Envelope parameter lain juga hanya QA pilot; tidak mendefinisikan rentang aman rumput laut. Source `suspect`/`rejected` memblokir konteks; status `unreviewed` tetap ditampilkan. Late arrival dan referensi pembanding tidak dapat mengubah hasil baris yang cutoff-nya lebih awal.

Flatline memerlukan ≥12 timestamp berbeda, rentang waktu ≥11 jam dalam jendela 12 jam, serta rentang nilai ≤0,01 °C. Hasilnya `flatline_candidate`, bukan bukti sensor rusak. Drift kalibrasi belum dapat dinilai karena tidak ada referensi terkalibrasi yang berada di lokasi sama; report menyebut ketidaktersediaan itu secara eksplisit. Riwayat aktivasi sensor belum berupa deployment dengan periode efektif; ambigu beberapa sensor pada waktu sama memblokir konteks.

## Batas spasial

Setiap sel regional membawa grid ID, koordinat grid, jarak, metode sampling, depth dan resolusi native bila diketahui. Lebar sel perkiraan memakai konversi derajat ke meter dan diberi label approximate. Jarak >10 km, resolusi >1 km, depth difference >1 m, depth tidak diketahui, land mask dan representativeness belum diverifikasi menghasilkan flag. Angka tersebut aturan review pilot. Land-mask issue memblokir konteks.

Ukuran plot belum tersedia sehingga perbandingan resolusi terhadap ukuran plot tetap `plot_size_unknown`. Resolusi native GFS belum dikunci pada registri; koordinat kembalian provider tidak dipakai untuk menebaknya. Height variabel atmosfer tidak dibandingkan sebagai depth sensor air. Depth comparison hanya memakai deployment aktif dengan kedalaman terukur; sensor dummy saat ini belum memilikinya. Satu sel regional tetap menjadi konteks bersama, tanpa klaim sebagai pengukuran air independen per plot.

## Reproduksibilitas dan akses

Policy version mengikat definisi serta SHA-256 file builder. Mengubah kebijakan/kode memerlukan versi baru sebelum deployment ulang. Hash body dan input manifest memakai serialisasi PostgreSQL; hash kebijakan memakai JSON kanonik Python. Kedua basis berbeda dan tidak boleh dibandingkan seolah encoding sama. Snapshot identik menghasilkan ID yang sama; hasil berbeda untuk key sumber/versi yang sama ditolak.

Worker `seagis_quality_worker` tidak memperoleh table grants, superuser atau bypass RLS. Ia hanya dapat mengeksekusi tiga fungsi privat: source bundle, save snapshot dan readback snapshot. Backend ini melayani operator tepercaya; registrasi code hash adalah identitas implementasi, bukan remote attestation terhadap proses Python. Semua tabel memakai RLS dan trigger append-only. Tidak ada schema baru yang diekspos ke Data API atau token perangkat.

Runtime A3 adalah command Python on demand; database, validasi lineage dan snapshot berada di Supabase. Scheduler A2 masih LaunchAgent Mac. Migrasi ke orchestration cloud memerlukan runtime worker yang disepakati dan tetap menjadi tindak lanjut operasional.


Navigasi: [[Indeks - Engineering]] · [[Provenance A3 - Paket Engineering 22 Oktober 2026]].
