-- A0 only. Reference catalogue plus private data contracts; no public API or live ingestion.
-- Apply transactionally. 0001 is the version; never rename an applied migration.
CREATE SCHEMA seagis;
CREATE SCHEMA seagis_raw;
CREATE SCHEMA seagis_features;
REVOKE ALL ON SCHEMA seagis, seagis_raw, seagis_features FROM PUBLIC, anon, authenticated;

CREATE DOMAIN seagis.finite_float AS double precision
  CHECK (VALUE > '-Infinity'::double precision AND VALUE < 'Infinity'::double precision);

CREATE TABLE seagis.source (
  source_key text PRIMARY KEY,
  provider text NOT NULL,
  documentation_url text NOT NULL
);

CREATE TABLE seagis.dataset (
  dataset_key text PRIMARY KEY,
  source_key text NOT NULL REFERENCES seagis.source,
  provider_product_id text,
  provider_dataset_id text NOT NULL,
  dataset_version text NOT NULL,
  scope text NOT NULL CHECK (scope IN ('local_sensor', 'regional_model')),
  native_cadence_seconds integer NOT NULL CHECK (native_cadence_seconds > 0),
  resolution_lat_deg seagis.finite_float CHECK (resolution_lat_deg > 0),
  resolution_lon_deg seagis.finite_float CHECK (resolution_lon_deg > 0),
  source_timezone text NOT NULL DEFAULT 'UTC',
  licence_url text NOT NULL,
  attribution text NOT NULL,
  raw_storage_permitted boolean NOT NULL DEFAULT false,
  real_ingestion_enabled boolean NOT NULL DEFAULT false,
  metadata_checked_at timestamptz NOT NULL,
  UNIQUE (dataset_key, scope)
);

CREATE TABLE seagis.parameter (
  parameter_code text PRIMARY KEY,
  unit text NOT NULL,
  description text NOT NULL,
  UNIQUE (parameter_code, unit)
);

CREATE TABLE seagis.dataset_parameter (
  dataset_key text NOT NULL REFERENCES seagis.dataset,
  parameter_code text NOT NULL,
  source_variable text NOT NULL,
  native_unit text NOT NULL,
  unit text NOT NULL,
  conversion_code text NOT NULL,
  conversion_factor seagis.finite_float NOT NULL DEFAULT 1 CHECK (conversion_factor <> 0),
  conversion_offset seagis.finite_float NOT NULL DEFAULT 0,
  temporal_support text NOT NULL CHECK (temporal_support IN ('instantaneous', 'mean', 'sum')),
  PRIMARY KEY (dataset_key, parameter_code),
  FOREIGN KEY (parameter_code, unit) REFERENCES seagis.parameter (parameter_code, unit),
  UNIQUE (dataset_key, parameter_code, native_unit, unit, conversion_code)
);

CREATE TABLE seagis.plot (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  plot_code text NOT NULL UNIQUE,
  name text NOT NULL,
  latitude seagis.finite_float CHECK (latitude BETWEEN -90 AND 90),
  longitude seagis.finite_float CHECK (longitude BETWEEN -180 AND 180),
  is_synthetic boolean NOT NULL,
  location_status text NOT NULL CHECK (location_status IN ('not_surveyed', 'surveyed', 'synthetic')),
  created_at timestamptz NOT NULL DEFAULT now(),
  CHECK ((latitude IS NULL) = (longitude IS NULL)),
  CHECK ((location_status = 'synthetic') = is_synthetic),
  CHECK (location_status <> 'surveyed' OR latitude IS NOT NULL),
  UNIQUE (id, is_synthetic)
);

CREATE TABLE seagis.sensor (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  sensor_code text NOT NULL UNIQUE,
  plot_id uuid NOT NULL,
  dataset_key text NOT NULL,
  scope text NOT NULL DEFAULT 'local_sensor' CHECK (scope = 'local_sensor'),
  parameter_code text NOT NULL DEFAULT 'water_temperature' CHECK (parameter_code = 'water_temperature'),
  depth_m seagis.finite_float CHECK (depth_m >= 0),
  depth_status text NOT NULL CHECK (depth_status IN ('unknown', 'measured', 'synthetic')),
  is_synthetic boolean NOT NULL,
  active boolean NOT NULL DEFAULT true,
  FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot (id, is_synthetic),
  FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset (dataset_key, scope),
  FOREIGN KEY (dataset_key, parameter_code) REFERENCES seagis.dataset_parameter,
  CHECK (depth_status <> 'unknown' OR depth_m IS NULL),
  CHECK (depth_status = 'unknown' OR depth_m IS NOT NULL),
  CHECK (depth_status <> 'synthetic' OR is_synthetic),
  UNIQUE (id, plot_id, dataset_key, is_synthetic)
);
CREATE UNIQUE INDEX one_active_temperature_sensor_per_plot ON seagis.sensor (plot_id) WHERE active;

CREATE TABLE seagis.ingestion_run (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  dataset_key text NOT NULL REFERENCES seagis.dataset,
  request_key text NOT NULL,
  adapter_version text NOT NULL,
  started_at timestamptz NOT NULL,
  completed_at timestamptz,
  status text NOT NULL CHECK (status IN ('running', 'succeeded', 'partial', 'failed')),
  is_synthetic boolean NOT NULL,
  error_code text,
  UNIQUE (dataset_key, request_key),
  UNIQUE (id, dataset_key, is_synthetic),
  CHECK (completed_at IS NULL OR completed_at >= started_at),
  CHECK ((status = 'running') = (completed_at IS NULL))
);

CREATE TABLE seagis_raw.raw_payload (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  ingestion_run_id uuid NOT NULL,
  dataset_key text NOT NULL,
  is_synthetic boolean NOT NULL,
  sha256 text NOT NULL CHECK (sha256 ~ '^[0-9a-f]{64}$'),
  hash_basis text NOT NULL DEFAULT 'source_bytes' CHECK (hash_basis IN ('source_bytes', 'synthetic_json_canonical_v1')),
  received_at timestamptz NOT NULL,
  storage_mode text NOT NULL CHECK (storage_mode IN ('inline', 'object', 'metadata_only')),
  payload jsonb,
  object_uri text,
  byte_size bigint NOT NULL CHECK (byte_size >= 0),
  format text NOT NULL,
  licence_snapshot text NOT NULL,
  provider_metadata jsonb NOT NULL DEFAULT '{}' CHECK (jsonb_typeof(provider_metadata) = 'object'),
  FOREIGN KEY (ingestion_run_id, dataset_key, is_synthetic)
    REFERENCES seagis.ingestion_run (id, dataset_key, is_synthetic),
  CHECK ((storage_mode = 'inline' AND payload IS NOT NULL AND object_uri IS NULL)
      OR (storage_mode = 'object' AND payload IS NULL AND object_uri IS NOT NULL AND object_uri LIKE 'storage://%')
      OR (storage_mode = 'metadata_only' AND payload IS NULL AND object_uri IS NULL)),
  CHECK (storage_mode <> 'inline' OR (is_synthetic AND hash_basis = 'synthetic_json_canonical_v1')),
  UNIQUE (ingestion_run_id, sha256),
  UNIQUE (id, ingestion_run_id, dataset_key, is_synthetic)
);

CREATE TABLE seagis.source_grid (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  dataset_key text NOT NULL,
  scope text NOT NULL DEFAULT 'regional_model' CHECK (scope = 'regional_model'),
  grid_key text NOT NULL,
  grid_version text NOT NULL,
  identity_basis text NOT NULL CHECK (identity_basis IN ('provider_cell', 'provider_returned_coordinate', 'synthetic')),
  latitude seagis.finite_float NOT NULL CHECK (latitude BETWEEN -90 AND 90),
  longitude seagis.finite_float NOT NULL CHECK (longitude BETWEEN -180 AND 180),
  depth_m seagis.finite_float NOT NULL CHECK (depth_m >= 0),
  is_synthetic boolean NOT NULL,
  FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset (dataset_key, scope),
  CHECK (identity_basis <> 'synthetic' OR is_synthetic),
  UNIQUE (dataset_key, grid_key, is_synthetic),
  UNIQUE (id, dataset_key, is_synthetic)
);

CREATE TABLE seagis.plot_grid_mapping (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  plot_id uuid NOT NULL,
  source_grid_id uuid NOT NULL REFERENCES seagis.source_grid,
  is_synthetic boolean NOT NULL,
  sampling_method text NOT NULL CHECK (sampling_method IN ('nearest_wet_cell', 'nearest_cell', 'provider_returned_coordinate', 'synthetic')),
  distance_m seagis.finite_float CHECK (distance_m >= 0),
  representativeness text NOT NULL CHECK (representativeness IN ('unverified', 'regional_only', 'land_mask_issue')),
  effective_from timestamptz NOT NULL,
  effective_until timestamptz,
  FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot (id, is_synthetic),
  CHECK (effective_until IS NULL OR effective_until > effective_from),
  UNIQUE (plot_id, source_grid_id, effective_from)
);
CREATE INDEX mapping_grid_plot ON seagis.plot_grid_mapping (source_grid_id, plot_id);

CREATE FUNCTION seagis.valid_value(v double precision, native double precision, status text, lim double precision)
RETURNS boolean LANGUAGE sql IMMUTABLE SET search_path = pg_catalog AS $$
  SELECT CASE WHEN status = 'present' THEN v IS NOT NULL AND native IS NOT NULL AND lim IS NULL
    WHEN status = 'below_detection_limit' THEN v IS NULL AND native IS NULL AND lim IS NOT NULL AND lim >= 0
    WHEN status IN ('missing', 'not_available') THEN v IS NULL AND native IS NULL AND lim IS NULL
    ELSE false END
$$;

CREATE FUNCTION seagis.valid_support(t timestamptz, support text, status text, a timestamptz, b timestamptz)
RETURNS boolean LANGUAGE sql IMMUTABLE SET search_path = pg_catalog AS $$
  SELECT CASE WHEN support = 'instantaneous' THEN status = 'not_applicable' AND a IS NULL AND b IS NULL
    WHEN support IN ('mean', 'sum') AND status = 'unknown' THEN a IS NULL AND b IS NULL
    WHEN support IN ('mean', 'sum') AND status = 'known' THEN a IS NOT NULL AND b IS NOT NULL AND a < b AND t BETWEEN a AND b
    ELSE false END
$$;

CREATE TABLE seagis.observation (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  plot_id uuid NOT NULL,
  sensor_id uuid NOT NULL,
  dataset_key text NOT NULL,
  ingestion_run_id uuid NOT NULL,
  raw_payload_id uuid NOT NULL,
  is_synthetic boolean NOT NULL,
  source_record_key text NOT NULL,
  parameter_code text NOT NULL CHECK (parameter_code = 'water_temperature'),
  native_value seagis.finite_float,
  native_unit text NOT NULL,
  value seagis.finite_float,
  unit text NOT NULL,
  conversion_code text NOT NULL,
  value_status text NOT NULL,
  detection_limit seagis.finite_float,
  observed_at timestamptz NOT NULL,
  ingested_at timestamptz NOT NULL,
  quality_status text NOT NULL CHECK (quality_status IN ('unreviewed', 'accepted', 'suspect', 'rejected')),
  FOREIGN KEY (sensor_id, plot_id, dataset_key, is_synthetic) REFERENCES seagis.sensor (id, plot_id, dataset_key, is_synthetic),
  FOREIGN KEY (raw_payload_id, ingestion_run_id, dataset_key, is_synthetic)
    REFERENCES seagis_raw.raw_payload (id, ingestion_run_id, dataset_key, is_synthetic),
  FOREIGN KEY (dataset_key, parameter_code, native_unit, unit, conversion_code)
    REFERENCES seagis.dataset_parameter (dataset_key, parameter_code, native_unit, unit, conversion_code),
  CHECK (seagis.valid_value(value, native_value, value_status, detection_limit)),
  UNIQUE (sensor_id, parameter_code, source_record_key),
  UNIQUE (id, ingestion_run_id, dataset_key, is_synthetic)
);
CREATE INDEX observation_plot_time ON seagis.observation (plot_id, parameter_code, observed_at DESC);
CREATE INDEX observation_ingestion ON seagis.observation (ingestion_run_id);

CREATE TABLE seagis.forecast_run (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  dataset_key text NOT NULL,
  scope text NOT NULL DEFAULT 'regional_model' CHECK (scope = 'regional_model'),
  ingestion_run_id uuid NOT NULL,
  raw_payload_id uuid NOT NULL,
  is_synthetic boolean NOT NULL,
  run_key text NOT NULL,
  run_kind text NOT NULL CHECK (run_kind IN ('forecast', 'analysis')),
  provider_run_id text,
  model_initialized_at timestamptz,
  issued_at timestamptz,
  issue_time_basis text NOT NULL CHECK (issue_time_basis IN ('provider_verified', 'unknown')),
  ingested_at timestamptz NOT NULL,
  FOREIGN KEY (dataset_key, scope) REFERENCES seagis.dataset (dataset_key, scope),
  FOREIGN KEY (raw_payload_id, ingestion_run_id, dataset_key, is_synthetic)
    REFERENCES seagis_raw.raw_payload (id, ingestion_run_id, dataset_key, is_synthetic),
  CHECK ((issue_time_basis = 'unknown') = (issued_at IS NULL)),
  CHECK (issued_at IS NULL OR issued_at <= ingested_at),
  CHECK (model_initialized_at IS NULL OR model_initialized_at <= ingested_at),
  UNIQUE (dataset_key, run_key),
  UNIQUE (id, dataset_key, is_synthetic)
);
CREATE INDEX forecast_run_asof ON seagis.forecast_run (dataset_key, ingested_at DESC);

CREATE TABLE seagis.forecast_value (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  forecast_run_id uuid NOT NULL,
  source_grid_id uuid NOT NULL,
  dataset_key text NOT NULL,
  is_synthetic boolean NOT NULL,
  parameter_code text NOT NULL,
  native_value seagis.finite_float,
  native_unit text NOT NULL,
  value seagis.finite_float,
  unit text NOT NULL,
  conversion_code text NOT NULL,
  value_status text NOT NULL,
  detection_limit seagis.finite_float,
  valid_at timestamptz NOT NULL,
  ingested_at timestamptz NOT NULL,
  temporal_support text NOT NULL,
  interval_status text NOT NULL,
  period_start_at timestamptz,
  period_end_at timestamptz,
  quality_status text NOT NULL CHECK (quality_status IN ('unreviewed', 'accepted', 'suspect', 'rejected')),
  FOREIGN KEY (forecast_run_id, dataset_key, is_synthetic) REFERENCES seagis.forecast_run (id, dataset_key, is_synthetic),
  FOREIGN KEY (source_grid_id, dataset_key, is_synthetic) REFERENCES seagis.source_grid (id, dataset_key, is_synthetic),
  FOREIGN KEY (dataset_key, parameter_code, native_unit, unit, conversion_code)
    REFERENCES seagis.dataset_parameter (dataset_key, parameter_code, native_unit, unit, conversion_code),
  CHECK (seagis.valid_value(value, native_value, value_status, detection_limit)),
  CHECK (seagis.valid_support(valid_at, temporal_support, interval_status, period_start_at, period_end_at)),
  UNIQUE (forecast_run_id, source_grid_id, parameter_code, valid_at),
  UNIQUE (id, dataset_key, is_synthetic)
);
CREATE INDEX forecast_grid_time ON seagis.forecast_value (source_grid_id, parameter_code, valid_at DESC);

CREATE TABLE seagis.quality_event (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  ingestion_run_id uuid NOT NULL,
  dataset_key text NOT NULL,
  is_synthetic boolean NOT NULL,
  event_key text NOT NULL,
  observation_id uuid,
  forecast_value_id uuid,
  event_code text NOT NULL,
  severity text NOT NULL CHECK (severity IN ('info', 'warning', 'error')),
  details jsonb NOT NULL DEFAULT '{}' CHECK (jsonb_typeof(details) = 'object'),
  created_at timestamptz NOT NULL DEFAULT now(),
  FOREIGN KEY (ingestion_run_id, dataset_key, is_synthetic) REFERENCES seagis.ingestion_run (id, dataset_key, is_synthetic),
  FOREIGN KEY (observation_id, ingestion_run_id, dataset_key, is_synthetic)
    REFERENCES seagis.observation (id, ingestion_run_id, dataset_key, is_synthetic),
  FOREIGN KEY (forecast_value_id, dataset_key, is_synthetic) REFERENCES seagis.forecast_value (id, dataset_key, is_synthetic),
  CHECK (num_nonnulls(observation_id, forecast_value_id) <= 1),
  UNIQUE (ingestion_run_id, event_key)
);
CREATE INDEX quality_event_observation ON seagis.quality_event (observation_id) WHERE observation_id IS NOT NULL;
CREATE INDEX quality_event_forecast ON seagis.quality_event (forecast_value_id) WHERE forecast_value_id IS NOT NULL;

-- Fixed UTF-8 encoding and jsonb serialization are deterministic within this DB version.
CREATE FUNCTION seagis.jsonb_sha256(value jsonb) RETURNS text
LANGUAGE sql IMMUTABLE STRICT SET search_path = pg_catalog AS $$
  SELECT encode(sha256(convert_to(value::text, 'UTF8')), 'hex')
$$;

CREATE TABLE seagis_features.feature_snapshot (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  plot_id uuid NOT NULL,
  is_synthetic boolean NOT NULL,
  as_of timestamptz NOT NULL,
  generated_at timestamptz NOT NULL,
  feature_version text NOT NULL,
  feature_schema_version text NOT NULL,
  features jsonb NOT NULL CHECK (jsonb_typeof(features) = 'object'),
  missing_context text[] NOT NULL DEFAULT '{}',
  status text NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'sealed')),
  input_manifest_sha256 text CHECK (input_manifest_sha256 ~ '^[0-9a-f]{64}$'),
  features_sha256 text GENERATED ALWAYS AS (seagis.jsonb_sha256(features)) STORED,
  FOREIGN KEY (plot_id, is_synthetic) REFERENCES seagis.plot (id, is_synthetic),
  CHECK (generated_at >= as_of),
  CHECK ((status = 'draft') = (input_manifest_sha256 IS NULL)),
  UNIQUE (plot_id, as_of, feature_version, input_manifest_sha256)
);

CREATE TABLE seagis_features.feature_input (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  snapshot_id uuid NOT NULL REFERENCES seagis_features.feature_snapshot,
  observation_id uuid REFERENCES seagis.observation,
  forecast_value_id uuid REFERENCES seagis.forecast_value,
  CHECK (num_nonnulls(observation_id, forecast_value_id) = 1)
);
CREATE UNIQUE INDEX feature_input_observation ON seagis_features.feature_input (snapshot_id, observation_id) WHERE observation_id IS NOT NULL;
CREATE UNIQUE INDEX feature_input_forecast ON seagis_features.feature_input (snapshot_id, forecast_value_id) WHERE forecast_value_id IS NOT NULL;

CREATE FUNCTION seagis.reject_mutation() RETURNS trigger LANGUAGE plpgsql SET search_path = pg_catalog AS $$
BEGIN RAISE EXCEPTION '% is append-only; create a new record or revision', TG_TABLE_NAME USING ERRCODE = '23514'; END
$$;

CREATE FUNCTION seagis.guard_ingestion() RETURNS trigger LANGUAGE plpgsql SET search_path = pg_catalog AS $$
BEGIN
  IF NOT NEW.is_synthetic AND NOT (SELECT real_ingestion_enabled FROM seagis.dataset WHERE dataset_key = NEW.dataset_key) THEN
    RAISE EXCEPTION 'Real ingestion is disabled for this dataset' USING ERRCODE = '23514';
  END IF;
  IF TG_OP = 'UPDATE' AND ROW(NEW.id,NEW.dataset_key,NEW.request_key,NEW.adapter_version,NEW.started_at,NEW.is_synthetic)
      IS DISTINCT FROM ROW(OLD.id,OLD.dataset_key,OLD.request_key,OLD.adapter_version,OLD.started_at,OLD.is_synthetic) THEN
    RAISE EXCEPTION 'Ingestion identity cannot change' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END $$;
CREATE TRIGGER guard_ingestion BEFORE INSERT OR UPDATE ON seagis.ingestion_run FOR EACH ROW EXECUTE FUNCTION seagis.guard_ingestion();

CREATE FUNCTION seagis.guard_dataset_identity() RETURNS trigger LANGUAGE plpgsql SET search_path = pg_catalog AS $$
BEGIN
  IF (to_jsonb(NEW) - 'raw_storage_permitted' - 'real_ingestion_enabled') IS DISTINCT FROM
      (to_jsonb(OLD) - 'raw_storage_permitted' - 'real_ingestion_enabled') THEN
    RAISE EXCEPTION 'Create a new versioned dataset to change provenance or cadence' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END $$;
CREATE TRIGGER guard_dataset_identity BEFORE UPDATE ON seagis.dataset FOR EACH ROW EXECUTE FUNCTION seagis.guard_dataset_identity();

CREATE FUNCTION seagis.guard_sensor_deployment() RETURNS trigger LANGUAGE plpgsql SET search_path = pg_catalog AS $$
BEGIN
  IF (to_jsonb(NEW) - 'active') IS DISTINCT FROM (to_jsonb(OLD) - 'active') THEN
    RAISE EXCEPTION 'Create a new sensor deployment to change plot or depth' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END $$;
CREATE TRIGGER guard_sensor_deployment BEFORE UPDATE ON seagis.sensor FOR EACH ROW EXECUTE FUNCTION seagis.guard_sensor_deployment();

CREATE FUNCTION seagis.guard_raw() RETURNS trigger LANGUAGE plpgsql SET search_path = pg_catalog AS $$
BEGIN
  IF NEW.received_at < (SELECT started_at FROM seagis.ingestion_run WHERE id = NEW.ingestion_run_id) THEN
    RAISE EXCEPTION 'Raw receipt predates ingestion start' USING ERRCODE = '23514';
  END IF;
  IF NOT NEW.is_synthetic AND NEW.storage_mode <> 'metadata_only' AND NOT
      (SELECT raw_storage_permitted FROM seagis.dataset WHERE dataset_key = NEW.dataset_key) THEN
    RAISE EXCEPTION 'Raw retention is not permitted for this dataset' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END $$;
CREATE TRIGGER guard_raw BEFORE INSERT ON seagis_raw.raw_payload FOR EACH ROW EXECUTE FUNCTION seagis.guard_raw();

CREATE FUNCTION seagis.guard_measurement() RETURNS trigger LANGUAGE plpgsql SET search_path = pg_catalog AS $$
DECLARE p seagis.dataset_parameter; available timestamptz;
BEGIN
  SELECT * INTO p FROM seagis.dataset_parameter WHERE dataset_key = NEW.dataset_key AND parameter_code = NEW.parameter_code;
  IF NEW.value IS NOT NULL AND NEW.native_value IS NOT NULL AND
      abs(NEW.value - (NEW.native_value * p.conversion_factor + p.conversion_offset)) > 1e-8 * greatest(1,abs(NEW.value)) THEN
    RAISE EXCEPTION 'Normalized value does not match declared conversion' USING ERRCODE = '23514';
  END IF;
  IF TG_TABLE_NAME = 'observation' THEN
    SELECT received_at INTO available FROM seagis_raw.raw_payload WHERE id = NEW.raw_payload_id;
  ELSE
    SELECT ingested_at INTO available FROM seagis.forecast_run WHERE id = NEW.forecast_run_id;
    IF NEW.temporal_support <> p.temporal_support THEN
      RAISE EXCEPTION 'Temporal support differs from dataset contract' USING ERRCODE = '23514';
    END IF;
    IF NEW.parameter_code = 'precipitation' AND
       (NEW.interval_status <> 'known' OR NEW.period_start_at IS NULL OR NEW.period_end_at IS NULL
        OR NEW.period_end_at <> NEW.valid_at OR NEW.period_end_at - NEW.period_start_at <> interval '1 hour') THEN
      RAISE EXCEPTION 'Precipitation must cover the preceding hour' USING ERRCODE = '23514';
    END IF;
  END IF;
  IF NEW.ingested_at < available THEN RAISE EXCEPTION 'Availability cannot predate upstream receipt' USING ERRCODE = '23514'; END IF;
  RETURN NEW;
END $$;
CREATE TRIGGER guard_observation BEFORE INSERT ON seagis.observation FOR EACH ROW EXECUTE FUNCTION seagis.guard_measurement();
CREATE TRIGGER guard_forecast_value BEFORE INSERT ON seagis.forecast_value FOR EACH ROW EXECUTE FUNCTION seagis.guard_measurement();

CREATE FUNCTION seagis.guard_run() RETURNS trigger LANGUAGE plpgsql SET search_path = pg_catalog AS $$
BEGIN
  IF NEW.ingested_at < (SELECT received_at FROM seagis_raw.raw_payload WHERE id = NEW.raw_payload_id) THEN
    RAISE EXCEPTION 'Forecast availability predates receipt' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END $$;
CREATE TRIGGER guard_run BEFORE INSERT ON seagis.forecast_run FOR EACH ROW EXECUTE FUNCTION seagis.guard_run();

CREATE FUNCTION seagis.guard_mapping() RETURNS trigger LANGUAGE plpgsql SET search_path = pg_catalog AS $$
BEGIN
  IF NEW.is_synthetic IS DISTINCT FROM (SELECT is_synthetic FROM seagis.source_grid WHERE id = NEW.source_grid_id) THEN
    RAISE EXCEPTION 'Synthetic and real grid mappings cannot mix' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END $$;
CREATE TRIGGER guard_mapping BEFORE INSERT OR UPDATE ON seagis.plot_grid_mapping FOR EACH ROW EXECUTE FUNCTION seagis.guard_mapping();

CREATE FUNCTION seagis.guard_quality_event() RETURNS trigger LANGUAGE plpgsql SET search_path = pg_catalog AS $$
BEGIN
  IF NEW.forecast_value_id IS NOT NULL AND NEW.ingestion_run_id IS DISTINCT FROM
      (SELECT r.ingestion_run_id FROM seagis.forecast_value v JOIN seagis.forecast_run r ON r.id = v.forecast_run_id WHERE v.id = NEW.forecast_value_id) THEN
    RAISE EXCEPTION 'QC event ingestion differs from forecast provenance' USING ERRCODE = '23514';
  END IF;
  RETURN NEW;
END $$;
CREATE TRIGGER guard_quality BEFORE INSERT ON seagis.quality_event FOR EACH ROW EXECUTE FUNCTION seagis.guard_quality_event();

CREATE FUNCTION seagis_features.guard_input() RETURNS trigger LANGUAGE plpgsql SET search_path = pg_catalog AS $$
DECLARE s seagis_features.feature_snapshot; o seagis.observation; v seagis.forecast_value; r seagis.forecast_run;
BEGIN
  -- Lock parent to serialize input inserts with sealing.
  SELECT * INTO s FROM seagis_features.feature_snapshot WHERE id = NEW.snapshot_id FOR UPDATE;
  IF s.status <> 'draft' THEN RAISE EXCEPTION 'Snapshot is sealed' USING ERRCODE = '23514'; END IF;
  IF NEW.observation_id IS NOT NULL THEN
    SELECT * INTO o FROM seagis.observation WHERE id = NEW.observation_id;
    IF o.plot_id <> s.plot_id OR o.is_synthetic <> s.is_synthetic OR o.observed_at > s.as_of OR o.ingested_at > s.as_of THEN
      RAISE EXCEPTION 'Observation violates plot, synthetic, or as-of boundary' USING ERRCODE = '23514';
    END IF;
  ELSIF NEW.forecast_value_id IS NOT NULL THEN
    SELECT * INTO v FROM seagis.forecast_value WHERE id = NEW.forecast_value_id;
    SELECT * INTO r FROM seagis.forecast_run WHERE id = v.forecast_run_id;
    IF v.is_synthetic <> s.is_synthetic OR v.ingested_at > s.as_of OR r.ingested_at > s.as_of OR r.issued_at > s.as_of
       OR NOT EXISTS (SELECT 1 FROM seagis.plot_grid_mapping m WHERE m.plot_id = s.plot_id AND m.source_grid_id = v.source_grid_id
          AND m.effective_from <= s.as_of AND (m.effective_until IS NULL OR m.effective_until > s.as_of)) THEN
      RAISE EXCEPTION 'Forecast violates availability or grid-mapping boundary' USING ERRCODE = '23514';
    END IF;
  END IF;
  RETURN NEW;
END $$;
CREATE TRIGGER guard_feature_input BEFORE INSERT ON seagis_features.feature_input FOR EACH ROW EXECUTE FUNCTION seagis_features.guard_input();

CREATE FUNCTION seagis_features.manifest_hash(snapshot uuid) RETURNS text LANGUAGE sql STABLE SET search_path = pg_catalog AS $$
  SELECT encode(sha256(convert_to(string_agg(
    CASE WHEN observation_id IS NOT NULL THEN 'observation:' || observation_id ELSE 'forecast_value:' || forecast_value_id END,
    E'\n' ORDER BY CASE WHEN observation_id IS NOT NULL THEN 'observation:' || observation_id ELSE 'forecast_value:' || forecast_value_id END
  ), 'UTF8')), 'hex') FROM seagis_features.feature_input WHERE snapshot_id = snapshot
$$;

CREATE FUNCTION seagis_features.guard_snapshot() RETURNS trigger LANGUAGE plpgsql SET search_path = pg_catalog AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    IF NEW.status <> 'draft' THEN RAISE EXCEPTION 'Create a draft before attaching inputs' USING ERRCODE = '23514'; END IF;
  ELSE
    IF OLD.status <> 'draft' OR NEW.status <> 'sealed' OR
       (to_jsonb(NEW) - 'status' - 'input_manifest_sha256' - 'features_sha256') IS DISTINCT FROM (to_jsonb(OLD) - 'status' - 'input_manifest_sha256' - 'features_sha256') OR
       NEW.input_manifest_sha256 IS NULL OR NEW.input_manifest_sha256 IS DISTINCT FROM seagis_features.manifest_hash(OLD.id) THEN
      RAISE EXCEPTION 'Only sealing with the exact nonempty input manifest is allowed' USING ERRCODE = '23514';
    END IF;
  END IF;
  RETURN NEW;
END $$;
CREATE TRIGGER guard_snapshot BEFORE INSERT OR UPDATE ON seagis_features.feature_snapshot FOR EACH ROW EXECUTE FUNCTION seagis_features.guard_snapshot();

-- No client grants, no exposed Data API schema. Worker roles are an A1 deployment decision.
DO $$
DECLARE ns text; t record;
BEGIN
  FOREACH ns IN ARRAY ARRAY['seagis','seagis_raw','seagis_features'] LOOP
    EXECUTE format('REVOKE ALL ON ALL TABLES IN SCHEMA %I FROM PUBLIC, anon, authenticated', ns);
    EXECUTE format('REVOKE ALL ON ALL FUNCTIONS IN SCHEMA %I FROM PUBLIC, anon, authenticated', ns);
    EXECUTE format('GRANT USAGE ON SCHEMA %I TO service_role', ns);
    EXECUTE format('REVOKE ALL ON ALL TABLES IN SCHEMA %I FROM service_role', ns);
    EXECUTE format('GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA %I TO service_role', ns);
    EXECUTE format('GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA %I TO service_role', ns);
    EXECUTE format('ALTER DEFAULT PRIVILEGES IN SCHEMA %I REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC', ns);
  END LOOP;
  FOR t IN SELECT schemaname, tablename FROM pg_tables WHERE schemaname IN ('seagis','seagis_raw','seagis_features') LOOP
    EXECUTE format('ALTER TABLE %I.%I ENABLE ROW LEVEL SECURITY', t.schemaname, t.tablename);
    EXECUTE format('CREATE POLICY backend_only ON %I.%I TO service_role USING (true) WITH CHECK (true)', t.schemaname, t.tablename);
  END LOOP;
  FOR t IN SELECT * FROM (VALUES ('seagis_raw','raw_payload'),('seagis','observation'),('seagis','forecast_run'),
      ('seagis','forecast_value'),('seagis','quality_event'),('seagis','dataset_parameter'),
      ('seagis','source_grid'),('seagis_features','feature_input')) AS x(ns,tb) LOOP
    EXECUTE format('CREATE TRIGGER append_only BEFORE UPDATE OR DELETE ON %I.%I FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation()', t.ns, t.tb);
  END LOOP;
END $$;
CREATE TRIGGER no_snapshot_delete BEFORE DELETE ON seagis_features.feature_snapshot FOR EACH ROW EXECUTE FUNCTION seagis.reject_mutation();

-- Reference catalogue, verified 2026-10-21. All live-ingestion switches stay off in A0.
INSERT INTO seagis.source VALUES
 ('sensor','SEAGIS local sensor / simulator','https://github.com/De-Voeux/Seagis-Model'),
 ('copernicus','E.U. Copernicus Marine Service / Mercator Ocean International','https://data.marine.copernicus.eu/'),
 ('open_meteo','Open-Meteo / NOAA GFS','https://open-meteo.com/en/docs/gfs-api');

INSERT INTO seagis.dataset (dataset_key,source_key,provider_product_id,provider_dataset_id,dataset_version,scope,native_cadence_seconds,resolution_lat_deg,resolution_lon_deg,licence_url,attribution,metadata_checked_at) VALUES
 ('sensor_temperature_v1','sensor',NULL,'seagis-water-temperature','v1','local_sensor',3600,NULL,NULL,'project-owned://sensor-data','SEAGIS; simulated until hardware commissioning','2026-10-21T00:00:00Z'),
 ('cmems_salinity_6h','copernicus','GLOBAL_ANALYSISFORECAST_PHY_001_024','cmems_mod_glo_phy-so_anfc_0.083deg_PT6H-i','202406','regional_model',21600,0.08333333333333333,0.08333333804392655,'https://marine.copernicus.eu/user-corner/service-commitments-and-licence','E.U. Copernicus Marine Service Information; product DOI 10.48670/moi-00016','2026-10-21T00:00:00Z'),
 ('cmems_currents_6h','copernicus','GLOBAL_ANALYSISFORECAST_PHY_001_024','cmems_mod_glo_phy-cur_anfc_0.083deg_PT6H-i','202406','regional_model',21600,0.08333333333333333,0.08333333804392655,'https://marine.copernicus.eu/user-corner/service-commitments-and-licence','E.U. Copernicus Marine Service Information; product DOI 10.48670/moi-00016','2026-10-21T00:00:00Z'),
 ('cmems_nutrients_daily','copernicus','GLOBAL_ANALYSISFORECAST_BGC_001_028','cmems_mod_glo_bgc-nut_anfc_0.25deg_P1D-m','202311','regional_model',86400,0.25,0.25,'https://marine.copernicus.eu/user-corner/service-commitments-and-licence','E.U. Copernicus Marine Service Information; product DOI 10.48670/moi-00015','2026-10-21T00:00:00Z'),
 ('open_meteo_gfs','open_meteo',NULL,'gfs_global','runtime_metadata_required','regional_model',3600,NULL,NULL,'https://open-meteo.com/en/terms','Weather data by Open-Meteo.com; NOAA GFS; CC BY 4.0 data, API entitlement separate','2026-10-21T00:00:00Z');

INSERT INTO seagis.parameter VALUES
 ('water_temperature','degC','Submerged local sensor temperature; distinct from air temperature'),
 ('salinity','1e-3','Provider-reported sea_water_salinity; PSU/ppt equivalence not assumed'),
 ('current_eastward','m/s','Eastward sea water velocity'),
 ('current_northward','m/s','Northward sea water velocity'),
 ('nitrate','mmol/m3','Mole concentration of nitrate, not mg/L'),
 ('phosphate','mmol/m3','Mole concentration of phosphate, not mg/L'),
 ('precipitation','mm','Preceding-hour atmospheric precipitation total'),
 ('wind_speed_10m','m/s','Wind speed at 10 m above ground'),
 ('wind_direction_10m','degree','Meteorological direction from which wind blows'),
 ('cloud_cover','percent','Cloud cover area fraction in percent'),
 ('uv_index','1','Dimensionless UV index'),
 ('air_temperature_2m','degC','Air temperature 2 m above ground; not water temperature');

INSERT INTO seagis.dataset_parameter (dataset_key,parameter_code,source_variable,native_unit,unit,conversion_code,temporal_support) VALUES
 ('sensor_temperature_v1','water_temperature','water_temperature','degC','degC','identity','instantaneous'),
 ('cmems_salinity_6h','salinity','so','1e-3','1e-3','identity','instantaneous'),
 ('cmems_currents_6h','current_eastward','uo','m s-1','m/s','unit_notation','instantaneous'),
 ('cmems_currents_6h','current_northward','vo','m s-1','m/s','unit_notation','instantaneous'),
 ('cmems_nutrients_daily','nitrate','no3','mmol m-3','mmol/m3','unit_notation','mean'),
 ('cmems_nutrients_daily','phosphate','po4','mmol m-3','mmol/m3','unit_notation','mean'),
 ('open_meteo_gfs','precipitation','precipitation','mm','mm','identity','sum'),
 ('open_meteo_gfs','wind_speed_10m','wind_speed_10m','m/s','m/s','identity','instantaneous'),
 ('open_meteo_gfs','wind_direction_10m','wind_direction_10m','°','degree','unit_notation','instantaneous'),
 ('open_meteo_gfs','cloud_cover','cloud_cover','%','percent','unit_notation','instantaneous'),
 ('open_meteo_gfs','uv_index','uv_index','','1','unit_notation','instantaneous'),
 ('open_meteo_gfs','air_temperature_2m','temperature_2m','°C','degC','unit_notation','instantaneous');
