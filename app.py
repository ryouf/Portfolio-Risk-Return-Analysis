import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Portfolio Risk & Return Analysis", layout="wide")

# ----------------------------
# Header
# ----------------------------
st.title("Portfolio Risk & Return Analysis")
st.caption("Risk-adjusted performance evaluation and portfolio optimization framework")

# ----------------------------
# Sidebar controls
# ----------------------------
st.sidebar.header("Settings")

default_tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "TSLA", "SPY"]
universe = sorted(list(set(default_tickers + ["GOOGL", "META", "JPM", "XOM", "QQQ", "VTI", "IWM"])))

tickers = st.sidebar.multiselect(
    "Select assets (5–8 recommended)",
    options=universe,
    default=default_tickers
)

start_date = st.sidebar.date_input("Start date", value=pd.to_datetime("2021-01-01"))
end_date = st.sidebar.date_input("End date", value=pd.to_datetime("2026-02-20"))

risk_free_rate = st.sidebar.number_input(
    "Risk-free rate (annual, decimal)",
    min_value=0.0, max_value=0.20, value=0.03, step=0.005
)

n_portfolios = st.sidebar.slider("Portfolios simulated", 2000, 20000, 8000, 1000)

if len(tickers) < 2:
    st.warning("Select at least 2 assets.")
    st.stop()

# ----------------------------
# Data load (cached)
# ----------------------------
@st.cache_data(ttl=60 * 60)
def load_prices(_tickers, start, end):
    df = yf.download(_tickers, start=start, end=end, auto_adjust=True, progress=False)["Close"]
    if isinstance(df, pd.Series):
        df = df.to_frame()
    df = df.dropna(how="all")
    # Ensure every chosen asset has a complete history over the selected window
    df = df.dropna(axis=1, how="any")
    return df

prices = load_prices(tickers, start_date, end_date)

if prices.shape[1] < 2:
    st.error("After cleaning, fewer than 2 assets remain (missing data). Try different tickers or dates.")
    st.stop()

# ----------------------------
# Returns + metrics
# ----------------------------
daily_returns = prices.pct_change().dropna()

trading_days = 252
ann_return = (1 + daily_returns.mean()) ** trading_days - 1
ann_vol = daily_returns.std() * np.sqrt(trading_days)
sharpe = (ann_return - risk_free_rate) / ann_vol

metrics = pd.DataFrame({
    "Annualized Return": ann_return,
    "Annualized Volatility": ann_vol,
    "Sharpe Ratio": sharpe
}).sort_values("Sharpe Ratio", ascending=False)

# ----------------------------
# KPI row
# ----------------------------
c1, c2, c3 = st.columns(3)
c1.metric("Assets in analysis", f"{prices.shape[1]}")
c2.metric("Date range", f"{prices.index.min().date()} → {prices.index.max().date()}")
c3.metric("Risk-free rate", f"{risk_free_rate:.2%}")

st.divider()

# ----------------------------
# Row 1: cumulative returns + asset risk/return
# ----------------------------
left, right = st.columns([1.2, 1])

cum = (1 + daily_returns).cumprod()
cum_fig = px.line(cum, title="Cumulative Returns (Normalized)")
left.plotly_chart(cum_fig, use_container_width=True)

scatter_df = metrics.reset_index(names="Ticker")
scatter_fig = px.scatter(
    scatter_df,
    x="Annualized Volatility",
    y="Annualized Return",
    text="Ticker",
    title="Risk vs Return (Annualized)",
)
scatter_fig.update_traces(textposition="top center")
right.plotly_chart(scatter_fig, use_container_width=True)

# ----------------------------
# Row 2: correlation heatmap + metrics table
# ----------------------------
left2, right2 = st.columns([1.2, 1])

corr = daily_returns.corr()
heat = px.imshow(corr, title="Correlation Heatmap", aspect="auto")
left2.plotly_chart(heat, use_container_width=True)

right2.subheader("Asset Metrics")
right2.dataframe(
    metrics.style.format({
        "Annualized Return": "{:.2%}",
        "Annualized Volatility": "{:.2%}",
        "Sharpe Ratio": "{:.2f}"
    }),
    use_container_width=True
)

st.divider()

# ----------------------------
# Efficient frontier simulation
# ----------------------------
st.subheader("Portfolio Optimization (Monte Carlo)")

mean_daily = daily_returns.mean()
cov_daily = daily_returns.cov()

np.random.seed(42)
n_assets = prices.shape[1]

weights_list = []
port_returns = []
port_vols = []
port_sharpes = []

for _ in range(n_portfolios):
    w = np.random.random(n_assets)
    w = w / np.sum(w)

    r = np.sum(mean_daily * w) * trading_days
    v = np.sqrt(np.dot(w.T, np.dot(cov_daily * trading_days, w)))
    s = (r - risk_free_rate) / v if v > 0 else np.nan

    weights_list.append(w)
    port_returns.append(r)
    port_vols.append(v)
    port_sharpes.append(s)

ef = pd.DataFrame({
    "Return": port_returns,
    "Volatility": port_vols,
    "Sharpe": port_sharpes
}).dropna()

best_idx = ef["Sharpe"].idxmax()
best = ef.loc[best_idx]
best_weights = pd.Series(weights_list[best_idx], index=prices.columns).sort_values(ascending=False)

# Efficient frontier plot + highlight Max Sharpe point
ef_fig = px.scatter(
    ef,
    x="Volatility",
    y="Return",
    title="Efficient Frontier (Simulated Portfolios)",
)
ef_fig.add_scatter(
    x=[best["Volatility"]],
    y=[best["Return"]],
    mode="markers",
    marker=dict(size=12),
    name="Max Sharpe Portfolio"
)
st.plotly_chart(ef_fig, use_container_width=True)

# ----------------------------
# Portfolio-level KPIs
# ----------------------------
st.subheader("Portfolio-Level Metrics (Max Sharpe)")

c4, c5, c6 = st.columns(3)
c4.metric("Expected Annual Return", f"{best['Return']:.2%}")
c5.metric("Expected Volatility", f"{best['Volatility']:.2%}")
c6.metric("Sharpe Ratio", f"{best['Sharpe']:.2f}")

# ----------------------------
# Weights table
# ----------------------------
st.subheader("Optimal Weights (Max Sharpe)")
st.dataframe(
    best_weights.to_frame("Weight").style.format({"Weight": "{:.2%}"}),
    use_container_width=True
)

# ----------------------------
# Executive interpretation
# ----------------------------
st.markdown("### Executive Interpretation")

st.write("""
The maximum Sharpe portfolio achieves superior capital efficiency by optimizing 
return per unit of risk.

The allocation structure demonstrates diversification benefits, as exposure 
is distributed across assets with varying correlation profiles, reducing 
unsystematic risk concentration.

From a portfolio construction perspective, this framework supports disciplined, 
risk-adjusted decision-making aligned with modern portfolio theory principles.
""")