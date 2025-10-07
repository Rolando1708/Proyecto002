import pandas as pd
from models import Operation
from portfolio_value import get_portfolio_value

def backtest(data, cash: float, params: dict) -> tuple[pd.Series, float, float]:
    """
    Calcula el total del portafolio a lo largo del tiempo, considerando las operaciones activas y el efectivo disponible.
    Args:
        data (pd.DataFrame): DataFrame que contiene los datos históricos del activo, incluyendo señales de compra y venta.
        cash (float): Monto inicial de efectivo disponible para operar.
        params (dict): Diccionario que contiene los parámetros necesarios para la simulación, como stop_loss, take_profit y capital_exposure.
        
    Returns:
        tuple[pd.Series, float, float]:
    """
    data = data.copy()
    COM = 0.00125 
    stop_loss = params['stop_loss']
    take_profit = params['take_profit']
    capital_exposure = params['capital_exposure']

    active_long_positions: list[Operation] = []
    active_short_positions: list[Operation] = []  

    portfolio_value = []
    trades = 0
    wins = 0

    for _, row in data.iterrows():
        n_shares = (cash * capital_exposure) / row.Close

        # Close LONG positions
        for position in active_long_positions.copy():
            if (position.stop_loss > row.Close) or (position.take_profit < row.Close):
                pnl = (row.Close - position.price) * position.n_shares * (1 - COM)
                if pnl > 0:
                    wins += 1
                trades += 1
                cash += row.Close * position.n_shares * (1 - COM)
                active_long_positions.remove(position)

        
        # Close SHORT positions
        for position in active_short_positions.copy():
            if (position.stop_loss < row.Close) or (position.take_profit > row.Close):
                pnl = (position.price - row.Close) * position.n_shares * (1 - COM)
                if pnl > 0:
                    wins += 1
                trades += 1
                cash += (position.price * position.n_shares) + pnl
                active_short_positions.remove(position)

        if row.buy_signal:
            cost = row.Close * n_shares * (1 + COM)
            if cash >= cost: 
                cash -= cost
                active_long_positions.append(
                    Operation(
                        time=row.Datetime,
                        price=row.Close,
                        stop_loss=row.Close * (1 - stop_loss),
                        take_profit=row.Close * (1 + take_profit),
                        n_shares=n_shares,
                        type="LONG",
                    )
                )
        if row.buy_signal:
            cost = row.Close * n_shares * (1 + COM)
            if cash >= cost: 
                cash -= cost
                active_long_positions.append(
                    Operation(
                        time=row.Datetime,
                        price=row.Close,
                        stop_loss=row.Close * (1 + stop_loss),
                        take_profit=row.Close * (1 - take_profit),
                        n_shares=n_shares,
                        type="LONG",
                    )
                )

        # --- RECORD PORTFOLIO VALUE ---
        portfolio_value.append(
            get_portfolio_value(
                cash,
                active_long_positions,
                active_short_positions,
                row.Close,
                n_shares,
            )
        )

    for position in active_long_positions.copy():
        pnl = (data.iloc[-1].Close - position.price) * position.n_shares * (1 - COM)
        if pnl > 0:
            wins += 1
        trades += 1
        cash += data.iloc[-1].Close * position.n_shares * (1 - COM)

    for position in active_short_positions.copy():
        pnl = (position.price - data.iloc[-1].Close) * position.n_shares * (1 - COM)
        if pnl > 0:
            wins += 1
        trades += 1
        cash += (position.price * position.n_shares) + pnl

    active_long_positions = []
    active_short_positions = []

    win_rate = (wins / trades) * 100.0 if trades > 0 else 0.0  # in percent
    return pd.Series(portfolio_value), cash, win_rate





    