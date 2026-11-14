# Uji SST hourly — paket reproduksi

Paket ini menguji **Copernicus aktual → subset terverifikasi → cache JSON lokal → HTTP loopback → klien Swift**. Ini bukan endpoint Seagis produksi, bukan aplikasi iOS yang sudah terintegrasi, dan bukan scheduler yang sudah dipasang.

Titik utama: `tidung-besar-reference`, **-5.8211, 106.5522**, diberikan pengguna 10 November 2026 sebagai referensi Pulau Tidung Besar. Ini belum koordinat farm/sensor. Dua titik contoh dari `config/a2_sources.json` disertakan sebagai pembanding dengan status asal tetap dipertahankan. Ketiga titik bukan tiga farm yang telah diverifikasi.

## Prasyarat

- Python dengan `copernicusmarine==2.5.0`, NumPy dan xarray. Pada mesin audit tersedia di `/Users/cindyram/Documents/Apple/Copernicus/.venv/bin/python`.
- Login Copernicus Marine Toolbox pada mesin operator. Gunakan prompt `copernicusmarine login`; jangan memasukkan password dalam kode/command yang disimpan.
- Swift compiler dengan Foundation/URLSession. Audit menggunakan Swift 6.4.2 pada macOS, bukan build Xcode iOS.
- Akses jaringan ke Copernicus. Semua akses provider read-only; server lokal hanya bind `127.0.0.1`.

## Jalankan ulang

Jalankan dari direktori paket ini. Gunakan folder output baru agar bukti bertanggal di `evidence/` tetap bisa dirujuk.

```sh
/Users/cindyram/Documents/Apple/Copernicus/.venv/bin/python audit_sst.py fetch --output /private/tmp/seagis-sst-run
/Users/cindyram/Documents/Apple/Copernicus/.venv/bin/python audit_sst.py fetch --output /private/tmp/seagis-sst-run
/Users/cindyram/Documents/Apple/Copernicus/.venv/bin/python -m unittest -v test_audit_sst.py
swiftc -parse-as-library -module-cache-path /private/tmp/sst-swift-module-cache AppProbe.swift -o /private/tmp/seagis-sst-app-probe
python3 audit_sst.py serve --output /private/tmp/seagis-sst-run --port 8876
```

Saat server berjalan, dari terminal lain:

```sh
/private/tmp/seagis-sst-app-probe http://127.0.0.1:8876/v1/plots/tidung-besar-reference/sst tidung-besar-reference
```

Hentikan server dengan Ctrl-C. Kredensial Copernicus hanya digunakan Python operator, tidak dikirim ke Swift. Untuk server produksi dibutuhkan HTTPS dan autentikasi/scope app; server lokal ini sengaja hanya untuk audit.

## Makna kontrak probe

- Dataset `cmems_mod_glo_phy_anfc_0.083deg_PT1H-m`, versi `202406`, variabel `thetao`: **potential temperature** lapisan nominal sekitar 0,494 m, mean per jam. Bukan rekaman probe farm atau observasi SST satelit murni.
- Unit native `degrees_C` dipetakan secara notasi ke `degC`, tanpa mengurangi 273,15.
- Window fetch: kemarin 00:00 sampai lusa 23:00 UTC, 96 timestamp native. Tidak membuat 24 jam dari satu nilai harian.
- `provider_updated_at` berasal dari metadata katalog, **bukan forecast issue time**. `issued_at=null` karena vintage model aslinya tidak dibuktikan oleh metadata itu.
- `last_checked_at` = akhir fetch sukses. `content_revision` = SHA-256 JSON canonical hasil subset, bukan hash byte transfer jaringan. Fetch identik mempertahankan `content_first_seen_at`.
- Endpoint memilih `current` menurut jam UTC berjalan, bukan timestamp forecast paling jauh. `rows` tetap memuat window lengkap untuk history/forecast dengan label regional.
- `temporal_status` memakai ketersediaan nilai jam berjalan dan umur update katalog ≤48 jam. Ini **policy engineering pilot**, bukan jaminan freshness forecast atau ambang biologis. Waktu update tidak diketahui/di masa depan ditolak.
- `spatial_support=unverified` dan `farm_fallback_authorized=false` selalu: angka valid pada cell belum membuktikan suhu farm.
- Null dipertahankan; tidak diganti nol. Jika metadata/cadence berubah, fetch gagal sebelum cache terakhir diganti. Penggantian snapshot utama atomik. Script harus dijalankan satu worker saja; belum ada distributed lock atau retry produksi.

## Fetch per jam

Fungsi `due` dan pengujian menguji interval 3600 detik, termasuk penggunaan pertama dan clock rollback. **Script tidak memasang timer/scheduler.** Dua fetch live berjarak pendek menguji konsistensi subset; pergantian jam diuji dengan clock fixture. Ini bukan soak test 24 jam.

Rancangan operasional: worker backend mengambil/memeriksa provider setiap jam, menyimpan hasil/revisi dan last-attempt/last-success secara terpisah, lalu endpoint app menyajikan nilai untuk jam berjalan dari cache. Banyak plot pada cell sama dapat berbagi data. App fetch saat dibuka/resume, setiap jam selama aktif, dan background refresh best effort. iOS tidak menjamin interval background tepat satu jam.

## Bukti

- `evidence/audit.json`: fetch utama, valid counts, cell, rentang nilai, durasi subset.
- `evidence/repeat-check.json`: fetch ulang dan deteksi perubahan konten.
- `evidence/catalog-before.json` / `catalog-after.json`: metadata provider dan pemeriksaan stabilitas selama fetch terakhir.
- `evidence/snapshot.json` / `hourly.csv`: hasil nyata, bukan fixture sintetis.
- `evidence/swift-probe.json`: hasil HTTP + decoding untuk tiap titik.
- `test_audit_sst.py`: fixture sintetis khusus pengujian perilaku gagal/refresh, tidak menjadi data lapangan.

Atribusi: E.U. Copernicus Marine Service Information / Mercator Ocean International. [Produk](https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_PHY_001_024/description), [akses dataset](https://data.marine.copernicus.eu/product/GLOBAL_ANALYSISFORECAST_PHY_001_024/services), [lisensi](https://marine.copernicus.eu/user-corner/service-commitments-and-licence). Pedoman background iOS: [Apple](https://developer.apple.com/documentation/backgroundtasks/choosing-background-strategies-for-your-app).
