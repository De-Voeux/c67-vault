---
type: engineering-requirements
project: "[[Challenge Final]]"
created: 2026-11-12
status: kebutuhan-perlu-verifikasi-dan-kesepakatan
tags: [challenge-final, seagis, backend, ios]
---

# Kebutuhan Backend untuk iOS - Seagis

Daftar ini mencatat **seluruh kebutuhan backend dari tim iOS pada 12 November 2026**. Nama endpoint dan struktur respons di bawah adalah usulan untuk disepakati, bukan kontrak atau fitur yang telah terbukti tersedia. Backend berada di proyek terpisah; catatan ini tidak mengimplementasikan atau men-deploy perubahan.

## Identitas dan data lahan

- [ ] Tabel petani dengan ID stabil dan data yang diperlukan aplikasi; relasi petani–lahan yang eksplisit, termasuk aturan kepemilikan/akses dan perubahan relasi.
- [ ] Setiap lahan memiliki ID, nama, luas beserta unit dan asal perhitungan, titik koordinat dan batas/polygon; geometri yang belum ada atau belum disurvei dinyatakan jelas, bukan diisi koordinat contoh.
- [ ] Identitas node 1 dan node 2, kepemilikan dan riwayat pemasangan per lahan dengan periode berlaku; pemindahan alat tidak mengubah asal data historis. Suhu dikaitkan dengan node dan lahan yang benar pada waktu pengukuran.
- [ ] API daftar petani beserta lahannya dan API detail lahan untuk farm map serta plot detail. Identitas lahan konsisten pada semua endpoint.

## Sensor dan lingkungan

- [ ] API status sensor: aktif atau status lain yang diketahui, waktu terakhir mengirim, baterai, sinyal, dan alasan stale; sertakan waktu masing-masing status/telemetri dan bedakan tidak diketahui dari tidak aktif. Bedakan kontak terakhir dari pengukuran valid terakhir.
- [ ] Suhu node 1 dan 2 serta salinitas, arus, nitrat, fosfat dan SST untuk lokasi lahan; API riwayat dan prakiraan tiga hari. Jika sumber tidak mendukung horizon, lokasi, atau parameter tertentu, kembalikan status tidak tersedia, bukan nilai rekaan.
- [ ] Pisahkan pengukuran sensor fisik, data regional, forecast dan data sintetis. Data grid regional adalah konteks lokasi dengan resolusi dan pemetaan yang jelas, bukan otomatis pengukuran lahan; SST berbeda dari suhu probe. Nilai sintetis tidak boleh menyamar sebagai observasi nyata.
- [ ] Setiap nilai atau seri menyertakan waktu relevan, unit, kualitas, sumber, dan status/alasan stale. Bedakan waktu pengukuran, penerimaan, waktu berlaku dan waktu terbit forecast; pertahankan nilai kosong sebagai kosong, bukan nol. Sertakan identitas run/grid dan versi pemetaan jika relevan.

## Laporan dan penilaian

- [ ] Tabel dan API laporan ice-ice yang mengikat laporan ke lahan yang benar; API riwayat dan kalender laporan dengan tanggal dan zona waktu yang jelas. Catat status laporan/gejala dan sumbernya; laporan tidak otomatis diagnosis terverifikasi.
- [ ] API penilaian kondisi lahan dengan status **belum dinilai**, **aman**, atau **perlu diperiksa**. Sertakan waktu, sumber, versi aturan dan alasan/data yang digunakan; bila data atau aturan belum memadai, gunakan belum dinilai. Makna “aman” harus disepakati dan dibatasi pada kondisi yang dinilai, bukan jaminan bebas penyakit atau prediksi ice-ice tervalidasi.

## Akses, dokumentasi, dan pengujian

- [ ] Akses app tanpa login melalui session sementara, bukan shared token tertanam. Penerbitan, masa berlaku, pembaruan dan pencabutan sesi perlu disepakati; akses harus dibatasi di server berdasarkan data dan operasi yang diizinkan. Tidak adanya login tidak dengan sendirinya membuktikan identitas atau hak atas data petani/lahan.
- [ ] Dokumentasi API berversi, contoh JSON tanpa token atau data pribadi nyata, error, paginasi, zona waktu dan perilaku nilai kosong. Sediakan data development/staging yang jelas ditandai sintetis dan dapat diuji oleh iOS.
- [ ] Contract dan integration tests untuk mencegah petani, lahan, node, suhu dan laporan tertukar antar-plot, termasuk akses sesi yang tidak berhak, pemindahan node, histori, data kosong/stale dan pemisahan sintetis/nyata.

## Bentuk API untuk didiskusikan

Berikut pembagian fungsi, bukan path final atau bukti endpoint sudah tersedia: pembuatan sesi; daftar petani dengan lahan; detail lahan dan geometri; status dan riwayat per node; kondisi lingkungan terkini, riwayat dan forecast per lahan; buat/baca laporan, riwayat dan agregasi kalender; serta pembacaan assessment. Tentukan operasi tulis yang memang dibutuhkan dan scope tiap sesi bersama iOS/backend.

## Dasar dan keputusan terbuka

Snapshot [[Supabase - seagis.plot]] tanggal 22 Oktober 2026 telah mencatat ID, nama dan koordinat nullable, tetapi bukan bukti bahwa seluruh kebutuhan di atas ada saat ini. [[Rancangan Kontrak dan Migrasi Hub IoT]] adalah usulan untuk review, termasuk mapping historis, health dan stale; bukan migrasi diterapkan. [[Status Integrasi Seagis - 28 Oktober 2026]] membedakan jalur demo regional dari API produksi. Handoff Track C 12 November mencatat kontrak plot/laporan/assessment dan sesi produksi belum tersedia pada auditnya; status backend terbaru masih perlu diperiksa.

Keputusan bersama yang masih diperlukan: relasi dan operasi petani/lahan; definisi kepemilikan dan instalasi node; akurasi/pemetaan geometri; penerbitan dan otorisasi sesi tanpa login; ketersediaan sumber per parameter dan horizon; definisi stale dan kalender; input, batas dan aturan assessment; serta kontrak versi, fixture dan lingkungan staging. Daftar ini tidak menetapkan prioritas atau menyatakan seluruh item sudah dibangun.

[[Indeks - Engineering]]
