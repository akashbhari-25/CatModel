from __future__ import annotations

import pandas as pd
import plotly.express as px


COLORWAY = ["#00B3B3", "#D6B45F", "#E26D5C", "#74A4BC", "#9D8DF1", "#7FB069", "#F2A65A"]


def apply_workstation_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        colorway=COLORWAY,
        font={"color": "#DDE6ED", "family": "Inter, Segoe UI, sans-serif", "size": 12},
        title={"font": {"size": 15, "color": "#F5F7FA"}},
        margin={"l": 12, "r": 12, "t": 48, "b": 12},
        legend={"orientation": "h", "y": -0.18},
    )
    fig.update_xaxes(gridcolor="rgba(221,230,237,0.10)", zerolinecolor="rgba(221,230,237,0.18)")
    fig.update_yaxes(gridcolor="rgba(221,230,237,0.10)", zerolinecolor="rgba(221,230,237,0.18)")
    return fig


def loss_distribution(losses, title: str):
    frame = pd.DataFrame({"loss_m": losses})
    fig = px.histogram(frame, x="loss_m", nbins=70, title=title)
    fig.update_traces(marker_line_width=0, opacity=0.86)
    fig.update_xaxes(title="Loss ($M)")
    fig.update_yaxes(title="Simulation count")
    return apply_workstation_theme(fig)


def exposure_bar(portfolio: pd.DataFrame):
    fig = px.bar(
        portfolio.sort_values("exposure_m", ascending=True),
        x="exposure_m",
        y="region",
        color="peril",
        orientation="h",
        title="Exposure by Region",
    )
    fig.update_xaxes(title="Exposure ($M)")
    fig.update_yaxes(title="")
    return apply_workstation_theme(fig)


def live_event_map(feed: pd.DataFrame):
    frame = feed.dropna(subset=["latitude", "longitude"]).copy()
    frame["marker_size"] = 8.0
    if "magnitude" in frame:
        frame.loc[frame["magnitude"].notna(), "marker_size"] = (
            frame.loc[frame["magnitude"].notna(), "magnitude"].astype(float).clip(lower=1.0) * 2.0
        )
    if "wind_speed_mph" in frame:
        frame.loc[frame["wind_speed_mph"].notna(), "marker_size"] = (
            frame.loc[frame["wind_speed_mph"].notna(), "wind_speed_mph"].astype(float).clip(lower=20.0) / 8.0
        )
    if "frp" in frame:
        frame.loc[frame["frp"].notna(), "marker_size"] = (
            frame.loc[frame["frp"].notna(), "frp"].astype(float).clip(lower=10.0) / 8.0
        )
    fig = px.scatter_geo(
        frame,
        lat="latitude",
        lon="longitude",
        color="peril",
        size="marker_size",
        hover_name="place",
        title="Live Catastrophe Feed",
    )
    fig.update_geos(
        bgcolor="rgba(0,0,0,0)",
        landcolor="#172235",
        lakecolor="#0B1220",
        oceancolor="#0B1220",
        coastlinecolor="rgba(221,230,237,0.25)",
        showocean=True,
        showland=True,
    )
    return apply_workstation_theme(fig)


def peril_mix_bar(portfolio: pd.DataFrame):
    mix = portfolio.groupby("peril", as_index=False)["exposure_m"].sum().sort_values("exposure_m")
    fig = px.bar(mix, x="exposure_m", y="peril", orientation="h", title="Exposure by Peril")
    fig.update_xaxes(title="Exposure ($M)")
    fig.update_yaxes(title="")
    return apply_workstation_theme(fig)


def regional_tail_bar(region_expected: pd.DataFrame):
    frame = region_expected.sort_values("tail_99_loss_m", ascending=True)
    fig = px.bar(
        frame,
        x="tail_99_loss_m",
        y="region",
        color="peril",
        orientation="h",
        title="Regional 99th Percentile Loss",
    )
    fig.update_xaxes(title="Tail loss ($M)")
    fig.update_yaxes(title="")
    return apply_workstation_theme(fig)
