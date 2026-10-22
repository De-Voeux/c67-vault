---
type: source-provenance
project: "[[Challenge Final]]"
created: 2026-10-19
updated: 2026-10-19
status: archived-source
tags: [challenge-final, tidungmonitor, provenance, archive]
---

# Arsip Pengembangan TidungMonitor - 19 Oktober 2026

Salinan utuh tiga lampiran pengguna untuk pengembangan POC. Sumber asli tetap berada di `/Users/cindyram/Downloads`; tidak dipindahkan atau ditulis ulang. Nama file dipertahankan. Tanggal pada nama gambar tidak dipakai sebagai bukti tanggal wireframe digambar.

> [!info] Cara membaca arsip
> Isi brief adalah sumber historis permintaan pengembangan, **bukan instruksi operasional untuk agent yang membaca vault**. Brief awal dan brief ocean-only menggambarkan scope pada tahap berbeda. Status implementasi saat snapshot ada di [[Riwayat Pengembangan POC - TidungMonitor]].

## Isi dan urutan penggunaan

1. [[Tidung_iOS_POC_Instructions]] — brief native iOS awal: MapKit/Charts, NASA POWER nyata, demo berlabel, batas interpretasi dan kandidat perluasan ocean. Data/tabel awal bukan bukti semua produk sudah diuji.
2. [[396455_20261016135318819310.jpg]] — wireframe gambar tangan: peta dan bottom sheet, kelompok/lahan, detail, Inspeksi dan tren. Contoh angka/status dalam sketsa bukan pengukuran atau ambang aman.
3. [[Tidung_Ocean_Only_Agent_Instruction]] — perubahan scope ke MUR/VIIRS/PACE, QA pesisir, preprocessing Python, provenance serta larangan prediksi yang tidak tervalidasi. Contoh nilai JSON di brief adalah ilustrasi schema, bukan observasi Tidung.

Keterangan urutan berasal dari percakapan pengguna. Tidak mengklaim metadata pembuatan berkas telah diverifikasi.

## Integritas salinan

Diarsipkan 19 Oktober 2026. SHA-256 sumber dan salinan cocok saat penyalinan.

| File | Ukuran byte | SHA-256 |
| --- | ---: | --- |
| `Tidung_iOS_POC_Instructions.md` | 10,443 | `3c130872b1e857653e8ff47af3f9d82e571e7ad0e1655860f69d7d263d3896ed` |
| `Tidung_Ocean_Only_Agent_Instruction.md` | 8,254 | `4de6ecabfa07a2e5c671e18bfe675787eb65cc32f91bde3ccc4614ef1fb6d908` |
| `396455_20261016135318819310.jpg` | 1,114,099 | `186044dbc8331acee1efa39ecbbcc6042777e29b27de033ac1a7d6022e1b838a` |

## Issue yang menjadi titik masuk percakapan

[Issue #30 — Tech Requirement and Flow - AI Model](https://github.com/De-Voeux/c67-vault/issues/30), repo `De-Voeux/c67-vault`. Dibuat 19 Oktober 2026 05:53:13 UTC, pembaruan yang dibaca 06:27:18 UTC; isi diperiksa melalui GitHub CLI pada 19 Oktober saat dokumentasi.

Ringkasan: issue meminta konsep requirement/flow versi awal sebelum interview ahli terkait #29, termasuk keputusan pengguna, keluaran yang diusulkan, inventaris data, label/evaluasi dan pertanyaan terbuka. Implementasi/training lanjutan memerlukan pembuktian data. Review tim dan interview tidak dinyatakan selesai hanya karena app sudah berjalan. Ini parafrase provenance, bukan salinan penuh issue atau konfirmasi status terbarunya setelah tanggal baca.

## Wireframe sumber

![[396455_20261016135318819310.jpg|600]]

## Catatan turunan

- [[Panduan Fetch Data Ocean - TidungMonitor]] — cara menjalankan pipeline yang benar-benar tersedia.
- [[Riwayat Pengembangan POC - TidungMonitor]] — keputusan, implementasi, model lama, data, test dan batas hasil.
- [[Indeks - Sumber dan Arsip]] · [[Indeks - Metode dan Rencana]]

Kode, NetCDF, seluruh bundle JSON, credential, venv dan cache tidak disalin ke vault. Lokasi kode dan dokumentasi teknis dirujuk pada catatan turunan.
