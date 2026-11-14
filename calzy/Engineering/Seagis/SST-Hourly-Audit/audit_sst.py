"""Read-only Copernicus -> local JSON/HTTP feasibility probe; no production writes."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

DATASET = "cmems_mod_glo_phy_anfc_0.083deg_PT1H-m"
VERSION = "202406"
PRODUCT = "GLOBAL_ANALYSISFORECAST_PHY_001_024"
CATALOG = f"https://stac.marine.copernicus.eu/metadata/{PRODUCT}/{DATASET}_{VERSION}/dataset.stac.json"
UTC = timezone.utc
PLOTS = [
    {"plot_id": "tidung-besar-reference", "latitude": -5.8211,
     "longitude": 106.5522, "coordinate_status": "user_provided_island_reference_not_farm"},
    {"plot_id": "00000000-0000-4000-8000-000000000001", "latitude": -5.79268,
     "longitude": 106.48012, "coordinate_status": "synthetic"},
    {"plot_id": "00000000-0000-4000-8000-000000000002", "latitude": -5.798,
     "longitude": 106.494, "coordinate_status": "example_not_surveyed"},
]


def iso(value):
    return value.astimezone(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def stamp(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False,
                                     separators=(",", ":")).encode()).hexdigest()


def save(path, value):
    """Atomic replacement: a failed fetch must leave the previous snapshot intact."""
    path = Path(path)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    os.replace(temporary, path)


def due(last_checked, now):
    """Elapsed hour, first launch, or clock rollback. Scheduling belongs to caller."""
    return last_checked is None or now < last_checked or (now - last_checked).total_seconds() >= 3600


def catalog():
    with urllib.request.urlopen(CATALOG, timeout=40) as response:
        return json.load(response)


def validate_catalog(data):
    props = data["properties"]
    dims = props["cube:dimensions"]
    assert data["id"] == f"{DATASET}_{VERSION}", "dataset changed"
    assert data["collection"] == PRODUCT, "product changed"
    assert dims["time"]["step"] == "PT1H", "not native hourly"
    for axis in ("latitude", "longitude"):
        assert abs(dims[axis]["step"] - 1 / 12) < 2e-5, "grid changed"
    assert props["cube:variables"]["thetao"]["unit"] == "degrees_C", "unit changed"
    assert props["cube:variables"]["thetao"]["standardName"] == "sea_water_potential_temperature"
    assert not props.get("admp_in_preparation"), "provider in preparation"
    return -max(dims["elevation"]["values"])


def distance_km(lat1, lon1, lat2, lon2):
    a, b = math.radians(lat1), math.radians(lat2)
    h = math.sin((b - a) / 2) ** 2 + math.cos(a) * math.cos(b) * math.sin(math.radians(lon2 - lon1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(min(1, h)))


def extract(ds, start, end):
    import numpy as np
    assert all(ds.sizes.get(k) == 1 for k in ("latitude", "longitude", "depth")), "not one cell"
    assert ds.thetao.attrs["units"] == "degrees_C", "unit changed"
    assert ds.thetao.attrs["standard_name"] == "sea_water_potential_temperature"
    assert ds.depth.attrs["units"] == "m"
    assert ds.latitude.attrs["units"] == "degrees_north"
    assert ds.longitude.attrs["units"] == "degrees_east"
    labels = [np.datetime_as_string(t, unit="s") + "Z" for t in ds.time.values]
    expected = [iso(start + timedelta(hours=n)) for n in range(int((end - start).total_seconds() / 3600) + 1)]
    assert labels == expected, "missing, duplicated, or nonhourly timestamps"
    values = ds.thetao.transpose("time", "depth", "latitude", "longitude").values.reshape(-1)
    rows = [{"valid_at": label, "value": float(v) if np.isfinite(v) and abs(v) < 1e30 else None,
             "value_status": "present" if np.isfinite(v) and abs(v) < 1e30 else "missing"}
            for label, v in zip(labels, values)]
    return {"latitude": float(ds.latitude.values[0]), "longitude": float(ds.longitude.values[0]),
            "depth_m": float(ds.depth.values[0]), "rows": rows}


def merge(previous, content, checked_at, provider_updated_at):
    revision = digest(content)
    unchanged = previous is not None and previous["content_revision"] == revision
    return {"schema_version": "sst-probe-1", "mode": "feasibility_probe",
            "training_authorized": False, "scope": "regional_model", "provider": "copernicus",
            "product": PRODUCT, "dataset": DATASET, "dataset_version": VERSION,
            "variable": "thetao", "unit": "degC", "native_unit": "degrees_C",
            "native_cadence_seconds": 3600, "temporal_statistic": "hourly_mean",
            "issued_at": None, "provider_updated_at": provider_updated_at,
            "last_checked_at": iso(checked_at), "content_revision": revision,
            "content_first_seen_at": previous["content_first_seen_at"] if unchanged else iso(checked_at),
            "content_changed": not unchanged, **content}


def payload(snapshot, plot_id, now):
    """Select the CURRENT hour, never the furthest future forecast as 'latest'."""
    plot = next((p for p in snapshot["plots"] if p["plot_id"] == plot_id), None)
    if plot is None:
        raise KeyError("plot_not_found")
    hour = iso(now.replace(minute=0, second=0, microsecond=0))
    current = next((r for r in plot["rows"] if r["valid_at"] == hour), None)
    # Pilot operational age only, NOT a biological threshold. Unknown age fails closed.
    updated = snapshot["provider_updated_at"]
    age = (now - stamp(updated)).total_seconds() if updated else None
    temporal_usable = current is not None and current["value"] is not None and age is not None and 0 <= age <= 48 * 3600
    return {**{k: v for k, v in snapshot.items() if k != "plots"}, "served_at": iso(now),
            "plot_id": plot_id, "coordinate_status": plot["coordinate_status"],
            "requested_location": plot["requested_location"], "cell": plot["cell"],
            "cell_distance_km": plot["cell_distance_km"], "spatial_support": "unverified",
            "farm_fallback_authorized": False, "provider_update_age_seconds": age,
            "temporal_status": "current_hour_available" if temporal_usable else "unavailable_or_stale",
            "current": current, "rows": plot["rows"]}


def fetch(output):
    import copernicusmarine as cm
    output.mkdir(parents=True, exist_ok=True)
    began = datetime.now(UTC)
    start = began.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    end = start + timedelta(hours=95)  # Yesterday + today + two future days, 96 native slots.
    before = catalog()
    depth = validate_catalog(before)
    plots = []
    timings = []
    for location in PLOTS:
        tick = time.monotonic()
        ds = cm.open_dataset(dataset_id=DATASET, dataset_version=VERSION, variables=["thetao"],
                             minimum_latitude=location["latitude"], maximum_latitude=location["latitude"],
                             minimum_longitude=location["longitude"], maximum_longitude=location["longitude"],
                             minimum_depth=depth, maximum_depth=depth,
                             start_datetime=iso(start), end_datetime=iso(end),
                             coordinates_selection_method="nearest", raise_if_updating=True)
        try:
            ds.load()
            result = extract(ds, start, end)
            assert abs(result["depth_m"] - depth) < 1e-6, "depth changed"
            cell = {k: v for k, v in result.items() if k != "rows"}
            plots.append({"plot_id": location["plot_id"], "coordinate_status": location["coordinate_status"],
                          "requested_location": {"latitude": location["latitude"], "longitude": location["longitude"]},
                          "cell": cell, "cell_distance_km": distance_km(location["latitude"], location["longitude"], cell["latitude"], cell["longitude"]),
                          "rows": result["rows"]})
        finally:
            ds.close()
        timings.append(round(time.monotonic() - tick, 3))
    after = catalog()
    validate_catalog(after)
    assert before["properties"].get("admp_updated_data") == after["properties"].get("admp_updated_data"), "provider changed during fetch"
    content = {"window_start": iso(start), "window_end": iso(end), "plots": plots}
    previous_path = output / "snapshot.json"
    previous = json.loads(previous_path.read_text()) if previous_path.exists() else None
    snapshot = merge(previous, content, datetime.now(UTC), before["properties"].get("admp_updated_data"))
    report = {"started_at": iso(began), "finished_at": snapshot["last_checked_at"],
              "toolbox_version": cm.__version__, "subset_seconds_per_plot": timings,
              "expected_slots_per_plot": 96, "content_changed": snapshot["content_changed"],
              "content_revision": snapshot["content_revision"], "catalog_stable_during_fetch": True,
              "plots": [{"plot_id": p["plot_id"], "cell": p["cell"],
                         "distance_km": p["cell_distance_km"], "slots": len(p["rows"]),
                         "valid": sum(r["value"] is not None for r in p["rows"]),
                         "min_degC": min((r["value"] for r in p["rows"] if r["value"] is not None), default=None),
                         "max_degC": max((r["value"] for r in p["rows"] if r["value"] is not None), default=None)} for p in plots]}
    save(output / "catalog-before.json", before)
    save(output / "catalog-after.json", after)
    save(output / ("repeat-check.json" if previous else "audit.json"), report)
    save(previous_path, snapshot)
    with (output / "hourly.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["plot_id", "valid_at", "value", "value_status", "unit"])
        writer.writeheader()
        for p in plots:
            writer.writerows({"plot_id": p["plot_id"], **row, "unit": "degC"} for row in p["rows"])
    print(json.dumps(report, indent=2))


def serve(output, port):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parts = self.path.split("/")
            if len(parts) != 5 or parts[1:3] != ["v1", "plots"] or parts[4] != "sst":
                self.send_error(404)
                return
            try:
                snapshot = json.loads((output / "snapshot.json").read_text())
                body = json.dumps(payload(snapshot, parts[3], datetime.now(UTC)), allow_nan=False).encode()
            except KeyError:
                self.send_error(404)
                return
            except (OSError, ValueError):
                self.send_error(503)
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    print(f"Local feasibility endpoint: http://127.0.0.1:{port}/v1/plots/<plot-id>/sst", flush=True)
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["fetch", "serve"])
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "evidence")
    parser.add_argument("--port", type=int, default=8876)
    args = parser.parse_args()
    if args.command == "fetch":
        fetch(args.output)
    else:
        serve(args.output, args.port)
