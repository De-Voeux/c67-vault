---
type: moc
project: "[[Challenge Final]]"
updated: 2026-10-22
tags: [challenge-final, seagis, category/engineering]
---

# Indeks - Engineering

Simpan semua catatan engineering baru proyek di folder ini: arsitektur, implementasi, kontrak data, dan panduan operasional. Catatan riset, metode validasi, dan rencana lapangan tetap di [[Indeks - Metode dan Rencana]].

## Rencana implementasi

Dokumen berikut adalah rencana kerja v0.1, bukan bukti bahwa komponen sudah diterapkan atau tervalidasi.

- [[TRACK_A_DATA_ML_ENGINEERING]] — rencana fondasi data, ingestion lingkungan, kualitas data, dan forecasting suhu.
- [[TRACK_B_SCIENTIFIC_KNOWLEDGE_VAULT]] — rencana evidence vault, verifikasi klaim ilmiah, retrieval, dan interpretasi on-device.

## Seagis

- [[Pembaruan Desain - Sensor Suhu Hourly dan Inferensi On-Device]] — keputusan perangkat dan inferensi on-device; ingestion IoT ada di A1; ingestion lingkungan regional ada di A2.

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

### Database Supabase — schema aktual\n\n- [[Peta Database Supabase Seagis]] — 28 tabel dan 1 view; detail kolom, constraints, relasi, indeks, trigger dan RLS berdasarkan snapshot catalog 22 Oktober 2026.\n\n### B0 — fondasi scientific knowledge vault

- [[Implementasi B0 - Fondasi Vault Pengetahuan Ilmiah Seagis]] — pertanyaan, taksonomi, schema, registry kandidat dan protokol review; 0 temuan terverifikasi.
- [[Provenance Impor B0 - Seagis Knowledge Vault - 21 Oktober 2026]] — commit sumber dan checksum snapshot 15 file.

## TidungMonitor

- [[Riwayat Pengembangan POC - TidungMonitor]] — log implementasi aplikasi dan pipeline.
- [[Panduan Fetch Data Ocean - TidungMonitor]] — runbook pemakaian pipeline.
