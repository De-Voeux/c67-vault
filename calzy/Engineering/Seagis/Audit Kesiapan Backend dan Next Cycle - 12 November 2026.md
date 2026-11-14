---
type: engineering-audit
project: "[[Challenge Final]]"
created: 2026-11-12
status: source-audited-live-not-rechecked
tags: [challenge-final, seagis, backend, ios, audit]
---

# Audit Kesiapan Backend dan Next Cycle - 12 November 2026

**Fondasi ingestion, suhu, status perangkat dan konteks regional tersedia untuk pengembangan. Backend belum memenuhi seluruh alur iOS dari petani hingga laporan dan penilaian lahan.** Next cycle sebaiknya menutup identitas petani/lahan, sesi dan kontrak aplikasi, kemudian integrasi dan pengujian lintas plot.

## Cakupan dan arti siap

Audit terhadap [[Kebutuhan Backend untuk iOS - Seagis]] membaca checkout bersih `/Users/cindyram/Documents/Apple/Seagis-Backend` commit `fb485a4` dan aplikasi `/Users/cindyram/Documents/Apple/Seagis` commit `c7fc14e`. Checkout `Seagis-Model` commit `9da4487` terpisah; bukan dasar untuk menyimpulkan API backend operasional terbaru.

“Siap development” berarti tersedia di source dan memiliki fondasi tes, bukan lulus acceptance production. Bukti deployment di bawah berasal dari dokumentasi repo bertanggal; audit ini tidak memakai credential, memanggil API live, membaca catalog cloud atau memverifikasi kesegaran provider. Tidak ada perubahan backend, app, atau deployment.

## Matriks seluruh kebutuhan iOS

| Kebutuhan | Yang sudah ada / status | Persiapan berikutnya |
| --- | --- | --- |
| Tabel petani | Belum ditemukan dalam migrasi backend. App membuat FarmStore dari fixture. | Entitas petani, ID stabil dan aturan data yang dibutuhkan. |
| Relasi petani–lahan | Belum ditemukan pada backend; relasi app masih lokal. | FK/relasi dan aturan kepemilikan versus hak akses; mapping ID app ke ID backend. |
| Kepemilikan dan pemasangan node 1/2 | Parsial: sensor terikat plot dan hub-node terdaftar. Dokumen physical 6 November mencatat dua node pada dua plot berbeda. | Tetapkan pemilik/nama/lokasi lahan; kontrak instalasi dan periode berlaku. Belum terbukti ada histori pemasangan temporal lengkap. |
| Nama, luas, titik, polygon lahan | Parsial: plot bernama dan berkoordinat nullable; migration 0008 menyediakan location version point/polygon dan fungsi registrasi operator. | Luas/unit/asalmya, validasi geometri dan API app. Dua plot physical masih not_surveyed menurut dokumen; dukungan polygon bukan bukti batas lahan sudah terisi. |
| API daftar petani dan lahannya | Belum ada route pada handler. | Kontrak list, pagination, filter scope dan implementasi. |
| API detail lahan untuk map/detail | Belum ada route detail lahan umum. History/environment per plot bukan pengganti detail lahan. | DTO ID, relasi, luas, geometri dan metadata lokasi. |
| Status aktif, last send, baterai, sinyal, stale | Parsial siap backend: `/v1/status`, policy, health dan reason codes tersedia. App memakai InMemorySensorService. | Adapter status iOS, arti status aktif/unknown, waktu health versus observasi, uji tanpa data dan backlog. |
| Suhu node–lahan yang benar | Siap development: sensor.plot_id, binding credential, hub mapping, history; tes dua node dan penolakan mapping berubah tersedia. | Pemetaan lahan nyata dan ID app; uji perpindahan node, histori dan multi-plot dari app. |
| Salinitas, arus, nitrat, fosfat, SST per lokasi | Parsial siap development: ingestion, pemetaan spasial, A3 dan `/v1/plots/{id}/environment`; SST opt-in `include_sst=true`. | Validasi lokasi dan eligibility; refresh snapshot; reader scope; uji live pada plot tujuan. Referensi regional tidak otomatis mewakili lahan. |
| Riwayat dan prakiraan tiga hari | Parsial: history suhu; forecast storage dan environment rentang waktu berbasis snapshot. | Kontrak horizon tiga hari per parameter/run, availability dan cutoff. Jangan menyimpulkan 72 jam lengkap hanya karena storage forecast ada. |
| Tabel dan API laporan ice-ice | Belum di checkout yang diaudit; app InMemoryIceIceReportService. Pekerjaan IID aktif terpisah. | Review dan integrasi hasil tugas `20261112-iid-records-62af`, migrasi, scope tulis, submit/fetch dan snapshot kejadian. |
| Riwayat dan kalender laporan | Kalender/service lokal ada; route backend belum ditemukan. | Query history, agregasi tanggal/zona waktu, filter plot dan integrasi kalender. |
| API penilaian belum dinilai/aman/perlu diperiksa | Belum ada route assessment. Konteks lingkungan bukan assessment; progres app menyatakan tetap belum dinilai. | Aturan dan batas makna, versi, alasan, waktu/input; data tidak cukup menghasilkan belum dinilai. |
| Session sementara tanpa login | Belum ada issuer/session lifecycle untuk app. Backend memakai reader/device credential. Debug memasok token lewat environment; Release provider melempar unauthorized. | Penerbitan sesi, expiry/refresh/revoke dan pemulihan sesi app; mekanisme pemberian hak akses data harus jelas. |
| Pembatasan data dan operasi per session | Parsial: token hash, expiry/revoke, reader_plot dan pemeriksaan plot sudah ada. | Kaitkan sesi baru ke hak data/operasi; scope tulis laporan; negative tests. Hak reader tidak otomatis hak tulis. |
| Pemisahan fisik/regional/forecast/sintetis | Siap sebagai fondasi: provenance/flag registrasi, scope dataset, lineage, commissioning gates, SST terpisah. | Pertahankan pada semua DTO baru, cache, report snapshot dan UI; audit histori lama yang belum pulih terpisah. |
| Waktu, unit, kualitas, sumber dan stale pada API | Parsial siap pada suhu/environment/status; source/available time, flags, lineage dan metadata spasial tersedia. | Konvensi konsisten untuk API baru dan data null; jangan menganggap field/time identik lintas jenis data. |
| Dokumentasi dan JSON tanpa token | Dokumentasi API suhu, physical, environment dan SST serta fixture tersedia. Sebagian dokumen deployment lebih tua daripada source. | Paket kontrak app berversi untuk seluruh endpoint, contoh tersanitasi, error dan skema; perbarui halaman yang tertinggal. |
| Data dev/staging yang dapat diuji iOS | Fixture dan development Singapore terdokumentasi; app mempunyai adapter suhu/regional. | Seed skenario multi-petani/multi-plot, sesi uji terbit melalui alur resmi dan smoke test; staging terisolasi belum dibuktikan siap. |
| Tes mencegah data tertukar antar-plot | Parsial: tes akses reader/plot, binding sensor/hub, provenance dan SST ada. | Tes relasi petani, laporan, sesi baru dan cache/UI lintas plot. Suite backend sekarang belum menguji kontrak yang belum dibuat. |

## Bukti teknis utama

- `supabase/functions/temperature/handler.ts`: route yang diterima adalah health, ingest, hub ingest, status, temperature per plot dan environment per plot. Tidak ada route petani, detail lahan umum, session issuer, laporan atau assessment pada handler ini.
- `supabase/migrations/0001_initial_schema.sql`: plot dan sensor; `0002_temperature_api.sql`: credential, reader_plot, history/status; `0006_hub_simulator.sql`: mapping hub/node dan status health; `0008_spatial_location_mapping.sql`: point/polygon berversi dan spatial gates; `20261106000100_physical_hub_provenance.sql`: physical provenance; `20261110000100_sst_hourly_ingestion.sql`: SST.
- `Seagis/App/AppContainer.swift`: fixture FarmStore, InMemorySensorService, InMemoryIceIceReportService; adapter jaringan suhu/regional, token development dari environment dan provider Release yang belum tersedia. Ini pembatas utama klaim kesiapan app.
- `docs/a1/physical-hub.md`: deployment 6 November dan pemeriksaan historis tercatat, tetapi lokasi/pemilik/kalibrasi belum ditetapkan dan pengukuran aktual firmware masih menunggu pergantian konfigurasi menurut dokumen tersebut.
- `docs/a2/sst-hourly.md`: ingestion SST live dan scheduler Mac tercatat 10 November; host harus awake/logged in. `docs/a3/app_environment_context_api.md` masih menyebut refresh operator dan keterbatasan verifikasi 4 November. Jadwal A2/A3 aktual perlu diverifikasi; dokumentasi ini tidak cukup membuktikan SLA selalu aktif.
- `docs/progress/2026-11-12-trackc-contract-reintegration.md` pada app: SST/reference configurable, quality gates dan cache per reference; probe fisik ditunda; auth Release dan kontrak lain belum tersedia.

## Verifikasi audit ini

Runner resmi `scripts/check_a0.py` dijalankan dengan Python environment backend terhadap PostgreSQL 17 sementara lokal: **133 tes lulus, tidak ada skip yang dilaporkan**, mencakup migrasi, kontrak, database, hub, physical provenance dan SST. Hasil ini memvalidasi source pada database baru, bukan upgrade pada database cloud yang sudah berisi data. Log lokal: `/private/tmp/seagis-backend-audit-tests-20261112.log`.

Audit tidak menjalankan ulang suite HTTP Deno, build/test iOS, pengujian perangkat atau tes API live; kesiapan jaringan, credential/scope live, data terbaru dan deployment parity masih terbuka. Bukti build iOS sebelumnya ada di progres Track C dan tidak dihitung sebagai build audit ini.

## Rekomendasi next cycle

Urutan berikut usulan engineering; semua kebutuhan iOS tetap masuk scope keseluruhan.

| Urutan | Paket kerja | Hasil yang harus tersedia | Kriteria selesai |
| --- | --- | --- | --- |
| 1 | Identitas dan akses aplikasi | Petani–plot, metadata/polygon/luas, instalasi node; session sementara dan matriks izin baca/tulis | Dua petani dengan beberapa plot memiliki ID konsisten; sesi tidak dapat membaca/menulis plot di luar scope; Release memperoleh sesi tanpa token bersama. |
| 2 | Kontrak map, detail dan perangkat | API list/detail, adapter status dan history; pemetaan lokasi dan sumber | Map/detail/status membaca backend dengan ID yang sama; pindah plot/cache tidak menampilkan data plot lain; unknown/stale terlihat benar. |
| 3 | Laporan dan kalender | Integrasi pekerjaan IID aktif, persistensi, submit/fetch, snapshot, history/calendar | Laporan bertahan setelah restart; retry tidak menggandakan laporan; snapshot kejadian tetap; kalender hanya mengagregasi laporan plot yang diizinkan. |
| 4 | Lingkungan dan forecast | Kontrak history/72 jam, eligibility lokasi, provenance dan operasi refresh | Horizon yang tersedia dibuktikan per sumber; gap/null/blocked eksplisit; run/time/unit konsisten; data referensi tidak diam-diam dipetakan ke lahan. |
| 5 | Penilaian dan acceptance | API assessment dengan aturan berversi, dokumentasi lengkap, staging dan contract tests app/backend | Tiga status dapat dijelaskan dengan input/waktu/aturan; data tidak cukup tidak menghasilkan aman; alur petani → plot → sensor → laporan → kalender lolos uji antar-plot. |

Paket 1 merupakan dependensi paket lain. Review rancangan laporan serta penyelarasan kontrak dapat dilakukan sambil menyiapkan paket 1; hindari menduplikasi pekerjaan IID aktif. Bila kapasitas satu cycle terbatas, target reviewable pertama adalah paket 1–3 dengan satu alur lengkap di staging. Forecast dan assessment tetap dicatat sebagai backlog dengan dependensi yang jelas, bukan diasumsikan selesai oleh ingestion existing.

Sebelum menyatakan siap integrasi live: cocokkan commit deploy/migration ledger, terbitkan sesi uji dengan scope benar, periksa snapshot dan cadence aktual, jalankan smoke test authorized/unauthorized pada endpoint tujuan, lalu uji app pada setidaknya dua plot. Penetapan lokasi fisik dan commissioning hardware mengikuti keputusan pengguna; audit ini tidak membuka kembali penundaan probe fisik.

[[Kebutuhan Backend untuk iOS - Seagis]] · [[Indeks - Engineering]]
