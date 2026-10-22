---
type: engineering-handover
project: "[[Challenge Final]]"
created: 2026-10-22
updated: 2026-10-22
status: implemented-provider-partial
tags: [challenge-final, seagis, engineering, a2]
source_commit: 24742513987227968228c54c1898d4c6d6dc54b2
---

# A2 — Hasil ingestion regional

## Status 22 Oktober 2026

**Pipeline A2 terpasang; tiga dari empat sumber menghasilkan data live. Salinitas masih menunggu provider menyelesaikan pembaruan.** Snapshot operasional di [ingestion_report_20261022.json](/Users/cindyram/Documents/Second Brain/02-Projects/Challenge Final/Engineering/Seagis/A2/ingestion_report_20261022.json), project Supabase Seagis `kibztbeviortyvbedogg`.

| Sumber | Hasil tersimpan | Sel / mapping demo | Valid time UTC |
|---|---:|---:|---|
| Copernicus arus 6 jam | 26 nilai (`uo`,`vo` × 13 timestamp) | 1 / 2 | 22 Okt 00:00–25 Okt 00:00 |
| Copernicus nutrien harian | 8 nilai (`no3`,`po4` × 4 timestamp) | 1 / 2 | 22 Okt 00:00–25 Okt 00:00 |
| Open-Meteo explicit GFS | 432 nilai (6 variabel × 72 jam) | 1 / 2 | 22 Okt 00:00–24 Okt 23:00 |
| Copernicus salinitas | 0 | 0 / 0 | current window ditolak safeguard provider |

Total **466 nilai model regional asli** pada tiga vintage, tiga grid, enam mapping demo. Tidak ada missing value pada tiga subset yang berhasil, tetapi itu bukan validasi akurasi provider atau lokasi farm. Keluaran arus memiliki 13 speed turunan dengan lineage ke dua komponen. Cadence nutrien tetap harian.

Copernicus `nearest` berlaku juga pada batas waktu: request dari 22 Okt 00:00 hingga 24 Okt 23:59:59 mengembalikan boundary terdekat 25 Okt 00:00. Karena itu subset berisi 13 instant arus / empat label daily, bukan klaim 72 observasi nutrien. Tidak ada timestamp atau nilai yang dibuat melalui interpolasi oleh pipeline.

Sel aktual:

- PHY currents: `(-5.83332824707031, 106.5)`, depth sekitar 0.494024992 m; jarak contoh A/B sekitar 4.46 / 3.98 km.
- BGC nutrients: `(-5.75, 106.5)`, depth sekitar 0.494025379 m; jarak 5.18 / 5.38 km.
- Open-Meteo returned coordinate: `(-5.798889, 106.52344)`; jarak 3.94 / 3.26 km. Height variabel cuaca berada dalam identitas parameter, bukan depth sensor air.

Preview A dan B masing-masing mengembalikan 308 nilai untuk 48 jam berikut pada waktu snapshot. Kedua preview menunjuk tiga UUID grid yang sama; tidak ada salinan nilai per plot. Sel dan nilai asli tetap non-synthetic, sedangkan plot/mapping tetap ditandai demo dan tidak boleh menjadi input training.

## Bukti operasi dan keamanan

- Migrasi `0001`–`0004` terpasang dengan ledger cocok ke source. Migrasi A0/A1 tidak diubah; A2 menambah schema privat dan memperjelas `analysis_forecast_unspecified` serta basis hash subset Toolbox.
- Repeat fetch arus menghasilkan status **duplicate**, run ID sama dan **0 inserted values**. Waktu availability vintage pertama dipertahankan.
- Seluruh `issued_at` / `model_initialized_at` masih null dengan `issue_time_basis=unknown`; setiap nilai menunjuk run dan `ingested_at` server yang terukur. Tidak ada tanggal katalog atau durasi generasi yang disulap menjadi issue time.
- Role worker punya **0 table grants** pada schema privat, bukan superuser, tidak bisa membuat DB/role atau bypass RLS. Credential file 0600; TLS verify-full dengan CA yang dipin. Runtime tidak membaca PAT admin.
- Empat dataset lingkungan di-enable untuk ingestion nyata. Sensor suhu nyata tetap disabled; tabel observasi A1 tetap **136 synthetic / 0 real**.
- Semua manifest A2 metadata_only; tidak ada raw object, payload penuh, token atau password pada laporan/vault.
- LaunchAgent `org.seagis.environment-ingestion` terpasang dan tick pertama selesai **exit 0**, melewati empat sumber yang saat itu belum due. Ini scheduler Mac lokal, bukan layanan cloud 24/7.
- Lint pada kode A2 lulus. **Tidak ada suite tests baru/ulang pada sesi A2**, termasuk regression A0/A1, failure injection, atau evaluasi model. Fetch/persist di atas adalah operasi ingestion sebenarnya, bukan hasil test sintetis.

## Kegagalan yang ditemukan dan ditangani

1. Open-Meteo menolak request dua koordinat dengan satu `elevation=nan` (HTTP 400); adapter diperbaiki agar jumlah elevation cocok jumlah koordinat. Respons kedua plot menunjuk sel/seri sama dan disimpan sekali.
2. STAC BGC tidak menyertakan property `product`; adapter memverifikasi `collection` dan versioned ID, serta memeriksa `product` jika tersedia. Fetch kemudian berhasil.
3. Satu proses salinitas terinterupsi saat turn berlanjut, meninggalkan lease tanpa proses aktif. Setelah inventory proses dikonfirmasi, operator mempercepat expiry lease tersebut; attempt tetap tercatat abandoned. Tidak ada data yang dihapus.
4. Dataset salinitas versi 202406 menyertakan `admp_updating_start_date=2026-10-07T06:00:00Z`. Requested window berada di rentang yang diperbarui; `raise_if_updating=True` menghentikannya. Error awal generik diperjelas menjadi `provider_updating`, disimpan dalam monitoring dengan backoff otomatis. Safeguard tidak dinonaktifkan, tidak diganti dataset diam-diam, dan tidak diisi dummy atau nol.

Sumber safeguard dan snapshot metadata ada di [source_evidence_20261022.json](/Users/cindyram/Documents/Second Brain/02-Projects/Challenge Final/Engineering/Seagis/A2/source_evidence_20261022.json). Ketersediaan salinitas terbaru adalah **ketergantungan eksternal yang belum selesai**. Scheduler akan mencoba lagi setelah backoff saat Mac aktif. Tidak perlu mengganti token Supabase/Copernicus untuk kondisi ini.

## Handover dan batas

A2 menyediakan adapter, private persistence, provenance, preview, jadwal, retry/backoff, batas stale, monitoring, dan kebijakan lisensi/retention. Sample end-to-end satu grid bersama dan dua plot demo berhasil pada tiga sumber. Data sensor lapangan, koordinat survei, salinitas terkini yang stabil, exact provider issuance, serta regresi menyeluruh belum tersedia/selesai.

A3 dapat memakai normalized snapshots beserta availability konservatif untuk pekerjaan quality/alignment berikutnya, dengan salinitas tetap unavailable hingga provider pulih. Jangan menganggap zero missing pada sampel berarti semua sumber lengkap atau hasil siap training; seluruh nilai masih `quality_status=unreviewed`. A4–A6, aplikasi publik, training/Core ML, dan commissioning hardware belum dijalankan.

Mulai membaca: [architecture.md](</Users/cindyram/Documents/Second Brain/02-Projects/Challenge Final/Engineering/Seagis/A2/Handover A2 - Ingestion Lingkungan dan Grid.md>), [operations.md](</Users/cindyram/Documents/Second Brain/02-Projects/Challenge Final/Engineering/Seagis/A2/Operasi A2 - Adapter dan Scheduler.md>), [licenses.md](</Users/cindyram/Documents/Second Brain/02-Projects/Challenge Final/Engineering/Seagis/A2/Lisensi A2 - Atribusi dan Retention.md>).


## Provenance salinan

Sumber: [review.md](/Users/cindyram/Documents/Apple/Seagis-Model/docs/a2/review.md), commit `2474251`. Salinan catatan lengkap dengan tautan lokal yang disesuaikan. [[Provenance A2 - Paket Engineering 22 Oktober 2026]] · [[Indeks - Engineering]].
