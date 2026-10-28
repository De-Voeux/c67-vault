# DATA_FLOW

Version: 1.0.0 | Date: 2026-10-27

[Complete document](../DATABASE_DOCUMENTATION.md) | [README](../../README.md)

PostgreSQL/Supabase is the backend persistence defined by code. Schema `seagis` owns registries, observations, forecasts and provenance; `seagis_raw` holds raw manifests; `seagis_api` bounds the IoT gateway; `seagis_environment` manages regional workers; `seagis_quality` stores QC reviews; `seagis_features` supplies containers not connected to a production feature builder. Supabase internal schemas such as auth/storage are not inventoried as application-owned: current catalog access is unavailable and they must not be assumed empty.

Python retrieves provider data outside the database. A2/A3 workers call stored functions through psycopg; the TypeScript handler invokes only ingest/history/status functions. No ORM was found on these paths. Mutation transactions live in SQL functions; fetch claiming is a separate transaction from persistence so network calls do not hold a database transaction.

The diagram contains disconnected components: the iOS mock has no backend edge. Future integration remains UNVERIFIED. Production Core ML, distributed caches, warehouses, queues and search indexes were NOT FOUND in inspected implementation files; that does not establish absence of services outside these checkouts.

Reproducible diagram: `assets/diagrams/architecture.mmd`.


```mermaid
flowchart TD
    sensor["IoT / simulator"]
    edge["temperature handler"]
    sql["PostgreSQL / 6 schemas"]
    providers["Copernicus + Open-Meteo"]
    a2["A2 adapters + leases"]
    a3["A3 quality / alignment"]
    csv["CSV experiments"]
    ios["iOS synthetic mock"]
    sensor --> edge
    edge --> sql
    providers --> a2
    a2 --> sql
    sql --> a3
    a3 --> csv
```

Reproducible diagram: `assets/diagrams/lineage.mmd`.


```mermaid
flowchart TD
    registry["source + dataset_parameter"]
    raw["ingestion_run + raw_payload"]
    obs["observation"]
    run["forecast_run + forecast_value"]
    map["source_grid + mappings"]
    bundle["source_bundle"]
    align["alignment_snapshot + snapshot_input"]
    registry --> raw
    raw --> obs
    raw --> run
    map --> run
    obs --> bundle
    run --> bundle
    bundle --> align
```

