# Standard library
from datetime import time

# Third-party libraries
import numpy as np
import pandas as pd

# Local imports


def backtest(data, deposit=100, risk_reward_ratio=2.5, starting_equity=10000, commission_per_share=0.005, slippage_bps=1, stop_distance=0.05):
    data = data.copy()
    position = None
    trades = []

    for i in range(len(data)):
        row = data.iloc[i]
        if position is None:
            if row["LongSignal"]:
                if i+1 < len(data):
                    theoretical_entry = round(data.iloc[i+1]["Open"], 2)
                    entry_time = row.name
                    original_stoploss = row["stoploss"]
                    risk = round(max(theoretical_entry-original_stoploss, stop_distance*row["ATR"]), 2)
                    shares = round(deposit/risk, 0)
                    actual_entry = theoretical_entry + slippage_bps/10000*theoretical_entry
                    stoploss = round(actual_entry-risk, 2)
                    takeProfit = round(actual_entry + (risk_reward_ratio*risk), 2)
                    if takeProfit <= actual_entry + 1.2*row["ATR"]:
                        position = {"side": "Long", "entry": actual_entry, "entry_time": entry_time, "risk": risk, "stoploss": stoploss, "takeProfit": takeProfit, "shares": shares}
                        
    
            elif row["ShortSignal"]:
                if i+1 < len(data):
                    theoretical_entry = round(data.iloc[i+1]["Open"], 2)
                    entry_time = row.name
                    original_stoploss = row["stoploss"]
                    risk = round(max(original_stoploss-theoretical_entry, stop_distance*row["ATR"]), 2)
                    shares = round(deposit/risk, 0)
                    actual_entry = theoretical_entry - slippage_bps/10000*theoretical_entry
                    stoploss = round(actual_entry+risk, 2)
                    takeProfit = round(actual_entry - (risk_reward_ratio*risk), 2)
                    if takeProfit >= actual_entry - 1.2*row["ATR"]:
                        position = {"side": "Short", "entry": actual_entry, "entry_time": entry_time, "risk": risk, "stoploss": stoploss, "takeProfit": takeProfit, "shares": shares}
                        
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
                                   "Exit": takeProfit-slippage_bps/10000*takeProfit,
                                   "Gross_PnL": (takeProfit - entry)*shares,
                                   "Commission + slippage": (slippage_bps/10000*takeProfit + 2*commission_per_share)*shares,
                                   "Net_PnL": (takeProfit-slippage_bps/10000*takeProfit - entry - 2*commission_per_share)*shares,
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
                                   "Exit": stoploss-slippage_bps/10000*stoploss,
                                   "Gross_PnL": (stoploss - entry)*shares,
                                   "Commission + slippage": (slippage_bps/10000*stoploss + 2*commission_per_share)*shares,
                                   "Net_PnL": (stoploss-slippage_bps/10000*stoploss - entry - 2*commission_per_share)*shares,
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
                                   "Exit": row["Close"]-slippage_bps/10000*row['Close'],
                                   "Gross_PnL": pnl*shares,
                                   "Commission + slippage": (slippage_bps/10000*row['Close'] + 2*commission_per_share)*shares,
                                   "Net_PnL": (pnl-slippage_bps/10000*row['Close'] - 2*commission_per_share)*shares,
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
                                   "Exit": takeProfit+slippage_bps/10000*takeProfit,
                                   "Gross_PnL": (entry-takeProfit)*shares,
                                   "Commission + slippage": (slippage_bps/10000*takeProfit + 2*commission_per_share)*shares,
                                   "Net_PnL": (entry - (takeProfit+slippage_bps/10000*takeProfit) - 2*commission_per_share)*shares,
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
                                   "Exit": stoploss+slippage_bps/10000*stoploss,
                                   "Gross_PnL": (entry-stoploss)*shares,
                                   "Commission + slippage": (slippage_bps/10000*stoploss + 2*commission_per_share)*shares,
                                   "Net_PnL": (entry - (stoploss+slippage_bps/10000*stoploss)- 2*commission_per_share)*shares,
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
                                   "Exit": row["Close"]+slippage_bps/10000*row['Close'],
                                   "Gross_PnL": pnl*shares,
                                   "Commission + slippage": (slippage_bps/10000*row['Close'] + 2*commission_per_share)*shares,
                                   "Net_PnL": (pnl+slippage_bps/10000*row['Close'] - 2*commission_per_share)*shares,
                                   "Reason exit": "EOD"})
                    position = None
    
    trades_df = pd.DataFrame(trades)
    
    #calculation maximum drawdown
    trades_df["CumPnL"] = trades_df["Net_PnL"].cumsum()
    trades_df["Equity"] = starting_equity + trades_df["Net_PnL"].cumsum()
    trades_df["Peak"] = trades_df["Equity"].cummax()
    trades_df["Drawdown"] = trades_df["Equity"] - trades_df["Peak"]
    trades_df["DrawdownPct"] = (trades_df["Equity"] - trades_df["Peak"]) / trades_df["Peak"]
    trades_df["Return"] = (trades_df["Equity"] / trades_df["Equity"].shift(1).fillna(starting_equity)) - 1
    
    return trades_df