# SIKLUS_HIDUP_DATA

Version: 1.0.0 | Date: 2026-10-27

[Dokumen lengkap](../DOKUMENTASI_DATABASE.md) | [README](../../README.md)

Pembuatan: UUID disediakan oleh caller/SQL sesuai dictionary; natural keys registry dipin seed/config. Raw, measurement, forecast, QC dan snapshot memiliki trigger pembatas mutasi. Dataset hanya dapat mengubah gate operasional tertentu; identitas dataset, parameter dan grid harus diberi versi baru bila semantiknya berubah. Sensor deployment baru diperlukan untuk perubahan lokasi/kedalaman; active dapat dinonaktifkan.

Ingestion berubah running → succeeded/failed/partial sesuai CHECK dan guard. Attempt regional berubah running → succeeded/duplicate/failed/abandoned. expired lease ditandai abandoned pada claim berikutnya. Feature snapshot berubah draft → sealed; manifest input harus cocok dan row lock induk mencegah race saat sealing. Snapshot A3 langsung immutable setelah insert. Credential dicabut dengan revoked_at atau habis lewat expires_at; ini bukan penghapusan observasi.

A0 awalnya memperbolehkan penutupan effective_until pada mapping. Migrasi 0005 menambah recorded_at dan trigger immutable_alignment_mapping sebelum UPDATE/DELETE. Karena itu instruksi lama untuk menutup mapping dengan UPDATE tidak lagi berlaku pada migrasi lengkap. Resolusi rentang baru harus dirancang tanpa menghapus histori atau melewati trigger secara diam-diam.

Tidak ditemukan job cleanup/retensi berbasis umur, soft delete umum, backup/restore teruji, replikasi lintas DB atau sinkronisasi iOS-cloud. A2 metadata_only adalah kebijakan konten raw, bukan TTL semua tabel. FK tanpa ON DELETE/UPDATE eksplisit memakai NO ACTION; tidak ada cascade delete yang boleh diasumsikan. Prototype FarmStore menghapus farmer beserta plot di memori; ini tidak menjalankan DELETE SQL backend.

Migrasi 0001 initial, 0002 temperature API, 0003 regional ingestion, 0004 provider_updating, 0005 quality alignment. SQL merupakan migrasi maju; rollback/down script NOT FOUND. Deploy scripts memakai administrator untuk provisioning dan memasang worker role; tidak dijalankan pada audit ini. Adopsi migrasi perlu backup, uji schema kosong dan uji upgrade; hal tersebut rekomendasi, bukan hasil pengujian sesi ini.

Keamanan: migration mengaktifkan RLS tabel aplikasi; FORCE RLS=false pada snapshot lama. PUBLIC/anon/authenticated dibatasi, gateway dan worker mendapat EXECUTE fungsi tertentu dengan SECURITY DEFINER serta search_path=pg_catalog. A2/A3 memakai TLS verify-full dan CA hash dipin. Token asli tidak dicetak; credential menyimpan hash. Hak administrator, role membership aktif, bucket policy, encryption-at-rest, rotasi aktual, backup dan recovery produksi UNVERIFIED. Rate-limit log, attempt, QC event dan hash menyediakan audit parsial; tidak ditemukan dead-letter queue atau alerting eksternal terkonfigurasi pada jalur ini.

Bukti implementasi utama: `Seagis-Model/supabase/migrations/0001_initial_schema.sql:1`; `Seagis-Model/supabase/migrations/0002_temperature_api.sql:1`; `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:1`; `Seagis-Model/supabase/migrations/0004_provider_update_status.sql:1`; `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:1`.

Bukti implementasi utama: `Seagis-Model/scripts/environmental/store.py:1`; `Seagis-Model/scripts/quality/store.py:1`; `Seagis-Model/supabase/functions/temperature/connection.ts:1`.

