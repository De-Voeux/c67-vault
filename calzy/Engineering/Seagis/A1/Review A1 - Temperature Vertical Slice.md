---
type: engineering-review
project: "[[Challenge Final]]"
created: 2026-10-22
updated: 2026-10-22
status: implemented-a1-development
source_commit: "96820a997060bec6aedf732779c7acd62fe8e96a"
tags: [challenge-final, seagis, engineering, a1, iot]
---

# Review A1 — temperature vertical slice

Status: **selesai, tervalidasi lokal dan di project development Supabase Seagis**. Pemeriksaan live terakhir 22 Oktober 2026, 03:34 UTC / 10:34 WIB. Hardware IoT belum tersedia; seluruh 136 observasi cloud adalah sintetis. A2 belum dimulai.

## Hasil dan lokasi

| Deliverable | Lokasi |
|---|---|
| Handover arsitektur, access point, payload, auth dan retry hardware | [[Handover A1 - Arsitektur Data dan Akses IoT]] |
| Provisioning, operasi dummy data, deployment dan troubleshooting | [[Operasi A1 - Simulator dan Credentials]] |
| API SQL privat, role gateway, credential scope, QC dan history | [0002_temperature_api.sql](</Users/cindyram/Documents/Apple/Seagis-Model/supabase/migrations/0002_temperature_api.sql>) |
| Edge Function temperature, HTTP boundary dan koneksi TLS | `supabase/functions/temperature/` |
| Kontrak paket IoT | [iot-packet.schema.json](</Users/cindyram/Documents/Apple/Seagis-Model/contracts/iot-packet.schema.json>) |
| Fixture 72 jam per plot | [hourly_synthetic.json](</Users/cindyram/Documents/Apple/Seagis-Model/fixtures/a1/hourly_synthetic.json>) |
| Simulator dan validasi cloud | `scripts/simulate_temperature.py`, `scripts/check_a1_live.py` |
| Pengujian DB, HTTP, retry dan keamanan | `tests/test_a1*.py`, `scripts/check_a1_http.py`, `handler.test.ts` |
| Bukti deployment dan pengujian live yang tidak mengandung secret | [validation_20261022.json](validation_20261022.json) |

## Pengujian dan acceptance

**63 Python tests dan 7 Deno tests lulus**, ditambah integration melalui proses HTTP Deno asli. SQL migration dijalankan dari database kosong; A0 tetap lolos. Uji HTTP mengirim 140 delivery: 136 insert, dua duplicate dan dua conflict; replay 140 delivery berikutnya tidak menambah observasi. Delapan concurrent retries atas satu paket menghasilkan satu insert dan tujuh duplicate dengan observation ID sama. Suite yang sama juga lulus di PostgreSQL lokal dengan TCP + SCRAM/password authentication, mengikuti batas autentikasi CI yang berbeda dari Unix socket trust.

Pemeriksaan live berhasil menguji 10 batas: health, tanpa token, perbedaan device/reader, sensor binding, penolakan spoofing `is_synthetic`, duplicate, conflict, plot yang tidak diizinkan dan reader status. Semua halaman riwayat dicocokkan dengan fixture dan identitas sensor/plot. Role gateway terverifikasi tidak dapat membaca tabel observation secara langsung. Lint, format dan `git diff --check` lulus. Workflow CI sudah diperbarui; belum dijalankan di GitHub pada pekerjaan ini karena tidak ada push.

| Acceptance A1 | Hasil |
|---|---|
| Duplikat tidak membuat pengukuran ganda | Lulus SQL, HTTP lokal, concurrency dan live replay; observation/run ID tetap |
| Paket terlambat mempertahankan observation time | Lulus; `observed_at` berasal dari paket, `ingested_at` dari server; delayed/out-of-order diberi flag |
| Gap, nilai bermasalah dan stale eksplisit | Lulus; missing/unusable hourly slots, quality events dan freshness berdasarkan observed time |
| Riwayat A/B dapat diambil independen | Lulus; masing-masing 68 observasi dari 72 slot, 4 gap, 1 null dan 1 nilai rejected |
| Jalur hardware siap sebelum alat tersedia | Endpoint/provisioning/sensor binding tersedia; commissioning sensor non-sintetis diperiksa lokal dengan real-ingestion gate |

Aturan kualitas A1 bersifat engineering sementara. `usable` pada coverage bukan label layak training; hardware dan biologinya belum tervalidasi.

## Cloud yang sudah berubah

- Target tunggal organisasi `pawuvcovwmmimqrcudpd`, project `kibztbeviortyvbedogg`, region Seoul.
- Migrasi **0001 dan 0002** diterapkan dan versi ledger cocok dengan lokal; source setiap migration diperiksa identik saat redeploy.
- Seed dua plot/sensor sintetis terpasang. Total **136 observasi sintetis, 0 observasi nyata**, beserta raw JSONB, provenance, quality events dan request audit.
- Fungsi `temperature` berstatus **ACTIVE**, deployment version **3** pada snapshot evidence; endpoint `https://kibztbeviortyvbedogg.supabase.co/functions/v1/temperature`.
- Login gateway khusus dan dua Edge secrets (URL database serta public CA) dikonfigurasi. Gateway memakai TLS dengan CA dan hostname verification, bukan trust store sistem yang tidak mencakup CA privat Supabase.
- Tiga credential pilot diprovisikan: device A, device B, reader A/B. Default expiry 30 hari; nilai token hanya di `.env.a1.devices` lokal mode 0600. `.env.a1.gateway` juga lokal mode 0600 dan diabaikan Git.
- Semua `real_ingestion_enabled` tetap false. Tidak ada bucket raw nyata, scheduler provider atau koneksi hardware yang diaktifkan.

Kedua plot memang stale pada snapshot: fixture historis berakhir 22 Oktober 00:00 UTC, dan pembacaan terakhirnya 21 Oktober 23:00 UTC. Ini menguji penanganan data lama; bukan kegagalan deployment.

## Batas handoff

Receiver dapat memakai endpoint dan kontrak yang sama setelah probe, transport, clock, daya, lokasi/depth dan credential sensor nyata selesai dikomisioning. UUID/label sintetis tidak diubah menjadi nyata. Sampai itu dilakukan, hanya simulator yang dioperasikan.

Belum ada autentikasi pengguna iOS, pengiriman otomatis perangkat fisik, notifikasi monitoring, purge log otomatis, atau SLA produksi. Reader token A1 digunakan backend/operator development. Raw sensor nyata masih metadata-only. A2–A6, model forecasting dan validasi ice-ice tetap tahap berikutnya.

Perubahan menggunakan Conventional Commits pada branch kerja A1. Tidak ada push, PR, training atau ingestion provider regional pada pekerjaan ini. Catatan handover juga disimpan dalam Second Brain di `Challenge Final/Engineering/Seagis/A1/`.

Provenance snapshot: [[Provenance A1 - Paket Handover 22 Oktober 2026]].
