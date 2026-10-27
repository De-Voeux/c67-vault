---
type: engineering-plan
project: "[[Challenge Final]]"
created: 2026-10-27
updated: 2026-10-27
status: planned
scope: A0-A3
tags: [challenge-final, seagis, engineering, plan, track-a]
source_repo: /Users/cindyram/Documents/Apple/Seagis-Model
baseline_commit: 291b6c5fdc7c990660ea98b1dcf676f6c0b58148
requirements_document: TRACK_A_DATA_ML_ENGINEERING_v0.2.md
---

# Rencana Track A v0.2 - Pembaruan A0 sampai A3

## Tujuan dan status

Rencana ini menyelaraskan implementasi Seagis hingga A3 dengan dokumen kebutuhan Track A v0.2 yang diberikan pengguna pada 27 Oktober 2026. Permintaan langsung pengguna adalah menulis plan di Engineering agar agent lain mengetahui pekerjaan yang direncanakan. **Status: perencanaan selesai; pekerjaan implementasi v0.2 di bawah belum dimulai.** Tidak ada perubahan schema, deploy, fetch provider atau training pada tugas penyusunan rencana ini.

Dokumen lampiran dipakai sebagai spesifikasi kebutuhan. Bagian “Agent execution protocol” di dalamnya tidak otomatis menginstruksikan restart A0 atau deploy pada sesi ini. Saat melanjutkan implementasi, cocokkan otorisasi terbaru dari pengguna dan keadaan repo sebelum menjalankan pekerjaan. Cakupan rencana ini A0–A3; A4–A6 hanya batas integrasi mendatang.

Baseline lokal yang diperiksa: repo `Seagis-Model`, branch `feat/contract-A3`, commit `291b6c5` pada 27 Oktober. Migrasi sumber `0001`–`0005` dan adapter A2 diperiksa; cloud tidak dibaca ulang. Hasil cloud/test yang dirujuk handover merupakan bukti 22–23 Oktober, bukan pemeriksaan live 27 Oktober. Snapshot A0–A3 lama tetap valid sebagai catatan scope versi sebelumnya; belum membuktikan seluruh acceptance v0.2 terpenuhi.

## Perubahan utama v0.2 terhadap baseline

| Area | Implementasi yang sudah ada | Tambahan v0.2 yang perlu dikerjakan |
| --- | --- | --- |
| Identitas spasial | `source_grid` saat ini mewakili sel/titik dataset+depth | Pisahkan definisi grid dataset/version dari sel; dukung identitas point API tanpa mengarang native cell ID |
| Lokasi plot | Plot A/B sintetis; koordinat contoh ada di config A2 | Koordinat/geometry configurable, versi lokasi dan provenance saat pindah koordinat |
| Mapping | `plot_grid_mapping` operasional dan bridge `demo_grid_mapping`; waktu pencatatan A3 | Mapping per sumber/variabel/depth, satu/lebih sel bila relevan, versi, requested/sample coordinates, metode, bobot dan validity |
| Dukungan lokasi | Preview/status sumber dan status sensor terpisah secara terbatas | Workflow resolution serta support per dataset; coverage, mapping, sensor dan model dievaluasi terpisah |
| Ingestion | Adapter nyata, vintage immutable, lease/retry; dua plot konfigurasi tetap | Resolve tiap lokasi independen; shared fetch hanya bila semantik sampling sama; active-plot dan on-demand retrieval |
| Pantai/coverage | Mask/missing dan warning jarak/depth ada | Aturan coastal validity/fallback terdokumentasi, fixture unsupported/boundary/cross-land, gagal dengan status eksplisit |
| QA/alignment | As-of, cadence, missingness, lineage dan policy berversi sudah ada | Report mapping validity, coastal evidence dan field-validation status; guard semua versi mapping/cell contribution |
| Tanpa sensor | Plot dan sensor tabel terpisah | Kontrak dan alur eksplisit untuk plot tanpa sensor; konteks regional tetap dapat tersedia, local forecast belum eligible |

Temuan kode yang perlu diperbaiki: Copernicus A2 menghitung titik referensi rata-rata tepat dua plot dari config dan mengambil satu sel untuk keduanya. Cara itu belum menjadi resolver plot arbitrary atau bukti bahwa tiap plot mendapat sel terdekatnya sendiri. Open-Meteo menyimpan returned coordinates sebagai identitas sampling, belum model dukungan lokasi/cache request lengkap. Nilai numerik sama tidak boleh dipakai untuk menyimpulkan identitas sel sama.

## Prinsip yang dipertahankan

- Satu backend Supabase dan worker Python yang koheren. Edge/Cron untuk orchestration ringan jika kelak diperlukan; scheduler A2 saat ini tetap Mac dan A3 on demand sampai ada perubahan runtime yang diminta/dibuktikan.
- Observasi suhu lokal berbeda dari keluaran model regional. Sensor belum terpasang tidak boleh diartikan suhu nol atau menggantinya dengan suhu udara.
- Retensi sesuai produk/lisensi; `metadata_only` tetap pilihan sah. Cache tampilan berbeda dari arsip vintage yang diperlukan reproduksi.
- Waktu UTC, nilai/unit asli dan konversi eksplisit; issue/init unknown tetap null. Contoh `psu` pada assessment lampiran tidak mengubah kontrak salinitas saat ini `1e-3` tanpa dasar konversi.
- Snapshot/raw/normalized historis tidak ditimpa untuk memenuhi schema baru. Seluruh revisi melalui migrasi dan versi kebijakan/kontrak baru yang sesuai.
- Mapping berhasil tidak berarti representatif di farm. Default field status tetap unknown/not field validated sampai ada pembandingan lapangan yang memadai.
- Tidak ada training, probabilitas ice-ice, ambang aman universal, integrasi WeatherKit, atau implementasi layar iOS dalam pekerjaan A0–A3 ini.

## Urutan kerja dan hasil yang harus diserahkan

ID di bawah adalah work package dalam rencana ini, bukan fase baru. Status semua paket: **belum dikerjakan**. Jalankan berurutan sesuai dependency; pembagian paket tidak menginstruksikan spawn agent atau pengerjaan paralel.

### P0 - Audit baseline dan keputusan kontrak

**Dependency:** awal implementasi. **Hasil:** gap checklist aktual, ADR dan daftar keputusan schema/enum.

1. Baca ulang AGENTS yang berlaku, status/diff repo, migrasi terpasang dan ledger cloud melalui akses operator yang dibatasi. Periksa perubahan setelah `291b6c5`; jangan mengasumsikan state lama masih sama.
2. Cocokkan seluruh acceptance A0–A3 v0.2 dengan kode, tests dan bukti. Tandai existing/partial/missing/unknown, bukan sekadar meneruskan label “A3 selesai”.
3. Periksa catalog provider terkini, grid/topology, CRS, mask, variable/depth/time coverage, pemilihan koordinat point API, entitlement, attribution dan retensi sebelum mengubah adapter live. Catat tanggal dan bukti resmi; plan ini belum mengonfirmasi ulang metadata provider.
4. Tetapkan status enums dan null semantics; bedakan coverage unsupported yang dikonfirmasi dari unknown dan error sementara unavailable.
5. Tentukan strategi kompatibilitas terhadap `forecast_value.source_grid_id`, mapping dan snapshot lama. Nomor migrasi berikutnya harus mengikuti ledger aktual; jangan edit `0001`–`0005` yang sudah diterapkan.

**Selesai bila:** keputusan tertulis mengikat identitas grid/cell/point response, support states, versioning lokasi/mapping dan migrasi kompatibel. Ketidakpastian katalog atau izin yang menghalangi live fetch dilaporkan; fixture tetap dapat disiapkan tanpa klaim coverage nyata.

### P1 - A0 tambahan: schema spasial, support dan kontrak

**Dependency:** P0. **Hasil source yang direncanakan:** `docs/spatial_mapping.md`, revisi architecture/source registry/data dictionary/data contracts/ADR, kontrak dan migrasi baru, seed/fixtures.

Rancangan entitas logis berikut harus dituangkan ke DDL setelah review FK/compatibility. Nama fisik final boleh disesuaikan melalui ADR; makna tidak boleh kembali tercampur.

| Entitas | Informasi minimum |
| --- | --- |
| Definisi `source_grid` baru | Dataset/product/grid version, topology regular/irregular/curvilinear, CRS, resolution dan unit/basis metadata, geometry availability, mask policy |
| `source_cell` | FK grid, provider cell ID jika tersedia, basis identitas, index/coordinates yang didukung sumber; geometry/boundary unknown bila tidak diberikan |
| Identitas sample point API | Requested dan returned coordinates, model, sampling/adjustment parameters, identitas request yang dapat direproduksi; native cell ID nullable |
| Versi lokasi plot | Koordinat/geometry input asli, CRS, recorded/effective time, version; tidak mengganti makna lokasi pada data lama |
| `plot_source_mapping` berversi | Plot/location version, dataset/variable/depth, method, status, validity, recorded time, jarak, requested/sample coordinates, evidence/fallback policy version |
| Kontribusi mapping | Satu/lebih cell/sample, bobot bila metode memerlukan, provenance kontributor; tidak memaksakan interpolation untuk nearest sample |
| `location_support` per sumber | Resolution request/status, spatial/temporal coverage, reason/evidence/check time/expiry, dataset version; sensor dan model eligibility terpisah |

Migrasi diusulkan **additive**: buat identitas baru dan bridge eksplisit dari ID lama, backfill hanya fakta yang memang ada, lalu perluas pembaca/guard. Definisi `source_grid` lama adalah identitas sel/titik; jangan mengganti isi/arti baris itu diam-diam menjadi grid definition. Snapshot lama harus tetap dapat direadback dengan versi lama. Inventaris dan verifikasi FK, unique keys, RLS/grants dan hashing sebelum cutover. Unknown metadata hasil backfill tetap unknown; migration time bukan bukti mapping tersedia sebelum migrasi.

Untuk curvilinear/irregular, kontrak menyimpan identitas/index sumber bila tersedia dan menolak asumsi rectangle dari lat/lon spacing. Jika adapter hanya mendukung produk tertentu, beri capability/status eksplisit; jangan mengklaim dukungan semua topology. Saat provider tidak memberi cell ID, pertahankan request/sampling metadata tanpa ID native fiktif.

**Selesai bila:** clean migration + upgrade populated database menjaga UUID/provenance lama, kontrak mencakup no-sensor/unknown/unavailable, dan dua plot dapat merujuk shared source tanpa dua pengukuran independen. Detail test ada pada matriks acceptance.

### P2 - A1 tambahan: lokasi tanpa sensor dan regresi akses IoT

**Dependency:** P1. **Hasil:** fixture plot no-sensor, typed status dan penyesuaian reader/status bila diperlukan, tanpa merusak kontrak paket perangkat.

- Registrasi/resolusi lokasi tidak otomatis membuat deployment atau mengaktifkan sensor. Buat kasus fixture plot tanpa sensor yang tetap dapat menerima konteks regional.
- Endpoint history/status menyatakan tidak ada sensor/tidak ada observasi secara terstruktur; tidak membuat pengukuran nol, status sehat semu atau forecast lokal otomatis.
- Pertahankan auth device/reader, binding sensor-plot, boot/sequence idempotency, delayed observed time, rate limit dan rejected audit. Perubahan koordinat tidak memindah/merelabel histori sensor lama.
- Bila respons berubah, versi kontrak atau adapter kompatibilitas wajib disertai regresi consumer. Jalur registration/resolution awal cukup backend operator/CLI; secured API publik integrasi adalah A6.

**Selesai bila:** no-sensor terlihat eksplisit dan akses history dua plot lama tetap independen; replay/conflict, missing/stale dan otorisasi A1 lulus regresi setelah migrasi.

### P3 - A2 tambahan: resolver per sumber dan reuse/cache

**Dependency:** P1; status no-sensor mengikuti P2. **Hasil:** resolver lokasi backend, adapter/scheduler yang tidak mengandalkan dua koordinat tetap, policy/cache dan evidence provider.

Alur yang ditargetkan:

```text
Koordinat/geometry baru atau berubah
  -> validasi input dan catat location version
  -> resolve coverage/sampling tiap dataset secara independen
  -> mapping version + support/evidence
  -> cek semantic reuse key dan freshness
  -> reuse valid cache atau fetch terbatas
  -> normalized vintage + provenance
  -> konteks regional / status unresolved-unavailable-unsupported
```

1. Validasi koordinat finite, rentang, geometry/CRS dan lokasi terhadap coverage spatial/temporal. Cakupan geografis tidak membuktikan resolusi mapping atau representativeness.
2. Copernicus: hentikan rata-rata dua plot sebagai resolver umum. Resolve tiap plot, kelompokkan fetch hanya sesudah sel/depth/dataset/semantik sampling yang sama terbukti. Pertahankan uo/vo dan derivasi speed dengan pasangan run/grid/waktu yang benar.
3. Open-Meteo: catat requested/returned coordinates, model dan seluruh adjustment/sampling yang memengaruhi respons. Jangan infer boundary/native cell ID dari koordinat returned atau resolusi nominal.
4. Cache key cell-based minimum dataset/version + grid/cell + variable + depth + valid time + run/vintage. Request cache sebelum run diketahui juga memerlukan produk/model/window/sampling policy agar tidak bertabrakan. Untuk interpolation/coordinate adjustment, tambahkan requested coordinates/geometry dan metode/weights/parameters yang relevan; reuse tidak cukup dengan nearest cell.
5. Pisahkan mapping resolution cache, display cache dan archive vintage. Atur TTL/expiry, attribution/retention sesuai produk; sumber diarsipkan hanya bila diizinkan. Perubahan data menjadi vintage baru, bukan overwrite.
6. Refresh active plots mengikuti cadence provider; shared requests didedup berdasarkan keys yang sah. Exploratory lokasi memakai on-demand resolution dengan rate/quota/cost controls dan expiry. Tidak prefetch global.
7. Provider outage menjaga umur sumber asli. Lease/retry/backoff/idempotency yang sudah ada diregresi; unsupported tidak dicoba sebagai kegagalan transient tanpa batas.

**Selesai bila:** dua plot same cell reuse satu sumber, plot ketiga different cell mendapat mapping berbeda walau angka sama, coordinate change membuat versi baru, dan unresolved/unsupported menghasilkan status yang benar. Fixture sah untuk boundary/error dan dilabeli; bukti live hanya untuk lokasi yang benar-benar di-fetch.

### P4 - A3 tambahan: validitas spasial dan report

**Dependency:** P1 + P3; P2 menyediakan fixture no-sensor. **Hasil:** bundle/contract A3 baru, guard/lineage mapping, QC report dan spatial fixtures.

- Perluas source bundle dan snapshot dengan location/mapping version, contributing cells/weights, metode, requested/sample coordinates, resolution beserta unit/basis, depth, mapping validity, coastal evidence dan representativeness status.
- As-of tidak hanya memeriksa observed/valid/issue/ingest: versi lokasi, mapping dan evidence/status yang digunakan harus sudah diketahui pada cutoff serta efektif saat itu. Keputusan dukungan lokasi yang dibuat kemudian tidak boleh mengubah hasil historis.
- Gunakan mask/coastal metadata sumber untuk menerima/menolak sample. Dokumentasikan kriteria sampel yang diperbolehkan dan fallback per produk. Tidak ada silent nearest-valid yang melompati daratan, berpindah water body atau mengganti sel jauh. Bila tidak ada sample acceptable, hasil unavailable dengan reason/evidence; unknown tetap terlihat dan tidak dilabeli valid.
- Bedakan mapping validity dari field-validation/representativeness. Jarak dekat atau sampling sukses tidak mengubah field status menjadi validated. Jika kelak ada comparison lapangan, catat metode, sensor/reference, lokasi/depth, periode dan batasnya.
- Pertahankan QC unit/NaN/null/zero/BDL, duplicate/outlier/stale/gap dan native cadence. Daily nutrient carry tetap input yang sama dengan age. Presipitasi sum tidak dipakai ulang sebagai hujan baru.
- Report per source/parameter/plot/window mencakup coverage, mapping/support validity, coastal/depth uncertainty, field status dan alasan konteks tidak usable. Coarse relative to plot hanya bisa dinilai jika geometry/ukuran tersedia; jika belum, beri unknown.
- Definisi atau kode builder berubah: registrasi policy/builder/schema versi baru dan server guard kompatibel. Jangan mengubah policy `pilot-quality-2` atau snapshot existing. Refresh source hash/body/manifest dengan basis serialisasi yang terdokumentasi.

**Selesai bila:** seluruh acceptance A3 lama dan spatial fixtures baru lulus; unsupported/invalid coastal sample tidak menghasilkan nilai yang tampak valid, dan readback snapshot lama serta snapshot baru deterministik tetap bekerja.

### P5 - Paket review A0–A3 v0.2

**Dependency:** P1–P4. **Hasil:** checklist bukti, handover vault dan keputusan siap/belum siap melanjutkan A4.

Per fase, catat file yang berubah, command yang perlu dijalankan, pemeriksaan yang benar-benar dilakukan, output/bukti, acceptance yang belum terpenuhi dan blocker. Pisahkan tests fixture lokal, bukti deploy cloud dan hasil field validation. Commit setiap perubahan logis dengan Conventional Commits, stage path eksplisit, tanpa push kecuali ada instruksi publikasi.

Perbarui handover A0–A3, kamus database, panduan skematik/PDF dan catatan ekspor CSV bila identitas/kolomnya berubah. Ekspor tetap **satu CSV per fitur** sesuai keputusan pengguna; mapping/grid/location version dan selection basis ikut terbawa. CSV latest-at-capture untuk eksplorasi tidak diberi label backtest as-of. Data lama dan snapshot bukti tidak dihapus untuk memperbaiki coverage.

## Matriks acceptance yang harus dibuktikan

| ID | Kasus | Bukti minimal yang diharapkan |
| --- | --- | --- |
| T01 | Upgrade dari `0001`–`0005` dan database kosong | Migrasi baru lulus kedua jalur; row/ID/FK sumber lama utuh; source ledger konsisten |
| T02 | Dua plot same cell | Satu cell/value source dipakai bersama dengan mapping plot terpisah dan provenance utuh |
| T03 | Different cell dengan nilai sama | Identitas cell/mapping tetap berbeda; dedup tidak didasarkan angka |
| T04 | Coordinate-adjusted/point-interpolated response | Request berbeda tidak salah reuse hanya karena nearest cell sama; cell ID unavailable tetap null |
| T05 | Irregular/curvilinear dan boundary | Kontrak/fixture tidak mengasumsikan rectangle; unsupported capability/status dinyatakan |
| T06 | Coastal land/masked/invalid atau beda water body | Tidak ada penggantian diam-diam; acceptable fallback eksplisit atau unavailable |
| T07 | No coverage, unknown, provider unavailable, resolution pending | Status dan reason berbeda; tidak berubah menjadi nol atau validated support |
| T08 | Plot tanpa sensor | Regional dapat tersedia; local observation tidak tersedia dan local forecast belum eligible |
| T09 | Lokasi/mapping berubah | Versi baru efektif/recorded; histori mapping dan sumber lama tetap; cutoff lama tak memakai versi baru |
| T10 | QC regression | Missing/BDL/zero/NaN/unit mismatch, duplicate/conflict, outlier, out-of-order, gap/stale dan daily context reuse |
| T11 | Leakage dan vintage | Future-issued/late-ingested input serta future-recorded mapping/evidence tidak masuk cutoff lebih awal |
| T12 | Snapshot reproducibility | Sama sumber/versi menghasilkan output sama; readback legacy tetap valid; lineage semua cell/QC reference terverifikasi |
| T13 | Akses dan retry | RLS/EXECUTE roles tetap terbatas; auth/plot binding/no-sensor responses, concurrent replay dan failure recovery |
| T14 | Scheduler/cache dan lisensi | Cadence/TTL/run identity tepat, active/on-demand bounded, outage tidak meremajakan timestamp, attribution/retention terbawa |
| T15 | Handover dan CSV | Dokumen/kamus/payload cocok dengan kode; tiap fitur terpisah, units/cadence/mapping version/availability jelas |

Daftar ini adalah rencana pemeriksaan, **belum hasil test**. Tidak ada test kode atau provider verification baru dijalankan pada tugas plan ini. Suite lama 94 Python + 7 Deno pada handover A3 adalah baseline historis, bukan jumlah target baru.

## Keputusan dan ketidakpastian untuk agent pelaksana

| Hal | Perlakuan dalam rencana |
| --- | --- |
| Rename `source_grid` lama vs tabel baru + bridge | Rekomendasi awal additive + bridge; finalisasi di ADR setelah audit FK/ledger, tanpa overwrite semantik |
| Geometry/CRS dan kebutuhan PostGIS | Pilih dukungan minimum yang benar-benar diperlukan; evaluasi kemampuan DB sebelum menambah extension; jangan mengarang polygon sel |
| Metode sampling awal | Utamakan metode provider yang terdokumentasi; simpan kontribusi untuk multi-cell bila dipakai, bukan memaksakan interpolation |
| Coastal fallback/distance cap | Harus product-specific, versioned dan didukung metadata; angka warning pilot existing bukan bukti validitas lintas daratan |
| Scope wilayah | Koordinat configurable; sumber boleh supported/unsupported/unknown per lokasi. Tidak menjanjikan universal coverage atau transfer model |
| Sensor/model eligibility | Sensor absent/simulated/installed dan model not evaluated terpisah dari regional coverage. Full eligibility/evaluasi model milik A5 |
| Shared assessment 0.2.0 | Siapkan typed support/spatial semantics di kontrak; packet/consumer version adapter direncanakan A6, jangan putuskan Track B diam-diam |
| Runtime cloud | Memindahkan scheduler bukan syarat otomatis dari update spatial; proposal terpisah jika diminta. Tetap jelaskan ketergantungan Mac aktual |

Jika metadata provider tidak memadai untuk membuktikan coastal validity atau cell identity, dokumentasikan keterbatasan dan hasil unavailable/unknown yang tepat. Jangan membuat status “available/valid” untuk menutup gap acceptance. Unknown scientific support tidak diselesaikan dengan test engineering saja.

## Handover untuk agent berikutnya

1. Mulai dari P0, baca dokumen kebutuhan v0.2 asli dan catatan ini; cocokkan perubahan pengguna setelah 27 Oktober. Jangan ulang implementasi A0 lama dari nol.
2. Cek AGENTS, Git root/remote/diff, task aktif dan ownership path. Kode berada di Seagis-Model; seluruh catatan baru di Engineering, bukan Methods. `.agent-work` hanya koordinasi lokal dan tidak di-commit.
3. Klaim file persis dan kunci sesuai aturan vault. Jika file dipakai task lain, tulis draft/handoff; jangan ambil alih lock atau overwrite.
4. Tandai progres P0–P5 beserta commit/bukti dan waktu pemeriksaan dalam catatan ini ketika scope tulis tersedia. Status awal semua paket planned. Dokumen ini membuat pekerjaan terlihat; keberadaannya tidak berarti agent lain sudah diberi tugas atau implementasi otomatis berjalan.
5. Setelah A3 v0.2 direview, laporkan gap yang tersisa sebelum A4. Tidak menjalankan A4/training dari rencana ini.

## Sumber dan navigasi

- Lampiran pengguna: `TRACK_A_DATA_ML_ENGINEERING_v0.2.md`, terbaca pada sesi 27 Oktober 2026; kebutuhan baru A0–A3 dan batas A4–A6. Path asal yang diberikan: `/Users/cindyram/Downloads/TRACK_A_DATA_ML_ENGINEERING_v0.2.md`. Akses path unduhan bisa berubah; isi lampiran menjadi acuan kebutuhan, bukan instruksi operasional otomatis. Tidak membuat klaim diff byte per byte terhadap v0.1; perbandingan di sini terhadap kode baseline.
- Source baseline: `/Users/cindyram/Documents/Apple/Seagis-Model`, `291b6c5`; `supabase/migrations/0001_initial_schema.sql` sampai `0005_quality_alignment.sql`, `scripts/environmental/copernicus.py`, `open_meteo.py`, `common.py`, `config/a2_sources.json` dan `scripts/quality/alignment.py`.
- [[Handover A1 - Arsitektur Data dan Akses IoT]], [[Handover A2 - Ingestion Lingkungan dan Grid]], [[Handover A3 - Kualitas dan Alignment Data]].
- [[Peta Database Supabase Seagis]], [[Pipeline Seagis A0-A3 - Alur dan Skematik]], [[CSV Forecast - Data dan Cara Pakai]].
- [[Indeks - Engineering]].
