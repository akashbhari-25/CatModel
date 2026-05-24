from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import requests


USGS_ENDPOINT = "https://earthquake.usgs.gov/fdsnws/event/1/query"


def sample_earthquakes() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("2026-05-20T04:12:00Z", "Japan", 6.4, 28.0, 38.3, 142.4, "Earthquake"),
            ("2026-05-21T11:40:00Z", "Chile", 5.9, 45.0, -32.8, -71.6, "Earthquake"),
            ("2026-05-22T17:05:00Z", "California", 4.8, 12.0, 34.1, -118.2, "Earthquake"),
        ],
        columns=["time", "place", "magnitude", "depth_km", "latitude", "longitude", "peril"],
    )


def fetch_recent_earthquakes(days: int = 7, min_magnitude: float = 4.5) -> pd.DataFrame:
    params = {
        "format": "geojson",
        "starttime": (date.today() - timedelta(days=days)).isoformat(),
        "minmagnitude": min_magnitude,
        "orderby": "time",
        "limit": 250,
    }
    try:
        response = requests.get(USGS_ENDPOINT, params=params, timeout=8)
        response.raise_for_status()
        features = response.json().get("features", [])
        rows = []
        for feature in features:
            props = feature.get("properties", {})
            coords = feature.get("geometry", {}).get("coordinates", [None, None, None])
            rows.append(
                {
                    "time": pd.to_datetime(props.get("time"), unit="ms", utc=True),
                    "place": props.get("place"),
                    "magnitude": props.get("mag"),
                    "depth_km": coords[2],
                    "latitude": coords[1],
                    "longitude": coords[0],
                    "peril": "Earthquake",
                }
            )
        return pd.DataFrame(rows) if rows else sample_earthquakes()
    except Exception:
        return sample_earthquakes()

