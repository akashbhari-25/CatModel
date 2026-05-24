# CatAlpha

CatAlpha is a catastrophe risk and reinsurance analytics workstation built around
probabilistic portfolio loss estimation rather than point prediction.

The project is designed for a FinRes / reinsurance analytics role:

- live catastrophe event monitoring
- global exposure portfolio analytics
- Poisson frequency modeling
- lognormal, Pareto, and GPD-style severity modeling
- Monte Carlo annual loss simulation
- excess-of-loss reinsurance layer modeling
- VaR, CVaR, PML, expected loss, and tail diagnostics
- stress scenarios for named catastrophe events
- optional clustering and anomaly analytics

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app attempts live API pulls where possible and falls back to sample event
data so the project remains demo-ready without network access.

## Project Shape

```text
cat_alpha/
  analytics/
  data/
  visualization/
app.py
requirements.txt
```

## JD Alignment

See [docs/jd_alignment.md](docs/jd_alignment.md) for a direct mapping between
CatAlpha and the D. E. Shaw Analyst - Reinsurance, Financial Research role.

## Inputs

- region exposure and policy count
- catastrophe peril selection
- event frequency assumptions
- severity distribution assumptions
- Monte Carlo simulation count
- reinsurance attachment and exhaustion points
- confidence level for VaR / CVaR
- stress scenario selection
