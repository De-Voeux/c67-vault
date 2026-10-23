# Review dan handoff A0

Status: **deliverable A0 selesai dan tervalidasi lokal; siap review sebelum A1**. Tanggal pemeriksaan: 21 Oktober 2026. Lokasi kerja: `Documents/Apple/Seagis-Model`.

## Deliverable

| Hasil | Lokasi |
| --- | --- |
| Arsitektur dan diagram, lifecycle raw → normalized → features, waktu, akses, idempotensi | [architecture.md](architecture.md) |
| Provider, dataset/version, variabel/unit, kedalaman, cadence, auth, lisensi, dan batas sumber | [source_registry.md](source_registry.md) dan [snapshot metadata](metadata/source_catalogue_20261021.json) |
| Entitas, field, constraint, satuan, status, dan hash | [data_dictionary.md](data_dictionary.md) |
| Kontrak bertipe dan contoh payload | [data_contracts.md](data_contracts.md), [source schema](../contracts/source.schema.json), [normalized schema](../contracts/normalized.schema.json), lima pasangan fixture |
| Schema private dengan RLS dan seed dua plot | [0001_initial_schema.sql](../supabase/migrations/0001_initial_schema.sql), [seed.sql](../supabase/seed.sql) |
| Keputusan penyimpanan dan tradeoff | [ADR-001](decisions/ADR-001-data-storage.md) |
| Validasi repeatable dan CI | `scripts/`, `tests/`, `pyproject.toml`, `uv.lock`, `.github/workflows/a0.yml` |

Tidak ada file lama yang ditimpa atau sumber asli yang diubah. Konfigurasi Supabase hasil setup dipertahankan. Semua artefak baru ada pada repo model ini; vault riset dan kode iOS tidak diubah.

## Pemeriksaan yang sudah dijalankan

```sh
uv sync --frozen --group dev
uv run --frozen ruff check scripts tests
uv run --frozen python scripts/validate_contracts.py
uv run --frozen python scripts/check_a0.py
git diff --check
```

Hasil: lint lulus; **5 pasangan source/normalized** lulus; **44 tests** lulus di PostgreSQL **17.11** lokal. Runner memulai cluster kosong terisolasi, membuat role Supabase minimal untuk test, menerapkan migrasi 0001 dalam transaksi, dan menjalankan seed dua kali. Tidak ada server test yang dibiarkan berjalan setelah runner selesai.

Cakupan pengujian:

- Unit registry SQL sama dengan kontrak; nilai, hash, grid/kedalaman, UTC, array provider, dan metadata request tetap konsisten.
- Sensor–plot tidak dapat tertukar; duplikat paket dan forecast ditolak; riwayat lokal dua plot tetap berbeda saat paket terlambat.
- Satu grid regional dapat dipakai dua plot tanpa menggandakan nilai; run berbeda mempertahankan forecast terpisah.
- Missing/null, modeled zero, dan cadence nutrien harian tetap berbeda. Presipitasi harus memiliki interval satu jam yang benar.
- Raw/measurement/run/grid/parameter append-only, real ingestion nonaktif, dan backend tidak mendapat hak TRUNCATE untuk melewati trigger.
- `anon`/`authenticated` tidak memperoleh akses schema. RLS juga menolak pembacaan bila grant SELECT diberikan sementara dalam test. Backend tepercaya dapat membaca.
- Input fitur sesudah cutoff, dari plot lain, atau tanpa mapping efektif ditolak. Future valid time diizinkan untuk forecast yang sudah tersedia. Sealing harus memakai manifest benar dan menutup perubahan input.

Ini tidak mencakup pengujian sensor fisik, full Supabase stack lokal, ingestion provider, akurasi model, atau validasi ice-ice. Workflow GitHub Actions sudah ditulis tetapi belum dijalankan di GitHub karena belum ada push.

## Acceptance criteria A0

| Kriteria Track A | Status | Bukti |
| --- | --- | --- |
| Measurement dapat ditelusuri ke provider, sensor/grid, waktu, unit, ingestion | Lulus lokal | Composite FK, registry field-level, raw manifest, test lineage semua fixture |
| Revisi forecast disimpan per run, tidak ditimpa | Lulus lokal | UNIQUE per run/grid/parameter/valid time, trigger append-only, test run terpisah |
| Pembaca dapat membedakan lokal vs regional | Lulus | Tabel observation vs forecast_value, scope dataset dan grid mapping, dokumentasi origin |
| Schema/payload valid, migrasi berjalan dari kosong, query dasar bekerja | Lulus lokal | JSON Schema + validasi semantic, cluster PostgreSQL kosong, 44 tests |

## Status cloud dan batas deployment

Target: organisasi **Seagis**, project **seagis-model-database**, ref `kibztbeviortyvbedogg`. Login, link, serta SELECT via HTTPS Management API sudah berhasil pada setup. Sebelum A0, project memiliki 0 tabel public dan 0 migrations.

**Migrasi A0 dan seed belum diterapkan ke cloud.** Pengujian A0 memakai database lokal disposable; kode tidak menjalankan write API cloud. File `0001_initial_schema.sql` tetap dapat ditinjau sebelum deployment bersama. Deployment harus mempertahankan versi riwayat `0001`; API apply-migration yang membuat timestamp otomatis tidak boleh menyebabkan versi lokal dan remote berbeda. Kendala IPv6 pada `supabase db query --linked` di Mac ini belum diselesaikan untuk koneksi PostgreSQL langsung/pooler; akses Management API HTTPS sudah terbukti bekerja.

## Keputusan terbuka sebelum fase berikutnya

| Keputusan | Batas fase |
| --- | --- |
| Format packet hardware, clock-skew policy, autentikasi perangkat, otorisasi plot, dan credential worker yang lebih sempit | Sebelum deployment A1; simulator dapat memakai kontrak A0 |
| Koordinat plot, kedalaman sensor nyata, wet mask, sel regional, dan jarak/representativitas | Sebelum konteks regional ditampilkan sebagai relevan untuk plot pada A2 |
| Verifikasi licence Copernicus penuh dan entitlement noncommercial/commercial Open-Meteo, retensi serta attribution final | Sebelum mengaktifkan fetch/raw storage nyata A2 |
| Provenance issue/init/availability per provider dan native grid tiap variabel GFS | Sebelum arsip forecast dipakai untuk backtest A2/A3 |
| QC rentang, stale/gap, temporal alignment, serta pemilihan vintage as-of yang lengkap | A1/A3; schema A0 bukan implementasi QC operasional |
| Perhitungan fitur, baseline dan evaluasi forecasting, uncertainty, ekspor Core ML | A4/A5, setelah data cukup |

Semua `real_ingestion_enabled` dan `raw_storage_permitted` masih false. Tidak ada biological warning threshold atau probabilitas ice-ice yang dibuat. A1 belum dimulai.

## Riwayat perubahan

Commit memakai Conventional Commits dan dikelompokkan per hasil yang dapat direview: setup, schema, koreksi provenance/privilege, kontrak dan tests, dokumentasi. Commit serta status akhir dapat diperiksa dengan `git log --oneline` dan `git status --short`. File koordinasi `.agent-work/`, credential, cache, dan lingkungan virtual tidak di-commit. Tidak ada push pada pekerjaan A0 ini.
