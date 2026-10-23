---
type: provenance
project: "[[Challenge Final]]"
created: 2026-10-22
updated: 2026-10-22
tags: [challenge-final, seagis, engineering, a2, provenance]
---

# Provenance A2 - Paket Engineering 22 Oktober 2026

Paket sumber berasal dari repo `/Users/cindyram/Documents/Apple/Seagis-Model`, branch `feat/contract-A2`, commit `24742513987227968228c54c1898d4c6d6dc54b2`. Tidak ada push dari sesi ini.

## Isi dan batas

- Empat catatan lengkap: arsitektur, operasi/scheduler, lisensi/retention dan review hasil. Frontmatter/provenance ditambahkan; tautan file disesuaikan untuk vault.
- Dua JSON publik disalin byte-identik: bukti sumber dan laporan operasi cloud. Tidak ada token, DSN, raw science payload atau credential file yang disalin.
- Hasil: 466 nilai model regional asli (26 arus + 8 nutrien + 432 cuaca), tiga sel, enam mapping preview, 13 speed turunan. A1 tetap 136 observasi sintetis / 0 observasi sensor nyata.
- Salinitas belum masuk karena provider menandai rentang sedang diperbarui sejak 7 Oktober; safeguard tetap aktif dan scheduler melakukan retry/backoff.
- Seluruh plot masih contoh belum disurvei; issue/init time tidak tersedia secara terverifikasi. Nilai unreviewed dan bridge demo tidak dapat masuk training.
- Scheduler lokal sudah terpasang dan tick pertama exit 0. Hanya berjalan saat Mac aktif dan user login, bukan cloud 24/7.
- Bukti adalah operasi fetch/persist, read-only inspection dan lint; suite tests/regresi A0/A1 tidak ditambah/dijalankan ulang pada A2.

## Commit implementasi

- `22f992f` — feat(ingestion): add regional adapters immutable vintages and restricted worker
- `5646805` — fix(ingestion): handle provider metadata variants and bound scheduled workers
- `4a40729` — fix(ingestion): report provider update safeguards explicitly
- `2474251` — docs(ingestion): hand over A2 operations licences and live regional results

## Checksum SHA-256

Checksum sumber dan salinan berbeda untuk Markdown karena penyesuaian vault. JSON identik.

| Sumber repo | SHA-256 sumber | Salinan vault | SHA-256 salinan |
|---|---|---|---|
| `docs/a2/architecture.md` | `530a0c4d72f8d9b05b53b0c09dee3d1c30064a6446a8dba7220fc9bd019f5655` | `Handover A2 - Ingestion Lingkungan dan Grid.md` | `5c21e5d0341ca00cc5bb523430e64d6e8ea65f6604806c4c4b301d33e73b2afa` |
| `docs/a2/operations.md` | `d0a4e9894254025cc7514a9fe808dd25bd929c0053c389f8ea05ff4208c2acfa` | `Operasi A2 - Adapter dan Scheduler.md` | `a6abf259f025b19e8a18404abe2e730289d7c5428f69c9ae48ea30d3e1ada190` |
| `docs/a2/licenses.md` | `c1551d495c52a5054f7974d2d7397d1e9ea3f841619b77ed4d504b4570d1743a` | `Lisensi A2 - Atribusi dan Retention.md` | `3b8e09a085baf6d040ea905d166339569417989baaabfc90a818edec59600231` |
| `docs/a2/review.md` | `ea22ff34a20cbf1691ecfcbe1b3269aeeb46d5d4d6bb5f450b8f9571667442a2` | `Review A2 - Hasil Ingestion Regional.md` | `f1bad10379a36a14afb9c589f024a2b5029dbbab791b39c125a064056227a9fe` |
| `docs/a2/source_evidence_20261022.json` | `a80fd90bae4da2694c049feed7b34bde43ff0ace51d5ddbb66389536b797b0e5` | `source_evidence_20261022.json` | `a80fd90bae4da2694c049feed7b34bde43ff0ace51d5ddbb66389536b797b0e5` |
| `docs/a2/ingestion_report_20261022.json` | `894bb8e96fa756341075c760c2841db21ff3d95e098aa44540e7557a29c34ddd` | `ingestion_report_20261022.json` | `894bb8e96fa756341075c760c2841db21ff3d95e098aa44540e7557a29c34ddd` |


Navigasi: [[Handover A2 - Ingestion Lingkungan dan Grid]] · [[Operasi A2 - Adapter dan Scheduler]] · [[Lisensi A2 - Atribusi dan Retention]] · [[Review A2 - Hasil Ingestion Regional]] · [[Indeks - Engineering]].
