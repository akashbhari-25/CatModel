from __future__ import annotations

import pandas as pd
import streamlit as st

from cat_alpha.analytics.clustering import cluster_regions
from cat_alpha.analytics.insights import (
    exposure_insights,
    live_feed_insights,
    monte_carlo_insights,
    portfolio_intelligence_insights,
    reinsurance_insights,
    stress_insights,
    tail_risk_insights,
)
from cat_alpha.analytics.monte_carlo import run_portfolio_simulation
from cat_alpha.analytics.stress_testing import SCENARIOS, run_stress_scenario
from cat_alpha.data.exposure_data import default_exposure_portfolio, exposure_summary
from cat_alpha.data.live_feed import fetch_live_catastrophe_feed
from cat_alpha.visualization.plots import (
    exposure_bar,
    live_event_deck,
    loss_distribution,
    peril_mix_bar,
    regional_tail_bar,
)


st.set_page_config(
    page_title="CatAlpha",
    page_icon="CA",
    layout="wide",
)


st.markdown(
    """
    <style>
    :root {
        --ca-bg: #07101D;
        --ca-panel: #0D1828;
        --ca-panel-2: #111F33;
        --ca-border: rgba(221, 230, 237, 0.14);
        --ca-text: #F5F7FA;
        --ca-muted: #9AA7B8;
        --ca-accent: #18C4C7;
        --ca-gold: #D6B45F;
        --ca-red: #E26D5C;
        --ca-green: #63C384;
    }
    header[data-testid="stHeader"] {
        background: rgba(7,16,29,0);
    }
    #MainMenu, footer, div[data-testid="stDecoration"] {
        visibility: hidden;
        height: 0;
    }
    .stApp {
        background:
            linear-gradient(180deg, rgba(7,16,29,0.98), rgba(7,16,29,1)),
            radial-gradient(circle at top right, rgba(24,196,199,0.10), transparent 32%);
    }
    .block-container {
        padding-top: 0.7rem;
        padding-bottom: 2.2rem;
        max-width: 1540px;
    }
    div[data-testid="stSidebar"] {
        border-right: 1px solid var(--ca-border);
        background: #081323;
    }
    div[data-testid="stSidebar"] h1,
    div[data-testid="stSidebar"] h2,
    div[data-testid="stSidebar"] h3 {
        letter-spacing: 0.02em;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(180deg, rgba(17,31,51,0.98), rgba(9,20,34,0.98));
        border: 1px solid var(--ca-border);
        border-radius: 4px;
        padding: 14px 14px 12px;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.035), 0 12px 30px rgba(0,0,0,0.22);
    }
    div[data-testid="stMetricLabel"] p {
        color: var(--ca-muted);
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }
    div[data-testid="stMetricValue"] {
        color: var(--ca-text);
        font-size: 1.55rem;
    }
    .ca-header {
        display: flex;
        justify-content: space-between;
        align-items: stretch;
        gap: 24px;
        border-bottom: 1px solid var(--ca-border);
        padding: 8px 0 14px;
        margin-bottom: 12px;
    }
    .ca-kicker {
        color: var(--ca-accent);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 3px;
    }
    .ca-title {
        font-size: 2.0rem;
        line-height: 1.05;
        font-weight: 700;
        color: var(--ca-text);
    }
    .ca-subtitle {
        color: var(--ca-muted);
        max-width: 720px;
        margin-top: 8px;
        font-size: 0.95rem;
    }
    .ca-status {
        border: 1px solid var(--ca-border);
        border-radius: 4px;
        background: rgba(13,24,40,0.92);
        padding: 11px 13px;
        min-width: 330px;
        color: var(--ca-muted);
        font-size: 0.80rem;
        display: grid;
        align-content: center;
    }
    .ca-status strong {
        color: var(--ca-text);
    }
    .ca-panel {
        border: 1px solid var(--ca-border);
        border-radius: 4px;
        background: linear-gradient(180deg, rgba(16,29,47,0.94), rgba(11,22,37,0.94));
        padding: 14px 16px;
        margin-bottom: 14px;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.035);
    }
    .ca-panel-title {
        color: var(--ca-text);
        font-size: 0.92rem;
        font-weight: 700;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .ca-panel ul {
        margin: 0;
        padding-left: 1.05rem;
        color: var(--ca-muted);
        font-size: 0.92rem;
    }
    .ca-panel li {
        margin: 0.45rem 0;
    }
    .ca-callout {
        border-left: 3px solid var(--ca-accent);
        background: rgba(0,179,179,0.08);
        padding: 10px 12px;
        color: #DDE6ED;
        border-radius: 0 4px 4px 0;
        margin-bottom: 12px;
        font-size: 0.92rem;
    }
    .ca-strip {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 10px;
        margin: 10px 0 14px;
    }
    .ca-strip-cell {
        border: 1px solid var(--ca-border);
        border-radius: 4px;
        background: rgba(13,24,40,0.78);
        padding: 10px 12px;
    }
    .ca-strip-label {
        color: var(--ca-muted);
        font-size: 0.70rem;
        text-transform: uppercase;
        letter-spacing: 0.07em;
    }
    .ca-strip-value {
        color: var(--ca-text);
        font-size: 0.96rem;
        margin-top: 3px;
        font-weight: 650;
    }
    .ca-led {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 7px;
        vertical-align: 1px;
        background: var(--ca-green);
        box-shadow: 0 0 10px rgba(99,195,132,0.7);
    }
    .ca-led.warn {
        background: var(--ca-gold);
        box-shadow: 0 0 10px rgba(214,180,95,0.65);
    }
    .ca-led.risk {
        background: var(--ca-red);
        box-shadow: 0 0 10px rgba(226,109,92,0.7);
    }
    .ca-section {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        margin: 4px 0 10px;
    }
    .ca-section h3 {
        color: var(--ca-text);
        font-size: 1.02rem;
        margin: 0;
        letter-spacing: 0.01em;
    }
    .ca-tag {
        border: 1px solid rgba(24,196,199,0.35);
        color: #BDFBFB;
        background: rgba(24,196,199,0.08);
        border-radius: 3px;
        padding: 4px 7px;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .ca-ruling {
        border: 1px solid var(--ca-border);
        background: rgba(8,19,35,0.72);
        border-radius: 4px;
        padding: 11px 12px;
        color: var(--ca-muted);
        font-size: 0.85rem;
        margin-bottom: 12px;
    }
    .ca-ruling strong {
        color: var(--ca-text);
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--ca-border);
        border-radius: 4px;
    }
    div[data-testid="stTabs"] [role="tablist"] {
        border-bottom: 1px solid var(--ca-border);
        gap: 4px;
    }
    button[data-baseweb="tab"] {
        font-size: 0.82rem;
        padding-top: 10px;
        padding-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.035em;
        color: var(--ca-muted);
        border-radius: 4px 4px 0 0;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: rgba(24,196,199,0.08);
        color: var(--ca-text);
    }
    @media (max-width: 900px) {
        .ca-header, .ca-strip {
            display: block;
        }
        .ca-status, .ca-strip-cell {
            margin-top: 10px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=900)
def cached_feed() -> pd.DataFrame:
    return fetch_live_catastrophe_feed()


@st.cache_data
def cached_portfolio() -> pd.DataFrame:
    return default_exposure_portfolio()


def metric_card(label: str, value: str, help_text: str | None = None) -> None:
    st.metric(label, value, help=help_text)


def insight_panel(title: str, items: list[str]) -> None:
    body = "".join(f"<li>{item}</li>" for item in items)
    st.markdown(
        f"""
        <div class="ca-panel">
            <div class="ca-panel-title">{title}</div>
            <ul>{body}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def model_note(text: str) -> None:
    st.markdown(f'<div class="ca-callout">{text}</div>', unsafe_allow_html=True)


def section_header(title: str, tag: str) -> None:
    st.markdown(
        f"""
        <div class="ca-section">
            <h3>{title}</h3>
            <span class="ca-tag">{tag}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def governance_strip(
    simulations: int,
    confidence: float,
    attachment: float,
    exhaustion: float,
    capital_relief: float,
) -> None:
    relief_class = "risk" if capital_relief < 0 else "warn" if capital_relief < 0.25 else ""
    st.markdown(
        f"""
        <div class="ca-strip">
            <div class="ca-strip-cell">
                <div class="ca-strip-label">Model Build</div>
                <div class="ca-strip-value"><span class="ca-led"></span>CAT-ALPHA v0.2</div>
            </div>
            <div class="ca-strip-cell">
                <div class="ca-strip-label">Run Profile</div>
                <div class="ca-strip-value">{simulations:,} sims | {confidence:.1%} tail</div>
            </div>
            <div class="ca-strip-cell">
                <div class="ca-strip-label">XOL Layer</div>
                <div class="ca-strip-value">${attachment:,.0f}M xs ${max(exhaustion - attachment, 0):,.0f}M</div>
            </div>
            <div class="ca-strip-cell">
                <div class="ca-strip-label">Capital Relief</div>
                <div class="ca-strip-value"><span class="ca-led {relief_class}"></span>{capital_relief:.1%} CVaR reduction</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def underwriting_ruling(title: str, verdict: str, rationale: str) -> None:
    st.markdown(
        f"""
        <div class="ca-ruling">
            <strong>{title}:</strong> {verdict}<br/>
            {rationale}
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <div class="ca-header">
        <div>
            <div class="ca-kicker">Internal reinsurance research terminal</div>
            <div class="ca-title">CatAlpha</div>
            <div class="ca-subtitle">
                Portfolio catastrophe intelligence, contract-layer economics, stress-event triage,
                and tail-capital diagnostics for underwriting and financial research workflows.
            </div>
        </div>
        <div class="ca-status">
            <strong>Book:</strong> Global property catastrophe / retro view<br/>
            <strong>Model mode:</strong> stochastic annual aggregate loss<br/>
            <strong>Decision lens:</strong> EL, CVaR, PML, retained capital
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

portfolio = cached_portfolio()

with st.sidebar:
    st.header("Control Panel")
    simulations = st.slider("Monte Carlo runs", 1_000, 100_000, 10_000, step=1_000)
    confidence_pct = st.slider("Confidence level", 90, 995, 990, step=5) / 1000
    attachment_m = st.number_input("XOL attachment ($M)", value=100.0, min_value=0.0, step=25.0)
    exhaustion_m = st.number_input("XOL exhaustion ($M)", value=500.0, min_value=0.0, step=25.0)
    tail_probability = st.slider("Tail shock probability", 0.0, 0.15, 0.025, step=0.005)
    pareto_alpha = st.slider("Pareto tail alpha", 1.2, 5.0, 2.2, step=0.1)
    selected_regions = st.multiselect(
        "Portfolio regions",
        options=portfolio["region"].tolist(),
        default=portfolio["region"].tolist(),
    )

portfolio = portfolio[portfolio["region"].isin(selected_regions)].reset_index(drop=True)
if portfolio.empty:
    st.warning("Select at least one region to run the portfolio model.")
    st.stop()

with st.sidebar.expander("Exposure assumptions", expanded=False):
    portfolio = st.data_editor(
        portfolio,
        use_container_width=True,
        hide_index=True,
        disabled=["region", "peril", "country"],
        key="portfolio_assumptions",
    )

simulation = run_portfolio_simulation(
    portfolio=portfolio,
    simulations=simulations,
    confidence=confidence_pct,
    attachment_m=attachment_m,
    exhaustion_m=exhaustion_m,
    tail_probability=tail_probability,
    pareto_alpha=pareto_alpha,
)
summary = exposure_summary(portfolio)
capital_relief = 1 - simulation["retained_risk"]["cvar_m"] / simulation["gross_risk"]["cvar_m"]

governance_strip(simulations, confidence_pct, attachment_m, exhaustion_m, capital_relief)

top = st.container()
with top:
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        metric_card("Total Exposure", f"${summary['total_exposure_m']:,.0f}M")
    with c2:
        metric_card("Expected Gross Loss", f"${simulation['gross_risk']['expected_loss_m']:,.1f}M")
    with c3:
        metric_card(f"{confidence_pct:.1%} Gross VaR", f"${simulation['gross_risk']['var_m']:,.1f}M")
    with c4:
        metric_card(f"{confidence_pct:.1%} Retained VaR", f"${simulation['retained_risk']['var_m']:,.1f}M")
    with c5:
        metric_card("Layer Attachment Prob.", f"{simulation['layer']['probability_layer_attaches']:.1%}")

tabs = st.tabs(
    [
        "Live Feed",
        "Exposure",
        "Monte Carlo",
        "Reinsurance",
        "Tail Risk",
        "Stress Tests",
        "Portfolio Intelligence",
    ]
)

with tabs[0]:
    section_header("Live Catastrophe Feed", "Event triage")
    feed = cached_feed()
    model_note("Use this view as the daily monitoring layer: identify active natural catastrophes, then move material events into stress testing.")
    left, right = st.columns([1.45, 0.8])
    with left:
        st.pydeck_chart(live_event_deck(feed), height=560, use_container_width=True)
        st.dataframe(feed, use_container_width=True, hide_index=True)
    with right:
        underwriting_ruling(
            "Monitoring ruling",
            "Review active perils against top exposed zones",
            "A live event is only decision-relevant when it intersects exposure, contract attachment, and plausible severity.",
        )
        insight_panel("Desk Readout", live_feed_insights(feed))

with tabs[1]:
    section_header("Exposure Portfolio", "Book composition")
    model_note("Exposure is the base of the risk stack. Small changes in concentrated zones can dominate tail results.")
    left, mid, right = st.columns([1.15, 0.9, 0.8])
    with left:
        st.dataframe(
            portfolio,
            use_container_width=True,
            hide_index=True,
        )
    with mid:
        st.plotly_chart(exposure_bar(portfolio), use_container_width=True)
    with right:
        st.plotly_chart(peril_mix_bar(portfolio), use_container_width=True)
        underwriting_ruling(
            "Concentration ruling",
            "Treat largest region and largest peril as primary tail drivers",
            "Concentration does not always mean bad risk, but it should receive explicit pricing and stress justification.",
        )
        insight_panel("Exposure Notes", exposure_insights(portfolio, summary))

with tabs[2]:
    section_header("Annual Loss Simulation", "Stochastic engine")
    model_note("This tab estimates a distribution of possible annual portfolio losses. The goal is not exact prediction; it is tail-aware risk estimation.")
    left, mid, right = st.columns([1.25, 0.95, 0.8])
    with left:
        st.plotly_chart(
            loss_distribution(simulation["gross_losses"], "Gross Annual Portfolio Loss Distribution"),
            use_container_width=True,
        )
    with mid:
        st.plotly_chart(regional_tail_bar(simulation["region_expected"]), use_container_width=True)
    with right:
        underwriting_ruling(
            "Simulation ruling",
            "Use VaR and CVaR as portfolio risk constraints",
            "Expected loss prices the center of the distribution; tail metrics govern capital, reinsurance need, and risk appetite.",
        )
        insight_panel("Simulation Interpretation", monte_carlo_insights(simulation, confidence_pct))
        st.dataframe(simulation["region_expected"], use_container_width=True, hide_index=True)

with tabs[3]:
    section_header("Reinsurance Layer Analysis", "Contract economics")
    model_note("The selected XOL layer converts gross catastrophe loss into ceded and retained loss. This is the core contract economics view.")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Mean Gross", f"${simulation['layer']['mean_gross_loss_m']:,.1f}M")
    with c2:
        metric_card("Mean Ceded", f"${simulation['layer']['mean_ceded_loss_m']:,.1f}M")
    with c3:
        metric_card("Mean Retained", f"${simulation['layer']['mean_retained_loss_m']:,.1f}M")
    with c4:
        metric_card("Ceded Share", f"{simulation['layer']['ceded_share']:.1%}")
    left, mid, right = st.columns([1, 1, 0.78])
    with left:
        st.plotly_chart(
            loss_distribution(simulation["ceded_losses"], "Ceded Loss Distribution"),
            use_container_width=True,
        )
    with mid:
        st.plotly_chart(
            loss_distribution(simulation["retained_losses"], "Retained Loss Distribution"),
            use_container_width=True,
        )
    with right:
        underwriting_ruling(
            "Layer ruling",
            "Assess attachment probability before judging premium adequacy",
            "High attachment probability implies frequent loss participation; low attachment probability shifts focus to tail protection value.",
        )
        insight_panel("Layer Recommendations", reinsurance_insights(simulation))

with tabs[4]:
    section_header("Tail Risk", "Capital view")
    model_note("Tail metrics are the capital and risk appetite view. CVaR and PML are usually more informative than expected loss for catastrophe portfolios.")
    gross = simulation["gross_risk"]
    retained = simulation["retained_risk"]
    tail_table = pd.DataFrame(
        [
            {"basis": "Gross", **gross},
            {"basis": "Retained", **retained},
        ]
    )
    left, right = st.columns([1.1, 0.8])
    with left:
        st.dataframe(tail_table, use_container_width=True, hide_index=True)
        st.plotly_chart(
            loss_distribution(simulation["retained_losses"], "Retained Annual Loss Distribution"),
            use_container_width=True,
        )
    with right:
        underwriting_ruling(
            "Capital ruling",
            "Retained CVaR is the key residual risk number",
            "If CVaR remains high after the selected layer, the book may need higher attachment discipline or additional retro protection.",
        )
        insight_panel("Tail-Risk Readout", tail_risk_insights(simulation))

with tabs[5]:
    section_header("Stress Scenario Engine", "Event memo")
    model_note("Stress tests translate named catastrophe events into gross, ceded, and retained loss for fast underwriter discussion.")
    scenario_name = st.selectbox("Scenario", list(SCENARIOS.keys()))
    stress = run_stress_scenario(portfolio, scenario_name, attachment_m, exhaustion_m)
    st.info(stress["narrative"])
    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Gross Scenario Loss", f"${stress['gross_loss_m']:,.1f}M")
    with c2:
        metric_card("Ceded Scenario Loss", f"${stress['ceded_loss_m']:,.1f}M")
    with c3:
        metric_card("Retained Scenario Loss", f"${stress['retained_loss_m']:,.1f}M")
    underwriting_ruling(
        "Scenario ruling",
        "Use retained scenario loss as the underwriter discussion anchor",
        "Gross loss explains event severity; retained loss explains economic exposure after contract protection.",
    )
    insight_panel("Scenario Recommendations", stress_insights(stress))

with tabs[6]:
    section_header("Portfolio Intelligence", "Research signals")
    model_note("This view summarizes concentration, diversification, and risk clustering. It is the starting point for deal-flow impact analysis.")
    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Largest Region Share", f"{summary['largest_region_share']:.1%}")
    with c2:
        metric_card("Exposure HHI", f"{summary['exposure_hhi']:.3f}")
    with c3:
        metric_card("Policies", f"{summary['policy_count']:,.0f}")
    left, right = st.columns([1.1, 0.85])
    with left:
        st.dataframe(cluster_regions(portfolio), use_container_width=True, hide_index=True)
    with right:
        underwriting_ruling(
            "Portfolio ruling",
            "Every new deal should be evaluated on marginal tail contribution",
            "A contract can be attractive on expected margin while still worsening portfolio CVaR or concentration.",
        )
        insight_panel("Portfolio Actions", portfolio_intelligence_insights(summary))
