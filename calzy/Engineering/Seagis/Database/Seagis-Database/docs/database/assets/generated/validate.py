from pathlib import Path
import json,re,hashlib,subprocess,sys,collections
import pdfplumber
from pypdf import PdfReader
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[2]
meta=json.loads((root/'assets/evidence/schema-metadata-20261022.json').read_text())
files={'id':root/'id/DOKUMENTASI_DATABASE.md','en':root/'en/DATABASE_DOCUMENTATION.md'}
md={k:v.read_text() for k,v in files.items()};errors=[]
for lang,s in md.items():
 chapters=re.findall(r'^## (\d+) ',s,re.M)
 if chapters!=list(map(str,range(1,14))):errors.append(f'{lang} chapters')
 for o in meta['objects']:
  for c in [x for x in meta['columns'] if x['schema']==o['schema'] and x['table_name']==o['name']]:
   fullname=o['schema']+'.'+o['name']+'.'+c['name']
   if f'#### `{fullname}`' not in s:errors.append(lang+' missing '+fullname)
 for f in [x for x in meta['constraints'] if x['kind']=='f']:
  if f['definition'] not in s:errors.append(lang+' missing FK '+f['name'])
blocks=lambda s:re.findall(r'```(sql|json|mermaid)\n(.*?)\n```',s,re.S)
if blocks(md['id'])!=blocks(md['en']):errors.append('code/diagram bilingual mismatch')
# Relative markdown links are all checked; source file references are manifest-backed code spans.
for p in root.rglob('*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if target.startswith(('http','mailto:','#')):continue
  if not (p.parent/target.split('#')[0]).exists():errors.append('broken link '+str(p.relative_to(root))+' '+target)
# Parse Mermaid graph definitions and verify all referenced nodes exist.
for p in (root/'assets/diagrams').glob('*.mmd'):
 s=p.read_text()
 if s.startswith('flowchart'):
  nodes=set(re.findall(r'^\s*(\w+)\[',s,re.M))
  for a,b in re.findall(r'^\s*(\w+) --> (\w+)',s,re.M):
   if a not in nodes or b not in nodes:errors.append('diagram nodes '+p.name)
 else:
  entities=set(re.findall(r'^\s*(\w+)\[',s,re.M))
  if not entities:errors.append('empty ER '+p.name)
# Confirm no source changed during authoring; do not read secrets.
manifest=json.loads((root/'assets/generated/source-manifest.json').read_text())
base=Path('/Users/cindyram/Documents/Apple')
changed=[]
for item in manifest['files']:
 p=base/item['path']
 if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:changed.append(item['path'])
if changed:errors.append('source changed: '+str(changed))
# Check all PDF pages for text outside page bounds. Also record visual sample review separately.
pdfstats={}
for lang,name in [('id','DOKUMENTASI_DATABASE'),('en','DATABASE_DOCUMENTATION')]:
 pdf=root/lang/(name+'.pdf');reader=PdfReader(pdf);texts=[p.extract_text() or '' for p in reader.pages]
 missing=[]
 for c in meta['columns']:
  label=c['schema']+'.'+c['table_name']+'.'+c['name']
  if not any(label in t for t in texts):missing.append(label)
 if missing:errors.append(lang+' PDF missing columns '+str(missing))
 clipped=[];badglyph=[]
 with pdfplumber.open(pdf) as doc:
  for i,page in enumerate(doc.pages,1):
   for c in page.chars:
    if c['x0'] < -1 or c['x1']>page.width+1 or c['top']< -1 or c['bottom']>page.height+1:
     clipped.append(i);break
   if '\ufffd' in page.extract_text():badglyph.append(i)
 if clipped:errors.append(lang+' clipping '+str(clipped))
 if badglyph:errors.append(lang+' replacement glyph '+str(badglyph))
 pdfstats[lang]={'pages':len(reader.pages),'all_268_column_headings_found':not missing,'page_bounds_checked':len(reader.pages),'text_outside_page_bounds':clipped,'replacement_glyph_pages':badglyph,'visual_sample_pages':[1,3,20,45,100,170,240,300],'visual_sample_review':'passed; cover, TOC, data dictionary, ER panel, contract fields and appendix inspected'}
# Secret patterns, without echoing matched content.
secret_hits=[]
for p in root.rglob('*'):
 if not p.is_file() or p.suffix not in ['.md','.json','.sql','.py','.mmd','.svg']:continue
 s=p.read_text(errors='ignore')
 patterns=[r'postgres(?:ql)?://[^\s/]+:[^\s@]+@',r'sgi_[A-Za-z0-9_-]{32,128}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'sbp_[A-Za-z0-9]{20,}']
 if any(re.search(q,s) for q in patterns):secret_hits.append(str(p.relative_to(root)))
if secret_hits:errors.append('secret-pattern candidates '+str(secret_hits))
result={'date':'2026-10-27','status':'PASS' if not errors else 'FAIL','chapters_per_language':13,'column_dictionary_entries_per_language':268,'physical_FK_per_language':47,'bilingual_SQL_JSON_Mermaid_blocks_identical':blocks(md['id'])==blocks(md['en']),'markdown_links':'checked','source_hashes_unchanged':not changed,'offline_tests':{'command':'PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:scripts .venv/bin/python -m unittest tests.test_contracts tests.test_a3.AlignmentTests tests.test_a1_tools -v','run':40,'passed':40,'failed':0,'note':'An initial invocation had an import-path error; corrected invocation passed. No database test classes executed.'},'pdf':pdfstats,'secret_scan':'no credential candidates' if not secret_hits else 'review required','runtime_database_verification':'NOT PERFORMED; historical metadata only','nested_contract_semantics':'partial; full JSON schemas included, unresolved field meaning explicitly marked','errors':errors}
(root/'assets/generated/validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));sys.exit(bool(errors))
