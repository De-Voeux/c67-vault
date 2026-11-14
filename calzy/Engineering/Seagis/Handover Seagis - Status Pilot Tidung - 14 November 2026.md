---
type: handover
project: "[[Challenge Final]]"
updated: 2026-11-14
tags: [challenge-final, seagis, engineering, handover, monitoring, iot]
---

# Handover Seagis — status pilot Tidung 14 November 2026

Snapshot 14 November 2026 sekitar 17:10 WIB. Catatan ini melanjutkan [[Handover Seagis - Integrasi dan Kesiapan Rilis - 12 November 2026]] dan hanya memuat perubahan setelah snapshot 12 November 22:45 WIB. Isinya ringkasan dari dokumen di tiap repository dan riwayat GitHub; tes tidak dijalankan ulang untuk catatan ini. Status yang dikutip berasal dari dokumen sumber yang disebut di tiap bagian.

**Kesimpulan:** dua probe fisik sudah dipasang di Pulau Tidung (13 November, ±13:56 WIB) dan dipetakan ke Dahlan Lahan 1 dan Lahan 2. Datanya masuk ke backend, tetapi semua observasi masih `suspect` (basis waktu `hub_rx`) dan belum layak untuk forecast atau training. Login penyuluh dengan email/password sudah live di backend; jalur Sign in with Apple dinonaktifkan. Pekerjaan iOS dan backend 14 November **belum di-push**; sebagian masih uncommitted.

## 1. Keputusan baru

- **Login penyuluh: email + password**, akun dibuat admin di Supabase Auth. Sign in with Apple tidak dipakai; pilot Apple di backend sudah dimatikan (endpoint `apple-auth` membalas 503).
- **Backend yang menentukan lahan per akun** (`seagis_app.account_plot`). App tidak mengirim plot atau scope.
- **Akun pilot Tidung** ditugaskan ke Dahlan Lahan 1 (`f528fa6e-…`) dan Lahan 2 (`c3f989aa-…`). Belum ada entitas wilayah/pulau; penugasan per plot.
- **Team Apple Developer final: 38L62PN5D7**, terhubung App Store Connect (`docs/open-decisions.md` D02).
- **Offline device** = tidak ada paket diterima lebih dari 3 jam (berbasis `ingested_at`, bukan cadence).
- **Seluruh tampilan Monitoring memakai WIB**; timestamp kanonik JSON/ingestion tetap UTC instant.

Keputusan 12 November tetap berlaku. Bagian yang berubah: probe fisik kini sudah dipetakan ke Lahan Dahlan berdasarkan lokasi pemasangan, bukan lagi "belum dipetakan".

## 2. Baseline

| Komponen | Branch lokal | Commit | Remote |
| --- | --- | --- | --- |
| iOS | `feat/account-login` | `a64544b` + perubahan uncommitted | Belum di-push |
| Backend | `feat/20261114-account-sessions` | `5322521` (main setelah PR #16) + semua file account/Apple untracked | Belum di-push, belum ada PR |
| Monitoring | `codex/20261113-prod-dashboard-check` | `511eeb0`, merged via PR #10 | Sinkron dengan origin |

## 3. Seagis iOS

### Sudah di-merge (12–14 November)

- PR #42: fondasi guest session dan wiring container.
- PR #43: tab bar baru.
- PR #44: perbaikan error.
- PR #45 (merged 14 Nov 15:22 WIB): release-readiness, termasuk commit localizable `2cf96f2`.

### Integrasi sensor Dahlan — commit `a64544b` (lokal)

Sumber: `docs/progress/2026-11-14-dahlan-physical-integration.md`. Status: implemented dan tested lokal.

- Anchor kedua lahan mengikuti titik pemasangan sensor (koordinat persis disimpan di dokumen progress repo iOS, tidak disalin ke vault publik). Polygon digeser agar centroid tepat di sensor; batas tetap ilustrasi, bukan survei.
- History dikunci 13–17 November WIB. Hari tanpa data tetap kosong; sampel setengah jam tetap terpisah.
- `suspect` tampil dengan label perlu verifikasi; `missing`/`rejected` tidak jadi titik grafik. Tidak ada penilaian risiko otomatis, forecast buatan, atau fallback SST yang menyamar sebagai suhu sensor.
- Koneksi reader token runtime (Keychain) ditambahkan untuk Release; credential verifikasi lokal berakhir 6 Desember 2026.
- Bukti: 169 tes / 36 suite lulus di simulator, build Release generic lulus, credential tidak ditemukan di executable Release. Snapshot cek history: Node 1 14 record (suspect), Node 2 25 record (24 suspect, 1 rejected).

### Login akun penyuluh — uncommitted

Sumber: `docs/progress/2026-11-14-account-login.md` (untracked). Status: implemented dan tested di simulator; belum di-commit.

- Layar pertama adalah login; peta tampil setelah session berisi kedua lahan Dahlan dan langsung membuka Lahan 1.
- Hanya refresh token dan metadata session yang disimpan di Keychain; access token di memori; password tidak disimpan. Session berlaku 30 hari sejak login.
- Session akun tidak jatuh ke guest atau reader token operator. Menu input reader token manual dihapus dari peta (`PhysicalReaderSession` tetap ada untuk tes).
- Bukti: 175 tes / 37 suite lulus (termasuk 6 `AccountSessionTests`). Test lama banner peta di-skip karena perlu fixture login.
- Login dengan password asli di perangkat belum diuji agent.
- Draft `ADR-003-penyuluh-auth-sign-in-with-apple.md` yang sempat ada di working tree sudah tidak ada lagi, sesuai keputusan tidak memakai Apple.

### Belum selesai di iOS

- Lupa/ganti password belum ada di app (reset lewat admin).
- **Hapus akun di app belum ada**, padahal wajib sebelum App Store (Guideline 5.1.1(v)). Akun demo untuk App Review juga belum ada.
- Lahan dan polygon Dahlan masih dari konfigurasi app; belum dinamis dari `plot_ids`/`/v1/farmers`.
- Archive bertanda tangan, upload App Store Connect, dan TestFlight belum dilakukan.

## 4. Seagis-Backend

### Operasi rilis pilot — PR #16 (merged 13 November)

Sumber: `docs/operations/handover-release-ops-20261113.md`.

- Target rilis pilot tetap project Singapore `mdtmupiftllpglkfoaqy`; tidak ada resource berbayar baru.
- Workflow A2 kini menyimpan artifact state per run selama 14 hari (`dispatcher.json`, `worker.jsonl`, `providers.json`), jadi outcome tetap tercatat saat database tidak bisa dihubungi (`fc5834a`).
- Worker SST menyimpan 192 nilai baru; alignment A3 empat snapshot berhasil; Open-Meteo gagal dengan `network_failure` dan state error/retry tersimpan.
- Scheduler Mac (LaunchAgent) tidak ada; tidak lagi diandalkan.
- Masih terbuka: plot `…0002` belum masuk active_plot_locations; Open-Meteo belum terbukti pulih.

### Login akun dan pilot Apple — uncommitted, tetapi sudah live

Sumber: `docs/operations/2026-11-14-account-sessions.md` dan `2026-11-14-apple-owner.md` (keduanya untracked).

- Live di production: migration `20261114130000_account_sessions.sql` dan fungsi `account-auth`.
- `POST /functions/v1/account-auth/v1/login` menerima `{email, password}` saja. Respons 201 berisi session Seagis (access 1 jam, refresh 30 hari) dan `plot_ids`. Kode error: 401 `invalid_credentials`/`account_inactive`, 403 `no_plot_access`, 503 `temporarily_unavailable`.
- Renew dan logout memakai app-api yang ada. Renew membaca ulang penugasan, jadi perubahan lahan berlaku paling lambat satu jam; akun di-ban atau penugasan dicabut memutus akses.
- Pilot Apple (`20261114100000_apple_owner_sessions.sql`, fungsi `apple-auth`) sempat live, lalu EXECUTE dicabut. Slot pemilik tidak pernah diklaim. Fungsi Edge `apple-auth` masih terdeploy dan bisa dihapus terpisah.
- Operasi penugasan: `scripts/deploy_account_auth.py --grant EMAIL --plot UUID` (untracked).
- Bukti: Deno 5 tes `account-auth` + regresi app-api 7 dan apple-auth 3 lulus. SQL `tests/account_sessions.sql` dijalankan di production dalam transaksi yang di-rollback. Smoke live: password salah 401, field tambahan 400, guest tetap 201.
- **Risiko terbuka:** signup publik Supabase Auth masih aktif (`disable_signup=false`). Akun baru tanpa penugasan tidak mendapat data, tetapi signup sebaiknya dimatikan.
- **Risiko repository:** migration dan fungsi sudah live di production, tetapi source-nya belum di-commit atau di-push. Kalau checkout ini hilang, production tidak bisa direkonstruksi dari Git.

### Audit ingestion IoT — 13 November (read-only)

Sumber: `docs/audits/2026-11-13-iot-ingestion-audit.md` (untracked). Window penerimaan 11:00–21:00 WIB.

- 29 observasi (14 Node A, 15 Node B) dan 77 record batch. Semua record ber-outcome `stored`, tetapi semua observasi `suspect` dengan flag `time_basis_hub_rx`; dua observasi Node B `missing` (tersimpan null, bukan nol).
- Terbukti: event `UPLOAD_FAIL` dan backlog. Satu record Node B berlabel 18:08 baru diterima 20:06 (selisih ±1 jam 58 menit). Ada juga label waktu hub yang ±3 menit 47 detik lebih maju dari server (`clock_ahead`).
- Node A: tidak ada observasi tersimpan setelah label 11:46; yang masuk hanya `gap/no_rx` dari 13:14 sampai 20:07. Node B: reset `watchdog` berulang dan antrean 48 terlapor.
- Belum terbukti: akar masalah (seluler, LoRa, daya, probe, NVS/SD, atau bug `estimateObs`). Firmware tidak diperiksa langsung.
- Rekomendasi P0 (belum diimplementasikan): cek fisik daya/probe/watchdog di lokasi dan ekspor log hub. Jangan mengklaim freshness atau forecast dari `hub_rx`. Pisahkan paket terakhir diterima, pengukuran aktual terakhir, dan nilai valid/suspect terakhir.

## 5. Seagis-Monitoring (PR #5–#10, 13 November)

Sumber: `docs/VERIFICATION.md`, `docs/TIDUNG-LIVE-HANDOVER.md`, `docs/WIB-TIMEZONE.md` pada `511eeb0`.

- **Tidung live (PR #5, #6):** migration `0009_live_devices` diterapkan setelah izin eksplisit pengguna. Empat sensor sintetis dinonaktifkan, test hub dicabut, dua sensor fisik aktif. Deployment `dpl_432AZrQ5…` READY.
- **WIB (PR #7, #8):** migration `0010` (default database Asia/Jakarta) dan `0011` (pin timezone pada fungsi dashboard/overview/spatial karena pooler tetap UTC). Semua tampilan Monitoring kini WIB. Deployment terakhir yang tercatat: `dpl_4nWJENGP…` (source `b5b6d92`).
- **Device offline dan bacaan terakhir:** `0009_device_offline_3h`. Kolom suhu dan "Last reading (WIB)" dipisah; QC pindah ke detail device.
- **shadcn/ui (PR #9):** lulus tes lokal (18 Node, 61 komponen, build) dan cek visual pada harness sintetis. Deployment produksi untuk PR #9 tidak tercatat di `VERIFICATION.md`.
- **Urutan migration:** dua migration `0009` saling bergantung. Database baru wajib menerapkan `0009_live_devices` sebelum `0009_device_offline_3h`, sesuai `scripts/verify_database.py`.
- **Cek produksi read-only (PR #10):** fungsi `dashboard` di production sudah versi `0009_device_offline_3h` dengan `TimeZone=Asia/Jakarta`.
- Belum diuji: login administrator dan penerimaan UI setelah login.

## 6. Scheduler — pembaruan status 12 November

Catatan 12 November menulis event jadwal otomatis "belum teramati". Per 14 November, `gh run list -e schedule` menunjukkan event schedule sudah berjalan di kedua repository:

| Workflow | Lima event schedule terakhir (WIB) | Conclusion |
| --- | --- | --- |
| Monitoring `hourly-monitoring.yml` | 13 Nov 10:22, 19:05; 14 Nov 03:26, 08:24, 15:54 | success semua |
| Backend `a2-ingestion-scheduler.yml` | 13 Nov 08:44, 16:20; 14 Nov 00:36, 06:25, 12:51 | success semua |

Jarak antar-event terlihat sekitar 5–9 jam, bukan per jam. Ini sejalan dengan catatan release-ops bahwa GitHub schedule bisa berjeda lebih dari empat jam. Conclusion `success` adalah status run workflow; isi artifact atau output collector tiap run belum diperiksa untuk catatan ini. Kalau SLA per jam dibutuhkan, perlu host always-on yang disepakati.

## 7. Handoff berikutnya

1. **Amankan source:** commit dan push branch iOS `feat/account-login` dan backend `feat/20261114-account-sessions`, terutama migration dan fungsi yang sudah live di production.
2. **Matikan signup publik** Supabase Auth.
3. **Hapus fungsi `apple-auth`** yang sudah pensiun (opsional, terpisah).
4. **IoT di lokasi:** cek daya, probe dan watchdog Node A/B; ekspor log hub; verifikasi `estimateObs` dan sinkronisasi jam.
5. **Syarat App Store:** hapus akun di app, akun demo App Review, fixture login untuk UI test, lalu archive bertanda tangan dan TestFlight.
6. **Uji login asli** di perangkat fisik dengan akun pilot.
7. **Rotasi reader credential** sebelum 6 Desember 2026, kalau jalur reader runtime masih dipakai.
8. **Konfirmasi deployment Monitoring** untuk PR #9 (shadcn) dan penerimaan UI setelah login admin.

Rencana dashboard admin untuk akun, lokasi dan sensor ada di [[Rencana Dashboard Admin Monitoring - Akun Lokasi Sensor]]. Catatan ini dan catatan 12 November sudah ditautkan dari [[Indeks - Engineering]].

## Sumber

- [[Handover Seagis - Integrasi dan Kesiapan Rilis - 12 November 2026]] — baseline sebelumnya.
- iOS: `docs/progress/2026-11-14-dahlan-physical-integration.md`, `docs/progress/2026-11-14-account-login.md`, `docs/open-decisions.md` (working tree 14 Nov), commit `a64544b`, PR #42–#45.
- Backend: `docs/operations/handover-release-ops-20261113.md`, `docs/operations/2026-11-14-account-sessions.md`, `docs/operations/2026-11-14-apple-owner.md`, `docs/audits/2026-11-13-iot-ingestion-audit.md`, PR #16.
- Monitoring: `docs/VERIFICATION.md` pada `511eeb0`, PR #5–#10.
- GitHub Actions: `gh run list -e schedule` untuk kedua workflow, 14 November 2026 ±17:09 WIB.
