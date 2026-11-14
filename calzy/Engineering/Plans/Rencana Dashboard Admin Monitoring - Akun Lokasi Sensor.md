---
type: plan
project: "[[Challenge Final]]"
created: 2026-11-14
updated: 2026-11-14
status: proposed
tags: [challenge-final, seagis, engineering, monitoring, admin, plan]
---

# Rencana dashboard admin Monitoring — akun, lokasi dan sensor

**Status: rencana.** Belum ada kode, migration, deployment atau perubahan domain. Dokumen ini menjelaskan cara menambahkan halaman admin di Seagis Monitoring (target domain `monitoring.seagis.app`). Dari halaman itu admin bisa mengatur akun yang dipakai login di app iOS, lahan yang boleh dilihat tiap akun, lokasi lahan, dan sensor/hub yang dipakai.

Baseline: [[Handover Seagis - Status Pilot Tidung - 14 November 2026]]. Schema di bawah dibaca dari migration Seagis-Backend per 14 November 2026. Nama tabel dan fungsi baru masih usulan.

## 1. Masalah yang mau diselesaikan

Saat ini semua pengaturan pilot dilakukan manual oleh engineer:

| Kebutuhan | Cara sekarang | Masalah |
| --- | --- | --- |
| Membuat akun penyuluh | Admin membuat user di Supabase Auth dashboard | Perlu akses dashboard Supabase; tidak ada jejak siapa membuat apa |
| Menugaskan lahan ke akun | `scripts/deploy_account_auth.py --grant EMAIL --plot UUID` | Perlu checkout backend dan credential operator |
| Mendaftarkan lahan dan lokasi | RPC `register_plot` / `register_location_version` (khusus `service_role`) | Hanya bisa lewat SQL/script |
| Mendaftarkan sensor dan hub | Insert manual ke `seagis.sensor`, `seagis_api.sim_hub`, `sim_hub_node`, `seagis_app.node_installation` | Rawan salah mapping node ↔ lahan |
| Daftar lahan di app | Dahlan Lahan 1/2 dan polygon-nya di-hardcode di konfigurasi app | Lahan baru perlu rilis app baru |

Tujuannya: semua hal di atas bisa dikerjakan admin dari web, tercatat di audit log, tanpa membagikan credential database atau `service_role`.

## 2. Yang sudah tersedia

**Monitoring** (`Seagis-Monitoring`, Next.js 16 App Router, shadcn/ui, Vercel `sin1`):
- Login admin lewat `/login` → `/api/session`. Server memvalidasi password ke Supabase Auth, mencocokkan UUID user dengan allowlist admin di server, lalu menyetel cookie HttpOnly `__Host-seagis-session` (maksimal 1 jam, tanpa refresh token).
- Mutasi berbasis cookie mewajibkan header `Origin` same-origin persis.
- Runtime database `seagis_monitor_web` hanya boleh menjalankan fungsi baca yang di-allowlist. Tidak ada akses langsung ke tabel observasi atau credential.
- Alias produksi saat ini `seagis-monitoring.vercel.app`. Belum ada konfigurasi `monitoring.seagis.app` di repo.

**Backend** (`Seagis-Backend`, project Singapore):
- `auth.users` (Supabase Auth) dan `seagis_app.account_plot (user_id, plot_id, granted_at)`. Renew session membaca ulang penugasan, jadi perubahan berlaku paling lambat 1 jam.
- `seagis.plot` (kode, nama, titik, `is_synthetic`, `location_status`) dan `seagis.plot_location_version`, yang versioned dan append-only (titik/polygon, `location_status`, `water_context`, `provenance`, `effective_from`).
- RPC `seagis_environment.register_plot`, `register_plot_polygon`, `register_location_version` dan `register_location_polygon_version`, semuanya hanya untuk `service_role`. Lokasi baru selalu mulai dari status `operator_unverified`.
- `seagis.sensor` (satu sensor suhu **aktif** per lahan, lewat unique index), `seagis_api.sim_hub` (token hash, expiry, revoke, `is_synthetic` immutable), `sim_hub_node` (node 1–2 per hub → sensor), dan `seagis_app.node_installation` (node_code, installed_at, removed_at).
- `seagis_app.farmer` / `farmer_plot` / `plot_metadata` (luas lahan), yang dibaca app lewat resource `farmers` dan `plot`.

## 3. Keputusan yang perlu diambil dulu

| ID | Pertanyaan | Usulan default |
| --- | --- | --- |
| K1 | Siapa pemilik domain `seagis.app` dan DNS-nya? | Pemilik domain menambahkan CNAME `monitoring` ke Vercel; alias lama tetap aktif selama transisi |
| K2 | Bagaimana akun baru mendapat password? | **Undangan email** dari Supabase Auth. Admin tidak pernah melihat atau mengetik password penyuluh. Alternatif: password sementara sekali tampil, tapi app belum punya fitur ganti password |
| K3 | Di mana `service_role` disimpan? | **Tidak di Vercel.** Simpan sebagai secret Edge Function `admin-api` di Supabase (bagian 4) |
| K4 | Siapa yang boleh jadi admin dan apakah ada level peran? | Dua peran: `admin` (semua) dan `operator` (lokasi + sensor, tanpa akun). Disimpan di database, bukan hanya env allowlist |
| K5 | Apakah admin boleh menghapus akun? | Ya, karena juga dibutuhkan untuk App Store Guideline 5.1.1(v). Usulan: hapus = ban + cabut semua penugasan + revoke session; hard-delete terpisah |
| K6 | Signup publik Supabase Auth | Matikan (`disable_signup=true`) sebelum dashboard dirilis, karena akun hanya dibuat admin |
| K7 | Apakah app membaca daftar lahan dan polygon dari backend? | Ya; konfigurasi hardcode Dahlan di app diganti `plot_ids` + resource `plot` (bagian 6) |

## 4. Arsitektur yang diusulkan

```
Browser admin ── HTTPS ──▶ monitoring.seagis.app (Next.js, Vercel)
                              │  cookie admin (access token Supabase Auth)
                              │  /api/admin/* (route handler, same-origin, no-store)
                              ▼
                    Supabase Edge Function `admin-api`
                              │  verifikasi JWT admin + peran di seagis_admin.member
                              │  service_role (secret Edge, tidak keluar)
                     ┌────────┴─────────┐
                     ▼                  ▼
            Supabase Auth Admin    RPC seagis_admin.* (SECURITY DEFINER)
            (invite, ban, reset)   + audit log append-only
```

Alasannya:
- `service_role` dan Auth Admin API hanya ada di Supabase. Vercel tidak mendapat secret baru yang punya hak tulis.
- Route `/api/admin/*` di Monitoring cukup meneruskan access token admin dari cookie ke `admin-api`. Pola cookie, Origin check dan allowlist yang ada tetap dipakai.
- Runtime baca `seagis_monitor_web` tidak diberi hak tulis. Mutasi hanya lewat fungsi `seagis_admin.*` yang di-grant ke role khusus Edge.
- Setiap mutasi menulis `seagis_admin.audit_event` (aktor, aksi, target, before/after ringkas, waktu, request id) dalam transaksi yang sama.

## 5. Paket kerja

### P0 — keputusan dan domain (Monitoring + pemilik domain)

1. Putuskan K1–K7.
2. Tambahkan domain `monitoring.seagis.app` di project Vercel yang ada, lalu pasang DNS. Pertahankan `seagis-monitoring.vercel.app` sampai cookie dan login di domain baru terverifikasi.
3. Cookie `__Host-` bersifat host-only, jadi admin perlu login ulang di domain baru. Origin check harus menerima domain baru, dan domain lama dihapus setelah transisi.
4. Perbarui `docs/DEPLOYMENT.md` dan `docs/AUTHENTICATION.md` dengan domain baru.

Selesai jika: login admin berhasil di `monitoring.seagis.app`, smoke 401/307 sama dengan alias lama.

### P1 — schema admin (Seagis-Backend, migration aditif)

- `seagis_admin.member (user_id → auth.users, role in ('admin','operator'), created_at, created_by, revoked_at)`. Ini menggantikan atau melengkapi allowlist UUID di env Monitoring; env allowlist tetap jadi bootstrap admin pertama.
- `seagis_admin.audit_event`, append-only lewat trigger seperti tabel audit lain.
- Fungsi SECURITY DEFINER, `search_path=pg_catalog`, di-grant hanya ke role Edge admin:
  - Akun: `list_accounts`, `grant_plot(user, plot)`, `revoke_plot(user, plot)`, `deactivate_account(user)` (cabut penugasan + revoke credential session aktif).
  - Lahan dan lokasi: `create_plot` (membungkus `register_plot`/`register_plot_polygon`), `add_location_version` (versi baru, tidak pernah mengedit versi lama), `set_location_status` (misalnya `operator_unverified` → `surveyed`, wajib isi provenance).
  - Sensor dan hub: `commission_hub` (mengembalikan token **sekali tampil**, yang disimpan hanya hash), `revoke_hub`, `register_sensor(plot, code, depth)`, `bind_node(hub, node_id, sensor)`, `record_installation(sensor, node_code, installed_at)`, `retire_sensor(sensor, removed_at)`.
- Aturan yang dipertahankan: satu sensor suhu aktif per lahan; provenance hub immutable (fisik ≠ sintetis, perlu hub baru); node 1–2 per hub; lokasi versioned; tidak ada mutasi observasi atau raw data dari dashboard.
- Tes SQL dalam transaksi yang di-rollback, mengikuti pola `tests/account_sessions.sql`.

### P2 — Edge Function `admin-api` (Seagis-Backend)

- Endpoint JSON berversi `/v1/...` untuk akun, lahan, lokasi, sensor, hub dan audit.
- Verifikasi JWT Supabase Auth dari header, cek `seagis_admin.member` dan peran, rate limit, batas ukuran body, dan tolak field yang tidak dikenal.
- Akun memakai Auth Admin API: invite (K2), resend invite, kirim reset password, ban/unban. Email, password dan token tidak dicatat ke log.
- Respons tidak pernah memuat token Auth, refresh token, hash credential atau `service_role`.
- Tes Deno untuk routing, otorisasi per peran, validasi body dan outage 503, seperti tes `account-auth`.

### P3 — halaman admin di Monitoring

Tambahkan grup navigasi **Pengaturan** di sidebar, hanya untuk member `admin`/`operator`:

1. **Akun app**
   - Tabel: email, status (diundang / aktif / nonaktif), lahan yang ditugaskan, login terakhir (jika tersedia), session aktif.
   - Aksi: undang akun, kirim ulang undangan, kirim reset password, tugaskan/cabut lahan (multi-select), nonaktifkan, hapus.
   - Catatan di UI: perubahan lahan berlaku di app paling lambat 1 jam (siklus renew).
2. **Lahan dan lokasi**
   - Peta (memakai komponen peta spasial yang ada) dengan daftar lahan, titik/polygon versi aktif, `location_status`, `water_context` dan provenance.
   - Aksi: buat lahan, tambah versi lokasi (titik atau gambar polygon), tandai surveyed. Riwayat versi tampil dan tidak bisa diedit.
   - Validasi: koordinat di dalam area pilot, peringatan kalau titik jatuh di darat/land mask, wajib isi provenance.
3. **Sensor dan hub**
   - Daftar hub (label, fisik/sintetis, expiry, revoked), node → sensor → lahan, instalasi dan pelepasan, status terakhir dari dashboard device yang ada.
   - Aksi: commission hub (token tampil sekali dengan tombol salin, tidak disimpan di browser), bind node, daftarkan sensor, catat instalasi, retire.
   - Peringatan saat mengganti sensor aktif sebuah lahan: sensor lama harus di-retire dulu.
4. **Audit**
   - Daftar `audit_event` yang bisa difilter berdasarkan aktor, aksi dan target, dalam WIB.

Aturan implementasi Monitoring: route di `app/api/admin/*`, handler di `lib/handlers/`, tanpa folder root `api/`, semua respons `no-store`, Origin check pada setiap mutasi, dan form memakai komponen shadcn/ui yang ada. Ikuti `AGENTS.md` repo Monitoring: jalankan typecheck, lint, test, test:components dan build; catat hasilnya di `docs/VERIFICATION.md`.

### P4 — app iOS membaca lahan dari backend

- Ganti daftar lahan dan polygon Dahlan yang di-hardcode dengan `plot_ids` dari session plus resource `plot` (nama, lokasi versi aktif, sensor, luas).
- Aturan yang ada tetap berlaku: lahan tanpa sensor aktif tetap tampil dengan konteks regional berlabel; data kosong tetap kosong.
- Tambahkan fitur hapus akun di app. Bisa memanggil endpoint yang sama dengan `deactivate_account` lewat app-api dengan session pengguna sendiri (K5).
- Tes: mapping kontrak `plot`, cache per lahan saat penugasan berubah, akun tanpa lahan (403).

### P5 — verifikasi dan rollout

1. Tes lokal semua repo, migration diuji di database PostgreSQL disposable, lalu rollback-only check di production.
2. Apply migration production dan deploy `admin-api` serta Monitoring, masing-masing dengan izin eksplisit pengguna.
3. Acceptance end-to-end di production dengan akun uji yang dihapus setelahnya:
   - undang akun → terima email → set password → login di app → lihat lahan yang ditugaskan;
   - cabut lahan → hilang dari app setelah renew;
   - nonaktifkan akun → login ditolak;
   - tambah versi lokasi → app menampilkan lokasi baru;
   - commission hub uji (sintetis) → bind → revoke;
   - semua langkah tercatat di audit.
4. Matikan signup publik (K6), lalu hapus fungsi `apple-auth` yang sudah pensiun.

## 6. Keamanan dan batas

- Tidak ada `service_role`, password database atau token hub yang masuk Vercel, browser, log, Git atau vault.
- Token hub hanya ditampilkan sekali saat commission; setelah itu hanya hash yang tersimpan.
- Admin tidak bisa membaca atau mengubah observasi, raw payload atau credential session dari dashboard.
- Lokasi dari dashboard berstatus `operator_unverified` sampai ditandai surveyed dengan provenance. Status ini tidak mengubah status kualitas data sensor.
- Koordinat lahan petani adalah data operasional dan tidak disalin ke vault publik.
- Dashboard tidak membuat penilaian risiko ice-ice; ia hanya mengatur identitas, akses dan registry.

## 7. Urutan dan estimasi kasar

| Urutan | Paket | Repo | Tergantung |
| --- | --- | --- | --- |
| 1 | P0 keputusan + domain | Monitoring, DNS | — |
| 2 | P1 schema admin | Backend | K2–K5 |
| 3 | P2 `admin-api` | Backend | P1 |
| 4 | P3 halaman admin | Monitoring | P0, P2 |
| 5 | P4 lahan dinamis + hapus akun | iOS | P1 (resource `plot` sudah ada) |
| 6 | P5 rollout | Semua | P1–P4 |

P4 bisa dikerjakan paralel dengan P2/P3 karena resource `plot` dan `plot_ids` sudah ada di backend.

## Sumber

- Monitoring: `AGENTS.md`, `docs/AUTHENTICATION.md`, `docs/DEPLOYMENT.md`, `docs/VERIFICATION.md` pada `511eeb0`.
- Backend: `supabase/migrations/0001_initial_schema.sql`, `0006_hub_simulator.sql`, `0008_spatial_location_mapping.sql`, `20261106000100_physical_hub_provenance.sql`, `20261112090100_app_identity_sessions.sql`, `20261112090200_app_farm_reads.sql`, `20261114130000_account_sessions.sql` (belum di-commit), dan `docs/operations/2026-11-14-account-sessions.md`.
- iOS: `docs/progress/2026-11-14-account-login.md`.
