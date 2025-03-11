# portfolio-analysis

Using riskfolio-lib to analyze portfolio data

### Current Analysis

```
python3 main.py

Downloading historical price data...
YF.download() has changed argument auto_adjust default to True
[*********************100%***********************]  9 of 9 completed
Data columns: ['Close', 'High', 'Low', 'Open', 'Volume']
Using 'Close' prices instead of 'Adj Close'

Sample of returns data:
Ticker          AAPL       ARM      INTC      META      MSFT      NVDA     TCEHY       TSM       VOO
Date
2023-09-15 -0.004154 -0.044661 -0.020429 -0.036603 -0.025037 -0.036880 -0.011745 -0.024270 -0.012467
2023-09-18  0.016913 -0.045267  0.002904  0.007459 -0.003513  0.001503 -0.009903 -0.004706  0.001101
2023-09-19  0.006181 -0.048793 -0.043432  0.008329 -0.001246 -0.010144 -0.009252 -0.007430 -0.002004
2023-09-20 -0.019992 -0.040964 -0.045405 -0.017701 -0.023977 -0.029435 -0.006058 -0.009981 -0.009354
2023-09-21 -0.008889 -0.014175 -0.001153 -0.013148 -0.003866 -0.028931 -0.027425 -0.022110 -0.016388

Creating portfolio object...

Calculating risk metrics for current portfolio...
Error calculating current portfolio metrics: 'Portfolio' object has no attribute 'port_risk'

Calculating efficient frontier...
Error calculating efficient frontier: 'Portfolio' object has no attribute 'ef_minimum_risk'

Calculating risk contributions...
Error calculating risk contributions: 'Portfolio' object has no attribute 'risk_contribution'

Calculating alternative portfolios...
Error calculating risk parity portfolio: 'Portfolio' object has no attribute 'weights'
Error calculating Mean-CVaR portfolio: 'Portfolio' object has no attribute 'ef_minimum_risk'
Error calculating portfolio metrics comparison: 'Portfolio' object has no attribute 'port_return'

Performing stress testing...

Stress Test Results:
                        Expected Portfolio Return (%)
Market Crash (-30%)                        -19.337392
Moderate Decline (-15%)                     -9.668696
Minor Correction (-5%)                      -3.222899

Recommended Portfolio Changes:
Decrease VOO by 32.70%
Decrease META by 31.41%
Decrease ARM by 20.55%
Decrease TSM by 15.97%
Decrease TCEHY by 11.19%
Decrease MSFT by 6.33%
Decrease INTC by 1.27%
Increase AAPL by 0.09%
Increase NVDA by 19.33%

Analysis complete.
```

```
python3 analyze_portfolio.py

Using predefined portfolio weights:
VOO: 32.70%
META: 31.41%
ARM: 20.55%
TSM: 15.97%
TCEHY: 11.19%
MSFT: 6.33%
INTC: 1.27%
AAPL: -0.09%
NVDA: -19.33%

Downloading historical price data...
YF.download() has changed argument auto_adjust default to True
[*********************100%***********************]  9 of 9 completed
Using 'Close' prices
Successfully downloaded data for 9 tickers
Time period: 2023-09-15 00:00:00 to 2025-03-10 00:00:00
Number of data points: 371

Creating portfolio object...

Current Portfolio - Expected Annual Return: 35.24%
Current Portfolio - Annual Volatility: 25.98%
Current Portfolio - Sharpe Ratio: -1.1367

Risk Contribution Analysis:
ARM: 53.22% of total risk
META: 27.97% of total risk
TSM: 15.77% of total risk
VOO: 11.15% of total risk
TCEHY: 4.55% of total risk
MSFT: 2.78% of total risk
INTC: 0.90% of total risk
AAPL: -0.03% of total risk
NVDA: -16.32% of total risk

Portfolio Concentration Score: 0.3274
Normalized Concentration (0-1 scale): 0.2433
Your portfolio is relatively well-diversified in terms of allocation.

Sector Exposure Analysis:
Technology: 67.30%
Broad Market ETF: 32.70%

Portfolio Recommendations:
1. Consider reducing these high-concentration positions:
   - VOO: 32.70% (aim for under 20% per position)
   - META: 31.41% (aim for under 20% per position)
   - ARM: 20.55% (aim for under 20% per position)

2. Your portfolio is heavily concentrated in technology stocks.
   Consider adding exposure to other sectors like:
   - Healthcare (e.g., XLV, JNJ, PFE)
   - Consumer Staples (e.g., XLP, PG, KO)
   - Utilities (e.g., XLU, NEE, DUK)
   - Financial Services (e.g., XLF, JPM, BAC)

3. You have short positions that increase your portfolio risk:
   - AAPL: -0.09%
   - NVDA: -19.33%
   Short positions have unlimited potential loss and can increase portfolio volatility.

4. Consider adding these assets for better diversification:
   - Bond ETFs (e.g., BND, AGG, VGLT) to reduce overall portfolio volatility
   - International market ETFs (e.g., VXUS, EFA, VWO) for geographic diversification
   - Alternative assets (e.g., GLD, VNQ) that may have lower correlation with stocks

Analysis complete.
```
