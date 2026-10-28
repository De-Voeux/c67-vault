-- A2 operations: distinguish provider update safeguards from schema failures.
CREATE OR REPLACE FUNCTION seagis_environment.finish_failure(lease uuid, code text)
RETURNS void LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE s seagis_environment.schedule_state;
BEGIN
 IF code NOT IN ('network_failure','rate_limited','auth_failure','schema_failure','storage_failure','licence_failure','timeout','provider_updating')
 THEN code:='schema_failure'; END IF;
 SELECT * INTO s FROM seagis_environment.schedule_state WHERE lease_id=lease FOR UPDATE;
 IF NOT FOUND THEN RAISE EXCEPTION 'lease_unavailable'; END IF;
 UPDATE seagis_environment.attempt SET status='failed',completed_at=clock_timestamp(),error_code=code WHERE id=lease AND status='running';
 UPDATE seagis_environment.schedule_state SET lease_id=NULL,lease_until=NULL,failures=failures+1,last_error_code=code,
  next_attempt_at=clock_timestamp()+make_interval(secs=>least(21600,900*power(2,least(failures,4)))::int)
 WHERE dataset_key=s.dataset_key;
END $$;

