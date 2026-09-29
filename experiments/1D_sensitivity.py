from src.data_loader import load_yfinance_data, load_daily_data
from src.indicators import get_vwap, get_ema, get_atr, get_dayrange
from src.strategy import crossover_strategy
from experiments.sensitivity_analysis import sensitivity_analysis_1d

ticker= "SPY"

data = load_yfinance_data(ticker)
daily = load_daily_data(ticker)

data = get_vwap(data)
data = get_ema(data)
data = get_atr(data, daily)
data = get_dayrange(data)

data = crossover_strategy(data)

parameters = {
    "stop_distance": [0.025, 0.05, 0.075, 0.1, 0.125, 0.15],
    "risk_reward_ratio": [1, 1.5, 2, 2.5, 3],
    "slippage_bps": [1, 2, 3, 4, 5],
    "commission_per_share": [0.002, 0.005, 0.007, 0.01]
}

parameter = "stop_distance"
results_df = sensitivity_analysis_1d(data, parameter, parameters[parameter])
print(results_df.to_string(index=False))
    
