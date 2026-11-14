---
type: engineering-design
project: "[[Challenge Final]]"
created: 2026-10-28
status: draft-perlu-review-backend
source: lampiran transfer knowledge hub IoT 28 Oktober 2026
tags: [challenge-final, seagis, engineering, a1, iot]
---

# Rancangan kontrak dan migrasi hub IoT

**Status: usulan untuk disepakati, bukan implementasi atau migrasi yang sudah diterapkan.** Sumbernya dokumen transfer knowledge yang diberikan pengguna; firmware dan server tiruan hanya teruji dalam simulasi. Snapshot backend lokal `Seagis-Model` yang diperiksa adalah `291b6c5`, migrasi 0001–0005; bukan bukti versi cloud saat ini. [[Handover A1 - Arsitektur Data dan Akses IoT]] menjelaskan endpoint lama. Pastikan source terbaru dan schema deployment sebelum menulis migrasi.

## Keputusan yang harus ditutup bersama backend dan firmware

| Keputusan | Usulan untuk review | Konsekuensi / batas |
| --- | --- | --- |
| Retensi raw nyata | Tentukan tujuan, lokasi, enkripsi/akses, lama retensi dan penghapusan sebelum mengaktifkan data nyata. Simulasi dapat menyimpan JSON yang diizinkan policy sekarang. | Constraint `raw_payload_inline_synthetic_v2` melarang inline non-sintetis. Hash saja tidak memenuhi syarat simpan isi mentah. Jangan melonggarkan constraint tanpa keputusan. |
| Kredensial | Identitas hub terikat ke deployment, mapping node ke sensor dan dataset; gunakan token opaque, expiry dan revocation. | Tinjau apakah perlu kind baru atau perluasan device; `node_id` tidak boleh memilih sensor di luar mapping token. |
| `delayed_packet` | Awal 108000 detik sebagai flag transport terpisah dari status observasi; putuskan apakah juga `suspect`. | Pertahankan semantik API lama dan provenance versi policy. Jangan mengubah 7200 detik global tanpa memeriksa konsumen. |
| `hub_rx` | Simpan estimasi dengan `time_basis` dan tandai waktu ukur tidak diketahui; keluarkan dari ΔT/variabilitas default sampai aturan disepakati. | `observed_at` pada basis ini waktu terima, bukan waktu ukur sebenarnya. |
| Gap | Simpan gap hub; hasil pengecekan jadwal server terpisah beserta sumber dan versi jadwal. | Hindari menghitung satu slot dua kali; jangan menyimpulkan penyebab node/hub tanpa bukti. |
| `no_news` | Hitung saat status dibaca dari jadwal 06:00 WIB dan batas 10:00 WIB, dengan `checked_at` dan waktu unggahan terakhir. | Tentukan apa yang berarti unggahan berhasil: satu chunk membuktikan kontak, tetapi tidak membuktikan seluruh backlog selesai. Laporkan dua hal terpisah; protokol saat ini tidak menyatakan akhir batch harian. |
| Notifikasi | Di luar PoC; tentukan penerima dan otorisasi nanti. | Polling status tidak mengirim alarm di luar jadwal hub. |

Usulan di atas bukan persetujuan operasional. Nilai ambang tegangan/sinyal dalam lampiran adalah placeholder engineering, bukan kalibrasi hardware atau ambang biologis.

## Kontrak ingest untuk review

`POST /functions/v1/temperature/v1/hub/ingest`, `Authorization: Bearer sgi_…`, `Content-Type: application/json`, batas body **8192 byte UTF-8**. `schema_version=2.0.0`, `batch_id` string echo, `sent_at`, `hub` dan `records` seperti contoh lampiran. Tiap request berdiri sendiri; format satu record per baris hanyalah format serialisasi, bukan persyaratan JSON. Pembatasan diukur dari byte body aktual, bukan jumlah karakter atau jumlah record perkiraan.

Waktu UTC `Z`: simpan `observed_at`, `received_at`, `sent_at`, `ingested_at` terpisah; untuk record tak berwaktu firmware menahannya di microSD. `time_basis=node_age` menggunakan umur node, sedangkan `hub_rx` hanya proksi yang dapat lebih lambat. `hub_boot`, `time_base`, versi build dan konfigurasi perlu disimpan sebagai metadata request untuk lineage. Waktu jaringan, drift dan konsistensi timestamp setelah reboot belum diuji fisik.

### Identitas dan hasil per record

| Jenis | Identitas yang diusulkan, dalam lingkup deployment hub | Hasil |
| --- | --- | --- |
| `obs`, `node_status` | sensor terpetakan + `boot_id` + `sequence` dalam satu namespace | Semantik sama: duplikat; beda: `packet_conflict`, simpan bukti dan jangan timpa. |
| `gap` | sensor + `slot_start` + sumber | Catat alasan dan perbedaan hasil hub/server. |
| `event` | hub + `code` + `at` + `hub_boot` | Risiko dua event identik pada detik yang sama perlu dievaluasi firmware. |
| `hub_health` | hub + `at` + `hub_boot` | Simpan snapshot, termasuk null sebagai tidak diketahui. |
| jenis asing / record tak valid | referensi request + indeks record | Simpan untuk karantina; bukan observasi palsu. |

Identitas harus stabil lintas retry **dan** penggantian token. Uji reset/persistensi `boot_id` dan `hub_boot`, pergantian alat, counter overflow dan tabrakan sebelum deployment. `batch_id` offset log bukan kunci dedup. Tentukan kanonisasi hash semantik dan field mana yang dipakai, termasuk health dan metadata waktu; perubahan RSSI/health pada replay dapat menyebabkan konflik bila firmware tidak membekukannya. Kunci + hash dan penyimpanan harus aman saat request paralel.

### Transaksi, respons dan kegagalan

1. Autentikasi dan validasi batas request/schema, lalu simpan isi yang dapat dipulihkan sesuai policy retensi **sebelum** memproses record; validasi JSON tingkat request tetap diperlukan. Raw byte persis dan JSONB berbeda; tentukan hash dan formatnya. Body invalid boleh ditolak tanpa kewajiban retensi.
2. Dalam transaksi yang membuat respons sukses, catat hasil seluruh record: diterima, duplikat, konflik, karantina atau tipe asing. Gunakan isolasi kegagalan per record agar record janggal tidak membatalkan lainnya. Bila penyimpanan raw atau hasil belum durable, rollback/kembalikan 5xx agar hub retry.
3. Balas 200/201 hanya setelah commit: `{"code":"stored","batch_id":"<echo>","received":<n>,"duplicates":<d>}`. Usulan `received` = panjang array input dan `duplicates` = jumlah duplikat di dalamnya, termasuk retry; konflik/karantina tetap tercakup di `received`. **Konfirmasi semantik angka dengan firmware**, karena contoh belum mendefinisikannya secara eksplisit. Echo persis tipe dan nilai `batch_id`.
4. 401 untuk token tidak sah; 400/413/415 untuk kesalahan request; 429/5xx untuk gangguan sementara. Firmware akan melewati chunk setelah tiga 4xx selain 401, sehingga semantik 403/422 dan schema tidak dikenal perlu disepakati sebelum uji. Jangan keluarkan 4xx karena satu record.

Karantina yang di-ACK harus dapat ditelusuri dan ditindaklanjuti operator, termasuk record indeks, alasan aman, request, waktu dan penyelesaian. ACK berarti server menerima tanggung jawab atas record, bukan bahwa data telah lolos QC. Jangan menyimpan token pada log.

## Rancangan migrasi bertahap

**Rancangan saja; tidak ada SQL siap eksekusi.** Nama dan constraint final bergantung pada keputusan di atas dan source backend yang diperbarui.

1. **Identitas dan akses:** perluas credential atau buat identitas hub dan tabel mapping deployment–node–sensor dengan FK, keunikan temporal yang mencegah dua mapping aktif, pemisahan sintetis/nyata dan revocation. Hak reader dibatasi plot yang diizinkan; pastikan status hub bersama tidak membocorkan node/plot lain.
2. **Penerimaan batch:** tabel receipt request berisi ID, hub, hash wire, ukuran, waktu server/sent, firmware/config dan referensi raw; tabel hasil/karantina per indeks untuk record yang tidak dapat dipetakan. Perhatikan model `raw_payload` sekarang terikat `ingestion_run` dan dataset, sedangkan satu batch dapat berisi beberapa sensor dan record hub: tentukan relasi batch ke raw dan observasi, jangan memaksakan FK yang keliru.
3. **Dedup dan telemetri:** receipt dengan unique key dan semantic digest dalam namespace yang sesuai; tabel health node, health hub, event dan gap append-only, dengan FK lineage batch dan identitas server. Periksa lifetime key dan konflik secara atomik. Simpan flags mentah dan nilai nullable.
4. **Policy berversi:** pisahkan threshold delivery dan kesegaran status. Simpan versi yang benar-benar dipakai pada hasil QC/label dan histori policy yang tidak ditimpa; singleton `temperature_policy` saat ini sendiri tidak menyimpan histori. Pertahankan kompatibilitas `/v1/ingest` dan `/v1/status` lama sampai migrasi konsumen disepakati.
5. **Runtime:** batasi direct table access; gunakan RLS, fungsi `SECURITY DEFINER` dengan `search_path` aman, izin minimal dan guard konsisten dengan 0001–0005. Review domain synthetic, constraint raw dan real-ingestion gate pada seluruh jalur baru, termasuk record non-observasi. Ukur batas transaksi dan rate limit pada ukuran maksimum.
6. **Rollout:** migrasi dan uji database lokal/terisolasi dahulu; deployment dan commissioning dikerjakan setelah review, kebijakan retensi dan kesiapan hardware. Sediakan rollback yang tidak menghapus raw/observasi yang sudah diterima.

## Status untuk aplikasi

Tambahkan `checked_at`, versi policy, hub dan node yang berhak diakses, label dan `reasons` berupa kode stabil. `unknown` bila belum ada data; setelah melewati tenggat tanpa kontak yang cukup, `no_news` mengutamakan fakta bahwa kondisi kini tidak diketahui. Baterai, gap dan nilai health terakhir tetap boleh ditampilkan dengan waktu pengamatannya, bukan sebagai kondisi kini. Bedakan `last_contact_at` dari kelengkapan backlog dan `last_valid_observed_at`; hasil keterlambatan satu hari bukan indikator kerusakan.

Tentukan definisi record valid, urutan label, penanganan counter kumulatif per boot, gap berulang, reset dan null sebelum implementasi. Hitungan reboot 24 jam butuh event/identitas yang cukup; `reset_reason` berulang pada setiap paket tidak berarti banyak reboot. `untimed_skipped` dan `skipped_chunks` persisten membutuhkan mekanisme penyelesaian agar label tidak selamanya warn. Tanpa jadwal aktif/timezone dan first deployment time yang jelas, `no_news` tidak bisa dihitung dengan aman.

## Acceptance tests sebelum integrasi

- [ ] Payload contoh firmware dan batas 8192/8193 byte; header, schema, JSON dan batch kosong; respons cocok dengan parser firmware.
- [ ] Dua node, `obs`/`node_status` berbagi sequence, retry sesudah commit dan respons hilang, retry konkuren, perubahan isi dengan key sama, record rusak dan tipe asing; tidak ada hilang atau observasi ganda.
- [ ] Campuran record valid/tidak valid dan kegagalan penyimpanan: 200 hanya setelah semua hasil durable; raw dan karantina dapat ditelusuri sesuai retensi yang disetujui.
- [ ] Token salah/kedaluwarsa/dicabut, mapping lintas hub/plot, rate limit, synthetic versus real disabled; tidak ada akses lintas tenant/plot.
- [ ] Jadwal 06:00/09:00/10:00 WIB, tidak ada riwayat, chunk parsial, backfill 24–30 jam, data lama dan `hub_rx`; status kontak terpisah dari kesegaran pengukuran.
- [ ] Urutan kedatangan terbalik, missing/rapid change, gap hub dan server, reboot, counter persisten dan null; policy dan asal waktu dapat diaudit.
- [ ] Uji perangkat nyata terpisah: clock NITZ/drift, TLS dengan validasi hostname/SNI, penyimpanan, LoRa, probe dan daya; belum dibuktikan simulator.

## Handoff

Backend dan firmware perlu menutup tabel keputusan, memastikan parser respons dan identitas persistennya, serta menyediakan checkout source terkini dan lingkungan uji. Setelah itu buat migrasi executable, endpoint dan contract tests; jangan mengaktifkan ingestion nyata berdasarkan dokumen ini. [[Operasi A1 - Simulator dan Credentials]] dan [[Peta Database Supabase Seagis]] adalah referensi snapshot pendukung.
