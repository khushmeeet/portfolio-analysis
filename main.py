# Portfolio Analysis with Riskfolio-Lib

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import riskfolio as rp
import yfinance as yf

# Define portfolio components based on the Robinhood portfolio data
portfolio_weights = {
    "VOO": 0.32696837455677735,
    "META": 0.314076211155608,
    "ARM": 0.20552028240241438,
    "TSM": 0.1597482981738112,
    "TCEHY": 0.11185533870633428,
    "MSFT": 0.0632978373213317,
    "INTC": 0.012749429447051862,
    "AAPL": -0.0009053423293624654,  # Short position
    "NVDA": -0.19331042943396642      # Short position
}

# 1. Data Retrieval - Get historical stock prices for the analysis
tickers = list(portfolio_weights.keys())
end_date = datetime.now()
start_date = end_date - timedelta(days=365*3)  # 3 years of data

print("Downloading historical price data...")
# Download data from Yahoo Finance with error handling
try:
    # First, let's try to download the data
    data = yf.download(tickers, start=start_date, end=end_date)

    # Check the structure of the data
    print(f"Data columns: {data.columns.levels[0].tolist() if isinstance(data.columns, pd.MultiIndex) else data.columns.tolist()}")

    # If 'Adj Close' is available in a MultiIndex column structure
    if isinstance(data.columns, pd.MultiIndex) and 'Adj Close' in data.columns.levels[0]:
        price_data = data['Adj Close']
    # If 'Close' is available in a MultiIndex
    elif isinstance(data.columns, pd.MultiIndex) and 'Close' in data.columns.levels[0]:
        price_data = data['Close']
        print("Using 'Close' prices instead of 'Adj Close'")
    # If the data is not in a MultiIndex format but has 'Adj Close'
    elif 'Adj Close' in data.columns:
        price_data = data['Adj Close']
    # If the data is not in a MultiIndex format but has 'Close'
    elif 'Close' in data.columns:
        price_data = data['Close']
        print("Using 'Close' prices instead of 'Adj Close'")
    else:
        raise KeyError("Neither 'Adj Close' nor 'Close' columns found in the data")

    # Calculate returns from prices
    returns = price_data.pct_change().dropna()

    # Display the first few rows of returns to verify
    print("\nSample of returns data:")
    print(returns.head())

except Exception as e:
    print(f"Error downloading or processing data: {e}")

    # Create mock data for demonstration if real data fails
    print("\nCreating synthetic data for demonstration purposes...")

    # Generate random returns for demonstration
    np.random.seed(42)  # For reproducibility
    dates = pd.date_range(start=start_date, end=end_date, freq='B')
    mock_returns = pd.DataFrame(
        np.random.normal(0.0005, 0.015, size=(len(dates), len(tickers))),
        index=dates,
        columns=tickers
    )

    # Use the mock data
    returns = mock_returns
    print("Using synthetic data for analysis. In a real scenario, you would need to fix the data source issue.")

# Convert the portfolio weights to a pandas Series
weights = pd.Series(portfolio_weights)

print("\nCreating portfolio object...")
# 2. Create a Portfolio object using riskfolio-lib
port = rp.Portfolio(returns=returns)

# 3. Calculate portfolio statistics and metrics
port.assets_stats(method_mu='hist', method_cov='hist')
# Note: If you need exponential weighting for covariance matrix, check the current documentation
# In some versions, it might be: port.assets_stats(method_mu='hist', method_cov='ewma', ewma_lambda=0.94)

# 4. Calculate the portfolio returns series based on current weights
portfolio_returns = returns.dot(weights)
cumulative_returns = (1 + portfolio_returns).cumprod()

print("\nCalculating risk metrics for current portfolio...")
# 5. Calculate risk metrics for the current portfolio
rm = 'MV'  # Using Mean-Variance as the risk measure
rf = 0.02  # Risk-free rate assumption (2%)

try:
    current_risk = port.port_risk(weights, rm=rm)
    current_return = port.port_return(weights)
    sharpe = port.sharpe_ratio(weights, rm=rm, rf=rf)

    print(f"Current Portfolio - Expected Annual Return: {current_return*252*100:.2f}%")
    print(f"Current Portfolio - Annual Volatility: {current_risk*np.sqrt(252)*100:.2f}%")
    print(f"Current Portfolio - Sharpe Ratio: {sharpe:.4f}")
except Exception as e:
    print(f"Error calculating current portfolio metrics: {e}")

print("\nCalculating efficient frontier...")
# 6. Estimate the efficient frontier using Mean-Variance optimization
# Define optimization parameters
model = 'Classic'  # Classic mean-variance model
obj = 'Sharpe'  # Maximize Sharpe ratio
hist = True  # Use historical returns
l = 0  # This parameter is not used when obj='Sharpe'

try:
    # Calculate the efficient frontier
    ef = port.ef_minimum_risk(model=model, rm=rm, rf=rf, hist=hist)

    # 7. Get the optimal portfolio weights
    optimal_weights = port.weights.sort_values(ascending=False)

    print("\nOptimal Portfolio Allocation:")
    for ticker, weight in optimal_weights.items():
        print(f"{ticker}: {weight*100:.2f}%")

    # Calculate metrics for optimal portfolio
    opt_return = port.port_return(optimal_weights)
    opt_risk = port.port_risk(optimal_weights, rm=rm)
    opt_sharpe = port.sharpe_ratio(optimal_weights, rm=rm, rf=rf)

    print(f"\nOptimal Portfolio - Expected Annual Return: {opt_return*252*100:.2f}%")
    print(f"Optimal Portfolio - Annual Volatility: {opt_risk*np.sqrt(252)*100:.2f}%")
    print(f"Optimal Portfolio - Sharpe Ratio: {opt_sharpe:.4f}")

except Exception as e:
    print(f"Error calculating efficient frontier: {e}")
    optimal_weights = pd.Series(index=weights.index, data=0)

print("\nCalculating risk contributions...")
# 9. Risk Decomposition Analysis for the current portfolio
# Risk contribution breakdown - how much each asset contributes to overall risk
try:
    risk_contrib = port.risk_contribution(weights, rm=rm)

    print("\nRisk Contribution Analysis:")
    for ticker, contrib in risk_contrib.sort_values(ascending=False).items():
        print(f"{ticker}: {contrib*100:.2f}% of total risk")
except Exception as e:
    print(f"Error calculating risk contributions: {e}")

print("\nCalculating alternative portfolios...")
# 11. Risk Parity Portfolio for comparison
try:
    # Calculate the risk parity portfolio
    rp_port = port.rp_optimization(model=model, rm=rm, rf=rf, hist=hist)
    rp_weights = port.weights

    # Calculate metrics for risk parity portfolio
    rp_return = port.port_return(rp_weights)
    rp_risk = port.port_risk(rp_weights, rm=rm)
    rp_sharpe = port.sharpe_ratio(rp_weights, rm=rm, rf=rf)

    print("\nRisk Parity Portfolio:")
    for ticker, weight in rp_weights.sort_values(ascending=False).items():
        print(f"{ticker}: {weight*100:.2f}%")

    print(f"\nRisk Parity - Expected Annual Return: {rp_return*252*100:.2f}%")
    print(f"Risk Parity - Annual Volatility: {rp_risk*np.sqrt(252)*100:.2f}%")
    print(f"Risk Parity - Sharpe Ratio: {rp_sharpe:.4f}")
except Exception as e:
    print(f"Error calculating risk parity portfolio: {e}")

# 12. Mean-CVaR Portfolio for comparison (more focused on tail risk)
try:
    cvar_port = port.ef_minimum_risk(model=model, rm='CVaR', rf=rf, hist=hist, alpha=0.05)
    cvar_weights = port.weights

    # Calculate metrics for CVaR portfolio
    cvar_return = port.port_return(cvar_weights)
    cvar_risk = port.port_risk(cvar_weights, rm='CVaR', alpha=0.05)
    cvar_sharpe = port.sharpe_ratio(cvar_weights, rm='CVaR', rf=rf, alpha=0.05)

    print("\nMean-CVaR Portfolio (focuses on reducing tail risk):")
    for ticker, weight in cvar_weights.sort_values(ascending=False).items():
        print(f"{ticker}: {weight*100:.2f}%")

    print(f"\nMean-CVaR - Expected Annual Return: {cvar_return*252*100:.2f}%")
    print(f"Mean-CVaR - CVaR (5%): {cvar_risk*np.sqrt(252)*100:.2f}%")
    print(f"Mean-CVaR - Modified Sharpe Ratio: {cvar_sharpe:.4f}")
except Exception as e:
    print(f"Error calculating Mean-CVaR portfolio: {e}")

# 13. Calculate Metrics for all portfolios
try:
    metrics = pd.DataFrame(index=['Current', 'Optimal', 'Risk Parity', 'Mean-CVaR'],
                           columns=['Expected Annual Return (%)', 'Risk (%)', 'Sharpe Ratio'])

    metrics.loc['Current'] = [port.port_return(weights)*252*100,
                             port.port_risk(weights, rm=rm)*np.sqrt(252)*100,
                             port.sharpe_ratio(weights, rm=rm, rf=rf)]

    metrics.loc['Optimal'] = [port.port_return(optimal_weights)*252*100,
                             port.port_risk(optimal_weights, rm=rm)*np.sqrt(252)*100,
                             port.sharpe_ratio(optimal_weights, rm=rm, rf=rf)]

    metrics.loc['Risk Parity'] = [port.port_return(rp_weights)*252*100,
                                 port.port_risk(rp_weights, rm=rm)*np.sqrt(252)*100,
                                 port.sharpe_ratio(rp_weights, rm=rm, rf=rf)]

    metrics.loc['Mean-CVaR'] = [port.port_return(cvar_weights)*252*100,
                               port.port_risk(cvar_weights, rm='CVaR', alpha=0.05)*np.sqrt(252)*100,
                               port.sharpe_ratio(cvar_weights, rm='CVaR', rf=rf, alpha=0.05)]

    print("\nPortfolio Performance Comparison:")
    print(metrics.round(2))
except Exception as e:
    print(f"Error calculating portfolio metrics comparison: {e}")

print("\nPerforming stress testing...")
# 14. Portfolio Diagnostics - Stress testing
try:
    # Stress testing - simulate market downturns
    stress_scenarios = {
        'Market Crash (-30%)': -0.30,
        'Moderate Decline (-15%)': -0.15,
        'Minor Correction (-5%)': -0.05
    }

    # Create correlation coefficients with market (assuming VOO represents the market)
    market_corr = returns.corrwith(returns['VOO'])

    # Calculate expected portfolio performance in each scenario
    stress_results = pd.DataFrame(index=stress_scenarios.keys(), columns=['Expected Portfolio Return (%)'])

    for scenario, market_return in stress_scenarios.items():
        # Simple stress testing model: asset_return = beta * market_return
        # where beta is approximated by correlation with market
        scenario_returns = market_corr * market_return
        stress_results.loc[scenario, 'Expected Portfolio Return (%)'] = scenario_returns.dot(weights) * 100

    print("\nStress Test Results:")
    print(stress_results.round(2))
except Exception as e:
    print(f"Error performing stress testing: {e}")

# Display the recommended changes to optimize the portfolio
try:
    if 'optimal_weights' in locals() and len(optimal_weights) > 0:
        print("\nRecommended Portfolio Changes:")
        changes = optimal_weights - weights
        for ticker, change in changes.sort_values().items():
            action = "Increase" if change > 0 else "Decrease"
            print(f"{action} {ticker} by {abs(change)*100:.2f}%")
except Exception as e:
    print(f"Error calculating recommended changes: {e}")

print("\nAnalysis complete.")
