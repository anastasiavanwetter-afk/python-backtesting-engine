# Standard library
from datetime import time

# Third-party libraries
import numpy as np
import pandas as pd

# Local imports
from ta.volatility import AverageTrueRange

def get_vwap(data):
    data = data.copy()

    data["TP"] = (data["High"] + data["Low"] + data["Close"]) / 3

    data["VWAP"] = (
        (data["TP"] * data["Volume"]).groupby(data["Date"]).cumsum()
        / data["Volume"].groupby(data["Date"]).cumsum()
    )

    return data

def get_ema(data, span=9):
    data = data.copy()

    data[f"EMA{span}"] = (
        data["Close"]
        .ewm(span=span, adjust=False)
        .mean()
    )

    return data

def get_atr(data, daily, window=14):
    data = data.copy()
    daily = daily.copy()

    atr = AverageTrueRange(
        high=daily["High"],
        low=daily["Low"],
        close=daily["Close"],
        window=window
    )

    daily["ATR"] = atr.average_true_range()

    atr_map = daily["ATR"]
    atr_map.index = daily.index.date

    data["ATR"] = data["Date"].map(atr_map)

    return data

def get_dayrange(data):
    data = data.copy()

    data["DayHighSoFar"] = data.groupby("Date")["High"].cummax()
    data["DayLowSoFar"] = data.groupby("Date")["Low"].cummin()

    data["Range"] = (
        data["DayHighSoFar"] -
        data["DayLowSoFar"]
    )

    return data