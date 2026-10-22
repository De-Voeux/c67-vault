# Tidung Environmental Monitor — iOS POC Agent Instructions

## Mission
Build a working, minimal iOS app that visualizes **NASA-derived environmental observations around Pulau Tidung, Kepulauan Seribu**. This is an environmental monitoring proof of concept, **not** an ice-ice diagnosis or disease prediction app.

**Primary framework:** MapKit. **Supporting framework:** Swift Charts. Use SwiftUI for the app shell and URLSession for HTTP. Do not add Core ML, Vision, IoT, authentication, push notifications, or a backend unless essential.

## Target and acceptance criteria
- Native SwiftUI iOS app, iOS 17+, Xcode project, portrait-first, clean restrained marine palette.
- Map centered near **-5.80, 106.50** (latitude, longitude), labeled as an approximate reference point, not a farm coordinate.
- Date range selection, metric picker, latest available observation, 30/90-day trend chart, observation date, source, units, spatial resolution, and quality/availability notes.
- Fetch at least **NASA POWER daily solar radiation** from a real API; do not present mock values as real. Include sample fixtures for offline/demo use, clearly labeled **DEMO DATA**.
- Architect SST and precipitation adapters with genuine source metadata and graceful `notConfigured`/`unavailable` states. Implement them only when actual tested access and parsing are available; never fabricate values.
- Provide an actionable README with setup, API endpoints, data limitations, and manual test steps.

## Scientific scope and limitations
- No disease probabilities, ice-ice alerts, causal claims, or thresholds without validated evidence.
- Satellite grid cells are not point measurements at seaweed ropes. Show pixel center/distance if available and distinguish nominal grid spacing from effective resolution.
- Coastal contamination, clouds, missing pixels, and model/reanalysis uncertainty must be surfaced.
- A regional SMAP sea surface salinity grid (~40–70 km effective scale) is **not** suitable as a local farm measurement; defer SMAP to a clearly marked optional regional-context layer.
- Radiation at the sea surface is not underwater irradiance. Rainfall is not a measured local salinity change.
- Preserve original observation dates, source product versions, units, and data quality. Do not turn missing values into zero.

## Data source catalog
| Variable | NASA source | Nominal spatial resolution | Time scale | Access | POC priority |
|---|---|---|---|---|---|
| Solar radiation | NASA POWER `ALLSKY_SFC_SW_DWN` | coarse gridded estimate, approximately 0.5° for relevant meteorological grids; verify selected product | daily | Public REST JSON | P0 live |
| Sea surface temperature | GHRSST MUR L4 via PO.DAAC | 0.01° (~1 km grid) | daily | NASA Earthdata/PO.DAAC, CMR/OPeNDAP | P1 |
| Precipitation | GPM IMERG V07 (Early/Late for recent; Final for historical) | 0.1° (~11 km at equator) | half-hourly or daily product | GES DISC/Earthdata | P1 |
| Chlorophyll-a / ocean color | PACE OCI L3 or VIIRS | product-dependent (~2.4 km PACE L3 for some products) | daily/8-day | OB.DAAC/Earthdata | P2 |
| Salinity | SMAP SSS | effective tens of km (~40–70 km), unsuitable for farm scale | multi-day | PO.DAAC/Earthdata | optional regional context |

Official entry points:
- POWER daily API: https://power.larc.nasa.gov/docs/services/api/temporal/daily/
- PO.DAAC: https://podaac.jpl.nasa.gov/
- GPM IMERG: https://gpm.nasa.gov/data/imerg
- GES DISC: https://disc.gsfc.nasa.gov/
- Ocean Color: https://oceandata.sci.gsfc.nasa.gov/
- Earthdata Search: https://search.earthdata.nasa.gov/

**Important engineering constraint:** Earthdata-authenticated granules and multidimensional NetCDF/HDF are not necessarily straightforward to parse on iOS. Do not embed Earthdata credentials or access tokens in the app. For P1, prefer a reproducible offline preprocessing script that fetches data with Earthdata login outside the app and exports small versioned JSON files to bundle or a static HTTPS endpoint. The app itself must remain native iOS. Direct live NASA API integration is required for POWER only in the first iteration.

## NASA POWER request (working starting point)
```http
GET https://power.larc.nasa.gov/api/temporal/daily/point?parameters=ALLSKY_SFC_SW_DWN&community=RE&longitude=106.50&latitude=-5.80&start=20260101&end=20260131&format=JSON
```
Parse `properties.parameter.ALLSKY_SFC_SW_DWN`, whose keys are `yyyyMMdd`. Verify `parameters` units from API response metadata; commonly kWh/m²/day. POWER may return documented fill/sentinel values: convert those to `nil`. Display source time convention and avoid calling this an on-site sensor.

## App screens and interaction
1. **Overview:** MapKit map around Pulau Tidung, single approximate reference pin, legend explaining that the region shown is not the spatial footprint of a measurement. Metric selector: Solar radiation / SST / Rainfall / Chlorophyll-a (disabled or unavailable until data exists). Current value card uses **latest available observation**, not “live now.” Display `Data updated` and observation date separately.
2. **History:** Swift Charts time-series with 30d / 90d / custom date range. Tap or scrub to inspect date, value, unit, and source. Gaps stay gaps. Optionally show 7-day rolling average, but only with sufficient valid samples.
3. **About data:** Data source, NASA product/version, native resolution, actual extraction strategy, latency, missingness, limitations, and demo/live provenance. Add explicit statement: “Environmental context only; not a prediction of ice-ice disease.”

## UI direction
- Minimal scientific instrument aesthetic; muted navy, slate, teal, white; accessible contrast.
- No exaggerated warning colors or unvalidated risk gauges.
- Use a small number of purposeful cards and clear typography; include loading, error, empty, stale, and offline states.
- Support Dynamic Type and VoiceOver descriptions for the chart and metric cards.

## Architecture
Suggested layout:
```
TidungMonitor/
  App/TidungMonitorApp.swift
  Models/EnvironmentalObservation.swift
  Models/DatasetMetadata.swift
  Services/NASAPowerClient.swift
  Services/ObservationRepository.swift
  Services/FixtureRepository.swift
  Services/OtherDatasetAdapters.swift
  ViewModels/MonitorViewModel.swift
  Views/OverviewView.swift
  Views/HistoryView.swift
  Views/DataSourcesView.swift
  Views/Components/
  Resources/demo_observations.json
  Tests/
README.md
```

Data model (Codable, dates ISO 8601 in normalized export):
```json
{
  "location_id": "tidung_reference",
  "latitude": -5.80,
  "longitude": 106.50,
  "metric": "solar_radiation",
  "date": "2026-01-15",
  "value": null,
  "unit": "kWh/m²/day",
  "source": "NASA POWER",
  "product": "ALLSKY_SFC_SW_DWN",
  "version": null,
  "nominal_resolution": "product-dependent; verify",
  "pixel_center": null,
  "quality_flags": [],
  "provenance": "live_api"
}
```
`null` above is a schema example, not a real measurement.

Repository contract:
- `fetchObservations(metric:dateRange:location:) async throws -> [EnvironmentalObservation]`
- `fetchDatasetMetadata(metric:) -> DatasetMetadata`
- `dataMode: live | demo` with persistent and prominent visual label in demo mode.
- Use `URLSession`, `async/await`, bounded timeout, HTTP error handling, decode validation, and small in-memory caching. No silent demo fallback on API failure.

## Feature engineering
- For daily series, calculate `delta_7d`, rolling 7-day mean, and valid sample counts.
- Historical anomaly requires a seasonally matched multiyear baseline; do **not** label a deviation from a 30-day mean as a climatological anomaly.
- Never calculate change across missing data as if measurements were continuous.
- Preprocessed exports should include the original timestamp/window, dataset ID, retrieval time, extraction coordinates, QC flags, and processing method.

## Execution plan
### Phase A — Must ship
1. Create and build Xcode SwiftUI iOS 17+ app.
2. Implement real NASA POWER fetch for chosen date range at the approximate Pulau Tidung point.
3. Parse valid daily values; exclude fill values, preserve units and source.
4. Implement MapKit reference map and Swift Charts trend view.
5. Add source/limitations screen and clear real/demo states.
6. Add tests for date parsing, missing values, network failures, chart gaps, and empty responses.

### Phase B — Real ocean variables
7. Build an external, reproducible Python preprocessing script for MUR SST and IMERG with NASA Earthdata login handled outside the app. Document exact short names and product versions verified during implementation.
8. Extract **valid ocean pixels** near the reference point, retain pixel centers and distances, and export normalized JSON.
9. Import JSON into iOS through bundled fixtures or a static HTTPS file endpoint; display provenance and freshness accurately.
10. Validate coastal coverage and compare missingness before enabling any new metric.

### Phase C — Optional
11. Add PACE/VIIRS ocean color only after valid coastal retrievals are demonstrated.
12. Add SMAP only as broad regional context with conspicuous resolution caveat.
13. Add multi-year baseline and seasonal anomaly once sufficient valid historical coverage exists.

## Acceptance tests
- NASA POWER request successfully returns and renders actual values when API is available.
- A failed request shows a real error with retry, never synthetic values presented as NASA observations.
- Demo fixtures have unmistakable labeling in every relevant screen.
- User can inspect exact date, metric unit, source, resolution, and freshness.
- Map never implies that a reference pin or a 1-km pixel is a direct farm-level observation.
- Chart preserves missing days and does not draw invented readings.
- App builds and launches in iOS Simulator, and README documents any unimplemented integrations.

## Deliverables
- Complete native Xcode project and source.
- README with run steps, supported metrics, tested NASA endpoints, known limitations, and screenshot checklist.
- Demo JSON fixture and unit tests.
- Optional preprocessing script plus dependency file for Phase B.

## Final instruction to coding agent
**Prioritize a truthful, functioning small app over an impressive but fabricated dashboard.** Finish Phase A before adding additional datasets. Never claim environmental measurements establish ice-ice presence, risk probability, or farm-scale water conditions.
