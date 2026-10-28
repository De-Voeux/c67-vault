-- A2: real regional model vintages, separate demo-only mapping, least-privilege worker.
CREATE SCHEMA seagis_environment;
REVOKE ALL ON SCHEMA seagis_environment FROM PUBLIC, anon, authenticated;
CREATE ROLE seagis_environment_worker NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOBYPASSRLS;
GRANT USAGE ON SCHEMA seagis_environment TO seagis_environment_worker;
ALTER DEFAULT PRIVILEGES IN SCHEMA seagis_environment REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;

ALTER TABLE seagis_raw.raw_payload DROP CONSTRAINT raw_payload_hash_basis_v2;
ALTER TABLE seagis_raw.raw_payload ADD CONSTRAINT raw_payload_hash_basis_v3
 CHECK (hash_basis IN ('source_bytes','synthetic_json_canonical_v1','jsonb_utf8_v1','toolbox_subset_json_v1'));

ALTER TABLE seagis.forecast_run DROP CONSTRAINT forecast_run_run_kind_check;
ALTER TABLE seagis.forecast_run ADD CONSTRAINT forecast_run_run_kind_check
 CHECK(run_kind IN ('forecast','analysis','analysis_forecast_unspecified'));

CREATE TABLE seagis_environment.policy (
 dataset_key text PRIMARY KEY REFERENCES seagis.dataset,
 enabled boolean NOT NULL DEFAULT true,
 purpose text NOT NULL CHECK(purpose='noncommercial_educational_prototype'),
 licence_url text NOT NULL,
 terms_review text NOT NULL,
 attribution text NOT NULL,
 update_seconds int NOT NULL CHECK(update_seconds>=21600),
 release_offset_seconds int NOT NULL CHECK(release_offset_seconds>=0 AND release_offset_seconds<update_seconds),
 stale_seconds int NOT NULL CHECK(stale_seconds>=update_seconds),
 -- metadata_only is an explicit operational retention policy, even when licence permits copies.
 retention_mode text NOT NULL DEFAULT 'metadata_only' CHECK(retention_mode='metadata_only'),
 reviewed_at timestamptz NOT NULL DEFAULT now()
);
INSERT INTO seagis_environment.policy(dataset_key,purpose,licence_url,terms_review,attribution,
 update_seconds,release_offset_seconds,stale_seconds)
SELECT dataset_key,'noncommercial_educational_prototype',licence_url,
 CASE WHEN source_key='copernicus' THEN 'cmems-licence-20261022-sections-2.2-2.4-2.6'
 ELSE 'open-meteo-terms-20261022-noncommercial-cc-by-4.0' END,
 attribution,
 CASE WHEN source_key='copernicus' THEN 86400 ELSE 21600 END,
 CASE WHEN dataset_key='cmems_nutrients_daily' THEN 45000
      WHEN source_key='copernicus' THEN 30600 ELSE 16200 END,
 CASE WHEN source_key='copernicus' THEN 172800 ELSE 43200 END
FROM seagis.dataset WHERE dataset_key IN
 ('cmems_salinity_6h','cmems_currents_6h','cmems_nutrients_daily','open_meteo_gfs');
UPDATE seagis.dataset SET real_ingestion_enabled=true
 WHERE dataset_key IN (SELECT dataset_key FROM seagis_environment.policy);

CREATE TABLE seagis_environment.schedule_state (
 dataset_key text PRIMARY KEY REFERENCES seagis_environment.policy,
 lease_id uuid,
 lease_until timestamptz,
 next_attempt_at timestamptz NOT NULL DEFAULT '-infinity',
 last_success_at timestamptz,
 last_attempt_at timestamptz,
 last_error_code text,
 failures int NOT NULL DEFAULT 0 CHECK(failures>=0),
 last_forecast_run_id uuid REFERENCES seagis.forecast_run
);
INSERT INTO seagis_environment.schedule_state(dataset_key) SELECT dataset_key FROM seagis_environment.policy;
CREATE TABLE seagis_environment.attempt (
 id uuid PRIMARY KEY,
 dataset_key text NOT NULL REFERENCES seagis_environment.policy,
 started_at timestamptz NOT NULL,
 completed_at timestamptz,
 status text NOT NULL CHECK(status IN ('running','succeeded','duplicate','failed','abandoned')),
 error_code text,
 forecast_run_id uuid REFERENCES seagis.forecast_run,
 CHECK ((completed_at IS NULL)=(status='running'))
);
-- This bridge is for fictional A/B preview only. It is NOT seagis.plot_grid_mapping;
-- the existing feature-input guards cannot accept it. Real/synthetic guards stay intact.
CREATE TABLE seagis_environment.demo_grid_mapping (
 plot_id uuid NOT NULL,
 plot_is_synthetic boolean NOT NULL DEFAULT true CHECK(plot_is_synthetic),
 source_grid_id uuid NOT NULL,
 dataset_key text NOT NULL REFERENCES seagis_environment.policy,
 grid_is_synthetic boolean NOT NULL DEFAULT false CHECK(NOT grid_is_synthetic),
 example_latitude seagis.finite_float NOT NULL CHECK(example_latitude BETWEEN -90 AND 90),
 example_longitude seagis.finite_float NOT NULL CHECK(example_longitude BETWEEN -180 AND 180),
 coordinate_status text NOT NULL CHECK(coordinate_status='example_not_surveyed'),
 distance_m seagis.finite_float NOT NULL CHECK(distance_m BETWEEN 0 AND 30000),
 sampling_method text NOT NULL CHECK(sampling_method IN ('nearest_cell','provider_returned_coordinate')),
 created_at timestamptz NOT NULL DEFAULT now(),
 FOREIGN KEY(plot_id,plot_is_synthetic) REFERENCES seagis.plot(id,is_synthetic),
 FOREIGN KEY(source_grid_id,dataset_key,grid_is_synthetic) REFERENCES seagis.source_grid(id,dataset_key,is_synthetic),
 PRIMARY KEY(plot_id,source_grid_id),
 CHECK(plot_id IN ('00000000-0000-4000-8000-000000000001'::uuid,'00000000-0000-4000-8000-000000000002'::uuid))
);
CREATE TRIGGER immutable_demo_mapping BEFORE UPDATE OR DELETE ON seagis_environment.demo_grid_mapping
 FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();

CREATE VIEW seagis_environment.current_speed WITH(security_invoker=true) AS
SELECT u.id AS eastward_value_id,v.id AS northward_value_id,u.forecast_run_id,u.source_grid_id,
 u.valid_at,u.ingested_at,greatest(u.ingested_at,v.ingested_at) AS available_at,
 CASE WHEN u.value_status='present' AND v.value_status='present'
 THEN sqrt(u.value*u.value+v.value*v.value) END AS speed_m_s,
 'sqrt(uo^2+vo^2); a2-vector-magnitude-v1'::text AS derivation
FROM seagis.forecast_value u JOIN seagis.forecast_value v
 ON u.forecast_run_id=v.forecast_run_id AND u.source_grid_id=v.source_grid_id AND u.valid_at=v.valid_at
WHERE u.parameter_code='current_eastward' AND v.parameter_code='current_northward';

CREATE FUNCTION seagis_environment.claim(k text, force_fetch boolean DEFAULT false)
RETURNS jsonb LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE p seagis_environment.policy; s seagis_environment.schedule_state; lease uuid:=gen_random_uuid();
BEGIN
 SELECT * INTO p FROM seagis_environment.policy WHERE dataset_key=k AND enabled;
 IF NOT FOUND THEN RAISE EXCEPTION 'environment_dataset_disabled'; END IF;
 SELECT * INTO s FROM seagis_environment.schedule_state WHERE dataset_key=k FOR UPDATE;
 IF s.lease_until>clock_timestamp() OR (NOT force_fetch AND s.next_attempt_at>clock_timestamp()) THEN
  RETURN jsonb_build_object('status','not_due','next_attempt_at',s.next_attempt_at,'lease_until',s.lease_until);
 END IF;
 UPDATE seagis_environment.attempt SET status='abandoned',completed_at=clock_timestamp(),error_code='lease_expired'
  WHERE id=s.lease_id AND status='running';
 UPDATE seagis_environment.schedule_state SET lease_id=lease,lease_until=clock_timestamp()+interval '20 minutes',
  last_attempt_at=clock_timestamp() WHERE dataset_key=k;
 INSERT INTO seagis_environment.attempt(id,dataset_key,started_at,status) VALUES(lease,k,clock_timestamp(),'running');
 RETURN jsonb_build_object('status','claimed','lease_id',lease,'policy',to_jsonb(p));
END $$;

CREATE FUNCTION seagis_environment.finish_failure(lease uuid, code text)
RETURNS void LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE s seagis_environment.schedule_state;
BEGIN
 IF code NOT IN ('network_failure','rate_limited','auth_failure','schema_failure','storage_failure','licence_failure','timeout')
 THEN code:='schema_failure'; END IF;
 SELECT * INTO s FROM seagis_environment.schedule_state WHERE lease_id=lease FOR UPDATE;
 IF NOT FOUND THEN RAISE EXCEPTION 'lease_unavailable'; END IF;
 UPDATE seagis_environment.attempt SET status='failed',completed_at=clock_timestamp(),error_code=code WHERE id=lease AND status='running';
 UPDATE seagis_environment.schedule_state SET lease_id=NULL,lease_until=NULL,failures=failures+1,last_error_code=code,
  next_attempt_at=clock_timestamp()+make_interval(secs=>least(21600,900*power(2,least(failures,4)))::int)
 WHERE dataset_key=s.dataset_key;
END $$;

CREATE FUNCTION seagis_environment.persist(lease uuid, batch jsonb)
RETURNS jsonb LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE s seagis_environment.schedule_state; pol seagis_environment.policy; d seagis.dataset;
 ing uuid:=gen_random_uuid(); raw_id uuid:=gen_random_uuid(); run_id uuid:=gen_random_uuid(); grid_id uuid;
 g jsonb; v jsonb; m jsonb; par seagis.dataset_parameter; t timestamptz:=clock_timestamp();
 started timestamptz; received timestamptz; duplicate boolean:=false; n int:=0; nxt timestamptz;
BEGIN
 IF batch IS NULL OR pg_column_size(batch)>2000000 OR jsonb_typeof(batch)<>'object'
 OR NOT batch ?& ARRAY['dataset_key','purpose','terms_review','dataset_version','provider_dataset_id',
 'run_key','raw_sha256','hash_basis','grids','values','mappings','started_at','received_at','metadata','raw_byte_size','format'] THEN RAISE EXCEPTION 'batch_size'; END IF;
 SELECT * INTO s FROM seagis_environment.schedule_state WHERE lease_id=lease FOR UPDATE;
 IF NOT FOUND OR s.lease_until<t THEN RAISE EXCEPTION 'lease_unavailable'; END IF;
 SELECT * INTO pol FROM seagis_environment.policy WHERE dataset_key=s.dataset_key AND enabled;
 IF NOT FOUND THEN RAISE EXCEPTION 'environment_dataset_disabled'; END IF;
 SELECT * INTO d FROM seagis.dataset WHERE dataset_key=s.dataset_key AND real_ingestion_enabled;
 IF NOT FOUND OR batch->>'dataset_key'<>s.dataset_key OR batch->>'purpose'<>pol.purpose
 OR batch->>'terms_review'<>pol.terms_review OR batch->>'dataset_version'<>d.dataset_version
 OR batch->>'provider_dataset_id'<>d.provider_dataset_id THEN RAISE EXCEPTION 'contract_or_licence_failure'; END IF;
 IF batch->>'run_key' !~ '^[0-9a-f]{64}$' OR batch->>'raw_sha256' !~ '^[0-9a-f]{64}$'
 OR batch->>'hash_basis' NOT IN ('source_bytes','toolbox_subset_json_v1')
 OR jsonb_array_length(batch->'grids') NOT BETWEEN 1 AND 4
 OR jsonb_array_length(batch->'values') NOT BETWEEN 1 AND 5000
 OR jsonb_array_length(batch->'mappings')<>2 THEN RAISE EXCEPTION 'batch_contract'; END IF;
 started:=(batch->>'started_at')::timestamptz; received:=(batch->>'received_at')::timestamptz;
 IF started>received OR received>t OR received<t-interval '1 hour' THEN RAISE EXCEPTION 'receipt_time'; END IF;
 -- Publication/init remains unknown: aggregate API/STAC timestamps cannot prove response issuance.
 IF batch->'metadata'->>'issue_time_basis'<>'unknown' THEN RAISE EXCEPTION 'unverified_issue_time'; END IF;
 SELECT id INTO run_id FROM seagis.forecast_run WHERE dataset_key=s.dataset_key AND run_key=batch->>'run_key';
 duplicate:=FOUND;
 IF NOT duplicate THEN
  run_id:=gen_random_uuid();
  INSERT INTO seagis.ingestion_run(id,dataset_key,request_key,adapter_version,started_at,status,is_synthetic)
   VALUES(ing,s.dataset_key,'a2:'||(batch->>'run_key'),'environment-1.0.0',started,'running',false);
  INSERT INTO seagis_raw.raw_payload(id,ingestion_run_id,dataset_key,is_synthetic,sha256,hash_basis,
   received_at,storage_mode,byte_size,format,licence_snapshot,provider_metadata)
  VALUES(raw_id,ing,s.dataset_key,false,batch->>'raw_sha256',batch->>'hash_basis',received,'metadata_only',
   (batch->>'raw_byte_size')::bigint,batch->>'format',pol.terms_review||'; '||pol.licence_url||'; '||pol.attribution,batch->'metadata');
  INSERT INTO seagis.forecast_run(id,dataset_key,ingestion_run_id,raw_payload_id,is_synthetic,run_key,run_kind,
   issue_time_basis,ingested_at)
  VALUES(run_id,s.dataset_key,ing,raw_id,false,batch->>'run_key',
   CASE WHEN d.source_key='copernicus' THEN 'analysis_forecast_unspecified' ELSE 'forecast' END,'unknown',t);
  FOR g IN SELECT value FROM jsonb_array_elements(batch->'grids') LOOP
   INSERT INTO seagis.source_grid(dataset_key,grid_key,grid_version,identity_basis,latitude,longitude,depth_m,is_synthetic)
   VALUES(s.dataset_key,g->>'key',d.dataset_version,g->>'identity_basis',(g->>'latitude')::float8,
    (g->>'longitude')::float8,(g->>'depth_m')::float8,false) ON CONFLICT(dataset_key,grid_key,is_synthetic) DO NOTHING;
   SELECT id INTO grid_id FROM seagis.source_grid WHERE dataset_key=s.dataset_key AND grid_key=g->>'key' AND NOT is_synthetic
    AND latitude=(g->>'latitude')::float8 AND longitude=(g->>'longitude')::float8 AND depth_m=(g->>'depth_m')::float8;
   IF NOT FOUND THEN RAISE EXCEPTION 'grid_identity_conflict'; END IF;
  END LOOP;
  FOR v IN SELECT value FROM jsonb_array_elements(batch->'values') LOOP
   SELECT * INTO par FROM seagis.dataset_parameter WHERE dataset_key=s.dataset_key AND parameter_code=v->>'parameter';
   IF NOT FOUND THEN RAISE EXCEPTION 'unknown_parameter'; END IF;
   SELECT id INTO STRICT grid_id FROM seagis.source_grid WHERE dataset_key=s.dataset_key AND grid_key=v->>'grid_key' AND NOT is_synthetic;
   INSERT INTO seagis.forecast_value(forecast_run_id,source_grid_id,dataset_key,is_synthetic,parameter_code,
    native_value,native_unit,value,unit,conversion_code,value_status,valid_at,ingested_at,
    temporal_support,interval_status,period_start_at,period_end_at,quality_status)
   VALUES(run_id,grid_id,s.dataset_key,false,par.parameter_code,(v->>'value')::float8,par.native_unit,
    (v->>'value')::float8,par.unit,par.conversion_code,v->>'value_status',(v->>'valid_at')::timestamptz,t,
    par.temporal_support,v->>'interval_status',(v->>'period_start_at')::timestamptz,(v->>'period_end_at')::timestamptz,'unreviewed');
   n:=n+1;
  END LOOP;
  UPDATE seagis.ingestion_run SET completed_at=clock_timestamp(),status='succeeded' WHERE id=ing;
 END IF;
 -- Mapping can be added on a duplicate fetch; values are never copied per plot.
 FOR m IN SELECT value FROM jsonb_array_elements(batch->'mappings') LOOP
  SELECT id INTO STRICT grid_id FROM seagis.source_grid WHERE dataset_key=s.dataset_key AND grid_key=m->>'grid_key' AND NOT is_synthetic;
  INSERT INTO seagis_environment.demo_grid_mapping(plot_id,source_grid_id,dataset_key,example_latitude,example_longitude,
   coordinate_status,distance_m,sampling_method)
  VALUES((m->>'plot_id')::uuid,grid_id,s.dataset_key,(m->>'latitude')::float8,(m->>'longitude')::float8,
   m->>'coordinate_status',(m->>'distance_m')::float8,m->>'sampling_method') ON CONFLICT DO NOTHING;
 END LOOP;
 -- Next nominal publication plus an explicit operational grace period; no hourly Copernicus fetch.
 nxt:=to_timestamp((floor((extract(epoch FROM t)-pol.release_offset_seconds)/pol.update_seconds)+1)*pol.update_seconds+pol.release_offset_seconds);
 UPDATE seagis_environment.schedule_state SET lease_id=NULL,lease_until=NULL,last_success_at=t,
  last_forecast_run_id=run_id,last_error_code=NULL,failures=0,next_attempt_at=nxt WHERE dataset_key=s.dataset_key;
 UPDATE seagis_environment.attempt SET completed_at=clock_timestamp(),status=CASE WHEN duplicate THEN 'duplicate' ELSE 'succeeded' END,
  forecast_run_id=run_id WHERE id=lease;
 RETURN jsonb_build_object('status',CASE WHEN duplicate THEN 'duplicate' ELSE 'succeeded' END,
  'forecast_run_id',run_id,'inserted_values',n,'next_attempt_at',nxt);
END $$;

CREATE FUNCTION seagis_environment.status()
RETURNS jsonb LANGUAGE sql SECURITY DEFINER SET search_path=pg_catalog AS $$
 SELECT coalesce(jsonb_agg(to_jsonb(x) ORDER BY dataset_key),'[]'::jsonb) FROM (
 SELECT p.dataset_key,p.enabled,p.attribution,p.licence_url,p.retention_mode,p.update_seconds,
 s.last_success_at,s.last_attempt_at,s.last_error_code,s.failures,s.next_attempt_at,s.lease_until,s.last_forecast_run_id,
 r.ingested_at AS vintage_available_at,
 CASE WHEN r.id IS NULL THEN 'unavailable' WHEN clock_timestamp()-r.ingested_at>make_interval(secs=>p.stale_seconds)
 THEN 'stale_unusable' WHEN s.last_error_code IS NOT NULL THEN 'cached_after_failure' ELSE 'available' END AS availability,
 (SELECT count(*) FROM seagis.forecast_value v WHERE v.forecast_run_id=r.id) AS value_count,
 (SELECT count(*) FROM seagis.source_grid g WHERE g.dataset_key=p.dataset_key AND NOT g.is_synthetic) AS grid_count,
 (SELECT count(*) FROM seagis_environment.demo_grid_mapping m WHERE m.dataset_key=p.dataset_key) AS demo_mapping_count
 FROM seagis_environment.policy p JOIN seagis_environment.schedule_state s USING(dataset_key)
 LEFT JOIN seagis.forecast_run r ON r.id=s.last_forecast_run_id) x
$$;

CREATE FUNCTION seagis_environment.preview(plot uuid, as_of timestamptz DEFAULT now())
RETURNS jsonb LANGUAGE sql SECURITY DEFINER SET search_path=pg_catalog AS $$
 WITH chosen AS (
 SELECT DISTINCT ON (r.dataset_key) r.* FROM seagis.forecast_run r
 JOIN seagis_environment.policy p USING(dataset_key)
 WHERE NOT r.is_synthetic AND p.enabled AND r.ingested_at<=least(as_of,clock_timestamp())
 AND least(as_of,clock_timestamp())-r.ingested_at<=make_interval(secs=>p.stale_seconds)
 ORDER BY r.dataset_key,r.ingested_at DESC,r.id DESC
 ), rows AS (
 SELECT r.dataset_key,r.id AS forecast_run_id,r.issued_at,r.issue_time_basis,r.ingested_at AS available_at,
 g.id AS grid_id,g.latitude,g.longitude,g.depth_m,m.distance_m,m.coordinate_status,
 v.id AS value_id,v.parameter_code,v.value,v.value_status,v.unit,v.valid_at,v.temporal_support,
 v.interval_status,v.period_start_at,v.period_end_at,v.quality_status,p.attribution,p.licence_url,
 cs.speed_m_s,cs.eastward_value_id,cs.northward_value_id
 FROM chosen r JOIN seagis.forecast_value v ON v.forecast_run_id=r.id
 JOIN seagis.source_grid g ON g.id=v.source_grid_id
 JOIN seagis_environment.demo_grid_mapping m ON m.source_grid_id=g.id AND m.plot_id=plot
 JOIN seagis_environment.policy p ON p.dataset_key=r.dataset_key
 LEFT JOIN seagis_environment.current_speed cs ON cs.eastward_value_id=v.id
 WHERE v.valid_at>=as_of AND v.valid_at<as_of+interval '2 days'
 ORDER BY r.dataset_key,v.valid_at,v.parameter_code LIMIT 1500)
 SELECT jsonb_build_object('use','demo_preview_only; excluded from training',
  'plot_id',plot,'as_of',as_of,'data',coalesce(jsonb_agg(to_jsonb(rows)),'[]'::jsonb)) FROM rows
$$;

DO $$ DECLARE t text; BEGIN
 FOREACH t IN ARRAY ARRAY['policy','schedule_state','attempt','demo_grid_mapping'] LOOP
  EXECUTE format('ALTER TABLE seagis_environment.%I ENABLE ROW LEVEL SECURITY',t);
 END LOOP;
END $$;
REVOKE ALL ON ALL TABLES IN SCHEMA seagis_environment FROM PUBLIC,anon,authenticated,seagis_environment_worker;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA seagis_environment FROM PUBLIC,anon,authenticated;
GRANT EXECUTE ON FUNCTION seagis_environment.claim(text,boolean),seagis_environment.finish_failure(uuid,text),
 seagis_environment.persist(uuid,jsonb),seagis_environment.status(),seagis_environment.preview(uuid,timestamptz)
 TO seagis_environment_worker;
