---
type: engineering-plan
project: "[[Challenge Final]]"
updated: 2026-11-11
status: planned
tags: [challenge-final, seagis, engineering, ui]
---

# Rencana Porting UI AppPOC ke Seagis

## Tujuan dan prinsip

Port seluruh UI dan komponen AppPOC ke aplikasi utama Seagis. AppPOC adalah acuan bentuk dan interaksi; Seagis tetap menjadi sumber alur, state, dan data. Prioritas pertama adalah menjaga sumber data Seagis yang sudah tersedia, kemudian menyelaraskan UI tanpa mengubah bentuk komponen.

- Pertahankan layout, hierarki, ukuran relatif, material, warna, grafik, animasi, gesture, dan state interaksi AppPOC. Bandingkan pada perangkat dan kondisi yang sama.
- Adaptasikan komponen ke model dan ViewModel Seagis; jangan menyalin service, store, fixture, atau perhitungan POC sebagai pengganti data Seagis.
- Jika data belum tersedia, tampilkan state kosong atau unavailable dengan bahasa visual yang konsisten. Jangan mengisi angka POC agar UI tampak lengkap.
- Pertahankan provenance, waktu sumber, kualitas, dan label data sintetis. Bedakan pengukuran lokal, konteks regional, dan forecast.
- Ikuti arsitektur aktif `View → ViewModel → Providing → Service`, dengan dependency injection melalui `AppContainer`.
- Ini rencana, bukan bukti implementasi atau validasi. Referensi: kode `/Users/cindyram/Documents/Apple/AppPOC/POCApp` dan `/Users/cindyram/Documents/Apple/Seagis` dibaca secara statis pada 11 November 2026; belum dibandingkan di simulator.

## Peta sumber data

| Alur | Kondisi Seagis yang diperiksa | Perlakuan porting |
| --- | --- | --- |
| Petani dan lahan | Farmer/plot service dan FarmStore in-memory dengan fixture sintetis | Pertahankan service dan identitas Seagis; adaptasikan UI POC. |
| Suhu | Jalur development HTTP, mapper, cache, dan ViewModel | Pertahankan jalur ini; jangan mengganti dengan simulasi POC. |
| Konteks regional | Jalur development HTTP, mapper, cache, dan ViewModel | Pakai parameter yang tersedia dan beri konteks regional, bukan pengukuran lokal. |
| Sensor individual | InMemorySensorService sintetis | Adaptasikan UI dan pertahankan penanda contoh; sensor produksi menunggu kontrak. |
| Laporan dan kalender ice-ice | InMemoryIceIceReportService dan calendar ViewModel | Gunakan laporan Seagis; penyimpanan saat ini hanya selama aplikasi berjalan. |
| Capture lahan | Flow simulasi dan state sementara | Port UI; GPS/AR aktual dan penyimpanan produksi perlu integrasi tersendiri. |
| Assessment | Status dan sebagian issue masih fixture/prototype | Pertahankan batas prototype; jangan menganggap threshold POC sebagai assessment tervalidasi. |

Dokumentasi Seagis menyebut pergantian plot pada jalur temperature dan regional context belum diimplementasikan. Verifikasi kondisi aktual dan tangani isolasi data sebelum UI memberi kesan bahwa setiap plot sudah memiliki koneksi live masing-masing.

## Tahapan

### 1. Baseline dan kontrak data

- Inventarisasi seluruh layar, komponen, state, interaksi, dan aset POC yang digunakan; pasangkan dengan implementasi Seagis dan catat gap.
- Jalankan kedua aplikasi pada simulator dan konfigurasi yang sama; ambil referensi light/dark, ukuran teks normal dan accessibility, serta state utama.
- Petakan setiap elemen ke identitas plot/sensor, nilai, unit, timestamp, quality, sumber, dan state loading/error/empty di Seagis.
- Periksa jalur temperature dan regional, plot development, cache, respons terlambat, serta batas data multi-plot.

**Selesai bila:** semua layar punya pasangan atau gap tercatat dan setiap nilai memiliki sumber Seagis yang jelas.

### 2. Fondasi visual dan komponen bersama

- Selaraskan `MarineTheme` dengan token POC, termasuk kontras light/dark, warna status dan pin grafik, serta shading waktu lampau.
- Port material sheet, sheet card, backdrop laut, spacing, radius, tombol lingkaran, ikon, typography, dan state pressed/focus/accessibility.
- Pertahankan komponen Seagis jika bisa diselaraskan; adaptasi komponen POC jika padanan belum sesuai.

**Selesai bila:** preview komponen Seagis sesuai referensi POC pada state yang sama tanpa mengubah semantik status.

### 3. Farm Map, navigasi, dan sensor

- Samakan polygon, gradient, label, penanda, alert, dan toolbar peta.
- Samakan detent minimized/collapsed/expanded, header kontekstual, tab, transisi, dan navigasi kembali.
- Port daftar petani/lahan, empty state, tambah/hapus, share, dan konfirmasi dengan tindakan Seagis.
- Port sensor list sheet, pengelompokan, filter, status koneksi, dan jalur menuju detail sensor; gunakan data sensor Seagis.

**Selesai bila:** alur peta setara dengan POC dan pilihan plot tidak mencampur data antar-lahan.

### 4. Detail lahan dan widget kondisi

- Samakan status card, issue, tindakan pencatatan, urutan widget yang perlu perhatian, dan bagian kondisi lain.
- Port widget suhu, salinitas, arus, nitrat dan fosfat: bentuk, grafik, gauge, animasi, label, dan accessibility.
- Samakan dua kolom nutrien dan layout Dynamic Type, backdrop, serta jarak pada setiap detent.
- Pertahankan state loading, partial, stale, empty, dan error dengan provenance Seagis.

**Selesai bila:** widget yang datanya tersedia sesuai POC secara visual dan tetap memakai sumber serta status Seagis.

### 5. Detail parameter dan sensor

- Port day strip, grafik per jam, swipe hari, pemilihan titik, ringkasan, insight, bagian tentang, dan highlights.
- Samakan daftar sensor, peta, pin, range, status koneksi, dan navigasi detail sensor.
- Tampilkan historis, saat ini, atau forecast hanya jika memang tersedia; pertahankan sumber, waktu, dan quality.
- Jangan menyatakan radius atau cakupan fisik sensor POC sebagai fakta tanpa kontrak deployment.

**Selesai bila:** navigasi dan visual setara POC; nilai dan ketersediaan berasal dari Seagis.

### 6. Catatan, statistik, tren, dan kalender

- Bangun Catatan dengan Statistik, Wawasan, dan Kalender; port kartu interaktif, expand/collapse, tren, filter periode, kalender, dan detail hari.
- Hubungkan laporan ke report service Seagis dan kondisi harian hanya ke tanggal/parameter yang tersedia.
- Petakan kebutuhan data statistik dan tren sebelum menampilkan angka. Bobot contoh, persentase, dan klaim “Pemicu Ice-ice” di POC tidak boleh dianggap bukti sebab atau probabilitas. Gunakan state unavailable jika tidak didukung.

**Selesai bila:** alur Catatan tersedia tanpa angka atau klaim yang tidak didukung sumber Seagis.

### 7. Capture dan penyimpanan lahan

- Port pemilihan metode, instruksi, peta, chrome, kontrol, undo, preview batas, dan save sheet untuk state simulasi Seagis.
- Audit integrasi GPS/AR aktual secara terpisah: permission, lifecycle, akurasi, dukungan perangkat, geometri, error, dan penyimpanan.

**Selesai bila:** simulasi mengikuti bentuk dan interaksi POC; kemampuan perangkat yang belum terhubung tetap disebut simulasi.

### 8. Panduan dan pencatatan ice-ice

- Samakan sheet, ilustrasi, tombol, scroll ke panduan, dan navigasi. Jawaban tetap melalui report service Seagis.
- Tinjau wording POC yang menyatakan sebab terlalu pasti; laporan gejala tidak otomatis menjadi diagnosis.

**Selesai bila:** visual dan interaksi selaras, jawaban tersimpan sesuai kemampuan service, dan isi sesuai batas bukti.

## Verifikasi akhir

- **Visual:** bandingkan screenshot setiap layar dan state dengan perangkat, ukuran teks, mode warna, detent, dan data presentasi yang sebanding; catat perbedaan yang diperlukan untuk provenance atau data unavailable.
- **Interaksi:** uji navigasi, sheet, gesture, filter, pemilihan grafik, tombol, dan back behavior.
- **Integritas data:** uji identitas plot/sensor, unit, waktu, quality, provenance, isolasi cache, dan respons terlambat; jangan ganti data Seagis dengan fixture POC.
- **Kondisi batas:** periksa loading, empty, error, offline/stale, data parsial, sensor terputus, dan ukuran teks accessibility.
- **Regresi:** jalankan build Seagis, test kontrak/mapping/ViewModel yang relevan, dan UI test alur utama. Gunakan XcodeGen sesuai `project.yml` saat struktur berubah.
- **Handoff:** catat setiap hasil sebagai implemented, tested, mocked, proposed, atau blocked beserta kontrak dan data yang masih dibutuhkan. Jangan mengklaim build atau visual parity sebelum benar-benar diuji.

## Rujukan proyek

- [[Status Integrasi Seagis - 28 Oktober 2026]] — audit awal historis; periksa kondisi aktual sebelum implementasi.
- [[Handover Track C - Status Integrasi 29 Oktober 2026]] — konteks integrasi historis.
- Repository Seagis: `README.md`, `AGENTS.md`, `SPEC_REFERENCE.md`, `docs/architecture.md`, serta ADR-002 untuk batas dan arsitektur aktif.
