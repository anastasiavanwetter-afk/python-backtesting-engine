from src.data_loader import load_yfinance_data, load_daily_data
from src.indicators import get_vwap, get_ema, get_atr, get_dayrange
from src.strategy import crossover_strategy
from src.backtester import backtest

# Standard library
from datetime import time

# Third-party libraries
import numpy as np
import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

def run_experiment(data, ticker, risk_reward_ratio, days, starting_equity=10000):
    trades = backtest(data, risk_reward_ratio=risk_reward_ratio)

    wins = trades[trades["PnL"] > 0]
    losses = trades[trades["PnL"] <= 0]
    winrate = (trades["PnL"] > 0).mean()
    
    gross_profit = trades.loc[trades["PnL"] > 0, "PnL"].sum()
    gross_loss = abs(trades.loc[trades["PnL"] < 0, "PnL"].sum())
    if gross_loss == 0:
        profit_factor = np.inf
    else:
        profit_factor = gross_profit / gross_loss

    EV = trades["PnL"].mean()
    pnl = trades["PnL"].sum()

    returns = trades["Return"]
    s = returns.std(ddof=1)
    sharpe = returns.mean()/s

    downside_returns = np.minimum(returns, 0)
    downside_deviation = np.sqrt(np.mean(downside_returns**2))
    sortino = returns.mean() / downside_deviation

    R_total = trades["Equity"].iloc[-1] / starting_equity - 1
    R_anual = (1 + R_total)**(365/days)-1
    Max_DD_perc = abs(trades["DrawdownPct"].min())
    calmar = R_anual/Max_DD_perc

    exit_counts = trades["Reason exit"].value_counts()
    SL_pct = exit_counts.get("SL", 0) / len(trades)
    TP_pct = exit_counts.get("TP", 0) / len(trades)
    EOD_pct = exit_counts.get("EOD", 0) / len(trades)

    return {
        "Ticker": ticker,
        "RR": risk_reward_ratio,
        "Trades": len(trades),
        "Win rate": round(winrate, 2),
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

rr_values = [1, 1.5, 2, 2.5, 3]
tickers = ["NVDA", "AAPL", "MSFT", "SPY"]
results=[]

for ticker in tickers:
    data = load_yfinance_data(ticker)
    daily = load_daily_data(ticker)
    start_date = data.index[0]
    end_date = data.index[-1]
    days = (end_date - start_date).days

    data = get_vwap(data)
    data = get_ema(data)
    data = get_atr(data, daily)
    data = get_dayrange(data)

    data = crossover_strategy(data)

    for rr in rr_values:
        result = run_experiment(data, ticker, rr, days)
        results.append(result)

results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))