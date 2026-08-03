# Standard library
from datetime import time

# Third-party libraries
import numpy as np
import pandas as pd

# Local imports
import yfinance as yf
from massive import RESTClient
from datetime import time

def load_yfinance_data(ticker, period="60d", interval="2m"):

    data = yf.download(
        ticker,
        period=period,
        interval=interval,
        auto_adjust=True
    )

    data.columns = data.columns.droplevel(1)
    data["Time"] = data.index.time
    data["Date"] = data.index.date

    return data

def load_daily_data(ticker, period="90d"):

    daily = yf.download(
        ticker,
        period=period,
        interval="1d",
        auto_adjust=True
    )

    daily.columns = daily.columns.droplevel(1)
    daily["Time"] = daily.index.time
    daily["Date"] = daily.index.date

    return daily

def load_massive_data(ticker, start, end, multiplier=2, timespan="minute"):
    client = RESTClient("MASSIVE_API_KEY")

    all_rows = []

    for agg in client.list_aggs(
        ticker=ticker,
        multiplier=multiplier,
        timespan=timespan,
        from_=start,
        to=end,
        limit=50000
    ):
       all_rows.append({
        "Ticker": ticker,
        "Date": pd.to_datetime(agg.timestamp, unit="ms"),
        "Open": agg.open,
        "High": agg.high,
        "Low": agg.low,
        "Close": agg.close,
        "Volume": agg.volume
        })
    
    data = pd.DataFrame(all_rows)
    data["Time"] = data.index.time
    data["Date"] = data.index.date
    
    #conversion to NY times
    data["Date"] = (
    pd.to_datetime(data["Date"], utc=True)
      .dt.tz_convert("America/New_York")
      .dt.tz_localize(None)
    )

    #sessionfilter
    data = data[
    (data.index.time >= time(9,30)) &
    (data.index.time <= time(16,0))
    ]

    data = data.set_index("Date")
    data.index.name = "Datetime"

    return data
        