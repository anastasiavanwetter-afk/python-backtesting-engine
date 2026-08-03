# Python Backtesting Engine

## Description
pyhton backtesting engine for developing and testing trading strategies on user-provided market data. It is a pipeline that separates loading data (+ preprocessing), introducing indicators, strategy generation, backtesting and statistics. Results are visualised with a separate plotting module. The Main purpose of this project is to improve my python skills while learning quantitative trading and backtesting strategies.

## Project structure

```text
src/
├── data_loader.py
├── indicators.py
├── strategy.py
├── backtester.py
├── performance.py
├── plots.py
└── main.py
```

| File | Description |
|------|-------------|
| `data_loader.py` | Downloads data, source can be chosen by the user. Prepares the data for usage. |
| `indicators.py` | Introduces technical indicators that will be used within the strategy. |
| `strategy.py` | Generates trading signals. |
| `backtester.py` | Uses the generated signals to simulate trades. |
| `performance.py` | Calculates perfpormance statistics from the list of simulated trades. |
| `plots.py` | Visualises the obtained results. |
| `main.py` | Runs complete pipeline |

## Installation
```bash
pip install yfinance pandas numpy matplotlib ta
```

## Pipeline
```python
ticker = "NVDA"

data = load_yfinance_data(ticker)
daily = load_daily_data(ticker)

data = get_vwap(data)
data = get_ema(data)
data = get_atr(data, daily)
data = get_dayrange(data)

data = crossover_strategy(data)

trades = backtest(data)

stats = key_statistics(trades)
print(stats)

equity_curve(trades)
drawdown_curve(trades)
pnl_per_trade(trades)
distribution_exits(trades)
distribution_PnL(trades)
```

## Strategy
To test the engine a crossover strategy was created where a signal is generated whenever the 9 EMA crosses over/under the VWAP within the first hour after market open (as this is a momentum driven strategy). 

Entry
- EMA crosses over VWAP --> long
- EMA crosses under VWAP --> short
- Timeframe: 09:40 - 10:30 (NY time)
- Entry on next candle open

Exit
- stoploss
- takeprofit
- end of day

Risk managment
- stoploss at cross (with a minimum stop of 0.05*ATR_(daily) to avoid too tight stops)
- takeprofit at a fixed risk-reward-ratio of 2 (which has to be within ATR_(daily) boundaries)

## Example output
Engine ran on 03/08/2026 13:28 for ticker "NVDA"

output:
```text
Trades            28.00
Winrate           42.86
ProfitFactor       1.81
TotalPnL        1077.80
AvgWin           200.19
AvgLoss          -82.78
MaxDrawdown     -647.89
Return/DD          1.66
dtype: float64
```

example plots:
### Equity Curve
![Equity Curve](images/equity_curve.png)

### Drawdown Curve
![Drawdown Curve](images/drawdown_curve.png)

### PnL Distribution
![PnL Distribution](images/pnl_distribution.png)

### Exit Distribution
![Exit Distribution](images/exit_distribution.png)

## Future improvements
- additional indicators such as RSI, MACD, Volume, Relative Volume
- adding news/events/earnings
- multiple strategies
- additional outcome statistics such as sharpe ratio ((sortino ratio), expectancy, average holding time
- commission/slippage modelling
- partial exit
- trailing stoploss
- parameter optimisation