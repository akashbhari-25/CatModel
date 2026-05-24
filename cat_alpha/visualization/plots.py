from __future__ import annotations

from html import escape

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


COLORWAY = ["#00B3B3", "#D6B45F", "#E26D5C", "#74A4BC", "#9D8DF1", "#7FB069", "#F2A65A"]
PERIL_COLORS = {
    "Earthquake": "#74B9F2",
    "Hurricane": "#0F74C9",
    "Typhoon": "#F2A0A0",
    "Severe Storm": "#F03A3A",
    "Wildfire": "#75D68B",
    "Flood": "#60D3D9",
}


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
        fig.update_layout(title="Live Catastrophe Feed", height=520)
        fig.update_xaxes(range=[-180, 180], title="Longitude")
        fig.update_yaxes(range=[-60, 85], title="Latitude")
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
    fig = px.scatter(
        frame,
        x="longitude",
        y="latitude",
        color="peril",
        size="marker_size",
        hover_name="place",
        hover_data={
            "latitude": ":.2f",
            "longitude": ":.2f",
            "marker_size": False,
        },
        title="Live Catastrophe Feed - Global Coordinate Map",
    )
    fig.update_traces(marker={"line": {"width": 0.8, "color": "#07101D"}, "opacity": 0.88})
    fig.add_vrect(x0=-170, x1=-30, fillcolor="rgba(116,164,188,0.055)", line_width=0)
    fig.add_vrect(x0=-20, x1=60, fillcolor="rgba(214,180,95,0.045)", line_width=0)
    fig.add_vrect(x0=60, x1=150, fillcolor="rgba(24,196,199,0.045)", line_width=0)
    fig.add_hrect(y0=-45, y1=65, fillcolor="rgba(255,255,255,0.018)", line_width=0)
    fig.add_annotation(text="Americas", x=-100, y=78, showarrow=False, font={"color": "#65758A", "size": 11})
    fig.add_annotation(text="Europe / Africa", x=20, y=78, showarrow=False, font={"color": "#65758A", "size": 11})
    fig.add_annotation(text="Asia-Pacific", x=105, y=78, showarrow=False, font={"color": "#65758A", "size": 11})
    fig.update_layout(height=520)
    fig.update_xaxes(range=[-180, 180], title="Longitude", dtick=45)
    fig.update_yaxes(range=[-60, 85], title="Latitude", dtick=20, scaleanchor="x", scaleratio=1)
    return apply_workstation_theme(fig)


def live_event_map_html(feed: pd.DataFrame) -> str:
    frame = feed.dropna(subset=["latitude", "longitude"]).copy()
    if frame.empty:
        points = (
            '<div class="ca-map-empty">No geocoded catastrophe events available from the current feed.</div>'
        )
    else:
        point_html = []
        for _, row in frame.iterrows():
            lon = float(row["longitude"])
            lat = float(row["latitude"])
            x = max(0, min(100, (lon + 180) / 360 * 100))
            y = max(0, min(100, (85 - lat) / 145 * 100))
            peril = str(row.get("peril", "Event"))
            color = PERIL_COLORS.get(peril, "#18C4C7")
            size = float(row.get("marker_size", 9) if pd.notna(row.get("marker_size", 9)) else 9)
            size = max(9, min(22, size))
            place = escape(str(row.get("place", "Unknown location")))
            label = escape(peril)
            point_html.append(
                f"""
                <div class="ca-map-point" title="{place} | {label}"
                     style="left:{x:.2f}%; top:{y:.2f}%; width:{size:.1f}px; height:{size:.1f}px;
                            background:{color}; box-shadow:0 0 16px {color};">
                    <span>{label}</span>
                </div>
                """
            )
        points = "".join(point_html)

    legend_items = "".join(
        f'<span><i style="background:{color};"></i>{escape(peril)}</span>'
        for peril, color in PERIL_COLORS.items()
    )
    world_svg = """
    <svg class="ca-world-svg" viewBox="0 0 1000 520" preserveAspectRatio="none" aria-hidden="true">
        <g class="ca-continent">
            <path d="M54,150 L86,106 L142,86 L206,105 L238,142 L218,184 L170,202 L148,246 L104,246 L74,216 Z"/>
            <path d="M155,246 L200,270 L220,326 L206,392 L178,470 L144,440 L128,360 L116,304 Z"/>
            <path d="M300,140 L356,118 L396,144 L382,188 L318,188 Z"/>
            <path d="M402,132 L480,104 L570,122 L636,156 L668,206 L610,230 L548,212 L490,236 L424,206 Z"/>
            <path d="M390,210 L444,224 L474,292 L456,388 L410,430 L362,360 L346,276 Z"/>
            <path d="M602,210 L700,198 L772,242 L806,316 L768,384 L680,342 L646,282 Z"/>
            <path d="M764,354 L838,370 L882,424 L846,468 L760,442 L724,392 Z"/>
            <path d="M884,328 L922,338 L942,360 L926,384 L888,374 Z"/>
        </g>
        <g class="ca-coastline">
            <path d="M54,150 L86,106 L142,86 L206,105 L238,142 L218,184 L170,202 L148,246 L104,246 L74,216 Z"/>
            <path d="M155,246 L200,270 L220,326 L206,392 L178,470 L144,440 L128,360 L116,304 Z"/>
            <path d="M300,140 L356,118 L396,144 L382,188 L318,188 Z"/>
            <path d="M402,132 L480,104 L570,122 L636,156 L668,206 L610,230 L548,212 L490,236 L424,206 Z"/>
            <path d="M390,210 L444,224 L474,292 L456,388 L410,430 L362,360 L346,276 Z"/>
            <path d="M602,210 L700,198 L772,242 L806,316 L768,384 L680,342 L646,282 Z"/>
            <path d="M764,354 L838,370 L882,424 L846,468 L760,442 L724,392 Z"/>
            <path d="M884,328 L922,338 L942,360 L926,384 L888,374 Z"/>
        </g>
        <g class="ca-islands">
            <circle cx="246" cy="220" r="7"/>
            <circle cx="292" cy="204" r="5"/>
            <circle cx="680" cy="250" r="5"/>
            <circle cx="708" cy="264" r="4"/>
            <circle cx="820" cy="308" r="5"/>
            <circle cx="860" cy="286" r="4"/>
        </g>
    </svg>
    """
    return f"""
    <style>
    .ca-map-wrap {{
        position: relative;
        height: 520px;
        border: 1px solid rgba(221,230,237,0.14);
        border-radius: 4px;
        overflow: hidden;
        background:
            radial-gradient(circle at 18% 28%, rgba(116,185,242,0.12), transparent 18%),
            radial-gradient(circle at 76% 45%, rgba(24,196,199,0.11), transparent 22%),
            linear-gradient(90deg, rgba(116,164,188,0.08) 0 41%, rgba(214,180,95,0.055) 41% 67%, rgba(24,196,199,0.075) 67% 100%),
            linear-gradient(180deg, rgba(9,22,38,0.98), rgba(5,13,24,0.99));
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.04), 0 12px 30px rgba(0,0,0,0.18);
    }}
    .ca-map-wrap::before {{
        content: "";
        position: absolute;
        inset: 0;
        background-image:
            linear-gradient(rgba(221,230,237,0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(221,230,237,0.08) 1px, transparent 1px);
        background-size: 8.333% 13.793%;
        opacity: 0.55;
    }}
    .ca-world-svg {{
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        z-index: 1;
        opacity: 0.92;
        filter: drop-shadow(0 0 16px rgba(24,196,199,0.10));
    }}
    .ca-continent path {{
        fill: rgba(35, 60, 82, 0.70);
    }}
    .ca-coastline path {{
        fill: none;
        stroke: rgba(221,230,237,0.24);
        stroke-width: 1.2;
    }}
    .ca-islands circle {{
        fill: rgba(35, 60, 82, 0.70);
        stroke: rgba(221,230,237,0.20);
        stroke-width: 1;
    }}
    .ca-map-title {{
        position: absolute;
        left: 18px;
        top: 16px;
        z-index: 6;
        color: #F5F7FA;
        font-weight: 750;
        font-size: 15px;
    }}
    .ca-map-subtitle {{
        position: absolute;
        left: 18px;
        top: 42px;
        z-index: 6;
        color: #9AA7B8;
        font-size: 12px;
    }}
    .ca-map-region {{
        position: absolute;
        top: 72px;
        z-index: 5;
        color: rgba(221,230,237,0.28);
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }}
    .ca-map-region.americas {{ left: 18%; }}
    .ca-map-region.emea {{ left: 48%; }}
    .ca-map-region.apac {{ left: 78%; }}
    .ca-map-equator {{
        position: absolute;
        left: 0;
        right: 0;
        top: 58.6%;
        border-top: 1px dashed rgba(221,230,237,0.18);
        z-index: 2;
    }}
    .ca-map-point {{
        position: absolute;
        z-index: 7;
        transform: translate(-50%, -50%);
        border: 2px solid #07101D;
        border-radius: 50%;
        cursor: default;
    }}
    .ca-map-point span {{
        display: none;
        position: absolute;
        left: 14px;
        top: -9px;
        white-space: nowrap;
        color: #F5F7FA;
        background: rgba(7,16,29,0.94);
        border: 1px solid rgba(221,230,237,0.18);
        border-radius: 3px;
        padding: 3px 6px;
        font-size: 11px;
    }}
    .ca-map-point:hover span {{ display: block; }}
    .ca-map-legend {{
        position: absolute;
        left: 18px;
        bottom: 14px;
        z-index: 5;
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        color: #DDE6ED;
        font-size: 12px;
    }}
    .ca-map-legend span {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }}
    .ca-map-legend i {{
        width: 9px;
        height: 9px;
        display: inline-block;
        border-radius: 50%;
    }}
    .ca-map-empty {{
        position: absolute;
        inset: 0;
        display: grid;
        place-items: center;
        color: #DDE6ED;
        z-index: 3;
    }}
    </style>
    <div class="ca-map-wrap">
        {world_svg}
        <div class="ca-map-title">Live Catastrophe Feed</div>
        <div class="ca-map-subtitle">Global event monitor with deployment-safe embedded map layer</div>
        <div class="ca-map-region americas">Americas</div>
        <div class="ca-map-region emea">Europe / Africa</div>
        <div class="ca-map-region apac">Asia-Pacific</div>
        <div class="ca-map-equator"></div>
        {points}
        <div class="ca-map-legend">{legend_items}</div>
    </div>
    """


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
