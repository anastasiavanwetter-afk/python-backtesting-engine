# Standard library
from datetime import time

# Third-party libraries
import numpy as np
import pandas as pd

# Local imports
import matplotlib.pyplot as plt

def equity_curve(trades_df):
    plt.figure(figsize=(12,6))
    trades_df = trades_df.copy()

    plt.plot(trades_df["CumPnL"], label="Equity")
    plt.title("Equity Curve")
    plt.xlabel("Trade")
    plt.ylabel("Cumulative PnL")
    
    plt.legend()
    plt.grid()
    plt.show()

def drawdown_curve(trades_df):
    plt.figure(figsize=(12,6))
    trades_df = trades_df.copy()

    plt.plot(trades_df["Drawdown"], label="Drawdown")
    plt.title("Drawdown Curve")
    plt.xlabel("Trade")
    plt.ylabel("Maximum Drawdown")

    plt.legend()
    plt.grid()
    plt.show()

def pnl_per_trade(trades_df):
    plt.figure(figsize=(12,6))
    trades_df = trades_df.copy()

    plt.bar(
        trades_df.index,
        trades_df["PnL"]
    )
    plt.title("PnL per trade")
    plt.xlabel("Trade")
    plt.ylabel("PnL")
    
    plt.grid()
    plt.show()

def distribution_exits(trades_df):
    plt.figure(figsize=(12,6))
    trades_df = trades_df.copy()
    
    exit_counts = trades_df["Reason exit"].value_counts()
    plt.bar(
        exit_counts.index,
        exit_counts.values
    )
    plt.title("Distribution exit reasons")
    plt.xlabel("Exit reason")
    plt.ylabel("Count of exits")

    plt.grid()
    plt.show()

def distribution_PnL(trades_df):
    plt.figure(figsize=(12,6))
    trades_df = trades_df.copy()

    plt.hist(
        trades_df["PnL"],
        bins=20
    )
    plt.title("Distribution of PnL")
    plt.xlabel("PnL bins")
    plt.ylabel("PnL")
    
    plt.grid()
    plt.show()