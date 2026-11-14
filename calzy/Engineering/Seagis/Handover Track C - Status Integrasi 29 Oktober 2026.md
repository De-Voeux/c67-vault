---
type: engineering-handover
project: "[[Challenge Final]]"
updated: 2026-10-29
status: partial-demo-integration
tags: [challenge-final, seagis, engineering, track-c, handover]
---

# Handover Track C — status integrasi Seagis · 29 Oktober 2026

## Ringkasan untuk penerima

Track C adalah jalur aplikasi iOS Seagis yang menghubungkan produk dengan layanan Track A dan, bila siap, interpretasi Track B. **Track C secara keseluruhan belum selesai.** Saat ini C0 telah diaudit sebagai draft untuk review; C1 memiliki vertical slice demo untuk suhu dan konteks regional yang sudah masuk UI/cache. Belum ada integrasi produksi, pairing, auth pengguna, sinkronisasi umum, laporan lapangan, forecast Seagis, integrasi knowledge produksi, atau release.

Scope kerja yang berlaku mengikuti arahan pengguna setelah rencana awal: lanjut dalam **mode demo tanpa UI login**, fokus ke API → UI, history dan alur; pairing code ditunda; forecast dikerjakan terpisah di Track A; UI parameter regional memakai komponen yang sudah ada. Rencana mandiri `~/Downloads/TRACK_C_INTEGRATION.md` adalah rencana v0.1, bukan bukti bahwa C0–C14 telah dikerjakan. Isi rencana awal yang berbeda dari arahan terbaru tidak dianggap sebagai scope yang masih disetujui.

## Status C0–C14

Status berikut merangkum rencana Track C v0.1 dan memisahkan pekerjaan yang benar-benar ada dari fase yang masih direncanakan.

| Fase | Cakupan rencana | Status saat handover |
| --- | --- | --- |
| C0 | Audit produk, repo, fitur, batas A/B/C, dan dependency | Audit tersedia di [[Status Integrasi Seagis - 28 Oktober 2026]] dan catatan progres lokal. Statusnya draft untuk review; kesepakatan pemilik A/B/C dan fitur rilis belum tercatat. |
| C1 | Kontrak integrasi dan fixture bersama | **Parsial/demo.** DTO suhu, pembacaan API A1, konteks regional A3, cache, dan UI sudah dicoba. Follow-up engineer melaporkan endpoint environment dan snapshot A3 tersedia di Supabase, tetapi panggilan iPhone setelah migration 0008 belum dibuktikan ulang di sesi ini. Kontrak belum final lintas tim dan acceptance C1 belum lengkap. |
| C2 | Repository Swift, cache lokal, mode demo | **Parsial.** Repository dan cache file untuk demo Plot A serta kebijakan refresh 06.00 ada. Belum ada repository/persistence umum untuk akun, plot dinamis, sinkronisasi, dan lifecycle data. |
| C3 | Identitas, izin, keamanan API | Login UI memang ditunda. Sesi acak proxy lokal hanya untuk demo terbatas; bukan auth aplikasi scoped yang siap produksi. Model ownership, revocation, dan akses silang belum diselesaikan. |
| C4 | Registrasi lokasi dan validasi perairan | Belum dimulai; plot UI tetap fixture dan tidak ada registrasi/geospasial baru. |
| C5 | Kondisi dan history live | **Parsial/demo.** History suhu 7 hari dan empat konteks regional dapat dipetakan pada plot demo. Route environment Supabase serta snapshot A3 dilaporkan tersedia, sementara re-verifikasi regional di iPhone setelah migration 0008 masih pending. Belum ada integrasi multi-plot atau verifikasi seluruh state/gap/coverage. |
| C6 | Offline sync, konflik, lifecycle | Cache baca lokal tersedia; outbox, sinkronisasi, konflik, tombstone, logout/purge belum ada. |
| C7 | Laporan kunjungan | Belum dimulai. |
| C8 | Forecast dan warning yang eligible | Tidak diimplementasikan di Track C saat ini; pengguna meminta forecast dipisahkan ke Track A. UI menampilkan forecast 3 hari belum tersedia; jangan membuat nilai prediksi. |
| C9 | Knowledge dan Foundation Models | Belum diintegrasikan. Track B belum menyediakan corpus verified/retrieval produksi menurut catatan status yang dibaca. |
| C10 | Pengujian aplikasi dan UX | Build simulator dan device pernah lulus. Beberapa uji DTO/repository lulus pada checkout sementara. Acceptance menyeluruh, VoiceOver, dan semua state belum diverifikasi. |
| C11 | Operasi produksi dan privasi | Belum dimulai untuk integrasi ini. |
| C12 | TestFlight dan pilot multi-lokasi | Belum dimulai sebagai bagian pekerjaan ini. |
| C13 | App Store readiness dan submission | Belum dimulai; dibahas pada tahap kesiapan App Store sesuai arahan pengguna. |
| C14 | Rilis, pemantauan dan iterasi | Belum dimulai. |

## Yang sudah dikerjakan dan buktinya

### Audit dan batas integrasi

- Menetapkan `/Users/cindyram/Documents/Apple/Seagis` sebagai aplikasi iOS acuan (`Seagis.xcodeproj`, scheme `Seagis`); app memakai SwiftUI/MapKit dan sebelumnya menggunakan fixtures sintetis pada alur peta/detail.
- Mencatat pemisahan tanggung jawab: Track A untuk ingestion/API/model, Track B untuk evidence/review ilmiah, Track C untuk adapter, state, UI, cache, uji dan release.
- Memeriksa kontrak history A1: `GET /v1/plots/{plot_id}/temperature?from=...&to=...`, interval maksimum tujuh hari dengan `next_cursor`; respons membawa unit, waktu pengamatan/ingestion, QC, flags, identitas sensor dan penanda sintetis.
- Mencatat gap yang belum ditutup: reader A1 adalah akses operator, bukan session pengguna; plot ID UI bukan UUID backend; endpoint assessment terpadu, pairing, auth scoped, akses silang, dan semantik produksi belum tersedia/dibuktikan.

### Demo suhu A1: simulator → backend → API → cache/UI

- Untuk demo saja, `plot-madnung-1` di UI dipetakan ke Plot A seed sintetis UUID `00000000-0000-4000-8000-000000000001`; sensor sintetisnya `00000000-0000-4000-8000-000000000101`. Ini tidak membuktikan identitas atau lokasi lahan nyata.
- Simulator mengirim 22 pembacaan sintetis yang tersimpan (`201 stored`); satu paket menghasilkan `409 packet_conflict` pada skenario simulator. History API mengembalikan 22 observasi. Catatan uji melaporkan ID observasi di cache app cocok dengan hasil API.
- App meminta jendela history tujuh hari dan mengikuti pagination. Model DTO mempertahankan nol, null, waktu, QC dan ID; respons invalid, plot tak cocok, dan otorisasi/error tidak menjadi fallback diam-diam pada jalur suhu.
- `TemperatureWidget` lama dipakai untuk nilai/history. Fetch pertama terjadi saat app dibuka tanpa cache; sesudah itu cache diperbarui pada pembukaan app setelah melewati batas pukul 06.00 WIB. Tidak ada timer/background polling. Jika fetch gagal, cache suhu terakhir dipertahankan dan state kegagalan tersedia.
- Akses demo memakai proxy lokal Mac GET-only dengan bearer acak berumur paling lama satu jam. Reader operator hanya berada di proses proxy, tidak ditanam dalam binary. Sesi ini **bukan** kredensial per pengguna atau mekanisme akses produksi.

### Konteks regional A3 pada UI

- Snapshot A3 `demo_review` read-only ditampilkan pada `plot-madnung-1` untuk salinitas, arus laut, nitrat, dan fosfat; respons disimpan di cache lokal app dan dibaca kembali saat pembukaan sesuai kebijakan 06.00 WIB. Checkout lokal `feat/integration` yang diperiksa membuat response `/environment` dengan `curate_environment.py --demo`; ini berbeda dari follow-up engineer yang melaporkan Edge Function environment telah dideploy dan proxy meneruskan request. Source dan jalur yang digunakan perlu disamakan sebelum verifikasi ulang.
- UI dikembalikan ke komponen dan susunan sebelum fetch: `GaugeWidget` untuk salinitas/nitrat/fosfat, `CurrentWidget` untuk arus, dan `TemperatureWidget` untuk suhu. Komponen detail parameter yang sudah ada tetap dipakai; tidak ditambahkan kartu atau halaman custom regional.
- Magnitude dan arah arus diambil dari komponen eastward/northward dengan waktu sumber dan grid yang sama. UI simulator yang diperiksa menunjukkan salinitas 33,3 ppt (nilai sumber 33,3413), arus 0,41 m/s menuju barat, nitrat 0,022 mmol/m³, dan fosfat 0,091 mmol/m³.
- Provenance menyebut konteks model regional, bukan pengukuran langsung. `training_authorized=false`; tidak ada status aman/bahaya atau threshold biologis yang diturunkan dari angka tersebut.

### Follow-up dari iOS engineer · laporan 29 Oktober 2026

Informasi berikut berasal dari file follow-up yang diberikan pengguna. Ini memperbarui gambaran C1, tetapi deployment, snapshot dan status PR belum diperiksa langsung pada sesi ini.

- Engineer melaporkan migration `0007_environment_context_api` dan `0008_environment_context_variable_fix` sudah diterapkan pada project Supabase `seagis-model-database`; Edge Function `temperature` version 6 menyediakan route temperature dan environment. Direct request temperature memakai reader development dilaporkan menghasilkan HTTP 200.
- Engineer melaporkan snapshot A3 Plot A dengan coverage 7 hari/168 hourly rows, window `2026-10-22T13:00:00Z`–`2026-10-29T13:00:00Z`, snapshot ID `7c346a90-394f-44f0-8502-ae9c5f862e1a`, mode `demo_review`, `training_authorized=false`, dan masing-masing 168 context untuk salinity, eastward/northward current, nitrate, dan phosphate.
- Engineer melaporkan PR [Seagis-Backend #9](https://github.com/De-Voeux/Seagis-Backend/pull/9) masih perlu di-merge ke `main`, sedangkan PR [Seagis #21](https://github.com/De-Voeux/Seagis/pull/21) telah di-merge ke `staging`. Status tersebut belum diverifikasi live di sini.
- Engineer melaporkan proxy TLS sudah memakai trusted CA bundle; Debug iPhone memperlihatkan history suhu berlabel “Backend development”, serta screenshot Plot Detail menunjukkan layar tidak crash setelah masalah URL environment diperbaiki. Re-verifikasi suhu dapat dianggap bukti dari laporan engineer; empat nilai regional setelah migration `0008` secara eksplisit masih menunggu satu run iPhone.
- Ada perbedaan source yang harus dibereskan: checkout lokal pada handover ini berada di `feat/integration` HEAD `ff5599b`, dan proxy `scripts/demo_plot_a_device_proxy.py` membangun environment response lewat `curate_environment.py --demo`. Follow-up menunjuk code path/PR `staging` yang meneruskan request environment. Jangan menganggap hasil screenshot atau endpoint route pada source staging otomatis berlaku pada worktree lokal ini.
- Lampiran menyarankan `git switch staging` dan `git pull --ff-only origin staging`. Perintah itu **belum dijalankan**. Worktree `feat/integration` yang diperiksa memiliki enam perubahan lokal; amankan/review perubahan dan periksa status branch sebelum berpindah atau menarik source.
- Catatan follow-up menyebut migration `0008` sudah diterapkan di “production”, sementara payload yang dijelaskan tetap `demo_review` dan Plot A sintetis. Environment/deployment target perlu dikonfirmasi sebelum endpoint ini disebut production-ready.

## Verifikasi yang tercatat

| Pemeriksaan | Hasil yang tercatat | Batas bukti |
| --- | --- | --- |
| Ingestion suhu simulator | 22 `201 stored`, satu `409 packet_conflict` skenario uji | Data sintetis development, bukan sensor lapangan. |
| History suhu API dan cache | 22 ID API cocok dengan 22 ID cache simulator pada sesi uji | Bukan pembuktian API produksi atau cakupan plot dinamis. |
| A3 database/API | Engineer melaporkan migration 0007/0008, Edge Function v6, endpoint environment, dan snapshot 7 hari/168 hourly rows | Belum diperiksa langsung di project atau dicocokkan dengan commit deploy; uji environment iPhone sesudah 0008 masih pending. |
| DTO/repository test | Catatan bertahap menyebut 3 uji DTO lulus dan 5 uji DTO+repository lulus pada checkout sementara | Bukan acceptance end-to-end; tidak dijalankan ulang pada perubahan UI terakhir. |
| UI dan build terakhir | Build Debug simulator dan signed iPhone berhasil; accessibility tree simulator memperlihatkan empat parameter pada widget lama. Build terbaru dipasang/diluncurkan di iPhone. Engineer juga melaporkan screenshot detail fisik memperlihatkan history suhu `Backend development`. | Screenshot engineer bukan verifikasi pada sesi ini; regional iPhone setelah 0008 masih pending. Automated tests tidak dijalankan pada perubahan UI terakhir. |
| Forecast/pairing/error matrix | Tidak ada forecast buatan; pairing ditunda sesuai arahan pengguna | Valid/invalid/reused pairing, akses silang, no-sensor, gap/null dan seluruh error-state belum menjadi acceptance suite. |

## Peta kode terkait

Repo app: `/Users/cindyram/Documents/Apple/Seagis`, branch `feat/integration`, HEAD `ff5599b` saat handover dibaca. Implementasi tersebar pada file berikut; daftar ini adalah peta source, bukan daftar perubahan yang semuanya belum di-commit:

- `Seagis/App/AppContainer.swift` — composition root memilih repository/cache demo; Debug membaca URL dan sesi sementara dari environment, Release tidak mengaktifkan endpoint demo.
- `Seagis/Repositories/Temperature/TemperatureHistoryRepository.swift` — request history suhu dan validasi respons; juga repository konteks regional A3.
- `Seagis/Repositories/Temperature/TemperatureRefreshCoordinator.swift` — state/cache/refresh suhu dan regional.
- `Seagis/Repositories/Temperature/TemperatureRefreshPolicy.swift` — batas refresh lokal Asia/Jakarta pukul 06.00.
- `Seagis/Repositories/Temperature/TemperatureCache.swift` — cache suhu dan identitas demo Plot A.
- `Seagis/DTOs/Temperature/TemperatureHistoryDTO.swift` dan DTO regional terkait — kontrak transport.
- `Seagis/Views/Components/PlotDetail/DevelopmentTemperatureView.swift` — pemetaan history suhu dan metrik regional.
- `Seagis/Views/PlotDetail/PlotDetailView.swift`, `Seagis/Views/FarmMap/FarmMapView.swift`, `Seagis/Views/PlotDetail/ParameterDetailView.swift`, `Seagis/Views/Components/PlotDetail/GaugeWidget.swift`, `Seagis/Models/PlotDetail/ParameterReading.swift` — injeksi state, pemakaian widget lama, detail dan provenance.

Worktree saat dicatat memiliki enam perubahan lokal yang belum di-commit: `Seagis/Models/PlotDetail/ParameterReading.swift`, `Seagis/Views/Components/PlotDetail/DevelopmentTemperatureView.swift`, `Seagis/Views/Components/PlotDetail/GaugeWidget.swift`, `Seagis/Views/FarmMap/FarmMapView.swift`, `Seagis/Views/PlotDetail/ParameterDetailView.swift`, dan `Seagis/Views/PlotDetail/PlotDetailView.swift`. Perubahan itu mengembalikan UI regional ke widget lama dan memetakan nilai A3. Selalu cek `git status` sebelum mengambil alih dan review perubahan ini sebelum commit.

## Cara menjalankan ulang demo

### Akses demo untuk penerima handover

- Akses hanya tersedia dari host development yang sudah memiliki checkout `/Users/cindyram/Documents/Apple/Seagis-Backend` dan konfigurasi lokal `.env.a1.devices` di root backend. Script membaca `SEAGIS_API_BASE_URL` dan `SEAGIS_READER_TOKEN` dari file itu. File tersebut adalah konfigurasi rahasia lokal; jangan salin ke repo Seagis, Second Brain, issue, chat, atau kirim sebagai lampiran. Kalau file atau reader tidak tersedia, minta pemilik backend menyediakan akses di host penerima melalui jalur internal yang disetujui; jangan mengganti dengan token app/operator lain.
- Jalankan demo dari `/Users/cindyram/Documents/Apple/Seagis`. Proxy membuat `SEAGIS_DEMO_SESSION` acak baru setiap kali dijalankan. App Debug mengirimnya sebagai Bearer ke proxy; proxy memeriksa token dan masa aktif, membatasi request ke GET Plot A sintetis, lalu mengambil suhu menggunakan reader lokal. **Tidak ada token statis yang bisa diambil dari handover ini.**
- Untuk suhu di simulator, `python3 scripts/demo_plot_a_simulator.py` membuat loopback proxy dan meluncurkan build simulator; helper ini mendukung endpoint suhu. Untuk A3 regional, gunakan `python3 scripts/demo_plot_a_device_proxy.py`, yang menyediakan route `/v1/plots/{uuid}/environment` melalui `curate_environment.py --demo` pada checkout backend lokal. Proxy A3 juga bisa dipakai dari simulator bila simulator diarahkan ke URL LAN yang dicetak helper.
- Untuk iPhone fisik, jalankan device proxy di Mac, set `SEAGIS_DEMO_API_BASE` dan `SEAGIS_DEMO_SESSION` yang dicetak helper pada **Edit Scheme → Run → Arguments → Environment Variables**, lalu jalankan build Debug. iPhone dan Mac harus tersambung ke Wi-Fi lokal yang sama; izinkan Local Network jika iOS meminta. Sesi berlaku maksimal 60 menit dan berhenti saat proxy dihentikan.
- Batas akses proxy: hanya GET, hanya Plot A sintetis tetap (`00000000-0000-4000-8000-000000000001`), tidak ada pairing atau akses plot lain. Route suhu meneruskan ke API development; route regional dibuat dari kurasi A3 lokal mode demo. Ini bukan login, API app umum, atau mekanisme untuk TestFlight/produksi.

### Alur menjalankan ulang

1. Buka repo app; cek branch/status dan generate project bila diperlukan dengan `xcodegen generate`.
2. Pilih helper sesuai kebutuhan di atas, pastikan reader/config backend sudah tersedia lokal, lalu biarkan proxy hidup selama uji.
3. Buka **Pak Madnung → Lahan 1** (fixture UI untuk `plot-madnung-1`). Catat fetch time vs observation/source time secara terpisah. Setelah 06.00 WIB, refresh terjadi saat app dibuka kembali, bukan saat app dibiarkan terbuka.
4. Jika helper atau sumber gagal, periksa state/cache sebelum menyimpulkan nilai di layar berasal dari fetch baru.

Perintah build yang terakhir dilaporkan: `xcodebuild -quiet -project Seagis.xcodeproj -scheme Seagis -configuration Debug -sdk iphonesimulator ... build` serta build `iphoneos` bertanda tangan dengan team development tersambung. Jalankan ulang sesuai device/toolchain sebelum menjadikan hasil tersebut baseline baru.

## Risiko dan batas yang perlu dijaga

- A1 memakai Plot A sintetis yang fixed dan proxy dengan kredensial operator di host Mac; ini demo terbatas. Belum ada session app scoped, expiry/revocation backend, policy akses objek untuk user app, atau uji cross-plot. Jangan gunakan jalur ini untuk TestFlight/produksi.
- Fetch regional yang belum menghasilkan snapshot masih memiliki fallback nilai fixture pada layout lama. Saat menguji error API, pastikan provenance/status cache dibaca; perlu state kegagalan yang jelas sebelum klaim “data live” untuk regional.
- Ada laporan deploy Edge Function/migration baru dan PR terkait, tetapi checkout `feat/integration` serta proxy lokal yang telah diperiksa belum tentu memuat jalur `staging` tersebut. Lakukan verifikasi endpoint dan iPhone pada commit yang sama; jangan mencampur bukti dari branch yang berbeda.
- Salinitas A3 dilaporkan dengan unit sumber `1e-3`, sedangkan UI menampilkan `ppt`. Kesesuaian konversi/display harus ditinjau pada kontrak bersama; label UI saja bukan bukti konversi provider.
- Koordinat/grid untuk plot contoh belum survei; nilai regional bukan pengukuran tambak dan tidak membuktikan representativitas lokasi.
- A3 snapshot review bukan hasil training. Suhu uji sintetis bukan pengukuran lapangan. Tidak ada model forecast Seagis atau bukti warning/diagnosis ice-ice.
- Catatan awal tentang “C1 acceptance” dan progres berikutnya berada di repo app `docs/progress/`; ringkasan Second Brain ini memperbarui status terpadu. Dokumen tersebut mencatat tahapan berbeda, jadi gunakan bukti terbaru di atas dan jangan menyamakan status lama sebelum proxy tersambung dengan hasil uji sesudahnya.

## Handoff kerja yang disarankan

1. Review enam perubahan lokal UI/state dan commit terpisah sesuai workflow repo. Pastikan nilai A3 tetap masuk komponen lama dan fixture tidak ditampilkan sebagai live tanpa provenance.
2. Perjelas state regional saat cache belum ada atau request gagal sambil mempertahankan layout; verifikasi empat widget dan nilai di layar detail iPhone fisik.
3. Tinjau mapping salinitas `1e-3` → `ppt`, time semantics, cadence native, nilai missing/zero, QC dan garis grafik bersama pemilik Track A.
4. Definisikan kontrak serta sesi demo yang didukung backend bila demo perlu dipakai lintas perangkat; jangan mengembangkan pairing kecuali scope dibuka lagi.
5. Untuk integrasi live multi-plot dan pengguna, tutup API auth/access Track A, plot/location mapping dan cache isolation sebelum memperluas UI.
6. Pertahankan forecast di Track A seperti arahan pengguna; Track C hanya mengonsumsi kontrak forecast yang sudah tersedia dan terverifikasi bila nanti diminta.
7. Setelah core/API/UI disepakati, susun acceptance matrix C10; baru tinjau privasi, operasi, TestFlight dan App Store sesuai fase serta arahan tersendiri.

## Catatan terkait

- [[Status Integrasi Seagis - 28 Oktober 2026]] — audit awal dan catatan progres C1.
- [[Handover A1 - Arsitektur Data dan Akses IoT]] · [[Operasi A1 - Simulator dan Credentials]] · [[Review A1 - Temperature Vertical Slice]]
- [[Handover A2 - Ingestion Lingkungan dan Grid]] · [[Review A2 - Hasil Ingestion Regional]]
- [[Handover A3 - Kualitas dan Alignment Data]] · [[Review A3 - Hasil dan Batas Validasi]]
- Sumber rencana Track C v0.1: `/Users/cindyram/Downloads/TRACK_C_INTEGRATION.md` (tetap file terpisah di Downloads).
