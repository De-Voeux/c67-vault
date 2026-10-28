# AUDIT_KUALITAS_DATA

Version: 1.0.0 | Date: 2026-10-27

[Dokumen lengkap](../DOKUMENTASI_DATABASE.md) | [README](../../README.md)

Audit read-only terhadap kode dan snapshot lama; severity menyatakan dampak potensial sesuai lingkup prototype, bukan insiden produksi terukur. Tidak ada perubahan schema/aplikasi yang diterapkan.

### F01 Assessment iOS belum terhubung ke backend

| Atribut | Temuan |
| --- | --- |
| Severity / category | High / Contract / integration |
| Status | VERIFIED |
| Deskripsi / dampak | Mock mengembalikan synthetic_fixture; tidak ada adapter API assessment yang ditemukan. Konsumen baru tidak boleh menganggap model domain sebagai wire contract. |
| Affected | Seagis/Seagis/Repositories/Shared/MockAssessmentRepository.swift, Seagis/Seagis/Models/Shared/Assessment.swift |
| Evidence | `Seagis/Seagis/Repositories/Shared/MockAssessmentRepository.swift:1`; `Seagis/Seagis/Models/Shared/Assessment.swift:1` |
| Rekomendasi | Sepakati kontrak executable dan mapping provenance/error sebelum integrasi. |

### F02 Mapping immutable setelah 0005 mengubah prosedur penutupan lama

| Atribut | Temuan |
| --- | --- |
| Severity / category | Medium / Lifecycle |
| Status | VERIFIED |
| Deskripsi / dampak | guard_mapping A0 mengizinkan penutupan interval; trigger 0005 menolak seluruh UPDATE/DELETE. Petunjuk arsitektur A0 untuk menutup mapping dapat gagal pada schema lengkap. |
| Affected | supabase/migrations/0001_initial_schema.sql, supabase/migrations/0005_quality_alignment.sql, docs/architecture.md |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:1`; `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:1`; `Seagis-Model/docs/architecture.md:1` |
| Rekomendasi | Definisikan prosedur append-only untuk supersession dan uji overlap/cutoff. |

### F03 Riwayat tumbuh tanpa job retensi yang ditemukan

| Atribut | Temuan |
| --- | --- |
| Severity / category | Medium / Governance / retention |
| Status | INFERRED |
| Deskripsi / dampak | request_event, observation, forecast dan snapshot append-only; TTL/cleanup terjadwal dan recovery test tidak ditemukan di checkout. Risiko kapasitas adalah inferensi, bukan hasil benchmark. |
| Affected | supabase/migrations/0001_initial_schema.sql, supabase/migrations/0002_temperature_api.sql, supabase/migrations/0005_quality_alignment.sql |
| Evidence | `Seagis-Model/supabase/migrations/0001_initial_schema.sql:1`; `Seagis-Model/supabase/migrations/0002_temperature_api.sql:1`; `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:1` |
| Rekomendasi | Tetapkan retention per domain, archival, backup dan restore drill sebelum skala produksi. |

### F04 SQL A3 memeriksa lineage tetapi tidak menghitung ulang seluruh QC

| Atribut | Temuan |
| --- | --- |
| Severity / category | Medium / Validation boundary |
| Status | VERIFIED |
| Deskripsi / dampak | save_snapshot memeriksa hash policy/kode dan nilai sumber, tetapi keputusan usable_context/flags/blocking_flags tidak direkalkulasi melalui Python di DB. Role worker tetap trust boundary. |
| Affected | supabase/migrations/0005_quality_alignment.sql, scripts/quality/alignment.py |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:1`; `Seagis-Model/scripts/quality/alignment.py:1` |
| Rekomendasi | Dokumentasikan trust worker; bila diperlukan, verifikasi deterministik QC tambahan dan test payload tampering. |

### F05 Metadata-only membatasi reproduksi raw

| Atribut | Temuan |
| --- | --- |
| Severity / category | Medium / Data provenance |
| Status | VERIFIED |
| Deskripsi / dampak | A2 tidak menyimpan raw content. Hash subset Toolbox bukan hash byte NetCDF/Zarr asli; memperoleh ulang aggregate provider tidak menjamin vintage yang sama. |
| Affected | scripts/environmental/copernicus.py, supabase/migrations/0003_environment_ingestion.sql |
| Evidence | `Seagis-Model/scripts/environmental/copernicus.py:1`; `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:1` |
| Rekomendasi | Pertahankan hash_basis; bila lisensi dan biaya disetujui, usulkan penyimpanan subset/objek versi immutable. |

### F06 CSV capture bukan backtest historis

| Atribut | Temuan |
| --- | --- |
| Severity / category | High / Analytics semantics |
| Status | VERIFIED |
| Deskripsi / dampak | Exporter memilih latest_available_at_capture; A3 memakai cutoff tiap jam. Memakai CSV tersebut sebagai histori availability berisiko leakage; training_authorized=false sudah dinyatakan kode. |
| Affected | scripts/export_experiment_csv.py, scripts/quality/alignment.py |
| Evidence | `Seagis-Model/scripts/export_experiment_csv.py:1`; `Seagis-Model/scripts/quality/alignment.py:1` |
| Rekomendasi | Gunakan source bundles seluruh vintage dan cutoff eksplisit untuk rancangan backtest; jangan melepas gate training tanpa validasi. |

### F07 Dokumen A0 mendahului implementasi A1–A3

| Atribut | Temuan |
| --- | --- |
| Severity / category | Low / Documentation drift |
| Status | VERIFIED |
| Deskripsi / dampak | docs/architecture.md mengatakan ingestion/scheduler/QC belum diimplementasikan, sedangkan migrasi dan worker berikutnya ada. Pernyataan harus dibaca dengan fase dan tanggal. |
| Affected | docs/architecture.md, scripts/ingest_environment.py, scripts/curate_environment.py |
| Evidence | `Seagis-Model/docs/architecture.md:1`; `Seagis-Model/scripts/ingest_environment.py:1`; `Seagis-Model/scripts/curate_environment.py:1` |
| Rekomendasi | Gunakan indeks status fase serta source-manifest untuk pembaruan dokumentasi. |

### F08 Snapshot catalog berumur lima hari

| Atribut | Temuan |
| --- | --- |
| Severity / category | Medium / Runtime verification |
| Status | UNVERIFIED |
| Deskripsi / dampak | Snapshot 22 Oktober bukan audit runtime 27 Oktober. Grants, row count, cron aktif dan migrasi cloud terkini tidak diverifikasi ulang. |
| Affected | runtime catalog |
| Evidence | schema-metadata-20261022.json inspected_at |
| Rekomendasi | Lakukan diff catalog read-only dan review grants sebelum keputusan produksi. |

Prioritas: P1 sepakati integrasi/kontrak dan cegah leakage (F01/F06); P2 tutup trust, retensi, mapping lifecycle dan raw reproducibility (F02–F05); P3 perbarui status dokumentasi dan catalog (F07/F08). Evaluasi indeks/performa membutuhkan EXPLAIN dan beban nyata: tidak ada klaim missing index atau query lambat yang dibuktikan hanya dari nama kolom.

