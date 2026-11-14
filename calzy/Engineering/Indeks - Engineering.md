---
type: moc
project: "[[Challenge Final]]"
updated: 2026-11-14
tags: [challenge-final, seagis, category/engineering]
---

# Indeks - Engineering

Simpan semua catatan engineering baru proyek di folder ini: arsitektur, implementasi, kontrak data, dan panduan operasional. Catatan riset, metode validasi, dan rencana lapangan tetap di [[Indeks - Metode dan Rencana]].

## Rencana implementasi

Dokumen berikut adalah rencana kerja, bukan bukti bahwa komponen sudah diterapkan atau tervalidasi.

- [[TRACK_A_DATA_ML_ENGINEERING]] — rencana fondasi data, ingestion lingkungan, kualitas data, dan forecasting suhu.
- [[Rencana Track A v0.2 - Pembaruan A0 sampai A3]] — gap baseline, urutan P0–P5, migrasi kompatibel dan 15 acceptance cases. Status implementasinya ada di [[Track A v0.2 - Handover Implementasi A0-A3]].
- [[TRACK_B_SCIENTIFIC_KNOWLEDGE_VAULT]] — rencana evidence vault, verifikasi klaim ilmiah, retrieval, dan interpretasi on-device.
- [[Status Track B - Fokus B0.5 dan Review Manual]] — prioritas interpretasi suhu FM dan bacaan untuk review manusia; B1 menunggu arahan.
- [[Rencana Dashboard Admin Monitoring - Akun Lokasi Sensor]] — rencana dashboard admin di monitoring.seagis.app untuk akun app, penugasan lahan, lokasi dan sensor; belum diimplementasikan.

## Seagis

### Status terbaru

- [[Handover Seagis - Status Pilot Tidung - 14 November 2026]] — probe fisik Tidung, login akun penyuluh, audit ingestion IoT, Monitoring WIB/offline dan status scheduler; daftar pekerjaan yang belum di-push.
- [[Handover Seagis - Integrasi dan Kesiapan Rilis - 12 November 2026]] — baseline sebelumnya: alignment app–API–database, forecast harian, logging ice-ice, checklist App Store dan aktivasi monitoring per jam.

### Audit dan kebutuhan

- [[Audit Kesiapan Backend dan Next Cycle - 12 November 2026]] — audit source backend/app terhadap kebutuhan iOS, hasil 133 tes lokal dan urutan pekerjaan berikutnya.

- [[Kebutuhan Backend untuk iOS - Seagis]] — kebutuhan data, API, sesi, provenance dan pengujian dari iOS; belum menyatakan implementasi.

- [[Status Integrasi Seagis - 28 Oktober 2026]] — lokasi aplikasi utama, baseline iOS dan kesiapan integrasi A/B/C; pemeriksaan awal, bukan implementasi live.
- [[Handover Track C - Status Integrasi 29 Oktober 2026]] — status keseluruhan C0–C14, bukti slice C1 demo, cara menjalankan ulang dan pekerjaan berikutnya.

- [[Pembaruan Desain - Sensor Suhu Hourly dan Inferensi On-Device]] — keputusan perangkat dan inferensi on-device; ingestion IoT ada di A1; ingestion lingkungan regional ada di A2.

### Rencana pembaruan Track A v0.2

- [[Rencana Track A v0.2 - Pembaruan A0 sampai A3]] — kebutuhan dan paket kerja P0–P5. Status implementasi branch, validasi, dan deployment dicatat di [[Track A v0.2 - Handover Implementasi A0-A3]].

### Model v1 — cakupan dan langkah berikutnya

- [[Model v1 - Cakupan dan Tugas Berikutnya]] — progress ML, keputusan menahan model, rencana 29 Oktober serta langkah A4 dan A5.
- [[Kontrak Fitur A4 - Forecast Suhu Air]] — ringkasan kontrak eksperimen forecast; rancangan, bukan kontrak production.
- [[A5 - Rencana Monitoring Training]] — kebutuhan menampilkan proses training di Monitoring; rencana, belum implementasi.

### SST hourly

- [[Uji SST Hourly - Copernicus ke App]] — uji akses Copernicus hourly sampai decoding Swift; bukti dan script di folder `SST-Hourly-Audit`.
- [[Integrasi SST Hourly - Pipeline A2 A3]] — SST hourly aktif di backend Singapore sejak 10 November; API dan Monitoring terverifikasi.

### UI aplikasi

- [[Rencana Porting UI AppPOC ke Seagis]] — port UI dan komponen AppPOC ke aplikasi utama dengan data tetap dari Seagis.

### Panduan pipeline A0-A3

- [[Pipeline Seagis A0-A3 - Alur dan Skematik]] — alur menyeluruh, enam diagram vektor, runtime Mac/Supabase, akses IoT, QC, cutoff, lineage dan handover.
- [[Seagis - Pipeline A0-A3.pdf]] — versi PDF panduan yang sama untuk dibaca dan dibagikan.

### CSV untuk eksperimen forecast

- [[CSV Forecast - Data dan Cara Pakai]] — 13 CSV terpisah per fitur: suhu air dummy per plot dan 11 parameter regional pada cadence native; metadata/QC, pemilihan vintage dan contoh pandas.

### Database Supabase — schema aktual

- [[Peta Database Supabase Seagis]] — inventaris live 28 tabel dan 1 view; catatan per tabel, kolom, constraint, FK, indeks, trigger dan RLS, diperiksa 22 Oktober 2026.

### A0 — fondasi data

- [[Implementasi A0 - Fondasi Data Seagis]] — snapshot rancangan dan validasi lokal A0 tanggal 21 Oktober; deployment cloud dilanjutkan pada A1.
- [[Seagis A0 - Architecture]]
- [[Seagis A0 - Source Registry]]
- [[Seagis A0 - Data Dictionary]]
- [[Seagis A0 - Data Contracts]]
- [[Seagis A0 - ADR-001 Data Storage]]
- [[Seagis A0 - A0 Review]]
- [[Provenance Salinan Engineering A0 Seagis - 21 Oktober 2026]]

### A1 — pipeline suhu dan handover IoT

- [[Handover A1 - Arsitektur Data dan Akses IoT]] — endpoint cloud, payload, sensor binding, QC dan commissioning hardware nanti.
- [[Operasi A1 - Simulator dan Credentials]] — command simulator, deployment, provisioning, expiry/revocation dan troubleshooting.
- [[Review A1 - Temperature Vertical Slice]] — 136 observasi sintetis live, hasil 63 Python + 7 Deno tests serta uji HTTP/SCRAM dan akses cloud.
- [[Provenance A1 - Paket Handover 22 Oktober 2026]] — commit sumber, checksum dan bukti live tanpa secrets.

### A2 — ingestion lingkungan regional

- [[Handover A2 - Ingestion Lingkungan dan Grid]] — adapter, grid bersama, vintage, preview demo dan batas availability.
- [[Operasi A2 - Adapter dan Scheduler]] — command worker terbatas, cadence provider, scheduler Mac dan monitoring.
- [[Lisensi A2 - Atribusi dan Retention]] — hak akses, credit dan kebijakan metadata_only.
- [[Review A2 - Hasil Ingestion Regional]] — 466 nilai live dari tiga sumber; salinitas tertahan pembaruan provider.
- [[Provenance A2 - Paket Engineering 22 Oktober 2026]] — commit sumber, checksum dan laporan operasi tanpa secrets.

### A3 — kualitas dan alignment data

- [[Handover A3 - Kualitas dan Alignment Data]] — QC pilot, hourly cutoff, cadence native, mapping dan lineage append-only.
- [[Operasi A3 - Snapshot dan Quality Report]] — command on demand, akses schema privat dan cara membaca coverage.
- [[Review A3 - Hasil dan Batas Validasi]] — 94 Python + 7 Deno tests; dua snapshot terbaru dengan 20 konteks regional per plot, tetap demo.
- [[Provenance A3 - Paket Engineering 22 Oktober 2026]] — commit, checksum, bukti operasi dan batas runtime Mac/Supabase.

### B0 — fondasi scientific knowledge vault

- [[Implementasi B0 - Fondasi Vault Pengetahuan Ilmiah Seagis]] — pertanyaan, taksonomi, schema, registry kandidat dan protokol review; 0 temuan terverifikasi.
- [[Provenance Impor B0 - Seagis Knowledge Vault - 21 Oktober 2026]] — commit sumber dan checksum snapshot 15 file.

## TidungMonitor

- [[Riwayat Pengembangan POC - TidungMonitor]] — log implementasi aplikasi dan pipeline.
- [[Panduan Fetch Data Ocean - TidungMonitor]] — runbook pemakaian pipeline.
