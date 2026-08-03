# Standard library
from datetime import time

# Third-party libraries
import numpy as np
import pandas as pd

# Local imports

def crossover_strategy(data, fast_indicator="EMA9", slow_indicator="VWAP", start=time(9, 40), end=time(10, 30)):
    data = data.copy()

    #Timespan in which crosses can occur. Opening range strategy: keep timespan short and eaarly to market-open to make sure enough momentum is generated in the crosses. Other indicators might help indicate momentum.
    data["InSession"] = (
        (data["Time"] >= start) &
        (data["Time"] <= end)
    )
    
    data["LongSignal"] = (
        data["InSession"] &
        (data[fast_indicator] > data[slow_indicator]) & 
        (data[fast_indicator].shift(1) <= data[slow_indicator].shift(1))
    )
    
    data["ShortSignal"] = (
        data["InSession"] &
        (data[fast_indicator] < data[slow_indicator]) & 
        (data[fast_indicator].shift(1) >= data[slow_indicator].shift(1))
    )

    data["stoploss"] = np.nan
    data.loc[data["LongSignal"], "stoploss"] = (
        data.loc[data["LongSignal"], [fast_indicator, slow_indicator]]
            .min(axis=1)
    )
    data.loc[data["ShortSignal"], "stoploss"] = (
        data.loc[data["ShortSignal"], [fast_indicator, slow_indicator]]
            .max(axis=1)
    )

    return data