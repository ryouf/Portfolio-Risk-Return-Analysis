# Portfolio Risk & Return Analysis
**Risk-Adjusted Performance Evaluation and Portfolio Optimization Framework**

---

## Project Overview

This project develops an interactive portfolio analytics dashboard designed to evaluate risk-adjusted performance and optimize asset allocation using Modern Portfolio Theory principles.

The core investment question addressed in this analysis is:

> How can an investor construct a diversified equity portfolio that maximizes expected return per unit of risk?

Rather than focusing solely on raw returns, this framework evaluates assets through volatility, correlation structure, and Sharpe ratio optimization. The objective is to move from performance observation to disciplined portfolio construction.

The dashboard provides an interactive environment where asset selection, time horizon, risk-free rate, and simulation depth can be adjusted dynamically to explore portfolio behavior under different assumptions.

---

## Data Source

Market data was sourced from Yahoo Finance using the `yfinance` API.

- Data type: Daily adjusted closing prices  
- Frequency: Daily  
- Time horizon: User-defined (default: 2021–2026)  
- Assets: U.S. equities and ETFs (e.g., AAPL, MSFT, NVDA, AMZN, TSLA, SPY)

Adjusted prices were used to ensure dividend and split adjustments are reflected in return calculations.

Yahoo Finance was selected due to:
- Public accessibility
- Broad coverage of equity markets
- Reliability for historical pricing analysis

---

## Methodology

### 1) Return Computation

Daily returns were calculated using percentage change in adjusted closing prices.

Annualized return was computed using geometric compounding:

$$
(1 + \bar{r}_{daily})^{252} - 1
$$

Volatility was annualized using:

$$
\sigma_{daily} \times \sqrt{252}
$$

A standard assumption of 252 trading days per year was applied.

---

### 2) Risk-Adjusted Performance

Sharpe ratio was calculated as:

$$
\frac{R_p - R_f}{\sigma_p}
$$

Where:
- \( R_p \) = Expected annual portfolio return  
- \( R_f \) = Risk-free rate (user-defined)  
- \( \sigma_p \) = Portfolio volatility  

This metric allows direct comparison of assets and portfolios on a risk-adjusted basis.

---

### 3) Correlation & Diversification

A correlation matrix was computed to evaluate inter-asset relationships.

Understanding correlation structure is critical, as diversification benefits arise when assets do not move perfectly together. Lower correlation reduces unsystematic risk concentration within the portfolio.

---

### 4) Monte Carlo Portfolio Simulation

A Monte Carlo simulation was performed to generate thousands of random portfolio allocations.

For each simulated portfolio:
- Random weights were generated and normalized
- Expected return and volatility were computed
- Sharpe ratio was evaluated

This process approximates the Efficient Frontier and identifies the portfolio with the highest Sharpe ratio (Max Sharpe Portfolio).

---

## Key Insights

1. **Risk concentration varies significantly across assets.**  
   High-growth equities (e.g., NVDA, TSLA) demonstrate superior raw returns but also materially higher volatility.

2. **Diversification materially improves risk-adjusted outcomes.**  
   The optimal allocation distributes exposure across assets with imperfect correlations, reducing total portfolio volatility relative to concentrated positions.

3. **Max Sharpe portfolio improves capital efficiency.**  
   The optimized portfolio delivers higher return per unit of risk compared to most individual assets.

4. **Correlation structure drives allocation decisions.**  
   Asset weights are influenced not only by expected return but by covariance dynamics within the portfolio.

5. **Risk-free rate sensitivity matters.**  
   Adjusting the risk-free rate meaningfully shifts Sharpe ratio optimization results, demonstrating sensitivity to macro assumptions.

---

## Assumptions & Limitations

- 252 trading days per year assumed for annualization.
- Risk-free rate is user-defined and static over the period.
- Historical returns are used as a proxy for expected returns.
- Monte Carlo simulation approximates but does not analytically derive the Efficient Frontier.
- Yahoo Finance data may contain minor historical discrepancies.

This model does not account for:
- Transaction costs
- Taxes
- Liquidity constraints
- Short-selling restrictions
- Rebalancing frequency

---

## Business Interpretation

From a portfolio construction perspective, this framework supports disciplined, quantitative decision-making aligned with institutional asset management practices.

The analysis demonstrates that optimal capital allocation emerges not from chasing the highest-return asset, but from balancing return expectations against volatility and correlation structure.

This approach reflects core principles used in investment management, risk advisory, and asset allocation strategy development.

---
