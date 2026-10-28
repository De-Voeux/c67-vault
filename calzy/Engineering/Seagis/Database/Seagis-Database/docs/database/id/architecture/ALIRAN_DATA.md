# ALIRAN_DATA

Version: 1.0.0 | Date: 2026-10-27

[Dokumen lengkap](../DOKUMENTASI_DATABASE.md) | [README](../../README.md)

PostgreSQL/Supabase adalah persistence backend yang didefinisikan kode. Schema `seagis` berisi registri, observasi, forecast dan provenance; `seagis_raw` menyimpan manifest raw; `seagis_api` membatasi IoT gateway; `seagis_environment` mengatur worker regional; `seagis_quality` menyimpan review QC; `seagis_features` menyediakan container fitur yang belum dihubungkan ke builder produksi. Schema internal Supabase seperti auth/storage tidak diinventaris sebagai milik aplikasi: akses catalog terkini tidak tersedia dan tidak boleh diasumsikan kosong.

Python melakukan pengambilan provider di luar database. Worker A2/A3 memanggil stored function lewat psycopg; TS handler memanggil hanya fungsi ingest/history/status. Tidak ada ORM yang ditemukan pada jalur ini. Transaksi mutasi berada di fungsi SQL; claim fetch merupakan transaksi terpisah dari persistence agar panggilan jaringan tidak menahan transaksi database.

Diagram memperlihatkan dua komponen yang terputus: mock iOS tidak memiliki edge ke backend. Integrasi masa depan tetap UNVERIFIED. Core ML, cache terdistribusi, warehouse, queue dan search index produksi NOT FOUND dalam file implementasi yang diinspeksi; ini bukan bukti bahwa layanan di luar checkout tidak ada.

Diagram reproduktif: `assets/diagrams/architecture.mmd`.


```mermaid
flowchart TD
    sensor["IoT / simulator"]
    edge["temperature handler"]
    sql["PostgreSQL / 6 schemas"]
    providers["Copernicus + Open-Meteo"]
    a2["A2 adapters + leases"]
    a3["A3 quality / alignment"]
    csv["CSV experiments"]
    ios["iOS synthetic mock"]
    sensor --> edge
    edge --> sql
    providers --> a2
    a2 --> sql
    sql --> a3
    a3 --> csv
```

Diagram reproduktif: `assets/diagrams/lineage.mmd`.


```mermaid
flowchart TD
    registry["source + dataset_parameter"]
    raw["ingestion_run + raw_payload"]
    obs["observation"]
    run["forecast_run + forecast_value"]
    map["source_grid + mappings"]
    bundle["source_bundle"]
    align["alignment_snapshot + snapshot_input"]
    registry --> raw
    raw --> obs
    raw --> run
    map --> run
    obs --> bundle
    run --> bundle
    bundle --> align
```

