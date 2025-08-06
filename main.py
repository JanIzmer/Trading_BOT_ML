import time
from config import CONFIGS
from core.data_loader import fetch_ohlcv
from core.indicators import add_indicators
from core.signaler import send_signal
from core.trader import handle_trade
from core.strategies.bull import generate_signal as bull_strategy
from core.strategies.bear import generate_signal as bear_strategy
from core.strategies.range import generate_signal as range_strategy
from core.market_type import MarketTrendDetector


def choose_strategy_and_config(df, base_config):
    """
    Detect the current market trend and select the corresponding strategy and config.

    Args:
        df (pd.DataFrame): DataFrame with price data and indicators.
        base_config (dict): Base configuration containing strategy configs for bull, bear, and sideways markets.

    Returns:
        tuple: (strategy_function, strategy_config) matching the detected market type.
    """
    market = MarketTrendDetector.detect_market_trend(df)

    if market == "bull":
        return bull_strategy, base_config['bull']
    elif market == "bear":
        return bear_strategy, base_config['bear']
    else:
        return range_strategy, base_config['sideways']


def run():
    """
    Main loop that:
    - Iterates over all configured symbols.
    - Fetches OHLCV data.
    - Adds technical indicators.
    - Selects the strategy based on market trend.
    - Generates trade signals.
    - Sends signals to users.
    - Executes trades.
    Then sleeps for the configured interval before repeating.
    """
    while True:
        for symbol, base_config in CONFIGS.items():
            try:
                df = fetch_ohlcv(base_config['symbol'], base_config['timeframe'], base_config['limit'])
                df = add_indicators(df)

                strategy, config = choose_strategy_and_config(df, base_config)
                market_type = MarketTrendDetector.detect_market_trend(df)
                signal = strategy(df)

                config_with_symbol = {**config, 'symbol': base_config['symbol'], 'leverage': base_config['leverage']}

                send_signal(base_config['symbol'], signal, df, market_type)
                handle_trade(config_with_symbol, signal, df)

            except Exception as e:
                print(f"⚠️ Error processing {symbol}: {e}")

        first_symbol = next(iter(CONFIGS))
        interval = CONFIGS[first_symbol]['interval_seconds']
        time.sleep(interval)


if __name__ == "__main__":
    run()
