---
type: implementation-plan
project: "[[Challenge Final]]"
created: 2026-10-23
updated: 2026-10-23
status: draft-for-team-review
owner: iOS app team
source_commit: "d8eda62151d5eda6364ec48a571d369d5199ecfc"
tags: [challenge-final, seagis, engineering, ios, architecture, ios-foundation]
---

# SEAGIS — iOS APP FOUNDATION & REPOSITORY BOOTSTRAP SPECIFICATION

**Status:** Draft implementation instructions v0.2 — belum persetujuan tim atau bukti implementasi.  
**Audience:** Tim aplikasi, product, design, data/ML, scientific knowledge, IoT, dan coding agent.  
**Language:** Bahasa Indonesia untuk dokumentasi; bahasa Inggris untuk identifiers dan kode.  
**Goal:** Menyiapkan repository aplikasi nyata `De-Voeux/Seagis` dan fondasi arsitektur iOS yang mengikuti spec bersama, menggunakan **opsi B sebagai baseline awal** dengan batas integrasi yang memungkinkan evaluasi opsi lain.

Dokumen ini merupakan spesifikasi mandiri untuk fondasi aplikasi iOS dan persiapan repository. Dokumen pipeline data/ML dan scientific knowledge menjadi referensi integrasi, bukan urutan fase yang harus dilanjutkan oleh aplikasi.

**Batas pekerjaan saat dokumen ini dibuat:** hanya menyusun spec. Pengguna akan meninjau dan push spec ke `c67-vault`; pembuatan repository dan scaffold menunggu instruksi berikutnya. Belum ada repository, kode Swift, API, atau deployment baru yang dibuat melalui dokumen ini.

## 0. Scope dan asumsi yang harus dipertahankan

1. `c67-vault` tetap menjadi acuan spec bersama. `Seagis` menjadi repository implementasi aplikasi iOS; bukan pengganti repository pipeline/model atau scientific knowledge vault.
2. Baseline rancangan pada 23 Oktober 2026: **opsi B, assessment/forecast engine berada di backend; iOS mengambil hasil terstruktur dan menampilkannya**. Ini baseline untuk draft bootstrap, masih memerlukan penyelarasan dengan pemilik engine.
3. Arsitektur aplikasi yang diusulkan: **MVVM + use cases + repository interfaces + infrastructure services**, dengan dependency injection pada composition root. Service menangani API/framework; repository menentukan akses dan pemetaan data; use case mengatur proses kebutuhan pengguna.
4. Pemisahan interface mengurangi perubahan UI ketika lokasi engine berubah. **Perubahan backend ↔ on-device tetap memerlukan perubahan implementasi, kontrak input, data availability, distribusi model, pengujian, dan kebijakan offline.** Tidak dijanjikan cukup memindahkan file.
5. Sasaran produk adalah assessment lingkungan bagi community advocates. Tidak menghasilkan diagnosis, probabilitas ice-ice, ambang biologis universal, atau peta penyebaran penyakit yang belum tervalidasi.
6. Alur inti tidak mewajibkan pencatatan kunjungan, foto, checklist gejala, atau observasi lapangan di aplikasi. Keterbatasan validasi ilmiah tetap harus dinyatakan; tidak otomatis menjadi fitur input baru.
7. SwiftUI dan MapKit menjadi fondasi UI/peta. Foundation Models adalah lapisan interpretasi opsional dengan fallback deterministik. Core ML menjadi kandidat adapter inferensi lokal, bukan dependency wajib baseline B. WeatherKit masih dipertimbangkan, tidak menggantikan Open-Meteo pada pipeline Track A.
8. SwiftData **tidak ditetapkan** oleh spec ini. Kebutuhan penyimpanan lokal tetap ada untuk cache yang dapat bertahan setelah aplikasi ditutup; mekanismenya diputuskan terpisah di balik interface penyimpanan.
9. Prototype `AppPOC` bukan otomatis basis produksi. Inventarisasi dan review dilakukan sebelum memilih kode yang layak diadopsi; jangan menyalin seluruh PoC tanpa pemeriksaan.

## 1. Status sumber dan konflik keputusan

Snapshot acuan vault yang dicatat pada draft sebelumnya (belum diaudit ulang dalam revisi ini): `De-Voeux/c67-vault@d8eda62151d5eda6364ec48a571d369d5199ecfc`, tanggal pembacaan yang dicatat: 23 Oktober 2026. Angka status implementasi di bawah adalah laporan dokumen, bukan audit live backend baru.

| Sumber | Temuan yang dipakai | Batas penggunaan |
| --- | --- | --- |
| [[TRACK_A_DATA_ML_ENGINEERING]] | Fase A0–A6; kontrak/provenance; target forecasting suhu; handoff assessment | Roadmap tidak membuktikan endpoint assessment final sudah tersedia |
| [[TRACK_B_SCIENTIFIC_KNOWLEDGE_VAULT]] | Evidence terverifikasi, retrieval, interpretasi Foundation Models, fallback | Output model bahasa bukan sumber angka atau severity otoritatif |
| [[Handover A1 - Arsitektur Data dan Akses IoT]] | History/status suhu dan ingestion development; sensor masih sintetis | Reader token development untuk backend/operator, bukan token bersama yang ditanam di aplikasi |
| [[Review A3 - Hasil dan Batas Validasi]] | QC/alignment telah dilaporkan; snapshot `training_authorized=false`; plot dummy | Belum bukti model terlatih, inferensi iOS, atau validasi penyakit |
| [[Pembaruan Desain - Sensor Suhu Hourly dan Inferensi On-Device]] | Arah 21 Oktober: suhu hourly, receiver/internet/backend, inferensi lokal | Berbeda dengan baseline B rancangan aplikasi tanggal 23 Oktober 2026; perlu keputusan bersama sebelum live integration |
| [[Transfer Knowledge - IoT Rumput Laut - 15 Oktober 2026]] | Handoff Radit dengan pembaruan 20 Oktober: suhu/salinitas, sesi 5 jam, BLE | Konteks historis; jangan otomatis menghidupkan BLE/salinitas dalam scaffold baru |

**Dasar acuan spec aplikasi:** kebutuhan produk dan user flow menentukan perilaku; keputusan arsitektur menentukan batas tanggung jawab; kontrak bersama menentukan integrasi; hi-fi menentukan detail tampilan; bukti implementasi menentukan kemampuan yang benar-benar tersedia. Roadmap data/ML dan scientific knowledge hanya mencakup sebagian dari acuan tersebut.

| Acuan tambahan | Peran dalam spec aplikasi | Status penggunaan pada revisi ini |
| --- | --- | --- |
| Kebutuhan produk, challenge response, dan flow observasi lingkungan | Tujuan pengguna, scope, dan batas klaim | Menggunakan konteks yang telah diberikan; versi resmi perlu dipin sebelum implementasi |
| AppPOC issue #2 — Architecture and Integration Setup | MVVM, integrasi, states, ownership, dan release | Isi tiket pernah diberikan dalam percakapan; status terkini belum diperiksa ulang |
| Hi-Fi Design for MVP, c67-design issue #16 | Screen, komponen, navigasi, dan interaksi | Dependensi review; hi-fi final belum diperiksa untuk menetapkan daftar screen |
| Kontrak API/schema dan fixture yang disepakati | Field, units, waktu, auth, error, dan kompatibilitas | Kontrak assessment final masih perlu disepakati; schema executable menjadi acuan implementasi |
| Seagis - Pipeline A0-A3, poin 1–10 saja | Status implementasi, runtime, cadence, QC, lineage, dan batas data | Dibaca dari PDF; snapshot 22 Oktober 2026, commit e93a005; bukan audit live |
| Implementasi AppPOC serta kebutuhan perangkat IoT | Reuse yang layak dan batas integrasi perangkat | Audit kode dan handoff operasional masih diperlukan; keberadaan repository bukan bukti kesiapan |
| Keputusan rancangan aplikasi tanggal 23 Oktober 2026 | Baseline B dan struktur type-first, feature-second | Dicatat pada draft ini; review lintas pemilik tetap terbuka |

**Batas implementasi berdasarkan PDF poin 1–10:** A1 menerima suhu melalui HTTPS di Supabase; sensor/plot masih sintetis. A2 berjalan dengan Python di Mac, dispatcher 15 menit hanya melakukan fetch ketika due. A3 berjalan on demand di Mac dan menghasilkan snapshot review, bukan endpoint assessment iOS. Salinitas/arus memiliki cadence native 6 jam, nutrien harian, dan Open-Meteo menggunakan GFS hourly. Semua hasil A3 membawa `training_authorized=false`; training, prakiraan suhu Seagis, dan integrasi inferensi iOS belum dilaksanakan sampai A3. Satuan salinitas tetap `1e-3`, tidak otomatis diubah menjadi PSU/ppt.

**Penanganan konflik:** keputusan yang telah disetujui dan kontrak versi terpin menjadi acuan implementasi. Draft ini mencatat usulan dan keputusan rancangan, bukan mengklaim persetujuan seluruh tim. Jika sumber bertentangan, catat konflik dan minta pemilik terkait menyelesaikannya sebelum pekerjaan yang bergantung padanya; jangan memilih berdasarkan nama track atau mengubah dokumen pemilik lain diam-diam.

Definisi opsi A/C belum dipastikan lengkap dari sumber yang dibaca. Jangan menebak bahwa huruf tertentu berarti hybrid atau BLE. Catat alternatif dengan nama eksplisit **remote inference**, **on-device inference**, atau **hybrid**, kemudian cocokkan penamaan A/C dalam keputusan tim.

## 2. Execution order / milestones

### Phase IOS-0 — Spec review dan publication ke vault (SEKARANG)

**Tasks**
- Review draft ini terhadap kebutuhan produk, user flow, desain, arsitektur, kontrak, IoT, status implementasi, serta dependensi data/ML dan scientific knowledge.
- Simpan `SEAGIS_IOS_APP_FOUNDATION_SPEC.md` dalam folder kontribusi baru milik penyusun di root `c67-vault`. Path final dicatat pada PR dan referensi spec setelah merge. Tidak ditempatkan dalam folder kontributor lain.
- Buat branch perubahan spec; stage hanya file spec, bukan seluruh perubahan Obsidian.
- Push dan buat PR oleh pengguna. Jika diperlukan, penambahan link pada indeks Engineering dilakukan sebagai perubahan terpisah yang diperiksa bersama.

**Required deliverables**
- Dokumen draft ini, daftar keputusan terbuka, dan PR spec di vault.

**Acceptance criteria**
- Reviewer bisa membedakan keputusan rancangan, usulan engineering, status historis, dan implementasi yang belum tersedia.
- Tidak ada kode aplikasi, repository baru, perubahan backend, atau push otomatis pada tahap penulisan draft.
- Setelah merge, catat commit vault hasil merge sebagai acuan bootstrap; `source_commit` di frontmatter hanya snapshot bahan bacaan, bukan commit yang sudah memuat draft ini.

### Phase IOS-1 — Repository dan dokumentasi fondasi (SETELAH INSTRUKSI BERIKUTNYA)

**Tasks**
- Periksa apakah `De-Voeux/Seagis` sudah ada. Jika ada, inventarisasi dan gunakan tanpa menimpa isi; jangan membuat duplikat.
- Bila belum ada dan pembuatan diizinkan, buat dengan nama persis `Seagis`. Visibility harus dikonfirmasi sebelum penciptaan; usulan awal private, bukan keputusan final.
- Buat dokumentasi arsitektur, keputusan lokasi engine, batas integrasi, workflow Git, serta referensi spec.
- Jangan memindahkan pipeline, database migrations, atau corpus riset ke repository iOS sebagai duplikat sumber kebenaran.

**Required deliverables**

| File target di `Seagis` | Isi wajib |
| --- | --- |
| `README.md` | Tujuan, status bootstrap, sumber spec, setup dan batas komponen yang tersedia |
| `AGENTS.md` | Cara membaca spec terpin, scope perubahan, review, validasi, dan larangan mengarang kontrak |
| `SPEC_REFERENCE.md` | Repo vault, commit penuh hasil merge, path spec ini serta seluruh kontrak dan dependensi relevan yang telah disetujui, status yang disetujui |
| `docs/architecture.md` | Lapisan, arah dependency, composition root, alur opsi B, fallback dan alternatif |
| `docs/integration-boundaries.md` | Kepemilikan engine, transport, DTO, cache, knowledge dan auth |
| `docs/decisions/ADR-001-engine-placement.md` | Baseline B, konflik catatan on-device, alternatif, konsekuensi, status review |
| `docs/open-decisions.md` | Pertanyaan, pemilik keputusan, tahap yang diblokir |
| `docs/development-workflow.md` | Update spec, implementasi, validasi, commit/PR pada repo yang sesuai |
| `.gitignore` | Build output, pengaturan lokal Xcode, secrets, koordinasi lokal dan file sistem |

**Acceptance criteria**
- Link spec menggunakan commit immutable yang benar-benar tersedia, bukan placeholder atau hanya `main`.
- Seluruh dokumentasi menyatakan scaffold/fitur yang belum dibuat secara jujur.
- Tidak ada production credentials atau shared development reader token di repository.
- Tidak ada klaim build lulus bila belum ada proyek atau toolchain yang menjalankan build.

### Phase IOS-2 — Scaffold Xcode dan batas modul (OTORISASI TERPISAH)

**Tasks**
- Konfirmasi minimum iOS, Xcode/Swift, bundle ID, signing team, dan perangkat target sebelum membuat project settings.
- Buat satu target aplikasi SwiftUI dan target test yang sesuai. Tetapkan nama fitur dari spec yang disepakati; jangan menganggap contoh `PlotDetail` sebagai nama wajib. Gunakan folder/modul sederhana; belum perlu banyak package/microservices.
- Buat composition root dan protocol untuk akses assessment, cache, knowledge dan explanation.
- Mulai dengan fixture sintetis serta fallback teks. Adapter live dan model tidak diaktifkan otomatis.

**Required deliverables**
- `Seagis.xcodeproj`, folder kode sesuai bagian 4, asset dasar, fixture dan test awal yang relevan.
- Konfigurasi sample tanpa secrets; petunjuk menjalankan build dan test.

**Acceptance criteria**
- Proyek dapat dibuka dan dibangun pada toolchain yang disepakati; hasil yang belum dijalankan harus ditandai belum diverifikasi.
- View/ViewModel tidak mengimpor Supabase SDK, Core ML, atau mengakses endpoint langsung.
- Repository mock dapat diganti melalui composition root tanpa mengubah View.

### Phase IOS-3 — Kandidat vertical slice pertama (BUKAN SCOPE BOOTSTRAP)

Peta dan detail plot di bawah merupakan usulan slice untuk review, bukan penguncian nama fitur/folder dari contoh pengguna.

**Tasks**
- Tampilkan plot demo pada MapKit dan detail assessment sintetis dengan identitas plot yang konsisten.
- Implementasikan loading, empty, error, data parsial, cached/offline dan schema tidak didukung.
- Simpan hasil terakhir yang valid untuk plot terkait, beserta asal/waktu dan statusnya.
- Gunakan fallback deterministik sebelum penjelasan Foundation Models.

**Acceptance criteria**
- Plot A tidak pernah menampilkan data cache Plot B; respons terlambat tidak menimpa pilihan pengguna terbaru.
- Setelah aplikasi ditutup dan dibuka offline, cache valid dapat dibaca dengan label hasil tersimpan dan waktu pembaruan.
- Jika tidak ada cache, tampilkan assessment belum tersedia; jangan membuat assessment baru seolah berasal dari engine.
- Fixture, angka model regional, pengukuran lokal, serta prakiraan tetap dapat dibedakan.
- Model bahasa yang tidak tersedia/gagal tidak menghalangi pembacaan nilai terstruktur.

### Phase IOS-4 — Live integration dan interpretasi (SETELAH KONTRAK SIAP)

**Tasks**
- Review schema assessment executable, contoh respons, versi, error, auth dan akses plot bersama Track A.
- Integrasikan repository remote menggunakan DTO mapper; endpoint A1 history/status tidak dianggap endpoint assessment.
- Integrasikan knowledge retrieval terverifikasi dari Track B dan Foundation Models hanya setelah pemeriksaan runtime availability serta validasi output.
- Evaluasi WeatherKit/Core ML sebagai pekerjaan terpisah sesuai keputusan tim.

**Acceptance criteria**
- Pengujian kontrak memvalidasi schema, units, IDs, timestamps, data hilang dan schema unsupported.
- Penjelasan tidak mengubah nilai engine, mengarang evidence ID, menentukan severity sendiri, atau membuat diagnosis.
- Autentikasi aplikasi dan otorisasi plot teruji tanpa memakai token bersama development di binary.

## 3. Baseline arsitektur: opsi B

| Lapisan | Tanggung jawab | Batas |
| --- | --- | --- |
| Presentation | SwiftUI Views, ViewModels, navigation dan state | Tidak menghitung risiko/forecast, tidak memanggil provider langsung |
| Application | Use cases seperti `LoadPlotAssessment` | Mengatur proses, bukan detail HTTP atau model |
| Domain | Model internal dan protocol repository | Tidak bergantung pada SwiftUI, URLSession atau ML framework |
| Data | Repository implementation, DTO mapping, cache policy | Mempertahankan semantik dan versi data |
| Infrastructure | API client, penyimpanan lokal, knowledge adapter, explanation service | Implementasi detail yang dapat diganti |
| App | Composition root | Memilih live/mock/fallback secara eksplisit |

Alur target: UI meminta use case → repository mengambil hasil backend atau cache → mapper memvalidasi → hasil terstruktur ditampilkan → explanation service dapat menambahkan teks berbasis evidence. Penjelasan tidak mengganti data sumber.

Backend menyediakan ingestion, QC/alignment, dan kelak engine/assessment. UI mengambil assessment; app tidak melakukan ingestion Copernicus/Open-Meteo atau training. Knowledge vault tetap dikelola Track B; cara distribusi subset terverifikasi ke iOS harus disepakati.

**Offline baseline B:** dapat membaca hasil yang sudah tersimpan, tidak menjamin assessment baru tanpa backend. Core ML untuk opsi lokal hanya dapat menghasilkan hasil baru jika model kompatibel dan semua input yang disyaratkan tersedia serta lolos pemeriksaan kualitas.

**Interface kandidat — usulan, bukan API final:** `AssessmentRepository`, `AssessmentCache`, `KnowledgeRepository`, `InsightGenerator`. Adapter Core ML hanya ditambahkan jika diperlukan. Nama/method final mengikuti kontrak dan kebutuhan nyata; jangan membuat implementasi kosong yang mengaku siap inferensi.

### Dampak perubahan lokasi engine

| Hal | Baseline remote | Jika on-device / hybrid diadopsi |
| --- | --- | --- |
| Sumber hasil | Assessment dari backend | Adapter lokal atau aturan routing yang eksplisit |
| Input | Respons assessment | Feature bundle, schema, cutoff, units, QC dan provenance yang cocok dengan training |
| Model | Dikelola backend | Konversi/kompatibilitas, distribusi, versi, rollback dan penggunaan resource perangkat |
| Offline | Cache hasil | Inferensi baru hanya jika input/model memenuhi syarat |
| Konsistensi | Versi backend dilacak | Perlu parity test, toleransi numerik, asal hasil dan versi kedua jalur |
| UI | Model domain/state | Dapat dipertahankan sejauh semantik output kompatibel; status baru mungkin diperlukan |

## 4. Struktur target repository — type-first, feature-second

**Keputusan struktur pada 23 Oktober 2026:** kelompokkan file berdasarkan jenis/tanggung jawab terlebih dahulu; di dalam setiap jenis, kelompokkan lagi berdasarkan fitur. Contoh: `Views/PlotDetail/`, `ViewModels/PlotDetail/`, `Models/PlotDetail/`. Struktur ini menggantikan usulan folder Presentation per fitur pada draft awal.

**Batas contoh:** `PlotDetail` hanya contoh penamaan. `Map` dan `PlotDetail` di tabel/daftar berikut adalah ilustrasi penerapan pola, bukan daftar fitur atau folder yang wajib dibuat pada bootstrap. Nama fitur aktual mengikuti spec fitur yang disepakati; scaffold IOS-2 tidak perlu membuat fitur contoh tersebut.

Struktur folder adalah cara organisasi file; aturan dependency MVVM, use case, repository dan service pada bagian 3 tetap berlaku. Tidak ada folder `PlotDetail` yang mengumpulkan semua jenis file sekaligus di root aplikasi.

| Path di dalam `Seagis/` | Isi |
| --- | --- |
| `App/` | App entry point, configuration dan composition root |
| `Views/Map/` | View peta dan komponen khusus fitur Map |
| `Views/PlotDetail/` | View detail plot dan komponen khusus PlotDetail |
| `Views/Shared/` | Komponen UI yang benar-benar dipakai beberapa fitur |
| `ViewModels/Map/` | State dan orchestration tampilan Map |
| `ViewModels/PlotDetail/` | State dan orchestration tampilan PlotDetail |
| `Models/Map/` | Model yang hanya dibutuhkan fitur Map |
| `Models/PlotDetail/` | Model yang hanya dibutuhkan fitur PlotDetail |
| `Models/Shared/` | Model domain bersama, misalnya identitas plot dan assessment lintas fitur |
| `UseCases/Map/` | Proses kebutuhan fitur Map |
| `UseCases/PlotDetail/` | Proses kebutuhan fitur PlotDetail |
| `UseCases/Shared/` | Proses yang benar-benar dipakai lintas fitur |
| `Repositories/PlotDetail/` | Protocol dan implementation akses data khusus PlotDetail |
| `Repositories/Shared/` | Protocol dan implementation repository lintas fitur |
| `Services/Networking/` | HTTP client bersama dan transport error handling |
| `Services/Persistence/` | Adapter penyimpanan lokal bersama |
| `Services/Intelligence/` | Fallback dan kelak adapter Foundation Models |
| `DTOs/PlotDetail/` | Payload transport khusus PlotDetail |
| `DTOs/Shared/` | Payload transport yang dipakai beberapa fitur |
| `Mappers/PlotDetail/` | Pemetaan DTO ke model internal fitur |
| `Mappers/Shared/` | Pemetaan lintas fitur |
| `Resources/` | Assets dan fixture demo berlabel sintetis |

Untuk jenis lain yang memiliki perilaku khusus fitur, gunakan pola yang sama: misalnya `Services/PlotDetail/`. Networking, Persistence dan Intelligence merupakan layanan lintas fitur, sehingga dikelompokkan menurut tanggung jawab teknisnya; jangan membuat salinan HTTP client untuk tiap fitur.

**Contoh penempatan file — nama usulan, bukan file yang sudah dibuat:**

- `Views/PlotDetail/PlotDetailView.swift`
- `Views/PlotDetail/AssessmentCardView.swift`
- `ViewModels/PlotDetail/PlotDetailViewModel.swift`
- `Models/PlotDetail/PlotDetailContent.swift`
- `Models/Shared/Plot.swift`
- `Models/Shared/Assessment.swift`
- `UseCases/PlotDetail/LoadPlotAssessment.swift`
- `Repositories/Shared/AssessmentRepository.swift`
- `Repositories/Shared/RemoteAssessmentRepository.swift`
- `DTOs/Shared/AssessmentPacketDTO.swift`
- `Mappers/Shared/AssessmentMapper.swift`

Protocol repository harus bebas dependency transport/framework meskipun diletakkan dekat implementation-nya. Model domain tetap dipisahkan dari DTO, dan tidak mengimpor SwiftUI. Jika diperlukan model presentasi, namai dan tandai perannya; jangan menjadikannya kontrak data backend.

`SeagisTests/` mengikuti jenis yang diuji kemudian fitur, misalnya `ViewModels/PlotDetail/`, `UseCases/PlotDetail/`, `Repositories/Shared/` dan `Mappers/Shared/`. Dokumen berada di `docs/`; referensi kontrak berversi berada di `contracts/`.

**Aturan penambahan fitur**

1. Gunakan nama fitur yang konsisten pada semua jenis folder, misalnya selalu `PlotDetail`.
2. Buat hanya folder/file yang dibutuhkan fase berjalan; tidak perlu folder kosong untuk setiap kombinasi jenis dan fitur.
3. Jangan menduplikasi `Plot`, `Assessment`, networking atau cache hanya supaya setiap fitur punya model/service sendiri.
4. View berkomunikasi melalui ViewModel; ViewModel memakai use case atau abstraction yang sesuai; repository mengatur akses data dan memanggil service. View tidak langsung memanggil HTTP atau engine.
5. Composition root memilih implementation live/mock/fallback. Pemindahan lokasi engine tidak mengubah aturan organisasi type-first ini.
6. Verifikasi keanggotaan target Xcode: folder di disk saja belum membuktikan file ikut dibangun.

**Acceptance criteria struktur:** reviewer dapat menemukan setiap file berdasarkan jenisnya kemudian fiturnya; komponen bersama mempunyai satu definisi; tidak ada akses transport langsung dari View/ViewModel; test mengikuti komponen yang diuji.

Core ML, WeatherKit, BLE, login UI, notifikasi, dan background refresh tidak otomatis masuk bootstrap. Tambahkan hanya pada fase dan kebutuhan yang disepakati.

## 5. Kontrak dan data yang harus disepakati

Contoh `assessment_packet` Track A masih ilustratif. Jangan mengubahnya menjadi kontrak produksi hanya karena contoh JSON dapat didekode.

- Pertahankan `schema_version`, `assessment_id`, `plot_id`, `generated_at`, measurements/findings, evidence IDs, quality dan missing context sesuai kontrak final.
- Pertahankan unit, scope local/regional, source/dataset/run/grid, cadence dan waktu pengukuran/valid/issue yang tersedia. Null bukan nol, waktu fetch bukan waktu pengukuran.
- Cache dipisahkan per plot dan versi schema; simpan timestamp pengambilan tanpa mengganti waktu asal. Aturan expiry/retention/stale belum boleh diisi dengan angka arbitrer.
- Request gagal atau respons invalid tidak boleh menimpa cache valid. Retry dibatasi; unauthorized, unsupported schema, dan network error dibedakan.
- Penjelasan harus terikat pada assessment ID dan knowledge version yang dipakai. Ganti assessment berarti invalidasi penjelasan lama yang tidak cocok.
- Peta menunjukkan lokasi/plot dan kondisi data; radius sensor atau warna risiko tidak boleh menyiratkan cakupan biologis tanpa dasar.

## 6. Keputusan terbuka dan pemilik review

| Keputusan | Reviewer yang diusulkan | Memblokir |
| --- | --- | --- |
| Baseline B vs catatan inferensi lokal; arti tepat opsi A/C | Tim aplikasi + pemilik data/ML dan scientific knowledge | Integrasi engine live; bukan penulisan draft |
| Visibility repository, bundle ID, target iOS/Xcode dan signing | Tim aplikasi | Penciptaan repo/settings sesuai item |
| Schema assessment, endpoint, auth dan akses plot | Track A + aplikasi | Live integration |
| Format/distribusi knowledge, availability dan bahasa model | Track B + aplikasi | Interpretasi AI produksi |
| Caching, retention, invalidasi, stale policy | Aplikasi + pemilik data | Acceptance offline penuh |
| Backend deployment/operator/API integrasi siapa pemiliknya | Tim | Operasi produksi; role iOS tidak otomatis memiliki semua backend |
| Adopsi kode AppPOC | Aplikasi | Reuse kode, bukan dokumentasi bootstrap |

## 7. Agent execution protocol

1. Baca `AGENTS.md` yang berlaku, spec ini, kebutuhan produk/user flow, kontrak, keputusan arsitektur, desain terkait dan dependensi data/ML, scientific knowledge serta IoT yang terpin. Periksa repository/branch/status/diff sebelum menulis. Hormati pekerjaan yang sudah ada.
2. Kerjakan fase yang diminta saja. Pada permintaan sekarang hasilnya IOS-0; jangan membuat `Seagis`, mengimplementasikan IOS-2–IOS-4 atau push atas nama pengguna.
3. Pada instruksi pembuatan repo berikutnya, mulai IOS-1 dan laporkan keputusan yang masih memblokir. Jangan otomatis memperluasnya menjadi aplikasi lengkap.
4. Tulis `SPEC_REFERENCE.md` dengan commit hasil merge spec yang benar. Link GitHub atau path lokal saja tidak membuktikan agent telah membaca sumber; laporkan dokumen yang benar-benar terbaca.
5. Jika API, model atau kontrak belum tersedia, gunakan fixture dengan label sintetis dan laporkan gap. Jangan mengarang endpoint, kredensial, clinical labels atau hasil test.
6. Bedakan status implemented, tested, mocked, proposed dan blocked. Setiap fase melaporkan file, pemeriksaan, batas hasil dan acceptance criteria.
7. Perubahan kontrak bersama diajukan di vault terlebih dahulu; implementasi menunjuk revisinya. Perubahan spec tidak otomatis memperbarui kode.

## 8. Provenance dan navigasi

Gaya penulisan mengikuti roadmap Track A/B (status, audience, goal, fase, tasks, deliverables, acceptance criteria, execution protocol), serta catatan Calzy/Radit (frontmatter, status keputusan, sumber dan wikilink). Spec ini bukan salinan keputusan seluruh tim; bagian usulan tetap memerlukan review.

Dasar revisi: keputusan dan koreksi rancangan tanggal 23 Oktober 2026, isi draft sebelumnya, serta PDF Pipeline A0–A3 poin 1–10 yang telah dibaca. `source_commit` mempertahankan provenance pembacaan repository yang dicatat pada draft sebelumnya; revisi ini tidak memverifikasi ulang kesamaan lampiran dengan repository. Referensi yang belum ditinjau langsung ditandai pada bagian 1. Tidak ada klaim audit live backend, pembacaan hi-fi final, atau pengujian ulang pipeline.

Navigasi: [[Indeks - Engineering]] · [[TRACK_A_DATA_ML_ENGINEERING]] · [[TRACK_B_SCIENTIFIC_KNOWLEDGE_VAULT]] · [[Challenge Final]].
