---
type: engineering-contract
project: "[[Challenge Final]]"
created: 2026-11-06
status: draft
tags: [challenge-final, seagis, engineering, track-a, feature-engineering]
---

# Kontrak Fitur A4 - Forecast Suhu Air

Kontrak eksperimen lengkap ada di `Documents/Apple/Seagis-Model/docs/FEATURE_CONTRACT_A4.md`, commit `9da4487`. Ini rancangan untuk eksplorasi model, belum implementasi atau kontrak production.

- Satu baris mewakili plot, deployment sensor, waktu keputusan dan horizon; target suhu terukur tetap terpisah.
- Bandingkan tanpa imputasi, forward fill terbatas, dan interpolasi gap satu slot ketika kedua observasi sudah tersedia pada cutoff. Label, umur, kualitas dan lineage wajib tercatat. Aturan mencari `n+2` dan seterusnya belum diputuskan.
- Kandidat fitur suhu meliputi lag, delta 1 jam, rolling mean 3/6/12/24/72 jam, min/max/std, pola waktu lokal, missingness dan baseline plot. Coverage dan jumlah imputasi dicatat; aturan awal rolling meminta seluruh slot usable.
- Forecast cuaca dapat dipakai jika sudah tersedia pada waktu keputusan; valid time boleh mendatang. Salinitas, nutrien dan arus tetap konteks regional dengan metadata lokasi dan kualitas.
- Keputusan 5 November mengeluarkan suhu udara dan angin dari scope Open-Meteo aktif; keduanya di kontrak hanya kandidat riset dan memerlukan keputusan/sumber terpisah. Perubahan backend ada pada branch terpisah, status deployment perlu diperiksa.
- Evaluasi dilakukan dengan baseline, split waktu, target non-imputed dan metrik per horizon. Data dummy dan regional yang belum overlap belum membuktikan kemampuan forecast farm.

Kondisi cuaca Tidung yang dibagikan pengguna adalah konteks rencana pengumpulan, bukan jaminan kondisi lapangan.

Terkait: [[Model v1 - Cakupan dan Tugas Berikutnya]], [[Track A v0.2 - Handover Implementasi A0-A3]].
