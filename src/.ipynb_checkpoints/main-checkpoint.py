from data_loader import load_yfinance_data, load_daily_data
from indicators import get_vwap, get_ema, get_atr, get_dayrange
from strategy import crossover_strategy
from backtester import backtest
from performance import key_statistics
from plots import (
    equity_curve,
    drawdown_curve,
    pnl_per_trade,
    distribution_exits,
    distribution_PnL,
)

ticker = "NVDA"

# Load data
data = load_yfinance_data(ticker)
daily = load_daily_data(ticker)

# Indicators
data = get_vwap(data)
data = get_ema(data)
data = get_atr(data, daily)
data = get_dayrange(data)

# Strategy
data = crossover_strategy(data)

# Backtest
trades = backtest(data)

# Statistics
stats = key_statistics(trades)
print(stats)

# Plots
equity_curve(trades)
drawdown_curve(trades)
pnl_per_trade(trades)
distribution_exits(trades)
distribution_PnL(trades)