# portfolio_analysis.py
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import riskfolio as rp
import yfinance as yf


def analyze_portfolio():
    # Use known portfolio weights from your previous output
    weights = {
        "VOO": 0.32696837455677735,
        "META": 0.314076211155608,
        "ARM": 0.20552028240241438,
        "TSM": 0.1597482981738112,
        "TCEHY": 0.11185533870633428,
        "MSFT": 0.0632978373213317,
        "INTC": 0.012749429447051862,
        "AAPL": -0.0009053423293624654,
        "NVDA": -0.19331042943396642
    }

    print("Using predefined portfolio weights:")
    for ticker, weight in weights.items():
        print(f"{ticker}: {weight*100:.2f}%")

    # Convert to Series for easier manipulation
    weights_series = pd.Series(weights)

    # Define time period for analysis
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*3)  # 3 years of data

    # Get historical data
    tickers = list(weights.keys())

    print("\nDownloading historical price data...")
    data = yf.download(tickers, start=start_date, end=end_date)

    if 'Close' in data.columns.levels[0]:
        price_data = data['Close']
        print("Using 'Close' prices")
    else:
        print("Using available price data")
        price_data = data

    # Calculate returns
    returns = price_data.pct_change().dropna()

    print(f"Successfully downloaded data for {len(tickers)} tickers")
    print(f"Time period: {returns.index[0]} to {returns.index[-1]}")
    print(f"Number of data points: {len(returns)}")

    # Create portfolio object
    print("\nCreating portfolio object...")
    port = rp.Portfolio(returns=returns)

    # Calculate asset statistics
    port.assets_stats(method_mu='hist', method_cov='hist')

    # Risk free rate
    risk_free_rate = 0.02  # 2%

    # Calculate metrics using manual calculations to avoid API issues
    cov_matrix = returns.cov()
    mean_returns = returns.mean()

    # Manual risk calculation - square root of weighted variance
    risk = np.sqrt(weights_series.dot(cov_matrix).dot(weights_series))

    # Manual return calculation - weighted average of returns
    ret = weights_series.dot(mean_returns)

    # Manual Sharpe ratio
    sharpe = (ret - risk_free_rate) / risk if risk > 0 else np.nan

    print(f"\nCurrent Portfolio - Expected Annual Return: {ret*252*100:.2f}%")
    print(f"Current Portfolio - Annual Volatility: {risk*np.sqrt(252)*100:.2f}%")
    print(f"Current Portfolio - Sharpe Ratio: {sharpe:.4f}")

    # Manual risk contribution calculation
    marginal_contrib = cov_matrix.dot(weights_series) / risk if risk > 0 else np.zeros_like(weights_series)
    risk_contrib = pd.Series(weights_series * marginal_contrib, index=weights_series.index)
    risk_contrib = risk_contrib / risk_contrib.sum() if risk_contrib.sum() != 0 else risk_contrib

    print("\nRisk Contribution Analysis:")
    for ticker, contrib in risk_contrib.sort_values(ascending=False).items():
        print(f"{ticker}: {contrib*100:.2f}% of total risk")

    # Portfolio concentration analysis
    concentration_score = (weights_series ** 2).sum()  # Herfindahl-Hirschman Index
    normalized_score = (concentration_score - 1/len(weights_series)) / (1 - 1/len(weights_series))

    print(f"\nPortfolio Concentration Score: {concentration_score:.4f}")
    print(f"Normalized Concentration (0-1 scale): {normalized_score:.4f}")

    if normalized_score > 0.7:
        print("Your portfolio is HIGHLY concentrated. Consider diversifying across more assets.")
    elif normalized_score > 0.4:
        print("Your portfolio has MODERATE concentration. Some additional diversification could be beneficial.")
    else:
        print("Your portfolio is relatively well-diversified in terms of allocation.")

    # Sector analysis
    sector_mapping = {
        'VOO': 'Broad Market ETF',
        'META': 'Technology',
        'ARM': 'Technology',
        'TSM': 'Technology',
        'TCEHY': 'Technology',
        'MSFT': 'Technology',
        'INTC': 'Technology',
        'AAPL': 'Technology',
        'NVDA': 'Technology'
    }

    sector_exposure = {}
    for ticker, weight in weights.items():
        sector = sector_mapping.get(ticker, 'Other')
        sector_exposure[sector] = sector_exposure.get(sector, 0) + weight

    print("\nSector Exposure Analysis:")
    for sector, exposure in sorted(sector_exposure.items(), key=lambda x: abs(x[1]), reverse=True):
        print(f"{sector}: {exposure*100:.2f}%")

    # Portfolio recommendations
    print("\nPortfolio Recommendations:")

    # Check for excessive concentration
    high_weights = {k: v for k, v in weights.items() if v > 0.2}
    if high_weights:
        print("1. Consider reducing these high-concentration positions:")
        for ticker, weight in high_weights.items():
            print(f"   - {ticker}: {weight*100:.2f}% (aim for under 20% per position)")

    # Check for sector concentration
    if sector_exposure.get('Technology', 0) > 0.5:
        print("\n2. Your portfolio is heavily concentrated in technology stocks.")
        print("   Consider adding exposure to other sectors like:")
        print("   - Healthcare (e.g., XLV, JNJ, PFE)")
        print("   - Consumer Staples (e.g., XLP, PG, KO)")
        print("   - Utilities (e.g., XLU, NEE, DUK)")
        print("   - Financial Services (e.g., XLF, JPM, BAC)")

    # Check for short positions
    short_positions = {k: v for k, v in weights.items() if v < 0}
    if short_positions:
        print("\n3. You have short positions that increase your portfolio risk:")
        for ticker, weight in short_positions.items():
            print(f"   - {ticker}: {weight*100:.2f}%")
        print("   Short positions have unlimited potential loss and can increase portfolio volatility.")

    # Recommendation for diversification
    print("\n4. Consider adding these assets for better diversification:")
    print("   - Bond ETFs (e.g., BND, AGG, VGLT) to reduce overall portfolio volatility")
    print("   - International market ETFs (e.g., VXUS, EFA, VWO) for geographic diversification")
    print("   - Alternative assets (e.g., GLD, VNQ) that may have lower correlation with stocks")

    print("\nAnalysis complete.")

if __name__ == "__main__":
    analyze_portfolio()
