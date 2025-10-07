import pandas as pd
import numpy as np

def sharpe_ratio(port_value: pd.Series) -> float:
    returns = port_value.pct_change().dropna()
    mu = returns.mean()
    sigma = returns.std()
    mu_ann = mu * (365 * 24)
    sigma_ann = sigma * np.sqrt(365 * 24)
    if sigma_ann > 0:
        sharpe = mu_ann / sigma_ann
    else:
        sharpe = 0
    return sharpe

def sortino_ratio(port_value: pd.Series) -> float:
    returns = port_value.pct_change().dropna()
    mean_ret = returns.mean()
    downside = np.minimum(returns ,0).std()

    mean_ann = mean_ret * (365 * 24)
    downside_std_ann = downside * np.sqrt(365 * 24)
    if downside_std_ann > 0:
        sortino = mean_ann / downside_std_ann
    else:
        sortino = 0
    return sortino

def maximum_drawdown(port_value: pd.Series) -> float:
    peaks = port_value.cummax()
    dd = (port_value - peaks) / peaks 
    maximum_dd = dd.min() 
    return abs(maximum_dd)

def calmar_ratio(port_value: pd.Series) -> float:
    returns = port_value.pct_change().dropna()
    mean_ann = returns.mean() * (24 * 365)
    mdd = maximum_drawdown(port_value) 

    if mdd > 0:
        calmar = mean_ann / mdd
    else:
        calmar = 0.0
    return calmar



def metrics(port_value: pd.Series) -> pd.DataFrame:
    metrics_df = pd.DataFrame({
        'Sharpe Ratio': [sharpe_ratio(port_value)],
        'Sortino Ratio': [sortino_ratio(port_value)],
        'Maximum Drawdown': [maximum_drawdown(port_value)],
        'Calmar Ratio': [calmar_ratio(port_value)],
    }, index = ["Metrics"])
    return metrics_df


    
