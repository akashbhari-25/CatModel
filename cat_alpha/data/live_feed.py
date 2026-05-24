from __future__ import annotations

import pandas as pd

from cat_alpha.data.fetch_nasa_firms import fetch_wildfire_hotspots
from cat_alpha.data.fetch_noaa import fetch_storm_events
from cat_alpha.data.fetch_usgs import fetch_recent_earthquakes


def fetch_live_catastrophe_feed() -> pd.DataFrame:
    frames = [
        fetch_recent_earthquakes(),
        fetch_storm_events(),
        fetch_wildfire_hotspots(),
    ]
    feed = pd.concat(frames, ignore_index=True, sort=False)
    feed["time"] = feed["time"].astype(str)
    return feed

