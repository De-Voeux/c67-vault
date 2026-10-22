---
type: engineering-handover
project: "[[Challenge Final]]"
created: 2026-10-22
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, a3]
source_repo: /Users/cindyram/Documents/Apple/Seagis-Model
source_path: docs/a3/operations.md
source_commit: e93a005c95d746e6e33a6adad12760e94eb8a6cf
---

# A3 — Operasi snapshot dan quality report

Semua command berikut dijalankan dari `/Users/cindyram/Documents/Apple/Seagis-Model`. Tidak ada token atau password yang perlu dikirim ke chat. Dokumen ini merujuk [[Handover A3 - Kualitas dan Alignment Data|arsitektur A3]], [[Review A3 - Hasil dan Batas Validasi|hasil aktual]], dan [[quality_report_20261022.json|laporan operasi]].

## Tanpa akses cloud

```sh
uv sync --frozen --group dev
uv run --frozen python scripts/curate_environment.py \
  --offline fixtures/a3/synthetic_bundle.json --demo \
  --out data/a3/offline_report.json \
  --document-out data/a3/offline_alignment.json
```

Fixture A3 diekspor dari PostgreSQL lokal disposable yang diisi fixture kontrak A0. Seluruh 12 record adalah sintetis. Fixture menunjukkan mean harian dengan nol/missing, forecast yang belum valid, receipt terlambat dan grid sintetis; ia tidak berisi provider science payload atau pengukuran lapangan. Mode offline tidak dapat melakukan persist cloud. File di `data/` diabaikan Git.

## Deployment Seagis

```sh
uv run --frozen python scripts/deploy_a3.py
uv run --frozen python scripts/deploy_a3.py --apply
```

Preflight memverifikasi org `pawuvcovwmmimqrcudpd` dan project `kibztbeviortyvbedogg`. Apply mempertahankan source migrasi 0001–0004, menambah 0005, mendaftarkan policy/kode, dan membuat restricted login. Migrasi yang sudah applied tidak diubah. Registrasi versi yang sama dengan policy/kode berbeda ditolak; buat versi baru untuk revisi implementasi.

Runtime memakai `.env.a3.worker` owner-only mode 0600 yang diabaikan Git. Secret itu untuk backend/operator, terpisah dari A1 gateway, A2 ingestion dan token perangkat. Koneksi memakai transaction pooler IPv4 dengan `sslmode=verify-full`, CA Supabase yang hash-nya diperiksa pada `data/a2/supabase-ca.crt`, serta timeout koneksi 20 detik dan statement 60 detik. PAT administrator hanya digunakan saat deployment/registrasi, bukan curation.

## Membaca atau menyimpan snapshot

Rentang harus berupa jam UTC utuh, `[from,to)`, maksimal tujuh hari. Jam terakhir harus sudah berlalu; `to` boleh akhir slot jam berjalan karena tidak ada baris pada nilai `to` itu sendiri. Gunakan rentang yang tercatat dalam laporan aktual bila ingin membandingkan hasil.

```sh
uv run --frozen python scripts/curate_environment.py \
  --plot-id 00000000-0000-4000-8000-000000000001 \
  --from 2026-10-21T07:00:00Z --to 2026-10-22T07:00:00Z \
  --demo --out data/a3/plot-a-report.json

uv run --frozen python scripts/curate_environment.py \
  --plot-id 00000000-0000-4000-8000-000000000001 \
  --from 2026-10-21T07:00:00Z --to 2026-10-22T07:00:00Z \
  --demo --persist --out data/a3/plot-a-report.json
```

Ganti UUID akhir `001` menjadi `002` untuk Plot B. Tanpa `--persist`, command hanya membaca sumber dan menghasilkan report. `--document-out data/a3/plot-a-alignment.json` mengekspor dokumen lengkap. Kedua plot masih sintetis dan memerlukan `--demo`. Plot/sensor nyata kelak memerlukan provisioning A1 dan mapping operasional efektif yang tercatat; commissioning lokasi/depth/sensor tetap prasyarat.

## Melihat tabel di dashboard Supabase

Project: [seagis-model-database](https://supabase.com/dashboard/project/kibztbeviortyvbedogg/editor). Schema default `public` bisa kosong. Pilih `seagis_quality` untuk hasil A3, `seagis` untuk nilai A1/A2, atau gunakan SQL Editor dengan akun operator:

```sql
select id, plot_id, mode, start_at, end_at, policy_version, created_at
from seagis_quality.alignment_snapshot
where policy_version = 'pilot-quality-2'
order by created_at desc;

select id, body->'quality_report' as quality_report
from seagis_quality.alignment_snapshot
where policy_version = 'pilot-quality-2'
order by created_at desc;

select table_schema, table_name
from information_schema.tables
where table_schema in ('seagis', 'seagis_quality', 'seagis_environment', 'seagis_raw')
order by table_schema, table_name;
```

Snapshot selalu menyimpan source/body/manifest hash. `snapshot_input` menghubungkan hasil per jam ke observation/forecast value asli. Snapshot atau normalized row tidak diperbaiki lewat UPDATE/DELETE; ambil snapshot baru dengan sumber/kebijakan yang benar.

## Membaca report dan kegagalan

Coverage adalah proporsi **konteks per jam** yang lolos QA, bukan akurasi model, bukan persentase penyakit, dan bukan jumlah pengamatan independen. Bandingkan `unique_selected_source_records`, cadence native, `value_status_counts`, `flag_counts`, serta `input_qc_flag_counts_at_final_cutoff`. Inventory input mencakup lookback dan cutoff terakhir; flag tiap baris hanya memakai input yang tersedia pada cutoff baris itu sendiri.

- `not_available`/`no_mapping_available_at_cutoff`: sumber atau mapping belum tersedia pada waktu historis tersebut. Data yang masuk kemudian tidak di-backdate.
- `missing_hour`, `stale_sensor`, `stale_vintage`, `native_step_expired`: umur input melewati kebijakan; nilai audit bisa terlihat tetapi `usable_context=false`.
- `below_detection_limit`: nilai null dan limit tersimpan; berbeda dari modeled/measured zero.
- `source_changed_rebuild_snapshot`: baca bundle dan bangun ulang; jangan mengganti source hash secara manual.
- `unregistered_quality_policy_or_code`: periksa versi dan deploy registrasi kode yang sesuai. Jangan mengubah row policy lama.
- `non_deterministic_alignment_output`: key sumber/versi sama menghasilkan dokumen berbeda; hentikan persist dan periksa perubahan builder.
- Kegagalan login: periksa file credential lokal dan role/project yang benar. CLI menekan detail exception agar DSN tidak muncul di output.

Setiap fase baru sebaiknya memakai snapshot tersimpan dan sumber append-only yang sama untuk reproduksi. Membaca kembali sumber operasional yang berubah status/metadata bisa menghasilkan source hash baru; snapshot lama tetap tersedia.

## Runtime dan pemeriksaan

A3 dijalankan on demand dengan Python. Command ini belum memiliki job cloud otomatis. A2 masih mengambil data lewat scheduler Mac yang didokumentasikan pada [[Operasi A2 - Adapter dan Scheduler|operasi A2]]; source dan hasil A3 disimpan di Supabase. Penjadwalan cloud memerlukan pengaturan orchestration serta worker Python yang sesuai.

```sh
uv run --frozen ruff check scripts tests
uv run --frozen python scripts/validate_contracts.py
deno task --config supabase/functions/temperature/deno.json check
uv run --frozen python scripts/check_a1.py
git diff --check
```

Runner hanya menerima database lokal disposable dan menerapkan seluruh migrasi dari kosong, kemudian menjalankan tests A0/A1/A3 serta HTTP Deno asli. CI mencakup suite dan command fixture offline; tidak ada push atau klaim CI GitHub sudah berjalan pada sesi ini.

## Remediasi credential 22 Oktober

Dua password backend yang sempat tampil pada output pemeriksaan sebelumnya telah dirotasi melalui `scripts/rotate_worker_credentials.py --apply`. File lokal A1/A2 dan secret A1 Edge diperbarui; login baru berhasil dan kedua login lama ditolak. Read-only status HTTP IoT diverifikasi sesudahnya. Token perangkat/reader tidak tampil dalam output tersebut dan tidak diganti. Script menyimpan recovery owner-only selama operasi; recovery dihapus setelah seluruh pemeriksaan berhasil. Jangan menyalin credential file atau recovery ke Git/vault.


Navigasi: [[Indeks - Engineering]] · [[Provenance A3 - Paket Engineering 22 Oktober 2026]].
