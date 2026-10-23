---
type: engineering-handover
project: "[[Challenge Final]]"
created: 2026-10-22
updated: 2026-10-22
status: implemented-provider-partial
tags: [challenge-final, seagis, engineering, a2]
source_commit: 24742513987227968228c54c1898d4c6d6dc54b2
---

# A2 — Operasi ingestion lingkungan

Semua command dijalankan di `/Users/cindyram/Documents/Apple/Seagis-Model`.

## Setup dan command

```sh
uv sync --frozen --group environment
uv run --frozen --group environment python scripts/deploy_a2.py --apply
uv run --frozen --group environment python scripts/ingest_environment.py run
uv run --frozen --group environment python scripts/ingest_environment.py status
uv run --frozen --group environment python scripts/ingest_environment.py preview --plot a
uv run --frozen --group environment python scripts/ingest_environment.py preview --plot b
```

Deployment memakai PAT lokal Supabase CLI, memverifikasi project `kibztbeviortyvbedogg` di org Seagis, mempertahankan source/identity semua migrasi, lalu membuat restricted login A2. Runtime tidak membutuhkan PAT. `.env.a2.worker` diabaikan Git dan dibuat mode 0600. CA publik tersimpan di `data/a2/supabase-ca.crt`, diverifikasi SHA-256 setiap koneksi; jangan memakai `sslmode=require` tanpa verifikasi sertifikat.

Copernicus memakai login Toolbox lokal yang sudah ada. Pada mesin baru:

```sh
uv run --frozen --group environment copernicusmarine login
```

Masukkan username/password di prompt terminal, bukan command, chat, repo, atau vault. Workflow ini memakai Toolbox 2.5.0 dan dependency lock repo. Open-Meteo gratis tidak membutuhkan API key dalam mode prototipe pendidikan nonkomersial. Untuk produk/aktivitas komersial, ubah konfigurasi akses dan policy sesudah entitlement yang sesuai tersedia; worker sekarang sengaja hanya menerima purpose nonkomersial tersebut.

## Jadwal dan pemulihan

Dispatcher dapat berjalan tiap 15 menit, tetapi **fetch provider hanya jika due**. Waktu UTC di bawah adalah slot operasional dengan grace period; bukan bukti issue time sebuah respons.

| Sumber | Fetch nominal UTC | WIB | Stale limit vintage |
|---|---|---|---|
| PHY salinity/currents | 08:30 harian | 15:30 | 48 jam |
| BGC nutrients | 12:30 harian | 19:30 | 48 jam |
| GFS | 04:30, 10:30, 16:30, 22:30 | 11:30, 17:30, 23:30, 05:30 hari berikut | 12 jam |

Refresh pertama dapat dilakukan sebelum slot, kemudian state DB menentukan slot berikutnya. Cadence sampel 6 jam / daily / hourly berbeda dari frekuensi publikasi. Lease 20 menit mencegah dua worker mengambil dataset yang sama bersamaan. Retry network/429/5xx maksimum tiga percobaan dengan jitter/backoff. `Retry-After` detik maupun HTTP-date dihormati; jeda panjang dikembalikan ke scheduler. Error autentikasi, unit/metadata, lisensi, atau dataset yang sedang diperbarui tidak diulang langsung. `provider_updating` berarti safeguard Toolbox menghentikan subset yang masih dalam area pembaruan, bukan token gagal atau nilai hilang yang boleh diganti nol. Kegagalan persisten menaikkan backoff 15 menit sampai empat jam; vintage terakhir tetap ada dan tidak diberi waktu baru.

Jika proses mati, lease menjadi dapat diklaim kembali setelah 20 menit; attempt lama diberi status abandoned. Periksa `status` sebelum retry. Untuk refresh manual yang disengaja:

```sh
uv run --frozen --group environment python scripts/ingest_environment.py run --dataset open_meteo_gfs --force
```

`--force` melewati waktu due, tetap menghormati lease aktif. Hindari loop force karena provider punya batas akses. Dispatcher mengisolasi kegagalan per dataset: sumber lain tetap diproses. Tidak ada penggantian sumber/model atau nilai nol saat provider gagal.

## Scheduler lokal macOS

```sh
uv run --frozen --group environment python scripts/install_a2_scheduler.py install
launchctl print "gui/$(id -u)/org.seagis.environment-ingestion"
```

LaunchAgent memanggil Python di `.venv` setiap 15 menit dan saat load, membatasi satu tick 15 menit, serta menyimpan log tersanitasi pada `data/a2/worker.log` dengan satu rotasi sekitar 2 MB. Definisi plist berada di `~/Library/LaunchAgents/org.seagis.environment-ingestion.plist`, tanpa secrets. Worker membaca credential lokal saat diperlukan.

**Scheduler lokal hanya berjalan ketika Mac aktif dan user login.** Tidur/offline dapat membuat slot terlewat; tick setelah bangun mengambil window terbaru, bukan mengklaim menangkap seluruh vintage yang terlewat. Tidak ada worker cloud 24/7 yang disediakan oleh LaunchAgent. Migrasikan runner yang sama ke host selalu aktif dengan credentials khusus bila dibutuhkan; jangan upload PAT administrasi ke runtime.

Menghentikan scheduler tanpa menghapus data:

```sh
uv run --frozen --group environment python scripts/install_a2_scheduler.py remove
```

## Monitoring dan handover

`status` menampilkan last attempt/success, failure count, next attempt, lease, latest vintage, grid/value/demo-mapping counts, attribution, license, retention dan availability. Jadikan `unavailable` atau `stale_unusable` sebagai data tidak dapat dipakai; `cached_after_failure` tetap harus ditampilkan sebagai cached beserta umur aslinya. Tidak ada sistem notifikasi eksternal otomatis pada A2.

Tabel `seagis_environment.attempt` mencatat sukses, duplicate, failed, abandoned. SQL admin untuk inspection hanya melalui akses operator Seagis; worker tidak dapat SELECT tabel langsung. Logs tidak menyimpan token, password, DSN, raw respons atau exception pihak ketiga. Untuk error, tampilkan hanya kode. Jika acknowledgement commit hilang, periksa status/run ID sebelum mengulang; run key dedup menjaga transaksi ulang.

A2 tidak menambah/menjalankan suite tests pada sesi ini. Bukti yang dicatat adalah penerapan migrasi, lint, operasi fetch/persist dan inspeksi hasil. Regresi penuh A0/A1 dan failure-injection suite belum dijalankan ulang untuk migrasi A2.


## Provenance salinan

Sumber: [operations.md](/Users/cindyram/Documents/Apple/Seagis-Model/docs/a2/operations.md), commit `2474251`. Salinan catatan lengkap dengan tautan lokal yang disesuaikan. [[Provenance A2 - Paket Engineering 22 Oktober 2026]] · [[Indeks - Engineering]].
