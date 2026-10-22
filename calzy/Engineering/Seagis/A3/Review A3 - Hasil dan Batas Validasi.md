---
type: engineering-handover
project: "[[Challenge Final]]"
created: 2026-10-22
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, a3]
source_repo: /Users/cindyram/Documents/Apple/Seagis-Model
source_path: docs/a3/review.md
source_commit: e93a005c95d746e6e33a6adad12760e94eb8a6cf
---

# A3 — Hasil dan batas validasi

Status: **implementasi QC/alignment A3 selesai, diperiksa lokal dan diterapkan di Supabase Seagis**. Inspeksi terakhir 22 Oktober 2026, 06:22 UTC / 13:22 WIB. Bukti terstruktur ada di [[quality_report_20261022.json|quality_report_20261022.json]]. Snapshot adalah review engineering dengan `training_authorized=false`.

## Deliverable

| Hasil | Lokasi |
|---|---|
| Kebijakan QA pilot, unit/conversion/domain/null/duplicate/stale dan flatline candidate | `config/a3_quality.json`, `scripts/quality/alignment.py` |
| Hourly as-of join, cadence native, pemilihan vintage dan metadata spasial | `scripts/quality/alignment.py` |
| Kontrak keluaran berversi | `contracts/alignment.schema.json` |
| Private source bundle, validasi lineage server, snapshot dan FK input append-only | `supabase/migrations/0005_quality_alignment.sql` |
| Restricted login, registrasi kebijakan/kode dan CLI on demand | `scripts/deploy_a3.py`, `scripts/quality/store.py`, `scripts/curate_environment.py` |
| Fixture sintetis yang dapat dipakai tanpa cloud | `fixtures/a3/synthetic_bundle.json` |
| Tests, workflow CI, handover dan report | `tests/test_a3.py`, `.github/workflows/a0.yml`, folder `docs/a3/` |

## Pemeriksaan lokal

**94 Python tests lulus**, mencakup 63 tests A0/A1 dan 31 tests A3, serta **7 Deno tests lulus**. Integrasi HTTP Deno asli dengan restricted DB role juga lulus: 136 insert, dua replay duplicate, dua packet conflict, replay seluruh paket, dan delapan concurrent retries. Lint, lima pasang kontrak A0, kontrak snapshot A3, offline CLI dan `git diff --check` lulus. Runner memulai PostgreSQL 17 disposable dari kosong, menerapkan migrasi 0001–0005, dan tidak memakai cloud database untuk unit/integration tests.

Kasus A3 mencakup NaN/null, unit dan konversi salah, nol lokal/model, below detection limit, duplikat sama/konflik, gap/stale/delayed/out-of-order, rapid change, baseline QC yang buruk, flatline dengan bukti minimum, sum presipitasi, mean harian, umur native step/vintage, mapping yang belum tercatat, forecast yang belum terbit/tersedia, serta pemisahan plot. Database menolak dokumen yang memalsukan nilai, lineage masa depan, parameter, metadata spasial/temporal dan versi kode. Idempotence, immutability dan RLS setelah accidental SELECT grant diperiksa.

Perintah pemeriksaan tersedia pada [[Operasi A3 - Snapshot dan Quality Report|operasi A3]]. CI GitHub diperbarui; belum dijalankan di GitHub pada sesi ini karena tidak ada push.

## Hasil cloud aktual

Target: org Seagis `pawuvcovwmmimqrcudpd`, project `kibztbeviortyvbedogg`. Source migrasi 0001–0005 cocok dengan ledger cloud. Worker A3 mempunyai nol table grants; TLS login dan tiga fungsi privat bekerja. Kebijakan terbaru `pilot-quality-2` / builder `a3-alignment-1.0.1` menyaring pembanding anomaly agar unit/konversi/envelope salah atau duplikat konflik tidak menciptakan false outlier. Kebijakan pertama tetap tersimpan untuk audit.

| Item | Snapshot inspeksi terakhir |
|---|---|
| Window konteks terbaru | 21 Okt 07:00 sampai 22 Okt 07:00 UTC, akhir eksklusif; 24 baris per plot |
| Plot A, policy 2 | `9e47755b-87c1-42cb-ad1f-d2b27ac70293` |
| Plot B, policy 2 | `a8af375a-f39b-43b0-9fef-4a9159242b11` |
| Hasil per plot | 20 konteks regional lolos QA teknis, pada 05:00 dan 06:00 UTC; 23 relasi input per snapshot |
| Observasi IoT cloud | 136 sintetis / 0 sensor nyata; konteks sensor yang terlihat tetap stale/suspect |
| Regional cloud | 479 normalized values, empat vintages; termasuk 13 nilai salinitas yang baru masuk |
| Arsip A3 keseluruhan | Empat snapshot: dua policy 1 historis dan dua policy 2 terbaru; 48 relasi input |
| Replay/readback | ID tetap sama saat persist ulang; isi readback sama dengan dokumen yang dibangun |

Pada pemeriksaan sebelum pause, dua snapshot awal memakai window sampai 22 Okt 05:00 UTC, dengan cutoff terakhir 04:00 UTC. Coverage saat itu nol: normalized data dan mapping regional baru tersedia setelah 04:00 UTC. Snapshot awal tetap dipertahankan, dan ringkasannya ada dalam `earlier_inspection` pada laporan.

Pemeriksaan setelah resume memiliki cutoff terakhir 06:00 UTC. Arus, nutrien dan cuaca sudah diketahui pada dua cutoff terakhir, sehingga masing-masing parameter itu memiliki 2/24 konteks tersedia. Nitrate/phosphate masing-masing tetap merujuk satu record harian yang dipakai ulang, dengan cadence dan umur eksplisit. Ini tidak menambah jumlah observasi independen.

Salinitas berhasil di-ingest pada 06:09 UTC / 13:09 WIB, sehingga status provider terakhir tidak lagi error. Namun cutoff 06:00 UTC pada snapshot terbaru mendahului receipt dan mapping salinitas tersebut: parameter itu masih tidak tersedia pada semua baris snapshot. Pengulangan dengan cutoff berikutnya yang benar-benar sudah berlalu dapat memasukkannya. Tidak ada backdating untuk memperbaiki coverage historis.

## Acceptance criteria A3

| Kriteria roadmap | Status dan bukti |
|---|---|
| QC missing/duplicate/stale/out-of-order/outlier/unit mismatch | Lulus tests A3 dan report per input/konteks |
| Forecast future-issued tidak masuk baris sebelumnya | Lulus unit dan actual PostgreSQL vintage-as-of test; server menolak lineage cutoff yang dilanggar |
| Quality report per source/parameter/plot/time range | Tersimpan untuk A/B, menyebut coverage konteks, cadence, input unik, status nilai dan flag |
| Alignment deterministic tanpa observasi harian fiktif | Lulus permutation/replay checks; daily context tetap menunjuk input sama |
| Jarak/depth/representativeness eksplisit | Metadata serta warning tersedia; lokasi plot, depth sensor dan ukuran plot belum terverifikasi |
| Drift checks ketika bukti memungkinkan | Flatline candidate tersedia; drift kalibrasi berstatus belum dapat dinilai tanpa referensi terkalibrasi co-located |

## Batas dan handover

Semua plot tetap dummy. Nilai regional asli tetap berbeda dari observasi sensor lokal sintetis. Coverage yang rendah mencerminkan waktu receipt, mapping, cadence dan umur input; tidak mengukur akurasi provider. Envelope QA pilot belum menjadi ambang biologis, validasi kondisi farm, atau prediksi penyakit.

Mapping belum disurvei, ukuran plot tidak tersedia, resolusi GFS belum dikunci, interval mean harian belum diketahui secara penuh, dan issue/init time provider masih tidak terverifikasi untuk data A2 saat ini. Flag tersebut tetap dibawa ke hasil. Hardware dan referensi kalibrasi belum tersedia. A4 dapat melanjutkan definisi fitur dengan batas ini dan lineage tersimpan; kemampuan training memerlukan data yang cukup serta validasi tersendiri.

A3 memakai command Python on demand dengan hasil di Supabase. Scheduler A2 yang sudah ada masih berjalan di Mac; migrasi orchestration cloud belum dikerjakan pada A3. Dua credential backend yang sempat terekspos telah dirotasi, login lama ditolak, serta endpoint status IoT setelah perubahan kembali memberi HTTP 200 untuk dua plot. Detail operasional tersedia pada [[Operasi A3 - Snapshot dan Quality Report|operations.md]].


Navigasi: [[Indeks - Engineering]] · [[Provenance A3 - Paket Engineering 22 Oktober 2026]].
