# Protokol review dan verifikasi bukti

## Alur status

`candidate → extracted → needs_review → verified / rejected / superseded`

`extracted` menyatakan satu klaim sudah ditranskripsikan; AI boleh menyiapkannya, lalu menyerahkannya sebagai `needs_review`. AI tidak boleh menyetujui bukti sendiri. Hanya manusia yang memeriksa sumber dapat membuat event `verified`. Setiap perubahan status dicatat pada `review_history` dengan actor, jenis actor, timestamp ISO 8601 berzona, dan alasan. Event terakhir harus cocok dengan status entri; waktu harus berurutan.

Transisi koreksi: `rejected → needs_review`; `verified → needs_review` untuk pencabutan sementara; `verified → superseded` untuk penggantian; `superseded` terminal. Pada penarikan/penggantian, metadata review terdahulu tetap dipertahankan dan event baru menjelaskan alasan. Setelah koreksi, verifikasi baru harus melewati reviewer dan pemeriksaan ulang. Validator tidak mengizinkan lompatan `candidate → verified`. Sumber dan klaim memiliki ID berbeda; sumber tidak mengikuti status klaim ini.

## Sumber, kutipan dan akses

1. Registrasikan sumber primer/review sekali. Cocokkan judul, penulis, tahun, DOI/URL dengan penerbit atau rekaman bibliografi; isi `bibliography_checked` hanya setelah pemeriksaan nyata. Normalisasi DOI huruf kecil dan tanpa awalan URL. Jangan memakai sitasi buatan model sebagai sumber.
2. Rekonsiliasi DOI/checksum dan ID lama sebelum ekstraksi. S13/S14 dalam matriks disebut duplikat; P24/W04 disebut studi yang sama. Itu petunjuk rekonsiliasi, belum audit ulang B0. Catatan internal adalah sumber sekunder, bukan pengganti paper.
3. Rekam akses dan cakupan pembacaan secara jujur. `full_text_available` hanya menyatakan akses; `selected_full_text`/`full_text` menyatakan yang dibaca. Abstrak saja tetap unverified untuk vault produksi ini. Jangan mengaku membaca full text dari ringkasan, cuplikan mesin pencari atau transkrip.
4. Gunakan locator tepat: nomor halaman PDF (bedakan dari halaman jurnal), section, tabel, figure atau paragraf. Sertakan judul tabel/panel atau uraian pembanding bila nomor saja ambigu. Kutipan pendek opsional harus verbatim dan diperiksa; maksimal 600 karakter di schema bukan izin menyalin sebanyak itu dari setiap sumber. Utamakan parafrasa dan taati hak akses/hak cipta.
5. Simpan metadata, checksum, referensi dan cuplikan secukupnya. PDF asli tetap di base sumber; jangan salin full text berhak cipta ke repo distribusi. Root base diatur secara lokal; path provenance selalu relatif tanpa `..`.

## Checklist manusia sebelum verified

- Cocokkan satu klaim dengan passage/tabel/figure yang diakses langsung; cek apakah hasil milik paper ini atau sekadar kutipan studi lain.
- Periksa spesies asli, strain, lokasi, tahap hidup, setting, desain/pembanding, aklimasi, paparan, durasi, n dan unit replikasi. Yang tidak dilaporkan tetap null dan dijelaskan di `unknown_fields`/limitations.
- Periksa angka, satuan, analit dan basis (NO3 vs N, PO4 vs P, definisi salinitas), tanda < / batas deteksi, mean/SD/SE dan durasi. Satuan tidak jelas tidak boleh dilengkapi dengan tebakan; batasi klaim atau tahan review jika maknanya bergantung pada unit itu.
- Periksa endpoint, arah efek, p-value, uncertainty, hasil nol/tidak signifikan dan inkonsistensi tabel–narasi. Jangan membuat p-value atau menganggap tidak dilaporkan sebagai tidak signifikan.
- Batasi interpretasi pada desain. Interaksi langsung memerlukan uji yang mendukungnya; paparan confounded tidak mengisolasi sebab. Korelasi tidak otomatis kausal; gejala, stres, penyakit dan prediksi masa depan tetap terpisah.
- Isi keterbatasan dan applicability, termasuk beda spesies/setting/durasi/lokasi dari Tidung. Pertahankan konflik lintas studi; jangan buat konsensus atau cutoff universal.
- Isi `verification.verified_by` (ID reviewer manusia yang stabil), `verified_at`, `reviewer_type: human`, seluruh enam checks bernilai true dan `review_notes` spesifik. Event verified harus memakai reviewer/tanggal yang sama.

Untuk verified, validator juga mewajibkan sumber primer/review, bibliografi diperiksa, full text tersedia dan minimal bagian full text dibaca; catatan internal, interview serta proposal engineering tidak dapat dipromosikan ke bukti ilmiah produksi. Sumber duplikat harus diarahkan ke sumber kanonis sebelum promosi.

## Penolakan, konflik dan revisi

Tolak bila tidak ada dukungan, bahasa kausal melampaui desain, ambang diada-adakan, unit/konteks penting tidak dapat diperiksa, atau generalisasi lintas spesies disajikan sebagai fakta. Catat alasan di event dan `review_notes`. Gunakan `needs_review` untuk masalah yang masih bisa diperbaiki. Entri superseded tetap tersimpan dan ditautkan oleh entri pengganti; jangan hapus jejak klaim lama.

Konflik yang sah tidak menuntut penolakan salah satu paper. Buat dua entri atomik dan relasi `contradicts`/`different_context`, dengan alasan serta konteks masing-masing. Review yang mengulang paper primer tidak dihitung sebagai replikasi.

## Batas pemeriksaan otomatis

Jalankan validator dan tests sebelum commit. Schema menolak verified tanpa locator, reviewer/tanggal, atau checklist lengkap; validator corpus memeriksa referensi, kronologi/transisi, metadata akses, konsistensi dasar dan duplikat. Pemeriksaan ini **tidak mengautentikasi reviewer atau membuktikan kutipan benar**, dan tidak menilai semua makna ilmiah. Fixture verified hanya data sintetis di memori test; tidak dimasukkan ke vault.

Retrieval produksi pada B4 hanya boleh memakai verified dan harus menyertakan keterbatasan serta konflik material. Status verified sendiri tidak memberi otorisasi untuk diagnosis, persentase probabilitas penyakit, dosing nutrisi, cutoff universal atau tindakan otomatis. Perubahan parameter engineering tetap diberi label usulan.

## Memasukkan base tambahan kelak

Catat `base_id` stabil, path relatif, SHA-256, versi/commit jika ada, status working tree dan waktu capture. Baca kebijakan akses base, deduplikasi sumber, verifikasi bibliografi/akses, lalu buat candidate; tidak ada status verified yang diwarisi otomatis. Petakan ID lama melalui `legacy_ids`. Jika metadata/konteks berubah, rekam revisi dan review ulang; jangan memulihkan snapshot lama atau mengubah sumber asli. B0 tidak menjadwalkan ingestion otomatis.
