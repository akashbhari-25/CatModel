from __future__ import annotations

import pandas as pd


def sample_wildfires() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("2026-05-22", "California", 36.7, -119.4, 72.0, "Wildfire"),
            ("2026-05-22", "Australia", -33.9, 151.2, 64.0, "Wildfire"),
            ("2026-05-23", "Indonesia", -2.5, 118.0, 58.0, "Wildfire"),
        ],
        columns=["time", "place", "latitude", "longitude", "frp", "peril"],
    )


def fetch_wildfire_hotspots() -> pd.DataFrame:
    """Placeholder for NASA FIRMS.

    NASA FIRMS usually requires an API key. The project keeps this function
    isolated so a key can be added later without changing the app.
    """
    return sample_wildfires()

