# DATA_CONTRACTS

Version: 1.0.0 | Date: 2026-10-27

[Complete document](../DATABASE_DOCUMENTATION.md) | [README](../../README.md)

Four contracts are explicit JSON Schemas; seven additional contracts are implementation-derived. This classification does not make them all public endpoints. No general version negotiation was found; mismatched constant versions/schemas are rejected. Breaking changes need a new version and consumer review, not assumed automatic compatibility. JSON errors below come from handler/SQL, not an invented standard error format.

| ID | Contract | Producer | Consumer | Interface | Class | Database | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C01 | A0 source envelope | fixture/provider logical extract | validate_source | JSON / Draft 2020-12 | explicit | seagis.ingestion_run + seagis_raw.raw_payload | `Seagis-Model/scripts/validate_contracts.py:1` |
| C02 | A0 normalized envelope | fixture normalization | validate_normalized + SQL guards | JSON / Draft 2020-12 | explicit | observation / forecast_run / forecast_value / source_grid | `Seagis-Model/scripts/validate_contracts.py:1` |
| C03 | A1 device packet | device/simulator | temperature handler + seagis_api.ingest | JSON / HTTP POST | explicit | observation + raw_payload + packet_receipt + quality_event | `Seagis-Model/supabase/functions/temperature/handler.ts:1` |
| C04 | A3 alignment document | scripts/quality/alignment.py::build | seagis_quality.save_snapshot | JSON / SQL jsonb | explicit | seagis_quality.alignment_snapshot + snapshot_input | `Seagis-Model/scripts/curate_environment.py:1` |
| C05 | A1 history/status/replies | seagis_api.history/status/reply | authorized reader | JSON / HTTP GET | implementation-derived | observation + sensor + packet_receipt | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:1` |
| C06 | A2 adapter batch/lease | Adapter.envelope + claim | seagis_environment.persist | JSON / SQL jsonb | implementation-derived | raw_payload + forecast_run + forecast_value + source_grid + demo_grid_mapping | `Seagis-Model/scripts/environmental/common.py:1` |
| C07 | A3 source_bundle | seagis_quality.source_bundle | build / CSV exporter | JSON / SQL jsonb | implementation-derived | plot + sensor + dataset_parameter + mappings + observation + forecast_value | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:1` |
| C08 | CSV experiment-csv-2 | export_experiment_csv.py::export | offline experiments / developer | CSV + JSON manifest | implementation-derived | derived files; no database writes | `Seagis-Model/scripts/export_experiment_csv.py:1` |
| C09 | iOS Assessment domain | MockAssessmentRepository | LoadDemoAssessment / ViewModel | Swift structs | implementation-derived / mock | NOT APPLICABLE: no backend mapping | `Seagis/Seagis/Models/Shared/Assessment.swift:1` |
| C10 | Open-Meteo response | Open-Meteo forecast API | OpenMeteo.parse/normalize | JSON hourly arrays | implementation-derived | forecast_value + grid + raw manifest | `Seagis-Model/scripts/environmental/open_meteo.py:1` |
| C11 | Copernicus subset | Copernicus Toolbox/xarray + STAC | Copernicus.parse/normalize | xarray + canonical logical JSON subset | implementation-derived | forecast_value + grid + raw manifest | `Seagis-Model/scripts/environmental/copernicus.py:1` |

### C01 A0 source envelope

| Attribute | Definition |
| --- | --- |
| Producer → consumer | fixture/provider logical extract → validate_source |
| Interface / format | JSON / Draft 2020-12 |
| Classification | explicit |
| Database mapping | seagis.ingestion_run + seagis_raw.raw_payload |
| Compatibility | Constant version where defined; general negotiation NOT FOUND |
| Evidence | `Seagis-Model/scripts/validate_contracts.py:1` |

| Field | Type / ref | Required | Nullable | Default | Meaning | Validation / allowed values | Units / timestamp | Example (illustrative) | DB mapping (boundary) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| schema_version | "const/enum" | True | False | NOT FOUND | Contract structure version; not a biological model version | {"const": "0.1.0"} | NOT APPLICABLE / schema | "0.1.0" | seagis.ingestion_run + seagis_raw.raw_payload |
| source_type | "const/enum" | True | False | NOT FOUND | Source adapter kind determining the fixture payload | {"enum": ["sensor", "copernicus", "open_meteo"]} | NOT APPLICABLE / schema | "sensor" | seagis.ingestion_run + seagis_raw.raw_payload |
| dataset_key | "const/enum" | True | False | NOT FOUND | Registered dataset key | {"enum": ["sensor_temperature_v1", "cmems_salinity_6h", "cmems_currents_6h", "cmems_nutrients_daily", "open_meteo_gfs"]} | NOT APPLICABLE / schema | "sensor_temperature_v1" | seagis.ingestion_run + seagis_raw.raw_payload |
| is_synthetic | "boolean" | True | False | NOT FOUND | Synthetic provenance flag, separate from QC | {"type": "boolean"} | NOT APPLICABLE / schema | false | seagis.ingestion_run + seagis_raw.raw_payload |
| received_at | "string" | True | False | NOT FOUND | Raw receipt instant at worker | {"type": "string", "format": "date-time", "pattern": "Z$"} | Units/time follow unit and parameter registry; UTC for normalized envelopes. | "2026-10-21T12:00:00Z" | seagis.ingestion_run + seagis_raw.raw_payload |
| provider_metadata | "object" | True | False | NOT FOUND | Sanitized provider and request metadata | {"type": "object"} | NOT APPLICABLE / schema | {} | seagis.ingestion_run + seagis_raw.raw_payload |
| payload | "object" | True | False | NOT FOUND | Synthetic raw JSON content when inline | {"type": "object"} | NOT APPLICABLE / schema | {} | seagis.ingestion_run + seagis_raw.raw_payload |

Complete schema for conditional rules and polymorphic structures (required above applies within each parent):

```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "schema_version": {
      "const": "0.1.0"
    },
    "source_type": {
      "enum": [
        "sensor",
        "copernicus",
        "open_meteo"
      ]
    },
    "dataset_key": {
      "enum": [
        "sensor_temperature_v1",
        "cmems_salinity_6h",
        "cmems_currents_6h",
        "cmems_nutrients_daily",
        "open_meteo_gfs"
      ]
    },
    "is_synthetic": {
      "type": "boolean"
    },
    "received_at": {
      "type": "string",
      "format": "date-time",
      "pattern": "Z$"
    },
    "provider_metadata": {
      "type": "object"
    },
    "payload": {
      "type": "object"
    }
  },
  "required": [
    "schema_version",
    "source_type",
    "dataset_key",
    "is_synthetic",
    "received_at",
    "provider_metadata",
    "payload"
  ],
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://seagis.local/contracts/source.schema.json",
  "title": "SEAGIS source envelopes v0.1.0",
  "allOf": [
    {
      "if": {
        "properties": {
          "source_type": {
            "const": "sensor"
          }
        }
      },
      "then": {
        "properties": {
          "payload": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
              "sensor_id": {
                "type": "string",
                "format": "uuid"
              },
              "boot_id": {
                "type": "string",
                "minLength": 1
              },
              "sequence": {
                "type": "integer",
                "minimum": 0
              },
              "observed_at": {
                "type": "string",
                "format": "date-time",
                "pattern": "Z$"
              },
              "water_temperature": {
                "type": [
                  "number",
                  "null"
                ]
              },
              "unit": {
                "const": "degC"
              },
              "value_status": {
                "enum": [
                  "present",
                  "missing",
                  "below_detection_limit",
                  "not_available"
                ]
              },
              "detection_limit": {
                "type": [
                  "number",
                  "null"
                ]
              }
            },
            "required": [
              "sensor_id",
              "boot_id",
              "sequence",
              "observed_at",
              "water_temperature",
              "unit",
              "value_status",
              "detection_limit"
            ]
          },
          "dataset_key": {
            "enum": [
              "sensor_temperature_v1"
            ]
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "source_type": {
            "const": "copernicus"
          }
        }
      },
      "then": {
        "properties": {
          "payload": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
              "representation": {
                "const": "netcdf-logical-extract"
              },
              "coordinates": {
                "type": "object",
                "additionalProperties": false,
                "properties": {
                  "time": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                      "type": "string",
                      "format": "date-time",
                      "pattern": "Z$"
                    }
                  },
                  "depth": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                      "type": "number",
                      "minimum": 0
                    }
                  },
                  "latitude": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                      "type": "number",
                      "minimum": -90,
                      "maximum": 90
                    }
                  },
                  "longitude": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                      "type": "number",
                      "minimum": -180,
                      "maximum": 180
                    }
                  }
                },
                "required": [
                  "time",
                  "depth",
                  "latitude",
                  "longitude"
                ]
              },
              "variables": {
                "type": "object",
                "additionalProperties": false,
                "properties": {
                  "so": {
                    "type": "object",
                    "additionalProperties": false,
                    "properties": {
                      "unit": {
                        "const": "1e-3"
                      },
                      "fill_value": {
                        "type": "number"
                      },
                      "values": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                          "type": [
                            "number",
                            "null"
                          ]
                        }
                      }
                    },
                    "required": [
                      "unit",
                      "fill_value",
                      "values"
                    ]
                  },
                  "uo": {
                    "type": "object",
                    "additionalProperties": false,
                    "properties": {
                      "unit": {
                        "const": "m s-1"
                      },
                      "fill_value": {
                        "type": "number"
                      },
                      "values": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                          "type": [
                            "number",
                            "null"
                          ]
                        }
                      }
                    },
                    "required": [
                      "unit",
                      "fill_value",
                      "values"
                    ]
                  },
                  "vo": {
                    "type": "object",
                    "additionalProperties": false,
                    "properties": {
                      "unit": {
                        "const": "m s-1"
                      },
                      "fill_value": {
                        "type": "number"
                      },
                      "values": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                          "type": [
                            "number",
                            "null"
                          ]
                        }
                      }
                    },
                    "required": [
                      "unit",
                      "fill_value",
                      "values"
                    ]
                  },
                  "no3": {
                    "type": "object",
                    "additionalProperties": false,
                    "properties": {
                      "unit": {
                        "const": "mmol m-3"
                      },
                      "fill_value": {
                        "type": "number"
                      },
                      "values": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                          "type": [
                            "number",
                            "null"
                          ]
                        }
                      }
                    },
                    "required": [
                      "unit",
                      "fill_value",
                      "values"
                    ]
                  },
                  "po4": {
                    "type": "object",
                    "additionalProperties": false,
                    "properties": {
                      "unit": {
                        "const": "mmol m-3"
                      },
                      "fill_value": {
                        "type": "number"
                      },
                      "values": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                          "type": [
                            "number",
                            "null"
                          ]
                        }
                      }
                    },
                    "required": [
                      "unit",
                      "fill_value",
                      "values"
                    ]
                  }
                },
                "minProperties": 1
              }
            },
            "required": [
              "representation",
              "coordinates",
              "variables"
            ]
          },
          "dataset_key": {
            "enum": [
              "cmems_salinity_6h",
              "cmems_currents_6h",
              "cmems_nutrients_daily"
            ]
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "source_type": {
            "const": "open_meteo"
          }
        }
      },
      "then": {
        "properties": {
          "payload": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
              "latitude": {
                "type": "number"
              },
              "longitude": {
                "type": "number"
              },
              "generationtime_ms": {
                "type": "number"
              },
              "utc_offset_seconds": {
                "const": 0
              },
              "timezone": {
                "enum": [
                  "GMT",
                  "UTC"
                ]
              },
              "timezone_abbreviation": {
                "enum": [
                  "GMT",
                  "UTC"
                ]
              },
              "hourly_units": {
                "type": "object",
                "additionalProperties": false,
                "properties": {
                  "time": {
                    "const": "iso8601"
                  },
                  "precipitation": {
                    "const": "mm"
                  },
                  "wind_speed_10m": {
                    "const": "m/s"
                  },
                  "wind_direction_10m": {
                    "const": "°"
                  },
                  "cloud_cover": {
                    "const": "%"
                  },
                  "uv_index": {
                    "const": ""
                  },
                  "temperature_2m": {
                    "const": "°C"
                  }
                },
                "required": [
                  "time",
                  "precipitation",
                  "wind_speed_10m",
                  "wind_direction_10m",
                  "cloud_cover",
                  "uv_index",
                  "temperature_2m"
                ]
              },
              "hourly": {
                "type": "object",
                "additionalProperties": false,
                "properties": {
                  "time": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                      "type": "string",
                      "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}$"
                    }
                  },
                  "precipitation": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                      "type": [
                        "number",
                        "null"
                      ]
                    }
                  },
                  "wind_speed_10m": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                      "type": [
                        "number",
                        "null"
                      ]
                    }
                  },
                  "wind_direction_10m": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                      "type": [
                        "number",
                        "null"
                      ]
                    }
                  },
                  "cloud_cover": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                      "type": [
                        "number",
                        "null"
                      ]
                    }
                  },
                  "uv_index": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                      "type": [
                        "number",
                        "null"
                      ]
                    }
                  },
                  "temperature_2m": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                      "type": [
                        "number",
                        "null"
                      ]
                    }
                  }
                },
                "required": [
                  "time",
                  "precipitation",
                  "wind_speed_10m",
                  "wind_direction_10m",
                  "cloud_cover",
                  "uv_index",
                  "temperature_2m"
                ]
              }
            },
            "required": [
              "latitude",
              "longitude",
              "generationtime_ms",
              "utc_offset_seconds",
              "timezone",
              "timezone_abbreviation",
              "hourly_units",
              "hourly"
            ]
          },
          "dataset_key": {
            "enum": [
              "open_meteo_gfs"
            ]
          }
        }
      }
    }
  ]
}
```

### C02 A0 normalized envelope

| Attribute | Definition |
| --- | --- |
| Producer → consumer | fixture normalization → validate_normalized + SQL guards |
| Interface / format | JSON / Draft 2020-12 |
| Classification | explicit |
| Database mapping | observation / forecast_run / forecast_value / source_grid |
| Compatibility | Constant version where defined; general negotiation NOT FOUND |
| Evidence | `Seagis-Model/scripts/validate_contracts.py:1` |

| Field | Type / ref | Required | Nullable | Default | Meaning | Validation / allowed values | Units / timestamp | Example (illustrative) | DB mapping (boundary) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| schema_version | "const/enum" | True | False | NOT FOUND | Contract structure version; not a biological model version | {"const": "0.1.0"} | NOT APPLICABLE / schema | "0.1.0" | observation / forecast_run / forecast_value / source_grid |
| dataset_key | "const/enum" | True | False | NOT FOUND | Registered dataset key | {"enum": ["sensor_temperature_v1", "cmems_salinity_6h", "cmems_currents_6h", "cmems_nutrients_daily", "open_meteo_gfs"]} | NOT APPLICABLE / schema | "sensor_temperature_v1" | observation / forecast_run / forecast_value / source_grid |
| ingestion_run | "object" | True | False | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "object", "additionalProperties": false, "required": ["id", "request_key", "adapter_version", "started_at", "completed_at", "status", "is_synthetic"]} | NOT APPLICABLE / schema | {} | observation / forecast_run / forecast_value / source_grid |
| ingestion_run.id | "string" | True | False | NOT FOUND | Row identity under the table primary key | {"type": "string", "format": "uuid"} | NOT APPLICABLE / schema | "00000000-0000-4000-8000-000000000001" | observation / forecast_run / forecast_value / source_grid |
| ingestion_run.request_key | "string" | True | False | NOT FOUND | Logical ingestion retry key per dataset | {"type": "string", "minLength": 1} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | observation / forecast_run / forecast_value / source_grid |
| ingestion_run.adapter_version | "string" | True | False | NOT FOUND | Ingestion adapter implementation version | {"type": "string", "minLength": 1} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | observation / forecast_run / forecast_value / source_grid |
| ingestion_run.started_at | "string" | True | False | NOT FOUND | Ingestion or attempt start instant | {"type": "string", "format": "date-time", "pattern": "Z$"} | NOT APPLICABLE / schema | "2026-10-21T12:00:00Z" | observation / forecast_run / forecast_value / source_grid |
| ingestion_run.completed_at | "string" | True | False | NOT FOUND | Completion instant; null while running | {"type": "string", "format": "date-time", "pattern": "Z$"} | NOT APPLICABLE / schema | "2026-10-21T12:00:00Z" | observation / forecast_run / forecast_value / source_grid |
| ingestion_run.status | "const/enum" | True | False | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"const": "succeeded"} | NOT APPLICABLE / schema | "succeeded" | observation / forecast_run / forecast_value / source_grid |
| ingestion_run.is_synthetic | "boolean" | True | False | NOT FOUND | Synthetic provenance flag, separate from QC | {"type": "boolean"} | NOT APPLICABLE / schema | false | observation / forecast_run / forecast_value / source_grid |
| raw_payload | "object" | True | False | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "object", "additionalProperties": false, "required": ["id", "sha256", "received_at", "format", "licence_snapshot"]} | NOT APPLICABLE / schema | {} | observation / forecast_run / forecast_value / source_grid |
| raw_payload.id | "string" | True | False | NOT FOUND | Row identity under the table primary key | {"type": "string", "format": "uuid"} | NOT APPLICABLE / schema | "00000000-0000-4000-8000-000000000001" | observation / forecast_run / forecast_value / source_grid |
| raw_payload.sha256 | "string" | True | False | NOT FOUND | Raw digest under hash_basis, not necessarily network bytes | {"type": "string", "pattern": "^[0-9a-f]{64}$"} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | observation / forecast_run / forecast_value / source_grid |
| raw_payload.received_at | "string" | True | False | NOT FOUND | Raw receipt instant at worker | {"type": "string", "format": "date-time", "pattern": "Z$"} | Units/time follow unit and parameter registry; UTC for normalized envelopes. | "2026-10-21T12:00:00Z" | observation / forecast_run / forecast_value / source_grid |
| raw_payload.format | "string" | True | False | NOT FOUND | Raw representation media type or format | {"type": "string", "minLength": 1} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | observation / forecast_run / forecast_value / source_grid |
| raw_payload.licence_snapshot | "string" | True | False | NOT FOUND | Licence statement at capture | {"type": "string", "minLength": 1} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | observation / forecast_run / forecast_value / source_grid |
| forecast_run/anyOf/0 | "object" | False | False | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "object", "additionalProperties": false, "required": ["id", "run_key", "run_kind", "provider_run_id", "model_initialized_at", "issued_at", "issue_time_basis", "ingested_at"]} | NOT APPLICABLE / schema | {} | observation / forecast_run / forecast_value / source_grid |
| forecast_run/anyOf/0.id | "string" | True | False | NOT FOUND | Row identity under the table primary key | {"type": "string", "format": "uuid"} | NOT APPLICABLE / schema | "00000000-0000-4000-8000-000000000001" | observation / forecast_run / forecast_value / source_grid |
| forecast_run/anyOf/0.run_key | "string" | True | False | NOT FOUND | Semantic capture identity per dataset | {"type": "string", "minLength": 1} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | observation / forecast_run / forecast_value / source_grid |
| forecast_run/anyOf/0.run_kind | "const/enum" | True | False | NOT FOUND | forecast, analysis or analysis_forecast_unspecified | {"enum": ["forecast", "analysis"]} | NOT APPLICABLE / schema | "forecast" | observation / forecast_run / forecast_value / source_grid |
| forecast_run/anyOf/0.provider_run_id | ["string", "null"] | True | True | NOT FOUND | Provider run ID only when actually available | {"type": ["string", "null"]} | NOT APPLICABLE / schema | null | observation / forecast_run / forecast_value / source_grid |
| forecast_run/anyOf/0.model_initialized_at/anyOf/0 | "string" | False | False | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "string", "format": "date-time", "pattern": "Z$"} | NOT APPLICABLE / schema | "2026-10-21T12:00:00Z" | observation / forecast_run / forecast_value / source_grid |
| forecast_run/anyOf/0.model_initialized_at/anyOf/1 | "null" | False | True | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "null"} | NOT APPLICABLE / schema | null | observation / forecast_run / forecast_value / source_grid |
| forecast_run/anyOf/0.issued_at/anyOf/0 | "string" | False | False | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "string", "format": "date-time", "pattern": "Z$"} | NOT APPLICABLE / schema | "2026-10-21T12:00:00Z" | observation / forecast_run / forecast_value / source_grid |
| forecast_run/anyOf/0.issued_at/anyOf/1 | "null" | False | True | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "null"} | NOT APPLICABLE / schema | null | observation / forecast_run / forecast_value / source_grid |
| forecast_run/anyOf/0.issue_time_basis | "const/enum" | True | False | NOT FOUND | Known/unknown publication-time basis | {"enum": ["provider_verified", "unknown"]} | NOT APPLICABLE / schema | "provider_verified" | observation / forecast_run / forecast_value / source_grid |
| forecast_run/anyOf/0.ingested_at | "string" | True | False | NOT FOUND | Instant data became available to the system | {"type": "string", "format": "date-time", "pattern": "Z$"} | NOT APPLICABLE / schema | "2026-10-21T12:00:00Z" | observation / forecast_run / forecast_value / source_grid |
| forecast_run/anyOf/1 | "null" | False | True | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "null"} | NOT APPLICABLE / schema | null | observation / forecast_run / forecast_value / source_grid |
| source_grid/anyOf/0 | "object" | False | False | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "object", "additionalProperties": false, "required": ["id", "grid_key", "grid_version", "identity_basis", "latitude", "longitude", "depth_m"]} | NOT APPLICABLE / schema | {} | observation / forecast_run / forecast_value / source_grid |
| source_grid/anyOf/0.id | "string" | True | False | NOT FOUND | Row identity under the table primary key | {"type": "string", "format": "uuid"} | NOT APPLICABLE / schema | "00000000-0000-4000-8000-000000000001" | observation / forecast_run / forecast_value / source_grid |
| source_grid/anyOf/0.grid_key | "string" | True | False | NOT FOUND | Cell key based on coordinates/depth or fixture | {"type": "string", "minLength": 1} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | observation / forecast_run / forecast_value / source_grid |
| source_grid/anyOf/0.grid_version | "string" | True | False | NOT FOUND | Grid identity version | {"type": "string", "minLength": 1} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | observation / forecast_run / forecast_value / source_grid |
| source_grid/anyOf/0.identity_basis | "const/enum" | True | False | NOT FOUND | Identity basis: native cell, response coordinate or synthetic | {"enum": ["provider_cell", "provider_returned_coordinate", "synthetic"]} | NOT APPLICABLE / schema | "provider_cell" | observation / forecast_run / forecast_value / source_grid |
| source_grid/anyOf/0.latitude | "number" | True | False | NOT FOUND | WGS84 latitude in degrees | {"type": "number", "minimum": -90, "maximum": 90} | NOT APPLICABLE / schema | 0 | observation / forecast_run / forecast_value / source_grid |
| source_grid/anyOf/0.longitude | "number" | True | False | NOT FOUND | WGS84 longitude in degrees | {"type": "number", "minimum": -180, "maximum": 180} | NOT APPLICABLE / schema | 0 | observation / forecast_run / forecast_value / source_grid |
| source_grid/anyOf/0.depth_m | "number" | True | False | NOT FOUND | Depth positive downward in metres | {"type": "number", "minimum": 0} | NOT APPLICABLE / schema | 0 | observation / forecast_run / forecast_value / source_grid |
| source_grid/anyOf/1 | "null" | False | True | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "null"} | NOT APPLICABLE / schema | null | observation / forecast_run / forecast_value / source_grid |
| measurements | "array" | True | False | NOT FOUND | Cross-field-validated observation/forecast_value list | {"type": "array", "minItems": 1} | NOT APPLICABLE / schema | [] | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/0 | "object" | False | False | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "object", "additionalProperties": false, "required": ["id", "parameter_code", "native_value", "native_unit", "value", "unit", "conversion_code", "value_status", "detection_limit", "ingested_at", "quality_status", "kind", "plot_id", "sensor_id", "source_record_key", "observed_at"]} | NOT APPLICABLE / schema | {} | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/0.id | "string" | True | False | NOT FOUND | Row identity under the table primary key | {"type": "string", "format": "uuid"} | NOT APPLICABLE / schema | "00000000-0000-4000-8000-000000000001" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/0.parameter_code | "const/enum" | True | False | NOT FOUND | Environmental parameter identity | {"enum": ["water_temperature", "salinity", "current_eastward", "current_northward", "nitrate", "phosphate", "precipitation", "wind_speed_10m", "wind_direction_10m", "cloud_cover", "uv_index", "air_temperature_2m"]} | NOT APPLICABLE / schema | "water_temperature" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/0.native_value | ["number", "null"] | True | True | NOT FOUND | Physical value in source units | {"type": ["number", "null"]} | Units/time follow unit and parameter registry; UTC for normalized envelopes. | null | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/0.native_unit | "string" | True | False | NOT FOUND | Original unit before normalization | {"type": "string"} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/0.value | ["number", "null"] | True | True | NOT FOUND | Normalized value; null follows value_status | {"type": ["number", "null"]} | Units/time follow unit and parameter registry; UTC for normalized envelopes. | null | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/0.unit | "string" | True | False | NOT FOUND | Normalized value unit from registry | {"type": "string", "minLength": 1} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/0.conversion_code | "const/enum" | True | False | NOT FOUND | Unit-conversion method identity | {"enum": ["identity", "unit_notation"]} | NOT APPLICABLE / schema | "identity" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/0.value_status | "const/enum" | True | False | NOT FOUND | Numeric availability, separate from quality | {"enum": ["present", "missing", "below_detection_limit", "not_available"]} | NOT APPLICABLE / schema | "present" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/0.detection_limit | ["number", "null"] | True | True | NOT FOUND | Detection limit in normalized units when applicable | {"type": ["number", "null"]} | Units/time follow unit and parameter registry; UTC for normalized envelopes. | null | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/0.ingested_at | "string" | True | False | NOT FOUND | Instant data became available to the system | {"type": "string", "format": "date-time", "pattern": "Z$"} | NOT APPLICABLE / schema | "2026-10-21T12:00:00Z" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/0.quality_status | "const/enum" | True | False | NOT FOUND | QC state unreviewed, accepted, suspect or rejected; not a diagnosis | {"enum": ["unreviewed", "accepted", "suspect", "rejected"]} | NOT APPLICABLE / schema | "unreviewed" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/0.kind | "const/enum" | True | False | NOT FOUND | Actor kind device or reader | {"const": "observation"} | NOT APPLICABLE / schema | "observation" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/0.plot_id | "string" | True | False | NOT FOUND | Cultivation plot reference | {"type": "string", "format": "uuid"} | NOT APPLICABLE / schema | "00000000-0000-4000-8000-000000000001" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/0.sensor_id | "string" | True | False | NOT FOUND | Sensor deployment reference | {"type": "string", "format": "uuid"} | NOT APPLICABLE / schema | "00000000-0000-4000-8000-000000000001" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/0.source_record_key | "string" | True | False | NOT FOUND | boot_id:sequence for A1 packets | {"type": "string", "minLength": 1} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/0.observed_at | "string" | True | False | NOT FOUND | Sensor measurement instant, distinct from receipt | {"type": "string", "format": "date-time", "pattern": "Z$"} | Units/time follow unit and parameter registry; UTC for normalized envelopes. | "2026-10-21T12:00:00Z" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/1 | "object" | False | False | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "object", "additionalProperties": false, "required": ["id", "parameter_code", "native_value", "native_unit", "value", "unit", "conversion_code", "value_status", "detection_limit", "ingested_at", "quality_status", "kind", "valid_at", "temporal_support", "interval_status", "period_start_at", "period_end_at"]} | NOT APPLICABLE / schema | {} | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/1.id | "string" | True | False | NOT FOUND | Row identity under the table primary key | {"type": "string", "format": "uuid"} | NOT APPLICABLE / schema | "00000000-0000-4000-8000-000000000001" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/1.parameter_code | "const/enum" | True | False | NOT FOUND | Environmental parameter identity | {"enum": ["water_temperature", "salinity", "current_eastward", "current_northward", "nitrate", "phosphate", "precipitation", "wind_speed_10m", "wind_direction_10m", "cloud_cover", "uv_index", "air_temperature_2m"]} | NOT APPLICABLE / schema | "water_temperature" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/1.native_value | ["number", "null"] | True | True | NOT FOUND | Physical value in source units | {"type": ["number", "null"]} | Units/time follow unit and parameter registry; UTC for normalized envelopes. | null | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/1.native_unit | "string" | True | False | NOT FOUND | Original unit before normalization | {"type": "string"} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/1.value | ["number", "null"] | True | True | NOT FOUND | Normalized value; null follows value_status | {"type": ["number", "null"]} | Units/time follow unit and parameter registry; UTC for normalized envelopes. | null | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/1.unit | "string" | True | False | NOT FOUND | Normalized value unit from registry | {"type": "string", "minLength": 1} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/1.conversion_code | "const/enum" | True | False | NOT FOUND | Unit-conversion method identity | {"enum": ["identity", "unit_notation"]} | NOT APPLICABLE / schema | "identity" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/1.value_status | "const/enum" | True | False | NOT FOUND | Numeric availability, separate from quality | {"enum": ["present", "missing", "below_detection_limit", "not_available"]} | NOT APPLICABLE / schema | "present" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/1.detection_limit | ["number", "null"] | True | True | NOT FOUND | Detection limit in normalized units when applicable | {"type": ["number", "null"]} | Units/time follow unit and parameter registry; UTC for normalized envelopes. | null | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/1.ingested_at | "string" | True | False | NOT FOUND | Instant data became available to the system | {"type": "string", "format": "date-time", "pattern": "Z$"} | NOT APPLICABLE / schema | "2026-10-21T12:00:00Z" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/1.quality_status | "const/enum" | True | False | NOT FOUND | QC state unreviewed, accepted, suspect or rejected; not a diagnosis | {"enum": ["unreviewed", "accepted", "suspect", "rejected"]} | NOT APPLICABLE / schema | "unreviewed" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/1.kind | "const/enum" | True | False | NOT FOUND | Actor kind device or reader | {"const": "forecast_value"} | NOT APPLICABLE / schema | "forecast_value" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/1.valid_at | "string" | True | False | NOT FOUND | Representative time of model value | {"type": "string", "format": "date-time", "pattern": "Z$"} | Units/time follow unit and parameter registry; UTC for normalized envelopes. | "2026-10-21T12:00:00Z" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/1.temporal_support | "const/enum" | True | False | NOT FOUND | Temporal support: instantaneous, mean or sum | {"enum": ["instantaneous", "mean", "sum"]} | NOT APPLICABLE / schema | "instantaneous" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/1.interval_status | "const/enum" | True | False | NOT FOUND | known, unknown or not_applicable interval status | {"enum": ["not_applicable", "known", "unknown"]} | NOT APPLICABLE / schema | "not_applicable" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/1.period_start_at/anyOf/0 | "string" | False | False | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "string", "format": "date-time", "pattern": "Z$"} | NOT APPLICABLE / schema | "2026-10-21T12:00:00Z" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/1.period_start_at/anyOf/1 | "null" | False | True | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "null"} | NOT APPLICABLE / schema | null | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/1.period_end_at/anyOf/0 | "string" | False | False | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "string", "format": "date-time", "pattern": "Z$"} | NOT APPLICABLE / schema | "2026-10-21T12:00:00Z" | observation / forecast_run / forecast_value / source_grid |
| measurements[]/oneOf/1.period_end_at/anyOf/1 | "null" | False | True | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "null"} | NOT APPLICABLE / schema | null | observation / forecast_run / forecast_value / source_grid |

Complete schema for conditional rules and polymorphic structures (required above applies within each parent):

```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "schema_version": {
      "const": "0.1.0"
    },
    "dataset_key": {
      "enum": [
        "sensor_temperature_v1",
        "cmems_salinity_6h",
        "cmems_currents_6h",
        "cmems_nutrients_daily",
        "open_meteo_gfs"
      ]
    },
    "ingestion_run": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "id": {
          "type": "string",
          "format": "uuid"
        },
        "request_key": {
          "type": "string",
          "minLength": 1
        },
        "adapter_version": {
          "type": "string",
          "minLength": 1
        },
        "started_at": {
          "type": "string",
          "format": "date-time",
          "pattern": "Z$"
        },
        "completed_at": {
          "type": "string",
          "format": "date-time",
          "pattern": "Z$"
        },
        "status": {
          "const": "succeeded"
        },
        "is_synthetic": {
          "type": "boolean"
        }
      },
      "required": [
        "id",
        "request_key",
        "adapter_version",
        "started_at",
        "completed_at",
        "status",
        "is_synthetic"
      ]
    },
    "raw_payload": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "id": {
          "type": "string",
          "format": "uuid"
        },
        "sha256": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        },
        "received_at": {
          "type": "string",
          "format": "date-time",
          "pattern": "Z$"
        },
        "format": {
          "type": "string",
          "minLength": 1
        },
        "licence_snapshot": {
          "type": "string",
          "minLength": 1
        }
      },
      "required": [
        "id",
        "sha256",
        "received_at",
        "format",
        "licence_snapshot"
      ]
    },
    "forecast_run": {
      "anyOf": [
        {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "id": {
              "type": "string",
              "format": "uuid"
            },
            "run_key": {
              "type": "string",
              "minLength": 1
            },
            "run_kind": {
              "enum": [
                "forecast",
                "analysis"
              ]
            },
            "provider_run_id": {
              "type": [
                "string",
                "null"
              ]
            },
            "model_initialized_at": {
              "anyOf": [
                {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "Z$"
                },
                {
                  "type": "null"
                }
              ]
            },
            "issued_at": {
              "anyOf": [
                {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "Z$"
                },
                {
                  "type": "null"
                }
              ]
            },
            "issue_time_basis": {
              "enum": [
                "provider_verified",
                "unknown"
              ]
            },
            "ingested_at": {
              "type": "string",
              "format": "date-time",
              "pattern": "Z$"
            }
          },
          "required": [
            "id",
            "run_key",
            "run_kind",
            "provider_run_id",
            "model_initialized_at",
            "issued_at",
            "issue_time_basis",
            "ingested_at"
          ]
        },
        {
          "type": "null"
        }
      ]
    },
    "source_grid": {
      "anyOf": [
        {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "id": {
              "type": "string",
              "format": "uuid"
            },
            "grid_key": {
              "type": "string",
              "minLength": 1
            },
            "grid_version": {
              "type": "string",
              "minLength": 1
            },
            "identity_basis": {
              "enum": [
                "provider_cell",
                "provider_returned_coordinate",
                "synthetic"
              ]
            },
            "latitude": {
              "type": "number",
              "minimum": -90,
              "maximum": 90
            },
            "longitude": {
              "type": "number",
              "minimum": -180,
              "maximum": 180
            },
            "depth_m": {
              "type": "number",
              "minimum": 0
            }
          },
          "required": [
            "id",
            "grid_key",
            "grid_version",
            "identity_basis",
            "latitude",
            "longitude",
            "depth_m"
          ]
        },
        {
          "type": "null"
        }
      ]
    },
    "measurements": {
      "type": "array",
      "minItems": 1,
      "items": {
        "oneOf": [
          {
            "type": "object",
            "additionalProperties": false,
            "properties": {
              "id": {
                "type": "string",
                "format": "uuid"
              },
              "parameter_code": {
                "enum": [
                  "water_temperature",
                  "salinity",
                  "current_eastward",
                  "current_northward",
                  "nitrate",
                  "phosphate",
                  "precipitation",
                  "wind_speed_10m",
                  "wind_direction_10m",
                  "cloud_cover",
                  "uv_index",
                  "air_temperature_2m"
                ]
              },
              "native_value": {
                "type": [
                  "number",
                  "null"
                ]
              },
              "native_unit": {
                "type": "string"
              },
              "value": {
                "type": [
                  "number",
                  "null"
                ]
              },
              "unit": {
                "type": "string",
                "minLength": 1
              },
              "conversion_code": {
                "enum": [
                  "identity",
                  "unit_notation"
                ]
              },
              "value_status": {
                "enum": [
                  "present",
                  "missing",
                  "below_detection_limit",
                  "not_available"
                ]
              },
              "detection_limit": {
                "type": [
                  "number",
                  "null"
                ]
              },
              "ingested_at": {
                "type": "string",
                "format": "date-time",
                "pattern": "Z$"
              },
              "quality_status": {
                "enum": [
                  "unreviewed",
                  "accepted",
                  "suspect",
                  "rejected"
                ]
              },
              "kind": {
                "const": "observation"
              },
              "plot_id": {
                "type": "string",
                "format": "uuid"
              },
              "sensor_id": {
                "type": "string",
                "format": "uuid"
              },
              "source_record_key": {
                "type": "string",
                "minLength": 1
              },
              "observed_at": {
                "type": "string",
                "format": "date-time",
                "pattern": "Z$"
              }
            },
            "required": [
              "id",
              "parameter_code",
              "native_value",
              "native_unit",
              "value",
              "unit",
              "conversion_code",
              "value_status",
              "detection_limit",
              "ingested_at",
              "quality_status",
              "kind",
              "plot_id",
              "sensor_id",
              "source_record_key",
              "observed_at"
            ]
          },
          {
            "type": "object",
            "additionalProperties": false,
            "properties": {
              "id": {
                "type": "string",
                "format": "uuid"
              },
              "parameter_code": {
                "enum": [
                  "water_temperature",
                  "salinity",
                  "current_eastward",
                  "current_northward",
                  "nitrate",
                  "phosphate",
                  "precipitation",
                  "wind_speed_10m",
                  "wind_direction_10m",
                  "cloud_cover",
                  "uv_index",
                  "air_temperature_2m"
                ]
              },
              "native_value": {
                "type": [
                  "number",
                  "null"
                ]
              },
              "native_unit": {
                "type": "string"
              },
              "value": {
                "type": [
                  "number",
                  "null"
                ]
              },
              "unit": {
                "type": "string",
                "minLength": 1
              },
              "conversion_code": {
                "enum": [
                  "identity",
                  "unit_notation"
                ]
              },
              "value_status": {
                "enum": [
                  "present",
                  "missing",
                  "below_detection_limit",
                  "not_available"
                ]
              },
              "detection_limit": {
                "type": [
                  "number",
                  "null"
                ]
              },
              "ingested_at": {
                "type": "string",
                "format": "date-time",
                "pattern": "Z$"
              },
              "quality_status": {
                "enum": [
                  "unreviewed",
                  "accepted",
                  "suspect",
                  "rejected"
                ]
              },
              "kind": {
                "const": "forecast_value"
              },
              "valid_at": {
                "type": "string",
                "format": "date-time",
                "pattern": "Z$"
              },
              "temporal_support": {
                "enum": [
                  "instantaneous",
                  "mean",
                  "sum"
                ]
              },
              "interval_status": {
                "enum": [
                  "not_applicable",
                  "known",
                  "unknown"
                ]
              },
              "period_start_at": {
                "anyOf": [
                  {
                    "type": "string",
                    "format": "date-time",
                    "pattern": "Z$"
                  },
                  {
                    "type": "null"
                  }
                ]
              },
              "period_end_at": {
                "anyOf": [
                  {
                    "type": "string",
                    "format": "date-time",
                    "pattern": "Z$"
                  },
                  {
                    "type": "null"
                  }
                ]
              }
            },
            "required": [
              "id",
              "parameter_code",
              "native_value",
              "native_unit",
              "value",
              "unit",
              "conversion_code",
              "value_status",
              "detection_limit",
              "ingested_at",
              "quality_status",
              "kind",
              "valid_at",
              "temporal_support",
              "interval_status",
              "period_start_at",
              "period_end_at"
            ]
          }
        ]
      }
    }
  },
  "required": [
    "schema_version",
    "dataset_key",
    "ingestion_run",
    "raw_payload",
    "forecast_run",
    "source_grid",
    "measurements"
  ],
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://seagis.local/contracts/normalized.schema.json",
  "title": "SEAGIS normalized envelope v0.1.0",
  "allOf": [
    {
      "if": {
        "properties": {
          "dataset_key": {
            "const": "sensor_temperature_v1"
          }
        }
      },
      "then": {
        "properties": {
          "forecast_run": {
            "type": "null"
          },
          "source_grid": {
            "type": "null"
          },
          "measurements": {
            "type": "array",
            "minItems": 1,
            "items": {
              "type": "object",
              "additionalProperties": false,
              "properties": {
                "id": {
                  "type": "string",
                  "format": "uuid"
                },
                "parameter_code": {
                  "enum": [
                    "water_temperature",
                    "salinity",
                    "current_eastward",
                    "current_northward",
                    "nitrate",
                    "phosphate",
                    "precipitation",
                    "wind_speed_10m",
                    "wind_direction_10m",
                    "cloud_cover",
                    "uv_index",
                    "air_temperature_2m"
                  ]
                },
                "native_value": {
                  "type": [
                    "number",
                    "null"
                  ]
                },
                "native_unit": {
                  "type": "string"
                },
                "value": {
                  "type": [
                    "number",
                    "null"
                  ]
                },
                "unit": {
                  "type": "string",
                  "minLength": 1
                },
                "conversion_code": {
                  "enum": [
                    "identity",
                    "unit_notation"
                  ]
                },
                "value_status": {
                  "enum": [
                    "present",
                    "missing",
                    "below_detection_limit",
                    "not_available"
                  ]
                },
                "detection_limit": {
                  "type": [
                    "number",
                    "null"
                  ]
                },
                "ingested_at": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "Z$"
                },
                "quality_status": {
                  "enum": [
                    "unreviewed",
                    "accepted",
                    "suspect",
                    "rejected"
                  ]
                },
                "kind": {
                  "const": "observation"
                },
                "plot_id": {
                  "type": "string",
                  "format": "uuid"
                },
                "sensor_id": {
                  "type": "string",
                  "format": "uuid"
                },
                "source_record_key": {
                  "type": "string",
                  "minLength": 1
                },
                "observed_at": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "Z$"
                }
              },
              "required": [
                "id",
                "parameter_code",
                "native_value",
                "native_unit",
                "value",
                "unit",
                "conversion_code",
                "value_status",
                "detection_limit",
                "ingested_at",
                "quality_status",
                "kind",
                "plot_id",
                "sensor_id",
                "source_record_key",
                "observed_at"
              ]
            }
          }
        }
      },
      "else": {
        "properties": {
          "forecast_run": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
              "id": {
                "type": "string",
                "format": "uuid"
              },
              "run_key": {
                "type": "string",
                "minLength": 1
              },
              "run_kind": {
                "enum": [
                  "forecast",
                  "analysis"
                ]
              },
              "provider_run_id": {
                "type": [
                  "string",
                  "null"
                ]
              },
              "model_initialized_at": {
                "anyOf": [
                  {
                    "type": "string",
                    "format": "date-time",
                    "pattern": "Z$"
                  },
                  {
                    "type": "null"
                  }
                ]
              },
              "issued_at": {
                "anyOf": [
                  {
                    "type": "string",
                    "format": "date-time",
                    "pattern": "Z$"
                  },
                  {
                    "type": "null"
                  }
                ]
              },
              "issue_time_basis": {
                "enum": [
                  "provider_verified",
                  "unknown"
                ]
              },
              "ingested_at": {
                "type": "string",
                "format": "date-time",
                "pattern": "Z$"
              }
            },
            "required": [
              "id",
              "run_key",
              "run_kind",
              "provider_run_id",
              "model_initialized_at",
              "issued_at",
              "issue_time_basis",
              "ingested_at"
            ]
          },
          "source_grid": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
              "id": {
                "type": "string",
                "format": "uuid"
              },
              "grid_key": {
                "type": "string",
                "minLength": 1
              },
              "grid_version": {
                "type": "string",
                "minLength": 1
              },
              "identity_basis": {
                "enum": [
                  "provider_cell",
                  "provider_returned_coordinate",
                  "synthetic"
                ]
              },
              "latitude": {
                "type": "number",
                "minimum": -90,
                "maximum": 90
              },
              "longitude": {
                "type": "number",
                "minimum": -180,
                "maximum": 180
              },
              "depth_m": {
                "type": "number",
                "minimum": 0
              }
            },
            "required": [
              "id",
              "grid_key",
              "grid_version",
              "identity_basis",
              "latitude",
              "longitude",
              "depth_m"
            ]
          },
          "measurements": {
            "type": "array",
            "minItems": 1,
            "items": {
              "type": "object",
              "additionalProperties": false,
              "properties": {
                "id": {
                  "type": "string",
                  "format": "uuid"
                },
                "parameter_code": {
                  "enum": [
                    "water_temperature",
                    "salinity",
                    "current_eastward",
                    "current_northward",
                    "nitrate",
                    "phosphate",
                    "precipitation",
                    "wind_speed_10m",
                    "wind_direction_10m",
                    "cloud_cover",
                    "uv_index",
                    "air_temperature_2m"
                  ]
                },
                "native_value": {
                  "type": [
                    "number",
                    "null"
                  ]
                },
                "native_unit": {
                  "type": "string"
                },
                "value": {
                  "type": [
                    "number",
                    "null"
                  ]
                },
                "unit": {
                  "type": "string",
                  "minLength": 1
                },
                "conversion_code": {
                  "enum": [
                    "identity",
                    "unit_notation"
                  ]
                },
                "value_status": {
                  "enum": [
                    "present",
                    "missing",
                    "below_detection_limit",
                    "not_available"
                  ]
                },
                "detection_limit": {
                  "type": [
                    "number",
                    "null"
                  ]
                },
                "ingested_at": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "Z$"
                },
                "quality_status": {
                  "enum": [
                    "unreviewed",
                    "accepted",
                    "suspect",
                    "rejected"
                  ]
                },
                "kind": {
                  "const": "forecast_value"
                },
                "valid_at": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "Z$"
                },
                "temporal_support": {
                  "enum": [
                    "instantaneous",
                    "mean",
                    "sum"
                  ]
                },
                "interval_status": {
                  "enum": [
                    "not_applicable",
                    "known",
                    "unknown"
                  ]
                },
                "period_start_at": {
                  "anyOf": [
                    {
                      "type": "string",
                      "format": "date-time",
                      "pattern": "Z$"
                    },
                    {
                      "type": "null"
                    }
                  ]
                },
                "period_end_at": {
                  "anyOf": [
                    {
                      "type": "string",
                      "format": "date-time",
                      "pattern": "Z$"
                    },
                    {
                      "type": "null"
                    }
                  ]
                }
              },
              "required": [
                "id",
                "parameter_code",
                "native_value",
                "native_unit",
                "value",
                "unit",
                "conversion_code",
                "value_status",
                "detection_limit",
                "ingested_at",
                "quality_status",
                "kind",
                "valid_at",
                "temporal_support",
                "interval_status",
                "period_start_at",
                "period_end_at"
              ]
            }
          }
        }
      }
    }
  ]
}
```

### C03 A1 device packet

| Attribute | Definition |
| --- | --- |
| Producer → consumer | device/simulator → temperature handler + seagis_api.ingest |
| Interface / format | JSON / HTTP POST |
| Classification | explicit |
| Database mapping | observation + raw_payload + packet_receipt + quality_event |
| Compatibility | Constant version where defined; general negotiation NOT FOUND |
| Evidence | `Seagis-Model/supabase/functions/temperature/handler.ts:1` |

| Field | Type / ref | Required | Nullable | Default | Meaning | Validation / allowed values | Units / timestamp | Example (illustrative) | DB mapping (boundary) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| schema_version | "const/enum" | True | False | NOT FOUND | Contract structure version; not a biological model version | {"const": "1.0.0"} | NOT APPLICABLE / schema | "1.0.0" | observation + raw_payload + packet_receipt + quality_event |
| sensor_id | "string" | True | False | NOT FOUND | Sensor deployment reference | {"type": "string", "format": "uuid"} | NOT APPLICABLE / schema | "00000000-0000-4000-8000-000000000001" | observation + raw_payload + packet_receipt + quality_event |
| boot_id | "string" | True | False | NOT FOUND | Sensor boot-session identity for idempotency | {"type": "string", "pattern": "^[A-Za-z0-9._-]{1,64}$"} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | observation + raw_payload + packet_receipt + quality_event |
| sequence | "integer" | True | False | NOT FOUND | uint32 counter within one boot; key combined with boot_id | {"type": "integer", "minimum": 0, "maximum": 4294967295} | NOT APPLICABLE / schema | 1 | observation + raw_payload + packet_receipt + quality_event |
| observed_at | "string" | True | False | NOT FOUND | Sensor measurement instant, distinct from receipt | {"type": "string", "format": "date-time", "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(\\.\\d{1,6})?Z$"} | Units/time follow unit and parameter registry; UTC for normalized envelopes. | "2026-10-21T12:00:00Z" | observation + raw_payload + packet_receipt + quality_event |
| water_temperature | ["number", "null"] | True | True | NOT FOUND | Water temperature in degC or null missing; distinct from air temperature | {"type": ["number", "null"]} | NOT APPLICABLE / schema | null | observation + raw_payload + packet_receipt + quality_event |
| unit | "const/enum" | True | False | NOT FOUND | Normalized value unit from registry | {"const": "degC"} | NOT APPLICABLE / schema | "degC" | observation + raw_payload + packet_receipt + quality_event |
| value_status | "const/enum" | True | False | NOT FOUND | Numeric availability, separate from quality | {"enum": ["present", "missing"]} | NOT APPLICABLE / schema | "present" | observation + raw_payload + packet_receipt + quality_event |

Complete schema for conditional rules and polymorphic structures (required above applies within each parent):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://seagis.local/contracts/iot-packet/1.0.0",
  "title": "SEAGIS temperature packet 1.0.0",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "sensor_id",
    "boot_id",
    "sequence",
    "observed_at",
    "water_temperature",
    "unit",
    "value_status"
  ],
  "properties": {
    "schema_version": {
      "const": "1.0.0"
    },
    "sensor_id": {
      "type": "string",
      "format": "uuid"
    },
    "boot_id": {
      "type": "string",
      "pattern": "^[A-Za-z0-9._-]{1,64}$"
    },
    "sequence": {
      "type": "integer",
      "minimum": 0,
      "maximum": 4294967295
    },
    "observed_at": {
      "type": "string",
      "format": "date-time",
      "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(\\.\\d{1,6})?Z$"
    },
    "water_temperature": {
      "type": [
        "number",
        "null"
      ]
    },
    "unit": {
      "const": "degC"
    },
    "value_status": {
      "enum": [
        "present",
        "missing"
      ]
    }
  },
  "allOf": [
    {
      "if": {
        "properties": {
          "value_status": {
            "const": "present"
          }
        }
      },
      "then": {
        "properties": {
          "water_temperature": {
            "type": "number"
          }
        }
      },
      "else": {
        "properties": {
          "water_temperature": {
            "type": "null"
          }
        }
      }
    }
  ]
}
```

### C04 A3 alignment document

| Attribute | Definition |
| --- | --- |
| Producer → consumer | scripts/quality/alignment.py::build → seagis_quality.save_snapshot |
| Interface / format | JSON / SQL jsonb |
| Classification | explicit |
| Database mapping | seagis_quality.alignment_snapshot + snapshot_input |
| Compatibility | Constant version where defined; general negotiation NOT FOUND |
| Evidence | `Seagis-Model/scripts/curate_environment.py:1` |

| Field | Type / ref | Required | Nullable | Default | Meaning | Validation / allowed values | Units / timestamp | Example (illustrative) | DB mapping (boundary) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| schema_version | "const/enum" | True | False | NOT FOUND | Contract structure version; not a biological model version | {"const": "a3-alignment-1"} | NOT APPLICABLE / schema | "a3-alignment-1" | seagis_quality.alignment_snapshot + snapshot_input |
| builder_version | "string" | True | False | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "string", "minLength": 1} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | seagis_quality.alignment_snapshot + snapshot_input |
| policy_version | "string" | True | False | NOT FOUND | QC policy version reference | {"type": "string", "minLength": 1} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | seagis_quality.alignment_snapshot + snapshot_input |
| policy_sha256 | "#/$defs/hash" | True | False | NOT FOUND | Policy-content digest | {"$ref": "#/$defs/hash"} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | seagis_quality.alignment_snapshot + snapshot_input |
| code_sha256 | "#/$defs/hash" | True | False | NOT FOUND | Alignment-builder source digest | {"$ref": "#/$defs/hash"} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | seagis_quality.alignment_snapshot + snapshot_input |
| source_sha256 | "#/$defs/hash" | True | False | NOT FOUND | Source-bundle digest for source-change detection | {"$ref": "#/$defs/hash"} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | seagis_quality.alignment_snapshot + snapshot_input |
| plot_id | "string" | True | False | NOT FOUND | Cultivation plot reference | {"type": "string", "format": "uuid"} | NOT APPLICABLE / schema | "00000000-0000-4000-8000-000000000001" | seagis_quality.alignment_snapshot + snapshot_input |
| mode | "const/enum" | True | False | NOT FOUND | demo_review or operational_review according to plot provenance | {"enum": ["demo_review", "operational_review"]} | NOT APPLICABLE / schema | "demo_review" | seagis_quality.alignment_snapshot + snapshot_input |
| use | "const/enum" | True | False | NOT FOUND | Document use restriction quality_alignment_review | {"const": "quality_alignment_review"} | NOT APPLICABLE / schema | "quality_alignment_review" | seagis_quality.alignment_snapshot + snapshot_input |
| training_authorized | "const/enum" | True | False | NOT FOUND | Must be false; review/demo is not an approved training dataset | {"const": false} | NOT APPLICABLE / schema | false | seagis_quality.alignment_snapshot + snapshot_input |
| source_registry | "array" | True | False | NOT FOUND | Parameter-contract copy checked against the SQL bundle | {"type": "array", "minItems": 1} | NOT APPLICABLE / schema | [] | seagis_quality.alignment_snapshot + snapshot_input |
| source_registry[] | "object" | True | False | NOT FOUND | Parameter-contract copy checked against the SQL bundle | {"type": "object", "required": ["dataset_key", "parameter_code", "native_unit", "unit", "conversion_code", "native_cadence_seconds", "attribution", "licence_url"]} | NOT APPLICABLE / schema | {} | seagis_quality.alignment_snapshot + snapshot_input |
| sensor_deployments | "array" | True | False | NOT FOUND | Deployment-identity copy for consistency checks | {"type": "array"} | NOT APPLICABLE / schema | [] | seagis_quality.alignment_snapshot + snapshot_input |
| sensor_deployments[] | "object" | True | False | NOT FOUND | Deployment-identity copy for consistency checks | {"type": "object"} | NOT APPLICABLE / schema | {} | seagis_quality.alignment_snapshot + snapshot_input |
| start_at | "string" | True | False | NOT FOUND | Inclusive alignment-window start | {"type": "string", "format": "date-time"} | Units/time follow unit and parameter registry; UTC for normalized envelopes. | "2026-10-21T12:00:00Z" | seagis_quality.alignment_snapshot + snapshot_input |
| end_at | "string" | True | False | NOT FOUND | Exclusive alignment-window end | {"type": "string", "format": "date-time"} | Units/time follow unit and parameter registry; UTC for normalized envelopes. | "2026-10-21T12:00:00Z" | seagis_quality.alignment_snapshot + snapshot_input |
| rows | "array" | True | False | NOT FOUND | UTC hourly context rows; not additional independent samples | {"type": "array", "minItems": 1, "maxItems": 168} | NOT APPLICABLE / schema | [] | seagis_quality.alignment_snapshot + snapshot_input |
| rows[] | "object" | True | False | NOT FOUND | UTC hourly context rows; not additional independent samples | {"type": "object", "required": ["at", "cells"], "additionalProperties": false} | NOT APPLICABLE / schema | {} | seagis_quality.alignment_snapshot + snapshot_input |
| rows[].at | "string" | True | False | NOT FOUND | UTC hourly cutoff for context selection | {"type": "string", "format": "date-time"} | NOT APPLICABLE / schema | "2026-10-21T12:00:00Z" | seagis_quality.alignment_snapshot + snapshot_input |
| rows[].cells | "array" | True | False | NOT FOUND | Per-dataset/parameter context at the hourly cutoff | {"type": "array", "minItems": 1} | NOT APPLICABLE / schema | [] | seagis_quality.alignment_snapshot + snapshot_input |
| rows[].cells[] | "#/$defs/cell" | True | False | NOT FOUND | Per-dataset/parameter context at the hourly cutoff | {"$ref": "#/$defs/cell"} | NOT APPLICABLE / schema | {} | seagis_quality.alignment_snapshot + snapshot_input |
| quality_report | "object" | True | False | NOT FOUND | QC summary and coverage based on hourly context | {"type": "object", "required": ["plot_id", "start_at", "end_at", "coverage_basis", "drift_assessment", "parameters"]} | NOT APPLICABLE / schema | {} | seagis_quality.alignment_snapshot + snapshot_input |
| quality_report.plot_id | "string" | True | False | NOT FOUND | Cultivation plot reference | {"type": "string", "format": "uuid"} | NOT APPLICABLE / schema | "00000000-0000-4000-8000-000000000001" | seagis_quality.alignment_snapshot + snapshot_input |
| quality_report.start_at | "string" | True | False | NOT FOUND | Inclusive alignment-window start | {"type": "string", "format": "date-time"} | Units/time follow unit and parameter registry; UTC for normalized envelopes. | "2026-10-21T12:00:00Z" | seagis_quality.alignment_snapshot + snapshot_input |
| quality_report.end_at | "string" | True | False | NOT FOUND | Exclusive alignment-window end | {"type": "string", "format": "date-time"} | Units/time follow unit and parameter registry; UTC for normalized envelopes. | "2026-10-21T12:00:00Z" | seagis_quality.alignment_snapshot + snapshot_input |
| quality_report.coverage_basis | "string" | True | False | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "string"} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | seagis_quality.alignment_snapshot + snapshot_input |
| quality_report.drift_assessment | "const/enum" | True | False | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"const": "not_assessable_without_calibrated_colocated_reference"} | NOT APPLICABLE / schema | "not_assessable_without_calibrated_colocated_reference" | seagis_quality.alignment_snapshot + snapshot_input |
| quality_report.parameters | "array" | True | False | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "array"} | NOT APPLICABLE / schema | [] | seagis_quality.alignment_snapshot + snapshot_input |
| quality_report.parameters[] | "object" | True | False | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "object", "required": ["dataset_key", "parameter_code", "expected_hourly_contexts", "usable_contexts", "unique_selected_source_records", "native_cadence_seconds", "coverage_fraction", "value_status_counts", "flag_counts", "input_qc_flag_counts_at_final_cutoff"]} | NOT APPLICABLE / schema | {} | seagis_quality.alignment_snapshot + snapshot_input |
| quality_report.parameters[].expected_hourly_contexts | "integer" | True | False | NOT FOUND | Hourly slots in window, not native sample count | {"type": "integer", "minimum": 1} | NOT APPLICABLE / schema | 1 | seagis_quality.alignment_snapshot + snapshot_input |
| quality_report.parameters[].usable_contexts | "integer" | True | False | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "integer", "minimum": 0} | NOT APPLICABLE / schema | 1 | seagis_quality.alignment_snapshot + snapshot_input |
| quality_report.parameters[].unique_selected_source_records | "integer" | True | False | NOT FOUND | Count of distinct selected source records | {"type": "integer", "minimum": 0} | NOT APPLICABLE / schema | 1 | seagis_quality.alignment_snapshot + snapshot_input |
| quality_report.parameters[].coverage_fraction | "number" | True | False | NOT FOUND | usable_contexts / expected_hourly_contexts | {"type": "number", "minimum": 0, "maximum": 1} | NOT APPLICABLE / schema | 0 | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.hash | "string" | False | False | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "string", "pattern": "^[0-9a-f]{64}$"} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.nullableTime | ["string", "null"] | False | True | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": ["string", "null"], "format": "date-time"} | NOT APPLICABLE / schema | null | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell | "object" | False | False | NOT FOUND | UNVERIFIED: contract structure/field; detailed meaning follows validator and source examples, not fully verified | {"type": "object", "required": ["dataset_key", "parameter_code", "scope", "native_cadence_seconds", "source_id", "value", "value_status", "unit", "source_time", "available_at", "age_seconds", "vintage_age_seconds", "lineage", "spatial", "flags", "blocking_flags", "usable_context"]} | NOT APPLICABLE / schema | {} | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.dataset_key | "string" | True | False | NOT FOUND | Registered dataset key | {"type": "string"} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.parameter_code | "string" | True | False | NOT FOUND | Environmental parameter identity | {"type": "string"} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.scope | "const/enum" | True | False | NOT FOUND | Origin: local_sensor or regional_model | {"enum": ["local_sensor", "regional_model"]} | NOT APPLICABLE / schema | "local_sensor" | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.native_cadence_seconds | "integer" | True | False | NOT FOUND | Native sample cadence, distinct from fetch interval | {"type": "integer", "minimum": 1} | NOT APPLICABLE / schema | 1 | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.source_id | ["string", "null"] | True | True | NOT FOUND | Typed reference to selected source record, or null | {"type": ["string", "null"], "pattern": "^(observation&#124;forecast_value):[0-9a-f-]{36}$"} | NOT APPLICABLE / schema | null | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.value | ["number", "null"] | True | True | NOT FOUND | Normalized value; null follows value_status | {"type": ["number", "null"]} | Units/time follow unit and parameter registry; UTC for normalized envelopes. | null | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.native_value | ["number", "null"] | False | True | NOT FOUND | Physical value in source units | {"type": ["number", "null"]} | Units/time follow unit and parameter registry; UTC for normalized envelopes. | null | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.value_status | "const/enum" | True | False | NOT FOUND | Numeric availability, separate from quality | {"enum": ["present", "missing", "below_detection_limit", "not_available"]} | NOT APPLICABLE / schema | "present" | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.unit | "string" | True | False | NOT FOUND | Normalized value unit from registry | {"type": "string"} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.source_time | "#/$defs/nullableTime" | True | True | NOT FOUND | Sensor observed_at or model valid_at | {"$ref": "#/$defs/nullableTime"} | Units/time follow unit and parameter registry; UTC for normalized envelopes. | null | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.available_at | "#/$defs/nullableTime" | True | True | NOT FOUND | Conservative input availability time | {"$ref": "#/$defs/nullableTime"} | Units/time follow unit and parameter registry; UTC for normalized envelopes. | null | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.age_seconds | ["number", "null"] | True | True | NOT FOUND | Age of source_time relative to cutoff in seconds | {"type": ["number", "null"], "minimum": 0} | NOT APPLICABLE / schema | null | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.vintage_age_seconds | ["number", "null"] | True | True | NOT FOUND | Run age relative to cutoff in seconds | {"type": ["number", "null"], "minimum": 0} | NOT APPLICABLE / schema | null | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.lineage | "array" | True | False | NOT FOUND | Typed references to selected records and supporting QC inputs | {"type": "array", "uniqueItems": true} | NOT APPLICABLE / schema | [] | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.lineage[] | "string" | True | False | NOT FOUND | Typed references to selected records and supporting QC inputs | {"type": "string", "pattern": "^(observation&#124;forecast_value):[0-9a-f-]{36}$"} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.spatial | ["object", "null"] | True | True | NOT FOUND | Grid mapping, resolution, distance and depth metadata | {"type": ["object", "null"]} | NOT APPLICABLE / schema | null | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.flags | "array" | True | False | NOT FOUND | QC codes from packet acceptance | {"type": "array", "uniqueItems": true} | NOT APPLICABLE / schema | [] | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.flags[] | "string" | True | False | NOT FOUND | QC codes from packet acceptance | {"type": "string"} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.blocking_flags | "array" | True | False | NOT FOUND | Reasons context is unusable under the builder | {"type": "array", "uniqueItems": true} | NOT APPLICABLE / schema | [] | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.blocking_flags[] | "string" | True | False | NOT FOUND | Reasons context is unusable under the builder | {"type": "string"} | NOT APPLICABLE / schema | "See complete fixture/schema; standalone field example unverified" | seagis_quality.alignment_snapshot + snapshot_input |
| $defs.cell.usable_context | "boolean" | True | False | NOT FOUND | Builder QC decision for review; not training authorization | {"type": "boolean"} | NOT APPLICABLE / schema | false | seagis_quality.alignment_snapshot + snapshot_input |

Complete schema for conditional rules and polymorphic structures (required above applies within each parent):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://seagis.local/contracts/alignment.schema.json",
  "title": "A3 quality and hourly alignment snapshot",
  "type": "object",
  "required": [
    "schema_version",
    "builder_version",
    "policy_version",
    "policy_sha256",
    "code_sha256",
    "source_sha256",
    "plot_id",
    "mode",
    "use",
    "training_authorized",
    "source_registry",
    "sensor_deployments",
    "start_at",
    "end_at",
    "rows",
    "quality_report"
  ],
  "additionalProperties": false,
  "properties": {
    "schema_version": {
      "const": "a3-alignment-1"
    },
    "builder_version": {
      "type": "string",
      "minLength": 1
    },
    "policy_version": {
      "type": "string",
      "minLength": 1
    },
    "policy_sha256": {
      "$ref": "#/$defs/hash"
    },
    "code_sha256": {
      "$ref": "#/$defs/hash"
    },
    "source_sha256": {
      "$ref": "#/$defs/hash"
    },
    "plot_id": {
      "type": "string",
      "format": "uuid"
    },
    "mode": {
      "enum": [
        "demo_review",
        "operational_review"
      ]
    },
    "use": {
      "const": "quality_alignment_review"
    },
    "training_authorized": {
      "const": false
    },
    "source_registry": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "dataset_key",
          "parameter_code",
          "native_unit",
          "unit",
          "conversion_code",
          "native_cadence_seconds",
          "attribution",
          "licence_url"
        ]
      }
    },
    "sensor_deployments": {
      "type": "array",
      "items": {
        "type": "object"
      }
    },
    "start_at": {
      "type": "string",
      "format": "date-time"
    },
    "end_at": {
      "type": "string",
      "format": "date-time"
    },
    "rows": {
      "type": "array",
      "minItems": 1,
      "maxItems": 168,
      "items": {
        "type": "object",
        "required": [
          "at",
          "cells"
        ],
        "additionalProperties": false,
        "properties": {
          "at": {
            "type": "string",
            "format": "date-time"
          },
          "cells": {
            "type": "array",
            "minItems": 1,
            "items": {
              "$ref": "#/$defs/cell"
            }
          }
        }
      }
    },
    "quality_report": {
      "type": "object",
      "required": [
        "plot_id",
        "start_at",
        "end_at",
        "coverage_basis",
        "drift_assessment",
        "parameters"
      ],
      "properties": {
        "plot_id": {
          "type": "string",
          "format": "uuid"
        },
        "start_at": {
          "type": "string",
          "format": "date-time"
        },
        "end_at": {
          "type": "string",
          "format": "date-time"
        },
        "coverage_basis": {
          "type": "string"
        },
        "drift_assessment": {
          "const": "not_assessable_without_calibrated_colocated_reference"
        },
        "parameters": {
          "type": "array",
          "items": {
            "type": "object",
            "required": [
              "dataset_key",
              "parameter_code",
              "expected_hourly_contexts",
              "usable_contexts",
              "unique_selected_source_records",
              "native_cadence_seconds",
              "coverage_fraction",
              "value_status_counts",
              "flag_counts",
              "input_qc_flag_counts_at_final_cutoff"
            ],
            "properties": {
              "expected_hourly_contexts": {
                "type": "integer",
                "minimum": 1
              },
              "usable_contexts": {
                "type": "integer",
                "minimum": 0
              },
              "unique_selected_source_records": {
                "type": "integer",
                "minimum": 0
              },
              "coverage_fraction": {
                "type": "number",
                "minimum": 0,
                "maximum": 1
              }
            }
          }
        }
      }
    }
  },
  "$defs": {
    "hash": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$"
    },
    "nullableTime": {
      "type": [
        "string",
        "null"
      ],
      "format": "date-time"
    },
    "cell": {
      "type": "object",
      "required": [
        "dataset_key",
        "parameter_code",
        "scope",
        "native_cadence_seconds",
        "source_id",
        "value",
        "value_status",
        "unit",
        "source_time",
        "available_at",
        "age_seconds",
        "vintage_age_seconds",
        "lineage",
        "spatial",
        "flags",
        "blocking_flags",
        "usable_context"
      ],
      "properties": {
        "dataset_key": {
          "type": "string"
        },
        "parameter_code": {
          "type": "string"
        },
        "scope": {
          "enum": [
            "local_sensor",
            "regional_model"
          ]
        },
        "native_cadence_seconds": {
          "type": "integer",
          "minimum": 1
        },
        "source_id": {
          "type": [
            "string",
            "null"
          ],
          "pattern": "^(observation|forecast_value):[0-9a-f-]{36}$"
        },
        "value": {
          "type": [
            "number",
            "null"
          ]
        },
        "native_value": {
          "type": [
            "number",
            "null"
          ]
        },
        "value_status": {
          "enum": [
            "present",
            "missing",
            "below_detection_limit",
            "not_available"
          ]
        },
        "unit": {
          "type": "string"
        },
        "source_time": {
          "$ref": "#/$defs/nullableTime"
        },
        "available_at": {
          "$ref": "#/$defs/nullableTime"
        },
        "age_seconds": {
          "type": [
            "number",
            "null"
          ],
          "minimum": 0
        },
        "vintage_age_seconds": {
          "type": [
            "number",
            "null"
          ],
          "minimum": 0
        },
        "lineage": {
          "type": "array",
          "uniqueItems": true,
          "items": {
            "type": "string",
            "pattern": "^(observation|forecast_value):[0-9a-f-]{36}$"
          }
        },
        "spatial": {
          "type": [
            "object",
            "null"
          ]
        },
        "flags": {
          "type": "array",
          "uniqueItems": true,
          "items": {
            "type": "string"
          }
        },
        "blocking_flags": {
          "type": "array",
          "uniqueItems": true,
          "items": {
            "type": "string"
          }
        },
        "usable_context": {
          "type": "boolean"
        }
      }
    }
  }
}
```

### C05 A1 history/status/replies

| Attribute | Definition |
| --- | --- |
| Producer → consumer | seagis_api.history/status/reply → authorized reader |
| Interface / format | JSON / HTTP GET |
| Classification | implementation-derived |
| Database mapping | observation + sensor + packet_receipt |
| Compatibility | Constant version where defined; general negotiation NOT FOUND |
| Evidence | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:1` |

| Field / group | Type / required | Meaning / validation / mapping |
| --- | --- | --- |
| from, to | string / required | UTC Z; from<to; <=7 days; observation.observed_at [from,to) |
| limit | integer string / optional; default 200 | 1..500 |
| cursor | UUID / optional | observation.id inside plot/window; ordering observed_at,id |
| code, request_id | string, UUID / response | SQL reply / handler error |
| observations[] | array / history response | id,sensor_id,value,unit,value_status,observed_at,ingested_at,quality_status,flags,ingestion_run_id,is_synthetic |
| coverage | object | expected_hours,hours_with_packets,hours_with_usable_values,missing_hours,unusable_hours |
| next_cursor | UUID&#124;null | last returned row if another page exists |

### C06 A2 adapter batch/lease

| Attribute | Definition |
| --- | --- |
| Producer → consumer | Adapter.envelope + claim → seagis_environment.persist |
| Interface / format | JSON / SQL jsonb |
| Classification | implementation-derived |
| Database mapping | raw_payload + forecast_run + forecast_value + source_grid + demo_grid_mapping |
| Compatibility | Constant version where defined; general negotiation NOT FOUND |
| Evidence | `Seagis-Model/scripts/environmental/common.py:1` |

| Field | Required | Validation / mapping |
| --- | --- | --- |
| dataset_key | True | Registered dataset key; raw_payload + forecast_run + forecast_value + source_grid + demo_grid_mapping |
| purpose | True | Purpose noncommercial_educational_prototype; raw_payload + forecast_run + forecast_value + source_grid + demo_grid_mapping |
| terms_review | True | Provider terms review identity; raw_payload + forecast_run + forecast_value + source_grid + demo_grid_mapping |
| dataset_version | True | Pinned dataset version; raw_payload + forecast_run + forecast_value + source_grid + demo_grid_mapping |
| provider_dataset_id | True | Original provider dataset identity; raw_payload + forecast_run + forecast_value + source_grid + demo_grid_mapping |
| run_key | True | Semantic capture identity per dataset; raw_payload + forecast_run + forecast_value + source_grid + demo_grid_mapping |
| raw_sha256 | True | See persist/envelope; raw_payload + forecast_run + forecast_value + source_grid + demo_grid_mapping |
| raw_byte_size | True | See persist/envelope; raw_payload + forecast_run + forecast_value + source_grid + demo_grid_mapping |
| hash_basis | True | Byte or serialization convention used for hashing; raw_payload + forecast_run + forecast_value + source_grid + demo_grid_mapping |
| format | True | Raw representation media type or format; raw_payload + forecast_run + forecast_value + source_grid + demo_grid_mapping |
| started_at | True | Ingestion or attempt start instant; raw_payload + forecast_run + forecast_value + source_grid + demo_grid_mapping |
| received_at | True | Raw receipt instant at worker; raw_payload + forecast_run + forecast_value + source_grid + demo_grid_mapping |
| metadata | True | See persist/envelope; raw_payload + forecast_run + forecast_value + source_grid + demo_grid_mapping |
| grids | True | See persist/envelope; raw_payload + forecast_run + forecast_value + source_grid + demo_grid_mapping |
| mappings | True | See persist/envelope; raw_payload + forecast_run + forecast_value + source_grid + demo_grid_mapping |
| values | True | See persist/envelope; raw_payload + forecast_run + forecast_value + source_grid + demo_grid_mapping |

Nested grids contain key, latitude, longitude, depth_m and identity_basis; values contain grid_key, parameter, value, native_unit, unit, conversion_code, value_status, valid_at, temporal_support, interval_status and period bounds. Mappings carry plot identity and example distance. SQL checks envelope field presence, lease, purpose/licence, 64-hex hashes and grid/value/mapping counts; this is not a universal JSON Schema.

### C07 A3 source_bundle

| Attribute | Definition |
| --- | --- |
| Producer → consumer | seagis_quality.source_bundle → build / CSV exporter |
| Interface / format | JSON / SQL jsonb |
| Classification | implementation-derived |
| Database mapping | plot + sensor + dataset_parameter + mappings + observation + forecast_value |
| Compatibility | Constant version where defined; general negotiation NOT FOUND |
| Evidence | `Seagis-Model/supabase/migrations/0005_quality_alignment.sql:1` |

| Field | Type / required | Mapping |
| --- | --- | --- |
| schema_version | constant a3-source-1 | internal |
| plot | object | seagis.plot |
| start_at,end_at | timestamptz / required | query bounds |
| sensors | array | seagis.sensor |
| parameters | array | dataset_parameter + dataset + environment.policy |
| mappings | array | plot_grid_mapping + demo_grid_mapping + source_grid |
| records | array | observation + forecast_value + quality_event |
| source_sha256 | 64-hex string | seagis.jsonb_sha256(bundle) |

### C08 CSV experiment-csv-2

| Attribute | Definition |
| --- | --- |
| Producer → consumer | export_experiment_csv.py::export → offline experiments / developer |
| Interface / format | CSV + JSON manifest |
| Classification | implementation-derived |
| Database mapping | derived files; no database writes |
| Compatibility | Constant version where defined; general negotiation NOT FOUND |
| Evidence | `Seagis-Model/scripts/export_experiment_csv.py:1` |

Manifest export_version=experiment-csv-2 records capture/export times, bounds, units, unique record counts, CSV counts and per-file checksums. Temperature CSV carries timestamp_utc, timestamp_wib, plot_id, value, raw_value, gap/synthetic/QC fields, observation_id, available_at_utc, training_authorized=false, parameter_code, unit, source_kind and value_policy. Regional CSV carries flattened source-record fields, cadence, attribution, licence_url, selection_basis and capture_at_utc. Dynamic source fields mean the CSV schema follows bundle records rather than a universal fixed column contract.

### C09 iOS Assessment domain

| Attribute | Definition |
| --- | --- |
| Producer → consumer | MockAssessmentRepository → LoadDemoAssessment / ViewModel |
| Interface / format | Swift structs |
| Classification | implementation-derived / mock |
| Database mapping | NOT APPLICABLE: no backend mapping |
| Compatibility | Constant version where defined; general negotiation NOT FOUND |
| Evidence | `Seagis/Seagis/Models/Shared/Assessment.swift:1` |

| Swift field | Type | Required | Meaning / mapping |
| --- | --- | --- | --- |
| id | String | True | Row identity under the table primary key |
| plotID | String | True | Demo domain field; not a backend DTO |
| title | String | True | Demo domain field; not a backend DTO |
| summary | String | True | Demo domain field; not a backend DTO |
| provenance | AssessmentProvenance.syntheticFixture | True | Demo domain field; not a backend DTO |
| evidenceIDs | [String] | True | Demo domain field; not a backend DTO |

### C10 Open-Meteo response

| Attribute | Definition |
| --- | --- |
| Producer → consumer | Open-Meteo forecast API → OpenMeteo.parse/normalize |
| Interface / format | JSON hourly arrays |
| Classification | implementation-derived |
| Database mapping | forecast_value + grid + raw manifest |
| Compatibility | Constant version where defined; general negotiation NOT FOUND |
| Evidence | `Seagis-Model/scripts/environmental/open_meteo.py:1` |

Response must be a list matching the two plots, each item carrying latitude/longitude/elevation, timezone UTC/GMT, utc_offset_seconds=0, hourly_units.time=iso8601 and aligned hourly arrays. Variable fields and units come from a2_sources.json. generationtime_ms is not issue time. Null/numeric handling follows common.point. No stable provider response_error format is claimed.

### C11 Copernicus subset

| Attribute | Definition |
| --- | --- |
| Producer → consumer | Copernicus Toolbox/xarray + STAC → Copernicus.parse/normalize |
| Interface / format | xarray + canonical logical JSON subset |
| Classification | implementation-derived |
| Database mapping | forecast_value + grid + raw manifest |
| Compatibility | Constant version where defined; general negotiation NOT FOUND |
| Evidence | `Seagis-Model/scripts/environmental/copernicus.py:1` |

STAC requires id, collection/product, cube:dimensions time/elevation/latitude/longitude and cube:variables unit/standardName. The xarray dataset has one latitude/longitude/depth and unique ordered times at native cadence; variables are transposed time,depth,latitude,longitude. The logical subset contains cell,time,variables,native_units and is not a provider wire format. Unknown original metadata is not fabricated.

### HTTP routes and responses

| Method | Path (temperature base) | Auth | Result / errors |
| --- | --- | --- | --- |
| GET | /health | none | 200 service=seagis-temperature, version=1.0.0 |
| POST | /v1/ingest | device Bearer | 201 stored; 200 duplicate; 409 packet_conflict; 422 invalid_packet; 403 sensor_forbidden/sensor_inactive; 503 commissioning_disabled |
| GET | /v1/plots/{plot_id}/temperature | reader Bearer + reader_plot | 200 observations/coverage; 400 invalid_query/invalid_plot_id; 403 plot_forbidden |
| GET | /v1/status | reader Bearer | 200 checked_at,stale_after_seconds,plots[] |
| all | known protected paths | Bearer sgi_ pattern | 401 unauthorized; 429 rate_limited |
| all | HTTP boundary | handler | 404 not_found; 405 method_not_allowed; 415 json_required; 413 payload_too_large; 400 invalid_json/empty_body/unexpected_query; 503 temporarily_unavailable |

Deployment base /functions/v1/temperature; the handler also accepts a /temperature prefix. Responses use no-store. Retry-After is 60 for 429 and 5 for 503. Status plots[] contains plot_id,plot_code,is_synthetic,latest_usable_observed_at,last_ingested_at,age_seconds,stale,observations_last_24h,rejected_last_24h. last_ingested_at need not belong to the latest_usable_observed_at record. Null time/age means unavailable.

### A1 payloads and errors

Synthetic structurally valid example; persistence requires a registered credential/sensor and active policy.
```json
{
  "schema_version": "1.0.0",
  "sensor_id": "00000000-0000-4000-8000-000000000101",
  "boot_id": "synthetic-boot-a",
  "sequence": 1,
  "observed_at": "2026-10-21T12:00:00Z",
  "water_temperature": 29.2,
  "unit": "degC",
  "value_status": "present"
}
```

Invalid example: change unit to kelvin. SQL returns 422 invalid_packet after successful authentication.
```json
{
  "code": "invalid_packet",
  "request_id": "00000000-0000-4000-8000-000000000999"
}
```

A stored response has observation_id, ingestion_run_id, observed_at, quality_status, flags, is_synthetic, code and request_id. UUIDs/times below are illustrative, not a live response.
```json
{
  "observation_id": "00000000-0000-4000-8000-000000000201",
  "ingestion_run_id": "00000000-0000-4000-8000-000000000301",
  "observed_at": "2026-10-21T12:00:00.000000Z",
  "quality_status": "accepted",
  "flags": [],
  "is_synthetic": true,
  "code": "stored",
  "request_id": "00000000-0000-4000-8000-000000000999"
}
```

| Boundary | Rule / discrepancy | Classification | Evidence |
| --- | --- | --- | --- |
| A0 vs A1 packet | A0 fixture uses a 0.1.0 envelope and detection_limit; A1 accepts exactly eight 1.0.0 fields and rejects extras. | VERIFIED | `Seagis-Model/contracts/iot-packet.schema.json:1` |
| A0 run_kind vs A2 | 0003 extends run_kind with analysis_forecast_unspecified; do not rely on the old A0 list. | VERIFIED | `Seagis-Model/supabase/migrations/0003_environment_ingestion.sql:1` |
| A3 JSON schema vs runtime | Tests validate the full schema; curate/build does not call a general JSON Schema validator and SQL enforces selected checks. | VERIFIED | `Seagis-Model/scripts/curate_environment.py:1` |
| API time vs PostgreSQL | A1 UTC Z; timestamptz session display / microseconds | VERIFIED | `Seagis-Model/supabase/migrations/0002_temperature_api.sql:1` |
| iOS Assessment vs DB | No verified backend assessment DTO/contract. | NOT FOUND | `Seagis/Seagis/Models/Shared/Assessment.swift:1` |

