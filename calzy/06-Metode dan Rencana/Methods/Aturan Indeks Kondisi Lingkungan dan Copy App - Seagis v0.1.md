---
type: design-specification
project: "[[Challenge Final]]"
created: 2026-11-02
updated: 2026-11-02
status: proposed-pilot
rule_version: seagis-condition-index-v0.1
tags: [challenge-final, seagis, rule-set, integrasi, copy]
---

# Aturan Indeks Kondisi Lingkungan dan Copy App — Seagis v0.1

Dokumen ini mencatat keputusan percakapan 2 November 2026 untuk integrasi berikutnya. Setiap parameter dinilai sendiri terhadap rentangnya dan mendapat bobot sama. Output berupa indeks, status perhatian, daftar parameter penyebab, serta kelengkapan data. Copy dibuat melalui template dan formatter.

**Arti indeks 80/100 adalah 80% parameter valid berada dalam rentang acuan.** Pengujian lapangan masih diperlukan untuk menghubungkan hasil ini dengan kondisi tanaman. Bobot, klasifikasi, dan ambang dalam dokumen ini merupakan keputusan pilot. Klaim peluang keselamatan farm atau probabilitas ice-ice memerlukan model dan validasi tersendiri.

## 1. Keputusan perhitungan

| Elemen | Aturan |
| --- | --- |
| Unit penilaian | Satu petak dan satu waktu penilaian. Parameter regional tetap berlabel regional. |
| Kontribusi parameter | Dalam rentang normal = 1 poin. Waspada atau bahaya = 0 poin. |
| Bobot | Semua parameter aktif dan valid berbobot sama. |
| Hubungan antardata | Evaluasi individual. Tiap parameter menghasilkan alasan berdasarkan kondisinya sendiri. |
| Indeks | `100 × normal_count / valid_count`. |
| Kelengkapan | `100 × valid_count / expected_count`. `expected_count` adalah jumlah parameter aktif pada profil yang sama. |
| Pembulatan | Tampilan indeks dan kelengkapan satu angka desimal bila diperlukan. Klasifikasi memakai nilai asli. |
| Data kosong | `valid_count = 0` menghasilkan `index = null`. `expected_count = 0` menghasilkan `index = null`, `coverage = null`, dan `configuration_missing`. |
| Versi | Simpan versi profil, aturan, dan daftar parameter aktif pada setiap hasil. |

Contoh 10 parameter aktif dan valid, 8 normal, 2 di luar rentang menghasilkan **80/100** dengan kelengkapan **10/10**. Contoh ini ilustrasi aritmetika. Jumlah parameter mengikuti profil yang benar-benar diaktifkan.

Suhu absolut dan Δ suhu dihitung sebagai dua parameter jika keduanya aktif. Dengan pilihan ini, perubahan dari satu sensor dapat mengurangi dua poin sekaligus. Konsekuensi tersebut mengikuti keputusan penilaian individual berbobot sama dan harus terlihat dalam daftar parameter aktif.

## 2. Profil awal untuk simulasi integrasi

Tabel berikut adalah **usulan konfigurasi awal**, disusun dari tabel pengguna pada 2 November. Batas salinitas waspada dilengkapi agar semua nilai tercakup. Endpoint arus diperjelas agar tidak tumpang tindih. Pemakaian merah pada suhu di luar 26–30°C dan Δ ≥1°C mengikuti tabel pengguna sebagai aturan pilot, dengan batas bukti pada bagian 9. Profil ini perlu review sebelum dipakai untuk peringatan farm nyata.

| ID parameter | Sumber dan unit penilaian | Normal | Waspada | Bahaya | Aktif dalam indeks |
| --- | --- | --- | --- | --- | --- |
| `water_temperature` | IoT petak, °C | `26 ≤ T ≤ 30` | Tidak digunakan pada profil ini | `T < 26` atau `T > 30` | Ya |
| `temperature_change` | Turunan dua pembacaan IoT, °C/jam | `D < 0,5` | `0,5 ≤ D < 1` | `D ≥ 1` | Ya, bila pasangan valid |
| `salinity` | Model regional, unit harus dipetakan sesuai metadata sumber | `28 ≤ S ≤ 34` | `24 ≤ S < 28` atau `34 < S ≤ 38` | `S < 24` atau `S > 38` | Ya, setelah pemetaan satuan disahkan |
| `current_speed` | Magnitude arus model regional, cm/detik | `20 ≤ V ≤ 40` | `10 ≤ V < 20` atau `40 < V ≤ 50` | `V < 10` atau `V > 50` | Ya |

Profil awal memuat empat parameter yang diharapkan. Syarat pasangan atau satuan yang gagal membuat parameter berstatus `unknown` dan mengurangi kelengkapan. Parameter tersebut tetap masuk `expected_count`. Penonaktifan parameter merupakan perubahan profil berversi, sehingga data hilang tidak diam-diam mengubah cakupan penilaian.

`D = abs(T_sekarang − T_sebelumnya) / selisih_waktu_dalam_jam`. Gunakan dua slot hourly berurutan dari sensor dan pemasangan yang sama, keduanya valid, dengan selisih aktual 45–75 menit. Selang waktu ditampilkan pada detail. Pasangan di luar jendela tersebut menghasilkan `unknown`; interpolasi melewati gap tidak digunakan. Jendela ini merupakan pilihan engineering pilot.

`V = sqrt(u² + v²) × 100` jika komponen arus sumber memakai m/s. Terapkan threshold pada magnitude, dengan komponen dari grid, kedalaman, dan waktu yang sama.

| Parameter lain | Perlakuan pada profil awal | Syarat untuk penambahan nanti |
| --- | --- | --- |
| Δ salinitas | Ditampilkan sebagai konteks perubahan antarwaktu model bila tersedia | Data native saat ini 6 jam. Definisikan jendela dan threshold sesuai cadence sumber sebelum dihitung. |
| Nitrat | Konteks, `enabled = false` | Referensi pengguna 0,9–3,5 mg/L masih memerlukan konfirmasi basis NO₃ versus NO₃-N dan review ambang. |
| Fosfat | Konteks, `enabled = false` | Referensi pengguna 0,051–1,00 mg/L masih memerlukan konfirmasi basis PO₄ versus PO₄-P dan review ambang. |
| Curah hujan/presipitasi | Konteks cuaca, `enabled = false` | Pilih satu field yang mewakili kebutuhan dan definisikan interval. Total presipitasi sudah mencakup hujan. |
| Tutupan awan, UV Index, angin | Konteks cuaca, `enabled = false` | Tentukan dasar dan rentang penilaian jika akan dimasukkan. |
| Koneksi IoT | Status perangkat terpisah | Hitung keterlambatan dari jadwal kedatangan berikutnya. ≤5 menit normal, >5 hingga ≤30 menit terlambat, >30 menit offline. |

Parameter konteks dan koneksi perangkat berada di luar `expected_count`. Jumlah parameter yang tampil di layar dapat lebih banyak daripada jumlah yang dihitung dalam indeks.

## 3. Syarat data yang boleh dinilai

1. Cocokkan petak atau grid wilayah, sumber, satuan, kedalaman bila relevan, dan waktu berlaku. Suhu IoT hanya berlaku pada titik yang terukur.
2. Terima data yang lolos kebijakan kualitas dan freshness pipeline A3 untuk sumber terkait. Simpan `quality_policy_version` serta `usable_until`. Jika kebijakan atau keputusan kelayakan belum tersedia, hasil parameter `unknown`.
3. Simpan waktu pengukuran/berlaku terpisah dari waktu diterima. Paket lama yang baru datang tetap memakai waktu pengukuran lamanya. Store UTC dan tampilkan Asia/Jakarta.
4. Data missing, invalid, stale, atau pasangan Δ yang tidak memenuhi syarat menghasilkan `unknown`, dengan alasan eksplisit. Ekstrem yang valid tetap dinilai menurut threshold.
5. Gunakan satu nilai representatif per parameter per penilaian. Retry, duplikat, serta nilai regional yang sama untuk beberapa petak tidak menambah jumlah parameter.
6. Penilaian kondisi saat ini dan prakiraan disimpan terpisah lewat `assessment_kind` serta `target_at`. Copy prakiraan selalu menyebut waktu berlaku. Δ suhu lokal memerlukan pasangan IoT yang sah.
7. Snapshot demo atau sintetis diberi `data_mode = synthetic` dan banner **Data simulasi**.

Salinitas dan arus yang tersedia setiap 6 jam dapat dipakai selama masih dinyatakan usable oleh pipeline. Reuse nilai itu pada snapshot berikutnya mempertahankan waktu asli. Nutrien mengikuti dukungan harian sumber. Daftar parameter yang dinilai harus terlihat agar perubahan komposisi input dapat diketahui pengguna.

## 4. Status dan peringatan

Indeks menampilkan jumlah parameter dalam rentang. Warna status mengikuti tingkat perhatian tertinggi yang masih valid pada waktu penilaian.

| Urutan | Kondisi | `assessment_status` | Copy status |
| --- | --- | --- | --- |
| 1 | Ada parameter valid `danger` | `danger` | Prioritaskan pemeriksaan |
| 2 | Ada parameter valid `warning`, tanpa `danger` | `warning` | Ada parameter perlu perhatian |
| 3 | Semua parameter aktif valid dan `normal` | `normal` | Seluruh parameter dalam rentang acuan |
| 4 | Selain kondisi di atas | `insufficient_data` | Penilaian belum lengkap |

Simpan `data_status` sebagai `complete` atau `incomplete` secara terpisah. Satu parameter merah dengan dua data hilang menghasilkan `assessment_status = danger` dan `data_status = incomplete`. Kartu menampilkan keduanya.

**90/100 dapat berdampingan dengan peringatan merah** apabila satu dari sepuluh parameter masuk bahaya. Klasifikasi normal/waspada/bahaya tidak memakai potongan skor seperti 80 atau 60 pada versi ini.

Ketika data pemicu menjadi stale, hitung ulang dengan status parameter `unknown`. Simpan kejadian sebelumnya dalam riwayat dan tampilkan **Peringatan sebelumnya belum terverifikasi pulih**. Koneksi putus tidak menjadi bukti pemulihan. Dokumen ini menetapkan status snapshot; penutupan tugas pemeriksaan memerlukan alur tindak lanjut tersendiri.

## 5. Pembentukan copy

Alur integrasi adalah **input usable → klasifikasi per parameter → hitung indeks dan status → pilih template → format nilai dan waktu**. Engine menghasilkan fakta terstruktur. Template menentukan kalimat. Formatter mengatur angka, satuan, dan waktu.

| Kondisi | Template |
| --- | --- |
| Angka utama | **Indeks kondisi lingkungan · {index}/100** |
| Ringkasan jumlah | “{normal_count} dari {valid_count} parameter yang dapat dinilai berada dalam rentang acuan.” |
| Lengkap dan normal | “Seluruh parameter yang dipantau berada dalam rentang acuan.” |
| Ada penyimpangan | “{outside_count} parameter perlu perhatian. {parameter_reasons}.” |
| Ada bahaya | “Prioritaskan pemeriksaan. {danger_reasons}.” |
| Ada data hilang | “Data {unknown_parameters} belum dapat dinilai. {valid_count} dari {expected_count} parameter tersedia.” |
| Seluruh data hilang | “Penilaian belum tersedia. Menunggu data yang valid.” Angka indeks tampil sebagai **—**. |
| Konfigurasi kosong | “Penilaian belum dikonfigurasi.” Angka indeks tampil sebagai **—**. |
| Prakiraan | “Prakiraan untuk {target_time}. {condition_summary}.” |

| Asal alasan | Template fakta |
| --- | --- |
| IoT, nilai tinggi | “Sensor petak mencatat {parameter} {value} {unit}, di atas rentang acuan {range}, pada {time}.” |
| IoT, nilai rendah | “Sensor petak mencatat {parameter} {value} {unit}, di bawah rentang acuan {range}, pada {time}.” |
| Δ suhu | “Suhu berubah {absolute_change}°C dalam {elapsed_minutes} menit, setara {rate}°C/jam.” |
| Model regional | “Model memperkirakan {parameter} wilayah {value} {unit}, {relation} rentang acuan {range}, untuk {valid_time}.” |

Alasan diurutkan `danger → warning`, lalu menurut urutan parameter pada profil. Tampilkan dua alasan pertama pada kartu ringkas dan “+{remaining_count} parameter lain” bila perlu. Semua alasan tersedia di detail. Parameter normal tetap dapat dilihat pada daftar.

Gunakan label **Indeks kondisi lingkungan**, **dalam rentang acuan**, **model regional**, dan **prakiraan** sesuai sumbernya. Kalimat menyebut kondisi setiap parameter. Hubungan penyebab antara hujan, nutrien, suhu, dan kondisi tanaman memerlukan bukti tambahan di luar output versi ini. LLM bersifat opsional untuk pengembangan berikutnya; kebutuhan copy v0.1 terpenuhi dengan template dan formatter.

## 6. Kontrak hasil untuk integrasi

Ini bentuk output yang diusulkan, dengan contoh sintetis. Endpoint dan penyimpanan dicocokkan saat implementasi.

```json
{
  "rule_version": "seagis-condition-index-v0.1",
  "profile_id": "pilot-four-parameters-v0.1",
  "subject_id": "demo-plot-a",
  "subject_scope": "plot",
  "assessment_kind": "current",
  "target_at": "2026-11-02T07:00:00Z",
  "evaluated_at": "2026-11-02T07:05:00Z",
  "data_mode": "synthetic",
  "index": 50,
  "normal_count": 2,
  "outside_count": 2,
  "valid_count": 4,
  "expected_count": 4,
  "coverage_percent": 100,
  "assessment_status": "danger",
  "data_status": "complete",
  "reason_codes": ["current_speed_low", "salinity_low"],
  "unknown_parameters": [],
  "template_key": "condition_danger",
  "parameters": [
    {"id": "water_temperature", "value": 29, "unit": "degC", "status": "normal", "source_kind": "iot_local"},
    {"id": "temperature_change", "value": 0.2, "unit": "degC/h", "status": "normal", "source_kind": "derived_iot"},
    {"id": "salinity", "value": 26, "unit": "source_verified", "status": "warning", "source_kind": "regional_model"},
    {"id": "current_speed", "value": 8, "unit": "cm/s", "status": "danger", "source_kind": "regional_model"}
  ]
}
```

Setiap parameter pada payload implementasi juga wajib membawa `source_id`, `value_ids` untuk lineage, `valid_at`, `received_at`, `usable_until`, `quality_policy_version`, `rule_id`, `reason_code` bila menyimpang, dan threshold yang terpakai. Simpan `source_grid_id` untuk regional, serta `sensor_id` untuk IoT. Δ membawa kedua record input dan selisih waktunya. Normalisasi salinitas harus mengganti placeholder `source_verified` dengan unit yang disahkan sebelum penilaian nyata.

Parameter `unknown` membawa `value = null` untuk penilaian dan `unavailable_reason`; angka terakhir boleh disimpan terpisah sebagai riwayat. Salinitas 26 pada contoh diasumsikan sudah lolos pemetaan satuan. Semua input contoh diasumsikan lolos QC dan freshness; contoh payload ringkas menonjolkan struktur hasil.

## 7. Contoh kartu dari hasil di atas

> **Data simulasi**  
> **Indeks kondisi lingkungan · 50/100**  
> 2 dari 4 parameter berada dalam rentang acuan. Data lengkap 4/4.  
> 🔴 **Prioritaskan pemeriksaan**  
> Arus wilayah diperkirakan 8 cm/detik, di bawah rentang acuan 20–40 cm/detik. Salinitas wilayah juga berada di bawah rentang acuan.  
> Suhu sensor petak tercatat 29°C.  
> **Lihat detail parameter**

Detail wajib menampilkan waktu asli masing-masing parameter, satuan yang telah disahkan, rentang, dan asal lokal atau regional. Penilaian petak ini memuat kedua skala tersebut. Untuk peta wilayah, hitung profil regional tersendiri dan tampilkan cakupan serta parameter aktifnya. Profil yang berbeda mempunyai komposisi indeks berbeda dan perlu diberi label saat dibandingkan.

## 8. Skenario pemeriksaan integrasi

| Skenario | Hasil yang diharapkan |
| --- | --- |
| 8 normal dari 10 valid, 2 warning | Indeks 80, warning, data complete, dua alasan. |
| 9 normal dari 10 valid, 1 danger | Indeks 90, danger, peringatan merah terlihat. |
| 8 normal dari 8 valid, 2 unknown dari profil 10 | Indeks 100, coverage 80%, insufficient_data, teks 8/10 tersedia. |
| 7 normal, 1 danger, 2 unknown dari profil 10 | Indeks 87,5, coverage 80%, danger dan incomplete. |
| Seluruh parameter unknown | Indeks null, insufficient_data, semua alasan ketidaktersediaan tercatat. |
| Tidak ada parameter aktif | Indeks dan coverage null, configuration_missing. |
| Suhu tepat 26 atau 30°C | Normal. Suhu 10°C valid masuk danger pada profil pilot. |
| Δ tepat 0,5 atau 1°C/jam | Warning pada 0,5; danger pada 1. |
| Salinitas tepat 24, 28, 34, 38 | Warning, normal, normal, warning. |
| Arus tepat 10, 20, 40, 50 cm/detik | Warning, normal, normal, warning. |
| Satu suhu tanpa pasangan hourly | Suhu absolut dinilai; Δ unknown; expected_count tetap empat. |
| Retry atau nilai regional di-fetch ulang | Jumlah parameter dan waktu berlaku tetap. |
| Data pemicu melewati usable_until | Parameter unknown, coverage turun, riwayat peringatan belum terverifikasi pulih terlihat. |
| Prakiraan di luar rentang untuk besok | Kartu prakiraan mencantumkan waktu besok dan terpisah dari penilaian saat ini. |

## 9. Dasar keputusan dan batas integrasi

**Keputusan pengguna** adalah penilaian individual, bobot sama, indeks berdasarkan jumlah dalam rentang, serta narasi berdasarkan kondisi. Formula, coverage, pemisahan status merah, kontrak hasil, dan template adalah spesifikasi engineering dari keputusan tersebut. Profil empat parameter merupakan usulan awal dokumen ini.

**Jejak ambang** berasal dari screenshot pengguna 2 November 2026, bukan pengesahan penelitian. [[Bukti dan Keputusan - Rule Set Cottonii v0.1]] mencatat bahwa cutoff alarm, laju perubahan, dan probabilitas penyakit belum tervalidasi. Karena itu suhu 25,9°C yang masuk merah pada profil ini menyatakan hasil konfigurasi pilot. Tingkat kerusakan biologisnya masih perlu diuji.

**Perbedaan dengan dokumen lama** perlu diperhatikan. [[Rule Set Lingkungan Cottonii v0.1 - Patokan Desain]] memakai pemicu, baseline, recovery, serta klasifikasi suhu yang berbeda. Integrator memilih satu profil berversi. Dokumen ini menjadi acuan untuk metode indeks dan copy dari keputusan terbaru; aturan lama tidak digabung otomatis. Aktivasi ambang untuk peringatan nyata tetap memerlukan review profil dan kualitas data.

**Metadata sumber** mengikuti [[Seagis A0 - Source Registry]] dan pemeriksaan kualitas/alignment [[Handover A3 - Kualitas dan Alignment Data]]. Registri merupakan snapshot dokumentasi, sehingga integrator perlu mencocokkannya dengan kontrak sumber dan policy A3 yang sedang dipakai. Satuan, cadence, freshness, dan lineage dipertahankan pada hasil.

Dokumen ini merupakan spesifikasi untuk integrasi kemudian. Pengujian engine melalui skenario bagian 8 dan validasi terhadap pemeriksaan tanaman merupakan pekerjaan lanjutan.
