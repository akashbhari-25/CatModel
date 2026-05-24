from __future__ import annotations

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def cluster_regions(portfolio: pd.DataFrame, clusters: int = 3) -> pd.DataFrame:
    if portfolio.empty:
        return pd.DataFrame(columns=["region", "peril", "exposure_m", "risk_cluster"])

    clusters = min(clusters, len(portfolio))
    if clusters <= 1:
        result = portfolio[["region", "peril", "exposure_m"]].copy()
        result["risk_cluster"] = 0
        return result

    features = portfolio[["exposure_m", "lambda_annual", "mean_severity_m", "severity_std_m"]]
    scaled = StandardScaler().fit_transform(features)
    labels = KMeans(n_clusters=clusters, random_state=42, n_init=10).fit_predict(scaled)
    result = portfolio[["region", "peril", "exposure_m"]].copy()
    result["risk_cluster"] = labels
    return result.sort_values(["risk_cluster", "exposure_m"], ascending=[True, False])
