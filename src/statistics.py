# Standard library
from datetime import time

# Third-party libraries
import numpy as np
import pandas as pd
from scipy.stats import t
from scipy.stats import norm

# Local imports

def win_rate(trades_df, confidence=0.95):
    if trades_df.empty:
        return pd.Series()

    n = len(trades_df)
    wins = (trades_df["PnL"] > 0).sum()
    p = wins/n
    SE_p = np.sqrt((p*(1-p))/n)

    alpha = 1- confidence
    z = norm.ppf(1-alpha/2)
    
    upper_CI = p + z*SE_p
    lower_CI = p - z*SE_p
    
    return pd.Series({
        "WinRate": p, 
        "StandardError": SE_p,
        "LowerCI": lower_CI,
        "UpperCI": upper_CI
    })

def expected_value(trades_df, confidence=0.95):
    if trades_df.empty:
        return pd.Series()

    n = len(trades_df)
    mean = trades_df["PnL"].mean()
    s = trades_df["PnL"].std(ddof=1)
    SE_mean = s/np.sqrt(n)

    alpha = 1- confidence
    df = n-1

    t_critical = t.ppf(1-alpha/2, df)
    
    upper_CI_mean = mean + t_critical*SE_mean
    lower_CI_mean = mean - t_critical*SE_mean

    return pd.Series({
        "ExpectedValue": mean,
        "StandardError": SE_mean,
        "LowerCI": lower_CI_mean,
        "UpperCI": upper_CI_mean
    })

def test_win_rate(trades_df, alpha=0.05):
    if trades_df.empty:
        return pd.Series()

    n = len(trades_df)
    wins = (trades_df["PnL"] > 0).sum()
    p = wins/n
    
    avgWin = trades_df.loc[trades_df["PnL"] > 0, "PnL"].mean()
    avgLoss = trades_df.loc[trades_df["PnL"] < 0, "PnL"].mean()
    
    p_0 = (-avgLoss)/(avgWin - avgLoss)
    SE_0 = np.sqrt((p_0*(1-p_0))/n)

    z_0 = (p - p_0)/SE_0

    #one sided test
    p_value = norm.sf(z_0)
    reject_null = p_value < alpha

    return pd.Series({
        "Observed_winrate": p,
        "Null_hypothesis_winrate": p_0,
        "StandardError": SE_0,
        "z_score": z_0,
        "p_value": p_value,
        "alpha": alpha,
        "Reject_null": reject_null
    })

def test_expected_value(trades_df, null=0, alpha=0.05):
    if trades_df.empty:
        return pd.Series()
    
    n = len(trades_df)
    
    EV = trades_df["PnL"].mean()
    s = trades_df["PnL"].std(ddof=1)
    SE_EV_0 = s/np.sqrt(n)

    t_stat = (EV - null)/SE_EV_0

    #one sided test
    p_value = t.sf(t_stat, df=n-1)
    reject_null = p_value < alpha

    return pd.Series({
        "Observed_EV": EV,
        "Null_hypothesis_EV": null,
        "StandardError": SE_EV_0,
        "t_score": t_stat,
        "p_value": p_value,
        "alpha": alpha,
        "Reject_null": reject_null
            
    })

def Sharpe_ratio(trades_df):
    if trades_df.empty:
        return pd.Series()

    returns = trades_df["Return"]
    s = returns.std(ddof=1)
    sharpe = returns.mean()/s

    return (sharpe)

def Sortino_ratio(trades_df):
    if trades_df.empty:
        return pd.Series()
        
    returns = trades_df["Return"]
    downside_returns = np.minimum(returns, 0)
    downside_deviation = np.sqrt(np.mean(downside_returns**2))
    
    sortino = returns.mean() / downside_deviation

    return (sortino)

def Calmar_ratio(trades_df, days, starting_equity=10000):
    if trades_df.empty:
        return pd.Series()

    R_total = trades_df["Equity"].iloc[-1] / starting_equity - 1
    R_anual = (1 + R_total)**(365/days)-1
    Max_DD_perc = abs(trades_df["DrawdownPct"].min())

    calmar = R_anual/Max_DD_perc

    return calmar