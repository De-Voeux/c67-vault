from pathlib import Path
import sys,re,json,html,textwrap,hashlib
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,PageBreak,LongTable,TableStyle,KeepTogether,Flowable
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing,Rect,String,Line,Polygon
from reportlab.graphics import renderPDF,renderSVG
from pypdf import PdfReader
OUT=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/private/tmp/seagis-db-build/Seagis-Database/docs/database')
FONT='/System/Library/Fonts/Supplemental/Arial.ttf';BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
pdfmetrics.registerFont(TTFont('Doc',FONT));pdfmetrics.registerFont(TTFont('DocBold',BOLD))
styles=getSampleStyleSheet()
for n in ['Normal','BodyText']:
 styles[n].fontName='Doc';styles[n].fontSize=9;styles[n].leading=13;styles[n].spaceAfter=7
for n,size in [('Title',25),('Heading1',19),('Heading2',15),('Heading3',11),('Heading4',9.5)]:
 styles[n].fontName='DocBold';styles[n].fontSize=size;styles[n].leading=size*1.3;styles[n].spaceBefore=12;styles[n].spaceAfter=8
styles.add(ParagraphStyle('Cell',fontName='Doc',fontSize=7.3,leading=10,wordWrap='CJK',spaceAfter=0))
styles.add(ParagraphStyle('CodeLine',fontName='Doc',fontSize=7.0,leading=9,spaceAfter=0,wordWrap='CJK'))
styles.add(ParagraphStyle('Small',fontName='Doc',fontSize=7,leading=10))
styles.add(ParagraphStyle('CoverSub',fontName='Doc',fontSize=12,leading=19,textColor=colors.HexColor('#46596b')))
W,H=A4; CONTENT=W-88

def inline(s):
 s=html.unescape(s).replace('<br>','\n')
 s=html.escape(s).replace('\n','<br/>')
 s=re.sub(r'`([^`]+)`',lambda m:'<font name="Doc">'+m[1]+'</font>',s)
 s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
 # Relative file hyperlinks are kept as readable labels; TOC is internal and active.
 s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m: '<link href="'+m[2]+'" color="#086b84">'+m[1]+'</link>' if re.match('https?://',m[2]) else m[1],s)
 return s

class Doc(BaseDocTemplate):
 def afterFlowable(self,f):
  if isinstance(f,Paragraph) and getattr(f,'_toc',False):
   level=f._toclevel;text=f.getPlainText();key='b'+str(self.seq.nextf('bookmark'))
   self.canv.bookmarkPage(key);self.canv.addOutlineEntry(text,key,level=level,closed=level>0)
   self.notify('TOCEntry',(level,text,self.page,key))

def footer(canvas,doc):
 canvas.saveState();canvas.setStrokeColor(colors.HexColor('#c9d5df'));canvas.line(44, H-35,W-44,H-35)
 canvas.setFont('Doc',7);canvas.setFillColor(colors.HexColor('#46596b'));canvas.drawString(44,H-27,'SEAGIS  |  Database architecture  |  v1.0.0  |  2026-10-27')
 canvas.drawString(44,24,'Repository + historical catalog audit • Current runtime UNVERIFIED');canvas.drawRightString(W-44,24,str(doc.page));canvas.restoreState()

def box(d,x,y,w,h,label,body=(),font=7):
 d.add(Rect(x,y,w,h,fillColor=colors.HexColor('#f0f7fa'),strokeColor=colors.HexColor('#7996a8'),radius=4))
 d.add(Rect(x,y+h-23,w,23,fillColor=colors.HexColor('#0c4e68'),strokeColor=None))
 labelsize=min(8.2,(w-12)/max(1,pdfmetrics.stringWidth(label,'DocBold',1)))
 d.add(String(x+6,y+h-15,label,fontName='DocBold',fontSize=labelsize,fillColor=colors.white))
 for i,line in enumerate(body):d.add(String(x+6,y+h-36-i*10,line,fontName='Doc',fontSize=font,fillColor=colors.HexColor('#193549')))

def arrow(d,x1,y1,x2,y2):
 d.add(Line(x1,y1,x2,y2,strokeColor=colors.HexColor('#59899b'),strokeWidth=1))
 if x2>x1:d.add(Polygon([x2,y2,x2-5,y2+3,x2-5,y2-3],fillColor=colors.HexColor('#59899b'),strokeColor=None))
 else:d.add(Polygon([x2,y2,x2-3,y2+5,x2+3,y2+5],fillColor=colors.HexColor('#59899b'),strokeColor=None))

def flowdiagram(code):
 nodes=re.findall(r'^\s*(\w+)\["([^"\n]+)"\]',code,re.M);edges=re.findall(r'^\s*(\w+) --> (\w+)',code,re.M)
 n=len(nodes);rows=(n+1)//2;bh=44;gap=28;h=rows*(bh+gap)+20;d=Drawing(CONTENT,h);pos={}
 for i,(key,label) in enumerate(nodes):
  row=i//2;col=i%2;x=8+col*(CONTENT/2);y=h-20-(row+1)*bh-row*gap;w=CONTENT/2-25
  box(d,x,y,w,bh,label);pos[key]=(x,y,w,bh)
 for a,b in edges:
  if a not in pos or b not in pos:continue
  x,y,w,bh=pos[a];xx,yy,ww,hh=pos[b]
  if abs(yy-y)<1:arrow(d,x+w,y+bh/2,xx,yy+hh/2)
  else:arrow(d,x+w/2,y,xx+ww/2,yy+hh)
 return [d]

meta=json.loads((OUT/'assets/evidence/schema-metadata-20261022.json').read_text());objects={o['schema']+'.'+o['name']:o for o in meta['objects']}
def erddiagrams(code):
 # Reproducible table-centred ER panels: every field and outgoing FK is drawn.
 names=re.findall(r'^\s*\w+\["([\w.]+)"\] \{',code,re.M)
 fks=[f for f in meta['constraints'] if f['kind']=='f'];result=[]
 for name in names:
  cols=[c for c in meta['columns'] if c['schema']+'.'+c['table_name']==name]
  rels=[f for f in fks if f['schema']+'.'+f['table_name']==name]
  cc=[c for c in meta['constraints'] if c['schema']+'.'+c['table_name']==name]
  bheight=max(58,38+len(cols)*10);rh=max(52,26+len(rels)*34);height=max(bheight,rh)+15
  d=Drawing(CONTENT,height);body=[]
  for c in cols:
   mark=[]
   if any(x['kind']=='p' and c['name'] in x['columns'] for x in cc):mark.append('PK')
   if any(x['kind']=='f' and c['name'] in x['columns'] for x in cc):mark.append('FK')
   typ=c['type'].replace('timestamp with time zone','timestamptz').replace('seagis.finite_float','finite_float').replace('double precision','float8')
   line=c['name']+' : '+typ+(' ['+','.join(mark)+']' if mark else '')
   body.append(line)
  leftw=CONTENT*.58
  # Fit longest field without shrinking all dictionary text.
  font=min(7.2,(leftw-12)/max(pdfmetrics.stringWidth(t,'Doc',1) for t in body))
  box(d,0,height-bheight-5,leftw,bheight,name,body,font)
  if not rels:
   d.add(String(leftw+18,height-30,'No outgoing physical FK',fontName='Doc',fontSize=7.0))
  for j,f in enumerate(rels):
   target=f['target_schema']+'.'+f['target_table'];y=height-40-j*34
   d.add(Rect(leftw+30,y-13,CONTENT-leftw-32,27,fillColor=colors.HexColor('#f8f3e8'),strokeColor=colors.HexColor('#c2ab75')))
   fontsize=min(7.1,(CONTENT-leftw-40)/max(1,pdfmetrics.stringWidth(target,'DocBold',1)))
   d.add(String(leftw+34,y+2,target,fontName='DocBold',fontSize=fontsize))
   keystr=','.join(f['columns']);nullable=any(not c['not_null'] for c in cols if c['name'] in f['columns'])
   unique=any(c['kind'] in ['p','u'] and set(c['columns']).issubset(set(f['columns'])) for c in cc)
   card=('0..1' if nullable else '1')+' parent / '+('0..1' if unique else '0..N')+' child'
   d.add(String(leftw+34,y-8,card,fontName='Doc',fontSize=6.5));arrow(d,leftw,y,leftw+30,y)
  result.append(d)
 return result

# Save standalone PDF/SVG renderings. The mmd files remain the canonical diagrams.
for mmd in sorted((OUT/'assets/diagrams').glob('*.mmd')):
 src=mmd.read_text();drawings=erddiagrams(src) if src.startswith('erDiagram') else flowdiagram(src)
 for i,d in enumerate(drawings,1):
  stem=mmd.stem+(f'-{i:02d}' if len(drawings)>1 else '')
  renderPDF.drawToFile(d,str(OUT/f'assets/diagrams/{stem}.pdf'))
  renderSVG.drawToFile(d,str(OUT/f'assets/diagrams/{stem}.svg'))

class ValidationTable(LongTable):pass

def make_table(lines):
 rows=[]
 for ln in lines:
  cells=[x.strip() for x in ln.strip().strip('|').split('|')]
  if cells and all(re.fullmatch(r':?-+:?',x) for x in cells):continue
  rows.append(cells)
 if not rows:return []
 nc=max(len(r) for r in rows);rows=[r+['']*(nc-len(r)) for r in rows]
 if nc==2:widths=[CONTENT*.25,CONTENT*.75]
 elif nc==3:widths=[CONTENT*.24,CONTENT*.25,CONTENT*.51]
 else:
  # Wide Markdown tables are transposed into keyed record blocks in PDF.
  # This preserves every field and avoids unreadable 7-9-column pages.
  out=[]
  for row in rows[1:]:
   pairs=[[Paragraph(inline(k),styles['Cell']),Paragraph(inline(v),styles['Cell'])] for k,v in zip(rows[0],row)]
   t=LongTable(pairs,colWidths=[CONTENT*.25,CONTENT*.75],hAlign='LEFT')
   t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(0,-1),colors.HexColor('#edf4f7')),('GRID',(0,0),(-1,-1),.2,colors.HexColor('#c7d4dd')),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]));out.extend([t,Spacer(1,7)])
  return out
 data=[[Paragraph(inline(v),styles['Cell']) for v in r] for r in rows]
 t=LongTable(data,colWidths=widths,repeatRows=1,hAlign='LEFT',splitInRow=1)
 t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dcebf1')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f6f9fb')]),('GRID',(0,0),(-1,-1),.2,colors.HexColor('#c7d4dd')),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
 return [t,Spacer(1,8)]

stats={}
for lang,name in [('id','DOKUMENTASI_DATABASE'),('en','DATABASE_DOCUMENTATION')]:
 path=OUT/lang/(name+'.pdf');md=(OUT/lang/(name+'.md')).read_text();lines=md.splitlines();story=[]
 story+=[Spacer(1,90),Paragraph('SEAGIS',styles['Title']),Spacer(1,20),Paragraph('Arsitektur Database,<br/>Lineage dan Kontrak Data' if lang=='id' else 'Database Architecture,<br/>Data Lineage and Contracts',styles['Title']),Spacer(1,25),Paragraph('Bahasa Indonesia' if lang=='id' else 'English',styles['CoverSub']),Spacer(1,18),Paragraph('Version 1.0.0<br/>27 October 2026 / Asia Jakarta<br/>Catalog snapshot: 22 October 2026',styles['CoverSub']),Spacer(1,30),Paragraph('Audit kode dan snapshot historis. Runtime terkini belum diverifikasi.' if lang=='id' else 'Code and historical-snapshot audit. Current runtime is unverified.',styles['CoverSub']),PageBreak()]
 story.append(Paragraph('Daftar Isi' if lang=='id' else 'Table of Contents',styles['Heading1']));toc=TableOfContents();toc.levelStyles=[ParagraphStyle('toc0',fontName='Doc',fontSize=10,leading=17,spaceBefore=5),ParagraphStyle('toc1',fontName='Doc',fontSize=8,leading=12,leftIndent=10)]
 story.extend([toc,PageBreak()]);i=0;skip_toc=False;diagram_count=0
 while i<len(lines):
  line=lines[i]
  if line.startswith('# '):i+=1;continue
  if line.startswith('## ') and ('Daftar Isi' in line or 'Table of Contents' in line):
   i+=1
   while i<len(lines) and not lines[i].startswith('## '):i+=1
   continue
  if line.startswith('```'):
   kind=line[3:].strip();buf=[];i+=1
   while i<len(lines) and not lines[i].startswith('```'):buf.append(lines[i]);i+=1
   text='\n'.join(buf)
   if kind=='mermaid':
    drawings=erddiagrams(text) if text.startswith('erDiagram') else flowdiagram(text)
    for d in drawings:story.extend([d,Spacer(1,12)]);diagram_count+=1
   else:
    for row in buf:
     # Wrap long code lines into paragraphs; all text remains extractable.
     for chunk in textwrap.wrap(row,100,replace_whitespace=False,drop_whitespace=False) or [' ']:story.append(Paragraph(html.escape(chunk).replace(' ','&#160;'),styles['CodeLine']))
    story.append(Spacer(1,8))
   i+=1;continue
  if line.startswith('|'):
   buf=[]
   while i<len(lines) and lines[i].startswith('|'):buf.append(lines[i]);i+=1
   story.extend(make_table(buf));continue
  if line.startswith('#'):
   level=len(line)-len(line.lstrip('#'));text=line[level:].strip()
   if level==2 and re.match(r'\d+ ',text):
    story.append(PageBreak());p=Paragraph(inline(text),styles['Heading1']);p._toc=True;p._toclevel=0
   elif level==3:
    p=Paragraph(inline(text),styles['Heading2']);p._toc=True;p._toclevel=1
   elif level==4:p=Paragraph(inline(text),styles['Heading3'])
   else:p=Paragraph(inline(text),styles['Heading4'])
   story.append(p);i+=1;continue
  if not line.strip():i+=1;continue
  buf=[line];i+=1
  while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||```)',lines[i]):buf.append(lines[i]);i+=1
  story.append(Paragraph(inline(' '.join(buf)),styles['BodyText']))
 doc=Doc(str(path),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=48,bottomMargin=42,title='SEAGIS '+name,author='SEAGIS documentation audit',allowSplitting=1)
 doc.addPageTemplates(PageTemplate(id='normal',frames=[Frame(44,42,CONTENT,H-90,leftPadding=0,bottomPadding=0,rightPadding=0,topPadding=0)],onPage=footer))
 doc.multiBuild(story,maxPasses=4)
 reader=PdfReader(path);text='\n'.join(p.extract_text() or '' for p in reader.pages)
 assert len(reader.pages)>13
 assert len(reader.outline)>=13
 assert 'seagis.observation.observed_at' in text
 assert 'F08' in text
 stats[lang]={'pdf_pages':len(reader.pages),'pdf_bytes':path.stat().st_size,'rendered_diagram_panels':diagram_count,'outline_entries':len(reader.outline),'pdf_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'chapters':13,'extractable_text_characters':len(text)}
 print(lang,stats[lang])
(OUT/'assets/generated/pdf-validation.json').write_text(json.dumps(stats,indent=2)+'\n')
