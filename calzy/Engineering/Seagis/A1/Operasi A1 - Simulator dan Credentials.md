---
type: runbook
project: "[[Challenge Final]]"
created: 2026-10-22
updated: 2026-10-22
status: implemented-a1-development
source_commit: "96820a997060bec6aedf732779c7acd62fe8e96a"
tags: [challenge-final, seagis, engineering, a1, iot]
---

# Operasi A1 — simulator, credentials dan deployment

Tanggal: 22 Oktober 2026. Root kode: `/Users/cindyram/Documents/Apple/Seagis-Model`. Gunakan [[Handover A1 - Arsitektur Data dan Akses IoT]] untuk kontrak paket, arsitektur dan semantics QC.

## Validasi lokal yang disposable

Prasyarat: Python ≥3.11, uv, PostgreSQL 17 dan Deno 2.8.3. Hardware, Docker dan credential cloud tidak diperlukan.

```sh
uv sync --frozen --group dev
uv run --frozen ruff check scripts tests
uv run --frozen ruff format --check scripts tests
deno task --config supabase/functions/temperature/deno.json check
uv run --frozen python scripts/validate_contracts.py
uv run --frozen python scripts/check_a1.py
```

Runner membuat database sementara, menerapkan semua migrasi, seed dua kali, menjalankan pengujian kontrak/database, lalu Deno HTTP asli memakai login gateway terbatas. Ia menguji fixture lewat HTTP, replay, pagination, perbedaan plot, credential scope, dan delapan concurrent retries. Process HTTP dan PostgreSQL dihentikan dan data lokal dibersihkan. CI menjalankan jalur yang sama dengan container PostgreSQL sementara; CI bukan deployment cloud otomatis.

## Deployment development Seagis

```sh
uv run --frozen python scripts/deploy_a1.py
uv run --frozen python scripts/deploy_a1.py --apply
```

Command pertama hanya memverifikasi organisasi/project dan membaca migration history. `--apply` menerapkan migrasi SQL dalam transaksi dan mencatat versi lokal **0001/0002** beserta source utuh pada ledger `supabase_migrations.schema_migrations`. Skrip tidak menggunakan API yang mengganti versi dengan timestamp otomatis; source migration yang sudah tercatat harus cocok persis atau skrip berhenti. Jangan mengedit migration yang sudah diterapkan; buat migration baru.

Deployment juga menjalankan seed idempotent, membuat/reuse secret login gateway dalam `.env.a1.gateway` mode 0600, memverifikasi TLS dan privilege login, menaruh URL database dan public CA pada Edge secrets, lalu deploy fungsi `temperature` via Supabase CLI/API. Gateway role dibuat NOLOGIN oleh migration dan baru diaktifkan di tahap provisioning. Seluruh schema tetap di luar daftar schema Data API.

PAT dibaca lokal dari environment atau Supabase CLI Keychain macOS. Izin deployment: Database Read/Write, Migrations Read/Write, Edge Functions Read/Write, Edge Function Secrets Read/Write, Database Pooling Config Read serta Project Settings Read. Seluruh request admin dikunci ke organisasi `pawuvcovwmmimqrcudpd` / project `kibztbeviortyvbedogg`. Jangan menaruh PAT di device atau repo.

TLS root CA diambil lewat HTTPS dari URL resmi Supabase download dan fingerprint DER SHA-256 dipin `807025ad50d4ed219d2c9c7d299c004f824eb00cf7f65afef607d07b72e6cafa`. Pergantian CA memerlukan peninjauan, bukan menonaktifkan certificate verification. Referensi: [Postgres SSL](https://supabase.com/docs/guides/platform/ssl-enforcement), [PSQL](https://supabase.com/docs/guides/database/psql), [pooler/serverless connections](https://supabase.com/docs/guides/database/connecting-to-postgres), [Edge deployment](https://supabase.com/docs/guides/functions/deploy).

## Credentials operator, reader dan device

```sh
uv run --frozen python scripts/provision_a1.py demo
```

Tiga credential pilot dibuat: simulator A, simulator B dan reader untuk kedua plot. Token acak hanya ditulis ke `.env.a1.devices` mode 0600; database hanya menyimpan hash. Default expiry 30 hari. File sudah ada tidak ditimpa; untuk rotasi buat file/credential baru, uji, lalu revoke ID lama.

Isi `.env.a1.devices`:

| Key | Penggunaan |
|---|---|
| `SEAGIS_API_BASE_URL` | Endpoint HTTPS fungsi temperature |
| `SEAGIS_DEVICE_A_TOKEN` / `SEAGIS_DEVICE_B_TOKEN` | Ingestion, hanya sensor masing-masing |
| `SEAGIS_READER_TOKEN` | History/status, hanya dua plot demo |
| `*_CREDENTIAL_ID` | Identitas revocation, bukan token |

`.env.a1.gateway` adalah password backend terbatas, **bukan** file handover ke hardware. `.env.a1.devices` memuat beberapa actor; bagikan hanya token perangkat yang diperlukan. Tidak ada secret dalam catatan Second Brain. `.env.example` hanya placeholder.

Provisioning untuk sensor yang sudah terdaftar atau reader baru:

```sh
uv run --frozen python scripts/provision_a1.py device \
  --sensor-id REGISTERED_SENSOR_UUID --label tidung-probe-01 --days 30 \
  --out .env.device-tidung-probe-01

uv run --frozen python scripts/provision_a1.py reader \
  --plots REGISTERED_PLOT_UUID --label pilot-reader --days 30 \
  --out .env.reader-pilot

uv run --frozen python scripts/provision_a1.py revoke \
  --credential-id CREDENTIAL_UUID
```

Provisioning menyimpan secret lokal sebelum transaksi admin, agar secret dapat dipulihkan bila respons jaringan hilang setelah commit. Jika hasil provisioning tidak jelas, periksa credential ID dan hash di DB sebelum mencoba file baru; jangan menampilkan token dalam log.

## Dummy data dan bukti dua plot

```sh
uv run --frozen python scripts/simulate_temperature.py generate
uv run --frozen python scripts/simulate_temperature.py send
uv run --frozen python scripts/simulate_temperature.py verify
```

Fixture default: [hourly_synthetic.json](</Users/cindyram/Documents/Apple/Seagis-Model/fixtures/a1/hourly_synthetic.json>), **19 Oktober 2026 00:00 UTC sampai 22 Oktober 2026 00:00 UTC** (72 jam per plot). Total 140 delivery: 136 paket unik, dua replay identik dan dua conflict yang disengaja. Masing-masing plot mempunyai 68 observasi, empat gap, satu nilai null dan satu outlier 99°C yang rejected. Dua gap/unusable tidak diganti nol; ada rapid-change dan delivery yang sengaja diurutkan terlambat. Semua angka merupakan formula diurnal + noise hash deterministik, bukan sampel lapangan. Historical fixture secara wajar diberi flag delayed/stale saat dikirim sekarang.

ID sintetis:

| Plot | Plot UUID | Sensor UUID |
|---|---|---|
| A | `00000000-0000-4000-8000-000000000001` | `00000000-0000-4000-8000-000000000101` |
| B | `00000000-0000-4000-8000-000000000002` | `00000000-0000-4000-8000-000000000102` |

`send` menggunakan kredensial dari file lokal, mempertahankan isi paket pada retry dan berhenti pada error yang tidak diharapkan. Replay yang benar tidak membuat baris baru. Dua conflict fixture memang harus menghasilkan `409`. Rate limit default 120 request/menit per credential; replay besar dalam menit yang sama dapat menunggu `Retry-After` secara sengaja. Verifikasi membandingkan fixture terhadap seluruh halaman history; tambahan paket manual dalam rentang yang sama akan dianggap mismatch agar pemeriksaan tidak memberikan hasil lulus palsu.

Untuk membuat rentang dummy lain, gunakan output terpisah dan start UTC penuh; boot/sequence serta nilai didasarkan epoch hour agar overlap rentang tetap idempotent:

```sh
uv run --frozen python scripts/simulate_temperature.py generate \
  --start 2026-10-22T00:00:00Z --hours 24 --out data/dummy-new.json
uv run --frozen python scripts/simulate_temperature.py send --input data/dummy-new.json
```

Buat direktori `data/` terlebih dahulu. Menghasilkan timestamp yang masih di depan waktu saat ini akan memicu clock QC; ini bukan demo untuk data yang sudah tersedia.

## Monitoring dan penanganan insiden

Reader memanggil `GET /v1/status` untuk melihat stale/age per plot. Edge mencatat `request_id`, HTTP status dan code; tabel `request_event` mencatat request actor yang terautentikasi. Gunakan request ID saat menghubungkan laporan perangkat ke log. Tidak ada dashboard, alert scheduler, SLA, atau automatic purge log pada A1.

- `401/403`: verifikasi expiry/revocation, sensor active, role device/reader dan reader_plot mapping.
- `409`: investigasi boot/sequence yang dipakai ulang; observasi lama tetap immutable.
- `503 temporarily_unavailable`: cek Edge logs, secret DB/CA, koneksi pooler dan kesehatan Supabase; sender retry terbatas.
- `503 commissioning_disabled`: real sensor belum diaktifkan oleh operator.
- `201` dengan `quality_status: rejected`: audit waktu atau nilai; transport sukses dan tidak perlu retry terus.
- Data stale: periksa `observed_at` dan antrian perangkat. `ingested_at` yang baru tidak membuat pengukuran lama menjadi baru.

Tindakan rollback ringan: revoke credential bermasalah atau nonaktifkan sensor terkait. Jangan drop schema/menghapus observasi untuk membatalkan deployment. Gateway password dapat dirotasi oleh operator bersama perubahan Edge secret; jangan membagikan credential admin. Riwayat data dan migrasi dipertahankan.

Provenance snapshot: [[Provenance A1 - Paket Handover 22 Oktober 2026]].
