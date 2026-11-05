---
type: project-status
created: 2026-11-05
updated: 2026-11-05
status: current-working-context
supersedes: "[[Status PoC IoT Suhu SEAGIS - 4 November 2026]]"
tags: [radit, iot, lora, suhu, poc]
---

# Status PoC IoT Suhu SEAGIS — 5 November 2026

Catatan status dari sesi kerja 5 November 2026, menggantikan [[Status PoC IoT Suhu SEAGIS - 4 November 2026]]. Ini status **uji meja sebagian, bukan bukti perangkat lulus uji meja penuh atau uji laut**. Radio antar board belum pernah jalan, dan upload lewat modem belum berhasil.

Isi catatan ini adalah klaim agent dari sesi kerja, kecuali yang ditandai diverifikasi, pernyataan, atau hasil ukur pengguna.

## Posisi terakhir

SIM800L sempat terdaftar ke jaringan dan membuka TCP ke server, lalu berhenti menjawab. LED modem mati menurut pengguna. Penyebabnya belum diketahui, dan pengukuran jalur daya belum selesai.

## Yang berubah

- **Part tiba (pernyataan pengguna).** E32 dan SIM800L terpasang di rakitan hub.
- **APN modem.** `config.h` di tiga salinan firmware kini memakai APN Telkomsel, bukan placeholder (diverifikasi).
- **Kartu SIM sementara.** Uji memakai kartu nano milik pengguna dengan adaptor kertas di slot micro. Ini hanya untuk uji meja; kartu lapangan belum dipilih.

## Hasil uji meja 5 November

| Bagian | Hasil | Asal bukti |
|---|---|---|
| Dua board lewat WiFi sampai server | HTTP 201, bukan uji LoRa | keluaran serial |
| E32 ke ESP32 | versi dan parameter terbaca | keluaran serial |
| Pancaran E32 | **belum terbukti**, butuh E32 kedua | - |
| OUT+ XL6009 tanpa beban | 4,89 V | ukur pengguna |
| SIM800L menjawab `AT` | lulus setelah kabel dibetulkan | keluaran serial |
| Registrasi 2G Telkomsel | terdaftar, CSQ sekitar 9–15 di lokasi uji | keluaran serial |
| GPRS dan TCP port 443 | dapat IP dan `CONNECT OK`, **baru satu kali** | keluaran serial |
| TLS dan upload lewat modem | **belum pernah jalan** | - |
| microSD setelah E32 dan modem terpasang | belum dites ulang | - |

- **Uji WiFi hanya menggantikan radio sementara.** Dua bacaan DS18B20 asli tersimpan di server, dengan flag `simulated=true` (flag diverifikasi di kode sketsa).
- **Kabel:** modem awalnya tidak menjawab karena kabel belum tersambung, lalu RST dan GND tertukar. Keduanya sudah dibetulkan (pernyataan pengguna).
- **Daya modem:** registrasi tidak stabil dan modem tampak restart sebelum baterai diganti ke lithium. Setelah itu tidak ada restart selama sekitar 2,5 menit pemantauan. Ini mendukung dugaan lonjakan arus, belum membuktikannya.
- **APN:** tiga pengaturan gagal dan satu berhasil. Belum pasti APN satu-satunya penentu, karena baru sekali berhasil.

## Daya hub (belum diukur)

Perkiraan agent, bukan hasil ukur: upload harian sekitar 68–224 jam, upload tiap jam sekitar 55–180 jam. Perhitungan ini memakai jendela dengar 6 menit, sedangkan firmware masih 10 menit (diverifikasi), jadi angkanya bisa agak optimis. Target 72 jam belum terbukti. Penentu terbesarnya arus tidur rakitan.

Jadwal tetap upload harian pukul 06:00 WIB (diverifikasi di `config.h`). Belum ada keputusan mengubah jadwal atau jenis baterai.

## Pekerjaan berikutnya

1. Cari penyebab LED modem mati dengan mengukur tegangan dari baterai sampai pin modem.
2. Uji TLS dan upload lewat modem, lalu ulangi GPRS beberapa kali.
3. Uji kirim antar board dengan E32 kedua di node, dan uji ulang microSD.
4. Ukur arus tidur rakitan hub, lalu putuskan jadwal upload dan baterai.
5. Pilih kartu lapangan dengan adaptor asli, dan cek data 2G di Tidung.
6. Perbarui `WIRING.md` dan diagram Wokwi. `WIRING.md` belum mengikuti rakitan (diverifikasi), dan menurut catatan sebelumnya repo Wokwi masih Ra-02 dan Air780E.
7. Selesaikan butir lama: batas EIRP 433 MHz, jalur koordinat, serta pembersihan record uji, reader token, perpanjangan token hub, dan sensor nyata dari backend.

## Sumber dan batas bukti

- Catatan sesi di second-brain pribadi (tidak ada di repo ini). Hasil ukur berasal dari pengguna dan tidak diulang dengan alat lain.
- Sinyal yang tercatat berasal dari lokasi uji, bukan Pulau Tidung.
