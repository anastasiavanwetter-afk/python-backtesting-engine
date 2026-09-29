from src.backtester import backtest

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def performance(data, deposit=100, risk_reward_ratio=2, starting_equity=10000, commission_per_share=0.005, slippage_bps=1, stop_distance=0.05):
    trades = backtest(data, deposit=deposit, risk_reward_ratio=risk_reward_ratio, starting_equity=starting_equity, commission_per_share=commission_per_share, slippage_bps=slippage_bps, stop_distance=stop_distance)
    '''trades.to_csv(f'trades_{stop_distance}.csv', index=False, encoding='utf-8')'''

    winrate = (trades["Net_PnL"] > 0).mean()
    avg_win = trades.loc[trades["Net_PnL"] > 0, "Net_PnL"].mean()
    avg_loss = trades.loc[trades["Net_PnL"] < 0, "Net_PnL"].mean()
    be_winrate = (-avg_loss) / (avg_win - avg_loss)
    
    gross_profit = trades.loc[trades["Net_PnL"] > 0, "Net_PnL"].sum()
    gross_loss = abs(trades.loc[trades["Net_PnL"] < 0, "Net_PnL"].sum())
    if gross_loss == 0:
        profit_factor = np.inf
    else:
        profit_factor = gross_profit / gross_loss

    EV = trades["Net_PnL"].mean()
    pnl = trades["Net_PnL"].sum()

    returns = trades["Return"]
    s = returns.std(ddof=1)
    sharpe = returns.mean()/s

    downside_returns = np.minimum(returns, 0)
    downside_deviation = np.sqrt(np.mean(downside_returns**2))
    sortino = returns.mean() / downside_deviation

    days = (data.index[-1] - data.index[0]).days
    R_total = trades["Equity"].iloc[-1] / starting_equity - 1
    R_anual = (1 + R_total)**(365/days)-1
    Max_DD_perc = abs(trades["DrawdownPct"].min())
    calmar = R_anual/Max_DD_perc

    exit_counts = trades["Reason exit"].value_counts()
    SL_pct = exit_counts.get("SL", 0) / len(trades)
    TP_pct = exit_counts.get("TP", 0) / len(trades)
    EOD_pct = exit_counts.get("EOD", 0) / len(trades)

    return {
        "Trades": len(trades),
        "Win rate": round(winrate, 2),
        "Avg win": round(avg_win, 2),
        "Avg loss": round(avg_loss, 2),
        "BE win rate": round(be_winrate, 2),
        "Profit factor": round(profit_factor, 2),
        "Total PnL": round(pnl, 2),
        "Expected value": round(EV, 2),
        "Sharpe": round(sharpe, 2),
        "Sortino": round(sortino, 2),
        "Calmar": round(calmar, 2),
        "SL %": round(SL_pct*100, 0),
        "TP %": round(TP_pct*100, 0),
        "EOD %": round(EOD_pct*100, 0)
    }

def sensitivity_analysis_1d(data, parameter, values):
    valid_parameters = {
        "risk_reward_ratio",
        "commission_per_share",
        "slippage_bps",
        "stop_distance"
    }

    if parameter not in valid_parameters:
        raise ValueError(
            f"Unknown parameter '{parameter}'. "
            f"Choose from: {valid_parameters}"
        )
        
    results = []

    for value in values:
        result = performance(data,**{parameter: value})
        result[parameter] = value
        results.append(result)

    results_df = pd.DataFrame(results)
    return results_df

def sensitivity_analysis_2d(data, parameter_1, values_1, parameter_2, values_2, metric):
    crosstable = pd.DataFrame(index=values_1, columns=values_2, dtype=float)

    for value_1 in values_1:
        for value_2 in values_2:
            result = performance(data,**{parameter_1: value_1}, **{parameter_2: value_2})
            crosstable.loc[value_1, value_2] = result[f"{metric}"]

    return crosstable

def heatmap(crosstable, parameter_1, parameter_2, metric):
    plt.figure(figsize=(6, 4))
    sns.heatmap(crosstable, annot=True, cmap="Blues")
    plt.title(f"{metric} for different combinations of {parameter_1} and {parameter_2}")
    plt.show()