# Agent Instruction — Pulau Tidung Ocean-Only NASA Data Integration

## Objective
Integrate **real, ocean-specific NASA observations** into the **existing iOS SwiftUI app** for seaweed cultivation environmental monitoring near Pulau Tidung, Kepulauan Seribu. Preserve the current architecture, screens, and low-fidelity/minimal visual design. Do not rebuild the app or invent disease predictions.

## Strict scope
**Include:**
1. **MUR GHRSST Level-4 SST**, ~0.01° / 1 km, daily, as the primary temperature time series. This is an analyzed, gap-filled ocean temperature product; clearly label it as such rather than a direct pixel measurement.
2. **VIIRS ocean-color products**, for chlorophyll-a and water optical properties (e.g., Kd490 and/or remote-sensing reflectance, depending on available validated products). Check exact platform, processing level, variable, units, and actual resolution in the collection metadata. Prefer high-resolution Level-2 swaths for spatial detail where available; Level-3 mapped products can be used for time series if suitable.
3. **PACE OCI ocean-color products**, for chlorophyll-a and spectral reflectance as an independent comparison source. Check Level-2 (~1.2 km nominal) vs Level-3 resolution and quality flags. Do not silently merge PACE and VIIRS.

**Exclude:** ECOSTRESS land surface temperature, NASA POWER solar radiation, GPM IMERG rainfall, SMAP salinity, terrestrial land-surface products, and all synthetic environmental values in production mode. Do not add a generic weather API.

## Scientific constraints
- Target is **coastal water**, not land. Use a reference coordinate near Pulau Tidung (~-5.80, 106.50) only as an initial search seed; locate actual farm plot coordinates from the existing app configuration if present. Never claim the seed is a verified farm site.
- Test a coastal bounding box initially [106.40, -5.90, 106.60, -5.70], then refine using the configured plots.
- A nominal 750 m–1 km pixel is **not** a 750 m–1 km accuracy guarantee. Reject land-contaminated, cloud-contaminated, shallow-bottom-affected, or otherwise invalid ocean-color pixels based on product quality flags. If a valid nearshore pixel is unavailable, return missing data with a reason.
- Record selected pixel coordinates, distance from the plot, acquisition time, temporal aggregation window, product ID/version, units, resolution, and QA flags.
- Kd490 is a **diffuse light attenuation coefficient**, not a direct turbidity measurement. Label it “water clarity proxy / Kd490,” not NTU. Reflectance is also not turbidity in NTU without a calibrated algorithm.
- Chlorophyll-a is not a direct measure of seaweed biomass or ice-ice disease.
- No ice-ice probability, thresholds, or warning levels without validated labeled evidence.

## Phase 0 — Repository reconnaissance
1. Inspect the existing Xcode project, package modules, `CultivationPlot`, `EnvironmentalObservation`, `MonitorViewModel`, and views (including history and map).
2. Report the current data source, mocks, network abstractions, model fields, and screens that need updates.
3. Make the smallest compatible changes. Preserve existing navigation and layout.

## Phase 1 — Verify NASA collections and access
Use official sources:
- PO.DAAC: https://podaac.jpl.nasa.gov/
- NASA Earthdata CMR: https://cmr.earthdata.nasa.gov/search/
- NASA Ocean Biology DAAC: https://oceandata.sci.gsfc.nasa.gov/
- Ocean Color: https://oceancolor.gsfc.nasa.gov/
- earthaccess Python: https://earthaccess.readthedocs.io/

Find exact collection IDs/short names through CMR rather than guessing endpoint URLs. Verify dataset version, access requirements, latency, file formats, and coverage for Pulau Tidung for a sample month in 2025 and a recent available month. Verify whether Level-2 ocean-color coverage and valid water pixels actually exist. Produce `docs/dataset_validation.md` with results and evidence, including examples of valid/missing observations. Do not claim integration success until actual records have been fetched and parsed.

## Phase 2 — Data ingestion and preprocessing
Preferred approach: Python preprocessing job (earthaccess, xarray, netCDF4/h5netcdf, numpy, pandas, pyarrow) feeding a small versioned JSON API or static JSON/Parquet export consumed by iOS. Do not ship NASA Earthdata credentials inside the app. Use an existing backend if the project already has one; otherwise start with a reproducible local exporter and an app-consumable JSON bundle.

Implement independent adapters:
- `MURSSTAdapter`: daily SST, convert Kelvin to Celsius if required, inspect quality/metadata.
- `VIIRSOceanColorAdapter`: chlorophyll-a, Kd490 and/or reflectance with documented QA filtering.
- `PACEOCIAdapter`: chlorophyll-a/reflectance with documented QA filtering.

For each adapter: discovery -> granule retrieval -> bounding-box subset -> ocean/QA masking -> nearest **valid** marine pixel or documented neighborhood statistic -> unit conversion -> normalized records -> cache. Respect Earthdata authentication, throttling, retries, and provenance.

Never fabricate values or fill gaps with unmarked interpolation. If using spatial neighborhood aggregation, report radius, valid-pixel count, and method. Keep source-specific series separate.

## Phase 3 — Normalized contract
Use a source-aware observation model, e.g.:

```json
{
  "plot_id": "tidung-reference",
  "variable": "sst",
  "value": 29.4,
  "unit": "degC",
  "observed_at": "2025-08-12T00:00:00Z",
  "aggregation": "daily_analysis",
  "dataset": "MUR_GHRSST_L4",
  "product_version": "verified-at-runtime",
  "pixel_lat": -5.8,
  "pixel_lon": 106.5,
  "distance_to_plot_m": null,
  "nominal_resolution_m": 1000,
  "quality": "valid",
  "quality_notes": [],
  "retrieved_at": "2026-10-19T00:00:00Z"
}
```

**All values above are illustrative schema examples, not actual Pulau Tidung observations.** Use `null` for unavailable values, with a structured reason (`no_swath`, `cloud`, `land_mask`, `qa_rejected`, `network_error`, etc.). Include source granule identifier and processing details in actual records.

## Phase 4 — iOS integration
- Build a typed `OceanObservationService`/repository using async/await and `URLSession` for JSON API or bundled cache; integrate into existing ViewModel without breaking existing public APIs unnecessarily.
- Add an explicit loading/empty/error state and a visible `last updated` timestamp.
- Keep separate series for MUR SST, VIIRS chlorophyll-a, VIIRS Kd490, and PACE comparison observations.
- Preserve current SwiftUI UI; show only useful indicators and concise labels. Use Swift Charts for historical series and MapKit for plot location/coverage if already in use.
- Show dataset, timestamp, nominal resolution, actual sample distance, and quality details on demand, not as a wall of text.
- Demo/mock mode must be explicitly marked and never silently substituted for production NASA observations.

## Phase 5 — Validation and acceptance
- Verify at least one real granule for each implemented source or document an evidence-based coverage limitation.
- Include automated tests for unit conversion, longitude/latitude ordering, time alignment, QA rejection, missing values, and source provenance.
- Confirm no land pixel is displayed as an ocean measurement.
- Test 2025 backfill and recent updates; handle differing source latency and missing swaths.
- Confirm iOS app compiles and the existing history/map flows remain functional.
- Produce `docs/data_sources.md`, `docs/dataset_validation.md`, `docs/runbook.md`, and a concise implementation report with actual tested dataset IDs, commands, sample record counts, and limitations.

## Execution order
1. Inspect project.
2. Verify data availability and quality **before** wiring UI.
3. Implement MUR SST end to end.
4. Implement VIIRS ocean-color series.
5. Add PACE OCI as separate optional comparison.
6. Validate real records, test app, and document gaps.

## Definition of done
The existing iOS app displays **real, traceable ocean-specific NASA observations** near configured Pulau Tidung plots, with source-specific resolution/QA metadata and honest missing-data behavior. No terrestrial datasets, invented observations, or unsupported ice-ice predictions.
