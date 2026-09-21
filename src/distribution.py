# Standard library
from datetime import time

# Third-party libraries
import numpy as np
import pandas as pd
from scipy.stats import t
from scipy.stats import norm

# Local imports

def distribution_statistics(trades_df):
    if trades_df.empty:
        return pd.Series()

    pnl = trades_df["PnL"]

    return pd.Series({
        "Median": pnl.median(),
        "Best": pnl.max(),
        "Worst": pnl.min(),
        "Skewness": pnl.skew(),
        "Kurtosis": pnl.kurt()
    })