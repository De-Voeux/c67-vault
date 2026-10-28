-- A1: private IoT API. Gateway can execute three routines, never access tables.
CREATE SCHEMA seagis_api;
REVOKE ALL ON SCHEMA seagis_api FROM PUBLIC, anon, authenticated, service_role;
DO $$ BEGIN
  IF EXISTS (SELECT FROM pg_roles WHERE rolname='seagis_iot_gateway') THEN
    RAISE EXCEPTION 'Role seagis_iot_gateway already exists; review ownership before migrating';
  END IF;
  CREATE ROLE seagis_iot_gateway NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOBYPASSRLS;
END $$;
GRANT USAGE ON SCHEMA seagis_api TO seagis_iot_gateway;
ALTER DEFAULT PRIVILEGES IN SCHEMA seagis_api REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;

-- A1 hashes retained synthetic JSON using PostgreSQL UTF-8 jsonb serialization.
-- Keep A0 fixture hashing unchanged; neither basis claims byte-for-byte wire retention.
DO $$ DECLARE c record; BEGIN
  FOR c IN SELECT conname FROM pg_constraint
    WHERE conrelid='seagis_raw.raw_payload'::regclass AND contype='c'
      AND pg_get_constraintdef(oid) LIKE '%hash_basis%' LOOP
    EXECUTE format('ALTER TABLE seagis_raw.raw_payload DROP CONSTRAINT %I', c.conname);
  END LOOP;
END $$;
ALTER TABLE seagis_raw.raw_payload ADD CONSTRAINT raw_payload_hash_basis_v2
 CHECK (hash_basis IN ('source_bytes','synthetic_json_canonical_v1','jsonb_utf8_v1'));
ALTER TABLE seagis_raw.raw_payload ADD CONSTRAINT raw_payload_inline_synthetic_v2
 CHECK (storage_mode<>'inline' OR (is_synthetic AND hash_basis IN ('synthetic_json_canonical_v1','jsonb_utf8_v1')));

CREATE TABLE seagis_api.credential (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 label text NOT NULL,
 token_sha256 text NOT NULL UNIQUE CHECK (token_sha256 ~ '^[0-9a-f]{64}$'),
 kind text NOT NULL CHECK (kind IN ('device','reader')),
 sensor_id uuid REFERENCES seagis.sensor,
 created_at timestamptz NOT NULL DEFAULT now(),
 expires_at timestamptz NOT NULL,
 revoked_at timestamptz,
 CHECK ((kind='device')=(sensor_id IS NOT NULL)),
 CHECK (expires_at>created_at)
);
CREATE TABLE seagis_api.reader_plot (
 credential_id uuid NOT NULL REFERENCES seagis_api.credential,
 plot_id uuid NOT NULL REFERENCES seagis.plot,
 PRIMARY KEY (credential_id,plot_id)
);
CREATE TABLE seagis_api.request_event (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 credential_id uuid NOT NULL REFERENCES seagis_api.credential,
 sensor_id uuid REFERENCES seagis.sensor,
 http_status integer NOT NULL,
 code text NOT NULL,
 created_at timestamptz NOT NULL DEFAULT clock_timestamp()
);
CREATE INDEX request_event_actor_time ON seagis_api.request_event (credential_id,created_at DESC);
CREATE TABLE seagis_api.packet_receipt (
 sensor_id uuid NOT NULL REFERENCES seagis.sensor,
 source_record_key text NOT NULL,
 semantic_sha256 text NOT NULL CHECK (semantic_sha256 ~ '^[0-9a-f]{64}$'),
 observation_id uuid NOT NULL UNIQUE REFERENCES seagis.observation,
 ingestion_run_id uuid NOT NULL REFERENCES seagis.ingestion_run,
 flags text[] NOT NULL,
 PRIMARY KEY (sensor_id,source_record_key)
);
CREATE TRIGGER receipt_append_only BEFORE UPDATE OR DELETE ON seagis_api.packet_receipt
 FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();
CREATE TRIGGER request_event_append_only BEFORE UPDATE OR DELETE ON seagis_api.request_event
 FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();

CREATE TABLE seagis_api.temperature_policy (
 id boolean PRIMARY KEY DEFAULT true CHECK (id),
 version text NOT NULL,
 min_degc double precision NOT NULL,
 max_degc double precision NOT NULL,
 max_step_degc double precision NOT NULL,
 future_tolerance_seconds integer NOT NULL,
 stale_after_seconds integer NOT NULL,
 requests_per_minute integer NOT NULL,
 CHECK (min_degc<max_degc AND max_step_degc>0 AND future_tolerance_seconds>0
   AND stale_after_seconds>0 AND requests_per_minute>0)
);
-- Provisional engineering QC, not biological thresholds or device specifications.
INSERT INTO seagis_api.temperature_policy VALUES (true,'pilot-qc-1',-5,60,3,300,7200,120);
DO $$ DECLARE t record; BEGIN
 FOR t IN SELECT tablename FROM pg_tables WHERE schemaname='seagis_api' LOOP
  EXECUTE format('ALTER TABLE seagis_api.%I ENABLE ROW LEVEL SECURITY',t.tablename);
  EXECUTE format('REVOKE ALL ON seagis_api.%I FROM PUBLIC,anon,authenticated,service_role,seagis_iot_gateway',t.tablename);
 END LOOP;
END $$;

CREATE FUNCTION seagis_api.utc(t timestamptz) RETURNS text LANGUAGE sql IMMUTABLE
 SET search_path=pg_catalog AS $$ SELECT to_char(t AT TIME ZONE 'UTC','YYYY-MM-DD"T"HH24:MI:SS.US"Z"') $$;
CREATE FUNCTION seagis_api.actor(token text, actor_kind text) RETURNS seagis_api.credential
 LANGUAGE sql STABLE SECURITY DEFINER SET search_path=pg_catalog AS $$
 SELECT c FROM seagis_api.credential c WHERE length(token) BETWEEN 32 AND 256
 AND c.token_sha256=encode(sha256(convert_to(token,'UTF8')),'hex')
 AND c.kind=actor_kind AND c.revoked_at IS NULL AND c.expires_at>now()
$$;
CREATE FUNCTION seagis_api.reply(actor_id uuid, status integer, code text, body jsonb DEFAULT '{}', sensor uuid DEFAULT NULL)
 RETURNS jsonb LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE request_id uuid:=gen_random_uuid(); BEGIN
 IF actor_id IS NOT NULL AND status<>429 THEN
  INSERT INTO seagis_api.request_event(id,credential_id,sensor_id,http_status,code)
   VALUES(request_id,actor_id,sensor,status,code);
 END IF;
 RETURN jsonb_build_object('http_status',status,'body',body||jsonb_build_object('code',code,'request_id',request_id));
END $$;
CREATE FUNCTION seagis_api.rate_ok(actor_id uuid) RETURNS boolean LANGUAGE plpgsql SECURITY DEFINER
 SET search_path=pg_catalog AS $$ BEGIN
 PERFORM pg_advisory_xact_lock(hashtextextended('actor:'||actor_id,0));
 RETURN (SELECT count(*) FROM seagis_api.request_event WHERE credential_id=actor_id
 AND created_at>clock_timestamp()-interval '1 minute') <
 (SELECT requests_per_minute FROM seagis_api.temperature_policy WHERE id);
END $$;

CREATE FUNCTION seagis_api.ingest(token text, packet jsonb, wire_sha256 text, wire_bytes integer)
 RETURNS jsonb LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE
 c seagis_api.credential; s seagis.sensor; pol seagis_api.temperature_policy;
 old seagis_api.packet_receipt; obs seagis.observation;
 t timestamptz; received timestamptz:=clock_timestamp(); val double precision;
 boot text; seq bigint; key text; digest text; flags text[]:='{}'; quality text:='accepted';
 prior seagis.observation; latest timestamptz; flag text;
 run_id uuid:=gen_random_uuid(); raw_id uuid:=gen_random_uuid(); observation_id uuid:=gen_random_uuid();
BEGIN
 c:=seagis_api.actor(token,'device');
 IF c.id IS NULL THEN RETURN seagis_api.reply(NULL,401,'unauthorized'); END IF;
 IF NOT seagis_api.rate_ok(c.id) THEN RETURN seagis_api.reply(c.id,429,'rate_limited'); END IF;
 SELECT * INTO s FROM seagis.sensor WHERE id=c.sensor_id;
 IF NOT s.active THEN RETURN seagis_api.reply(c.id,403,'sensor_inactive','{}',s.id); END IF;
 IF NOT s.is_synthetic AND NOT (SELECT real_ingestion_enabled FROM seagis.dataset WHERE dataset_key=s.dataset_key) THEN
  RETURN seagis_api.reply(c.id,503,'commissioning_disabled','{}',s.id);
 END IF;
 SELECT * INTO pol FROM seagis_api.temperature_policy WHERE id;
 IF jsonb_typeof(packet)<>'object' OR packet IS NULL THEN
  RETURN seagis_api.reply(c.id,422,'invalid_packet','{}',s.id);
 END IF;
 IF (SELECT array_agg(k ORDER BY k) FROM jsonb_object_keys(packet) k) IS DISTINCT FROM
 ARRAY['boot_id','observed_at','schema_version','sensor_id','sequence','unit','value_status','water_temperature']::text[]
 OR packet->>'schema_version' IS DISTINCT FROM '1.0.0'
 OR packet->>'unit' IS DISTINCT FROM 'degC'
 OR jsonb_typeof(packet->'boot_id') IS DISTINCT FROM 'string'
 OR packet->>'boot_id' !~ '^[A-Za-z0-9._-]{1,64}$'
 OR jsonb_typeof(packet->'sequence') IS DISTINCT FROM 'number'
 OR packet->>'sequence' !~ '^[0-9]{1,10}$'
 OR jsonb_typeof(packet->'observed_at') IS DISTINCT FROM 'string'
 OR packet->>'observed_at' !~ '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,6})?Z$'
 OR jsonb_typeof(packet->'sensor_id') IS DISTINCT FROM 'string'
 OR wire_sha256 IS NULL OR wire_sha256 !~ '^[0-9a-f]{64}$'
 OR wire_bytes IS NULL OR wire_bytes NOT BETWEEN 1 AND 8192 THEN
  RETURN seagis_api.reply(c.id,422,'invalid_packet','{}',s.id);
 END IF;
 IF packet->>'sensor_id' IS DISTINCT FROM s.id::text THEN
  RETURN seagis_api.reply(c.id,403,'sensor_forbidden','{}',s.id);
 END IF;
 BEGIN
  seq:=(packet->>'sequence')::bigint;
  t:=(packet->>'observed_at')::timestamptz;
  IF seq>4294967295 OR NOT isfinite(t) OR to_char(t AT TIME ZONE 'UTC','YYYY-MM-DD"T"HH24:MI:SS')<>left(packet->>'observed_at',19) THEN RAISE EXCEPTION 'invalid'; END IF;
  IF packet->>'value_status'='present' AND jsonb_typeof(packet->'water_temperature')='number' THEN
   val:=(packet->>'water_temperature')::double precision;
   IF NOT (val>'-Infinity'::double precision AND val<'Infinity'::double precision) THEN RAISE EXCEPTION 'invalid'; END IF;
  ELSIF packet->>'value_status'='missing' AND packet->'water_temperature'='null'::jsonb THEN val:=NULL;
  ELSE RAISE EXCEPTION 'invalid'; END IF;
 EXCEPTION WHEN OTHERS THEN RETURN seagis_api.reply(c.id,422,'invalid_packet','{}',s.id); END;
 boot:=packet->>'boot_id'; key:=boot||':'||seq;
 -- Semantic normalization makes numeric formatting, key order and timestamp precision retry-safe.
 digest:=seagis.jsonb_sha256(jsonb_build_object('sensor',s.id,'boot',boot,'seq',seq,
  'time',seagis_api.utc(t),'value',val,'status',packet->>'value_status'));
 PERFORM pg_advisory_xact_lock(hashtextextended('sensor:'||s.id,0));
 SELECT * INTO old FROM seagis_api.packet_receipt WHERE sensor_id=s.id AND source_record_key=key;
 IF FOUND THEN
  IF old.semantic_sha256<>digest THEN RETURN seagis_api.reply(c.id,409,'packet_conflict','{}',s.id); END IF;
  SELECT * INTO obs FROM seagis.observation WHERE id=old.observation_id;
  RETURN seagis_api.reply(c.id,200,'duplicate',jsonb_build_object('observation_id',obs.id,
    'ingestion_run_id',old.ingestion_run_id,'observed_at',seagis_api.utc(obs.observed_at),
    'quality_status',obs.quality_status,'flags',old.flags,'is_synthetic',s.is_synthetic),s.id);
 END IF;
 SELECT max(observed_at) INTO latest FROM seagis.observation WHERE sensor_id=s.id AND quality_status<>'rejected';
 SELECT * INTO prior FROM seagis.observation WHERE sensor_id=s.id AND observed_at<t
   AND value_status='present' AND quality_status<>'rejected' ORDER BY observed_at DESC LIMIT 1;
 IF val IS NULL THEN flags:=array_append(flags,'sensor_missing'); quality:='suspect'; END IF;
 IF val<pol.min_degc OR val>pol.max_degc THEN flags:=array_append(flags,'outside_pilot_envelope'); quality:='rejected'; END IF;
 IF t>received+make_interval(secs=>pol.future_tolerance_seconds) THEN
  flags:=array_append(flags,'clock_in_future'); quality:='rejected';
 ELSIF t>received THEN flags:=array_append(flags,'clock_ahead'); END IF;
 IF t<received-make_interval(secs=>pol.stale_after_seconds) THEN flags:=array_append(flags,'delayed_packet'); END IF;
 IF t<latest THEN flags:=array_append(flags,'out_of_order'); END IF;
 IF t>latest+interval '90 minutes' THEN flags:=array_append(flags,'gap_before'); END IF;
 IF prior.id IS NOT NULL AND t-prior.observed_at<=interval '2 hours' AND abs(val-prior.value)>pol.max_step_degc THEN
  flags:=array_append(flags,'rapid_change');
 END IF;
 IF quality='accepted' AND flags && ARRAY['clock_ahead','delayed_packet','rapid_change'] THEN quality:='suspect'; END IF;
 INSERT INTO seagis.ingestion_run(id,dataset_key,request_key,adapter_version,started_at,status,is_synthetic)
  VALUES(run_id,s.dataset_key,'a1:'||s.id||':'||key,'temperature-1.0.0',received,'running',s.is_synthetic);
 INSERT INTO seagis_raw.raw_payload(id,ingestion_run_id,dataset_key,is_synthetic,sha256,hash_basis,
   received_at,storage_mode,payload,byte_size,format,licence_snapshot,provider_metadata)
 VALUES(raw_id,run_id,s.dataset_key,s.is_synthetic,
   CASE WHEN s.is_synthetic THEN seagis.jsonb_sha256(packet) ELSE wire_sha256 END,
   CASE WHEN s.is_synthetic THEN 'jsonb_utf8_v1' ELSE 'source_bytes' END,
   received,CASE WHEN s.is_synthetic THEN 'inline' ELSE 'metadata_only' END,
   CASE WHEN s.is_synthetic THEN packet ELSE NULL END,wire_bytes,'application/json',
   'project-owned; A1 synthetic development / real retention gated',
   jsonb_build_object('wire_sha256',wire_sha256,'packet_schema','1.0.0','qc_policy',pol.version));
 INSERT INTO seagis.observation(id,plot_id,sensor_id,dataset_key,ingestion_run_id,raw_payload_id,
   is_synthetic,source_record_key,parameter_code,native_value,native_unit,value,unit,conversion_code,
   value_status,observed_at,ingested_at,quality_status)
 VALUES(observation_id,s.plot_id,s.id,s.dataset_key,run_id,raw_id,s.is_synthetic,key,
   'water_temperature',val,'degC',val,'degC','identity',packet->>'value_status',t,received,quality);
 FOREACH flag IN ARRAY flags LOOP
  INSERT INTO seagis.quality_event(ingestion_run_id,dataset_key,is_synthetic,event_key,observation_id,
    event_code,severity,details)
  VALUES(run_id,s.dataset_key,s.is_synthetic,flag,observation_id,flag,
   CASE WHEN quality='rejected' THEN 'error' WHEN flag IN ('gap_before','out_of_order') THEN 'info' ELSE 'warning' END,
   jsonb_build_object('policy_version',pol.version,'min_degc',pol.min_degc,'max_degc',pol.max_degc,
     'max_step_degc',pol.max_step_degc,'stale_after_seconds',pol.stale_after_seconds));
 END LOOP;
 INSERT INTO seagis_api.packet_receipt VALUES(s.id,key,digest,observation_id,run_id,flags);
 UPDATE seagis.ingestion_run SET status='succeeded',completed_at=clock_timestamp() WHERE id=run_id;
 RETURN seagis_api.reply(c.id,201,'stored',jsonb_build_object('observation_id',observation_id,
   'ingestion_run_id',run_id,'observed_at',seagis_api.utc(t),'quality_status',quality,
   'flags',flags,'is_synthetic',s.is_synthetic),s.id);
END $$;

CREATE FUNCTION seagis_api.history(token text, target_plot uuid, spec jsonb)
 RETURNS jsonb LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE c seagis_api.credential; a timestamptz; b timestamptz; lim integer;
 cursor_id uuid; cursor_time timestamptz; rows jsonb; next_id uuid; coverage jsonb; synthetic boolean;
BEGIN
 c:=seagis_api.actor(token,'reader');
 IF c.id IS NULL THEN RETURN seagis_api.reply(NULL,401,'unauthorized'); END IF;
 IF NOT seagis_api.rate_ok(c.id) THEN RETURN seagis_api.reply(c.id,429,'rate_limited'); END IF;
 IF NOT EXISTS(SELECT FROM seagis_api.reader_plot WHERE credential_id=c.id AND plot_id=target_plot) THEN
  RETURN seagis_api.reply(c.id,403,'plot_forbidden'); END IF;
 BEGIN
  IF spec->>'from' IS NULL OR spec->>'to' IS NULL
   OR spec->>'from' !~ '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,6})?Z$'
   OR spec->>'to' !~ '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,6})?Z$' THEN RAISE EXCEPTION 'invalid'; END IF;
  a:=(spec->>'from')::timestamptz; b:=(spec->>'to')::timestamptz;
  lim:=coalesce((spec->>'limit')::integer,200);
  IF NOT isfinite(a) OR NOT isfinite(b)
   OR to_char(a AT TIME ZONE 'UTC','YYYY-MM-DD"T"HH24:MI:SS')<>left(spec->>'from',19)
   OR to_char(b AT TIME ZONE 'UTC','YYYY-MM-DD"T"HH24:MI:SS')<>left(spec->>'to',19) OR a>=b OR b-a>interval '7 days' OR lim NOT BETWEEN 1 AND 500 THEN RAISE EXCEPTION 'invalid'; END IF;
  IF spec->>'cursor' IS NOT NULL THEN
   cursor_id:=(spec->>'cursor')::uuid;
   SELECT observed_at INTO cursor_time FROM seagis.observation WHERE id=cursor_id AND plot_id=target_plot AND observed_at>=a AND observed_at<b;
   IF NOT FOUND THEN RAISE EXCEPTION 'invalid'; END IF;
  END IF;
 EXCEPTION WHEN OTHERS THEN RETURN seagis_api.reply(c.id,400,'invalid_query'); END;
 SELECT is_synthetic INTO synthetic FROM seagis.plot WHERE id=target_plot;
 WITH page AS (
  SELECT o.*,r.flags,row_number() OVER(ORDER BY o.observed_at,o.id) AS n
  FROM seagis.observation o LEFT JOIN seagis_api.packet_receipt r ON r.observation_id=o.id
  WHERE o.plot_id=target_plot AND o.observed_at>=a AND o.observed_at<b
   AND (cursor_id IS NULL OR (o.observed_at,o.id)>(cursor_time,cursor_id))
  ORDER BY o.observed_at,o.id LIMIT lim+1
 ) SELECT coalesce(jsonb_agg(jsonb_build_object('id',id,'sensor_id',sensor_id,'value',value,
   'unit',unit,'value_status',value_status,'observed_at',seagis_api.utc(observed_at),
   'ingested_at',seagis_api.utc(ingested_at),'quality_status',quality_status,'flags',coalesce(flags,'{}'),
   'ingestion_run_id',ingestion_run_id,'is_synthetic',is_synthetic) ORDER BY observed_at,id) FILTER(WHERE n<=lim),'[]'),
   CASE WHEN max(n)>lim THEN (array_agg(id ORDER BY observed_at,id) FILTER(WHERE n=lim))[1] END
 INTO rows,next_id FROM page;
 WITH slots AS (SELECT generate_series(date_trunc('hour',a AT TIME ZONE 'UTC') AT TIME ZONE 'UTC',
   date_trunc('hour',(b-interval '1 microsecond') AT TIME ZONE 'UTC') AT TIME ZONE 'UTC',interval '1 hour') t),
 buckets AS (SELECT date_trunc('hour',observed_at AT TIME ZONE 'UTC') AT TIME ZONE 'UTC' t,
   count(*) packets,count(*) FILTER(WHERE value_status='present' AND quality_status<>'rejected') usable
   FROM seagis.observation WHERE plot_id=target_plot AND observed_at>=a AND observed_at<b GROUP BY 1)
 SELECT jsonb_build_object('expected_hours',count(*),'hours_with_packets',count(*) FILTER(WHERE packets>0),
  'hours_with_usable_values',count(*) FILTER(WHERE usable>0),
  'missing_hours',coalesce(jsonb_agg(seagis_api.utc(slots.t) ORDER BY slots.t) FILTER(WHERE packets IS NULL),'[]'),
  'unusable_hours',coalesce(jsonb_agg(seagis_api.utc(slots.t) ORDER BY slots.t) FILTER(WHERE packets>0 AND usable=0),'[]'))
 INTO coverage FROM slots LEFT JOIN buckets USING(t);
 RETURN seagis_api.reply(c.id,200,'ok',jsonb_build_object('plot_id',target_plot,'is_synthetic',synthetic,
  'from',seagis_api.utc(a),'to',seagis_api.utc(b),'observations',rows,'next_cursor',next_id,'coverage',coverage));
END $$;

CREATE FUNCTION seagis_api.status(token text) RETURNS jsonb LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE c seagis_api.credential; result jsonb; stale_seconds integer; BEGIN
 c:=seagis_api.actor(token,'reader');
 IF c.id IS NULL THEN RETURN seagis_api.reply(NULL,401,'unauthorized'); END IF;
 IF NOT seagis_api.rate_ok(c.id) THEN RETURN seagis_api.reply(c.id,429,'rate_limited'); END IF;
 SELECT stale_after_seconds INTO stale_seconds FROM seagis_api.temperature_policy WHERE id;
 SELECT coalesce(jsonb_agg(jsonb_build_object('plot_id',p.id,'plot_code',p.plot_code,'is_synthetic',p.is_synthetic,
  'latest_usable_observed_at',seagis_api.utc(o.latest),'last_ingested_at',seagis_api.utc(o.received),
  'age_seconds',extract(epoch FROM now()-o.latest),'stale',o.latest IS NULL OR now()-o.latest>make_interval(secs=>stale_seconds),
  'observations_last_24h',o.n,'rejected_last_24h',o.bad) ORDER BY p.plot_code),'[]') INTO result
 FROM seagis_api.reader_plot rp JOIN seagis.plot p ON p.id=rp.plot_id
 CROSS JOIN LATERAL (SELECT max(observed_at) FILTER(WHERE value_status='present' AND quality_status<>'rejected' AND observed_at<=now()) latest,
  max(ingested_at) received,count(*) FILTER(WHERE ingested_at>now()-interval '24 hours') n,
  count(*) FILTER(WHERE ingested_at>now()-interval '24 hours' AND quality_status='rejected') bad
  FROM seagis.observation WHERE plot_id=p.id) o WHERE rp.credential_id=c.id;
 RETURN seagis_api.reply(c.id,200,'ok',jsonb_build_object('checked_at',seagis_api.utc(now()),
  'stale_after_seconds',stale_seconds,'plots',result));
END $$;

REVOKE ALL ON ALL FUNCTIONS IN SCHEMA seagis_api FROM PUBLIC,anon,authenticated,service_role,seagis_iot_gateway;
GRANT EXECUTE ON FUNCTION seagis_api.ingest(text,jsonb,text,integer),
 seagis_api.history(text,uuid,jsonb),seagis_api.status(text) TO seagis_iot_gateway;
ALTER ROLE seagis_iot_gateway SET statement_timeout='10s';
ALTER ROLE seagis_iot_gateway SET idle_in_transaction_session_timeout='10s';
