-- A3: bounded source bundles and append-only quality/alignment snapshots.
-- No new provider fetches, Data API grants or model feature computations.
CREATE SCHEMA seagis_quality;
REVOKE ALL ON SCHEMA seagis_quality FROM PUBLIC, anon, authenticated, service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA seagis_quality REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;
CREATE ROLE seagis_quality_worker NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOBYPASSRLS;
GRANT USAGE ON SCHEMA seagis_quality TO seagis_quality_worker;

-- Effective time alone does not prove when a mapping became known to the system.
ALTER TABLE seagis.plot_grid_mapping ADD COLUMN recorded_at timestamptz NOT NULL DEFAULT clock_timestamp();
CREATE TRIGGER immutable_alignment_mapping BEFORE UPDATE OR DELETE ON seagis.plot_grid_mapping
 FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();

CREATE TABLE seagis_quality.policy (
 version text PRIMARY KEY,
 definition jsonb NOT NULL CHECK(jsonb_typeof(definition)='object'),
 policy_sha256 text NOT NULL CHECK(policy_sha256 ~ '^[0-9a-f]{64}$'),
 code_sha256 text NOT NULL CHECK(code_sha256 ~ '^[0-9a-f]{64}$'),
 registered_at timestamptz NOT NULL DEFAULT clock_timestamp()
);
CREATE TABLE seagis_quality.alignment_snapshot (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 plot_id uuid NOT NULL REFERENCES seagis.plot,
 mode text NOT NULL CHECK(mode IN ('demo_review','operational_review')),
 start_at timestamptz NOT NULL,
 end_at timestamptz NOT NULL CHECK(end_at>start_at AND end_at-start_at<=interval '7 days'),
 policy_version text NOT NULL REFERENCES seagis_quality.policy,
 source_sha256 text NOT NULL CHECK(source_sha256 ~ '^[0-9a-f]{64}$'),
 input_manifest_sha256 text NOT NULL CHECK(input_manifest_sha256 ~ '^[0-9a-f]{64}$'),
 body jsonb NOT NULL CHECK(jsonb_typeof(body)='object'),
 body_sha256 text GENERATED ALWAYS AS (seagis.jsonb_sha256(body)) STORED,
 created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
 UNIQUE(plot_id,mode,start_at,end_at,policy_version,source_sha256)
);
CREATE TABLE seagis_quality.snapshot_input (
 snapshot_id uuid NOT NULL REFERENCES seagis_quality.alignment_snapshot,
 aligned_at timestamptz NOT NULL,
 source_ref text NOT NULL,
 observation_id uuid REFERENCES seagis.observation,
 forecast_value_id uuid REFERENCES seagis.forecast_value,
 CHECK(num_nonnulls(observation_id,forecast_value_id)=1),
 CHECK(source_ref=CASE WHEN observation_id IS NOT NULL THEN 'observation:'||observation_id
                      ELSE 'forecast_value:'||forecast_value_id END),
 PRIMARY KEY(snapshot_id,aligned_at,source_ref)
);

CREATE FUNCTION seagis_quality.source_bundle(p_plot uuid,p_start timestamptz,p_end timestamptz,p_demo boolean DEFAULT false)
RETURNS jsonb LANGUAGE plpgsql STABLE SECURITY DEFINER SET search_path=pg_catalog SET timezone='UTC' AS $$
DECLARE pl seagis.plot; mappings jsonb; observations jsonb; forecasts jsonb; result jsonb;
BEGIN
 IF p_start IS NULL OR p_end IS NULL OR p_demo IS NULL OR p_start<>date_trunc('hour',p_start)
  OR p_end<>date_trunc('hour',p_end) OR p_end<=p_start OR p_end-p_start>interval '7 days'
  OR p_end-interval '1 hour'>statement_timestamp() THEN RAISE EXCEPTION 'invalid_alignment_window'; END IF;
 SELECT * INTO pl FROM seagis.plot WHERE id=p_plot;
 IF NOT FOUND OR pl.is_synthetic<>p_demo THEN RAISE EXCEPTION 'plot_mode_mismatch'; END IF;

 SELECT coalesce(jsonb_agg(x ORDER BY x->>'mapping_key'),'[]'::jsonb) INTO mappings FROM (
  SELECT jsonb_build_object('mapping_key','mapping:'||m.id,'kind','operational',
   'plot_id',m.plot_id,'source_grid_id',g.id,'dataset_key',g.dataset_key,
   'recorded_at',m.recorded_at,'effective_from',m.effective_from,'effective_until',m.effective_until,
   'distance_m',m.distance_m,'sampling_method',m.sampling_method,'representativeness',m.representativeness,
   'grid_latitude',g.latitude,'grid_longitude',g.longitude,'depth_m',g.depth_m,
   'resolution_lat_deg',d.resolution_lat_deg,'resolution_lon_deg',d.resolution_lon_deg,
   'coordinate_status',pl.location_status) x
  FROM seagis.plot_grid_mapping m JOIN seagis.source_grid g ON g.id=m.source_grid_id
  JOIN seagis.dataset d ON d.dataset_key=g.dataset_key
  WHERE m.plot_id=p_plot AND m.is_synthetic=pl.is_synthetic AND g.is_synthetic=pl.is_synthetic
   AND m.recorded_at<p_end AND m.effective_from<p_end AND (m.effective_until IS NULL OR m.effective_until>p_start)
  UNION ALL
  SELECT jsonb_build_object('mapping_key','demo:'||g.id,'kind','demo',
   'plot_id',m.plot_id,'source_grid_id',g.id,'dataset_key',g.dataset_key,
   'recorded_at',m.created_at,'effective_from',m.created_at,'effective_until',NULL,
   'distance_m',m.distance_m,'sampling_method',m.sampling_method,'representativeness','unverified',
   'grid_latitude',g.latitude,'grid_longitude',g.longitude,'depth_m',g.depth_m,
   'resolution_lat_deg',d.resolution_lat_deg,'resolution_lon_deg',d.resolution_lon_deg,
   'coordinate_status',m.coordinate_status) x
  FROM seagis_environment.demo_grid_mapping m JOIN seagis.source_grid g ON g.id=m.source_grid_id
  JOIN seagis.dataset d ON d.dataset_key=g.dataset_key
  WHERE p_demo AND m.plot_id=p_plot AND m.created_at<p_end
 ) all_mappings;

 SELECT coalesce(jsonb_agg(to_jsonb(o)||jsonb_build_object(
  'kind','observation','source_time',o.observed_at,'available_at',greatest(o.ingested_at,r.received_at),
  'quality_events',(SELECT coalesce(jsonb_agg(jsonb_build_object('event_code',q.event_code,'created_at',q.created_at)
   ORDER BY q.event_code,q.created_at),'[]'::jsonb) FROM seagis.quality_event q WHERE q.observation_id=o.id AND q.created_at<p_end)
 ) ORDER BY o.id),'[]'::jsonb) INTO observations
 FROM seagis.observation o JOIN seagis_raw.raw_payload r ON r.id=o.raw_payload_id
 WHERE o.plot_id=p_plot AND o.is_synthetic=pl.is_synthetic AND o.observed_at<p_end AND o.ingested_at<p_end
 AND (o.observed_at>=p_start-interval '72 hours' OR o.id IN (
  SELECT DISTINCT ON (sensor_id) id FROM seagis.observation
  WHERE plot_id=p_plot AND observed_at<p_start-interval '72 hours' AND ingested_at<p_end
  ORDER BY sensor_id,observed_at DESC,id));

 SELECT coalesce(jsonb_agg(to_jsonb(v)||jsonb_build_object(
  'kind','forecast_value','source_time',v.valid_at,
  'available_at',greatest(v.ingested_at,r.ingested_at,raw.received_at,r.issued_at,r.model_initialized_at),
  'run_ingested_at',r.ingested_at,'issued_at',r.issued_at,'issue_time_basis',r.issue_time_basis,
  'model_initialized_at',r.model_initialized_at,'run_kind',r.run_kind,
  'quality_events',(SELECT coalesce(jsonb_agg(jsonb_build_object('event_code',q.event_code,'created_at',q.created_at)
   ORDER BY q.event_code,q.created_at),'[]'::jsonb) FROM seagis.quality_event q WHERE q.forecast_value_id=v.id AND q.created_at<p_end)
 ) ORDER BY v.id),'[]'::jsonb) INTO forecasts
 FROM seagis.forecast_value v JOIN seagis.forecast_run r ON r.id=v.forecast_run_id
 JOIN seagis_raw.raw_payload raw ON raw.id=r.raw_payload_id
 WHERE v.valid_at>=p_start-interval '72 hours' AND v.valid_at<p_end AND v.ingested_at<p_end
 AND v.source_grid_id IN (SELECT (m->>'source_grid_id')::uuid FROM jsonb_array_elements(mappings) m);

 IF jsonb_array_length(observations)+jsonb_array_length(forecasts)>20000 THEN
  RAISE EXCEPTION 'source_bundle_too_large'; END IF;
 result:=jsonb_build_object('schema_version','a3-source-1','plot',to_jsonb(pl),'start_at',p_start,'end_at',p_end,
  'sensors',(SELECT coalesce(jsonb_agg(to_jsonb(s) ORDER BY s.id),'[]'::jsonb) FROM seagis.sensor s WHERE s.plot_id=p_plot),
  'parameters',(SELECT jsonb_agg(to_jsonb(dp)||jsonb_build_object('scope',d.scope,
   'native_cadence_seconds',d.native_cadence_seconds,'stale_seconds',coalesce(pol.stale_seconds,7200),
   'attribution',d.attribution,'licence_url',d.licence_url) ORDER BY dp.dataset_key,dp.parameter_code)
   FROM seagis.dataset_parameter dp JOIN seagis.dataset d USING(dataset_key)
   LEFT JOIN seagis_environment.policy pol USING(dataset_key)),
  'mappings',mappings,'records',observations||forecasts);
 IF octet_length(result::text)>12000000 THEN RAISE EXCEPTION 'source_bundle_too_large'; END IF;
 RETURN result||jsonb_build_object('source_sha256',seagis.jsonb_sha256(result));
END $$;

CREATE FUNCTION seagis_quality.save_snapshot(document jsonb)
RETURNS jsonb LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog SET timezone='UTC' AS $$
DECLARE bundle jsonb; pl uuid; a timestamptz; b timestamptz; pol seagis_quality.policy; field text;
 row_data jsonb; cell jsonb; source jsonb; mapping jsonb; reference text; at_time timestamptz;
 snapshot uuid; manifest text; existing seagis_quality.alignment_snapshot; expected int;
BEGIN
 IF document->>'schema_version' IS DISTINCT FROM 'a3-alignment-1'
  OR document->>'mode' NOT IN ('demo_review','operational_review')
  OR document->'training_authorized' IS DISTINCT FROM 'false'::jsonb
  OR jsonb_typeof(document->'rows') IS DISTINCT FROM 'array'
  OR octet_length(document::text)>12000000 THEN RAISE EXCEPTION 'invalid_alignment_document'; END IF;
 pl:=(document->>'plot_id')::uuid; a:=(document->>'start_at')::timestamptz; b:=(document->>'end_at')::timestamptz;
 bundle:=seagis_quality.source_bundle(pl,a,b,document->>'mode'='demo_review');
 SELECT * INTO pol FROM seagis_quality.policy WHERE version=document->>'policy_version';
 IF NOT FOUND OR pol.policy_sha256 IS DISTINCT FROM document->>'policy_sha256'
  OR pol.code_sha256 IS DISTINCT FROM document->>'code_sha256'
  OR pol.definition->>'builder_version' IS DISTINCT FROM document->>'builder_version' THEN
  RAISE EXCEPTION 'unregistered_quality_policy_or_code'; END IF;
 IF bundle->>'source_sha256' IS DISTINCT FROM document->>'source_sha256' THEN
  RAISE EXCEPTION 'source_changed_rebuild_snapshot'; END IF;
 IF document->'source_registry' IS DISTINCT FROM bundle->'parameters'
  OR document->'sensor_deployments' IS DISTINCT FROM bundle->'sensors' THEN
  RAISE EXCEPTION 'source_registry_differs_from_bundle'; END IF;
 expected:=extract(epoch FROM b-a)::int/3600;
 IF jsonb_array_length(document->'rows')<>expected OR
  (SELECT count(DISTINCT (x->>'at')::timestamptz) FROM jsonb_array_elements(document->'rows') x)<>expected THEN
  RAISE EXCEPTION 'invalid_alignment_hours'; END IF;
 FOR row_data IN SELECT value FROM jsonb_array_elements(document->'rows') LOOP
  at_time:=(row_data->>'at')::timestamptz;
  IF at_time IS NULL OR at_time<a OR at_time>=b OR at_time<>date_trunc('hour',at_time)
   OR jsonb_array_length(row_data->'cells')<>jsonb_array_length(bundle->'parameters')
   OR (SELECT count(DISTINCT (x->>'dataset_key',x->>'parameter_code'))
       FROM jsonb_array_elements(row_data->'cells') x)<>jsonb_array_length(bundle->'parameters') THEN
   RAISE EXCEPTION 'invalid_alignment_cells'; END IF;
  FOR cell IN SELECT value FROM jsonb_array_elements(row_data->'cells') LOOP
   IF NOT EXISTS(SELECT 1 FROM jsonb_array_elements(bundle->'parameters') p
    WHERE p->>'dataset_key'=cell->>'dataset_key' AND p->>'parameter_code'=cell->>'parameter_code')
    OR jsonb_typeof(cell->'lineage') IS DISTINCT FROM 'array' THEN RAISE EXCEPTION 'unknown_alignment_parameter'; END IF;
   IF cell->>'source_id' IS NULL THEN
    IF jsonb_array_length(cell->'lineage')<>0 OR cell->'value' IS DISTINCT FROM 'null'::jsonb
     OR cell->>'value_status' IS DISTINCT FROM 'not_available' OR cell->'usable_context' IS DISTINCT FROM 'false'::jsonb
     THEN RAISE EXCEPTION 'invalid_empty_alignment_cell'; END IF;
   ELSIF NOT cell->'lineage' ? (cell->>'source_id') THEN RAISE EXCEPTION 'missing_selected_lineage'; END IF;
   FOR reference IN SELECT jsonb_array_elements_text(cell->'lineage') LOOP
    SELECT r INTO source FROM jsonb_array_elements(bundle->'records') r
     WHERE (r->>'kind')||':'||(r->>'id')=reference;
    IF NOT FOUND OR source->>'dataset_key' IS DISTINCT FROM cell->>'dataset_key'
     OR source->>'parameter_code' IS DISTINCT FROM cell->>'parameter_code'
     OR (source->>'source_time')::timestamptz>at_time OR (source->>'available_at')::timestamptz>at_time
     THEN RAISE EXCEPTION 'input_violates_scope_or_availability'; END IF;
    IF source->>'kind'='forecast_value' THEN
     SELECT m INTO mapping FROM jsonb_array_elements(bundle->'mappings') m
      WHERE m->>'mapping_key'=cell->'spatial'->>'mapping_key'
       AND m->>'source_grid_id'=source->>'source_grid_id'
       AND (m->>'recorded_at')::timestamptz<=at_time AND (m->>'effective_from')::timestamptz<=at_time
       AND (m->>'effective_until' IS NULL OR (m->>'effective_until')::timestamptz>at_time);
     IF NOT FOUND THEN RAISE EXCEPTION 'input_violates_grid_mapping'; END IF;
     FOREACH field IN ARRAY ARRAY['mapping_key','source_grid_id','distance_m','sampling_method',
      'representativeness','grid_latitude','grid_longitude','depth_m','resolution_lat_deg',
      'resolution_lon_deg','coordinate_status','recorded_at','effective_from','effective_until'] LOOP
      IF cell->'spatial'->field IS DISTINCT FROM mapping->field THEN
       RAISE EXCEPTION 'spatial_metadata_differs_from_source'; END IF;
     END LOOP;
    END IF;
    IF reference=cell->>'source_id' AND (
     cell->'value' IS DISTINCT FROM source->'value' OR cell->'native_value' IS DISTINCT FROM source->'native_value'
     OR cell->'native_unit' IS DISTINCT FROM source->'native_unit' OR cell->'unit' IS DISTINCT FROM source->'unit'
     OR cell->'value_status' IS DISTINCT FROM source->'value_status'
     OR cell->'is_synthetic' IS DISTINCT FROM source->'is_synthetic'
     OR (cell->>'source_time')::timestamptz IS DISTINCT FROM (source->>'source_time')::timestamptz
     OR (cell->>'available_at')::timestamptz IS DISTINCT FROM (source->>'available_at')::timestamptz) THEN
     RAISE EXCEPTION 'selected_value_differs_from_source'; END IF;
    IF reference=cell->>'source_id' THEN
     FOREACH field IN ARRAY ARRAY['source_grid_id','forecast_run_id','sensor_id','issued_at',
      'issue_time_basis','detection_limit'] LOOP
      IF coalesce(cell->field,'null'::jsonb) IS DISTINCT FROM coalesce(source->field,'null'::jsonb) THEN
       RAISE EXCEPTION 'selected_metadata_differs_from_source'; END IF;
     END LOOP;
     IF source->>'kind'='forecast_value' THEN
      FOREACH field IN ARRAY ARRAY['temporal_support','interval_status','period_start_at','period_end_at'] LOOP
       IF cell->field IS DISTINCT FROM source->field THEN RAISE EXCEPTION 'selected_metadata_differs_from_source'; END IF;
      END LOOP;
     END IF;
    END IF;
   END LOOP;
  END LOOP;
 END LOOP;
 SELECT encode(sha256(convert_to(coalesce(string_agg(x,E'\n' ORDER BY x),''),'UTF8')),'hex') INTO manifest
 FROM (SELECT DISTINCT (r->>'at')||'|'||ref x FROM jsonb_array_elements(document->'rows') r,
  jsonb_array_elements(r->'cells') c,jsonb_array_elements_text(c->'lineage') ref) inputs;
 INSERT INTO seagis_quality.alignment_snapshot(plot_id,mode,start_at,end_at,policy_version,source_sha256,input_manifest_sha256,body)
 VALUES(pl,document->>'mode',a,b,pol.version,document->>'source_sha256',manifest,document)
 ON CONFLICT DO NOTHING RETURNING id INTO snapshot;
 IF snapshot IS NULL THEN
  SELECT * INTO existing FROM seagis_quality.alignment_snapshot WHERE plot_id=pl AND mode=document->>'mode'
   AND start_at=a AND end_at=b AND policy_version=pol.version AND source_sha256=document->>'source_sha256';
  IF existing.body IS DISTINCT FROM document THEN RAISE EXCEPTION 'non_deterministic_alignment_output'; END IF;
  snapshot:=existing.id;
 ELSE
  INSERT INTO seagis_quality.snapshot_input(snapshot_id,aligned_at,source_ref,observation_id,forecast_value_id)
  SELECT DISTINCT snapshot,(r->>'at')::timestamptz,ref,
   CASE WHEN split_part(ref,':',1)='observation' THEN split_part(ref,':',2)::uuid END,
   CASE WHEN split_part(ref,':',1)='forecast_value' THEN split_part(ref,':',2)::uuid END
  FROM jsonb_array_elements(document->'rows') r,jsonb_array_elements(r->'cells') c,
   jsonb_array_elements_text(c->'lineage') ref;
 END IF;
 RETURN jsonb_build_object('snapshot_id',snapshot,'body_sha256',seagis.jsonb_sha256(document),
  'input_manifest_sha256',manifest,'hour_count',expected,
  'input_count',(SELECT count(*) FROM seagis_quality.snapshot_input WHERE snapshot_id=snapshot));
END $$;

CREATE FUNCTION seagis_quality.snapshot(identity uuid)
RETURNS jsonb LANGUAGE sql STABLE SECURITY DEFINER SET search_path=pg_catalog AS $$
 SELECT jsonb_build_object('snapshot_id',s.id,'created_at',s.created_at,'body_sha256',s.body_sha256,
  'input_manifest_sha256',s.input_manifest_sha256,'body',s.body)
 FROM seagis_quality.alignment_snapshot s WHERE s.id=identity
$$;

DO $$ DECLARE tb text; BEGIN
 FOREACH tb IN ARRAY ARRAY['policy','alignment_snapshot','snapshot_input'] LOOP
  EXECUTE format('ALTER TABLE seagis_quality.%I ENABLE ROW LEVEL SECURITY',tb);
  EXECUTE format('CREATE TRIGGER append_only BEFORE UPDATE OR DELETE ON seagis_quality.%I
   FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation()',tb);
 END LOOP;
END $$;
REVOKE ALL ON ALL TABLES IN SCHEMA seagis_quality FROM PUBLIC,anon,authenticated,service_role,seagis_quality_worker;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA seagis_quality FROM PUBLIC,anon,authenticated,service_role;
GRANT EXECUTE ON FUNCTION seagis_quality.source_bundle(uuid,timestamptz,timestamptz,boolean),
 seagis_quality.save_snapshot(jsonb),seagis_quality.snapshot(uuid) TO seagis_quality_worker;
