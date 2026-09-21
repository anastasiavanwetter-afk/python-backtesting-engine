# Standard library
from datetime import time

# Third-party libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Local imports


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
    plt.title("PnL per Trade")
    plt.xlabel("Trade Number")
    plt.ylabel("PnL ($)")
    
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
    plt.title("Exit Distribution")
    plt.xlabel("Exit Reason")
    plt.ylabel("Number of Trades")

    plt.grid()
    plt.show()

def plot_pnl_distribution(trades_df):
    pnl = trades_df["PnL"]

    plt.figure(figsize=(10, 6))
    plt.hist(pnl, bins=10, edgecolor="black")

    plt.axvline(pnl.mean(), linestyle='--', label=f"Mean={pnl.mean():.2f}")
    plt.axvline(pnl.median(), linestyle='--', label=f"Median={pnl.median():.2f}")

    plt.xlabel("PnL per trade")
    plt.ylabel("Frequency")
    plt.title("Distribution of trades PnL")
    plt.legend()
    plt.show()
    