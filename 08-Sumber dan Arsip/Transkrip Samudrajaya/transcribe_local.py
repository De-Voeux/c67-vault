import json
import os
import subprocess
from pathlib import Path
import numpy as np
import mlx_whisper

ROOT = Path(os.environ.get('TRANSCRIPT_OUTPUT', str(Path(__file__).resolve().parent)))
ROOT.mkdir(parents=True, exist_ok=True)
MODEL = os.environ.get('TRANSCRIPT_MODEL', '/private/tmp/samudrajaya-model')
FILES = [Path('/Users/cindyram/Downloads/Samudrajaya.m4a'), Path('/Users/cindyram/Downloads/Samudrajaya 2.m4a')]

def stamp(t, ms=False):
    total = round(t * 1000)
    h, rest = divmod(total, 3600000)
    m, rest = divmod(rest, 60000)
    s, milli = divmod(rest, 1000)
    return f'{h:02}:{m:02}:{s:02}' + (f'.{milli:03}' if ms else '')

for source in FILES:
    name = source.stem
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(source), '-f', 'f32le', '-ac', '1', '-ar', '16000', '-'])
    samples = np.frombuffer(raw, dtype=np.float32).copy()
    del raw
    chunks = ROOT / 'data' / name
    chunks.mkdir(parents=True, exist_ok=True)
    segments = []
    for offset in range(0, len(samples), 600 * 16000):
        start = offset / 16000
        target = chunks / f'{int(start):06}.json'
        if target.exists():
            result = json.loads(target.read_text())
        else:
            print(f'START {name} {stamp(start)}', flush=True)
            result = mlx_whisper.transcribe(
                samples[offset:offset + 600 * 16000],
                path_or_hf_repo=MODEL,
                language='id', task='transcribe', word_timestamps=True,
                verbose=False, condition_on_previous_text=False,
                temperature=(0.0, 0.2, 0.4),
            )
            target.write_text(json.dumps(result, ensure_ascii=False, indent=2))
        for segment in result['segments']:
            segment['start'] += start
            segment['end'] += start
            for word in segment.get('words', []):
                word['start'] += start
                word['end'] += start
            segments.append(segment)
        print(f'DONE {name} through {stamp(min((offset + 600 * 16000) / 16000, len(samples) / 16000))}', flush=True)
        (ROOT / f'{name}.json').write_text(json.dumps({'source': str(source), 'duration': len(samples)/16000, 'segments': segments}, ensure_ascii=False, indent=2))
        lines = [f'# {name} — transkrip otomatis', '', 'Timestamp dihitung dari awal file ini. Ejaan, kata pengisi, bagian tumpang tindih, dan ucapan kurang jelas belum diverifikasi dengan mendengarkan. Nama pembicara tidak ditentukan.', '']
        words = ['mulai\tselesai\tkata\tprobabilitas_model']
        subtitles = []
        for i, segment in enumerate(segments, 1):
            text = segment['text'].strip()
            uncertain = segment.get('avg_logprob', 0) < -0.8
            lines.append(f"[{stamp(segment['start'], True)} – {stamp(segment['end'], True)}] {'[perlu cek audio] ' if uncertain else ''}{text}")
            lines.append('')
            subtitles.append(f"{i}\n{stamp(segment['start'], True).replace('.', ',')} --> {stamp(segment['end'], True).replace('.', ',')}\n{text}\n")
            for word in segment.get('words', []):
                words.append(f"{stamp(word['start'], True)}\t{stamp(word['end'], True)}\t{word['word'].strip()}\t{word.get('probability', '')}")
        (ROOT / f'{name}.md').write_text('\n'.join(lines))
        (ROOT / f'{name} - per kata.tsv').write_text('\n'.join(words))
        (ROOT / f'{name}.srt').write_text('\n'.join(subtitles))
    print(f'COMPLETE {name}', flush=True)
