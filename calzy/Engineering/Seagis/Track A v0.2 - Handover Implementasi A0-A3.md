---
type: engineering-handover
project: "[[Challenge Final]]"
created: 2026-11-03
updated: 2026-11-04
status: singapore-live-seoul-retired
scope: A0-A3
repo: /Users/cindyram/Documents/Apple/Seagis-Backend
branch: codex/sg-finalize-project-retirement
base_commit: f155184
latest_commit: 1bf186e
tags: [challenge-final, seagis, engineering, track-a, handover]
---

# Track A v0.2 — Handover implementasi A0–A3

## Cutover Singapore selesai; project Seoul dihapus — 4 November 2026

Project aktif adalah **seagis-model-database** di organisasi Seagis Free Plan, region Singapore (`ap-southeast-1`), status `ACTIVE_HEALTHY`. Project ref API immutable tetap `mdtmupiftllpglkfoaqy`; rename dari `seagis-model-database-sg` hanya mengganti nama tampilan. Endpoint aktif: `https://mdtmupiftllpglkfoaqy.supabase.co/functions/v1/temperature` ([dashboard](https://supabase.com/dashboard/project/mdtmupiftllpglkfoaqy)). Project Seoul (`kibztbeviortyvbedogg`, `ap-northeast-2`) sudah dihapus dan tidak lagi melayani URL lama. Tidak ada upgrade billing.

### Database, SQL routines, dan data

- Sebelum penghapusan sumber, 97 relation dan 836 kolom memiliki signature yang sama; 161 routine PostgreSQL, 50 trigger, dan 16 policy cocok. Ada 54 routine di schema `seagis*`; tidak ada object PostgreSQL `PROCEDURE` tersendiri karena operasi database diekspos sebagai SQL functions.
- Sebelas migration SQL tercatat di tujuan, termasuk `20261104141620_singapore_monitoring_indexes`. Lima index monitoring dan unique constraint migration ledger yang sebelumnya tertinggal sudah diterapkan. Target memiliki 59 index pada schema `seagis`.
- Isi tabel aplikasi, Auth, IoT, environment, quality, feature, dan monitoring disalin dan dicocokkan dengan jumlah serta hash. Sampel pemeriksaan akhir: 188 observation, 6 quality snapshot, dan 106 environment attempt. Dua ledger platform-managed, `realtime.schema_migrations` dan `storage.migrations`, mempertahankan riwayat native project Singapore dan tidak ditimpa dengan migration history Seoul. Tidak ada Storage object yang perlu dipindahkan.
- Core Auth settings, worker roles, secret Edge, pooler, TLS dan custom token IoT/reader telah dikonfigurasi untuk project tujuan. API key Supabase berbeda antarproject; pengguna Auth mungkin perlu refresh/sign-in ulang. Login TLS gateway/A2/A3 lulus verifikasi tanpa direct table grants.

### Edge Function dan endpoint

Edge Function aktif `temperature` versi 2 di Singapore; bundle memuat telemetry dan route kompatibilitas `/v1/plots/{plot_id}/environment`. `/health` dan `/v1/status` dengan reader token sama-sama HTTP 200; status memuat dua plot uji. URL lama Seoul tidak lagi menjadi alias.

Route `/environment` sudah terpasang dan memanggil routine SQL yang sama di tujuan. Reader token uji tidak punya akses ke plot A3 sehingga pemeriksaan plot itu mendapat `403 plot_forbidden`; plot uji lain tanpa snapshot mendapat `503 environment_context_unavailable`. Smoke test dengan reader yang berwenang atas plot A3 belum dilakukan; tidak ada izin yang diperluas untuk mengakalinya.

### Aplikasi, monitoring, dan operasi

- Monitoring production Vercel telah diarahkan ke Singapore dan redeploy artifact yang disetujui sebelumnya berhasil. Homepage `200`, anonymous monitor/collector `401`, authenticated collector `200`, serta query dashboard restricted berhasil.
- Backend runtime, pooler dan cache Supabase CLI lokal mengarah ke ref `mdtmupiftllpglkfoaqy`. Scheduler A2 tetap LaunchAgent di Mac saat Mac aktif dan user login; A3 tetap on-demand.
- Backup dump/restore dan konfigurasi privat tersimpan owner-only di `data/migration-singapore/` repo backend dan diabaikan Git. Karena Seoul dihapus, rollback perlu membuat project baru dan restore backup; backup bukan replika aktif.
- Backend commit `22797ac` (parity Edge/migration) dan `1bf186e` (handover) ada pada branch lokal `codex/sg-finalize-project-retirement`; keduanya belum dipush dan belum mempunyai CI run baru. Tes 106, integrasi HTTP, Ruff, dan CI yang disebut di bawah berasal dari commit sebelumnya. App commit `7736634` mengarah ke endpoint baru pada branch lokal `codex/singapore-api-endpoint`, tetapi belum dipush atau dibuild. Pengujian perangkat iOS, sign-in Auth pengguna, dan satu siklus cron monitoring berikut belum terverifikasi.

Runbook migrasi lengkap: `/Users/cindyram/Documents/Apple/Seagis-Backend/docs/operations/singapore_migration.md`.

## Percobaan awal batas kuota free tier — 4 November 2026 (historis, sudah terselesaikan)

Bagian ini merekam keadaan sebelum pengguna meninggalkan Capital SEO. Setelah slot gratis dibebaskan, project Singapore dibuat dan cutover diselesaikan seperti dicatat di bagian status akhir di atas.

Pengguna menyetujui deployment secara eksplisit. Migration 0008 dan 0009 telah diterapkan ke project development Seagis `kibztbeviortyvbedogg`; seluruh 10 migration ledger cocok persis dengan source, tanpa pending migration. Policy `pilot-quality-spatial-1` terdaftar. Restricted worker TLS berhasil diverifikasi dengan nol table grants; smoke check cloud menghasilkan `a3-source-2` dan `a3-alignment-2` untuk satu jam, `training_authorized=false`, tanpa persist snapshot baru.

Pengguna juga meminta pindah ke Singapore/Jakarta dan membatasi biaya ke gratis. Region sumber saat ini Seoul (`ap-northeast-2`); organisasi Seagis terkonfirmasi Free Plan. Tujuan yang tersedia adalah Singapore (`ap-southeast-1`); Jakarta tidak ada pada [daftar region resmi](https://supabase.com/docs/guides/platform/regions). [Pindah region memerlukan project baru](https://supabase.com/kb/troubleshooting/change-project-region-eWJo5Z), migrasi database, serta pembaruan endpoint/configuration.

Percobaan pembuatan project Singapore pertama ditolak Supabase HTTP 400 karena dua owner/admin organisasi saat itu telah mencapai batas dua project gratis aktif. Pada checkpoint tersebut belum ada project tujuan atau data yang dipindahkan; tidak ada upgrade berbayar. Hambatan kuota kemudian diselesaikan setelah pengguna meninggalkan Capital SEO. Database sumber sekitar 26 MB; 1 Auth user dan 0 Storage objects terdeteksi saat inventaris. Clone dashboard tidak dipilih karena berbayar dan dokumentasinya mempertahankan region sumber.

## Preflight ledger — 3 November 2026 (snapshot sebelum migrasi)

Target Seagis `pawuvcovwmmimqrcudpd` / project `kibztbeviortyvbedogg` sehat dan terverifikasi melalui Management API. Ledger awal menemukan nomor 0007 cloud berisi environment API, sedangkan 0007 lokal berisi telemetry; migration cloud `20261029132449_environment_context_variable_fix` juga belum ada di source. Commit `07a1d4a` mengarsipkan kedua source cloud persis dan memindahkan telemetry yang belum diterapkan ke nomor 0009. Seluruh delapan migration applied kini exact-match; pending hanya `0008_spatial_location_mapping` dan `0009_operational_telemetry`.

106 test, HTTP integration lokal, dan [CI commit rekonsiliasi](https://github.com/De-Voeux/Seagis-Backend/actions/runs/41646559879) lulus. Deployment `scripts/deploy_a3.py --apply` belum dijalankan: automatic approval review menolak karena mutasi cloud, registrasi policy, serta provisioning/refresh credential dan role worker memerlukan persetujuan eksplisit tepat sebelum aksi. Tindakan yang menunggu persetujuan: apply 0008/0009, registrasi policy spatial A3, provisioning/refresh restricted worker, lalu verifikasi ledger/TLS/grants. Tidak ada perubahan cloud pada preflight ini.

## Pembaruan CI — 3 November 2026 (status pada checkpoint tersebut)

Status terbaru: branch sudah dipublikasikan, perbaikan sudah di-commit dan di-push. Commit `ec0dd6d` memperbaiki lima lint errors; `98a0b5c` memulihkan mapping sintetis pada source bundle A3. Dua test temporal kini tetap memeriksa cadence/interval sambil mengharapkan support unknown sebagai blocking flag.

Seluruh 106 test Python dan integrasi HTTP A1 lulus pada PostgreSQL 17 lokal disposable. [GitHub Actions run 41645679469](https://github.com/De-Voeux/Seagis-Backend/actions/runs/41645679469) berhasil: Ruff, kontrak, Deno, database/HTTP dan curation A3 offline. Pada checkpoint 3 November, migration 0008 belum diterapkan ke Supabase dan ledger cloud belum diverifikasi ulang; langkah itu diselesaikan pada cutover 4 November di bagian status akhir.

## Snapshot awal sebelum publikasi dan perbaikan CI (historis)

Kode A0–A3 v0.2 dan dokumentasinya sudah disiapkan pada branch lokal `codex/track-a-v02-implementation` di repo `/Users/cindyram/Documents/Apple/Seagis-Backend`. Perubahan masih berupa working-tree diff: **belum di-commit, belum di-push, dan belum diterapkan ke Supabase**. Branch dimulai dari `f155184`; remote `origin` mengarah ke `https://github.com/De-Voeux/Seagis-Backend.git`.

Penyimpanan Supabase saat ini tidak berubah oleh pekerjaan ini. Pemeriksaan `supabase migration list --linked` berhenti dengan `DbConfigIpv6Error` (jaringan ini tidak mendukung IPv6), sehingga ledger cloud belum terverifikasi. Tidak ada `db push`, apply migrasi, provider fetch, atau perubahan credential.

## Yang disiapkan

### A0 — identitas spasial dan versi lokasi

Migration baru `supabase/migrations/0008_spatial_location_mapping.sql` bersifat additive. Ia mempertahankan `seagis.source_grid` sebagai identitas lama, lalu menambahkan definisi grid dan cell sampling, versi lokasi point/polygon, mapping per location-version/dataset/parameter, tabel cell kontributor, serta riwayat support. Backfill tidak menebak geometri cell, ID provider, konteks perairan, atau bukti survei yang tidak tersimpan.

RPC pendaftaran lokasi dan pencatatan support dibatasi ke `service_role`; tabel tetap privat. Point baru dimulai sebagai `operator_unverified`; konteks air atau dukungan yang belum diketahui tetap `unknown`.

### A1 — status sensor

Read path history/status membedakan `no_sensor`, `no_observations`, `stale`, dan `available`. Tidak adanya perangkat tidak menjadi nilai nol dan tidak menghapus pemisahan antara pengukuran lokal dengan konteks model regional. Jalur ingestion IoT dan endpoint perangkat yang sudah ada tidak diganti pada tugas ini.

### A2 — resolver per lokasi

- Dispatcher mengambil lokasi point aktif dari database dan dapat dibatasi dengan `--plot-id`. UUID yang tidak dikenal gagal eksplisit; polygon dicatat dan dilewati dengan `unsupported_geometry`.
- Copernicus meminta nearest cell untuk tiap koordinat unik, lalu menyimpan returned cell dan request semantics untuk mapping lokasi.
- Open-Meteo meminta per lokasi dan memilih preferensi `sea`, `land`, atau `nearest` dari `water_context`; request yang identik dalam batch dipakai ulang.
- Data nilai tetap disimpan satu kali per source cell dan bisa dipakai beberapa lokasi melalui mapping. Request sukses atau koordinat returned tidak otomatis menjadi bukti support atau representativitas.

Command operasional setelah migration dan provisioning tersedia:

```sh
uv run --frozen --group environment python scripts/ingest_environment.py run --plot-id PLOT_UUID --force
uv run --frozen --group environment python scripts/ingest_environment.py preview --plot-id PLOT_UUID
```

Scheduler A2 yang ada masih berjalan sebagai LaunchAgent macOS setiap 15 menit selama Mac aktif dan user login. Perubahan ini **tidak** memindahkan scheduler ke Supabase atau membuat worker cloud 24/7.

### A3 — alignment dan quality snapshot

Builder menerima source bundle v1/v2 dan menghasilkan schema `a3-alignment-2` dengan policy `pilot-quality-spatial-1`. Metadata mapping, cell/grid identity, versi lokasi, status support, dan field validation dibawa ke setiap konteks regional. Pemilihan mapping dan support tunduk pada cutoff; bukti yang muncul setelah cutoff tidak membenarkan baris yang lebih lama. Lokasi belum terverifikasi, water context unknown, identity cell unknown/missing, mapping belum resolved, dan support yang belum confirmed menghasilkan blocking flag. `training_authorized` tetap false.

SQL `save_snapshot` memeriksa binding metadata spasial dengan source bundle dan menolak `schema_version`/`mode` kosong. Policy dan builder lama tidak ditimpa; config dan kontrak branch menggunakan versi baru.

### Handover dan dokumentasi repo

Dokumen baru `docs/spatial_mapping.md` menerangkan skema, status, RPC operator, resolusi A2, command, serta batas polygon/lake/coastline. Architecture, dictionary, ADR, source registry, operasi A1–A3 dan kontrak alignment diselaraskan dengan rancangan baru. Inventaris database di vault berasal dari snapshot cloud 22 Oktober dan belum diperbarui; gunakan catatan cutover di atas untuk status region dan perpindahan database.

## Status sisa dan batas pilot

1. **Migrasi dan cutover selesai, Seoul sudah dihapus.** Sebelas migration diterapkan; isi tabel aplikasi/Auth/monitoring cocok. Kedua commit final backend `22797ac` dan `1bf186e` masih lokal di branch `codex/sg-finalize-project-retirement`; CI yang telah lulus adalah run untuk commit terdahulu `e5976d7`, bukan dua commit final tersebut.
2. **Validasi implementasi A0–A3 sebelumnya lulus.** 106 test Python, integrasi HTTP A1 lokal, Ruff, dan smoke check cloud A3 sukses; smoke check itu tidak menyimpan snapshot baru serta mengembalikan `training_authorized=false`. Smoke `/environment` untuk plot A3 dengan reader berizin masih belum terverifikasi.
3. **Geografi dan dukungan ilmiah masih batas pilot.** RPC polygon hanya memeriksa tipe GeoJSON dan ukuran payload; belum memvalidasi topology, coastline, perairan yang sama, atau cell coverage. A2 sekarang point-only. Pemilihan Open-Meteo `sea`/`land` adalah preferensi cell, bukan validasi water-body. Dukungan sumber dan field validation perlu bukti terpisah. [Open-Meteo GFS API](https://open-meteo.com/en/docs/gfs-api); [Copernicus Marine Toolbox nearest](https://help.marine.copernicus.eu/en/articles/8684964-using-the-copernicus-marine-toolbox-in-operational-workflows).
4. A4, feature engineering, model training, forecast evaluation, dan migrasi scheduler cloud tidak termasuk scope. Scheduler A2 masih berjalan di Mac saat Mac aktif dan user login.

## Alur operasional setelah deploy

1. Daftarkan koordinat point dan konteks air yang memiliki sumber; lokasi baru tetap `operator_unverified` sampai diverifikasi. Pendaftaran polygon belum bisa masuk A2.
2. Jalankan ingestion untuk plot yang dipilih. Gunakan preview untuk memeriksa cell, jarak, nilai, status, dan waktu sumber tanpa menganggapnya pengukuran plot.
3. Catat `location_support` hanya dengan evidence coverage yang sesuai. `supported` bukan berarti field-validated; jangan mengubah field status ke `validated` tanpa pembandingan lapangan.
4. Jalankan curation A3 pada rentang jam UTC penuh dan review blocking flags. Simpan snapshot dengan `--persist` hanya setelah policy/kode branch terdaftar dan source bundle lulus guard.
5. Untuk perangkat IoT kelak, jalur tetap A1: device mengirim observation melalui fungsi `temperature` dengan credential device yang terikat sensor. Tugas ini tidak membuat endpoint public untuk mendaftarkan plot atau menulis support.

## Jejak kerja

- Rencana kebutuhan: [[Rencana Track A v0.2 - Pembaruan A0 sampai A3]].
- Implementasi backend sebelumnya ada di branch `codex/track-a-v02-implementation`; perbaikan parity dan runbook cutover terbaru ada di `22797ac` dan `1bf186e` pada branch `codex/sg-finalize-project-retirement`. Keduanya belum dipush.
- Deploy dan operasi DB dijelaskan di `docs/operations/singapore_migration.md` pada repo backend.
- [[Indeks - Engineering]].
