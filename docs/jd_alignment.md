# CatAlpha JD Alignment

Role: Analyst - Reinsurance, Financial Research

## What The JD Actually Wants

The JD is not asking for a generic finance dashboard. It points to a workflow
that supports underwriters and brokers through catastrophe modeling, contract
analytics, portfolio monitoring, and regular reporting.

Core workstreams:

- catastrophe modeling for insurance, reinsurance, and retrocession contracts
- expected loss analysis on both per-contract and portfolio basis
- understanding of reinsurance structures such as per-occurrence, XOL, and aggregate
- awareness of ILWs, cat bonds, reinsurance, and retrocession contracts
- monitoring natural catastrophes globally and assessing portfolio impact
- deal-flow based portfolio maintenance
- claims information verification and reporting
- building analytical tools and optimizing team workflows

## What CatAlpha Already Covers

CatAlpha Phase 1 maps well to these JD requirements:

- Daily catastrophe monitoring:
  - live USGS earthquake feed
  - NOAA/NASA-style hooks for storm and wildfire feeds
  - global event map and event table

- Catastrophe modeling:
  - Poisson event frequency model
  - lognormal severity model
  - Pareto tail amplification
  - Monte Carlo annual loss simulation

- Expected loss:
  - expected gross portfolio loss
  - expected regional loss contribution
  - retained expected loss after reinsurance

- Portfolio analytics:
  - global exposure portfolio by region and peril
  - concentration analytics
  - exposure HHI
  - risk clustering

- Reinsurance structures:
  - XOL attachment and exhaustion modeling
  - ceded loss
  - retained loss
  - probability that the layer attaches

- Business decision support:
  - VaR, CVaR, PML
  - stress scenarios
  - gross vs retained loss comparison
  - scenario-level reinsurer impact

## Gaps To Close For A Stronger DE Shaw-Level Project

These are the next features that would make the project much closer to the JD:

1. Per-Contract Modeling

Add a contract table with:

- contract ID
- counterparty / broker
- peril
- covered region
- limit
- attachment
- exhaustion
- premium
- expected loss
- rate on line
- technical margin

This directly addresses "calculate expected loss on a per-contract and portfolio basis."

2. More Reinsurance Structures

Add:

- per-occurrence XOL
- aggregate annual cover
- quota share
- stop loss
- retrocession layer

This maps directly to "per occurrence, XOL, aggregate, etc."

3. ILW Module

Industry loss warranty payoff:

- trigger industry loss threshold
- notional
- binary payout
- modeled trigger probability
- expected payout

This maps directly to "instrument types such as industry loss warranties."

4. Cat Bond Module

Cat bond analytics:

- principal
- coupon spread
- trigger probability
- expected principal impairment
- expected investor return
- spread vs expected loss

This maps directly to "cat bonds."

5. Deal Flow / Portfolio Maintenance

Add a deal intake screen:

- proposed contract
- add/remove from portfolio
- before/after VaR, CVaR, PML
- marginal contribution to tail risk
- diversification impact

This maps directly to "incorporating deal flow and generating portfolio reports."

6. Claims Tracker

Add claims-related records:

- event ID
- region
- contract affected
- reported claim
- estimated ultimate loss
- paid loss
- case reserve
- IBNR estimate
- data quality flag

This maps directly to "verify and maintain claims-related information."

7. Underwriter Report Generator

Generate a concise report:

- current live events
- affected portfolio regions
- expected loss impact
- layer attachment probability
- stress losses
- top risk drivers
- recommended attention items

This maps directly to "meaningful and actionable analytical support."

## Interview Positioning

The strongest way to describe this project:

CatAlpha is a catastrophe risk and reinsurance analytics workstation that
combines live natural catastrophe monitoring, probabilistic loss simulation,
contract-level reinsurance economics, and portfolio tail-risk analytics to help
underwriters understand expected loss, retained risk, and stress-event impacts.

The important positioning is:

- not a stock prediction project
- not an AI disaster predictor
- not a generic dashboard
- a probabilistic risk and decision-support system

