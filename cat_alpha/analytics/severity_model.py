from __future__ import annotations

import numpy as np
import pandas as pd


def lognormal_parameters(mean: np.ndarray, std: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    variance = std**2
    sigma2 = np.log1p(variance / (mean**2))
    mu = np.log(mean) - sigma2 / 2
    return mu, np.sqrt(sigma2)


def simulate_lognormal_event_losses(
    portfolio: pd.DataFrame,
    event_counts: np.ndarray,
    rng: np.random.Generator,
) -> np.ndarray:
    means = portfolio["mean_severity_m"].to_numpy(dtype=float)
    stds = portfolio["severity_std_m"].to_numpy(dtype=float)
    mu, sigma = lognormal_parameters(means, stds)
    losses = np.zeros_like(event_counts, dtype=float)
    for j in range(event_counts.shape[1]):
        counts = event_counts[:, j]
        max_count = int(counts.max()) if counts.size else 0
        if max_count == 0:
            continue
        draws = rng.lognormal(mean=mu[j], sigma=sigma[j], size=(event_counts.shape[0], max_count))
        mask = np.arange(max_count)[None, :] < counts[:, None]
        losses[:, j] = (draws * mask).sum(axis=1)
    return losses


def apply_tail_amplification(
    losses: np.ndarray,
    tail_probability: float,
    pareto_alpha: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Blend in Pareto shocks to reflect catastrophe tail thickness."""
    if tail_probability <= 0:
        return losses
    shocks = rng.random(losses.shape) < tail_probability
    pareto_multiplier = 1 + rng.pareto(a=pareto_alpha, size=losses.shape)
    return np.where(shocks, losses * pareto_multiplier, losses)

