import pandas as pd
import ta
from ta.trend import MACD
from ta.volatility import BollingerBands

def rsi(data: pd.DataFrame, rsi_window: int, rsi_lower: int, rsi_upper: int) -> tuple:
    rsi_indicator = ta.momentum.RSIIndicator(data.Close, window=rsi_window)
    rsi_indicator = rsi_indicator.rsi()
    buy_signal_rsi = rsi_indicator < rsi_lower
    sell_signal_rsi = rsi_indicator > rsi_upper

    return buy_signal_rsi, sell_signal_rsi

def macd(data: pd.DataFrame, short_window: int, long_window: int, signal_window: int) -> tuple:
    macd_indicator = MACD(
        close=data.Close,
        window_slow=long_window,
        window_fast=short_window,
        window_sign=signal_window
    )

    macd_line = macd_indicator.macd()
    signal_line = macd_indicator.macd_signal()
    buy_signal_macd = macd_line > signal_line
    sell_signal_macd = macd_line < signal_line

    return buy_signal_macd, sell_signal_macd

def bollinger(data: pd.DataFrame, bb_window: int, bb_std: int) -> tuple:
    bb_indicator = BollingerBands(close=data.Close, window=bb_window, window_dev=bb_std)

    upper_band = bb_indicator.bollinger_hband()
    lower_band = bb_indicator.bollinger_lband()
    buy_signal_bb = data.Close < lower_band
    sell_signal_bb = data.Close > upper_band

    return buy_signal_bb, sell_signal_bb