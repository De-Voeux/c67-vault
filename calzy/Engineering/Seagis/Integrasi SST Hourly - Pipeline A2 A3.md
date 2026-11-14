---
type: engineering-handover
project: "[[Challenge Final]]"
created: 2026-11-10
updated: 2026-11-10
status: deployed-backend-app-integration-pending
tags: [challenge-final, seagis, engineering, sst, ingestion, monitoring]
---

# Integrasi SST hourly — Pipeline A2 A3

**Pembaruan10 November 2026: SST sudah aktif di backend Seagis Singapore, Edge v3 dan worker operasional. API serta entry Monitoring production telah diverifikasi. Integrasi kode iOS masih terpisah.** Pengguna meminta persiapan integrasi mengikuti rule pipeline yang ada, kemudian menambahkan permintaan entry Monitoring. Pekerjaan ini melanjutkan [[Uji SST Hourly - Copernicus ke App]].


## Aktivasi production — 10 November 2026

Persetujuan pengguna “right, do all that” meliputi aktivasi backend. Migration**20261110000100**, policy A3**pilot-quality-spatial-sst-1**, source worker dan Edge**temperature v3** sudah diterapkan pada project**mdtmupiftllpglkfoaqy**. Source operasional cocok dengan20file paket teruji sebelum pembaruan dokumentasi. Perubahan physical-hub dan UI Monitoring sebelumnya dipertahankan; tidak ada push.

- Ingestion pertama**20:50 WIB**: **192 nilai dari 2 cell**,96 slot hourly per cell, window9–12NovemberUTC. Referensi Tidung Besar menggunakan cell sekitar-5.833328,106.583344; PlotA demo memakai cell tetangga.
- Replay production menghasilkan**duplicate,0 nilai baru**, forecast run yang sama; vintage receipt tetap13:50 UTC walau pemeriksaan sukses berikutnya lebih baru.
- Empat snapshot A3 (history 168h dan current 1h untuk dua plot) sukses melalui worker restricted. Execution telemetry tercatat; scheduler Mac loaded, tick 900 detik, sourcepolicy 3600 detik, nominalslot H:05UTC. Mac harus tetap aktif/login; tidak ada host cloud 24/7baru.
- HTTPS reader scoped berhasil200 untuk SST. Saat cutoff**2026-11-10T14:00:00+00:00**, API memberikan **30.620832°C**, persis forecast_value sumber. Cold-start sebelum cutoff berikutnya tetap not_available, lalu angka muncul setelah rollover tanpa memundurkan waktu receipt.
- Respons lama tanpa SST tetap200 dan tidak menambahkan parameter baru; token kosong/salah401, invalidopt-in400, plot di luar scope403. `training_authorized=false`; `usable_context=false` karena spatial/field support belum diverifikasi.
- Referensi terpisah**2237aa43-eccc-4013-8732-9a63e9c07168** (`tidung-sst-ref`), operator_unverified, water context unknown, tanpa sensor. Reader physical yang sudah dibagikan ditambah read scope referensi ini, tanpa mengubah dua lokasi sensor. Fileenvhandoff `/private/tmp/seagis-ios-handoff-f391/seagis-ios.env` diperbarui dengan `SEAGIS_SST_REFERENCE_PLOT_ID`.
- Role login**seagis_monitor_web** terverifikasi membaca SST worker dan volume192 melalui fungsi Monitoring production. Entry aktivasi dicatat di docs/IMPLEMENTATION_PLAN.md dan docs/VERIFICATION.md pada checkout Monitoring asli; tidak deploy ulang frontend atau menimpa dirty UI/map.
- Semua**957 observasi yang ada sebelum deployment tetap identik** menurut fingerprint row set pada cutoff preflight. Tidak mengirim dummy ke identitas physical, tidak merotasi reader/gateway credentials.

Verifikasi final yang sebelumnya tertunda kini selesai: **133 tes PostgreSQL+HTTP lokal**, **actual-provider local full-chain smoke**, serta production ingestion/replay/A3/API/Monitoring. Soak beberapa hari, password login browser Monitoring, dan build/integrasi iOS tidak diklaim.

Deployment Edge awal sempat ditolak automaticreview karena flag `--no-verify-jwt`. Pemeriksaan read-only membuktikan production v2 sudah `verify_jwt=false`, missing/wrongopaque token401 dan reader200. Deployment disetujui setelah bukti ini, dengan assertion bahwa konfigurasi tidak berubah; v3 tetap memakai autentikasi reader opaque di handler. Ini bukan bypass atau pelemahan auth.

Bukti aktivasi: [manifest](../../.agent-work/20261110-sst-activation-a219/drafts/activation-manifest.json), [migrasi](../../.agent-work/20261110-sst-activation-a219/drafts/migration-applied.json), [Edge](../../.agent-work/20261110-sst-activation-a219/drafts/edge-deployed.json), [APIcurrent](../../.agent-work/20261110-sst-activation-a219/drafts/https-present-verified.json), [dedup](../../.agent-work/20261110-sst-activation-a219/drafts/live-replay-verified.json), [Monitoringrestricted](../../.agent-work/20261110-sst-activation-a219/drafts/restricted-monitoring-live.json), [preservasiobservasi](../../.agent-work/20261110-sst-activation-a219/drafts/preservation-check.json), [133 tes+HTTP](../../.agent-work/20261110-sst-activation-a219/drafts/final-133-db-http-tests.log).

Bagian di bawah mempertahankan riwayat paket persiapan, pemeriksaan dan langkah aktivasi pada checkpoint sebelum deployment; status production terbaru ada pada bagian ini.

## Paket implementasi

| Paket | Lokasi dan commit |
| --- | --- |
| Backend | `/private/tmp/seagis-sst-ingestion-8c31`, branch `codex/20261110-sst-ingestion-8c31`, commit `48332e046401568e7a814f6ba7252435da966fc0` |
| Monitoring | `/private/tmp/seagis-sst-monitoring-8c31`, branch `codex/20261110-sst-monitoring-8c31`, commit `09f694accbd3630e6466bf6e2fdb031f9fdd1009` |
| Patch backend permanen lokal | [backend-sst.patch](../../.agent-work/20261110-sst-ingestion-8c31/drafts/backend-sst.patch) |
| Patch Monitoring permanen lokal | [monitoring-sst.patch](../../.agent-work/20261110-sst-ingestion-8c31/drafts/monitoring-sst.patch) |
| Manifest file dan provenance | [manifest.json](../../.agent-work/20261110-sst-ingestion-8c31/drafts/manifest.json) |

Checkout asli backend memiliki perubahan physical hub yang belum di-commit. Baseline isolated `83ae5ca` mempertahankan perubahan itu di atas HEAD asli `c496285`; patch SST hanya delta tugas ini. Monitoring asli memiliki perubahan `components/monitor-dashboard.tsx`, yang tidak disentuh atau disalin sebagai hasil SST. Kedua patch lulus `git apply --check` terhadap checkout asal ketika handover dibuat. Tidak ada push/PR.

## Yang diimplementasikan

- Dataset **`cmems_sst_hourly`**, variabel `thetao`, native hourly mean, depth nominal sekitar 0,494 m. Parameter **`sea_surface_temperature`** regional dipisahkan dari **`water_temperature`** sensor lokal.
- Profil A2 dan migration additive **`20261110000100_sst_hourly_ingestion.sql`**: registry, unit notasi `degrees_C` → `degC`, policy/state, gate serta wrapper validasi SQL sebelum persistence A2 yang sudah ada.
- Fetch/check nominal **3600 detik**, slot **H:05 UTC**, melalui dispatcher A2 tiap 900 detik. Publikasi model tetap nominal harian. Lease/backoff, retry dan `metadata_only` mengikuti rule sebelumnya; jadwal sumber lain dipertahankan.
- Adapter memeriksa product/dataset/version, grid, unit, standard name, depth, cadence, kelengkapan96slot dan perubahan revisi katalog selama fetch. Batas akhir request adalah timestamp23:00, supaya pemilihan `nearest` tidak menambahkan jam00:00 hari berikutnya.
- Dedup run/vintage tetap immutable: fetch identik tidak menambah nilai atau memperbarui receipt vintage pertama. Cell dapat dipakai beberapa plot. Source regional tidak ditulis sebagai observation sensor.
- Command **`ingest_environment.py plan --dataset cmems_sst_hourly`** menampilkan rencana ingestion secara offline/read-only, langsung dari konfigurasi pipeline. Policy/state database tetap otoritas jadwal setelah aktivasi.
- Wrapper scheduler A2 menjalankan `--refresh-alignment`, dengan restricted A2/A3 credentials terpisah. A3 menyimpan **history168jam selesai dan current1jam sebagai dua snapshot**, mempertahankan kompatibilitas request tujuh hari app lama. Kegagalan per source/plot/window diisolasi; execution telemetry memakai kode tersanitasi.
- Route API regional tetap sama, dengan opt-in **`include_sst=true`**. Tanpa opt-in, respons hanya parameter lama. Autentikasi, scope plot, rate limit dan batas window tetap berlaku; endpoint sensor tidak menerima opt-in ini.
- Policy A3 baru `pilot-quality-spatial-sst-1` menambahkan envelope QA suhu regional. Nilainya adalah envelope engineering, bukan threshold biologis atau risiko ice-ice.
- CI diperbarui untuk dependency group `environment` agar adapter SST dan pengujiannya tersedia; source schema/normalized schema dan executable contract registry ikut diperbarui.

## Rule yang tetap berlaku

`issue_time_basis=unknown`; waktu update STAC bukan issue time. Mean interval bounds tidak ditebak. `metadata_only`, lineage, immutable vintages, real/synthetic provenance, receipt cutoff dan pemeriksaan spatial/field support tetap dipertahankan. `training_authorized=false`. Suhu regional tidak mengisi missing sensor secara diam-diam.

Koordinat **-5.8211,106.5522** tetap referensi pulau dari pengguna, bukan lokasi dua probe physical. Config menyimpannya sebagai `audit_reference`, **bukan lokasi dispatcher**. Dispatcher mengambil location version yang terdaftar. Lokasi probe belum diketahui tidak otomatis memakai koordinat ini.

Cutoff A3 tetap awal jam: data pertama diterima13:20 tidak boleh mengisi row13:00. Dalam smoke lokal, API200 memuat konteks SST namun nilai current hour tetap `not_available` karena receipt lebih lambat dari cutoff; ini hasil yang benar, bukan kegagalan yang harus ditutup dengan backfill. Forecast untuk14:00 yang sudah diterima sebelum14:00 dapat dipilih pada cutoff berikutnya. Spatial gate masih dapat membuat `usable_context=false`.

## Entry Seagis Monitoring

Entry bertanggal10November sudah ditambahkan ke **`docs/IMPLEMENTATION_PLAN.md` dan `docs/VERIFICATION.md` pada branch Monitoring di atas**, bersama regression `tests/sst.sql`. Ini entry implementasi/test lokal, bukan deployment log production.

Monitoring menggunakan discovery dinamis dari `schedule_state`, attempt, ingestion run dan forecast volume. Setelah aktivasi backend, sumber SST akan terbaca pada **Pipelines → Environment workers / Execution attempts / Environmental output volume**. Tidak menambahkan baris sukses palsu atau memerlukan daftar sumber hardcoded. Observation/device coverage tetap khusus sensor. Verifikasi dilakukan pada source Monitoring lokal; kondisi schema/dashboard cloud saat ini tidak diperiksa ulang.

## Pemeriksaan yang benar-benar dijalankan

| Pemeriksaan | Hasil dan batas |
| --- | --- |
| PostgreSQL17 disposable, seluruh migrasi dan suite backend | **132 tes lulus**, sebelum refinemen orchestration terakhir |
| Final SST adapter/alignment/dispatcher unit tests | **14 tes lulus** pada source final, termasuk dua window A3 dan kegagalan claim source yang tidak menghentikan source lain |
| Deno route/contract/format/lint/type checks | **14 tes lulus**, format/lint/type checks lulus pada source final |
| Ruff, diff/whitespace, JSON dan patch applicability | Lulus; kedua patch dapat diterapkan ke baseline checkout asal saat diperiksa |
| End-to-end provider double sintetis → PostgreSQL17 → A2 → A3 → API → Monitoring | **Lulus**:96nilai, replay duplicate menambah0nilai, snapshot tersimpan, API200, entry/volume Monitoring terbaca melalui role runtime terbatas |
| Actual provider melalui adapter baru | Percobaan setelah koreksi batas waktu melewati fetch/parse/persist/A3/API sebelum gagal pada setup/pemeriksaan Monitoring harness; **bukan kelulusan smoke final lengkap** |
| Rerun final actual provider + Monitoring setelah harness diperbaiki | **Tidak dieksekusi**: automatic approval review mencapai batas penggunaan. Ini review failure karena kuota, bukan safety rejection |
| Full DB suite setelah refinemen orchestration terakhir / HTTP process integration | Belum dijalankan ulang; final unit dan Deno checks tersedia. Jangan menyebut133tes full DB atau HTTP end-to-end lulus |
| Production / iOS app | Tidak deploy, tidak build/ubah app, tidak memasang scheduler atau mengklaim kontinuitas hourly24/7 |

Bukti lokal permanen: [132 tests](../../.agent-work/20261110-sst-ingestion-8c31/drafts/postgres-132-tests.log), [14 final unit tests](../../.agent-work/20261110-sst-ingestion-8c31/drafts/final-14-unit-tests.log), [Deno final](../../.agent-work/20261110-sst-ingestion-8c31/drafts/deno-final.log), [synthetic full-chain smoke](../../.agent-work/20261110-sst-ingestion-8c31/drafts/synthetic-local-smoke-20261110.json), [ingestion plan](../../.agent-work/20261110-sst-ingestion-8c31/drafts/ingestion-plan.json). Data aktual dan fixture sintetis tidak dicampur sebagai bukti lapangan.

## Aktivasi berikutnya

Runbook terperinci berada di `docs/a2/sst-hourly.md` pada paket backend. Urutan yang disiapkan: rekonsiliasi ledger/HEAD cloud → apply migration SST baru saja → register hash/policy A3 → deploy opt-in Edge → release worker/config dan verifikasi restricted credentials → fetch terbatasi untuk lokasi terdaftar → periksa A3/API/Monitoring → observasi lintas jam dan hari pada host aktif. Script deploy umum dapat merotasi credentials; tidak dijalankan sekadar untuk menambah SST.

Untuk verifikasi final, setelah kuota review tersedia:

```sh
uv run --frozen --group environment python scripts/check_a1.py
uv run --frozen --group environment python scripts/check_sst_ingestion.py --live-provider --monitoring-path /private/tmp/seagis-sst-monitoring-8c31 --out artifacts/sst/live-local-smoke-20261110.json
```

Kedua command di atas menggunakan database test PostgreSQL lokal, bukan database cloud. `--live-provider` hanya mengaktifkan pengambilan Copernicus. Tidak boleh menganggapnya sudah dijalankan berdasarkan keberadaan command ini.

Integrasi iOS masih pekerjaan terpisah: DTO/domain/service/cache SST, opt-in dan pemicu/policy hourly/resume, label sumber fallback, lalu uji perangkat. Background iOS tidak menjamin waktu fetch tepat setiap jam. Keterwakilan suhu farm tetap perlu lokasi probe, kedalaman dan perbandingan overlap.

Indeks Engineering tidak diedit karena sudah memiliki perubahan pekerjaan lain. Terkait: [[Uji SST Hourly - Copernicus ke App]], [[Kontrak Fitur A4 - Forecast Suhu Air]], [[Operasi A2 - Adapter dan Scheduler]].
