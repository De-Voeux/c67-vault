# SEAGIS — Database documentation / Dokumentasi database

Version: 1.0.0 | 2026-10-27 (Asia/Jakarta)

Audit kode lokal dan snapshot catalog 2026-10-22; bukan audit runtime terkini. / Local code and 2026-10-22 catalog audit; not a current runtime audit.

| Bahasa / Language | Markdown lengkap / Complete Markdown | PDF |
| --- | --- | --- |
| Bahasa Indonesia | [Dokumentasi lengkap](id/DOKUMENTASI_DATABASE.md) | [PDF Indonesia](id/DOKUMENTASI_DATABASE.pdf) |
| English | [Complete documentation](en/DATABASE_DOCUMENTATION.md) | [English PDF](en/DATABASE_DOCUMENTATION.pdf) |

## Modul / Modules

| ID | EN |
| --- | --- |
| [INVENTARIS_DATABASE](id/schemas/INVENTARIS_DATABASE.md) | [DATABASE_INVENTORY](en/schemas/DATABASE_INVENTORY.md) |
| [KAMUS_DATA](id/schemas/KAMUS_DATA.md) | [DATA_DICTIONARY](en/schemas/DATA_DICTIONARY.md) |
| [RELASI_ENTITAS](id/schemas/RELASI_ENTITAS.md) | [ENTITY_RELATIONSHIPS](en/schemas/ENTITY_RELATIONSHIPS.md) |
| [ALUR_ASAL_DATA](id/pipelines/ALUR_ASAL_DATA.md) | [DATA_LINEAGE](en/pipelines/DATA_LINEAGE.md) |
| [PIPELINE_INGESTI](id/pipelines/PIPELINE_INGESTI.md) | [INGESTION_PIPELINES](en/pipelines/INGESTION_PIPELINES.md) |
| [PEMETAAN_SUMBER_TUJUAN](id/pipelines/PEMETAAN_SUMBER_TUJUAN.md) | [SOURCE_TO_TARGET_MAPPING](en/pipelines/SOURCE_TO_TARGET_MAPPING.md) |
| [KONTRAK_DATA](id/contracts/KONTRAK_DATA.md) | [DATA_CONTRACTS](en/contracts/DATA_CONTRACTS.md) |
| [ERD](id/architecture/ERD.md) | [ERD](en/architecture/ERD.md) |
| [ALIRAN_DATA](id/architecture/ALIRAN_DATA.md) | [DATA_FLOW](en/architecture/DATA_FLOW.md) |
| [SIKLUS_HIDUP_DATA](id/architecture/SIKLUS_HIDUP_DATA.md) | [DATA_LIFECYCLE](en/architecture/DATA_LIFECYCLE.md) |
| [DEPENDENSI_DATA](id/architecture/DEPENDENSI_DATA.md) | [DATA_DEPENDENCIES](en/architecture/DATA_DEPENDENCIES.md) |
| [AUDIT_KUALITAS_DATA](id/audit/AUDIT_KUALITAS_DATA.md) | [DATA_QUALITY_AUDIT](en/audit/DATA_QUALITY_AUDIT.md) |

## Evidence & reproduction / Bukti dan reproduksi

- [Source manifest](assets/generated/source-manifest.json): commit, paths and SHA-256; no credentials or table records.
- [Coverage](assets/generated/coverage.json) and [validation](assets/generated/validation.json).
- [Catalog snapshot](assets/evidence/schema-metadata-20261022.json); not a fresh live inspection.
- Mermaid source and deterministic vector renderings: `assets/diagrams/`.
- Rebuild documentation: `python3 assets/generated/build_docs.py`; set `SEAGIS_DOC_OUTPUT` to a new output directory if needed. Local source checkouts and catalog snapshot are required at the paths recorded in the script.
- Rebuild PDFs: `python3 assets/generated/render_pdf.py /path/to/docs/database`. Requires ReportLab and pypdf; Poppler is used for layout inspection.

Do not run migrations, provisioning or ingestion to reproduce documentation. No application code, database schema or production records were changed. Full runtime architecture completeness remains unverified. / Jangan menjalankan migrasi, provisioning atau ingestion untuk membangun ulang dokumentasi. Kode aplikasi, schema dan record produksi tidak diubah. Kelengkapan arsitektur runtime belum terverifikasi.
