# Acuan awal dan batas akses B0

Capture: `2026-10-21T23:23:40+07:00`. Base awal: `second_brain_challenge_final`, folder lokal `Documents/Second Brain/02-Projects/Challenge Final`. Root absolut tidak disimpan di registry; gunakan root lokal sendiri untuk resolve path. Acuan implementasi: lampiran `TRACK_B_SCIENTIFIC_KNOWLEDGE_VAULT.md`, bagian B0. User meminta B0 saja dan commit, bukan publikasi atau fase berikutnya.

## Registry awal

Keempat sumber di bawah adalah **catatan sekunder internal**, bukan empat studi independen. Konten lengkap tidak disalin. `year: 2026` adalah tahun catatan. Tidak ada identitas reviewer manusia yang dibuat dari nama penulis/narasumber.

| ID | Path relatif base | SHA-256 saat capture |
|---|---|---|
| `SB-SYNTHESIS` | `07-Riset Ice-Ice/Research Ice-Ice/Sintesis Penyebab Ice-Ice.md` | `124b367170c1320f5a20c19a26760ac4820233e2f15e8ac3900f40c0e3681fac` |
| `SB-MATRIX` | `07-Riset Ice-Ice/Research Ice-Ice/Matriks Bukti Ice-Ice.md` | `d28424eed7be861375933762354323c7f7b0349e8dec2196b923eb382298ccfd` |
| `SB-INDICATORS` | `07-Riset Ice-Ice/Research Ice-Ice/Kajian Indikator Warning Ice-Ice - Uji Asumsi Fitur.md` | `eedcd8cc094fb8ced96c98423e37c01173d624a15d90fdf25b56bc4db02b5669` |
| `SB-THREE-PAPERS` | `07-Riset Ice-Ice/Research Ice-Ice/Tiga Paper Baru - Implikasi Pengukuran IoT 2026-10-20.md` | `8bc75dfe5ac8d7e40e41949c97f1afe5dcdc114401b56dd583ad1f22c3444243` |

Git source saat capture: `6a839b6e19e77e80bf0ecc2c301e37610f108c4a`. Hash byte tiap file dan `working_tree_modified` di registry adalah penentu snapshot; HEAD saja tidak mewakili perubahan belum di-commit. Status dan diff sumber diperiksa, seluruh perubahan existing dipertahankan. Tidak ada catatan Second Brain diubah dalam tugas ini.

## Konteks desain yang dibaca

`Challenge Final.md`, `00-Navigasi/Challenge Response - Seaweed Ice-Ice.md`, `00-Navigasi/Peta Catatan - Challenge Final.md`, `07-Riset Ice-Ice/Indeks - Riset Ice-Ice.md`, serta `07-Riset Ice-Ice/Research Ice-Ice/Empat Variabel Lingkungan dan Batas Kuantifikasi Ice-Ice.md` dipakai untuk framing dan batas klaim. Manifest tiga paper lokal dipakai untuk mengidentifikasi calon sumber, bukan untuk mewarisi klaim verified.

Catatan terbaru halaman proyek menyatakan sensor suhu saja, satu per tambak, hourly; alasan tim: biaya dan kualitas pengukuran sensor salinitas yang dapat diperoleh. Ini keputusan/rencana engineering. Catatan tiga paper bertanggal 20 Oktober masih memuat konfigurasi suhu+salinitas dan angka pilot; jangan menganggapnya requirement perangkat terkini atau threshold biologis.

## Petunjuk sumber primer untuk B1

Berikut metadata yang **dilaporkan catatan/manifest**, belum diperiksa ulang daring atau dari PDF pada B0:

| ID lama | Penulis/tahun menurut catatan | DOI menurut catatan | Status dalam B0 |
|---|---|---|---|
| P22 | Tabonda-Nabor et al., 2026 | `10.1111/jpy.70148` | Lead cahaya; belum record paper/ekstraksi baru |
| P23 | Aguilar et al., 2026 | `10.1093/femsle/fnag080` | Lead asosiasi bakteri gene bank; bukan challenge kausal yang diasumsikan |
| P24 / W04 | Gacura et al., 2025 | `10.1111/jpy.70044` | Lead salinitas–nutrisi; dua ID untuk studi sama menurut catatan |

Catatan matriks memuat 21 PDF/20 artikel unik dan menyebut S14 duplikat S13. Angka cakupan tersebut milik audit terdahulu, bukan jumlah paper yang direview ulang B0. Jangan menjumlahkan catatan sintesis sebagai replikasi.

## Akses dan batas hasil

File Markdown dan manifest lokal dapat dibaca. Tidak dilakukan akses ulang PDF, verifikasi passage/tabel primer, pencarian paper baru, audit retraction, atau pemeriksaan metadata daring. Riwayat pengecekan PDF dalam catatan lama tidak sama dengan human verification vault ini. Karena itu registry awal memakai `bibliography_checked: false`, `read_scope: local_note`, dan seluruh evidence checks candidate false.

Satu lead `LEAD-SAL-NUTRIENTS-001` merujuk section catatan tiga paper. `finding`, outcome, angka dan durasi tetap kosong. Lead memberi jalur penelusuran tanpa memasukkan klaim numerik atau temuan biologis yang belum diperiksa. Scope B0 tidak mengesahkan kontrak assessment packet Track A, integrasi iOS, atau prediksi ice-ice.

B1 berikutnya perlu memverifikasi bibliografi dan akses full text, merekonsiliasi ID/duplikat, lalu memilih 5–8 studi relevan. B2 mengekstrak kandidat; B3 memerlukan reviewer manusia. Ketiadaan klaim verified saat ini adalah status corpus, bukan simpulan bahwa literatur tidak memiliki bukti.
