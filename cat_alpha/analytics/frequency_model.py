from __future__ import annotations

import numpy as np
import pandas as pd
import math


def simulate_event_counts(
    portfolio: pd.DataFrame,
    simulations: int,
    rng: np.random.Generator,
) -> np.ndarray:
    lambdas = portfolio["lambda_annual"].to_numpy(dtype=float)
    return rng.poisson(lam=lambdas, size=(simulations, len(lambdas)))


def poisson_probability(lam: float, k: int) -> float:
    return float(np.exp(-lam) * (lam**k) / math.factorial(k))
