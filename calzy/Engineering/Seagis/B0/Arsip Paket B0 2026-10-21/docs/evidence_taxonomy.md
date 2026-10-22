# Taksonomi bukti 0.1.0

Sumber kosakata mesin: `schemas/taxonomy.schema.json`. Schema sumber dan entri merujuk file yang sama. Nilai baru harus ditambahkan melalui perubahan schema, dokumentasi, pengujian dan versi yang ditinjau; jangan memasukkan tag bebas diam-diam.

## Kosakata terkontrol

### `parameter_tags`

`water_temperature`, `salinity`, `nitrate`, `phosphate`, `ammonium`, `total_inorganic_nitrogen`, `current_velocity`, `precipitation`, `wind_speed`, `cloud_cover`, `solar_irradiance`, `par`, `uv_exposure`, `water_depth`, `turbidity`, `microbial_exposure`.

### `species`

`Kappaphycus alvarezii`, `Kappaphycus striatus`, `Kappaphycus malesianus`, `Eucheuma denticulatum`, `other_eucheumatoid`, `other_macroalga`, `other_organism`, `unresolved`.

### `outcome`

`growth_rate`, `biomass`, `photosynthetic_performance`, `pigment_concentration`, `oxidative_stress`, `gene_expression`, `nutrient_uptake`, `carrageenan_quality`, `bleaching`, `tissue_damage`, `ice_ice_incidence`, `ice_ice_prevalence`, `ice_ice_severity`, `mortality`, `other`.

### `evidence_type`

`controlled_experiment`, `observational_association`, `mechanistic_hypothesis`, `review_synthesis`, `field_observation`, `interview_report`, `team_interpretation`, `engineering_proposal`.

### `experimental_setting`

`laboratory`, `hatchery`, `open_sea_farm`, `pond`, `mesocosm`, `mixed`, `not_applicable`, `not_reported`.

### `verification_status`

`candidate`, `extracted`, `needs_review`, `verified`, `rejected`, `superseded`.

### `applicability`

`unassessed`, `same_species_context_limited`, `related_eucheumatoid_context_limited`, `hypothesis_only`, `local_field_evidence`, `not_applicable`.

### `limitation_tags`

`secondary_source_only`, `abstract_only`, `full_text_unavailable`, `units_unresolved`, `exposure_unreported`, `strain_unresolved`, `species_unresolved`, `small_sample`, `short_exposure`, `confounded_treatments`, `interaction_not_isolated`, `cross_species`, `non_local`, `setting_mismatch`, `observational_only`, `statistical_reporting_conflict`, `outcome_mismatch`, `no_disease_endpoint`, `no_predictive_validation`, `reader_inference`, `not_independent_evidence`, `synthetic_fixture`.

### `relationship_type`

`single_parameter`, `interaction`, `combined_exposure`, `context_only`.

### `direction`

`increase`, `decrease`, `no_detected_difference`, `mixed`, `not_reported`, `not_applicable`.

### `significance`

`significant`, `not_significant`, `not_tested`, `not_reported`, `conflicting_reporting`.

### `interaction_test`

`direct_test_reported`, `not_isolated`, `not_tested`, `not_reported`, `not_applicable`.

### `life_stage`

`vegetative_thallus`, `propagule`, `spore`, `mixed`, `other`, `not_reported`.

### `source_kind`

`primary_study`, `review`, `internal_synthesis`, `interview_note`, `engineering_note`, `other`.

### `access_status`

`not_checked`, `metadata_only`, `abstract_only`, `full_text_available`, `local_note_available`, `unavailable`.

### `read_scope`

`not_read`, `metadata_only`, `abstract_only`, `selected_full_text`, `full_text`, `local_note`.

### `quantity_basis`

`as_ion`, `as_N`, `as_P`, `practical_salinity`, `absolute_salinity`, `instrument_ppt_unspecified`, `not_applicable`, `not_reported`.

### `relation_type`

`supports`, `contradicts`, `different_context`, `duplicate_evidence`, `supersedes`.

### `reviewer_type`

`human`, `ai`.

## Makna dan aturan pemakaian

- `species` adalah daftar takson yang relevan untuk satu kontras. Nama asli, ejaan penulis dan strain disimpan dalam `experimental_conditions`; kategori `other_*` wajib dijelaskan di `species_reported`. `unresolved` bukan bukti spesies farm. `local_field_evidence` hanya untuk pengamatan lapangan di lokasi target, bukan sinonim spesies sama.
- `outcome` satu kategori per entri. `outcome_detail` menyimpan metode/denominator/definisi; `other` harus dijelaskan. Incidence, prevalence, severity dan bleaching tidak saling menggantikan. `null` diperbolehkan saat candidate belum diekstrak.
- `evidence_type` menyatakan dasar klaim, bukan kualitas keseluruhan paper. `controlled_experiment` tidak otomatis berarti semua parameter terisolasi. Asosiasi, hipotesis, sintesis review, penuturan narasumber, interpretasi tim dan proposal engineering tetap berbeda.
- `single_parameter`: satu tag; `interaction`: minimal dua tag dan uji langsung dilaporkan; `combined_exposure`: minimal dua tag tetapi efek gabungan belum diisolasi; `context_only`: konteks/lead tanpa klaim hubungan eksperimen. Paper gabungan salinitas–nutrisi tidak otomatis eksperimen interaksi faktorial.
- `direction` menyatakan arah outcome dalam pembanding yang dijelaskan, bukan nilai keselamatan tanaman. `no_detected_difference` memerlukan `not_significant`; hasil tidak signifikan tidak membuktikan ekuivalensi atau tidak adanya efek.
- `conflicting_reporting` untuk inkonsistensi statistik dalam sumber; konflik lintas sumber direkam melalui `related_entries` dan alasan. Kedua entri tetap disimpan. `mixed` harus dijelaskan; pisahkan endpoint bila memungkinkan.
- `quantity` menyimpan `values`, `unit_reported`, `basis`, `analyte_reported` dan `original_text`. `original_text` mempertahankan qualifier seperti <, ±, range, mean/SD/SE; jangan hilangkan batas deteksi. Konversi tidak mengganti satuan asli. `not_reported` berarti basis tidak dijelaskan, bukan nilai nol.
- `quantity_basis` memisahkan NO3/as N dan PO4/as P serta Practical Salinity, Absolute Salinity dan ppt yang definisinya belum jelas. Ketidakjelasan masuk `unknown_fields`, `limitations` dan `units_unresolved`; pemeriksaan boleh menyimpulkan unit memang tidak dilaporkan, tanpa mengarangnya.
- `exposures` berisi level/paparan dengan tag yang juga tercantum pada `parameter_tags`; `exposure_duration` memakai quantity, misalnya hari/jam, dan n menyimpan unit replikasi dalam teks. Semua properti konteks wajib hadir, tetapi nilai yang tidak diketahui boleh null dan harus ditandai.
- `limitations` adalah uraian spesifik wajib; `limitation_tags` membantu pencarian. `applicability` adalah kesesuaian konteks, bukan probabilitas penyakit. Organisme lintas kelompok hanya dapat menjadi `hypothesis_only`/`not_applicable`, tidak bukti langsung Tidung.
- `source_kind` menyatakan jenis dokumen. `access_status`, `read_scope` dan `bibliography_checked` adalah tiga hal berbeda. Memiliki PDF tidak sama dengan membaca atau mengecek bibliografi; membaca catatan internal tidak sama dengan membaca paper yang dikutip.

## Identitas dan relasi

ID stabil memakai huruf besar, angka, `_` atau `-`, misalnya `SRC-0001` dan `CLAIM-0001`. Jangan memasukkan besaran efek atau status review ke ID. `legacy_ids` menyimpan ID base lama. `duplicate_of` mengarah sumber kanonis dan tidak boleh berantai/siklis; dua record DOI/checksum sama hanya diizinkan jika duplikat ditandai.

`source_id` wajib resolve. `related_entries` menghubungkan dukungan, konflik, konteks berbeda, bukti duplikat, atau penggantian. `supersedes` ditempatkan pada entri pengganti yang menunjuk versi lama; versi lama harus `superseded`. `supports` bukan bukti independensi.

Versi 0.1.0 berlaku pada schema sumber dan entri. Perubahan makna/struktur harus dimigrasikan secara eksplisit. Versi corpus untuk retrieval produksi akan ditetapkan di B4 setelah ada kurasi; B0 belum menjanjikan kontrak Track A atau model.
