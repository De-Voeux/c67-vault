---
type: engineering-handover
project: "[[Challenge Final]]"
created: 2026-10-22
updated: 2026-10-22
status: implemented-provider-partial
tags: [challenge-final, seagis, engineering, a2]
source_commit: 24742513987227968228c54c1898d4c6d6dc54b2
---

# A2 — Lisensi, atribusi, dan retention

Review engineering tanggal 22 Oktober 2026 untuk **prototipe pendidikan nonkomersial**. Rangkuman berikut adalah interpretasi operasional tim terhadap sumber resmi, bukan perubahan lisensi provider.

## Copernicus Marine

[Licence to use the Copernicus Marine Service Products](https://marine.copernicus.eu/user-corner/service-commitments-and-licence) berhasil diambil utuh via HTTP terminal meskipun browser fetch pernah mengembalikan 403. Bagian 2.2 mengizinkan salinan internal/back-up, modifikasi/produk turunan, serta redistribusi; 2.3–2.4 menetapkan credit/DOI; 2.6 meminta rekam jejak penggunaan dan propagasi ketentuan terkait kepada penerima. Kepemilikan sumber tetap UE; kualitas/ketersediaan tidak dijamin; lisensi dapat direvisi dan hak akses dapat ditarik bila terjadi pelanggaran. Label STAC `proprietary` tidak digunakan sebagai kesimpulan hak pakai.

Review ID database: `cmems-licence-20261022-sections-2.2-2.4-2.6`. Product DOI PHY: [10.48670/moi-00016](https://doi.org/10.48670/moi-00016); BGC: [10.48670/moi-00015](https://doi.org/10.48670/moi-00015). Dataset ID/version/depth/request/katalog dicatat per manifest. Untuk keluaran turunan gunakan credit yang menyebut Copernicus Marine dan DOI relevan; untuk redistribusi asli pakai credit bentuk redistribusi. [Panduan citation resmi](https://help.marine.copernicus.eu/en/articles/4444611-citing-copernicus-marine-products-and-services) membedakan ketiganya dan merujuk lisensi sebagai acuan.

## Open-Meteo / NOAA GFS

[Terms of Use](https://open-meteo.com/en/terms) membedakan **CC BY 4.0 pada data** dari **hak akses layanan API gratis**. API gratis hanya nonkomersial, dengan batas kurang dari 10.000 panggilan/hari, 5.000/jam, 600/menit. Produk/promosi komersial memerlukan entitlement layanan yang sesuai meskipun lisensi datanya memperbolehkan penggunaan komersial dengan atribusi. Konfigurasi A2 tidak membeli subscription dan tidak memakai endpoint customer.

Review ID: `open-meteo-terms-20261022-noncommercial-cc-by-4.0`. Credit menyebut Open-Meteo.com, NOAA GFS dan CC BY 4.0; tautan license/attribution ikut preview. Cadence default empat fetch per hari, dua koordinat dalam satu request, jauh di bawah batas untuk scope kecil ini; penghitungan/batas aplikasi dan IP provider tetap berlaku. Native cadence/interpolasi dirujuk pada [dokumentasi GFS](https://open-meteo.com/en/docs/gfs-api).

## Enforcement implementasi

- Empat dataset A2 di-enable untuk normalized ingestion setelah review; source sensor real tetap disabled.
- Runtime purpose dan review ID harus cocok dengan policy database. Worker hanya dapat memakai empat dataset yang terdaftar, fungsi privat, dan kredensial role terbatas.
- **A2 memilih metadata_only**: database menolak penyimpanan full raw lewat worker; `raw_storage_permitted` tetap false. Payload JSON/hasil subset hanya berada dalam memori sementara. Tidak ada raw science payload yang di-commit, diunggah ke vault atau disimpan di Storage.
- Normalized nilai/vintage, manifest hash/ukuran/metadata dan jejak attempt dipertahankan untuk provenance. Tidak ada batas retensi normalized yang ditetapkan provider pada klausul yang ditinjau; A2 menyimpannya append-only sampai ada kebijakan arsip proyek yang disepakati. Ini kebijakan proyek, bukan kewajiban menyimpan selamanya dari provider.
- Preview menyertakan atribusi dan URL lisensi. Konsumen UI/ekspor perlu menampilkan credit pada halaman akses data dan membawa provenance/ketentuan lisensi yang relevan; A2 belum menerbitkan UI/ekspor publik.
- Hash `toolbox_subset_json_v1` tidak dipasarkan sebagai checksum file asli. Tanpa raw response yang dipertahankan, replay byte-identik provider tidak tersedia; normalized snapshot dan lineage tersedia.
- Perubahan tujuan komersial, model/dataset, licence, raw retention atau distribusi perlu review dan policy baru; tidak diterka dari izin API.

URL, retrieval status dan checksum HTML publik: [source_evidence_20261022.json](/Users/cindyram/Documents/Second Brain/02-Projects/Challenge Final/Engineering/Seagis/A2/source_evidence_20261022.json). HTML dinamis dapat berubah checksum walau isi lisensi sama; ID review merujuk pembacaan klausul, bukan signature provider.


## Provenance salinan

Sumber: [licenses.md](/Users/cindyram/Documents/Apple/Seagis-Model/docs/a2/licenses.md), commit `2474251`. Salinan catatan lengkap dengan tautan lokal yang disesuaikan. [[Provenance A2 - Paket Engineering 22 Oktober 2026]] · [[Indeks - Engineering]].
