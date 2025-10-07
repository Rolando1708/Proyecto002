import pandas as pd
import ta
from ta.volatility import BollingerBands

def rsi(data: pd.DataFrame, rsi_window: int, rsi_lower: int, rsi_upper: int) -> tuple:
    """
    Calcula las señales de compra y venta basadas en el indicador RSI (Relative Strength Index).
    Args:
        data (pd.DataFrame): DataFrame que contiene los datos históricos del activo, incluyendo la columna 'Close'.
        rsi_window (int): Ventana de tiempo para calcular el RSI.
        rsi_lower (int): Umbral inferior para generar señales de compra.
        rsi_upper (int): Umbral superior para generar señales de venta.
    Returns:
        tuple: Dos Series booleanas que indican las señales de compra y venta respectivamente.
    """
    rsi_indicator = ta.momentum.RSIIndicator(data.Close, window=rsi_window)
    rsi_indicator = rsi_indicator.rsi()
    buy_signal_rsi = rsi_indicator < rsi_lower
    sell_signal_rsi = rsi_indicator > rsi_upper

    return buy_signal_rsi, sell_signal_rsi

def macd(data: pd.DataFrame, short_window: int, long_window: int, signal_window: int) -> tuple:
    """
    Calcula las señales de compra y venta basadas en el indicador MACD (Moving Average Convergence Divergence).
    Args:
        data (pd.DataFrame): DataFrame que contiene los datos históricos del activo, incluyendo la columna 'Close'.
        short_window (int): Ventana de tiempo para la media móvil rápida.
        long_window (int): Ventana de tiempo para la media móvil lenta.
        signal_window (int): Ventana de tiempo para la línea de señal.
    Returns:
        tuple: Dos Series booleanas que indican las señales de compra y venta respectivamente.
    """
    macd_indicator = ta.trend.MACD(
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
    """
    Calcula las señales de compra y venta basadas en las Bandas de Bollinger.
    Args:
        data (pd.DataFrame): DataFrame que contiene los datos históricos del activo, incluyendo la columna 'Close'.
        bb_window (int): Ventana de tiempo para calcular las Bandas de Bollinger.
        bb_std (int): Número de desviaciones estándar para calcular las Bandas de Bollinger.
    Returns:
        tuple: Dos Series booleanas que indican las señales de compra y venta respectivamente.
    """
    bb_indicator = BollingerBands(close=data.Close, window=bb_window, window_dev=bb_std)

    upper_band = bb_indicator.bollinger_hband()
    lower_band = bb_indicator.bollinger_lband()
    buy_signal_bb = data.Close < lower_band
    sell_signal_bb = data.Close > upper_band

    return buy_signal_bb, sell_signal_bb

def get_signals(data: pd.DataFrame, params: dict) -> pd.DataFrame:
    # Individual signals
    buy_rsi, sell_rsi = rsi(
        data,
        params['rsi_window'],
        params['rsi_lower'],
        params['rsi_upper']
    )

    buy_macd, sell_macd = macd(
        data,
        params['macd_fast'],
        params['macd_slow'],
        params['macd_signal']
    )

    buy_bb, sell_bb = bollinger(
        data,
        params['bb_window'],
        params['bb_dev']
    )

    buy_signals = buy_rsi.astype(int) + buy_macd.astype(int) + buy_bb.astype(int)
    sell_signals = sell_rsi.astype(int) + sell_macd.astype(int) + sell_bb.astype(int)
    data['buy_signal'] = buy_signals >= 2 
    data['sell_signal'] = sell_signals >= 2 

    return data