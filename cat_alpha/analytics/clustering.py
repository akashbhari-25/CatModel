from __future__ import annotations

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def cluster_regions(portfolio: pd.DataFrame, clusters: int = 3) -> pd.DataFrame:
    features = portfolio[["exposure_m", "lambda_annual", "mean_severity_m", "severity_std_m"]]
    scaled = StandardScaler().fit_transform(features)
    labels = KMeans(n_clusters=clusters, random_state=42, n_init=10).fit_predict(scaled)
    result = portfolio[["region", "peril", "exposure_m"]].copy()
    result["risk_cluster"] = labels
    return result.sort_values(["risk_cluster", "exposure_m"], ascending=[True, False])

