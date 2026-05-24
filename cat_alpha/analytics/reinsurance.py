from __future__ import annotations

import numpy as np


def apply_xol_layer(
    gross_losses: np.ndarray,
    attachment_m: float,
    exhaustion_m: float,
) -> dict[str, np.ndarray]:
    limit = max(exhaustion_m - attachment_m, 0.0)
    ceded = np.minimum(np.maximum(gross_losses - attachment_m, 0.0), limit)
    retained = gross_losses - ceded
    return {
        "gross": gross_losses,
        "ceded": ceded,
        "retained": retained,
    }


def layer_summary(gross: np.ndarray, ceded: np.ndarray, retained: np.ndarray) -> dict[str, float]:
    return {
        "mean_gross_loss_m": float(np.mean(gross)),
        "mean_ceded_loss_m": float(np.mean(ceded)),
        "mean_retained_loss_m": float(np.mean(retained)),
        "ceded_share": float(np.mean(ceded) / np.mean(gross)) if np.mean(gross) else 0.0,
        "probability_layer_attaches": float(np.mean(ceded > 0)),
    }

