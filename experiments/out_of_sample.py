from experiments.split_data import split_data
from src.backtester import backtest
from src.performance import key_statistics
from src.statistics import win_rate, expected_value, test_expected_value, Sharpe_ratio, Sortino_ratio, Calmar_ratio
from src.distribution import distribution_statistics

import pandas as pd

ticker = "SPY"
# Based on sensitivity analysis on IS data and frozen before evaluating OOS data
chosen_rr = 1.5

is_data, oos_data = split_data(ticker, 2026, 9, 1)
is_days = (is_data.index[-1] - is_data.index[0]).days
oos_days = (oos_data.index[-1] - oos_data.index[0]).days

is_trades = backtest(is_data, risk_reward_ratio=chosen_rr, starting_equity=10000)
oos_trades = backtest(oos_data, risk_reward_ratio=chosen_rr, starting_equity=10000)

is_stats = key_statistics(is_trades)
oos_stats = key_statistics(oos_trades)

is_winrate = win_rate(is_trades)
is_ev = expected_value(is_trades)
is_ev_reliability = test_expected_value(is_trades)
is_sharpe = Sharpe_ratio(is_trades)
is_sortino = Sortino_ratio(is_trades)
is_calmar = Calmar_ratio(is_trades, is_days)
is_distribution = distribution_statistics(is_trades)

oos_winrate = win_rate(oos_trades)
oos_ev = expected_value(oos_trades)
oos_ev_reliability = test_expected_value(oos_trades)
oos_sharpe = Sharpe_ratio(oos_trades)
oos_sortino = Sortino_ratio(oos_trades)
oos_calmar = Calmar_ratio(oos_trades, oos_days)
oos_distribution = distribution_statistics(oos_trades)

comparison = pd.DataFrame({
    "In-Sample": {
        "Trades": is_stats["Trades"],
        "Win rate": is_stats["Winrate"],
        "Profit factor": is_stats["ProfitFactor"],
        "Total PnL": is_stats["TotalPnL"],
        "Avg win": is_stats["AvgWin"],
        "Avg loss": is_stats["AvgLoss"],
        "Max drawdown": is_stats["MaxDrawdown"],
        "Return / DD": is_stats["Return/DD"],

        "Expected value": is_ev["ExpectedValue"],
        "Sharpe": is_sharpe,
        "Sortino": is_sortino,
        "Calmar": is_calmar,

        "Median PnL": is_distribution["Median"],
        "Best trade": is_distribution["Best"],
        "Worst trade": is_distribution["Worst"],
        "Skewness": is_distribution["Skewness"],
        "Kurtosis": is_distribution["Kurtosis"],
    },

    "Out-of-Sample": {
        "Trades": oos_stats["Trades"],
        "Win rate": oos_stats["Winrate"],
        "Profit factor": oos_stats["ProfitFactor"],
        "Total PnL": oos_stats["TotalPnL"],
        "Avg win": oos_stats["AvgWin"],
        "Avg loss": oos_stats["AvgLoss"],
        "Max drawdown": oos_stats["MaxDrawdown"],
        "Return / DD": oos_stats["Return/DD"],

        "Expected value": oos_ev["ExpectedValue"],
        "Sharpe": oos_sharpe,
        "Sortino": oos_sortino,
        "Calmar": oos_calmar,

        "Median PnL": oos_distribution["Median"],
        "Best trade": oos_distribution["Best"],
        "Worst trade": oos_distribution["Worst"],
        "Skewness": oos_distribution["Skewness"],
        "Kurtosis": oos_distribution["Kurtosis"],
    },

        "diff": {
        "Trades": oos_stats["Trades"] - is_stats["Trades"],
        "Win rate": oos_stats["Winrate"] - is_stats["Winrate"],
        "Profit factor": oos_stats["ProfitFactor"] - is_stats["ProfitFactor"],
        "Total PnL": oos_stats["TotalPnL"] - is_stats["TotalPnL"],
        "Avg win": oos_stats["AvgWin"] - is_stats["AvgWin"],
        "Avg loss": oos_stats["AvgLoss"] - is_stats["AvgLoss"],
        "Max drawdown": oos_stats["MaxDrawdown"] - is_stats["MaxDrawdown"],
        "Return / DD": oos_stats["Return/DD"] - is_stats["Return/DD"],
    
        "Expected value": oos_ev["ExpectedValue"] - is_ev["ExpectedValue"],
        "Sharpe": oos_sharpe - is_sharpe,
        "Sortino": oos_sortino - is_sortino,
        "Calmar": oos_calmar - is_calmar,
    
        "Median PnL": oos_distribution["Median"] - is_distribution["Median"],
        "Best trade": oos_distribution["Best"] - is_distribution["Best"],
        "Worst trade": oos_distribution["Worst"] - is_distribution["Worst"],
        "Skewness": oos_distribution["Skewness"] - is_distribution["Skewness"],
        "Kurtosis": oos_distribution["Kurtosis"] - is_distribution["Kurtosis"],
    }
})

print("\n========== IS vs OOS ==========")
print(comparison.round(2).to_string())