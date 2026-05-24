from __future__ import annotations

import pandas as pd

from cat_alpha.analytics.reinsurance import apply_xol_layer


SCENARIOS = {
    "Category 5 Hurricane - Florida": {
        "region_match": "Florida",
        "gross_loss_ratio": 0.72,
        "narrative": "Major Miami landfall with storm surge and high insured coastal exposure.",
    },
    "Tokyo Region Earthquake": {
        "region_match": "Japan",
        "gross_loss_ratio": 0.68,
        "narrative": "Severe quake affecting dense commercial and residential exposures.",
    },
    "California Wildfire Season": {
        "region_match": "California Wildfire",
        "gross_loss_ratio": 0.62,
        "narrative": "Multi-county wildfire sequence with correlated claims accumulation.",
    },
    "Mumbai Urban Flood": {
        "region_match": "Mumbai",
        "gross_loss_ratio": 0.55,
        "narrative": "Extreme rainfall and infrastructure disruption in concentrated urban exposure.",
    },
    "Pacific Quake + Tsunami": {
        "region_match": "Indonesia",
        "gross_loss_ratio": 0.75,
        "narrative": "Compound earthquake and tsunami event with severe coastal loss.",
    },
}


def run_stress_scenario(
    portfolio: pd.DataFrame,
    scenario_name: str,
    attachment_m: float,
    exhaustion_m: float,
) -> dict[str, object]:
    scenario = SCENARIOS[scenario_name]
    region = portfolio[portfolio["region"].eq(scenario["region_match"])]
    if region.empty:
        gross = 0.0
    else:
        gross = float(region["exposure_m"].iloc[0] * scenario["gross_loss_ratio"])
    layer = apply_xol_layer(
        gross_losses=pd.Series([gross]).to_numpy(),
        attachment_m=attachment_m,
        exhaustion_m=exhaustion_m,
    )
    return {
        "scenario": scenario_name,
        "narrative": scenario["narrative"],
        "gross_loss_m": gross,
        "ceded_loss_m": float(layer["ceded"][0]),
        "retained_loss_m": float(layer["retained"][0]),
    }

