---
type: engineering-handover
project: "[[Challenge Final]]"
created: 2026-10-27
updated: 2026-10-27
tags: [seagis, engineering, ios, current]
source_commit: 7ac8cd1
---

# AppPOC - Magnitude Arus dan Penghapusan TidungMonitor

> **Pembaruan 28 Oktober:** ini snapshot historis AppPOC. Aplikasi utama sekarang berada di `/Users/cindyram/Documents/Apple/Seagis`; perilaku dan hasil uji AppPOC di bawah tidak otomatis berlaku pada aplikasi tersebut. Lihat [[Status Integrasi Seagis - 28 Oktober 2026]].

User meminta perubahan khusus arus dan penghapusan app lama. Source: `/Users/cindyram/Documents/Apple/AppPOC`, commit `7ac8cd1`.

- `CurrentVector` menyimpan komponen eastward/northward m/s. Speed = hypot(uo,vo). Direction toward = atan2(uo,vo), clockwise dari utara, 0..360 derajat.
- `ConditionPoint.current` menyimpan magnitude pada value untuk grafik dan vektor asal pada currentVector. CurrentWidget membaca magnitude/arah dari vektor; nilai tanpa vektor tampil tidak tersedia.
- Vektor nol mempunyai speed0 dan arah nil. Null/nonfinite/overflow ditolak. Komponen negatif sah. Aksesibilitas tidak mengasumsikan utara jika arah hilang.
- Simulator membentuk pasangan komponen pada timestamp sama lalu melalui jalur vektor yang sama. Tetap data sintetis. Belum ada koneksi API backend atau klaim data regional live.
- Adapter backend kelak wajib memeriksa pasangan run/cell/depth/valid time sama sebelum membentuk CurrentVector; tipe matematis ini belum memverifikasi provenance database.

Build simulator POCApp generic destination dengan signing dimatikan lulus. Pemeriksaan Swift magnitude 3/4->5, kuadran/cardinal, zero/nil/NaN/infinity/overflow lulus. Tidak ada pemeriksaan UI visual atau perangkat fisik pada tugas ini.

`TidungMonitor/` dan `TidungMonitor.xcodeproj/` dihapus. Package TidungCore, Model, Tools, Documentation, UI tests lama dan project.yml tetap disimpan sebagai arsip; manifest lama tidak boleh digunakan untuk generate POCApp. AGENTS dan README menjelaskan app aktif POCApp. Cleanup luas aset pendukung ditolak automatic approval review karena potensi aset bersama; scope dipersempit dan berhasil. Arsip pemulihan dua folder app lama ada sementara di `/private/tmp/AppPOC-TidungMonitor-before-removal.tar.gz`.

Perubahan signing pengguna pada POCApp.xcodeproj/project.pbxproj dipertahankan dan tidak ikut commit agent. Tidak ada push atau pembaruan PR C67 pada tugas implementasi app ini.

Navigasi: [[Indeks - Engineering]] · [[Rencana Track A v0.2 - Pembaruan A0 sampai A3]].
