import json
from pathlib import Path

root = Path(__file__).resolve().parent
def stamp(t):
    total = round(t * 1000)
    h, rem = divmod(total, 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return f'{h:02}:{m:02}:{s:02}.{ms:03}'

combined = ['# 08-Sumber dan Arsip/Transkrip Samudrajaya', '', 'Draf transkripsi otomatis seluruh kedua rekaman, tanpa identifikasi pembicara. Belum diperiksa dengan mendengarkan, sehingga belum dapat dianggap transkrip verbatim terverifikasi. Kata pengisi, nama, istilah, suara jauh, dan percakapan bertumpuk bisa salah atau terlewat. Timestamp merupakan estimasi model dan dimulai dari nol untuk masing-masing file. Tanda [perlu cek audio] menunjukkan sebagian hasil yang keyakinan modelnya rendah; hasil tanpa tanda juga belum diverifikasi.', '']
allwords = ['TRANSKRIP PER KATA — DRAF OTOMATIS', 'Timestamp merupakan estimasi; ucapan dan waktu belum diverifikasi dengan mendengarkan.', '[?] = keyakinan model rendah. Tidak adanya tanda bukan jaminan kata benar.', '']
for name in ['Samudrajaya', 'Samudrajaya 2']:
    data = json.loads((root / f'{name}.json').read_text())
    segments = data['segments']
    assert len(list((root / 'data' / name).glob('*.json'))) == (int(data['duration']) + 599) // 600
    combined.extend([f'## {name}.m4a', '', f"Durasi file: {stamp(data['duration'])}", ''])
    allwords.extend([f'=== {name}.m4a ===', ''])
    count = 0
    previous = 0
    for seg in segments:
        assert 0 <= seg['start'] <= seg['end'] <= data['duration'] + 0.1
        assert seg['start'] >= previous - 0.1
        previous = seg['start']
        low = seg.get('avg_logprob', 0) < -0.55 or any(w.get('probability', 1) < 0.35 for w in seg.get('words', []))
        combined.extend([f"[{stamp(seg['start'])} – {stamp(seg['end'])}] {'[perlu cek audio] ' if low else ''}{seg['text'].strip()}", ''])
        for w in seg.get('words', []):
            allwords.append(f"[{stamp(w['start'])} – {stamp(w['end'])}] {w['word'].strip()}{' [?]' if w.get('probability', 1) < 0.5 else ''}")
            count += 1
    print(name, 'duration', data['duration'], 'segments', len(segments), 'word_tokens', count, 'last_timestamp', segments[-1]['end'])
    allwords.append('')
(root / 'Transkrip lengkap.md').write_text('\n'.join(combined))
(root / 'Transkrip per kata.txt').write_text('\n'.join(allwords))
