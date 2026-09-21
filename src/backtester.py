# Standard library
from datetime import time

# Third-party libraries
import numpy as np
import pandas as pd

# Local imports


def backtest(data, deposit=100, risk_reward_ratio=2, starting_equity=10000):
    data = data.copy()
    position = None
    trades = []

    for i in range(len(data)):
        row = data.iloc[i]
        if position is None:
            if row["LongSignal"]:
                if i+1 < len(data):
                    entry = round(data.iloc[i+1]["Open"], 2)
                    entry_time = row.name
                    stoploss = round(row["stoploss"], 2)
                    risk = round(max(entry-stoploss, 0.05*row["ATR"]), 2)
                    takeProfit = round(entry + (risk_reward_ratio*risk), 2)
                    shares = round(deposit/risk, 0)
                    if takeProfit <= entry + 1.2*row["ATR"]:
                        position = {"side": "Long", "entry": entry, "entry_time": entry_time, "risk": risk, "stoploss": stoploss, "takeProfit": takeProfit, "shares": shares}
                        
    
            elif row["ShortSignal"]:
                if i+1 < len(data):
                    entry = round(data.iloc[i+1]["Open"], 2)
                    entry_time = row.name
                    stoploss = round(row["stoploss"], 2)
                    risk = round(max(stoploss-entry, 0.05*row["ATR"]), 2)
                    takeProfit = round(entry - (risk_reward_ratio*risk), 2)
                    shares = round(deposit/risk, 0)
                    if takeProfit >= entry - 1.2*row["ATR"]:
                        position = {"side": "Short", "entry": entry, "entry_time": entry_time, "risk": risk, "stoploss": stoploss, "takeProfit": takeProfit, "shares": shares}
                        
        else:
            entry = position["entry"]
            side = position["side"]
            entry_time = position["entry_time"]
            risk = position["risk"]
            stoploss = position["stoploss"]
            takeProfit = position["takeProfit"]
            shares = position["shares"]
            
            if side == "Long":
                if row["High"] >= takeProfit:
                    trades.append({"Entry Time": entry_time,
                                   "Entry": entry,
                                   "Type": side,
                                   "Risk": risk,
                                   "Stoploss": stoploss,
                                   "Takeprofit": takeProfit,
                                   "Size": shares,
                                   "Exit Time": row.name,
                                   "Exit": takeProfit,
                                   "PnL": (takeProfit - entry)*shares,
                                   "Reason exit": "TP"})
                    position = None
    
                elif row["Low"] <= stoploss:
                    trades.append({"Entry Time": entry_time,
                                   "Entry": entry,
                                   "Type": side,
                                   "Risk": risk,
                                   "Stoploss": stoploss,
                                   "Takeprofit": takeProfit,
                                   "Size": shares,
                                   "Exit Time": row.name,
                                   "Exit": stoploss,
                                   "PnL": (stoploss - entry)*shares,
                                   "Reason exit": "SL"})
                    position = None
    
                elif row["Time"] >= time(15,55):
                    pnl = row["Close"] - entry
                    trades.append({"Entry Time": entry_time,
                                   "Entry": entry,
                                   "Type": side,
                                   "Risk": risk,
                                   "Stoploss": stoploss,
                                   "Takeprofit": takeProfit,
                                   "Size": shares,
                                   "Exit Time": row.name,
                                   "Exit": row["Close"],
                                   "PnL": pnl*shares,
                                   "Reason exit": "EOD"})
                    position = None
    
            elif side == "Short" :
                if row["Low"] <= takeProfit:
                    trades.append({"Entry Time": entry_time,
                                   "Entry": entry,
                                   "Type": side,
                                   "Risk": risk,
                                   "Stoploss": stoploss,
                                   "Takeprofit": takeProfit,
                                   "Size": shares,
                                   "Exit Time": row.name,
                                   "Exit": takeProfit,
                                   "PnL": (entry - takeProfit)*shares,
                                   "Reason exit": "TP"})
                    position = None
    
                elif row["High"] >= stoploss:
                    trades.append({"Entry Time": entry_time,
                                   "Entry": entry,
                                   "Type": side,
                                   "Risk": risk,
                                   "Stoploss": stoploss,
                                   "Takeprofit": takeProfit,
                                   "Size": shares,
                                   "Exit Time": row.name,
                                   "Exit": stoploss,
                                   "PnL": (entry - stoploss)*shares,
                                   "Reason exit": "SL"})
                    position = None
    
                elif row["Time"] >= time(15,55):
                    pnl = entry - row["Close"]
                    trades.append({"Entry Time": entry_time,
                                   "Entry": entry,
                                   "Type": side,
                                   "Risk": risk,
                                   "Stoploss": stoploss,
                                   "Takeprofit": takeProfit,
                                   "Size": shares,
                                   "Exit Time": row.name,
                                   "Exit": row["Close"],
                                   "PnL": pnl*shares,
                                   "Reason exit": "EOD"})
                    position = None
    
    trades_df = pd.DataFrame(trades)
    
    #calculation maximum drawdown
    trades_df["CumPnL"] = trades_df["PnL"].cumsum()
    trades_df["Equity"] = starting_equity + trades_df["PnL"].cumsum()
    trades_df["Peak"] = trades_df["Equity"].cummax()
    trades_df["Drawdown"] = trades_df["Equity"] - trades_df["Peak"]
    trades_df["DrawdownPct"] = (trades_df["Equity"] - trades_df["Peak"]) / trades_df["Peak"]
    trades_df["Return"] = (trades_df["Equity"] / trades_df["Equity"].shift(1).fillna(starting_equity)) - 1
    
    return trades_df