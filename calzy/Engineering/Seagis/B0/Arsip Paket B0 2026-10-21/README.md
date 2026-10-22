# Seagis Knowledge Vault

Fondasi **B0, schema 0.1.0** untuk bukti ilmiah budidaya rumput laut Pulau Tidung. Dokumentasi berbahasa Indonesia; identifier terstruktur berbahasa Inggris.

Saat ini ada **4 sumber catatan sekunder**, **1 lead `candidate` tanpa finding/angka**, dan **0 klaim verified**. B0 membangun pertanyaan, taksonomi, schema dan aturan review; belum melakukan discovery/ekstraksi B1–B3, retrieval produksi, atau integrasi Foundation Models.

- [Pertanyaan riset](docs/research_questions.md)
- [Taksonomi](docs/evidence_taxonomy.md)
- [Protokol review](docs/review_protocol.md)
- [Acuan awal, provenance, dan batas akses](docs/context_and_provenance.md)
- Schema: [sumber](schemas/source.schema.json), [klaim](schemas/knowledge_entry.schema.json), [kosakata](schemas/taxonomy.schema.json)
- Registry: [sources.jsonl](vault/sources.jsonl), [entries.jsonl](vault/entries.jsonl)
- [Contoh belum terverifikasi](examples/candidate_entry.json), identik dengan lead di vault.

## Pemeriksaan lokal

Python 3.10+:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python extraction/validate_schema.py
.venv/bin/python -m unittest discover -s tests -v
```

Validator memeriksa JSON Schema Draft 2020-12 (termasuk format tanggal), ID/rujukan, duplikat DOI/checksum, riwayat status, dan syarat promosi verified. Exit code bukan nol berarti ada kegagalan. Tidak mengambil sumber dari internet atau menulis ulang registry. Untuk vault di lokasi lain: `--sources PATH --entries PATH`.

Schema memeriksa kelengkapan rekaman; manusia tetap harus memeriksa kebenaran bukti dan identitas reviewer. Tanda `human` dalam JSON bukan autentikasi. Verified belum berarti ambang universal, diagnosis, atau model prediksi tervalidasi.

## Git

Gunakan Conventional Commits: `feat(b0): ...`, `fix(schema): ...`, `docs(evidence): ...`, `test(validation): ...`. Stage path deliverable secara eksplisit. Commit lokal per perubahan logis yang selesai dan diperiksa; jangan commit `.agent-work/`, PDF penuh, kredensial atau path pribadi tambahan. Push mengikuti permintaan publikasi terpisah.
