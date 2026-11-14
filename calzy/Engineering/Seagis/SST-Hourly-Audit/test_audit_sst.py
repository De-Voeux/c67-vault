"""Failure/refresh checks for the probe; synthetic fixtures, never field evidence."""
import copy
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from audit_sst import UTC, due, extract, iso, merge, payload, save


class RefreshChecks(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 11, 10, 6, 15, tzinfo=UTC)
        self.content = {"plots": [{"plot_id": "p1", "coordinate_status": "synthetic",
                                 "requested_location": {}, "cell": {}, "cell_distance_km": 2,
                                 "rows": [{"valid_at": "2026-11-10T06:00:00Z", "value": 29.0, "value_status": "present"},
                                          {"valid_at": "2026-11-10T07:00:00Z", "value": 29.1, "value_status": "present"}]}]}
        self.snapshot = merge(None, self.content, self.now, "2026-11-10T03:00:00Z")

    def test_hourly_due_first_launch_boundary_and_clock_rollback(self):
        self.assertTrue(due(None, self.now))
        self.assertFalse(due(self.now, self.now + timedelta(seconds=3599)))
        self.assertTrue(due(self.now, self.now + timedelta(hours=1)))
        self.assertTrue(due(self.now, self.now - timedelta(seconds=1)))

    def test_repeat_does_not_rejuvenate_content(self):
        second = merge(self.snapshot, self.content, self.now + timedelta(hours=1), self.snapshot["provider_updated_at"])
        self.assertFalse(second["content_changed"])
        self.assertEqual(second["content_first_seen_at"], self.snapshot["content_first_seen_at"])
        self.assertNotEqual(second["last_checked_at"], self.snapshot["last_checked_at"])

    def test_new_hour_selects_next_value_without_picking_furthest_forecast(self):
        a = payload(self.snapshot, "p1", self.now)
        b = payload(self.snapshot, "p1", self.now + timedelta(hours=1))
        self.assertEqual(a["current"]["value"], 29.0)
        self.assertEqual(b["current"]["value"], 29.1)
        self.assertFalse(b["farm_fallback_authorized"])

    def test_revision_replaces_same_hour_instead_of_adding_duplicate(self):
        revised = copy.deepcopy(self.content)
        revised["plots"][0]["rows"][0]["value"] = 29.5
        second = merge(self.snapshot, revised, self.now + timedelta(hours=1), "2026-11-10T07:00:00Z")
        self.assertTrue(second["content_changed"])
        self.assertNotEqual(second["content_revision"], self.snapshot["content_revision"])
        self.assertEqual(len(second["plots"][0]["rows"]), 2)

    def test_missing_is_not_zero(self):
        self.snapshot["plots"][0]["rows"][0].update(value=None, value_status="missing")
        result = payload(self.snapshot, "p1", self.now)
        self.assertIsNone(result["current"]["value"])
        self.assertEqual(result["temporal_status"], "unavailable_or_stale")

    def test_unknown_plot_is_rejected(self):
        with self.assertRaises(KeyError):
            payload(self.snapshot, "wrong", self.now)

    def test_old_unknown_future_provider_update_rejected_despite_recent_fetch(self):
        for updated in ("2026-11-07T03:00:00Z", None, "2026-11-11T03:00:00Z"):
            self.snapshot["provider_updated_at"] = updated
            result = payload(self.snapshot, "p1", self.now)
            self.assertEqual(result["temporal_status"], "unavailable_or_stale")

    def test_missing_current_hour_does_not_use_future_value(self):
        self.snapshot["plots"][0]["rows"].pop(0)
        self.assertIsNone(payload(self.snapshot, "p1", self.now)["current"])

    def test_failed_json_save_preserves_last_good_snapshot(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "snapshot.json"
            save(path, self.snapshot)
            before = path.read_bytes()
            with self.assertRaises(ValueError):
                save(path, {"invalid": float("nan")})
            self.assertEqual(before, path.read_bytes())

    def test_nonhourly_or_duplicate_time_is_rejected(self):
        import numpy as np
        import xarray as xr
        start = self.now.replace(minute=0)
        ds = xr.Dataset({"thetao": (("time", "depth", "latitude", "longitude"), np.ones((2, 1, 1, 1)))},
                        coords={"time": np.array(["2026-11-10T06:00:00", "2026-11-10T08:00:00"], dtype="datetime64[s]"),
                                "depth": [0.494], "latitude": [-5.75], "longitude": [106.5]})
        ds.thetao.attrs.update(units="degrees_C", standard_name="sea_water_potential_temperature")
        ds.depth.attrs["units"] = "m"
        ds.latitude.attrs["units"] = "degrees_north"
        ds.longitude.attrs["units"] = "degrees_east"
        with self.assertRaises(AssertionError):
            extract(ds, start, start + timedelta(hours=1))
        ds = ds.assign_coords(time=[np.datetime64("2026-11-10T06:00:00")] * 2)
        with self.assertRaises(AssertionError):
            extract(ds, start, start + timedelta(hours=1))


if __name__ == "__main__":
    unittest.main()
