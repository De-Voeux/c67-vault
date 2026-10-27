---
type: engineering-note
project: "[[Challenge Final]]"
status: imported-foundation
created: 2026-10-21
tags: [challenge-final, seagis, engineering, knowledge-vault, evidence-schema]
---

# Implementasi B0 - Fondasi Vault Pengetahuan Ilmiah Seagis

Snapshot B0 dari repo `Seagis-Knowledge-Vault`, disimpan lengkap dalam [[Arsip Paket B0 2026-10-21/README|paket B0]]. Provenance, commit sumber dan checksum tiap berkas ada di [[Provenance Impor B0 - Seagis Knowledge Vault - 21 Oktober 2026]].

## Isi catatan

- [[Arsip Paket B0 2026-10-21/docs/research_questions|Pertanyaan riset]] — lima pertanyaan utama dan batas kajian.
- [[Arsip Paket B0 2026-10-21/docs/evidence_taxonomy|Taksonomi bukti]] — kosakata terkontrol untuk variabel, spesies, outcome, desain bukti, status dan batas.
- [[Arsip Paket B0 2026-10-21/docs/review_protocol|Protokol review]] — alur `candidate → extracted → needs_review → verified/rejected/superseded`, verifikasi manusia dan aturan sumber.
- [[Arsip Paket B0 2026-10-21/docs/context_and_provenance|Acuan awal dan provenance]] — catatan Challenge Final yang dipakai, batas akses, petunjuk sumber B1 dan checksum.

Paket juga mencakup tiga JSON Schema, JSONL registry sumber/entri, satu contoh candidate, validator lokal, 24 tes, dependency dan README asli. Seluruh 15 file disalin byte-for-byte; struktur direktori sumber dipertahankan.

## Status dan hubungan dengan riset

Status saat capture: **4 catatan sumber sekunder; 1 lead `candidate`; 0 temuan `verified`**. Nilai angka dan finding pada lead sengaja kosong. Catatan Challenge Final memberi petunjuk paper dan konteks, tetapi B0 tidak mengimpor klaim primer seolah-olah telah diperiksa ulang.

B0 menjawab tahap fondasi: pertanyaan, taksonomi, schema, registry minimal dan prosedur review. Pembacaan ini tidak mengubah ringkasan riset atau hasil observasi di vault. Sensor suhu saja adalah arah perangkat terbaru; cakupan literatur tetap menampung salinitas/nitrat/fosfat sebagai variabel riset.

Validator dan 24 tes lulus di repo sumber ketika B0 ditutup. Hasil tersebut memeriksa format dan integritas registry; bukan autentikasi reviewer atau validasi biologis. Berikutnya B1 membutuhkan pemeriksaan bibliografi dan akses full text, deduplikasi, lalu discovery 5–8 studi sebelum ekstraksi. B3 memerlukan review manusia; AI tidak menandai bukti sebagai verified.

## Arsip paket

[[Arsip Paket B0 2026-10-21/README|README dan panduan validator]] · [Registry sumber](Arsip Paket B0 2026-10-21/vault/sources.jsonl) · [Registry entri](Arsip Paket B0 2026-10-21/vault/entries.jsonl) · [Contoh candidate](Arsip Paket B0 2026-10-21/examples/candidate_entry.json)

[[Indeks - Engineering]] · [[Konteks Progres Seagis - 21 Oktober 2026]] · [[Challenge Final]]

## Rencana Track B dan scope lanjutan

[[TRACK_B_SCIENTIFIC_KNOWLEDGE_VAULT]] menyimpan rencana lengkap v0.1. [[Status Track B - Fokus B0.5 dan Review Manual]] mencatat prioritas B0.5, kebutuhan interpretasi suhu dan pemeriksaan literatur oleh pengguna sebelum melanjutkan tahap berikutnya.
