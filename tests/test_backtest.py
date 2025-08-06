import sys
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for saving plots
import matplotlib.pyplot as plt

# Add parent directory to sys.path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.strategytest import run_backtest
from core.market_type import MarketTrendDetector


def generate_report(df60, trades, balance_curve):
    """
    Generates performance metrics and saves a visual report based on backtest results.

    Parameters:
        df60 (pd.DataFrame): Original 60-minute OHLCV candles with timestamp.
        trades (list): List of executed trades returned by the backtest.
        balance_curve (list): List of balance values over time.

    Output:
        Saves a chart with price, trades, and trend regions to 'static/reports/btc_close_price.png'
        Prints performance metrics to stdout.
    """
    df_trades = pd.DataFrame(trades)

    if trades != []:
        # Basic performance statistics
        df_trades['profit_abs'] = (df_trades['profit_pct'] / 100) + 1
        total_profit_pct = (df_trades['profit_abs'].prod() - 1) * 100
        win_rate = (df_trades['profit_pct'] > 0).mean() * 100
        avg_profit = df_trades['profit_pct'].mean()

        # Profit summary per trend
        breakdown = df_trades.groupby("trend")['profit_pct'].agg(['count', 'mean', 'sum'])
        breakdown_reason = df_trades.groupby(['trend', 'exit_reason']).size().unstack(fill_value=0)

        # Drawdown calculation
        equity = pd.Series(balance_curve)
        peak = equity.cummax()
        drawdown = (equity - peak) / peak
        max_drawdown = drawdown.min() * 100

        # Print performance results
        print("\n📈 === OVERALL METRICS ===")
        print(f"Trades executed: {len(df_trades)}")
        print(f"Win rate: {win_rate:.2f}%")
        print(f"Average profit per trade: {avg_profit:.2f}%")
        print(f"Total profit: {total_profit_pct:.2f}%")
        print(f"Max drawdown: {max_drawdown:.2f}%")

        print("\n📊 === BY MARKET TYPE ===")
        print(breakdown)
        print("\n")
        print(breakdown_reason)

        # Convert timestamp to datetime (and drop timezone)
        df60['timestamp'] = pd.to_datetime(df60['timestamp']).dt.tz_localize(None)

        # Detect trend for each candle
        trends = []
        window = 200
        trend_detector = MarketTrendDetector()
        for i in range(len(df60)):
            if i < window - 1:
                trends.append(None)
            else:
                df_sub = df60.iloc[i - window + 1 : i + 1]
                trend = trend_detector.detect_market_trend(df=df_sub)
                trends.append(trend)
        df60['trend'] = trends

        # Color map for trend background
        colors = {
            'bull': 'green',
            'bear': 'red',
            'sideways': 'gray',
            None: 'white'
        }

        # Plot close price with background colored by trend
        plt.figure(figsize=(14, 6))
        plt.plot(df60['timestamp'], df60['close'], label='BTC/USDT Close Price', color='blue')
        plt.xlabel('Time')
        plt.ylabel('Price (USDT)')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        for trend_type in df60['trend'].unique():
            mask = df60['trend'] == trend_type
            plt.fill_between(df60['timestamp'],
                             df60['close'].min(), df60['close'].max(),
                             where=mask,
                             color=colors[trend_type], alpha=0.2, label=trend_type)

        # Mark trade entries and exits on the plot
        for trade in trades:
            trade_time = pd.to_datetime(trade['entry_time'])
            exit_time = pd.to_datetime(trade['exit_time'])
            entry_price = trade['entry_price']
            exit_price = trade['exit_price']

            if trade['position'] == 'short':
                plt.scatter(trade_time, entry_price, color='red', s=25, zorder=5)
                plt.scatter(exit_time, exit_price, color='yellow', s=25)
            elif trade['position'] == 'long':
                plt.scatter(trade_time, entry_price, color='green', s=25, zorder=5)
                plt.scatter(exit_time, exit_price, color='yellow', s=25)

        # Save the final report image
        plt.savefig('static/reports/btc_close_price.png')
        plt.close()

    else:
        print('Trades is empty')


def test_backtest_runs(rows=3500):
    """
    Loads historical data, runs backtest, generates report, and performs basic assertions.

    Parameters:
        rows (int): Number of rows (candles) to read from the CSV file.

    Output:
        Prints summary and saves report image.
        Raises AssertionError if output is not as expected.
    """
    df = pd.read_csv("static/data/BTCUSDT_60m.csv", nrows=rows)
    df.columns = df.columns.str.lower()

    final_balance, curve, trades = run_backtest(df)

    print(f"\nFinal balance: {final_balance:.2f} USDT")
    print(f"Total trades: {len(trades)}")

    generate_report(df, trades, curve)

    # Basic sanity checks
    assert isinstance(final_balance, (int, float))
    assert isinstance(curve, list)
    assert isinstance(trades, list)
    assert final_balance > 0
    assert len(curve) > 0
    assert all('entry_price' in t and 'exit_price' in t and 'profit_pct' in t for t in trades)



