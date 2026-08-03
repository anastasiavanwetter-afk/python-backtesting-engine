# Standard library
from datetime import time

# Third-party libraries
import numpy as np
import pandas as pd

# Local imports

def key_statistics(trades_df):
    if trades_df.empty:
        return pd.Series()
    else:
        trades_df = trades_df.copy()
        results = {}
        
        wins = trades_df[trades_df["PnL"] > 0]
        losses = trades_df[trades_df["PnL"] <= 0]
        
        gross_profit = trades_df.loc[trades_df["PnL"] > 0, "PnL"].sum()
        gross_loss = abs(trades_df.loc[trades_df["PnL"] < 0, "PnL"].sum())
        if gross_loss == 0:
            profit_factor = np.inf
        else:
            profit_factor = gross_profit / gross_loss
        
        winrate = len(wins) / len(trades_df) * 100
    
        results = {
            "Trades": len(trades_df),
            "Winrate": round(winrate, 2),
            "ProfitFactor": round(profit_factor, 2),
            "TotalPnL": round(trades_df["PnL"].sum(), 2),
            "AvgWin": round(trades_df.loc[trades_df["PnL"] > 0, "PnL"].mean(), 2),
            "AvgLoss": round(trades_df.loc[trades_df["PnL"] <= 0, "PnL"].mean(), 2),
            "MaxDrawdown": round(trades_df["Drawdown"].min(), 2),
            "Return/DD": round(trades_df["PnL"].sum()/abs(trades_df["Drawdown"].min()), 2)
        }
    
        return pd.Series(results)
    