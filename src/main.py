from data_loader import load_yfinance_data, load_daily_data
from indicators import get_vwap, get_ema, get_atr, get_dayrange
from strategy import crossover_strategy
from backtester import backtest
from performance import key_statistics
from statistics import win_rate, expected_value, test_expected_value, Sharpe_ratio, Sortino_ratio, Calmar_ratio
from distribution import distribution_statistics
from plots import equity_curve, drawdown_curve, pnl_per_trade, distribution_exits, plot_pnl_distribution

ticker = "AAPL"

# Load data
data = load_yfinance_data(ticker)
daily = load_daily_data(ticker)

start_date = data.index[0]
end_date = data.index[-1]
days = (end_date - start_date).days

# Indicators
data = get_vwap(data)
data = get_ema(data)
data = get_atr(data, daily)
data = get_dayrange(data)

# Strategy
data = crossover_strategy(data)

# Backtest
trades = backtest(data, risk_reward_ratio=2)

# Statistics
performance_metrics = key_statistics(trades)
winrate = win_rate(trades)
ev = expected_value(trades)
ev_reliability = test_expected_value(trades)
sharpe = Sharpe_ratio(trades)
sortino = Sortino_ratio(trades)
calmar = Calmar_ratio(trades, days)
distribution = distribution_statistics(trades)

print("\n========== BACKTEST RESULTS ==========")

print("\nPERFORMANCE")
print(f"Ticker:              {ticker}")
print(f"Trades:              {performance_metrics['Trades']:.0f}")
print(f"Win rate:            {performance_metrics['Winrate']:.2f}%")
print(f"Profit factor:       {performance_metrics['ProfitFactor']:.2f}")
print(f"Total PnL:           {performance_metrics['TotalPnL']:.2f}")
print(f"Average win:         {performance_metrics['AvgWin']:.2f}")
print(f"Average loss:        {performance_metrics['AvgLoss']:.2f}")
print(f"Max drawdown:        {performance_metrics['MaxDrawdown']:.2f}")
print(f"Return / Drawdown:   {performance_metrics['Return/DD']:.2f}")
print(f"Sharpe Ratio:        {sharpe:.2f}")
print(f"Sortino Ratio:       {sortino:.2f}")
print(f"Calmar Ratio:        {calmar:.2f}")
print(performance_metrics["Exits"])
print(performance_metrics["Percentage exits"])

print("\nCONFIDENCE INTERVALS")
print(f"Observed win rate:   {winrate['WinRate']:.2%}")
print(f"Standard error:      {winrate['StandardError']:.4f}")
print(f"95% CI:              {winrate['LowerCI']:.2%}, {winrate['UpperCI']:.2%}")
print(f"Observed EV:         {ev['ExpectedValue']:.2f}")
print(f"Standard error:      {ev['StandardError']:.4f}")
print(f"95% CI:              {ev['LowerCI']:.2f}, {ev['UpperCI']:.2f}")

print("\nEXPECTED VALUE TEST")
print(f"Observed EV:         {ev_reliability['Observed_EV']:.2f}")
print(f"Null hypothesis EV:  {ev_reliability['Null_hypothesis_EV']:.2f}")
print(f"Standard error:      {ev_reliability['StandardError']:.4f}")
print(f"t-score:             {ev_reliability['t_score']:.3f}")
print(f"p-value:             {ev_reliability['p_value']:.4f}")
print(f"Alpha:               {ev_reliability['alpha']:.2f}")

if ev_reliability["Reject_null"]:
    print("Conclusion:          Reject H0")
else:
    print("Conclusion:          Fail to reject H0")

print("\nDISTRIBUTION")
print(f"Median:              {distribution['Median']:.2f}")
print(f"Best trade:          {distribution['Best']:.2f}")
print(f"Worst trade:         {distribution['Worst']:.2f}")
print(f"Skewness:            {distribution['Skewness']:.2f}")
print(f"Kurtosis:            {distribution['Kurtosis']:.2f}")

# Plots
equity_curve(trades)
drawdown_curve(trades)
pnl_per_trade(trades)
distribution_exits(trades)
plot_pnl_distribution(trades)