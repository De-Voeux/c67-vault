---
type: provenance
project: "[[Challenge Final]]"
created: 2026-10-22
updated: 2026-10-22
source_commit: "96820a997060bec6aedf732779c7acd62fe8e96a"
tags: [challenge-final, seagis, engineering, a1, provenance]
---

# Provenance A1 - Paket Handover 22 Oktober 2026

Sumber: `/Users/cindyram/Documents/Apple/Seagis-Model`, commit `96820a997060bec6aedf732779c7acd62fe8e96a`. Tiga catatan engineering diimpor utuh secara isi dengan penambahan frontmatter, backlink provenance, adaptasi tautan internal menjadi wikilink, dan tautan kode yang diarahkan ke repo asli. Artefak kode/schema/dummy fixture tetap di repo model. Catatan A0/B0 dipertahankan sebagai snapshot historis.

| Catatan vault | Sumber relatif repo | SHA-256 sumber |
|---|---|---|
| [[Handover A1 - Arsitektur Data dan Akses IoT]] | `docs/a1/iot_handover.md` | `7fbd035f3e1b843ca05b69958f7a442515c51e4df5ca33b36bb4c1a6f0914333` |
| [[Operasi A1 - Simulator dan Credentials]] | `docs/a1/operations.md` | `01d9de4516a22f3683b8065a5fd0b3a02941e027bba38e81307b87e821c0c36e` |
| [[Review A1 - Temperature Vertical Slice]] | `docs/a1/review.md` | `b2d95bdf10bff99cf560b93d0a86c2227525f882412d04b1b031d7e3cbdf705c` |

Hash salinan vault yang sudah diadaptasi:

- `Handover A1 - Arsitektur Data dan Akses IoT.md`: `bb2fdc719859eae5ecf4c26b3bed43b33ad809d7237b00c814dfe1d1abcf0e2d`
- `Operasi A1 - Simulator dan Credentials.md`: `c89eff765e5a5549d3b701442daa21779ab112d4eafa3981f8677c3ca286315c`
- `Review A1 - Temperature Vertical Slice.md`: `095ea13f013b2f11bef53306967f18889325351462d879a872b1fbcc140f6803`

[Bukti live JSON](validation_20261022.json) disalin byte-identik dari repo. SHA-256: `1ad7b37395480199d2b6b2fa55cab7455862212901b8474c0e4bbc05577dae99`. Bukti ini memuat project ref, endpoint, status HTTP, versi migration/function dan data sintetis; tidak memuat token, password, raw header atau data pribadi lapangan.

Status A1 berbeda dari snapshot A0: migration 0001/0002 sudah terpasang pada development Seagis, endpoint temperature aktif, dan 136 observasi sintetis tersedia. Hardware belum dikomisioning dan real ingestion masih mati. Hasil pengujian lokal/live dicatat dari eksekusi pada 22 Oktober 2026; bukan validasi biologis atau akurasi model.
