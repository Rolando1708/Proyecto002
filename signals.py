import pandas as pd
import ta

def rsi(data: pd.DataFrame, rsi_window: int, rsi_lower: int, rsi_upper: int) -> tuple:
    rsi_indicator = ta.momentum.RSIIndicator(data.Close, window=rsi_window)
    rsi_indicator = rsi_indicator.rsi()
    buy_signal_rsi = rsi_indicator < rsi_lower
    sell_signal_rsi = rsi_indicator > rsi_upper

    return buy_signal_rsi, sell_signal_rsi