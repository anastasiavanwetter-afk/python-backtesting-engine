from src.data_loader import load_yfinance_data, load_daily_data
from src.indicators import get_vwap, get_ema, get_atr, get_dayrange
from src.strategy import crossover_strategy

from datetime import date

def split_data(ticker, year, month, day):
    data = load_yfinance_data(ticker)
    daily = load_daily_data(ticker)
    
    data = get_vwap(data)
    data = get_ema(data)
    data = get_atr(data, daily)
    data = get_dayrange(data)
    
    data = crossover_strategy(data)
    
    # split data at chosen date boundary
    split_date = date(year, month, day)
    
    is_data = data[data["Date"] < split_date].copy()
    oos_data = data[data["Date"] >= split_date].copy()

    return is_data, oos_data
    
    
    