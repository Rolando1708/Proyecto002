import pandas as pd
import numpy as np

def sharpe_ratio(port_value: pd.Series) -> float:
    returns = port_value.pct_change().dropna()
    mu = returns.mean()
    sigma = returns.std()
    mu_ann = mu * 365 * 24
    sigma_ann = sigma * np.sqrt(365 * 24)
    if sigma_ann > 0:
        sharpe = mu_ann / sigma_ann
    else:
        sharpe = 0
    return sharpe

def sortino_ratio(port_value: pd.Series) -> float:
    returns = port_value.pct_change().dropna()
    mean_ret = returns.mean()
    downside = returns[returns < 0]

    mean_ann = mean_ret * 365 * 24
    downside_std_ann = downside.std() * np.sqrt(365 * 24)
    if downside_std_ann > 0:
        sortino = mean_ann / downside_std_ann
    else:
        sortino = 0
    return sortino

def maximum_drawdown(port_value: pd.Series) -> float:
    peaks = port_value.cummax()
    dd = (port_value / peaks) - 1
    maximum_dd = dd.min()
    return maximum_dd


def calmar_ratio(port_value: pd.Series) -> float:
    returns = port_value.pct_change().dropna()
    mean_ann = returns.mean() * 365 * 24
    mdd = maximum_drawdown(port_value)

    if mdd > 0:
        calmar = mean_ann / mdd
    else:
        calmar = 0
    return calmar

def win_rate(port_value: pd.Series) -> float:
    returns = port_value.pct_change().dropna()
    total_trades = len(returns)
    winning_trades = (returns > 0).sum()

    if winning_trades > 0:
        win_rate_ = winning_trades / total_trades
    else:
        win_rate_ = 0
    return win_rate_