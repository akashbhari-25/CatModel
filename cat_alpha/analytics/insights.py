from __future__ import annotations

import pandas as pd


def live_feed_insights(feed: pd.DataFrame) -> list[str]:
    if feed.empty:
        return ["No live events are available from the current feed. Use fallback portfolio risk metrics."]
    counts = feed["peril"].fillna("Unknown").value_counts()
    top_peril = counts.index[0]
    return [
        f"Current feed is most active in {top_peril}, with {int(counts.iloc[0])} observed event(s).",
        "Review overlap between active event regions and the highest exposure zones before discussing new deals.",
        "Escalate events with high magnitude, wind speed, or fire intensity into the stress testing tab.",
    ]


def exposure_insights(portfolio: pd.DataFrame, summary: dict[str, float]) -> list[str]:
    top = portfolio.sort_values("exposure_m", ascending=False).iloc[0]
    peril_mix = portfolio.groupby("peril")["exposure_m"].sum().sort_values(ascending=False)
    return [
        f"Largest single-region exposure is {top['region']} at ${top['exposure_m']:,.0f}M.",
        f"Dominant peril is {peril_mix.index[0]}, representing ${peril_mix.iloc[0]:,.0f}M of exposure.",
        f"Exposure HHI is {summary['exposure_hhi']:.3f}; monitor this as a concentration risk indicator.",
    ]


def monte_carlo_insights(simulation: dict[str, object], confidence: float) -> list[str]:
    gross = simulation["gross_risk"]
    ratio = gross["var_m"] / gross["expected_loss_m"] if gross["expected_loss_m"] else 0.0
    return [
        f"At {confidence:.1%} confidence, gross VaR is {ratio:.1f}x expected loss.",
        "The right tail is the business driver: use CVaR and PML rather than average loss alone.",
        "Regions with high 99th percentile loss should receive tighter underwriting review.",
    ]


def reinsurance_insights(simulation: dict[str, object]) -> list[str]:
    layer = simulation["layer"]
    return [
        f"The selected layer attaches in {layer['probability_layer_attaches']:.1%} of simulated years.",
        f"Ceded share is {layer['ceded_share']:.1%}; compare this against premium and target margin.",
        "If attachment probability is too high, the layer may behave more like working cover than remote protection.",
    ]


def tail_risk_insights(simulation: dict[str, object]) -> list[str]:
    gross = simulation["gross_risk"]
    retained = simulation["retained_risk"]
    reduction = 1 - retained["cvar_m"] / gross["cvar_m"] if gross["cvar_m"] else 0.0
    return [
        f"Reinsurance reduces modeled CVaR by {reduction:.1%} under the selected layer.",
        "CVaR is the stronger underwriting metric because it describes severity after the VaR threshold is breached.",
        "Use PML as a capital-at-risk proxy when summarizing portfolio stress to underwriters.",
    ]


def stress_insights(stress: dict[str, object]) -> list[str]:
    ceded_share = stress["ceded_loss_m"] / stress["gross_loss_m"] if stress["gross_loss_m"] else 0.0
    return [
        f"Scenario ceded share is {ceded_share:.1%} of gross event loss.",
        "Compare retained loss against appetite before accepting similar regional exposure.",
        "Use this scenario as an underwriter-facing event memo if live events resemble the selected shock.",
    ]


def portfolio_intelligence_insights(summary: dict[str, float]) -> list[str]:
    return [
        f"Largest region share is {summary['largest_region_share']:.1%}; diversification improves as this falls.",
        "Clusters identify regions with similar exposure-frequency-severity profiles for underwriting review.",
        "Prioritize marginal VaR contribution next: every new deal should show before/after portfolio tail risk.",
    ]

