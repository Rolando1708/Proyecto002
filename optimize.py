import numpy as np
from backtest import backtest
from metrics import calmar_ratio
from signals import get_signals


def optimization(trial, train_data) -> float:
    data = train_data.copy()
    rsi_window = trial.suggest_int('rsi_window', 10, 20)
    rsi_lower = trial.suggest_int('rsi_lower', 20, 35)
    rsi_upper = trial.suggest_int('rsi_upper', 65, 80)

    macd_fast = trial.suggest_int('macd_fast', 8, 15)
    macd_slow = trial.suggest_int('macd_slow', 20, 40)
    macd_signal = trial.suggest_int('macd_signal', 5, 10)

    bb_window = trial.suggest_int('bb_window', 18, 25)
    bb_dev = trial.suggest_float('bb_dev', 1.8, 2.5)

    stop_loss = trial.suggest_float('stop_loss', 0.01, 0.10)
    take_profit = trial.suggest_float('take_profit', 0.01, 0.15)
    capital_exposure = trial.suggest_float('capital_exposure', 0.001, 0.25, log=True)

    params = {
        'rsi_window': rsi_window,
        'rsi_lower': rsi_lower,
        'rsi_upper': rsi_upper,
        'macd_fast': macd_fast,
        'macd_slow': macd_slow,
        'macd_signal': macd_signal,
        'bb_window': bb_window,
        'bb_dev': bb_dev,
        'stop_loss': stop_loss,
        'take_profit': take_profit,
        'capital_exposure': capital_exposure
    }

    data = get_signals(data, params)
    n_splits = 5
    len_data = len(data)
    calmars = []
    for i in range(n_splits):
        size = len_data // n_splits
        start_index = i * size
        end_index = (i + 1) * size
        chunk = data.iloc[start_index:end_index, :]
        port_vals, _, _ = backtest(chunk, cash=1_000_000, params=params)
        calmar = calmar_ratio(port_vals)
        calmars.append(calmar)

    return float(np.mean(calmars))

        