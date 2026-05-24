from __future__ import annotations

import pandas as pd


def sample_storms() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("2026-05-18", "Florida offshore disturbance", 28.5, -79.3, 85, 985, "Hurricane"),
            ("2026-05-19", "Philippines typhoon cell", 14.6, 122.0, 95, 970, "Typhoon"),
            ("2026-05-21", "Gulf severe storm", 29.7, -94.8, 62, 998, "Severe Storm"),
        ],
        columns=["time", "place", "latitude", "longitude", "wind_speed_mph", "pressure_mb", "peril"],
    )


def fetch_storm_events() -> pd.DataFrame:
    """NOAA/NHC hook.

    Historical tropical cyclone data is best sourced from IBTrACS/HURDAT2 and
    scheduled NOAA pulls. This demo returns a stable storm feed until a NOAA
    tokenized or file-based pipeline is configured.
    """
    return sample_storms()

