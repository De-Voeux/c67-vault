---
type: research-context
project: "[[Challenge Final]]"
created: 2026-10-14
status: imported-context
source: "[[seaweed_research_vault_context]]"
tags: [challenge-final, rumput-laut, ice-ice, research-context]
---

# Data Pengamatan Bumi dan Eksplorasi Produk Rumput Laut

Kandidat data dan gagasan produk dari percakapan; spesifikasi dataset dan konsep belum menjadi kebutuhan final.

Asal: [[seaweed_research_vault_context]]; cakupan percakapan 3–14 Oktober 2026 menurut lampiran. Indeks: [[Konteks Riset Rumput Laut - 14 Oktober 2026]].

## Catatan terkait

- [[Penginderaan Jauh dan SIG Pesisir]]
- [[Remote Monitoring NASA dan Validasi Early Warning Rumput Laut]]
- [[Data Lingkungan ke Tindakan]]
- [[Challenge Response - Seaweed Ice-Ice]] — proposal tim yang dicatat terpisah.

Resolusi yang disebut dalam lampiran adalah perkiraan historis menurut produk, belum dicek ulang. Untuk pemakaian data, catat nama produk/versi, spacing grid, resolusi efektif, periode, latency dan mutu piksel pesisir. Gagasan situs, SwiftUI, probe, dan intelijen pasokan disimpan sebagai riwayat eksplorasi, bukan daftar pekerjaan yang harus dijalankan.

## Materi konteks yang dipertahankan

## 7. Earth Observation & Environmental Data

Potential sources identified during discussions include:

| Data or product | Source candidates | Practical caution |
| --- | --- | --- |
| SST | NASA/NOAA VIIRS, Sentinel-3, Copernicus Marine, Open-Meteo Marine | Surface temperature and sensor product differ; coastal contamination/cloud coverage and sparse temporal coverage matter. |
| Salinity | Copernicus Marine, remote-sensing/model products, **local salinity probe** | Many salinity products are coarse; cannot assume plot-level validity. |
| Irradiance/light | Meteorological radiation products, cloud cover, optical attenuation proxies | Above-water sunlight ≠ irradiance experienced by submerged seaweed. |
| Currents/waves | Copernicus Marine, Open-Meteo Marine, local/current observations | Nearshore flow may be dominated by bathymetry, tide, coastal geometry; km-scale model cells can be too coarse. |
| Rainfall/wind | NASA GPM, weather observations / BMKG | Precipitation and wind influence local conditions indirectly; local effects need validation. |
| Ocean color/chlorophyll/turbidity proxies | VIIRS, Sentinel-3 OLCI, Sentinel-2 where suitable | Optical proxies are not direct measurements of pathogens or ice-ice; shallow-bottom effects can mislead. |
| Bathymetry/tides | GEBCO, relevant tidal datasets | Coarse bathymetry/tide products may not resolve cultivation microhabitats. |

Previously mentioned indicative sensor/model resolutions included **Sentinel-3 OLCI ~300 m**, **VIIRS SST ~750 m**, and some **Copernicus Marine fields ~8–9 km**. These are **product-dependent approximations, not universal data specifications**; check each dataset's actual grid, effective resolution, coverage, update latency, and nearshore quality before using.

A key user question was the size of a map grid compared with **Pulau Tidung being only several kilometers wide**. For every map layer, distinguish **pixel/grid spacing**, **effective spatial resolution**, and **represented area**. A visually detailed map does not imply fine-scale measurements.

**Critical scale mismatch:** Cultivation happens in shallow nearshore plots (often within ~500 m of shore), whereas many oceanographic gridded products represent km-scale sea-surface conditions. Satellite data may capture **regional context or anomaly**, not every small water-condition change farmers describe.


## 9. Product / Prototype Ideas (Context Only; Not a Requirement)

Several concepts were considered over time:

- **Water Detective / water-condition warnings:** help detect or document unusual coastal conditions, potentially for extension workers.
- **Cultivation advisor:** compare possible planting locations/timing using environmental context.
- **Photo + location + environmental-data POC:** simple website where a photo and location accompany **demo weather/ocean data** to illustrate a provisional crop-health/ice-ice assessment. **Demo results are not scientifically validated predictions.**
- **Mac/iOS prototypes:** at different points, SwiftUI, MapKit, Charts, Vision/Core ML were explored as supporting technologies; these do not define the research question.
- **Low-cost IoT probe:** combined temperature + salinity in a small immersed device, possible wired USB-C/Lightning connection to iPhone or periodic data transfer; cost/availability were concerns. Hardware choices were exploratory.
- **Regional production/supply intelligence:** explored earlier, not the current scientific focus.

**Important preference:** When asked to explain a scientific article, **do not pivot to MVPs, Apple frameworks, architecture, UI features, or product suggestions** unless the user explicitly requests that translation.




## Navigasi kategori

[[Indeks - Riset Ice-Ice]] · [[Peta Catatan - Challenge Final]]


## Masukan mentoring IoT — diimpor 15 Oktober 2026

[[Diskusi - Mas Ricky (Mentoring IoT dan Pengukuran Kondisi Laut)]] dan [[Rencana Pengukuran IoT Kondisi Laut - Diskusi Mas Ricky]] mencatat alternatif sensor, daya dan komunikasi. Belum spesifikasi atau validasi lapangan.
