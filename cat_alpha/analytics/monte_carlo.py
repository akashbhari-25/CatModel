from __future__ import annotations

import numpy as np
import pandas as pd

from cat_alpha.analytics.frequency_model import simulate_event_counts
from cat_alpha.analytics.reinsurance import apply_xol_layer, layer_summary
from cat_alpha.analytics.severity_model import (
    apply_tail_amplification,
    simulate_lognormal_event_losses,
)
from cat_alpha.analytics.var_cvar import risk_summary


def run_portfolio_simulation(
    portfolio: pd.DataFrame,
    simulations: int = 10_000,
    confidence: float = 0.99,
    attachment_m: float = 100.0,
    exhaustion_m: float = 500.0,
    tail_probability: float = 0.025,
    pareto_alpha: float = 2.2,
    seed: int = 42,
) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    counts = simulate_event_counts(portfolio, simulations, rng)
    regional_losses = simulate_lognormal_event_losses(portfolio, counts, rng)
    regional_losses = apply_tail_amplification(
        regional_losses,
        tail_probability=tail_probability,
        pareto_alpha=pareto_alpha,
        rng=rng,
    )
    exposure_caps = portfolio["exposure_m"].to_numpy(dtype=float)
    regional_losses = np.minimum(regional_losses, exposure_caps)
    gross = regional_losses.sum(axis=1)
    layer = apply_xol_layer(gross, attachment_m, exhaustion_m)
    region_expected = pd.DataFrame(
        {
            "region": portfolio["region"],
            "peril": portfolio["peril"],
            "expected_loss_m": regional_losses.mean(axis=0),
            "tail_99_loss_m": np.quantile(regional_losses, 0.99, axis=0),
        }
    ).sort_values("expected_loss_m", ascending=False)
    return {
        "event_counts": counts,
        "regional_losses": regional_losses,
        "gross_losses": gross,
        "ceded_losses": layer["ceded"],
        "retained_losses": layer["retained"],
        "gross_risk": risk_summary(gross, confidence),
        "retained_risk": risk_summary(layer["retained"], confidence),
        "layer": layer_summary(gross, layer["ceded"], layer["retained"]),
        "region_expected": region_expected,
    }

