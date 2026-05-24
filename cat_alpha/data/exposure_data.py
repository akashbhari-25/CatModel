from __future__ import annotations

import pandas as pd


def default_exposure_portfolio() -> pd.DataFrame:
    """Institutional-looking seed portfolio in USD millions."""
    rows = [
        ("Florida", "Hurricane", "United States", 500, 1200, 2.4, 250, 120),
        ("Texas", "Severe Storm", "United States", 325, 850, 2.0, 175, 80),
        ("Louisiana", "Storm Surge", "United States", 275, 650, 1.5, 210, 95),
        ("Caribbean", "Hurricane", "Caribbean", 300, 700, 1.8, 230, 110),
        ("Philippines", "Typhoon", "Philippines", 240, 620, 2.2, 160, 75),
        ("California Quake", "Earthquake", "United States", 450, 900, 0.8, 320, 160),
        ("California Wildfire", "Wildfire", "United States", 280, 750, 1.3, 190, 90),
        ("Japan", "Earthquake", "Japan", 375, 820, 1.1, 300, 145),
        ("Chile", "Earthquake", "Chile", 220, 460, 0.9, 210, 100),
        ("Turkey", "Earthquake", "Turkey", 210, 500, 0.7, 190, 85),
        ("Indonesia", "Earthquake + Tsunami", "Indonesia", 260, 580, 1.0, 240, 120),
        ("Australia", "Wildfire", "Australia", 250, 540, 1.0, 155, 70),
        ("Germany", "Flood", "Germany", 240, 510, 0.6, 170, 80),
        ("Bangladesh", "Flood", "Bangladesh", 190, 700, 1.4, 125, 60),
        ("Mumbai", "Flood", "India", 225, 780, 1.2, 145, 65),
    ]
    cols = [
        "region",
        "peril",
        "country",
        "exposure_m",
        "policy_count",
        "lambda_annual",
        "mean_severity_m",
        "severity_std_m",
    ]
    return pd.DataFrame(rows, columns=cols)


def exposure_summary(portfolio: pd.DataFrame) -> dict[str, float]:
    total = float(portfolio["exposure_m"].sum())
    top_share = float(portfolio["exposure_m"].max() / total) if total else 0.0
    herfindahl = float(((portfolio["exposure_m"] / total) ** 2).sum()) if total else 0.0
    return {
        "total_exposure_m": total,
        "largest_region_share": top_share,
        "exposure_hhi": herfindahl,
        "policy_count": float(portfolio["policy_count"].sum()),
    }

