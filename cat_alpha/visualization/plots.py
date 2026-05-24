from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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
    if frame.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No geocoded catastrophe events available",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font={"color": "#DDE6ED", "size": 14},
        )
        fig.update_geos(
            projection_type="equirectangular",
            showland=True,
            showocean=True,
            landcolor="#172235",
            oceancolor="#0B1220",
            coastlinecolor="rgba(221,230,237,0.25)",
            lataxis_range=[-60, 80],
            lonaxis_range=[-180, 180],
        )
        fig.update_layout(title="Live Catastrophe Feed", height=520)
        return apply_workstation_theme(fig)

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
        hover_data={
            "latitude": ":.2f",
            "longitude": ":.2f",
            "marker_size": False,
        },
        title="Live Catastrophe Feed",
        projection="equirectangular",
    )
    fig.update_traces(marker={"line": {"width": 0.8, "color": "#07101D"}, "opacity": 0.88})
    fig.update_geos(
        bgcolor="rgba(0,0,0,0)",
        landcolor="#172235",
        lakecolor="#0B1220",
        oceancolor="#0B1220",
        coastlinecolor="rgba(221,230,237,0.35)",
        countrycolor="rgba(221,230,237,0.14)",
        subunitcolor="rgba(221,230,237,0.10)",
        coastlinewidth=0.7,
        showcountries=True,
        showocean=True,
        showland=True,
        showlakes=True,
        lataxis_range=[-60, 80],
        lonaxis_range=[-180, 180],
        resolution=110,
    )
    fig.update_layout(height=520, geo={"domain": {"x": [0, 1], "y": [0, 1]}})
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
