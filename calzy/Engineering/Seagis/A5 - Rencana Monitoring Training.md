---
type: engineering-plan
project: "[[Challenge Final]]"
created: 2026-11-06
status: planned
tags: [challenge-final, seagis, engineering, track-a, monitoring, ml]
---

# A5 - Rencana Monitoring Training

## Maksud dan status

Pengguna ingin proses training model suhu air nantinya terlihat di Seagis Monitoring. Ini kebutuhan untuk fase **A5 — modelling dan evaluasi**, dengan integrasi ke web monitoring setelah kontrak run tersedia. **Status: catatan rencana; belum ada implementasi, training, perubahan database, deployment, atau jadwal yang ditetapkan.** A4 menyiapkan fitur/lineage; A5 menyiapkan eksperimen, training dan evaluasi. Web monitoring bertugas membaca status dan hasil yang dipublikasikan training worker; training tidak harus berjalan di dalam server dashboard.

```text
Data + fitur berversi → training worker → catatan run & artefak
                                         ↓
                           API/reader terbatas → Monitoring web
```

## Informasi yang ingin ditampilkan

- Status run: queued, running, succeeded, failed, cancelled; waktu mulai/selesai, durasi, progress bila benar-benar tersedia dan alasan kegagalan yang aman.
- Identitas eksperimen/model, versi kode dan fitur, cutoff, plot, rentang dan kualitas data, jumlah contoh, horizon, serta penanda sintetis atau nyata.
- Metrik evaluasi per horizon dan split waktu seperti MAE, RMSE, bias, coverage, jumlah sampel dan pembanding baseline; tampilkan periode, plot dan unit °C. Jangan bandingkan run dengan data/split berbeda seolah setara.
- Tautan/identitas artefak, model card, status eligibility, versi model yang digunakan dan riwayat keputusan penerimaan/penolakan jika mekanisme tersebut nanti dirancang.
- Status belum tersedia dan penyebabnya saat training belum dijalankan, metrik belum dihitung, worker offline atau data tidak layak; jangan tampilkan nilai nol atau progress palsu.

## Keputusan desain yang masih terbuka

1. Di mana worker berjalan, bagaimana trigger/jadwal/retry/cancel bekerja, dan bagaimana memenuhi batas biaya gratis pengguna. Runtime, kuota dan retensi perlu dievaluasi sebelum dipilih.
2. Dashboard awal cukup read-only atau operator juga perlu tombol menjalankan/membatalkan training? Akses tulis, audit dan otorisasi terpisah memerlukan desain dan persetujuan sesuai konteks implementasi.
3. Bentuk kontrak `training_run`, lifecycle, metadata dataset/split, penyimpanan artefak, lineage, update progress dan retensi log. Jangan menyalin raw data atau secret ke dashboard.
4. Siapa yang menyetujui penggunaan model dan bagaimana rollback dilakukan? Training sukses tidak otomatis berarti model layak digunakan di farm atau tersedia untuk app.
5. Bagaimana membedakan eksperimen sintetis dari evaluasi data lapangan, dan bagaimana mencatat dukungan model untuk lokasi/horizon berbeda?

## Batas saat ini

Kontrak fitur masih draft: [[Kontrak Fitur A4 - Forecast Suhu Air]]. [[Model v1 - Cakupan dan Tugas Berikutnya]] mencatat bahwa model dan training belum selesai. Sistem monitoring telah memiliki rancangan observability lain, namun pekerjaan itu tidak membuktikan adanya kontrak job training atau hasil model. Evaluasi akurasi lapangan memerlukan data sensor nyata, split kronologis dan baseline; tidak ada diagnosis atau probabilitas ice-ice dari metrik training.

## Kriteria handover fase A5 mendatang

- Run beridentitas dan berversi dapat ditelusuri dari input yang diizinkan hingga metrik dan artefak.
- Dashboard dengan akses terbatas memperlihatkan status, kesalahan yang aman dan hasil aktual, termasuk keadaan kosong/offline.
- Eksperimen sintetis diberi label dan tidak dipresentasikan sebagai validasi lapangan; promosi model merupakan keputusan terpisah.
- Uji lifecycle job, hak akses, kegagalan, pencatatan hasil dan batas biaya sebelum rollout.
