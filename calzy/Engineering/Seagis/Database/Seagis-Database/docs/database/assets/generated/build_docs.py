from pathlib import Path
import json,re,hashlib,subprocess,datetime,collections,os
BASE=Path(os.environ.get('SEAGIS_DOC_OUTPUT',str(Path(__file__).resolve().parents[4]))); OUT=BASE/'docs/database'
BACK=Path('/Users/cindyram/Documents/Apple/Seagis-Model'); APP=Path('/Users/cindyram/Documents/Apple/Seagis'); POC=Path('/Users/cindyram/Documents/Apple/AppPOC')
VAULT=Path('/Users/cindyram/Documents/Second Brain/02-Projects/Challenge Final')
META=json.loads((VAULT/'Engineering/Seagis/Database/schema-metadata-20261022.json').read_text())
for d in ['id/schemas','id/pipelines','id/contracts','id/architecture','id/audit','en/schemas','en/pipelines','en/contracts','en/architecture','en/audit','assets/diagrams','assets/generated','assets/evidence']:(OUT/d).mkdir(parents=True,exist_ok=True)
DATE='2026-10-27'; VERSION='1.0.0'; snapshot='2026-10-22T10:42:58.974431+00:00'
sha=lambda b:hashlib.sha256(b).hexdigest()
# No environment files, credentials, records or runtime logs are collected.
sources={}; roots={'Seagis-Model':BACK,'Seagis':APP,'AppPOC':POC}
for label,root in roots.items():
 for p in sorted(root.rglob('*')):
  rel=p.relative_to(root)
  if any(x.startswith('.') or x in ['node_modules','DerivedData','build'] for x in rel.parts): continue
  if not p.is_file() or p.suffix not in ['.sql','.py','.ts','.swift','.toml','.json','.md','.yml','.yaml']:continue
  if label=='Seagis-Model' and rel.parts[0] in ['data']:continue
  if label in ['Seagis','AppPOC'] and p.suffix not in ['.swift','.md']:continue
  if p.stat().st_size>200000:continue
  text=p.read_text(errors='replace'); key=label+'/'+str(rel)
  sources[key]={'text':text,'sha256':sha(p.read_bytes()),'lines':len(text.splitlines())}
# Index all inspected implementation artifacts; excerpts referenced by path+line.
commits={label:subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip() for label,root in roots.items()}
source_manifest=[{'path':p,'sha256':v['sha256'],'lines':v['lines']} for p,v in sources.items()]
(OUT/'assets/generated/source-manifest.json').write_text(json.dumps({'date':DATE,'commits':commits,'files':source_manifest},indent=2)+'\n')
(OUT/'assets/evidence/schema-metadata-20261022.json').write_text(json.dumps(META,indent=2)+'\n')
for name in ['source.schema.json','normalized.schema.json','iot-packet.schema.json','alignment.schema.json']:
 (OUT/'assets/evidence'/name).write_text((BACK/'contracts'/name).read_text())
for p in sorted((BACK/'supabase/migrations').glob('*.sql')):(OUT/'assets/evidence'/p.name).write_text(p.read_text())
for name in ['a2_sources.json','a3_quality.json']:(OUT/'assets/evidence'/name).write_text((BACK/'config'/name).read_text())

def evidence(path,pattern=None):
 key=path if path in sources else 'Seagis-Model/'+path
 v=sources.get(key)
 if not v:return '`'+key+'`'
 line=next((i for i,l in enumerate(v['text'].splitlines(),1) if pattern and re.search(pattern,l)),1)
 return '`'+key+':'+str(line)+'`'

def table(headers,rows):
 def esc(s):return str(s).replace('|','&#124;').replace('\n','<br>') if s is not None else 'NULL'
 return '| '+' | '.join(map(esc,headers))+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(map(esc,r))+' |\n' for r in rows)+'\n'
def code(s,lang='sql'):return '\n```'+lang+'\n'+s.strip()+'\n```\n\n'
def T(i,e,lang):return i if lang=='id' else e

def cols(obj):return [c for c in META['columns'] if c['schema']==obj['schema'] and c['table_name']==obj['name']]
def cons(obj):return [c for c in META['constraints'] if c['schema']==obj['schema'] and c['table_name']==obj['name']]
def fullname(obj):return obj['schema']+'.'+obj['name']
def sqlref(obj):
 for key,v in sources.items():
  if '/migrations/' in key and re.search(r'CREATE (?:TABLE|VIEW) '+re.escape(fullname(obj))+r'\b',v['text']):return evidence(key,r'CREATE (?:TABLE|VIEW) '+re.escape(fullname(obj)))
 return 'NOT FOUND'
def constraints_for(obj,col):return [c for c in cons(obj) if col['name'] in c['columns'] or (c['kind']=='c' and re.search(r'\b'+re.escape(col['name'])+r'\b',c['definition']))]

PURPOSE={
'seagis.source':('Registri penyedia asal dataset.','Registry of dataset providers.'),
'seagis.dataset':('Identitas dataset, versi, cadence, lisensi dan gate ingestion.','Dataset identity, version, cadence, licence and ingestion gates.'),
'seagis.parameter':('Registri parameter dan satuan normalisasi.','Registry of parameters and normalized units.'),
'seagis.dataset_parameter':('Kontrak variabel sumber ke parameter dan aturan konversi.','Source-variable to parameter contract and conversion rules.'),
'seagis.plot':('Identitas plot dan status survei; koordinat nullable bukan bukti lokasi lapangan.','Plot identity and survey status; nullable coordinates are not evidence of a surveyed location.'),
'seagis.sensor':('Identitas deployment sensor suhu, plot, kedalaman dan status aktif.','Temperature sensor deployment identity, plot, depth and active state.'),
'seagis.ingestion_run':('Audit satu ingestion logis beserta status penyelesaian.','Audit of a logical ingestion and its completion state.'),
'seagis_raw.raw_payload':('Manifest raw immutable: digest, basis hash, lisensi dan mode retensi.','Immutable raw manifest: digest, hash basis, licence and retention mode.'),
'seagis.source_grid':('Identitas sel regional dan layer kedalaman; bukan plot budidaya.','Regional cell and depth-layer identity; distinct from cultivation plots.'),
'seagis.plot_grid_mapping':('Pemetaan operasional plot ke grid dengan waktu efektif dan waktu tercatat.','Operational plot-to-grid mapping with effective and recorded times.'),
'seagis.observation':('Pembacaan suhu air sensor lokal, dengan nilai native, QC dan lineage raw.','Local sensor water-temperature readings, retaining native values, QC and raw lineage.'),
'seagis.forecast_run':('Capture/vintage model regional; waktu publikasi yang tidak diketahui tetap null.','Regional model capture/vintage; unknown publication time remains null.'),
'seagis.forecast_value':('Nilai parameter per run, grid dan valid time; tidak diduplikasi per plot.','Parameter value per run, grid and valid time; not duplicated per plot.'),
'seagis.quality_event':('Log QC append-only untuk ingestion atau satu measurement.','Append-only QC log for ingestion or one measurement.'),
'seagis_features.feature_snapshot':('Container fitur draft/sealed dengan cutoff dan hash; builder produksi belum ditemukan.','Draft/sealed feature container with cutoff and hashes; no production builder found.'),
'seagis_features.feature_input':('Lineage FK input feature snapshot dan guard cutoff.','Foreign-key input lineage and cutoff guards for feature snapshots.'),
'seagis_api.credential':('Identitas aktor API berupa hash token, masa berlaku dan pencabutan.','API actor identity using token hashes, expiry and revocation.'),
'seagis_api.reader_plot':('Daftar plot yang boleh dibaca satu credential reader.','Plot allowlist for a reader credential.'),
'seagis_api.request_event':('Audit respons API terautentikasi dan dasar rate limit.','Authenticated API response audit and rate-limit basis.'),
'seagis_api.packet_receipt':('Kunci idempotensi paket sensor dan digest semantik.','Sensor-packet idempotency key and semantic digest.'),
'seagis_api.temperature_policy':('Konfigurasi QC engineering pilot dan batas request; bukan ambang penyakit.','Pilot engineering QC settings and request limit; not disease thresholds.'),
'seagis_environment.policy':('Kebijakan fetch, lisensi, cadence scheduler, staleness dan retensi regional.','Regional fetch, licence, scheduler cadence, staleness and retention policy.'),
'seagis_environment.schedule_state':('State mutable lease, due time, backoff dan keberhasilan terakhir.','Mutable lease, due time, backoff and last-success state.'),
'seagis_environment.attempt':('Audit satu upaya fetch termasuk duplicate dan abandoned.','Audit of a fetch attempt, including duplicate and abandoned outcomes.'),
'seagis_environment.demo_grid_mapping':('Bridge khusus dua plot fiktif ke grid nyata untuk preview, bukan otorisasi training.','Bridge from two fictional plots to real grids for preview, not training authorization.'),
'seagis_environment.current_speed':('View magnitude arus dari pasangan komponen dengan run/grid/waktu yang sama.','Current-magnitude view joining components from the same run, grid and time.'),
'seagis_quality.policy':('Registri versi kebijakan QC dan hash kode builder yang immutable.','Immutable registry of QC policy versions and builder code hashes.'),
'seagis_quality.alignment_snapshot':('Dokumen QC/alignment hourly immutable; selalu training_authorized=false.','Immutable hourly QC/alignment document; always training_authorized=false.'),
'seagis_quality.snapshot_input':('Lineage measurement per jam alignment snapshot.','Per-hour measurement lineage of an alignment snapshot.')}
# Bilingual meanings are a single paired evidence base, not independent translations.
MEAN={}
def meanings(text):
 for line in text.strip().splitlines():
  key,i,e=line.split('|',2);MEAN[key]=(i,e)
meanings('''id|Identitas baris menurut PK tabel|Row identity under the table primary key
source_key|Kunci penyedia sumber|Source-provider key
provider|Nama penyedia dataset|Dataset provider name
documentation_url|URL dokumentasi penyedia|Provider documentation URL
dataset_key|Kunci dataset terdaftar|Registered dataset key
provider_product_id|Identitas produk penyedia bila tersedia|Provider product identity when available
provider_dataset_id|Identitas dataset asli penyedia|Original provider dataset identity
dataset_version|Versi dataset yang dipin|Pinned dataset version
scope|Asal local_sensor atau regional_model|Origin: local_sensor or regional_model
native_cadence_seconds|Jarak waktu asli sampel, bukan interval fetch|Native sample cadence, distinct from fetch interval
resolution_lat_deg|Resolusi latitude dalam derajat bila diketahui|Latitude resolution in degrees when known
resolution_lon_deg|Resolusi longitude dalam derajat bila diketahui|Longitude resolution in degrees when known
source_timezone|Konteks zona waktu asal|Original source timezone context
licence_url|Referensi lisensi sumber|Source licence reference
attribution|Teks atribusi yang harus dipertahankan|Attribution text to preserve
raw_storage_permitted|Gate izin menyimpan raw, bukan jaminan objek telah disimpan|Raw-retention permission gate, not proof of stored objects
real_ingestion_enabled|Gate ingestion data nonsintetis|Gate for nonsynthetic ingestion
metadata_checked_at|Waktu metadata sumber diperiksa|Time source metadata was checked
parameter_code|Identitas parameter lingkungan|Environmental parameter identity
source_variable|Nama variabel asli provider|Original provider variable name
native_unit|Satuan asli sebelum normalisasi|Original unit before normalization
unit|Satuan nilai normalisasi menurut registri|Normalized value unit from registry
conversion_code|Identitas metode konversi satuan|Unit-conversion method identity
conversion_factor|Pengali pada value=native_value*factor+offset|Multiplier in value=native_value*factor+offset
conversion_offset|Offset setelah perkalian faktor|Offset after multiplying by factor
temporal_support|Dukungan waktu instantaneous, mean atau sum|Temporal support: instantaneous, mean or sum
plot_code|Kode plot unik yang dapat dibaca manusia|Unique human-readable plot code
name|Nama tampilan plot|Plot display name
latitude|Latitude WGS84 dalam derajat|WGS84 latitude in degrees
longitude|Longitude WGS84 dalam derajat|WGS84 longitude in degrees
is_synthetic|Penanda asal sintetis, terpisah dari QC|Synthetic provenance flag, separate from QC
location_status|Status lokasi synthetic, not_surveyed atau surveyed|Location state: synthetic, not_surveyed or surveyed
created_at|Instan pembuatan baris|Row creation instant
sensor_code|Kode deployment sensor unik|Unique sensor-deployment code
plot_id|Referensi plot budidaya|Cultivation plot reference
sensor_id|Referensi deployment sensor|Sensor deployment reference
depth_m|Kedalaman positif ke bawah dalam meter|Depth positive downward in metres
depth_status|Status pengetahuan kedalaman sensor|Sensor-depth knowledge status
active|Apakah deployment sensor masih aktif|Whether the sensor deployment remains active
request_key|Kunci logis retry ingestion per dataset|Logical ingestion retry key per dataset
adapter_version|Versi implementasi adapter ingestion|Ingestion adapter implementation version
started_at|Instan dimulainya ingestion atau attempt|Ingestion or attempt start instant
completed_at|Instan selesai; null selama running|Completion instant; null while running
error_code|Kode kegagalan tersanitasi|Sanitized failure code
ingestion_run_id|Referensi ingestion asal|Source ingestion reference
raw_payload_id|Referensi manifest raw asal|Source raw-manifest reference
sha256|Digest raw sesuai hash_basis, bukan selalu byte jaringan|Raw digest under hash_basis, not necessarily network bytes
hash_basis|Aturan byte/serialisasi yang di-hash|Byte or serialization convention used for hashing
received_at|Instan penerimaan raw oleh worker|Raw receipt instant at worker
storage_mode|inline, object atau metadata_only menentukan lokasi konten|inline, object or metadata_only determines content location
payload|Konten JSON raw sintetis bila inline|Synthetic raw JSON content when inline
object_uri|Referensi privat objek bila mode object|Private object reference in object mode
byte_size|Ukuran byte yang dilaporkan pada capture|Byte count reported at capture
format|Media type/format representasi raw|Raw representation media type or format
licence_snapshot|Keterangan lisensi saat capture|Licence statement at capture
provider_metadata|Metadata provider/request tersanitasi|Sanitized provider and request metadata
source_grid_id|Referensi sel regional dan layer|Regional cell and layer reference
grid_key|Kunci sel berbasis koordinat/depth atau fixture|Cell key based on coordinates/depth or fixture
grid_version|Versi identitas grid|Grid identity version
identity_basis|Dasar identitas sel asli, koordinat respons atau sintetis|Identity basis: native cell, response coordinate or synthetic
sampling_method|Metode pemilihan grid untuk plot|Grid selection method for plot
distance_m|Jarak plot ke sel dalam meter|Plot-to-cell distance in metres
representativeness|Status keterwakilan regional, bukan bukti representasi lokal|Regional representativeness status, not proof of local validity
effective_from|Awal inklusif rentang pemetaan|Inclusive mapping interval start
effective_until|Akhir eksklusif pemetaan; null berarti terbuka|Exclusive mapping end; null means open-ended
recorded_at|Instan pemetaan pertama diketahui sistem|Instant mapping first became known to the system
source_record_key|boot_id:sequence untuk paket A1|boot_id:sequence for A1 packets
native_value|Nilai fisik dalam satuan sumber|Physical value in source units
value|Nilai normalisasi; null mengikuti value_status|Normalized value; null follows value_status
value_status|Ketersediaan angka, terpisah dari kualitas|Numeric availability, separate from quality
quality_status|Status QC unreviewed, accepted, suspect atau rejected; bukan diagnosis|QC state unreviewed, accepted, suspect or rejected; not a diagnosis
detection_limit|Batas deteksi pada satuan normalisasi bila relevan|Detection limit in normalized units when applicable
observed_at|Instan pengukuran sensor, bukan receipt|Sensor measurement instant, distinct from receipt
ingested_at|Instan data tersedia bagi sistem|Instant data became available to the system
forecast_run_id|Referensi capture/vintage model regional|Regional model capture/vintage reference
run_key|Identitas capture semantik per dataset|Semantic capture identity per dataset
run_kind|forecast, analysis atau analysis_forecast_unspecified|forecast, analysis or analysis_forecast_unspecified
provider_run_id|ID run provider jika benar-benar tersedia|Provider run ID only when actually available
model_initialized_at|Instan inisialisasi model jika diketahui|Model initialization instant when known
issued_at|Instan publikasi provider terverifikasi; null jika tidak diketahui|Verified provider publication instant; null when unknown
issue_time_basis|Dasar known/unknown waktu publikasi|Known/unknown publication-time basis
valid_at|Waktu representatif nilai model|Representative time of model value
interval_status|known, unknown atau not_applicable untuk interval|known, unknown or not_applicable interval status
period_start_at|Awal interval mean/sum jika diketahui|Mean/sum interval start when known
period_end_at|Akhir interval mean/sum jika diketahui|Mean/sum interval end when known
event_key|Identitas event unik per ingestion|Unique event identity per ingestion
observation_id|Referensi pembacaan sensor lokal|Local sensor reading reference
forecast_value_id|Referensi satu nilai model regional|Single regional model value reference
event_code|Kode jenis kejadian QC|QC event-type code
severity|Tingkat kejadian info, warning atau error; bukan risiko penyakit|Event level info, warning or error; not disease risk
details|Rincian QC JSON tanpa rahasia|QC JSON details without secrets
as_of|Cutoff informasi untuk feature snapshot|Information cutoff for feature snapshot
generated_at|Instan snapshot fitur dihasilkan|Feature snapshot generation instant
feature_version|Versi definisi/builder fitur|Feature definition or builder version
feature_schema_version|Versi struktur JSON fitur|Feature JSON structure version
features|Objek JSON fitur; validitas perhitungan tidak dibuktikan container|Feature JSON object; container does not prove calculation correctness
missing_context|Daftar konteks yang tidak tersedia|List of unavailable context
input_manifest_sha256|Digest daftar input lineage terurut|Digest of ordered lineage-input manifest
features_sha256|Digest JSONB fitur menurut PostgreSQL|PostgreSQL JSONB feature digest
snapshot_id|Referensi snapshot induk|Parent snapshot reference
label|Label administratif credential|Administrative credential label
token_sha256|Hash token Bearer; token asli tidak disimpan di kolom|Bearer token hash; original token not stored in column
kind|Jenis aktor device atau reader|Actor kind device or reader
expires_at|Instan credential tidak berlaku lagi|Instant credential expires
revoked_at|Instan pencabutan; null bila belum dicabut|Revocation instant; null if not revoked
credential_id|Referensi aktor API terdaftar|Registered API actor reference
http_status|Status HTTP respons yang diaudit|Audited response HTTP status
code|Kode respons API|API response code
semantic_sha256|Hash paket setelah normalisasi semantik retry|Packet hash after retry-safe semantic normalization
flags|Kode QC dari penerimaan paket|QC codes from packet acceptance
version|Identitas versi kebijakan|Policy version identity
min_degc|Batas bawah envelope QC engineering pilot dalam degC|Pilot engineering QC lower envelope in degC
max_degc|Batas atas envelope QC engineering pilot dalam degC|Pilot engineering QC upper envelope in degC
max_step_degc|Batas perubahan suhu pilot dalam degC|Pilot temperature-step limit in degC
future_tolerance_seconds|Toleransi jam sensor ke depan dalam detik|Future sensor-clock tolerance in seconds
stale_after_seconds|Batas keterlambatan sensor dalam detik|Sensor delay boundary in seconds
requests_per_minute|Batas request per aktor per jendela satu menit|Request limit per actor per one-minute window
enabled|Apakah policy regional mengizinkan fetch|Whether regional policy enables fetching
purpose|Tujuan noncommercial_educational_prototype|Purpose noncommercial_educational_prototype
terms_review|Identitas review ketentuan provider|Provider terms review identity
update_seconds|Interval nominal scheduler per provider dalam detik|Nominal per-provider scheduler interval in seconds
release_offset_seconds|Offset fase jadwal dalam detik|Schedule phase offset in seconds
stale_seconds|Usia vintage maksimum menurut policy dalam detik|Maximum vintage age under policy in seconds
retention_mode|Kebijakan metadata_only pada A2|metadata_only retention policy in A2
reviewed_at|Instan review kebijakan|Policy review instant
lease_id|Identitas lease fetch aktif|Active fetch lease identity
lease_until|Instan lease tidak lagi valid|Lease expiry instant
next_attempt_at|Waktu fetch paling awal; dapat bernilai -infinity pada awal|Earliest next fetch; may initially be -infinity
last_success_at|Instan fetch/persist terakhir berhasil|Last successful fetch/persist instant
last_attempt_at|Instan attempt terakhir dimulai|Last attempt start instant
last_error_code|Kode kegagalan attempt terakhir|Last attempt failure code
failures|Jumlah kegagalan untuk perhitungan backoff|Failure count used for backoff
last_forecast_run_id|Referensi vintage terakhir berhasil|Last successful vintage reference
plot_is_synthetic|Harus true untuk bridge demo|Must be true for demo bridge
grid_is_synthetic|Harus false untuk grid nyata di bridge demo|Must be false for real grid in demo bridge
example_latitude|Latitude contoh fiktif, bukan survei|Fictional example latitude, not a survey
example_longitude|Longitude contoh fiktif, bukan survei|Fictional example longitude, not a survey
coordinate_status|example_not_surveyed pada bridge demo|example_not_surveyed in demo bridge
eastward_value_id|ID komponen current_eastward pada view|current_eastward component ID in view
northward_value_id|ID komponen current_northward pada view|current_northward component ID in view
available_at|Waktu konservatif ketersediaan input|Conservative input availability time
speed_m_s|sqrt(uo²+vo²), null bila salah satu komponen tidak present|sqrt(uo²+vo²), null unless both components are present
derivation|Label formula dan versi magnitude arus|Current-magnitude formula and version label
definition|Dokumen kebijakan QC yang diregistrasi|Registered QC policy document
policy_sha256|Digest isi policy|Policy-content digest
code_sha256|Digest source builder alignment|Alignment-builder source digest
registered_at|Instan registrasi policy immutable|Immutable policy registration instant
mode|demo_review atau operational_review sesuai asal plot|demo_review or operational_review according to plot provenance
start_at|Awal inklusif jendela alignment|Inclusive alignment-window start
end_at|Akhir eksklusif jendela alignment|Exclusive alignment-window end
policy_version|Referensi versi policy QC|QC policy version reference
source_sha256|Digest source bundle untuk deteksi sumber berubah|Source-bundle digest for source-change detection
body|Dokumen alignment lengkap, termasuk rows dan laporan QC|Complete alignment document, including rows and QC report
body_sha256|Digest generated atas JSONB body|Generated digest of JSONB body
aligned_at|Jam UTC baris alignment|UTC hour of alignment row
source_ref|Referensi typed observation:uuid atau forecast_value:uuid|Typed reference observation:uuid or forecast_value:uuid
description|Penjelasan registri parameter|Parameter registry description''')

# Writers and readers are derived from actual routines, not presumed services.
def ownership(obj):
 name=fullname(obj);s=obj['schema'];n=obj['name']
 if n in ['source','dataset','parameter','dataset_parameter','plot','sensor']:return ('supabase/seed.sql; scripts/provision_a1.py; scripts/deploy_a2.py','A1 ingest/history; A2 persist/preview; A3 source_bundle')
 if name in ['seagis.ingestion_run','seagis_raw.raw_payload']:return ('seagis_api.ingest; seagis_environment.persist; A0 fixtures','A3 source_bundle; provenance guards')
 if n=='observation':return ('seagis_api.ingest; A0 fixtures','seagis_api.history/status; A3 source_bundle; export_experiment_csv.py')
 if n in ['forecast_run','forecast_value','source_grid']:return ('seagis_environment.persist; A0 fixtures','seagis_environment.preview/current_speed; A3 source_bundle; CSV exporter')
 if s=='seagis_api':return (('seagis_api.ingest/reply' if n in ['packet_receipt','request_event'] else 'scripts/provision_a1.py; migration 0002'),'seagis_api.actor/rate_ok/ingest/history/status')
 if s=='seagis_environment':return (('NOT APPLICABLE: view' if n=='current_speed' else 'seagis_environment.claim/persist/finish_failure; migration 0003'),'A2 status/preview; A3 source_bundle')
 if s=='seagis_quality':return (('scripts/quality/store.py::register_policy' if n=='policy' else 'seagis_quality.save_snapshot'),'seagis_quality.source_bundle/save_snapshot/snapshot; curate_environment.py')
 if s=='seagis_features':return ('A0 fixture/test inserts; production builder NOT FOUND','snapshot/input guards; production ML consumer NOT FOUND')
 if n=='quality_event':return ('seagis_api.ingest; A0 fixtures','A3 source_bundle/alignment')
 return ('A0 fixture/admin SQL','A3 source_bundle; feature_input guards')

def origin(obj,c):
 n=c['name'];name=fullname(obj);writers,_=ownership(obj)
 # Exact origin categories; untraced expressions are explicitly not fabricated.
 if c['generated']:return ('DB generated',c['default_expression'] or '', 'VERIFIED')
 if n=='id' and c['default_expression']:return ('DB default / explicit UUID',c['default_expression'],'VERIFIED')
 if name=='seagis_environment.current_speed':
  expr={'eastward_value_id':'u.id','northward_value_id':'v.id','forecast_run_id':'u.forecast_run_id','source_grid_id':'u.source_grid_id','valid_at':'u.valid_at','ingested_at':'u.ingested_at','available_at':'greatest(u.ingested_at,v.ingested_at)','speed_m_s':"CASE WHEN both value_status='present' THEN sqrt(u.value*u.value+v.value*v.value) END",'derivation':"'sqrt(uo^2+vo^2); a2-vector-magnitude-v1'"}[n]
  return ('seagis.forecast_value u/v',expr,'VERIFIED')
 if name=='seagis.observation':
  expr={'plot_id':'registered sensor.plot_id','sensor_id':'authenticated credential.sensor_id','dataset_key':'registered sensor.dataset_key','is_synthetic':'registered sensor.is_synthetic','source_record_key':'boot_id || : || sequence','parameter_code':"constant water_temperature",'native_value':'packet.water_temperature','value':'packet.water_temperature (identity)','native_unit':"constant degC",'unit':"constant degC",'conversion_code':"constant identity",'value_status':'packet.value_status','observed_at':'packet.observed_at cast timestamptz','ingested_at':'server received = clock_timestamp()','quality_status':'pilot policy + flags','ingestion_run_id':'ingest-generated run_id','raw_payload_id':'ingest-generated raw_id','detection_limit':'omitted -> SQL NULL'}
  if n in expr:return ('A1 packet + registered identity + server',expr[n],'VERIFIED')
 if name=='seagis.forecast_value':
  expr={'forecast_run_id':'persist run_id','source_grid_id':'grid lookup by dataset/key/synthetic','dataset_key':'leased dataset','is_synthetic':'false','parameter_code':"batch.values[].parameter",'native_value':'batch.values[].value','value':'batch.values[].value','native_unit':'v.native_unit','unit':'v.unit','conversion_code':'v.conversion_code','value_status':'v.value_status','valid_at':'v.valid_at::timestamptz','ingested_at':'persist t = clock_timestamp()','temporal_support':'v.temporal_support','interval_status':'v.interval_status','period_start_at':'v.period_start_at::timestamptz','period_end_at':'v.period_end_at::timestamptz','quality_status':'default unreviewed','detection_limit':'omitted -> SQL NULL'}
  if n in expr:return ('A2 adapter batch',expr[n],'VERIFIED')
 if name=='seagis_quality.alignment_snapshot':
  expr={'plot_id':'document.plot_id','mode':'document.mode','start_at':'document.start_at','end_at':'document.end_at','policy_version':'registered policy.version','source_sha256':'document.source_sha256 checked against fresh source_bundle','input_manifest_sha256':'SHA256 sorted distinct at|source_ref lines','body':'document','created_at':'SQL default clock_timestamp()'}
  if n in expr:return ('A3 build -> save_snapshot',expr[n],'VERIFIED')
 if name=='seagis_quality.snapshot_input':return ('A3 document.rows[].cells[].lineage',{'snapshot_id':'saved snapshot UUID','aligned_at':'row.at::timestamptz','source_ref':'lineage ref','observation_id':"UUID if ref prefix observation else NULL",'forecast_value_id':"UUID if ref prefix forecast_value else NULL"}[n],'VERIFIED')
 if c['default_expression']:return ('caller / SQL default',c['default_expression'],'VERIFIED')
 return (writers,T('Lihat INSERT/UPDATE pada routine pemilik; derivasi field belum ditelusuri penuh','See owning routine INSERT/UPDATE; field derivation not fully traced','en'),'UNVERIFIED')

# Diagrams: Mermaid canonical plus deterministic vector PDF rendering of the same nodes/edges.
DIAGS={
'architecture': [('sensor','IoT / simulator'),('edge','temperature handler'),('sql','PostgreSQL / 6 schemas'),('providers','Copernicus + Open-Meteo'),('a2','A2 adapters + leases'),('a3','A3 quality / alignment'),('csv','CSV experiments'),('ios','iOS synthetic mock')],
'lineage': [('registry','source + dataset_parameter'),('raw','ingestion_run + raw_payload'),('obs','observation'),('run','forecast_run + forecast_value'),('map','source_grid + mappings'),('bundle','source_bundle'),('align','alignment_snapshot + snapshot_input')],
'dependencies':[('obs','observation'),('fc','forecast_value'),('hist','temperature history/status'),('preview','regional preview/current_speed'),('quality','A3 alignment'),('export','CSV export'),('mock','MockAssessmentRepository'),('ui','SwiftUI / MapKit')],
'a1':[('wire','JSON bytes <=8192'),('auth','Bearer + actor + sensor'),('check','schema + semantic hash + QC'),('write','raw + observation + QC + receipt'),('reply','201 stored / 200 duplicate / 409 conflict')],
'a2':[('claim','claim / 20 min lease'),('fetch','bounded provider fetch'),('parse','units + coordinates + cadence'),('normal','dedupe + semantic run_key'),('persist','atomic persist / metadata_only'),('next','schedule due / failure backoff')],
'a3':[('bundle','source_bundle / <=7 days'),('cutoff','source_time + available_at cutoff'),('qc','QC + spatial metadata'),('hour','hourly cells + lineage'),('seal','save_snapshot + policy/source hash'),('review','review only / training false')]}
EDGES={'architecture':[('sensor','edge'),('edge','sql'),('providers','a2'),('a2','sql'),('sql','a3'),('a3','csv')], 'lineage':[('registry','raw'),('raw','obs'),('raw','run'),('map','run'),('obs','bundle'),('run','bundle'),('bundle','align')], 'dependencies':[('obs','hist'),('fc','preview'),('obs','quality'),('fc','quality'),('quality','export'),('mock','ui')], 'a1':[('wire','auth'),('auth','check'),('check','write'),('write','reply')], 'a2':[('claim','fetch'),('fetch','parse'),('parse','normal'),('normal','persist'),('persist','next')], 'a3':[('bundle','cutoff'),('cutoff','qc'),('qc','hour'),('hour','seal'),('seal','review')]}
for name,nodes in DIAGS.items():
 s='flowchart TD\n'+''.join(f'    {k}["{v}"]\n' for k,v in nodes)+''.join(f'    {a} --> {b}\n' for a,b in EDGES[name])
 (OUT/f'assets/diagrams/{name}.mmd').write_text(s)

def diagram(name,lang):return T('Diagram reproduktif','Reproducible diagram',lang)+': `assets/diagrams/'+name+'.mmd`.\n\n'+code((OUT/f'assets/diagrams/{name}.mmd').read_text(),'mermaid')
# All 47 physical relationships, including composite keys.
FKS=[c for c in META['constraints'] if c['kind']=='f']
OBJ={fullname(o):o for o in META['objects']}

def relation_info(f):
 child=OBJ[f['schema']+'.'+f['table_name']];nullable=any(not next(c for c in cols(child) if c['name']==n)['not_null'] for n in f['columns'])
 unique=any(c['kind'] in ['p','u'] and set(c['columns']).issubset(set(f['columns'])) for c in cons(child))
 return nullable,unique

def erd(schema=None):
 chosen=[o for o in META['objects'] if o['kind']=='r' and (not schema or o['schema']==schema)]
 keys={fullname(o) for o in chosen}
 if schema:
  for f in FKS:
   if f['schema']==schema:keys.add(f['target_schema']+'.'+f['target_table'])
 lines=['erDiagram']
 for key in sorted(keys):
  o=OBJ[key];lines.append('    '+key.replace('.','_')+'["'+key+'"] {')
  for c in cols(o):
   cc=constraints_for(o,c); mark=[]
   if any(x['kind']=='p' for x in cc):mark.append('PK')
   if any(x['kind']=='f' for x in cc):mark.append('FK')
   # Single-column unique is distinct from composite membership.
   if any(x['kind']=='u' and x['columns']==[c['name']] for x in cc):mark.append('UK')
   typ=re.sub(r'[^a-zA-Z0-9_]','_',c['type'])
   lines.append('        '+typ+' '+c['name']+(' '+','.join(mark) if mark else ''))
  lines.append('    }')
 for i,f in enumerate(FKS,1):
  child=f['schema']+'.'+f['table_name'];parent=f['target_schema']+'.'+f['target_table']
  if child not in keys or parent not in keys:continue
  null,unique=relation_info(f)
  lines.append('    '+parent.replace('.','_')+(' |o' if null else ' ||')+('--o|' if unique else '--o{')+' '+child.replace('.','_')+' : "FK'+str(i)+'"')
 return '\n'.join(lines)+'\n'
(OUT/'assets/diagrams/erd.mmd').write_text(erd())
for s in [x['name'] for x in META['schemas']]:(OUT/f'assets/diagrams/erd-{s}.mmd').write_text(erd(s))

# Bilingual hand-written architecture explanations.
TEXT={
'summary':('''Audit ini mendokumentasikan implementasi backend dan konsumen lokal yang dapat diperiksa pada 27 Oktober 2026. Satu database PostgreSQL aplikasi ditemukan melalui migrasi dan snapshot catalog 22 Oktober: enam schema, 28 tabel, satu view, 268 kolom termasuk sembilan kolom view, dan 47 FK. Tidak ada koneksi live yang dibuat dalam audit ini; jumlah baris, deployment terkini, backup, role membership dan drift setelah snapshot tetap UNVERIFIED.

A1 menerima paket suhu lewat Edge Function, menetapkan identitas dari credential, menyimpan raw/provenance, observasi dan QC secara atomik, serta mengenali retry semantik. A2 mengambil empat dataset regional, mempertahankan grid dan native cadence, lalu menyimpan vintage immutable. A3 menyusun konteks per jam dengan cutoff ketersediaan dan menyimpan snapshot review. A3 bukan feature builder produksi atau model penyakit.

Aplikasi `Seagis` dan prototype `AppPOC` diperiksa sebagai konsumen terpisah. `MockAssessmentRepository` menghasilkan assessment sintetis; tidak ditemukan jalur produksi dari assessment ke database backend. Status QC, data model regional dan demo tidak boleh diperlakukan sebagai diagnosis atau probabilitas ice-ice. Dokumen ini adalah rujukan audit kode versi tertentu, bukan sertifikasi sistem produksi.''', '''This audit documents inspectable backend and local consumer implementations as of 27 October 2026. One application PostgreSQL database is identified through migrations and the 22 October catalog snapshot: six schemas, 28 tables, one view, 268 columns including nine view columns, and 47 foreign keys. No live database connection was made in this audit; row counts, current deployment, backups, role membership and post-snapshot drift remain UNVERIFIED.

A1 accepts temperature packets through an Edge Function, derives identity from credentials, atomically stores raw provenance, observations and QC, and recognizes semantic retries. A2 retrieves four regional datasets, preserves grids and native cadence, and persists immutable vintages. A3 builds hourly contexts using availability cutoffs and saves review snapshots. A3 is not a production feature builder or disease model.

The `Seagis` app and `AppPOC` prototype were inspected as separate consumers. `MockAssessmentRepository` produces synthetic assessments; no production assessment-to-backend-database path was found. QC state, regional model data and demo content must not be treated as ice-ice diagnosis or probability. This document is a versioned code-audit reference, not production-system certification.'''),
'architecture':('''PostgreSQL/Supabase adalah persistence backend yang didefinisikan kode. Schema `seagis` berisi registri, observasi, forecast dan provenance; `seagis_raw` menyimpan manifest raw; `seagis_api` membatasi IoT gateway; `seagis_environment` mengatur worker regional; `seagis_quality` menyimpan review QC; `seagis_features` menyediakan container fitur yang belum dihubungkan ke builder produksi. Schema internal Supabase seperti auth/storage tidak diinventaris sebagai milik aplikasi: akses catalog terkini tidak tersedia dan tidak boleh diasumsikan kosong.

Python melakukan pengambilan provider di luar database. Worker A2/A3 memanggil stored function lewat psycopg; TS handler memanggil hanya fungsi ingest/history/status. Tidak ada ORM yang ditemukan pada jalur ini. Transaksi mutasi berada di fungsi SQL; claim fetch merupakan transaksi terpisah dari persistence agar panggilan jaringan tidak menahan transaksi database.

Diagram memperlihatkan dua komponen yang terputus: mock iOS tidak memiliki edge ke backend. Integrasi masa depan tetap UNVERIFIED. Core ML, cache terdistribusi, warehouse, queue dan search index produksi NOT FOUND dalam file implementasi yang diinspeksi; ini bukan bukti bahwa layanan di luar checkout tidak ada.''','''PostgreSQL/Supabase is the backend persistence defined by code. Schema `seagis` owns registries, observations, forecasts and provenance; `seagis_raw` holds raw manifests; `seagis_api` bounds the IoT gateway; `seagis_environment` manages regional workers; `seagis_quality` stores QC reviews; `seagis_features` supplies containers not connected to a production feature builder. Supabase internal schemas such as auth/storage are not inventoried as application-owned: current catalog access is unavailable and they must not be assumed empty.

Python retrieves provider data outside the database. A2/A3 workers call stored functions through psycopg; the TypeScript handler invokes only ingest/history/status functions. No ORM was found on these paths. Mutation transactions live in SQL functions; fetch claiming is a separate transaction from persistence so network calls do not hold a database transaction.

The diagram contains disconnected components: the iOS mock has no backend edge. Future integration remains UNVERIFIED. Production Core ML, distributed caches, warehouses, queues and search indexes were NOT FOUND in inspected implementation files; that does not establish absence of services outside these checkouts.'''),
'lineage':('''A1: simulator/perangkat → byte JSON → validasi HTTP → autentikasi dan identitas sensor → validasi SQL → digest semantik → raw manifest + observation + quality_event + packet_receipt → history/status. `sensor_id`, plot dan flag sintetis tidak dipercaya dari input bebas: identitas diverifikasi terhadap credential dan deployment. Paket hilang tidak menciptakan observasi nol.

A2: registry/config → claim lease → fetch provider → pemeriksaan metadata/unit/cadence/koordinat → satu sel/layer Copernicus atau koordinat respons Open-Meteo → deduplikasi → run_key semantik → manifest metadata_only → forecast_run + source_grid + forecast_value + bridge demo → preview atau A3. Source bytes Open-Meteo dan canonical logical subset Copernicus memiliki hash_basis berbeda. STAC update dan generationtime_ms tidak dijadikan issued_at.

A3: source_bundle menggabungkan sensor, parameter, pemetaan, record dan event QC; jendela maksimum tujuh hari dengan lookback 72 jam dan sentinel sensor lebih lama bila diperlukan. Builder memfilter source_time dan available_at pada setiap cutoff, memilih konteks, mencatat spatial metadata, flags dan lineage. Penyimpanan membangun ulang source bundle, memeriksa hash/kebijakan/kode, lalu menyimpan snapshot dan input per jam. Perubahan sumber memaksa rebuild.

Ekspor CSV membaca source_bundle dalam REPEATABLE READ READ ONLY, atau capture JSON offline. Dua plot demo diperbolehkan. CSV regional memilih vintage terbaru pada waktu capture, sedangkan alignment JSON menyimpan cutoff historis. Keduanya tidak boleh saling menggantikan untuk backtest. Semua output exporter menandai training_authorized=false.''','''A1: simulator/device → JSON bytes → HTTP validation → authentication and sensor identity → SQL validation → semantic digest → raw manifest + observation + quality_event + packet_receipt → history/status. Sensor identity, plot and synthetic provenance are verified against credentials and deployment rather than accepted as arbitrary input. Missing packets do not create zero observations.

A2: registry/config → lease claim → provider fetch → metadata/unit/cadence/coordinate checks → one Copernicus cell/layer or Open-Meteo response coordinate → deduplication → semantic run_key → metadata_only manifest → forecast_run + source_grid + forecast_value + demo bridge → preview or A3. Open-Meteo source bytes and the canonical Copernicus logical subset have different hash bases. Neither STAC updates nor generationtime_ms become issued_at.

A3: source_bundle joins sensors, parameters, mappings, records and QC events; the maximum window is seven days with a 72-hour lookback and an older sensor sentinel when needed. The builder filters source_time and available_at at each cutoff, selects context, and records spatial metadata, flags and lineage. Persistence rebuilds the source bundle, verifies source/policy/code hashes, and saves a snapshot with hourly inputs. Source changes require a rebuild.

CSV export reads source_bundle in REPEATABLE READ READ ONLY or uses an offline JSON capture. Only two demo plots are supported. Regional CSV selects the latest vintage at capture time, while alignment JSON retains historical cutoffs. These representations are not interchangeable for backtesting. Every exporter output declares training_authorized=false.'''),
'ingest':('''A1 menjalankan satu function call SQL per request. Handler menerima application/json maksimum 8192 byte; byte di-hash SHA-256 sebelum JSON dikirim ke SQL. SQL memerlukan delapan field tepat, schema_version=1.0.0, degC, sequence uint32 dan UTC Z dengan presisi maksimal enam digit. Advisory transaction lock per aktor melindungi rate limit, lalu lock per sensor melindungi deduplikasi dan QC. Retry sama menghasilkan 200 duplicate, konten berbeda pada boot/sequence yang sama menghasilkan 409 packet_conflict. Record baru menghasilkan 201 stored. QC dapat menyimpan reading rejected; rejected bukan respons penolakan HTTP otomatis.

A2 berjalan per dataset setelah claim mengambil row lock pada schedule_state, membuat lease 20 menit dan attempt running. File installer launchd menetapkan tick 900 detik, tetapi ini konfigurasi installer, bukan bukti job aktif. Policy fetch nominal Copernicus 86400 detik, Open-Meteo 21600 detik; cadence nilai asli tetap 6 jam/harian/jam. Offset salinity/currents 30600 detik, nutrients 45000 detik, weather 16200 detik. Worker wrapper timeout 900 detik; HTTP timeout 40 detik; response maksimum 4 juta byte; retry tiga attempt pada timeout/network/429/5xx tertentu dengan backoff dan jitter. Retry-After panjang diserahkan pada backoff scheduler.

Open-Meteo dipin gfs_global, UTC, wind_speed_unit=ms dan forecast_days=3. Parser memeriksa unit, array sejajar dan timezone sebelum menambahkan UTC pada label tanpa suffix. Sel respons yang sama dideduplikasi. Copernicus memeriksa product/dataset/version, STAC cadence/grid/depth/unit, memuat nearest cell tetap untuk centroid dua plot contoh, memeriksa revisi katalog sebelum/sesudah, lalu decode melalui Toolbox/xarray. Nilai nonfinite/fill ekstrem menjadi null missing; daily mean tidak diubah menjadi 24 sampel independen.

Adapter memvalidasi 1–4 grid, tepat dua mapping, nilai tidak kosong dan key unik; SQL membatasi batch dua juta byte dan 1–5000 nilai. `persist` memeriksa lease, policy, versi dataset dan receipt time sebelum seluruh insert. Run_key sudah ada berarti duplicate; perubahan konten yang mengubah identitas semantik membuat vintage baru. Grid dan demo mapping memakai ON CONFLICT DO NOTHING dengan pemeriksaan identitas grid. Kegagalan statement mengembalikan seluruh transaksi persistence; claim/attempt tetap tercatat dan finish_failure dijalankan terpisah. Hilangnya commit acknowledgement memerlukan pemeriksaan status sebelum retry manual.

A3 tidak fetch provider dan tidak mengubah observation/forecast. `build` menghasilkan konteks hourly, mendeteksi unit mismatch, missing, rapid change, flatline candidate, staleness dan ketidakpastian spatial. Policy pilot-quality-2 adalah batas engineering. SQL memeriksa lineage, cutoff, nilai terpilih, pemetaan dan determinisme saat conflict; ia tidak menjalankan ulang seluruh keputusan QC Python. Tidak ada imputation atau training otomatis pada jalur ini.''','''A1 makes one SQL function call per request. The handler accepts application/json up to 8192 bytes and hashes the bytes with SHA-256 before passing JSON to SQL. SQL requires exactly eight fields, schema_version=1.0.0, degC, a uint32 sequence and UTC Z timestamps with up to six fractional digits. An actor advisory transaction lock protects rate limiting, followed by a sensor lock protecting deduplication and QC. An identical retry returns 200 duplicate; changed content under the same boot/sequence returns 409 packet_conflict. New records return 201 stored. QC may persist a rejected reading; rejected does not automatically mean HTTP rejection.

A2 claims each dataset by locking schedule_state, creating a 20-minute lease and a running attempt. The launchd installer configures a 900-second tick; this is installer configuration, not proof of an active job. Nominal policy fetch intervals are 86400 seconds for Copernicus and 21600 for Open-Meteo; native value cadence remains six-hourly/daily/hourly. Offsets are 30600 seconds for salinity/currents, 45000 for nutrients and 16200 for weather. The worker wrapper has a 900-second timeout; HTTP timeout is 40 seconds, response cap four million bytes, and three retry attempts handle network/timeouts/429/selected 5xx with backoff and jitter. Long Retry-After delays are delegated to scheduler backoff.

Open-Meteo pins gfs_global, UTC, wind_speed_unit=ms and forecast_days=3. Its parser checks units, aligned arrays and timezone before assigning UTC to suffix-free labels. Shared returned cells are deduplicated. Copernicus checks product/dataset/version, STAC cadence/grid/depth/units, loads a fixed nearest cell for the two example plots' centroid, checks catalog revision before/after fetching, and decodes through Toolbox/xarray. Nonfinite/extreme fill values become null missing; daily means are not converted into 24 independent samples.

The adapter validates 1–4 grids, exactly two mappings, nonempty values and unique keys; SQL caps batches at two million bytes and 1–5000 values. persist checks lease, policy, dataset version and receipt time before inserting atomically. An existing run_key means duplicate; content changes that alter semantic identity create a new vintage. Grid and demo mapping use ON CONFLICT DO NOTHING with grid identity checks. Statement failure rolls back the entire persistence transaction; claim/attempt state remains and finish_failure is called separately. Lost commit acknowledgement requires status inspection before manual retry.

A3 neither fetches providers nor mutates observations/forecasts. build creates hourly context and detects unit mismatch, missing values, rapid change, flatline candidates, staleness and spatial uncertainty. pilot-quality-2 is an engineering policy. SQL checks lineage, cutoff, selected values, mapping and deterministic output on conflict; it does not rerun all Python QC decisions. This path has no imputation or automatic training.'''),
'lifecycle':('''Pembuatan: UUID disediakan oleh caller/SQL sesuai dictionary; natural keys registry dipin seed/config. Raw, measurement, forecast, QC dan snapshot memiliki trigger pembatas mutasi. Dataset hanya dapat mengubah gate operasional tertentu; identitas dataset, parameter dan grid harus diberi versi baru bila semantiknya berubah. Sensor deployment baru diperlukan untuk perubahan lokasi/kedalaman; active dapat dinonaktifkan.

Ingestion berubah running → succeeded/failed/partial sesuai CHECK dan guard. Attempt regional berubah running → succeeded/duplicate/failed/abandoned. expired lease ditandai abandoned pada claim berikutnya. Feature snapshot berubah draft → sealed; manifest input harus cocok dan row lock induk mencegah race saat sealing. Snapshot A3 langsung immutable setelah insert. Credential dicabut dengan revoked_at atau habis lewat expires_at; ini bukan penghapusan observasi.

A0 awalnya memperbolehkan penutupan effective_until pada mapping. Migrasi 0005 menambah recorded_at dan trigger immutable_alignment_mapping sebelum UPDATE/DELETE. Karena itu instruksi lama untuk menutup mapping dengan UPDATE tidak lagi berlaku pada migrasi lengkap. Resolusi rentang baru harus dirancang tanpa menghapus histori atau melewati trigger secara diam-diam.

Tidak ditemukan job cleanup/retensi berbasis umur, soft delete umum, backup/restore teruji, replikasi lintas DB atau sinkronisasi iOS-cloud. A2 metadata_only adalah kebijakan konten raw, bukan TTL semua tabel. FK tanpa ON DELETE/UPDATE eksplisit memakai NO ACTION; tidak ada cascade delete yang boleh diasumsikan. Prototype FarmStore menghapus farmer beserta plot di memori; ini tidak menjalankan DELETE SQL backend.

Migrasi 0001 initial, 0002 temperature API, 0003 regional ingestion, 0004 provider_updating, 0005 quality alignment. SQL merupakan migrasi maju; rollback/down script NOT FOUND. Deploy scripts memakai administrator untuk provisioning dan memasang worker role; tidak dijalankan pada audit ini. Adopsi migrasi perlu backup, uji schema kosong dan uji upgrade; hal tersebut rekomendasi, bukan hasil pengujian sesi ini.

Keamanan: migration mengaktifkan RLS tabel aplikasi; FORCE RLS=false pada snapshot lama. PUBLIC/anon/authenticated dibatasi, gateway dan worker mendapat EXECUTE fungsi tertentu dengan SECURITY DEFINER serta search_path=pg_catalog. A2/A3 memakai TLS verify-full dan CA hash dipin. Token asli tidak dicetak; credential menyimpan hash. Hak administrator, role membership aktif, bucket policy, encryption-at-rest, rotasi aktual, backup dan recovery produksi UNVERIFIED. Rate-limit log, attempt, QC event dan hash menyediakan audit parsial; tidak ditemukan dead-letter queue atau alerting eksternal terkonfigurasi pada jalur ini.''','''Creation: callers or SQL supply UUIDs as specified in the dictionary; registry natural keys are pinned in seed/config. Raw data, measurements, forecasts, QC and snapshots have mutation guards. Dataset changes are restricted to certain operational gates; semantic changes to dataset, parameter or grid identities require new versions. Location/depth changes require a new sensor deployment; active can be disabled.

Ingestion transitions from running to succeeded/failed/partial under checks and guards. Regional attempts transition from running to succeeded/duplicate/failed/abandoned. An expired lease is marked abandoned on the next claim. Feature snapshots transition draft → sealed; the input manifest must match and a parent row lock prevents races during sealing. A3 snapshots are immutable immediately after insertion. Credentials are revoked using revoked_at or expire through expires_at; neither deletes observations.

A0 initially allowed closing effective_until on mappings. Migration 0005 adds recorded_at and an immutable_alignment_mapping trigger before UPDATE/DELETE. Therefore older instructions to close mappings through UPDATE no longer apply after the full migration chain. New interval resolution requires a design that preserves history without silently bypassing guards.

No age-based cleanup/retention job, general soft delete, tested backup/restore, cross-database replication or iOS-cloud synchronization was found. A2 metadata_only is a raw-content policy, not a TTL for all tables. Foreign keys without explicit ON DELETE/UPDATE use NO ACTION; cascade deletion must not be assumed. Prototype FarmStore deletes farmers and their plots in memory; it does not issue backend SQL DELETE statements.

Migration sequence: 0001 initial, 0002 temperature API, 0003 regional ingestion, 0004 provider_updating, 0005 quality alignment. SQL migrations are forward-only; rollback/down scripts were NOT FOUND. Deployment scripts use administrator access for provisioning and worker-role setup; none was run during this audit. Migration adoption should include backups, empty-schema tests and upgrade tests; these are recommendations, not session test results.

Security: migrations enable RLS on application tables; FORCE RLS=false in the historical snapshot. PUBLIC/anon/authenticated access is restricted; gateway/workers receive selected EXECUTE permissions using SECURITY DEFINER and search_path=pg_catalog. A2/A3 use TLS verify-full with a pinned CA hash. Original tokens are not printed; credentials store hashes. Active administrator privileges, role membership, bucket policies, encryption at rest, actual rotation, production backup and recovery remain UNVERIFIED. Rate-limit logs, attempts, QC events and hashes provide partial auditing; no dead-letter queue or configured external alerting was found on these paths.'''),
'depend':('''Workflow suhu: perangkat mengirim packet → handler → seagis_api.ingest → receipt/observation/QC → reader terotorisasi memanggil history dengan from/to dan cursor → JSON data dan coverage. History mengurutkan observed_at,id; from inklusif, to eksklusif, maksimum tujuh hari, limit default 200/maksimal 500. Coverage memakai bucket jam UTC dan dapat berbeda dari jumlah baris pagination. Status memberi ringkasan deployment/last packet; bukan assessment penyakit.

Workflow regional: dispatcher → claim/fetch/persist → preview memilih run terbaru yang tersedia pada cutoff dan tidak stale menurut policy, membatasi valid_at dua hari ke depan dan maksimum 1500 baris. current_speed adalah join inner komponen; pasangan tidak lengkap tidak menghasilkan baris view, sementara pasangan lengkap dengan missing menghasilkan speed null. Preview demo mempertahankan identitas grid dan batas representativitas.

Workflow iOS: AppContainer menyuntikkan MockAssessmentRepository → LoadDemoAssessment → BootstrapViewModel → SwiftUI. Assessment domain hanya memiliki provenance synthetic_fixture, tidak memiliki DTO backend terverifikasi. FarmStore AppPOC menyimpan Farmer/CultivationPlot dalam array, membuat UUID, men-trim nama, dan menghapus relasi secara in-memory. Tidak ada mapping ID farmer/plot prototype ke seagis.plot yang terverifikasi. Cache/persistensi lokal produksi dan konflik sinkronisasi belum ditemukan implementasinya.

Konsumen analitik yang terverifikasi berupa build QC dan CSV exporter; tabel seagis_features belum memiliki produksi feature builder/training consumer yang ditemukan. Angka coverage hourly tidak dihitung sebagai jumlah pengamatan independen. Tidak ditemukan model ML terlatih yang menghasilkan probabilitas ice-ice pada jalur backend ini.''','''Temperature workflow: device packet → handler → seagis_api.ingest → receipt/observation/QC → authorized reader history call with from/to and cursor → data/coverage JSON. History orders by observed_at,id; from is inclusive and to exclusive, with a seven-day maximum window and default limit 200/maximum 500. Coverage uses UTC hourly buckets and may differ from paginated row counts. Status summarizes deployments/last packets; it is not a disease assessment.

Regional workflow: dispatcher → claim/fetch/persist → preview selects the latest run available at cutoff and not stale under policy, limits valid_at to the next two days and returns at most 1500 rows. current_speed is an inner join of components; incomplete pairs produce no view row, whereas complete pairs containing missing values produce null speed. Demo preview preserves grid identity and representativeness limitations.

The iOS workflow is AppContainer dependency injection → MockAssessmentRepository → LoadDemoAssessment → BootstrapViewModel → SwiftUI. The Assessment domain model only has synthetic_fixture provenance and no verified backend DTO. AppPOC FarmStore keeps Farmer/CultivationPlot arrays, generates UUIDs, trims names and deletes relationships in memory. No verified mapping connects prototype farmer/plot IDs to seagis.plot. Production local caching/persistence and synchronization conflict handling were not found implemented.

Verified analytical consumers are QC building and CSV export; no production feature builder or training consumer was found for seagis_features. Hourly coverage is not counted as independent observations. No trained ML model producing ice-ice probabilities was found on these backend paths.''')}
# Recover explicit INSERT mappings (nested SQL expressions split at top-level commas).
def split_sql(s):
 result=[];start=0;depth=0;quote=False;i=0
 while i<len(s):
  ch=s[i]
  if ch=="'":
   if quote and i+1<len(s) and s[i+1]=="'":i+=2;continue
   quote=not quote
  if not quote:
   if ch=='(':depth+=1
   elif ch==')':depth-=1
   elif ch==',' and depth==0:result.append(s[start:i].strip());start=i+1
  i+=1
 result.append(s[start:].strip());return result

def balanced(s,start):
 depth=0;quote=False;i=start
 while i<len(s):
  if s[i]=="'":
   if quote and i+1<len(s) and s[i+1]=="'":i+=2;continue
   quote=not quote
  if not quote:
   if s[i]=='(':depth+=1
   elif s[i]==')':
    depth-=1
    if depth==0:return s[start+1:i],i+1
  i+=1
 return '',start
INSERTS=collections.defaultdict(list)
for key,v in sources.items():
 if '/migrations/' not in key and not key.endswith('/seed.sql'):continue
 s=v['text']
 for m in re.finditer(r'INSERT\s+INTO\s+([\w]+\.[\w]+)\s*',s,re.I):
  name=m[1]
  if name not in OBJ:continue
  pos=m.end(); names=[c['name'] for c in cols(OBJ[name])]
  if s[pos:pos+1]=='(':
   fieldstr,pos=balanced(s,pos); names=[x.strip() for x in fieldstr.split(',')]
  tail=s[pos:];vm=re.match(r'\s*VALUES\s*\(',tail,re.I)
  if vm:
   values,end=balanced(s,pos+vm.end()-1);exprs=split_sql(values)
  else:
   sm=re.match(r'\s*SELECT\s+',tail,re.I)
   if not sm:continue
   # Stop at FROM at depth zero; select expression uses quoted strings and nested functions.
   begin=pos+sm.end();depth=0;quote=False;end=begin
   for end in range(begin,len(s)):
    ch=s[end]
    if ch=="'":quote=not quote
    if not quote:
     if ch=='(':depth+=1
     elif ch==')':depth-=1
     if depth==0 and (ch==';' or re.match(r'\sFROM\s',s[end:],re.I)):break
   exprs=split_sql(s[begin:end])
  if len(names)!=len(exprs):continue
  ref=f'`{key}:{s[:m.start()].count(chr(10))+1}`'
  for namecol,expr in zip(names,exprs):INSERTS[(name,namecol)].append((ref,re.sub(r'\s+',' ',expr)))
old_origin=origin
def origin(obj,c):
 base=old_origin(obj,c)
 if base[2]=='UNVERIFIED' and INSERTS[(fullname(obj),c['name'])]:
  ref,expr=INSERTS[(fullname(obj),c['name'])][0]
  return (ref,expr,'VERIFIED')
 return base

# Close nullable omitted fields and explicit administrative/fixture boundaries from inspected code.
prior_origin=origin
def origin(obj,c):
 name=fullname(obj);n=c['name']; result=prior_origin(obj,c)
 if name=='seagis.forecast_value' and n in ['native_unit','unit','conversion_code','temporal_support']:
  return ('registered seagis.dataset_parameter par','par.'+n,'VERIFIED')
 if result[2]=='VERIFIED':return result
 overrides={
 'seagis.ingestion_run':{'completed_at':'UPDATE at end of A1/A2: clock_timestamp(); NULL while running','error_code':'A1/A2 successful rows omit -> NULL; failure codes tracked in environment.attempt'},
 'seagis_api.credential':{'label':'provision_a1.create(label) CLI --label','token_sha256':'sha256((sgi_ + secrets.token_urlsafe(32)).encode()).hexdigest(); original token excluded','kind':'provision_a1.create(kind), CLI device/reader','sensor_id':'validated CLI sensor UUID for device, NULL for reader','expires_at':'now()+make_interval(days=>days); CLI 1..365, default 30','revoked_at':'NULL initially; revoke command UPDATE revoked_at=now()'},
 'seagis_api.reader_plot':{'credential_id':'provision_a1.create generated credential UUID','plot_id':'CLI plots validated with UUID(), FK checked by database'},
 'seagis_environment.attempt':{'completed_at':'clock_timestamp() at persist/failure/abandon; initially NULL','error_code':'finish_failure sanitized code or lease_expired on abandoned; otherwise NULL','forecast_run_id':'persist run_id, also on duplicate; NULL before completion'},
 'seagis_environment.schedule_state':{'lease_id':'claim gen_random_uuid(); cleared after persist/failure','lease_until':"claim clock_timestamp()+interval 20 minutes; cleared after persist/failure",'last_success_at':'persist t=clock_timestamp()','last_attempt_at':'claim clock_timestamp()','last_error_code':'finish_failure sanitized code; cleared on success','last_forecast_run_id':'persist run_id'},
 'seagis_quality.policy':{'version':'register_policy policy[version]','definition':'register_policy JSON policy argument (config/a3_quality.json)','policy_sha256':'register_policy policy_hash from digest(policy)','code_sha256':'register_policy builder_hash from code_hash()'}
 }
 if n in overrides.get(name,{}):return ('owning routine / caller',overrides[name][n],'VERIFIED')
 if obj['schema']=='seagis_features':
  if n=='input_manifest_sha256':return ('seagis_features.manifest_hash(snapshot)','SHA256 sorted input references at draft -> sealed','VERIFIED')
  return ('A0 fixtures/tests; production builder NOT FOUND','caller-supplied '+n+' subject to guard_input/guard_snapshot; no production derivation claimed','VERIFIED')
 if name=='seagis.plot_grid_mapping':return ('A0 fixtures/test SQL; operational creator NOT FOUND','caller-supplied '+n+' subject to FK/CHECK/guard_mapping; recorded_at SQL default','VERIFIED')
 if not c['not_null'] and not c['default_expression']:
  return ('active loader omits column / nullable schema','NULL in inspected A1/A2 path; other callers may supply under schema guards','VERIFIED')
 return result

FINDINGS=[
('F01','High','Contract / integration',('Assessment iOS belum terhubung ke backend','iOS assessment is not connected to backend'),('Mock mengembalikan synthetic_fixture; tidak ada adapter API assessment yang ditemukan. Konsumen baru tidak boleh menganggap model domain sebagai wire contract.','The mock returns synthetic_fixture; no assessment API adapter was found. New consumers must not treat the domain model as a wire contract.'),['Seagis/Seagis/Repositories/Shared/MockAssessmentRepository.swift','Seagis/Seagis/Models/Shared/Assessment.swift'],('Sepakati kontrak executable dan mapping provenance/error sebelum integrasi.','Agree an executable contract and provenance/error mapping before integration.'),'VERIFIED'),
('F02','Medium','Lifecycle',('Mapping immutable setelah 0005 mengubah prosedur penutupan lama','Mapping immutability after 0005 changes the old closing procedure'),('guard_mapping A0 mengizinkan penutupan interval; trigger 0005 menolak seluruh UPDATE/DELETE. Petunjuk arsitektur A0 untuk menutup mapping dapat gagal pada schema lengkap.','A0 guard_mapping permits interval closure; the 0005 trigger rejects all UPDATE/DELETE. A0 architecture instructions for closing mappings can fail on the complete schema.'),['supabase/migrations/0001_initial_schema.sql','supabase/migrations/0005_quality_alignment.sql','docs/architecture.md'],('Definisikan prosedur append-only untuk supersession dan uji overlap/cutoff.','Define append-only supersession and test interval overlap/cutoff.'),'VERIFIED'),
('F03','Medium','Governance / retention',('Riwayat tumbuh tanpa job retensi yang ditemukan','History grows without a discovered retention job'),('request_event, observation, forecast dan snapshot append-only; TTL/cleanup terjadwal dan recovery test tidak ditemukan di checkout. Risiko kapasitas adalah inferensi, bukan hasil benchmark.','request_event, observations, forecasts and snapshots are append-only; scheduled TTL/cleanup and recovery tests were not found in the checkouts. Capacity risk is inferred, not benchmarked.'),['supabase/migrations/0001_initial_schema.sql','supabase/migrations/0002_temperature_api.sql','supabase/migrations/0005_quality_alignment.sql'],('Tetapkan retention per domain, archival, backup dan restore drill sebelum skala produksi.','Set domain retention, archival, backups and restore drills before production scale.'),'INFERRED'),
('F04','Medium','Validation boundary',('SQL A3 memeriksa lineage tetapi tidak menghitung ulang seluruh QC','A3 SQL checks lineage but does not recompute all QC'),('save_snapshot memeriksa hash policy/kode dan nilai sumber, tetapi keputusan usable_context/flags/blocking_flags tidak direkalkulasi melalui Python di DB. Role worker tetap trust boundary.','save_snapshot verifies policy/code hashes and source values, but usable_context/flags/blocking_flags decisions are not recomputed through Python inside the DB. The worker role remains a trust boundary.'),['supabase/migrations/0005_quality_alignment.sql','scripts/quality/alignment.py'],('Dokumentasikan trust worker; bila diperlukan, verifikasi deterministik QC tambahan dan test payload tampering.','Document worker trust; add deterministic QC verification and payload-tampering tests where required.'),'VERIFIED'),
('F05','Medium','Data provenance',('Metadata-only membatasi reproduksi raw','Metadata-only limits raw reproducibility'),('A2 tidak menyimpan raw content. Hash subset Toolbox bukan hash byte NetCDF/Zarr asli; memperoleh ulang aggregate provider tidak menjamin vintage yang sama.','A2 retains no raw content. A Toolbox subset hash is not an original NetCDF/Zarr byte hash; refetching a provider aggregate does not guarantee the same vintage.'),['scripts/environmental/copernicus.py','supabase/migrations/0003_environment_ingestion.sql'],('Pertahankan hash_basis; bila lisensi dan biaya disetujui, usulkan penyimpanan subset/objek versi immutable.','Preserve hash_basis; if licence and cost allow, propose immutable versioned subset/object retention.'),'VERIFIED'),
('F06','High','Analytics semantics',('CSV capture bukan backtest historis','Capture CSV is not a historical backtest'),('Exporter memilih latest_available_at_capture; A3 memakai cutoff tiap jam. Memakai CSV tersebut sebagai histori availability berisiko leakage; training_authorized=false sudah dinyatakan kode.','The exporter selects latest_available_at_capture; A3 uses a per-hour cutoff. Treating the CSV as historical availability risks leakage; code explicitly sets training_authorized=false.'),['scripts/export_experiment_csv.py','scripts/quality/alignment.py'],('Gunakan source bundles seluruh vintage dan cutoff eksplisit untuk rancangan backtest; jangan melepas gate training tanpa validasi.','Use all-vintage source bundles and explicit cutoffs when designing backtests; retain the training gate until validation.'),'VERIFIED'),
('F07','Low','Documentation drift',('Dokumen A0 mendahului implementasi A1–A3','A0 documentation predates A1–A3 implementation'),('docs/architecture.md mengatakan ingestion/scheduler/QC belum diimplementasikan, sedangkan migrasi dan worker berikutnya ada. Pernyataan harus dibaca dengan fase dan tanggal.','docs/architecture.md says ingestion/scheduler/QC are not implemented, while subsequent migrations and workers exist. Statements require phase/date context.'),['docs/architecture.md','scripts/ingest_environment.py','scripts/curate_environment.py'],('Gunakan indeks status fase serta source-manifest untuk pembaruan dokumentasi.','Use a phase-status index and source manifest for documentation updates.'),'VERIFIED'),
('F08','Medium','Runtime verification',('Snapshot catalog berumur lima hari','Catalog snapshot is five days old'),('Snapshot 22 Oktober bukan audit runtime 27 Oktober. Grants, row count, cron aktif dan migrasi cloud terkini tidak diverifikasi ulang.','The 22 October snapshot is not a 27 October runtime audit. Grants, row counts, active schedules and current cloud migrations were not reverified.'),[],('Lakukan diff catalog read-only dan review grants sebelum keputusan produksi.','Run a read-only catalog diff and grants review before production decisions.'),'UNVERIFIED')]

def section_inventory(lang):
 s=TEXT['architecture'][lang=='en']+'\n\n'
 rows=[['PostgreSQL / Supabase','VERIFIED (repository + historical catalog)',T('Backend; lingkungan deployment terkini UNVERIFIED','Backend; current deployment environment UNVERIFIED',lang),'Seagis-Model',T('Registri, sensor, regional, QC, fitur','Registry, sensor, regional, QC, features',lang),'read/write via stored functions',T('Otoritatif untuk record yang tersimpan; bukan diagnosis','Authoritative for persisted records; not a diagnosis',lang),evidence('supabase/migrations/0001_initial_schema.sql')],
 ['Supabase Storage','configured / UNVERIFIED usage',T('Storage enabled lokal; object_uri didukung, bucket aplikasi NOT FOUND','Local storage enabled; object_uri supported, application bucket NOT FOUND',lang),'Supabase','objects / metadata_only','configured',T('Tidak dibuktikan sebagai penyimpan raw aktif','Not proven to be active raw storage',lang),evidence('supabase/config.toml',r'^\[storage\]')],
 ['UserDefaults / launch arguments','VERIFIED code',T('Akses preferensi/debug UI; bukan penyimpan plot','Preference/debug UI access; not plot persistence',lang),'AppPOC','initialPlot / initialFarmer / skipCaptureSteps / detailDay','read preference/argument values',T('Tidak otoritatif untuk data backend','Not authoritative for backend data',lang),evidence('AppPOC/POCApp/Features/FarmMap/ViewModels/FarmMapViewModel.swift')],
 ['legacy AR files','VERIFIED cleanup code',T('File ar-site.json/ar-site.worldmap hanya dihapus saat sesi AR baru','ar-site.json/ar-site.worldmap are only deleted at new AR session start',lang),'AppPOC','legacy local AR files','best-effort delete; active writer NOT FOUND',T('Bukan persistence aktif','Not active persistence',lang),evidence('AppPOC/POCApp/Features/PlotCapture/ViewModels/ARCaptureViewModel.swift')],
 ['JSON / CSV files','VERIFIED code',T('Fixture sintetis, policy, export eksperimen dan manifest','Synthetic fixtures, policies, experimental exports and manifests',lang),'Python scripts','fixtures/config/export','file read/write',T('Hanya otoritatif untuk capture/fixture versinya','Authoritative only for that capture/fixture version',lang),evidence('scripts/export_experiment_csv.py')],
 ['in-memory Swift arrays','VERIFIED code',T('State prototype; hilang saat proses berakhir','Prototype state; lost at process termination',lang),'AppPOC','Farmer / CultivationPlot','array append/remove',T('State demo lokal','Local demo state',lang),evidence('AppPOC/POCApp/Shared/Data/FarmStore.swift')]]
 s+=table(['Store','Evidence status',T('Tujuan/lingkungan','Purpose/environment',lang),'Owner','Scope','Access',T('Otoritas','Authority',lang),'Evidence'],rows)
 s+=T('Default layanan Supabase auth, vector dan analytics tercantum dalam config lokal, tetapi bucket/index/dataset aplikasi aktif tidak dibuktikan. Ini konfigurasi layanan, bukan database aplikasi tambahan. Jumlah baris seluruh tabel: UNVERIFIED; tidak diestimasi dari fixture.\n\n','Supabase auth, vector and analytics service defaults appear in local configuration, but active application buckets/indexes/datasets are not established. These are service settings, not additional application databases. All table row counts are UNVERIFIED; fixtures are not used as runtime estimates.\n\n',lang)
 rows=[]
 for schema in META['schemas']:
  name=schema['name']; oo=[o for o in META['objects'] if o['schema']==name]
  rows.append([name,', '.join(o['name'] for o in oo),len([o for o in oo if o['kind']=='r']),len([o for o in oo if o['kind']=='v']),T('Akses melalui routine backend; membership live UNVERIFIED','Access through backend routines; live membership UNVERIFIED',lang)])
 s+=table(['Schema',T('Objek','Objects',lang),'Tables','Views',T('Batas akses','Access boundary',lang)],rows)
 s+=table([T('Objek fisik','Physical object',lang),T('Fungsi','Purpose',lang),T('Kolom','Columns',lang),'Evidence'],[[fullname(o),PURPOSE[fullname(o)][lang=='en'],len(cols(o)),sqlref(o)] for o in META['objects']])
 return s

def section_dictionary(lang):
 s=T('Domain seagis.finite_float adalah double precision yang menolak NaN dan infinity; NULL tetap diatur kolom. value_status present memerlukan angka; status nonpresent memerlukan null; valid_value/valid_support serta guard SQL menetapkan aturan lintas field. Presipitasi mm adalah total satu jam, salinitas 1e-3 tidak otomatis PSU/ppt, wind direction adalah arah dari dalam derajat. Metadata tipe/null/default/constraint/index berasal dari snapshot catalog 22 Oktober; definisi SQL diverifikasi terhadap rantai migrasi lokal 0001–0005. Baris view tidak memiliki PK/FK fisik walaupun field-nya berasal dari measurement. Contoh adalah ilustrasi sintetis dan belum tentu satu row INSERT yang valid. NOT APPLICABLE berarti atribut tidak relevan; UNVERIFIED berarti semantik atau derivasi spesifik belum dibuktikan.\n\n','The seagis.finite_float domain is double precision rejecting NaN and infinity; column nullability remains separate. value_status present requires numbers; nonpresent statuses require null; valid_value/valid_support and SQL guards enforce cross-field rules. Precipitation mm is a one-hour total, salinity 1e-3 is not automatically PSU/ppt, and wind direction is the direction from in degrees. Type/null/default/constraint/index metadata comes from the 22 October catalog snapshot; SQL definitions were checked against the local 0001–0005 migration chain. View rows have no physical PK/FK even when fields originate from measurements. Examples are synthetic illustrations, not necessarily a valid complete INSERT row. NOT APPLICABLE means an attribute does not apply; UNVERIFIED means a specific meaning or derivation is not established.\n\n',lang)
 for idx,o in enumerate(META['objects'],1):
  name=fullname(o);writers,readers=ownership(o)
  s+=f'### 4.{idx} `{name}`\n\n'+PURPOSE[name][lang=='en']+'\n\n'
  cc=cons(o);pks=[x['definition'] for x in cc if x['kind']=='p'];uks=[x['definition'] for x in cc if x['kind']=='u']
  triggers=[x for x in META['triggers'] if x['schema']==o['schema'] and x['table_name']==o['name']]
  s+=table([T('Atribut','Attribute',lang),T('Definisi','Definition',lang)],[['Schema / domain',o['schema']],['Kind', 'view' if o['kind']=='v' else 'table'],['Primary key','; '.join(pks) or 'NOT APPLICABLE: view'],['Unique','; '.join(uks) or 'NOT FOUND'],['Rows','UNVERIFIED'],['Writer',writers],['Reader',readers],[T('Otoritas','Authority',lang),T('Record domain ini; registry/config atau sumber asal tetap ditelusuri','Records of this domain; registry/config or original source remains traceable',lang)],['Lifecycle',T('Lihat trigger di bawah dan Bab 9; tanpa TTL terverifikasi','See triggers below and Chapter 9; no verified TTL',lang)],['Evidence',sqlref(o)]])
  for c in cols(o):
   ck=constraints_for(o,c); pk=any(x['kind']=='p' for x in ck); fks=[x['definition'] for x in ck if x['kind']=='f'];unique=any(x['kind'] in ['p','u'] and x['columns']==[c['name']] for x in ck)
   meaning=MEAN.get(c['name'])
   if c['name']=='status':
    meaning={'ingestion_run':('running/succeeded/failed/partial beserta completed_at','running/succeeded/failed/partial together with completed_at'),'attempt':('running/succeeded/duplicate/failed/abandoned untuk fetch attempt','running/succeeded/duplicate/failed/abandoned fetch-attempt state'),'feature_snapshot':('draft sebelum sealing, sealed setelah manifest cocok','draft before sealing, sealed after manifest verification')}.get(o['name'])
   if o['name']=='temperature_policy' and c['name']=='id':meaning=('Singleton boolean harus true; bukan UUID','Singleton boolean must be true; not a UUID')
   assert meaning,(name,c['name'])
   src,expr,status=origin(o,c)
   typ=c['type'];example='NOT APPLICABLE'
   if 'uuid' in typ:example='00000000-0000-4000-8000-000000000001'
   elif 'timestamp' in typ:example='2026-10-21T12:00:00Z'
   elif typ=='boolean':example='true'
   elif typ in ['integer','bigint','double precision','seagis.finite_float']:example='1'
   elif typ=='jsonb':example='{}'
   elif typ.endswith('[]'):example='[]'
   else:example=T('Lihat nilai enum/CHECK di bawah; contoh bebas tidak diasumsikan valid','See enum/CHECK below; arbitrary example is not presumed valid',lang)
   units='NOT APPLICABLE'
   if c['name'] in ['value','native_value','detection_limit']:units=T('Mengikuti unit/native_unit dan dataset_parameter','Defined by unit/native_unit and dataset_parameter',lang)
   elif c['name'].endswith('_m') or c['name']=='speed_m_s':units='m/s' if c['name']=='speed_m_s' else 'm'
   elif c['name'].endswith('_seconds'):units='s'
   elif c['name'].endswith('_degc'):units='degC'
   elif c['name'] in ['latitude','longitude','example_latitude','example_longitude','resolution_lat_deg','resolution_lon_deg']:units='degree'
   vals='; '.join(x['definition'] for x in ck if x['kind']=='c') or T('Tidak ada CHECK lokal; constraint lintas tabel/trigger tetap berlaku','No local CHECK; cross-table constraints/triggers still apply',lang)
   times=T('Instan timestamptz, presisi PostgreSQL mikrodetik; tampilan mengikuti session. Kontrak API A1 wajib UTC Z. next_attempt_at mendukung -infinity.','timestamptz instant, PostgreSQL microsecond precision; display follows session. A1 API requires UTC Z. next_attempt_at supports -infinity.',lang) if 'timestamp' in typ else 'NOT APPLICABLE'
   s+='#### `'+name+'.'+c['name']+'`\n\n'
   s+=table([T('Atribut','Attribute',lang),T('Definisi','Definition',lang)],[
    ['Type / nullable',f'`{typ}` / '+('false' if c['not_null'] else 'true')],['Default / generated',('`'+str(c['default_expression'])+'`') if c['default_expression'] else 'NOT FOUND'],
    ['PK / unique',f'{str(pk).lower()} / {str(unique).lower()}'+T(' (unique satu kolom; composite di bawah)',' (single-column uniqueness; composites below)',lang)],['FK','; '.join(fks) or 'NOT APPLICABLE'],
    [T('Arti bisnis / teknis','Business / technical meaning',lang),meaning[lang=='en']],['Valid values / checks',vals],['Units / time',units+'; '+times],['Example',example],
    [T('Asal / transformasi','Origin / transformation',lang),src+' → `'+str(expr)+'` ('+status+')'],
    [T('Mutasi / konsumen','Mutation / consumers',lang),T('Mengikuti trigger/mutasi tabel, bukan asumsi mutable; ','Follows table triggers/mutations, not assumed mutable; ',lang)+readers],['Evidence',sqlref(o)+'; catalog '+name+'.'+c['name']]])
  s+='#### '+T('Constraint, indeks dan trigger','Constraints, indexes and triggers',lang)+'\n\n'
  for label,items in [('constraints',[x['definition'] for x in cc]),('indexes',[x['definition'] for x in META['indexes'] if x['schema']==o['schema'] and x['table_name']==o['name']]),('triggers',[x['definition'] for x in triggers])]:
   s+='**'+label+'**\n'+(code(';\n'.join(items)+';') if items else 'NOT APPLICABLE / NOT FOUND\n\n')
  if o['kind']=='v':s+=code(next(v['definition'] for v in META['views'] if v['schema']==o['schema'] and v['name']==o['name']))
  else:s+=T('RLS pada snapshot: ','RLS at snapshot: ',lang)+str(o['rls'])+'; FORCE RLS: '+str(o['force_rls'])+'. '+T('Membership/grant terkini UNVERIFIED.','Current membership/grants UNVERIFIED.',lang)+'\n\n'
 return s

def section_relations(lang):
 s=T('Semua relasi di bawah adalah FK fisik dari catalog lama dan migrasi. Parent memiliki 0..N child kecuali child join key unik, yang membatasi 0..1 child; child merujuk tepat satu parent bila seluruh kolom NOT NULL, atau 0..1 bila nullable dengan MATCH SIMPLE. FK composite mengikat dataset/flag sintetis agar lineage tidak tercampur. Keberadaan FK tidak membuktikan parent wajib mempunyai child.\n\n','All relationships below are physical foreign keys from the historical catalog and migrations. A parent has 0..N children unless the child join key is unique, limiting it to 0..1; a child references exactly one parent when all columns are NOT NULL, or 0..1 when nullable under MATCH SIMPLE. Composite foreign keys bind dataset/synthetic flags to prevent lineage mixing. A foreign key does not require a parent to have children.\n\n',lang)
 for i,f in enumerate(FKS,1):
  null,unique=relation_info(f);child=f['schema']+'.'+f['table_name'];parent=f['target_schema']+'.'+f['target_table']
  s+=f'### FK{i} `{parent}` → `{child}`\n\n'
  s+=table([T('Atribut','Attribute',lang),T('Definisi','Definition',lang)],[['Constraint',f['name']],['Join','('+','.join(f['columns'])+') → ('+','.join(f['target_columns'])+')'],['Cardinality',('1:0..1' if unique else '1:0..N')+'; child → parent '+('0..1' if null else '1')],['Optional',str(null).lower()],['ON DELETE / ON UPDATE','NO ACTION / NO ACTION (default)' if 'ON DELETE' not in f['definition'] and 'ON UPDATE' not in f['definition'] else f['definition']],['Meaning',PURPOSE[child][lang=='en']],[T('Risiko integritas','Integrity risk',lang),T('FK menolak orphan; nullable composite memakai MATCH SIMPLE. Semantik QC/waktu memerlukan guard tambahan.','FK rejects orphans; nullable composites use MATCH SIMPLE. QC/time semantics need additional guards.',lang)],['Evidence',sqlref(OBJ[child])]])
  s+=code(f['definition']+';')
 s+=T('Relasi logis tambahan: dua alias forecast_value di current_speed bergabung pada forecast_run_id, source_grid_id, valid_at; parameter_code membedakan u/v. Ini join view, bukan FK baru. source_ref memakai prefix typed dan CHECK serta dua FK alternatif; tidak dibuat FK ke string polimorfik. Tidak ditemukan self-reference FK. reader_plot, dataset_parameter, feature_input dan snapshot_input berperan sebagai association/lineage, dengan composite key/unique yang tercantum pada dictionary. Relasi Farmer→CultivationPlot berada di memori AppPOC dan tidak masuk 47 FK PostgreSQL.\n\n','Additional logical relationships: two forecast_value aliases in current_speed join on forecast_run_id, source_grid_id and valid_at; parameter_code distinguishes u/v. This is a view join, not a new FK. source_ref uses typed prefixes, a CHECK and two alternative FKs; no invented FK targets a polymorphic string. No self-referencing FK was found. reader_plot, dataset_parameter, feature_input and snapshot_input act as association/lineage entities, with composite keys/uniqueness recorded in the dictionary. AppPOC Farmer→CultivationPlot is an in-memory relationship and is excluded from the 47 PostgreSQL FKs.\n\n',lang)
 s+=T('ERD lengkap dan per schema terdapat pada modul architecture/ERD.md.','Full and per-schema ERDs are in architecture/ERD.md.',lang)+'\n\n'
 return s

def section_mapping(lang):
 s=T('Setiap kolom tujuan memiliki satu baris pemetaan. VERIFIED berarti ekspresi/default/join memiliki bukti; pemetaan administrasi/fixture bukan klaim loader produksi. UNVERIFIED menandai derivasi yang belum ditutup dan dihitung sebagai gap. Lihat kamus data untuk tipe, arti dan guard; ekspresi SQL mempertahankan identifier asli.\n\n','Every destination column has a mapping row. VERIFIED means an expression/default/join has evidence; an administrative/fixture mapping does not imply a production loader. UNVERIFIED marks unresolved derivations and is counted as a gap. Consult the dictionary for types, meanings and guards; SQL expressions retain original identifiers.\n\n',lang)
 rows=[]
 for o in META['objects']:
  for c in cols(o):
   src,expr,status=origin(o,c);rows.append([fullname(o),c['name'],src,expr,ownership(o)[0],status,sqlref(o)])
 return s+table(['Destination table','Column','Source / field',T('Transformasi','Transformation',lang),'Loader / trigger','Status','Evidence'],rows)
CONTRACTS=[
('C01','source.schema.json','A0 source envelope','fixture/provider logical extract','validate_source','JSON / Draft 2020-12','explicit','seagis.ingestion_run + seagis_raw.raw_payload','scripts/validate_contracts.py'),
('C02','normalized.schema.json','A0 normalized envelope','fixture normalization','validate_normalized + SQL guards','JSON / Draft 2020-12','explicit','observation / forecast_run / forecast_value / source_grid','scripts/validate_contracts.py'),
('C03','iot-packet.schema.json','A1 device packet','device/simulator','temperature handler + seagis_api.ingest','JSON / HTTP POST','explicit','observation + raw_payload + packet_receipt + quality_event','supabase/functions/temperature/handler.ts'),
('C04','alignment.schema.json','A3 alignment document','scripts/quality/alignment.py::build','seagis_quality.save_snapshot','JSON / SQL jsonb','explicit','seagis_quality.alignment_snapshot + snapshot_input','scripts/curate_environment.py'),
('C05',None,'A1 history/status/replies','seagis_api.history/status/reply','authorized reader','JSON / HTTP GET','implementation-derived','observation + sensor + packet_receipt','supabase/migrations/0002_temperature_api.sql'),
('C06',None,'A2 adapter batch/lease','Adapter.envelope + claim','seagis_environment.persist','JSON / SQL jsonb','implementation-derived','raw_payload + forecast_run + forecast_value + source_grid + demo_grid_mapping','scripts/environmental/common.py'),
('C07',None,'A3 source_bundle','seagis_quality.source_bundle','build / CSV exporter','JSON / SQL jsonb','implementation-derived','plot + sensor + dataset_parameter + mappings + observation + forecast_value','supabase/migrations/0005_quality_alignment.sql'),
('C08',None,'CSV experiment-csv-2','export_experiment_csv.py::export','offline experiments / developer','CSV + JSON manifest','implementation-derived','derived files; no database writes','scripts/export_experiment_csv.py'),
('C09',None,'iOS Assessment domain','MockAssessmentRepository','LoadDemoAssessment / ViewModel','Swift structs','implementation-derived / mock','NOT APPLICABLE: no backend mapping','Seagis/Seagis/Models/Shared/Assessment.swift'),
('C10',None,'Open-Meteo response','Open-Meteo forecast API','OpenMeteo.parse/normalize','JSON hourly arrays','implementation-derived','forecast_value + grid + raw manifest','scripts/environmental/open_meteo.py'),
('C11',None,'Copernicus subset','Copernicus Toolbox/xarray + STAC','Copernicus.parse/normalize','xarray + canonical logical JSON subset','implementation-derived','forecast_value + grid + raw manifest','scripts/environmental/copernicus.py')]

def schema_fields(schema):
 rows=[]
 def visit(node,path,required):
  if not isinstance(node,dict):return
  if path and any(k in node for k in ['type','$ref','const','enum','properties']):rows.append((path,required,node))
  for k,v in node.get('properties',{}).items():visit(v,path+'.'+k if path else k,k in node.get('required',[]))
  if isinstance(node.get('items'),dict):visit(node['items'],path+'[]',True)
  for k,v in node.get('$defs',{}).items():visit(v,'$defs.'+k,False)
  for k in ['oneOf','anyOf','allOf']:
   for i,v in enumerate(node.get(k,[])):visit(v,path+f'/{k}/{i}',False)
 visit(schema,'',False);return rows

CONTRACT_MEAN={
'schema_version':('Versi struktur kontrak; bukan versi model biologis','Contract structure version; not a biological model version'),
'boot_id':('Identitas sesi boot sensor untuk idempotensi','Sensor boot-session identity for idempotency'),
'sequence':('Counter uint32 dalam satu boot; key digabung dengan boot_id','uint32 counter within one boot; key combined with boot_id'),
'water_temperature':('Suhu air degC atau null missing; bukan suhu udara','Water temperature in degC or null missing; distinct from air temperature'),
'measurements':('Daftar observation/forecast_value yang divalidasi lintas field','Cross-field-validated observation/forecast_value list'),
'rows':('Baris konteks per jam UTC; bukan sampel independen tambahan','UTC hourly context rows; not additional independent samples'),
'cells':('Konteks tiap dataset/parameter pada cutoff jam','Per-dataset/parameter context at the hourly cutoff'),
'lineage':('Referensi typed record terpilih dan input pendukung QC','Typed references to selected records and supporting QC inputs'),
'flags':('Peringatan QC/konteks, bukan severity penyakit','QC/context flags, not disease severity'),
'blocking_flags':('Alasan konteks tidak dapat dipakai menurut builder','Reasons context is unusable under the builder'),
'usable_context':('Keputusan QC builder untuk review; bukan izin training','Builder QC decision for review; not training authorization'),
'age_seconds':('Umur source_time terhadap cutoff dalam detik','Age of source_time relative to cutoff in seconds'),
'vintage_age_seconds':('Umur run terhadap cutoff dalam detik','Run age relative to cutoff in seconds'),
'training_authorized':('Harus false; review/demo bukan dataset training yang disahkan','Must be false; review/demo is not an approved training dataset'),
'source_registry':('Salinan kontrak parameter yang dibandingkan dengan bundle SQL','Parameter-contract copy checked against the SQL bundle'),
'sensor_deployments':('Salinan identitas deployment untuk pemeriksaan konsistensi','Deployment-identity copy for consistency checks'),
'spatial':('Metadata pemetaan grid, resolusi, jarak dan kedalaman','Grid mapping, resolution, distance and depth metadata'),
'quality_report':('Ringkasan QC dan coverage berbasis konteks jam','QC summary and coverage based on hourly context'),
'coverage_fraction':('usable_contexts / expected_hourly_contexts','usable_contexts / expected_hourly_contexts'),
'expected_hourly_contexts':('Jumlah slot jam pada jendela, bukan jumlah sampel asli','Hourly slots in window, not native sample count'),
'unique_selected_source_records':('Jumlah record asal unik yang dipilih','Count of distinct selected source records'),
'use':('Pembatas penggunaan dokumen quality_alignment_review','Document use restriction quality_alignment_review'),
'body':('Dokumen respons/rincian yang ditetapkan routine','Response/detail document defined by the routine'),
'at':('Cutoff jam UTC untuk pemilihan konteks','UTC hourly cutoff for context selection'),
'source_time':('observed_at sensor atau valid_at model','Sensor observed_at or model valid_at'),
'source_id':('Typed reference record asal terpilih, atau null','Typed reference to selected source record, or null'),
'source_type':('Jenis adapter asal yang menentukan payload fixture','Source adapter kind determining the fixture payload'),
'records':('Gabungan observation dan forecast_value dari source_bundle','Combined observations and forecast_values from source_bundle')}

def section_contracts(lang):
 s=T('Kontrak eksplisit berupa empat JSON Schema; tujuh kontrak lain diturunkan dari implementasi. Klasifikasi tidak menyatakan semuanya endpoint publik. Tidak ditemukan version negotiation umum; versi/schema konstan ditolak bila tidak sesuai. Perubahan breaking memerlukan versi baru dan consumer review, bukan kompatibilitas otomatis. Error JSON yang dicontohkan di bawah berasal dari handler/SQL, bukan error standar yang diasumsikan.\n\n','Four contracts are explicit JSON Schemas; seven additional contracts are implementation-derived. This classification does not make them all public endpoints. No general version negotiation was found; mismatched constant versions/schemas are rejected. Breaking changes need a new version and consumer review, not assumed automatic compatibility. JSON errors below come from handler/SQL, not an invented standard error format.\n\n',lang)
 s+=table(['ID','Contract','Producer','Consumer','Interface','Class','Database','Evidence'],[[a,c,d,e,f,g,h,evidence(i)] for a,b,c,d,e,f,g,h,i in CONTRACTS])
 for cid,filename,name,producer,consumer,interface,classification,mapping,path in CONTRACTS:
  s+=f'### {cid} {name}\n\n'
  s+=table([T('Atribut','Attribute',lang),T('Definisi','Definition',lang)],[['Producer → consumer',producer+' → '+consumer],['Interface / format',interface],['Classification',classification],['Database mapping',mapping],['Compatibility',T('Versi konstan bila ditetapkan; negosiasi umum NOT FOUND','Constant version where defined; general negotiation NOT FOUND',lang)],['Evidence',evidence(path)]])
  if filename:
   sch=json.loads((BACK/'contracts'/filename).read_text());rows=[]
   for field,required,n in schema_fields(sch):
    k=field.split('.')[-1].replace('[]','');meaning=MEAN.get(k) or CONTRACT_MEAN.get(k)
    meaning=meaning[lang=='en'] if meaning else T('UNVERIFIED: struktur/field kontrak; arti rinci mengikuti validator dan contoh sumber, belum seluruhnya diverifikasi','UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified',lang)
    details={k:v for k,v in n.items() if k not in ['properties','items','$defs','allOf','oneOf','anyOf']}
    types=n.get('type',n.get('$ref','const/enum' if ('const' in n or 'enum' in n) else 'object'))
    resolved=n
    if '$ref' in n and n['$ref'].startswith('#/'):
     resolved=sch
     for segment in n['$ref'][2:].split('/'):resolved=resolved[segment]
    resolved_type=resolved.get('type')
    nullable=(('null' in resolved_type) if isinstance(resolved_type,list) else resolved_type=='null') if resolved_type is not None else (None in resolved['enum'] if 'enum' in resolved else (resolved['const'] is None if 'const' in resolved else 'UNVERIFIED: conditional schema'))
    if 'const' in n:ex=n['const']
    elif 'enum' in n:ex=n['enum'][0]
    elif nullable is True:ex=None
    elif resolved_type=='integer':ex=max(1,n.get('minimum',1))
    elif resolved_type=='number':ex=max(0,n.get('minimum',0))
    elif resolved_type=='boolean':ex=False
    elif resolved_type=='array':ex=[]
    elif resolved_type=='object':ex={}
    elif n.get('format')=='uuid':ex='00000000-0000-4000-8000-000000000001'
    elif n.get('format')=='date-time':ex='2026-10-21T12:00:00Z'
    else:ex=T('Lihat fixture/schema lengkap; contoh field mandiri belum diverifikasi','See complete fixture/schema; standalone field example unverified',lang)
    field_semantics=T('Satuan/waktu mengikuti unit dan parameter registry; UTC untuk envelope normalized.','Units/time follow unit and parameter registry; UTC for normalized envelopes.',lang) if k in ['value','native_value','detection_limit','observed_at','valid_at','available_at','source_time','start_at','end_at','received_at'] else 'NOT APPLICABLE / schema'

    rows.append([field,json.dumps(types,ensure_ascii=False),required,nullable,n.get('default','NOT FOUND'),meaning,json.dumps(details,ensure_ascii=False),field_semantics,json.dumps(ex,ensure_ascii=False),mapping])
   s+=table(['Field','Type / ref','Required','Nullable','Default',T('Arti','Meaning',lang),'Validation / allowed values','Units / timestamp','Example (illustrative)','DB mapping (boundary)'],rows)
   s+=T('Schema lengkap untuk aturan kondisional dan struktur polimorfik (required di atas berlaku dalam parent masing-masing):\n','Complete schema for conditional rules and polymorphic structures (required above applies within each parent):\n',lang)+code(json.dumps(sch,indent=2,ensure_ascii=False),'json')
  else:
   if cid=='C05':
    s+=table(['Field / group','Type / required',T('Arti / validasi / mapping','Meaning / validation / mapping',lang)],[['from, to','string / required','UTC Z; from<to; <=7 days; observation.observed_at [from,to)'],['limit','integer string / optional; default 200','1..500'],['cursor','UUID / optional','observation.id inside plot/window; ordering observed_at,id'],['code, request_id','string, UUID / response','SQL reply / handler error'],['observations[]','array / history response','id,sensor_id,value,unit,value_status,observed_at,ingested_at,quality_status,flags,ingestion_run_id,is_synthetic'],['coverage','object','expected_hours,hours_with_packets,hours_with_usable_values,missing_hours,unusable_hours'],['next_cursor','UUID|null','last returned row if another page exists']])
   elif cid=='C06':
    fields=['dataset_key','purpose','terms_review','dataset_version','provider_dataset_id','run_key','raw_sha256','raw_byte_size','hash_basis','format','started_at','received_at','metadata','grids','mappings','values']
    s+=table(['Field','Required',T('Validasi / pemetaan','Validation / mapping',lang)],[[f,True,MEAN.get(f,CONTRACT_MEAN.get(f,(T('Lihat persist/envelope','See persist/envelope',lang),)*2))[lang=='en']+'; '+mapping] for f in fields])
    s+=T('Nested grids berisi key, latitude, longitude, depth_m, identity_basis; values berisi grid_key, parameter, value, native_unit, unit, conversion_code, value_status, valid_at, temporal_support, interval_status dan period bounds. mappings membawa identitas plot dan jarak contoh. SQL memeriksa kehadiran field envelope, lease, tujuan/lisensi, hash 64 hex, jumlah grid/nilai/mapping; bukan JSON Schema universal.\n\n','Nested grids contain key, latitude, longitude, depth_m and identity_basis; values contain grid_key, parameter, value, native_unit, unit, conversion_code, value_status, valid_at, temporal_support, interval_status and period bounds. Mappings carry plot identity and example distance. SQL checks envelope field presence, lease, purpose/licence, 64-hex hashes and grid/value/mapping counts; this is not a universal JSON Schema.\n\n',lang)
   elif cid=='C07':
    s+=table(['Field','Type / required','Mapping'],[[f,t,m] for f,t,m in [('schema_version','constant a3-source-1','internal'),('plot','object','seagis.plot'),('start_at,end_at','timestamptz / required','query bounds'),('sensors','array','seagis.sensor'),('parameters','array','dataset_parameter + dataset + environment.policy'),('mappings','array','plot_grid_mapping + demo_grid_mapping + source_grid'),('records','array','observation + forecast_value + quality_event'),('source_sha256','64-hex string','seagis.jsonb_sha256(bundle)')]])
   elif cid=='C08':
    s+=T('Manifest export_version=experiment-csv-2; capture/export time, rentang, unit, jumlah record unik, jumlah CSV dan checksum per file. Suhu CSV membawa timestamp_utc, timestamp_wib, plot_id, value, raw_value, gap/synthetic/QC, observation_id, available_at_utc, training_authorized=false, parameter_code, unit, source_kind dan value_policy. CSV regional membawa field record sumber datar, cadence, attribution, licence_url, selection_basis dan capture_at_utc. Field sumber dinamis berarti schema CSV mengikuti record bundle, bukan kontrak kolom tetap universal.\n\n','Manifest export_version=experiment-csv-2 records capture/export times, bounds, units, unique record counts, CSV counts and per-file checksums. Temperature CSV carries timestamp_utc, timestamp_wib, plot_id, value, raw_value, gap/synthetic/QC fields, observation_id, available_at_utc, training_authorized=false, parameter_code, unit, source_kind and value_policy. Regional CSV carries flattened source-record fields, cadence, attribution, licence_url, selection_basis and capture_at_utc. Dynamic source fields mean the CSV schema follows bundle records rather than a universal fixed column contract.\n\n',lang)
   elif cid=='C09':
    s+=table(['Swift field','Type','Required','Meaning / mapping'],[[f,t,True,MEAN.get(f,(T('Field domain demo; bukan DTO backend','Demo domain field; not a backend DTO',lang),)*2)[lang=='en']] for f,t in [('id','String'),('plotID','String'),('title','String'),('summary','String'),('provenance','AssessmentProvenance.syntheticFixture'),('evidenceIDs','[String]')]])
   elif cid=='C10':
    s+=T('Respons harus list sepanjang dua plot, setiap item memiliki latitude/longitude/elevation, timezone UTC/GMT, utc_offset_seconds=0, hourly_units.time=iso8601 dan array hourly sejajar. Field variabel dan unit ditetapkan config a2_sources.json. generationtime_ms tidak dipakai sebagai issue time. Null/angka mengikuti normalisasi common.point. Tidak ada response_error provider yang diklaim stabil.\n\n','Response must be a list matching the two plots, each item carrying latitude/longitude/elevation, timezone UTC/GMT, utc_offset_seconds=0, hourly_units.time=iso8601 and aligned hourly arrays. Variable fields and units come from a2_sources.json. generationtime_ms is not issue time. Null/numeric handling follows common.point. No stable provider response_error format is claimed.\n\n',lang)
   elif cid=='C11':
    s+=T('STAC memerlukan id, collection/product, cube:dimensions time/elevation/latitude/longitude dan cube:variables unit/standardName. Dataset xarray memiliki satu latitude/longitude/depth dan time unik berurutan sesuai cadence; variabel di-transpose time,depth,latitude,longitude. Logical subset berisi cell,time,variables,native_units, bukan wire format provider. Metadata asli yang tidak diketahui tidak diciptakan.\n\n','STAC requires id, collection/product, cube:dimensions time/elevation/latitude/longitude and cube:variables unit/standardName. The xarray dataset has one latitude/longitude/depth and unique ordered times at native cadence; variables are transposed time,depth,latitude,longitude. The logical subset contains cell,time,variables,native_units and is not a provider wire format. Unknown original metadata is not fabricated.\n\n',lang)
 s+='### '+T('Rute HTTP dan respons','HTTP routes and responses',lang)+'\n\n'
 s+=table(['Method','Path (temperature base)','Auth','Result / errors'],[
 ['GET','/health','none','200 service=seagis-temperature, version=1.0.0'],
 ['POST','/v1/ingest','device Bearer','201 stored; 200 duplicate; 409 packet_conflict; 422 invalid_packet; 403 sensor_forbidden/sensor_inactive; 503 commissioning_disabled'],
 ['GET','/v1/plots/{plot_id}/temperature','reader Bearer + reader_plot','200 observations/coverage; 400 invalid_query/invalid_plot_id; 403 plot_forbidden'],
 ['GET','/v1/status','reader Bearer','200 checked_at,stale_after_seconds,plots[]'],
 ['all','known protected paths','Bearer sgi_ pattern','401 unauthorized; 429 rate_limited'],
 ['all','HTTP boundary','handler','404 not_found; 405 method_not_allowed; 415 json_required; 413 payload_too_large; 400 invalid_json/empty_body/unexpected_query; 503 temporarily_unavailable']])
 s+=T('Base deployment /functions/v1/temperature; handler juga menerima prefix /temperature. Semua respons no-store. Retry-After 60 untuk 429 dan 5 untuk 503. plots[] status berisi plot_id,plot_code,is_synthetic,latest_usable_observed_at,last_ingested_at,age_seconds,stale,observations_last_24h,rejected_last_24h. Waktu last_ingested_at tidak harus milik record latest_usable_observed_at. Null waktu/umur berarti belum tersedia.','Deployment base /functions/v1/temperature; the handler also accepts a /temperature prefix. Responses use no-store. Retry-After is 60 for 429 and 5 for 503. Status plots[] contains plot_id,plot_code,is_synthetic,latest_usable_observed_at,last_ingested_at,age_seconds,stale,observations_last_24h,rejected_last_24h. last_ingested_at need not belong to the latest_usable_observed_at record. Null time/age means unavailable.',lang)+'\n\n'
 s+='### '+T('Payload dan error A1','A1 payloads and errors',lang)+'\n\n'
 packet={'schema_version':'1.0.0','sensor_id':'00000000-0000-4000-8000-000000000101','boot_id':'synthetic-boot-a','sequence':1,'observed_at':'2026-10-21T12:00:00Z','water_temperature':29.2,'unit':'degC','value_status':'present'}
 s+=T('Contoh sintetis valid secara bentuk; penyimpanan memerlukan credential/sensor terdaftar dan policy aktif.','Synthetic structurally valid example; persistence requires a registered credential/sensor and active policy.',lang)+code(json.dumps(packet,indent=2),'json')
 s+=T('Contoh tidak valid: ubah unit menjadi kelvin. SQL mengembalikan 422 invalid_packet setelah autentikasi lolos.','Invalid example: change unit to kelvin. SQL returns 422 invalid_packet after successful authentication.',lang)+code(json.dumps({'code':'invalid_packet','request_id':'00000000-0000-4000-8000-000000000999'},indent=2),'json')
 s+=T('Respons stored memiliki observation_id, ingestion_run_id, observed_at, quality_status, flags, is_synthetic, code dan request_id. UUID dan waktu di bawah ilustratif, bukan response live.','A stored response has observation_id, ingestion_run_id, observed_at, quality_status, flags, is_synthetic, code and request_id. UUIDs/times below are illustrative, not a live response.',lang)+code(json.dumps({'observation_id':'00000000-0000-4000-8000-000000000201','ingestion_run_id':'00000000-0000-4000-8000-000000000301','observed_at':'2026-10-21T12:00:00.000000Z','quality_status':'accepted','flags':[],'is_synthetic':True,'code':'stored','request_id':'00000000-0000-4000-8000-000000000999'},indent=2),'json')
 s+=table(['Boundary','Rule / discrepancy','Classification','Evidence'],[
 ['A0 vs A1 packet',T('A0 fixture memakai envelope 0.1.0 dan detection_limit; A1 tepat delapan field schema 1.0.0, tidak menerima field tambahan.','A0 fixture uses a 0.1.0 envelope and detection_limit; A1 accepts exactly eight 1.0.0 fields and rejects extras.',lang),'VERIFIED',evidence('contracts/iot-packet.schema.json')],
 ['A0 run_kind vs A2',T('0003 memperluas run_kind dengan analysis_forecast_unspecified; jangan memakai daftar A0 lama.','0003 extends run_kind with analysis_forecast_unspecified; do not rely on the old A0 list.',lang),'VERIFIED',evidence('supabase/migrations/0003_environment_ingestion.sql')],
 ['A3 JSON schema vs runtime',T('Schema lengkap diuji oleh test; curate/build tidak memanggil JSON Schema umum, SQL menegakkan pemeriksaan terpilih.','Tests validate the full schema; curate/build does not call a general JSON Schema validator and SQL enforces selected checks.',lang),'VERIFIED',evidence('scripts/curate_environment.py')],
 ['API time vs PostgreSQL','A1 UTC Z; timestamptz session display / microseconds','VERIFIED',evidence('supabase/migrations/0002_temperature_api.sql')],
 ['iOS Assessment vs DB',T('Tidak ada DTO/kontrak assessment backend terverifikasi.','No verified backend assessment DTO/contract.',lang),'NOT FOUND',evidence('Seagis/Seagis/Models/Shared/Assessment.swift')]])
 return s

def section_audit(lang):
 s=T('Audit read-only terhadap kode dan snapshot lama; severity menyatakan dampak potensial sesuai lingkup prototype, bukan insiden produksi terukur. Tidak ada perubahan schema/aplikasi yang diterapkan.\n\n','Read-only audit of code and historical metadata; severity expresses potential impact within the prototype scope, not a measured production incident. No application/schema changes were applied.\n\n',lang)
 for fid,severity,cat,title,desc,paths,rec,status in FINDINGS:
  s+='### '+fid+' '+title[lang=='en']+'\n\n'
  s+=table([T('Atribut','Attribute',lang),T('Temuan','Finding',lang)],[['Severity / category',severity+' / '+cat],['Status',status],[T('Deskripsi / dampak','Description / impact',lang),desc[lang=='en']],['Affected',', '.join(paths) or 'runtime catalog'],['Evidence','; '.join(evidence(p) for p in paths) or 'schema-metadata-20261022.json inspected_at'],[T('Rekomendasi','Recommendation',lang),rec[lang=='en']]])
 s+=T('Prioritas: P1 sepakati integrasi/kontrak dan cegah leakage (F01/F06); P2 tutup trust, retensi, mapping lifecycle dan raw reproducibility (F02–F05); P3 perbarui status dokumentasi dan catalog (F07/F08). Evaluasi indeks/performa membutuhkan EXPLAIN dan beban nyata: tidak ada klaim missing index atau query lambat yang dibuktikan hanya dari nama kolom.\n\n','Priority: P1 agree integration/contracts and prevent leakage (F01/F06); P2 address trust, retention, mapping lifecycle and raw reproducibility (F02–F05); P3 refresh documentation status/catalog (F07/F08). Index/performance evaluation needs EXPLAIN and actual workloads: no missing-index or slow-query claim is established merely from column names.\n\n',lang)
 return s

def glossary(lang):
 items=[('Origin', 'Asal data: sensor, model regional atau nilai turunan','Data origin: sensor, regional model or derived value'),('Ingestion','Penerimaan dan persistence satu capture','Receipt and persistence of one capture'),('Vintage','Versi capture model yang dipertahankan','Preserved model capture version'),('Native cadence','Interval sampel asli, berbeda dari tick scheduler','Original sample interval, distinct from scheduler tick'),('Availability cutoff','Batas informasi yang sudah tersedia saat keputusan','Boundary of information available at decision time'),('Value status','Ketersediaan angka, bukan status penyakit','Numeric availability, not disease state'),('QC','Pemeriksaan kualitas data; bukan diagnosis','Data quality checks; not diagnosis'),('Idempotency','Retry identik tidak menambah measurement','Identical retry does not add a measurement'),('Lineage','Jejak referensi dari hasil ke sumber','Reference trail from output to source'),('Manifest','Daftar input/berkas dengan identitas dan digest','Input/file list with identities and digests'),('RLS','Row Level Security; efektivitas tergantung role dan grants','Row Level Security; effect depends on roles and grants'),('FK','Foreign key: integritas referensi antarbaris','Foreign key: referential integrity between rows'),('NULL','Nilai tidak tersedia; tidak sama dengan angka nol','Unavailable value; distinct from numeric zero'),('Metadata-only','Menyimpan provenance/digest tanpa konten raw','Provenance/digest retention without raw content'),('Sealed snapshot','Snapshot yang tidak boleh diubah setelah sealing','Snapshot that cannot be mutated after sealing'),('Ice-ice','Konteks penyakit budidaya; dokumentasi ini tidak memvalidasi prediksinya','Cultivation disease context; this documentation does not validate its prediction')]
 return table(['Term',T('Definisi','Definition',lang)],[[x[0],x[1 if lang=='id' else 2]] for x in items])


CSV_INVENTORY=[]
import csv
for csvpath in sorted((BACK/'data').rglob('*.csv')):
 with csvpath.open(newline='') as stream:
  reader=csv.reader(stream);headers=next(reader,[]);count=sum(1 for _ in reader)
 CSV_INVENTORY.append({'path':'Seagis-Model/'+str(csvpath.relative_to(BACK)),'columns':headers,'rows':count,'sha256':sha(csvpath.read_bytes())})
(OUT/'assets/generated/local-dataset-inventory.json').write_text(json.dumps(CSV_INVENTORY,indent=2)+'\n')

def appendix(lang):
 s='### 13.1 '+T('Basis bukti dan batas audit','Evidence base and audit boundaries',lang)+'\n\n'
 s+=table(['Repository','Commit','Path'],[[k,v,str(roots[k])] for k,v in commits.items()])
 s+=T('File implementasi dibaca melalui pembangkit dokumentasi dan pencarian terarah; manifest mencatat hash per file. Tidak ada source eksternal yang digunakan untuk menggantikan implementasi. Tidak ada migrasi, worker ingestion, test yang menulis database atau deploy dijalankan. Test kontrak murni/offline dilaporkan terpisah pada validation.json. File .env, credential dan isi tabel tidak disalin.\n\n','Implementation files were read through the documentation generator and targeted searches; the manifest records per-file hashes. No external source substitutes for implementation. No migrations, ingestion workers, database-writing tests or deployment were run. Pure/offline contract tests are reported separately in validation.json. Environment files, credentials and table contents were not copied.\n\n',lang)
 s+='### 13.2 '+T('Cakupan terukur','Measured coverage',lang)+'\n\n'
 unmapped=[fullname(o)+'.'+c['name'] for o in META['objects'] for c in cols(o) if origin(o,c)[2]!='VERIFIED']
 num_fields=sum(len(schema_fields(json.loads((BACK/'contracts'/n).read_text()))) for n in ['source.schema.json','normalized.schema.json','iot-packet.schema.json','alignment.schema.json'])
 s+=table(['Component','Discovered','ID documented','EN documented','Evidence / gaps'],[
 ['Application databases',1,1,1,T('Kode + catalog lama; runtime terkini belum','Code + historical catalog; current runtime unresolved',lang)],['Application schemas',6,6,6,'historical catalog + migrations'],['Physical tables',28,28,28,'row counts UNVERIFIED'],['Views',1,1,1,'current_speed'],['Columns (tables + view)',268,268,268,T('259 tabel + 9 view; arti field tertentu masih terbatas','259 table + 9 view fields; some meanings remain limited',lang)],['Physical FK',len(FKS),len(FKS),len(FKS),'historical catalog + SQL'],['Column-origin mappings',268,268,268,f'{268-len(unmapped)} VERIFIED; {len(unmapped)} UNVERIFIED'],['Pipeline paths',4,4,4,'A1, A2, A3, CSV export'],['Boundary contracts',len(CONTRACTS),len(CONTRACTS),len(CONTRACTS),'4 explicit; 7 implementation-derived'],['JSON-schema field/structure entries',num_fields,num_fields,num_fields,T('Nested semantics belum semua ditutup; schema lengkap disertakan','Not all nested semantics resolved; full schemas included',lang)],['Object dependency rows',29,29,29,'writers/readers from code; deployment unverified'],['Runtime rows/grants/backups','UNVERIFIED','UNVERIFIED','UNVERIFIED',T('Tidak ada akses live pada audit ini','No live access in this audit',lang)]])
 s+=T('Cakupan inventaris snapshot 29/29 objek dan 268/268 kolom bukan klaim 100% arsitektur produksi. Schema internal, sumber di luar tiga checkout, deployment runtime dan nested field ambigu tidak menjadi denominator yang diketahui.\n\n','Coverage of 29/29 snapshot objects and 268/268 columns is not a claim of 100% production-architecture coverage. Internal schemas, sources outside the three checkouts, runtime deployment and ambiguous nested fields have no known complete denominator.\n\n',lang)
 if unmapped:s+=T('Asal kolom belum terverifikasi penuh: ','Column origins not fully verified: ',lang)+', '.join('`'+n+'`' for n in unmapped)+'.\n\n'
 s+='### 13.2.1 '+T('Dataset file lokal teramati','Observed local file datasets',lang)+'\n\n'
 s+=T('Metadata CSV berikut diperiksa tanpa menyalin nilai baris. Jumlah ini milik file capture lokal, bukan row count database. CSV regional mengikuti native cadence dan latest_available_at_capture; suhu plot adalah sintetis. source_bundles/alignment/manifest JSON merupakan keluaran exporter atau curator dengan kontrak C04/C07/C08; worker.log hanya log operasional dan CA certificate hanya trust material, bukan dataset lingkungan.','CSV metadata below was inspected without copying row values. Counts belong to local capture files, not database tables. Regional CSV retains native cadence and latest_available_at_capture; plot temperatures are synthetic. source_bundles/alignment/manifest JSON are exporter/curator outputs under C04/C07/C08; worker.log is operational logging and the CA certificate is trust material, not an environmental dataset.',lang)+'\n\n'
 s+=table(['File','Rows observed','Columns / contract'],[[x['path'],x['rows'],', '.join(x['columns'])] for x in CSV_INVENTORY])
 s+='### 13.3 '+T('Pertanyaan terbuka','Open questions',lang)+'\n\n'
 for i,e in [('Apakah schema cloud dan grants berubah sejak 22 Oktober?','Have cloud schemas and grants changed since 22 October?'),('Bagaimana supersession pemetaan immutable dan penyelesaian overlap ditetapkan?','How are immutable mapping supersession and overlap resolution defined?'),('Siapa pemilik operasi backup/retensi dan bagaimana restore dibuktikan?','Who owns backup/retention operations and how is restore verified?'),('Kontrak assessment apa yang akan disetujui lintas backend/iOS?','Which assessment contract will backend/iOS approve?'),('Kapan plot/lokasi/kedalaman sensor nyata tervalidasi dan training gate dapat dievaluasi?','When will real plots/locations/sensor depths be validated and the training gate evaluated?')]:s+='- '+T(i,e,lang)+'\n'
 s+='\n### 13.4 '+T('SQL read-only ilustratif','Illustrative read-only SQL',lang)+'\n\n'
 s+=T('Query berikut belum dijalankan terhadap cloud dalam audit ini.','The following query was not executed against the cloud in this audit.',lang)+code("BEGIN READ ONLY;\nSELECT schemaname, tablename FROM pg_catalog.pg_tables\nWHERE schemaname IN ('seagis','seagis_raw','seagis_api',\n 'seagis_environment','seagis_quality','seagis_features')\nORDER BY schemaname, tablename;\nROLLBACK;")
 s+='### 13.5 '+T('Registry fungsi SQL','SQL function registry',lang)+'\n\n'
 funcs=[]
 for key,v in sources.items():
  if '/migrations/' not in key:continue
  for m in re.finditer(r'CREATE (?:OR REPLACE )?FUNCTION ([\w.]+)\(([^)]*)\)',v['text']):funcs.append([m[1],re.sub(r'\s+',' ',m[2]),f'`{key}:{v["text"][:m.start()].count(chr(10))+1}`'])
 s+=table(['Function','Arguments','Evidence'],funcs)
 s+='### 13.6 '+T('Register sumber','Source register',lang)+'\n\n'
 # Include all inspected source references in both consolidated files.
 s+=table(['Path','Lines','SHA-256'],[[p['path'],p['lines'],p['sha256']] for p in source_manifest])
 s+=T('Salinan migrasi dan empat kontrak tersedia di assets/evidence. source-manifest.json, coverage.json dan validation.json berada di assets/generated. File pembangkit dokumentasi dan PDF disertakan agar hasil dapat direproduksi.\n\n','Migration copies and four contracts are in assets/evidence. source-manifest.json, coverage.json and validation.json are in assets/generated. Documentation/PDF generators are included for reproduction.\n\n',lang)
 return s

TITLES_ID=['Ringkasan Eksekutif','Gambaran Arsitektur Sistem dan Data','Inventaris Database dan Skema','Kamus Data Lengkap','Hubungan Antarentitas','Sumber dan Asal-Usul Data','Ingesti dan Transformasi Data','Kontrak Data','Siklus Hidup Data','Dependensi Data pada Aplikasi','Audit Kualitas Data dan Arsitektur','Glosarium','Lampiran']
TITLES_EN=['Executive Summary','System and Data Architecture Overview','Database and Schema Inventory','Complete Data Dictionary','Entity Relationships','Data Sources and Lineage','Data Ingestion and Transformation','Data Contracts','Data Lifecycle','Application Data Dependencies','Data Quality and Architecture Audit','Glossary','Appendices']
MODS_ID=['schemas/INVENTARIS_DATABASE.md','schemas/KAMUS_DATA.md','schemas/RELASI_ENTITAS.md','pipelines/ALUR_ASAL_DATA.md','pipelines/PIPELINE_INGESTI.md','pipelines/PEMETAAN_SUMBER_TUJUAN.md','contracts/KONTRAK_DATA.md','architecture/ERD.md','architecture/ALIRAN_DATA.md','architecture/SIKLUS_HIDUP_DATA.md','architecture/DEPENDENSI_DATA.md','audit/AUDIT_KUALITAS_DATA.md']
MODS_EN=['schemas/DATABASE_INVENTORY.md','schemas/DATA_DICTIONARY.md','schemas/ENTITY_RELATIONSHIPS.md','pipelines/DATA_LINEAGE.md','pipelines/INGESTION_PIPELINES.md','pipelines/SOURCE_TO_TARGET_MAPPING.md','contracts/DATA_CONTRACTS.md','architecture/ERD.md','architecture/DATA_FLOW.md','architecture/DATA_LIFECYCLE.md','architecture/DATA_DEPENDENCIES.md','audit/DATA_QUALITY_AUDIT.md']

def evidence_refs(text,lang):
 return T('Bukti implementasi utama: ','Main implementation evidence: ',lang)+'; '.join(evidence(p) for p in text)+'.\n\n'
for lang in ['id','en']:
 titles=TITLES_ID if lang=='id' else TITLES_EN;mods=MODS_ID if lang=='id' else MODS_EN
 refs=evidence_refs(['supabase/migrations/0001_initial_schema.sql','supabase/migrations/0002_temperature_api.sql','supabase/migrations/0003_environment_ingestion.sql','supabase/migrations/0004_provider_update_status.sql','supabase/migrations/0005_quality_alignment.sql'],lang)
 inv=section_inventory(lang); dictionary=section_dictionary(lang); relations=section_relations(lang);mapping=section_mapping(lang);contracts=section_contracts(lang);audit=section_audit(lang)
 er=T('ERD lengkap memuat seluruh kolom tabel fisik; PK/FK/UK mempertahankan nama fisik. FK1–FK47 dijelaskan pada Bab 5. Nama node menggunakan underscore hanya untuk sintaks Mermaid; label menyimpan schema.table. View current_speed didokumentasikan terpisah karena tidak memiliki FK fisik.\n\n','The complete ERD contains every physical-table column; PK/FK/UK retain physical names. FK1–FK47 are explained in Chapter 5. Node IDs use underscores for Mermaid syntax only; labels retain schema.table. current_speed is documented separately because it has no physical FKs.\n\n',lang)+code(erd(),'mermaid')
 for sc in META['schemas']:er+='### '+sc['name']+'\n\n'+code(erd(sc['name']),'mermaid')
 lineage=TEXT['lineage'][lang=='en']+'\n\n'+evidence_refs(['supabase/functions/temperature/handler.ts','scripts/environmental/copernicus.py','scripts/environmental/open_meteo.py','scripts/quality/alignment.py','scripts/export_experiment_csv.py'],lang)+diagram('lineage',lang)
 ingestion=TEXT['ingest'][lang=='en']+'\n\n'+refs+evidence_refs(['scripts/ingest_environment.py','scripts/environmental/common.py','scripts/install_a2_scheduler.py','scripts/run_a2_worker.py','scripts/curate_environment.py'],lang)+''.join(diagram(n,lang) for n in ['a1','a2','a3'])
 # explicit source fields, cadence and units
 config=json.loads((BACK/'config/a2_sources.json').read_text())
 source_rows=[['sensor_temperature_v1','device/simulator','water_temperature','degC','degC',3600,'instantaneous','seagis.observation.value']]
 for key,prof in config['datasets'].items():
  for var,spec in prof['variables'].items():source_rows.append([key,prof['provider'],var,spec[1],spec[2],prof['cadence_seconds'],spec[4],'seagis.forecast_value.value ('+spec[0]+')'])
 lineage+=table(['Dataset','Owner / source','Field','Native unit','Unit','Cadence s','Support','Target'],source_rows)+T('Sensor cadence 3600 berasal dari seed kontrak pilot, bukan bukti setiap perangkat selalu mengirim tepat waktu. Keandalan provider tidak diukur ulang; adapter memiliki retry/validasi tetapi tidak menjamin SLA.','The 3600-second sensor cadence comes from the pilot seed contract, not proof that every device always transmits on time. Provider reliability was not remeasured; retries/validation do not guarantee an SLA.',lang)+'\n\n'+evidence_refs(['supabase/seed.sql','config/a2_sources.json'],lang)
 lifecycle=TEXT['lifecycle'][lang=='en']+'\n\n'+refs+evidence_refs(['scripts/environmental/store.py','scripts/quality/store.py','supabase/functions/temperature/connection.ts'],lang)
 deps=TEXT['depend'][lang=='en']+'\n\n'+evidence_refs(['Seagis/Seagis/Repositories/Shared/MockAssessmentRepository.swift','AppPOC/POCApp/Shared/Data/FarmStore.swift','supabase/migrations/0002_temperature_api.sql','supabase/migrations/0003_environment_ingestion.sql'],lang)+diagram('dependencies',lang)
 deps+=table(['Data entity','Producer / writers','Readers','API / feature','Downstream'],[[fullname(o),ownership(o)[0],ownership(o)[1],('temperature history/status' if o['name']=='observation' else 'private SQL / demo / offline'),PURPOSE[fullname(o)][lang=='en']] for o in META['objects']])
 parts=[TEXT['summary'][lang=='en']+'\n\n'+refs,TEXT['architecture'][lang=='en']+'\n\n'+refs+diagram('architecture',lang),inv,dictionary,relations+er,lineage,ingestion+'### 7.1 '+T('Pemetaan Sumber–Tujuan','Source-to-Target Mapping',lang)+'\n\n'+mapping,contracts,lifecycle,deps,audit,glossary(lang),appendix(lang)]
 title=T('Dokumentasi Arsitektur Database, Lineage dan Kontrak Data SEAGIS','SEAGIS Database Architecture, Data Lineage and Data Contracts',lang)
 header=f'# {title}\n\nVersion: {VERSION} | Date: {DATE} (Asia/Jakarta) | Catalog snapshot: {snapshot}\n\n'+T('Status: audit kode dan snapshot historis; runtime terkini UNVERIFIED.','Status: code and historical-snapshot audit; current runtime UNVERIFIED.',lang)+'\n\n'
 header+=table(['Label',T('Makna','Meaning',lang)],[['VERIFIED',T('Didukung kode/inspeksi; tidak otomatis diuji runtime','Supported by code/inspection; not automatically runtime-tested',lang)],['INFERRED',T('Interpretasi masuk akal, tidak eksplisit','Reasonable interpretation, not explicit',lang)],['UNVERIFIED',T('Belum dapat dibuktikan dengan akses tersedia','Not established with available access',lang)],['NOT FOUND',T('Dicari pada lingkup yang disebut, tidak ditemukan','Searched within the stated scope, not found',lang)],['NOT APPLICABLE',T('Tidak relevan untuk komponen','Does not apply to component',lang)]])
 header+='## '+T('Daftar Isi','Table of Contents',lang)+'\n\n'
 for i,t in enumerate(titles,1):
  anchor=re.sub(r'[^\w -]','',f'{i} {t}'.lower()).replace(' ','-');header+=f'{i}. [{t}](#{anchor})\n'
 header+='\n'
 master=header+''.join(f'## {i} {t}\n\n'+p+'\n' for i,(t,p) in enumerate(zip(titles,parts),1))
 mastername='DOKUMENTASI_DATABASE.md' if lang=='id' else 'DATABASE_DOCUMENTATION.md'
 (OUT/lang/mastername).write_text(master)
 module_content=[inv,dictionary,relations,lineage,ingestion,mapping,contracts,er,TEXT['architecture'][lang=='en']+'\n\n'+diagram('architecture',lang)+diagram('lineage',lang),lifecycle,deps,audit]
 for path,content in zip(mods,module_content):
  relmaster='../../'+mastername # corrected below: module directory to master is one parent
  intro=f'# {Path(path).stem}\n\nVersion: {VERSION} | Date: {DATE}\n\n'+f'[{T("Dokumen lengkap","Complete document",lang)}](../{mastername}) | [README](../../README.md)\n\n'
  (OUT/lang/path).write_text(intro+content)
readme='''# SEAGIS — Database documentation / Dokumentasi database

Version: 1.0.0 | 2026-10-27 (Asia/Jakarta)

Audit kode lokal dan snapshot catalog 2026-10-22; bukan audit runtime terkini. / Local code and 2026-10-22 catalog audit; not a current runtime audit.

| Bahasa / Language | Markdown lengkap / Complete Markdown | PDF |
| --- | --- | --- |
| Bahasa Indonesia | [Dokumentasi lengkap](id/DOKUMENTASI_DATABASE.md) | [PDF Indonesia](id/DOKUMENTASI_DATABASE.pdf) |
| English | [Complete documentation](en/DATABASE_DOCUMENTATION.md) | [English PDF](en/DATABASE_DOCUMENTATION.pdf) |

## Modul / Modules

'''
readme+=table(['ID','EN'],[[f'[{Path(i).stem}](id/{i})',f'[{Path(e).stem}](en/{e})'] for i,e in zip(MODS_ID,MODS_EN)])
readme+='''## Evidence & reproduction / Bukti dan reproduksi

- [Source manifest](assets/generated/source-manifest.json): commit, paths and SHA-256; no credentials or table records.
- [Coverage](assets/generated/coverage.json) and [validation](assets/generated/validation.json).
- [Catalog snapshot](assets/evidence/schema-metadata-20261022.json); not a fresh live inspection.
- Mermaid source and deterministic vector renderings: `assets/diagrams/`.
- Rebuild documentation: `python3 assets/generated/build_docs.py`; set `SEAGIS_DOC_OUTPUT` to a new output directory if needed. Local source checkouts and catalog snapshot are required at the paths recorded in the script.
- Rebuild PDFs: `python3 assets/generated/render_pdf.py /path/to/docs/database`. Requires ReportLab and pypdf; Poppler is used for layout inspection.

Do not run migrations, provisioning or ingestion to reproduce documentation. No application code, database schema or production records were changed. Full runtime architecture completeness remains unverified. / Jangan menjalankan migrasi, provisioning atau ingestion untuk membangun ulang dokumentasi. Kode aplikasi, schema dan record produksi tidak diubah. Kelengkapan arsitektur runtime belum terverifikasi.
'''
(OUT/'README.md').write_text(readme)
coverage={'date':DATE,'snapshot':snapshot,'databases':1,'schemas':6,'tables':28,'views':1,'columns':268,'table_columns':259,'view_columns':9,'physical_relationships':len(FKS),'pipeline_paths':4,'contracts':len(CONTRACTS),'dependencies':29,'field_origins_verified':sum(origin(o,c)[2]=='VERIFIED' for o in META['objects'] for c in cols(o)),'field_origins_unverified':[fullname(o)+'.'+c['name'] for o in META['objects'] for c in cols(o) if origin(o,c)[2]!='VERIFIED'],'full_runtime_coverage':'UNVERIFIED'}
(OUT/'assets/generated/coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
print(json.dumps(coverage,indent=2))
