import numpy as np
from backtest import backtest
from metrics import calmar_ratio
from signals import get_signals


def optimize(trial, train_data) -> float:
    rsi_window = trial.suggest_int('rsi_window', 5, 50)
    rsi_lower = trial.suggest_int('rsi_lower', 5, 35)
    rsi_upper = trial.suggest_int('rsi_upper', 65, 95)

    macd_fast = trial.suggest_int('macd_fast', 8, 15)
    macd_slow = trial.suggest_int('macd_slow', 20, 35)
    macd_signal = trial.suggest_int('macd_signal', 5, 10)

    bb_window = trial.suggest_int('bb_window', 10, 30)
    bb_dev = trial.suggest_int('bb_dev', 1, 3)

    params = {
        'rsi_window': rsi_window,
        'rsi_lower': rsi_lower,
        'rsi_upper': rsi_upper,
        'macd_fast': macd_fast,
        'macd_slow': macd_slow,
        'macd_signal': macd_signal,
        'bb_window': bb_window,
        'bb_dev': bb_dev
    }

    stop_loss = trial.suggest_float('stop_loss', 0.01, 0.15)
    take_profit = trial.suggest_float('take_profit', 0.01, 0.15)
    n_shares = trial.suggest_int('n_shares', 50, 500)


    data = train_data.copy()
    #trial.suggest params
    n_splits = 5
    len_data = len(data)
    calmars = []
    data = get_signals(data, params)
    for i in range (n_splits):
        size = len_data // n_splits
        start_index = i * size
        end_index = (i + 1) * size
        chunk = data.iloc[start_index:end_index]
        port_vals = backtest(chunk, stop_loss, take_profit, n_shares)
        calmar = calmar_ratio(port_vals)
        calmars.append(calmar)

        return np.mean(calmars)
        