"""
Basic Distance Approach - Following Hudson & Thames Video
https://www.youtube.com/watch?v=sKgDeqI39b4

This script implements the Basic Distance Approach for pairs trading with 4 methods:
1. Basic Method (Euclidean SSD)
2. Industry Group Method
3. Zero Crossings Method
4. Variance Method

Author: Based on Hudson & Thames workshop
Date: 2025-02-27
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from arbitragelab.distance_approach import basic_distance_approach
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================

def load_data():
    """
    Download S&P 500 stock data for 4 major industries:
    - Information Technology
    - Industrials
    - Financials
    - Healthcare
    """
    print("="*70)
    print("STEP 1: Loading Data")
    print("="*70)

    # Get industry data from Wikipedia
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    stock_table = table[0]

    # Industry groups to use
    industry_group = ['Information Technology', 'Industrials', 'Financials', 'Health Care']

    # Get tickers from S&P 500 which are in those industry groups
    ticker_industry = stock_table[stock_table['GICS Sector'].isin(industry_group)].reset_index(drop=True)
    ticker_industry = ticker_industry[['Symbol', 'GICS Sector']]

    # Get tickers to use as a list
    tickers = ticker_industry['Symbol'].to_list()
    remove_tickers = ['CARR', 'ABC', 'BRK.B', 'VNT', 'OTIS']
    tickers = [ticker for ticker in tickers if ticker not in remove_tickers]

    # Get a dictionary of industry group
    industry_dict = pd.Series(ticker_industry['GICS Sector'].values,
                              index=ticker_industry['Symbol']).to_dict()

    print(f"Total tickers: {len(tickers)}")

    # Loading data - Formation: Jan 2018 to Dec 2018 (12 months)
    # Trading: Jan 2019 to July 2019 (6 months)
    print("\nDownloading training data (Jan 2018 - Dec 2018)...")
    train_data = yf.download(tickers, start="2018-01-03", end="2019-01-01", progress=False)
    train_data = train_data["Adj Close"]
    print(f"Training data shape: {train_data.shape}")

    print("\nDownloading test data (Jan 2019 - July 2019)...")
    test_data = yf.download(tickers, start="2019-01-02", end="2019-07-01", progress=False)
    test_data = test_data["Adj Close"]
    print(f"Test data shape: {test_data.shape}")

    return train_data, test_data, industry_dict


# ============================================================================
# STEP 2: PAIRS FORMATION
# ============================================================================

def form_pairs(train_data, industry_dict):
    """
    Form pairs using 4 different methods:
    1. Basic Method (smallest Euclidean SSD)
    2. Industry Method (same industry group)
    3. Zero Crossings Method (highest number of zero crossings)
    4. Variance Method (highest historical standard deviation)
    """
    print("\n" + "="*70)
    print("STEP 2: Pairs Formation - 4 Methods")
    print("="*70)

    strategies = {}

    # Method 1: Basic Distance Approach
    print("\n[1/4] Basic Distance Approach (Euclidean SSD)...")
    strategy_basic = basic_distance_approach.DistanceStrategy()
    strategy_basic.form_pairs(train_data, num_top=20)
    strategies['basic'] = strategy_basic
    pairs_basic = strategy_basic.get_pairs()
    print(f"Top 5 pairs: {pairs_basic[:5]}")

    # Method 2: Industry Group Method
    print("\n[2/4] Industry Group Method...")
    strategy_industry = basic_distance_approach.DistanceStrategy()
    strategy_industry.form_pairs(train_data, industry_dict=industry_dict, num_top=20)
    strategies['industry'] = strategy_industry
    pairs_industry = strategy_industry.get_pairs()
    print(f"Top 5 pairs: {pairs_industry[:5]}")

    # Method 3: Zero Crossings Method
    print("\n[3/4] Zero Crossings Method...")
    strategy_zero = basic_distance_approach.DistanceStrategy()
    strategy_zero.form_pairs(train_data, method='zero_crossing',
                            industry_dict=industry_dict, num_top=20)
    strategies['zero_crossing'] = strategy_zero
    pairs_zero = strategy_zero.get_pairs()
    num_crossings = strategy_zero.get_num_crossing()
    print(f"Top 5 pairs: {pairs_zero[:5]}")
    for pair in pairs_zero[:3]:
        print(f"  {pair}: {num_crossings.get(pair, 0)} crossings")

    # Method 4: Variance Method
    print("\n[4/4] Variance Method...")
    strategy_variance = basic_distance_approach.DistanceStrategy()
    strategy_variance.form_pairs(train_data, method='variance',
                                 industry_dict=industry_dict, num_top=20)
    strategies['variance'] = strategy_variance
    pairs_variance = strategy_variance.get_pairs()
    print(f"Top 5 pairs: {pairs_variance[:5]}")

    return strategies


# ============================================================================
# STEP 3: TRADING SIGNAL GENERATION
# ============================================================================

def generate_signals(strategies, test_data, divergence=2):
    """
    Generate trading signals for all strategies.

    Trading Rules:
    - If portfolio value > divergence * std → Sell signal (-1)
    - If portfolio value < -divergence * std → Buy signal (+1)
    - Close position when portfolio crosses zero
    """
    print("\n" + "="*70)
    print("STEP 3: Trading Signal Generation")
    print("="*70)
    print(f"Threshold: {divergence} standard deviations\n")

    for name, strategy in strategies.items():
        strategy.trade_pairs(test_data, divergence=divergence)
        signals = strategy.get_signals()
        print(f"{name.capitalize():15} method: {len(signals.columns)} pairs, "
              f"{signals.sum().sum():.0f} total signals")


# ============================================================================
# STEP 4: CALCULATE PORTFOLIO RETURNS
# ============================================================================

def calculate_portfolio_returns(strategy, test_data):
    """
    Calculate portfolio returns for a given strategy.
    Uses equal weighting (50% long, 50% short for each pair).
    """
    pairs = strategy.get_pairs()
    signals = strategy.get_signals()

    # Calculate daily returns
    test_data_returns = (test_data / test_data.shift(1) - 1)[1:]

    # Store individual pair returns and total portfolio return
    pair_returns = {}
    total_return = pd.Series(0.0, index=test_data_returns.index)

    for pair in pairs:
        first_stock, second_stock = pair

        # Equal weighted portfolio (50% each leg)
        pair_return = (test_data_returns[first_stock] * 0.5 -
                       test_data_returns[second_stock] * 0.5)

        # Apply trading signals (shift by 1 to avoid look-ahead)
        pair_return = pair_return * signals[str(pair)].shift(1)

        # Calculate cumulative returns
        pair_cumret = (pair_return + 1).cumprod()

        # Store final return for this pair
        pair_returns[pair] = pair_cumret.iloc[-1] - 1

        # Add to total portfolio
        total_return = total_return.add(pair_cumret, fill_value=0)

    # Equal weight across all pairs
    total_return = total_return / len(pairs)

    return pair_returns, total_return


def calculate_all_returns(strategies, test_data):
    """Calculate returns for all strategies."""
    print("\n" + "="*70)
    print("STEP 4: Calculate Portfolio Returns")
    print("="*70)

    portfolios = {}
    for name, strategy in strategies.items():
        pair_returns, portfolio = calculate_portfolio_returns(strategy, test_data)
        portfolios[name] = portfolio
        final_return = portfolio.iloc[-1] - 1
        print(f"{name.capitalize():15} method - Final Return: {final_return:.4f}")

    return portfolios


# ============================================================================
# STEP 5: PLOT RESULTS
# ============================================================================

def plot_results(portfolios):
    """Plot equity curves for all methods."""
    print("\n" + "="*70)
    print("STEP 5: Plotting Results")
    print("="*70)

    # Create output directory
    os.makedirs('distance_approach_results', exist_ok=True)

    # Plot all equity curves together
    plt.figure(figsize=(14, 8))

    labels = {
        'basic': 'Basic Method',
        'industry': 'Industry Method',
        'zero_crossing': 'Zero Crossings Method',
        'variance': 'Variance Method'
    }

    for name, portfolio in portfolios.items():
        (portfolio - 1).plot(label=labels[name], linewidth=2)

    plt.title('Basic Distance Approach - Equity Curves Comparison\n'
              'Form: Jan-Dec 2018 | Trade: Jan-Jul 2019',
              fontsize=14, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Portfolio Return', fontsize=12)
    plt.legend(loc='best', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
    plt.tight_layout()

    output_path = 'distance_approach_results/equity_curves_comparison.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nChart saved: {output_path}")
    plt.show()

    # Plot individual equity curves
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    axes = axes.flatten()

    for ax, (name, portfolio) in zip(axes, portfolios.items()):
        (portfolio - 1).plot(ax=ax, linewidth=2)
        final_return = portfolio.iloc[-1] - 1
        ax.set_title(f'{labels[name]}\nFinal Return: {final_return:.2%}',
                    fontsize=12, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Return')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='black', linestyle='--', linewidth=0.5)

    plt.suptitle('Basic Distance Approach - Individual Method Equity Curves',
                fontsize=14, fontweight='bold')
    plt.tight_layout()

    output_path = 'distance_approach_results/individual_equity_curves.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Chart saved: {output_path}")
    plt.show()


# ============================================================================
# STEP 6: SUMMARY STATISTICS
# ============================================================================

def calculate_statistics(portfolio):
    """Calculate statistics for a portfolio."""
    returns = portfolio.diff().dropna()
    cumret = portfolio.iloc[-1] - 1

    # Calculate max drawdown
    cum_returns = (portfolio - 1)
    rolling_max = cum_returns.expanding().max()
    drawdown = cum_returns - rolling_max
    max_dd = drawdown.min()

    # Sharpe ratio (annualized)
    daily_returns = returns
    sharpe = daily_returns.mean() / daily_returns.std() * np.sqrt(252) if daily_returns.std() > 0 else 0

    return {
        'Final Return': cumret,
        'Max Drawdown': max_dd,
        'Sharpe Ratio': sharpe,
        'Win Rate': (returns > 0).sum() / len(returns)
    }


def print_summary(portfolios):
    """Print summary statistics for all methods."""
    print("\n" + "="*70)
    print("STEP 6: Summary Statistics")
    print("="*70)

    labels = {
        'basic': 'Basic Method',
        'industry': 'Industry Method',
        'zero_crossing': 'Zero Crossings Method',
        'variance': 'Variance Method'
    }

    print(f"\n{'Method':<20} {'Final Return':<15} {'Max Drawdown':<15} {'Sharpe Ratio':<15} {'Win Rate':<10}")
    print("-" * 75)

    for name, portfolio in portfolios.items():
        stats = calculate_statistics(portfolio)
        print(f"{labels[name]:<20} {stats['Final Return']:>14.2%} "
              f"{stats['Max Drawdown']:>14.2%} {stats['Sharpe Ratio']:>14.2f} "
              f"{stats['Win Rate']:>9.1%}")

    print("="*70)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    print("\n" + "="*70)
    print("BASIC DISTANCE APPROACH - HUDSON & THAMES WORKSHOP")
    print("https://www.youtube.com/watch?v=sKgDeqI39b4")
    print("="*70)

    # Step 1: Load Data
    train_data, test_data, industry_dict = load_data()

    # Step 2: Form Pairs
    strategies = form_pairs(train_data, industry_dict)

    # Step 3: Generate Trading Signals
    generate_signals(strategies, test_data, divergence=2)

    # Step 4: Calculate Returns
    portfolios = calculate_all_returns(strategies, test_data)

    # Step 5: Plot Results
    plot_results(portfolios)

    # Step 6: Print Summary
    print_summary(portfolios)

    print("\n" + "="*70)
    print("EXECUTION COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
