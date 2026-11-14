#!/usr/bin/env python3
"""Build the vault's A0-A3 guide and vector SVG diagrams with ReportLab.

Requires reportlab. Run with the bundled Codex Python or another Python that
provides ReportLab. No network, credentials, live data or pipeline execution.
Markdown is the source of prose; diagram specifications below are shared by
the embedded SVGs and the PDF. Outputs are relative to this file.
"""
from pathlib import Path
from html import escape
import math
import re

from reportlab.graphics import renderSVG
from reportlab.graphics.shapes import Drawing, Rect, Line, Polygon, String
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    Preformatted,
)

BASE = Path(__file__).resolve().parent
NOTE = BASE / 'Pipeline Seagis A0-A3 - Alur dan Skematik.md'
PDF = BASE / 'output/pdf/Seagis - Pipeline A0-A3.pdf'
ASSETS = BASE / 'assets'
INK = '#15363E'
TEAL = '#167C74'
BLUE = '#3D68A2'
MUTED = '#546970'
PALE = '#EDF6F3'
BLUE_PALE = '#EEF3FA'
AMBER = '#946323'
AMBER_PALE = '#FAF3E8'
BORDER = '#CDDDDB'


def fonts():
    font_dir = Path('/System/Library/Fonts/Supplemental')
    candidates = [
        (font_dir / 'Arial.ttf', font_dir / 'Arial Bold.ttf'),
        (Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),
         Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')),
    ]
    for regular, bold in candidates:
        if regular.exists() and bold.exists():
            pdfmetrics.registerFont(TTFont('Guide', str(regular)))
            pdfmetrics.registerFont(TTFont('GuideBold', str(bold)))
            pdfmetrics.registerFontFamily('Guide', normal='Guide', bold='GuideBold',
                                         italic='Guide', boldItalic='GuideBold')
            return
    raise RuntimeError('Install Arial or DejaVu Sans before building the PDF.')


def wrap(text, width, font='Guide', size=9):
    lines, current = [], ''
    for word in text.split():
        candidate = (current + ' ' + word).strip()
        if current and pdfmetrics.stringWidth(candidate, font, size) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


class Diagram:
    def __init__(self, height):
        self.height = height
        self.d = Drawing(499, height)
        self.d.add(Rect(0, 0, 499, height, fillColor=colors.HexColor('#FBFDFC'),
                        strokeColor=colors.HexColor(BORDER), strokeWidth=.6,
                        rx=7, ry=7))

    def text(self, x, top, text, size=9, color=MUTED, bold=False, anchor='start'):
        self.d.add(String(x, self.height-top, text, fontName='GuideBold' if bold else 'Guide',
                          fontSize=size, fillColor=colors.HexColor(color), textAnchor=anchor))

    def box(self, x, top, w, h, title, body='', kind='cloud', future=False):
        line, fill = (BLUE, BLUE_PALE) if kind == 'mac' else (TEAL, PALE)
        if future:
            line, fill = AMBER, AMBER_PALE
        rect = Rect(x, self.height-top-h, w, h, rx=5, ry=5,
                    fillColor=colors.HexColor(fill), strokeColor=colors.HexColor(line), strokeWidth=.8)
        if future:
            rect.strokeDashArray = [4, 3]
        self.d.add(rect)
        ts = wrap(title, w-16, 'GuideBold', 10)
        bs = wrap(body, w-16, 'Guide', 8.5)
        total = len(ts)*12 + len(bs)*10
        if total > h-8:
            raise ValueError(f'Diagram node is too short: {title}')
        y = top + (h-total)/2 + 9
        for s in ts:
            self.text(x+8, y, s, 10, INK, True); y += 12
        for s in bs:
            self.text(x+8, y, s, 8.5, MUTED); y += 10

    def arrow(self, points, dashed=False, color=MUTED):
        for (x1,y1),(x2,y2) in zip(points,points[1:]):
            ln = Line(x1,self.height-y1,x2,self.height-y2,
                      strokeColor=colors.HexColor(color),strokeWidth=.95)
            if dashed:
                ln.strokeDashArray = [3,3]
            self.d.add(ln)
        (x0,y0),(x1,y1)=points[-2:]
        theta=math.atan2(y1-y0,x1-x0)
        length=5
        a=(x1-length*math.cos(theta)+2.5*math.sin(theta),
           y1-length*math.sin(theta)-2.5*math.cos(theta))
        b=(x1-length*math.cos(theta)-2.5*math.sin(theta),
           y1-length*math.sin(theta)+2.5*math.cos(theta))
        self.d.add(Polygon([x1,self.height-y1,a[0],self.height-a[1],b[0],self.height-b[1]],
                           fillColor=colors.HexColor(color),strokeColor=None))


def diagrams():
    ds = {}
    d = Diagram(279)
    for x in (125,374):
        d.arrow([(x,50),(x,63)])
        d.arrow([(x,105),(x,118)])
    d.arrow([(125,160),(125,169),(249,169),(249,179)])
    d.arrow([(374,160),(374,169),(249,169)])
    d.arrow([(249,219),(249,231)])
    d.box(14,10,222,40,'Simulator / IoT','A1: suhu per sensor; hardware kelak',kind='mac')
    d.box(263,10,222,40,'Copernicus / Open-Meteo','A2: keluaran model regional asli')
    d.box(14,63,222,42,'Edge + SQL API | Supabase','HTTPS, auth, dedup, QC awal')
    d.box(263,63,222,42,'Python A2 | Mac','LaunchAgent 15 menit; fetch bila due',kind='mac')
    d.box(14,118,222,42,'seagis.observation','Sensor/plot + ingestion/raw/quality')
    d.box(263,118,222,42,'forecast_run / forecast_value','Grid + vintage + manifest regional')
    d.box(106,179,286,40,'Python A3 | Mac, on demand','Cutoff per jam, QA, mapping dan cadence',kind='mac')
    d.box(106,231,286,38,'seagis_quality | Supabase','Snapshot + report + lineage; review only')
    ds['01-overview'] = d.d

    d = Diagram(288)
    d.box(14,10,471,38,'Registry A0: source / dataset / parameter / dataset_parameter',
          'Kontrak identitas, versi, cadence, unit dan konversi')
    d.arrow([(125,48),(125,61)])
    d.arrow([(374,48),(374,61)])
    d.box(14,61,222,38,'ingestion_run','Request / adapter / status / waktu')
    d.box(263,61,222,38,'source_grid + mapping','Sel dataset/depth; plot ke grid')
    d.arrow([(125,99),(125,112)])
    d.arrow([(485,80),(493,80),(493,185),(485,185)])
    d.box(14,112,222,40,'seagis_raw.raw_payload','Manifest, receipt, digest dan lisensi')
    d.arrow([(236,132),(263,132)])
    d.box(263,112,222,40,'forecast_run','Capture/vintage regional')
    d.arrow([(125,152),(125,165)])
    d.arrow([(374,152),(374,165)])
    d.box(14,165,222,40,'observation + plot / sensor','Nilai lokal, observed_at, quality')
    d.box(263,165,222,40,'forecast_value + source_grid','Nilai model per valid_at')
    d.arrow([(125,205),(125,216),(249,216),(249,228)])
    d.arrow([(374,205),(374,216),(249,216)])
    d.box(73,228,353,41,'alignment_snapshot + snapshot_input | A3',
          'FK input + hash; quality_event tetap sebagai audit sumber')
    d.text(249,281,'Ringkasan lineage; seluruh FK tersedia pada Peta Database.',8,anchor='middle')
    ds['02-lineage'] = d.d

    d = Diagram(259)
    d.box(14,10,222,42,'Simulator A1 | Mac','Paket sintetis melalui HTTP',kind='mac')
    d.box(263,10,222,42,'Receiver IoT | kelak','UTC, queue persisten, boot + sequence',future=True)
    d.arrow([(125,52),(125,63),(249,63),(249,76)])
    d.arrow([(374,52),(374,63),(249,63)],dashed=True)
    d.box(53,76,393,39,'HTTPS POST /v1/ingest | Edge temperature',
          'Bearer device token; satu sensor / satu paket')
    d.arrow([(249,115),(249,128)])
    d.box(53,128,393,40,'SQL privat | seagis_api.ingest',
          'Auth + binding + rate limit + digest + QC + lock')
    d.arrow([(249,168),(249,181)])
    d.box(14,181,471,40,'Transaksi PostgreSQL | Supabase',
          'ingestion + raw + observation + quality_event + packet_receipt')
    d.text(249,238,'201 stored / 200 duplicate: acknowledge; 409: karantina konflik.',9,anchor='middle')
    d.text(249,251,'GET history / status memakai reader token dengan scope plot.',9,anchor='middle')
    ds['03-iot'] = d.d

    d = Diagram(274)
    d.box(14,10,222,42,'Dispatcher Python | Mac','Tick 15 menit; cek due',kind='mac')
    d.arrow([(236,31),(263,31)])
    d.box(263,10,222,42,'claim() | Supabase','State per dataset; lease 20 menit')
    d.arrow([(374,52),(374,62),(125,62),(125,77)])
    d.box(14,77,222,43,'Provider / adapter | Mac','Copernicus Toolbox / GFS JSON',kind='mac')
    d.arrow([(236,98),(263,98)])
    d.box(263,77,222,43,'Parse / normalize / validate','Identitas, unit, time, depth, mask',kind='mac')
    d.arrow([(374,120),(374,138)])
    d.box(263,138,222,43,'persist() | Supabase','Atomic; digest sama = vintage sama')
    d.arrow([(263,159),(236,159)])
    d.box(14,138,222,43,'Manifest + run + grid + values','Metadata only; normalized retained')
    d.arrow([(125,181),(125,204)])
    d.box(14,204,222,43,'preview() + demo mapping','As-of, attribution, cache age')
    d.box(263,204,222,43,'Failure -> finish_failure()','Backoff / status; data lama tetap')
    d.arrow([(485,98),(493,98),(493,225),(485,225)],dashed=True,color=AMBER)
    d.text(249,263,'DB menyimpan state; Mac yang mengeksekusi fetch. Tick bukan cadence nilai.',8.3,anchor='middle')
    ds['04-regional'] = d.d

    d = Diagram(264)
    d.text(125,19,'SUPABASE | fungsi privat',10,TEAL,True,anchor='middle')
    d.text(374,19,'MAC | Python on demand',10,BLUE,True,anchor='middle')
    d.box(14,32,222,48,'source_bundle()','Observasi, model, mapping, registry; hash')
    d.arrow([(236,56),(263,56)])
    d.box(263,32,222,48,'Builder QC + alignment','Jam UTC; cutoff; policy + code hash',kind='mac')
    d.arrow([(374,80),(374,103)])
    d.box(263,103,222,48,'Dokumen + quality report','Output lokal; review per plot/jam',kind='mac')
    d.arrow([(263,127),(236,127)])
    d.text(249,96,'--persist',8,anchor='middle')
    d.box(14,103,222,48,'save_snapshot()','Re-read source; guard nilai / waktu / FK')
    d.arrow([(125,151),(125,181)])
    d.box(14,181,222,48,'Snapshot + snapshot_input','Append-only; hash body/manifest')
    d.arrow([(236,205),(263,205)])
    d.box(263,181,222,48,'snapshot() / readback','ID sama pada replay identik',kind='mac')
    d.text(249,249,'Semua hasil: training_authorized=false. Offline tidak dapat persist cloud.',8.5,anchor='middle')
    ds['05-alignment'] = d.d

    d = Diagram(218)
    d.text(16,23,'Ilustrasi WIB | jarak gambar tidak menunjukkan durasi proporsional',9,INK,True)
    d.arrow([(35,66),(470,66)])
    for x,label,body in [(65,'09:00','Diukur'),(210,'09:05','Diterima/ingest'),(440,'10:00','Cutoff berikut')]:
        d.d.add(Line(x,d.height-58,x,d.height-75,strokeColor=colors.HexColor(INK),strokeWidth=1))
        d.text(x,48,label,10,INK,True,anchor='middle')
        d.text(x,91,body,8.5,anchor='middle')
    d.box(14,113,222,57,'Cutoff 09:00 -> belum tersedia',
          'Receipt 09:05 melewati cutoff. Baris 09:00 tidak memakai paket.',future=True)
    d.box(263,113,222,57,'Cutoff 10:00 -> kandidat konteks',
          'Sudah tersedia, umur 60 menit. Tetap harus lolos cadence dan QC.')
    d.text(249,194,'observed_at berbeda dari ingested_at; histori tidak di-backdate.',9,INK,anchor='middle')
    d.text(249,209,'Paket ilustratif; tidak menyatakan hardware sudah mengirim data nyata.',8,anchor='middle')
    ds['06-cutoff'] = d.d
    return ds


def inline(text):
    # Resolve human-readable vault labels; PDF has no dependency on Obsidian.
    text = re.sub(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]',
                  lambda m: m.group(2) or m.group(1), text)
    chunks = re.split(r'(`[^`]+`)', text)
    result = ''
    for part in chunks:
        if part.startswith('`') and part.endswith('`'):
            token=escape(part[1:-1])
            # Allow long identifiers/paths to wrap without altering extracted text.
            for char in ('/', '_', '.'):
                token=token.replace(char,char+'<wbr/>')
            result += '<font name="Courier" size="8.2">'+token+'</font>'
        else:
            part=escape(part)
            part=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',part)
            result += part
    return result


def styles():
    s=getSampleStyleSheet()
    s.add(ParagraphStyle('GuideBody',fontName='Guide',fontSize=9.8,leading=13.1,
                         textColor=colors.HexColor(INK),spaceAfter=7,
                         allowWidows=0,allowOrphans=0))
    s.add(ParagraphStyle('GuideSection',fontName='GuideBold',fontSize=20,leading=24,
                         textColor=colors.HexColor(INK),spaceAfter=12,keepWithNext=True))
    s.add(ParagraphStyle('GuideTable',fontName='Guide',fontSize=9,leading=11.5,
                         textColor=colors.HexColor(INK),spaceAfter=0))
    s.add(ParagraphStyle('GuideHead',parent=s['GuideTable'],fontName='GuideBold',
                         textColor=colors.white))
    s.add(ParagraphStyle('GuideCode',fontName='Courier',fontSize=7.9,leading=11,
                         textColor=colors.HexColor(INK),backColor=colors.HexColor(BLUE_PALE),
                         borderPadding=8,spaceBefore=3,spaceAfter=10))
    s.add(ParagraphStyle('GuideBullet',parent=s['GuideBody'],leftIndent=12,
                         firstLineIndent=-8,spaceAfter=5))
    return s


class GuideDoc(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name=='GuideSection':
            title=flowable.getPlainText()
            key='section-'+title.split(' ')[0]
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title,key,level=0,closed=False)


def page(canvas, doc):
    w,h=A4
    canvas.saveState()
    canvas.setFillColor(colors.HexColor(TEAL))
    canvas.rect(0,h-7,w,7,fill=1,stroke=0)
    canvas.setFont('GuideBold',9)
    canvas.drawString(48,h-32,'SEAGIS / ENGINEERING')
    canvas.setFont('Guide',8.5)
    canvas.setFillColor(colors.HexColor(MUTED))
    canvas.drawRightString(w-48,h-32,'PIPELINE A0-A3 | 22 OKTOBER 2026')
    canvas.setStrokeColor(colors.HexColor(BORDER))
    canvas.line(48,40,w-48,40)
    canvas.setFont('Guide',8)
    canvas.drawString(48,26,'Development / demo review | Basis kode e93a005')
    canvas.drawRightString(w-48,26,str(doc.page))
    canvas.restoreState()


def build():
    fonts()
    ASSETS.mkdir(parents=True,exist_ok=True)
    PDF.parent.mkdir(parents=True,exist_ok=True)
    ds=diagrams()
    for name,drawing in ds.items():
        target=ASSETS/(name+'.svg')
        renderSVG.drawToFile(drawing,str(target))
        # PDF embeds the registered TTF. SVG needs a portable system font name.
        svg=target.read_text()
        svg=svg.replace('font-family: GuideBold;',
                        'font-family: Arial, Helvetica, sans-serif; font-weight: bold;')
        svg=svg.replace('font-family: Guide;',
                        'font-family: Arial, Helvetica, sans-serif;')
        svg=svg.replace('<title>...</title>',f'<title>Seagis A0-A3 / {name}</title>')
        svg=svg.replace('<desc>...</desc>',
                        '<desc>Diagram engineering berdasarkan implementasi e93a005. '
                        'Biru: proses Mac. Hijau: sumber atau layanan/data cloud. '
                        'Amber putus-putus: jalur kelak atau kegagalan.</desc>')
        svg=re.sub(r'<!DOCTYPE.*?>\s*','',svg,flags=re.S)
        target.write_text(svg)
    lines=NOTE.read_text().splitlines()
    start=next(i for i,l in enumerate(lines) if l.startswith('## 01'))
    lines=lines[start:]
    s=styles(); story=[]; i=0; section_count=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:
            i+=1; continue
        if line.startswith('## '):
            if section_count:
                story.append(PageBreak())
            section_count+=1
            story.append(Paragraph(inline(line[3:]),s['GuideSection']))
            i+=1;continue
        if line.startswith('![['):
            name=line[3:-2].removesuffix('.svg')
            story.extend([ds[name],Spacer(1,12)])
            i+=1;continue
        if line.startswith('```'):
            i+=1; code=[]
            while i<len(lines) and not lines[i].startswith('```'):
                code.append(lines[i]);i+=1
            # Fold only command display at spaces if needed; keep example code exact.
            story.append(Preformatted('\n'.join(code),s['GuideCode']))
            i+=1;continue
        if line.startswith('|'):
            raw=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[:\- ]+',c) for c in cells):
                    raw.append(cells)
                i+=1
            count=len(raw[0])
            # Most tables are explanatory, with a shorter identifier column.
            ratios={2:[.32,.68],3:[.24,.35,.41],4:[.25,.27,.27,.21]}[count]
            data=[[Paragraph(inline(c),s['GuideHead'] if r==0 else s['GuideTable'])
                   for c in row] for r,row in enumerate(raw)]
            table=Table(data,colWidths=[499*r for r in ratios],repeatRows=1,hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(-1,0),colors.HexColor(TEAL)),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#F0F6F4'),colors.white]),
                ('VALIGN',(0,0),(-1,-1),'TOP'),
                ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
                ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
                ('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor(BORDER)),
            ]))
            story.extend([table,Spacer(1,10)])
            continue
        if line.startswith('- '):
            story.append(Paragraph('- '+inline(line[2:]),s['GuideBullet']))
            i+=1;continue
        parts=[line];i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('## ','|','```','![[','- ')):
            parts.append(lines[i].strip());i+=1
        story.append(Paragraph(inline(' '.join(parts)),s['GuideBody']))
    doc=GuideDoc(str(PDF),pagesize=A4,rightMargin=48,leftMargin=48,
                 topMargin=59,bottomMargin=53,title='Seagis - Pipeline A0-A3',
                 author='Seagis Engineering',subject='Alur data, runtime, akses dan QC A0-A3')
    doc.build(story,onFirstPage=page,onLaterPages=page)
    print(f'Created {PDF.name} and {len(ds)} SVG diagrams from {section_count} chapters.')


if __name__=='__main__':
    build()
