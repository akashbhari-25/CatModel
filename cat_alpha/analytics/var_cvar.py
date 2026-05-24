from __future__ import annotations

import numpy as np


def value_at_risk(losses: np.ndarray, confidence: float) -> float:
    return float(np.quantile(losses, confidence))


def conditional_value_at_risk(losses: np.ndarray, confidence: float) -> float:
    var = value_at_risk(losses, confidence)
    tail = losses[losses >= var]
    return float(tail.mean()) if tail.size else var


def risk_summary(losses: np.ndarray, confidence: float) -> dict[str, float]:
    var = value_at_risk(losses, confidence)
    cvar = conditional_value_at_risk(losses, confidence)
    return {
        "expected_loss_m": float(np.mean(losses)),
        "std_loss_m": float(np.std(losses)),
        "var_m": var,
        "cvar_m": cvar,
        "pml_m": float(np.quantile(losses, 0.995)),
        "max_loss_m": float(np.max(losses)),
    }

