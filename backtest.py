import ta

from models import Operation
from portfolio_value import get_portfolio_value


def backtest(data, trail) -> float:
    data = data.copy()

    # Hyperparameters
    rsi_window = trail.suggest_int('rsi_window', 5, 50)
    rsi_lower = trail.suggest_int('rsi_lower', 5, 35)
    rsi_upper = trail.suggest_int('rsi_upper', 65, 95)
    stop_loss = trail.suggest_float('stop_loss', 0.01, 0.15)
    take_profit = trail.suggest_float('take_profit', 0.01, 0.15)
    n_shares = trail.suggest_int('n_shares', 50, 500)

    # RSI
    rsi_indicator = ta.momentum.RSIIndicator(data.Close, window=rsi_window)
    data['RSI'] = rsi_indicator.rsi()

    # Signals
    historic = data.dropna()
    historic['buy_signal'] = historic.RSI < rsi_lower   # LONG ENTRY
    historic['sell_signal'] = historic.RSI > rsi_upper  # SHORT ENTRY

    # Trading setup
    COM = 0.125 / 100
    SL = stop_loss
    TP = take_profit

    cash = 1_000_000
    active_long_positions: list[Operation] = []
    active_short_positions: list[Operation] = []

    portfolio_value = [cash]

    # Loop through each row
    for i, row in historic.iterrows():

        # --- close long positions ---
        for position in active_long_positions.copy():
            if row.Close > position.take_profit or row.Close < position.stop_loss:
                cash += row.Close * position.n_shares * (1 - COM)
                active_long_positions.remove(position)

        # --- close short positions ---
        for position in active_short_positions.copy():
            if row.Close < position.take_profit or row.Close > position.stop_loss:
                # buy back to cover short
                pnl = (position.price - row.Close) * position.n_shares
                cash += pnl - (row.Close * position.n_shares * COM)
                active_short_positions.remove(position)

        # --- enter LONG if signal and enough cash ---
        if row.buy_signal:
            if cash >= row.Close * n_shares * (1 + COM):
                cash -= row.Close * n_shares * (1 + COM)
                active_long_positions.append(
                    Operation(
                        time=row.Datetime,
                        price=row.Close,
                        stop_loss=row.Close * (1 - SL),
                        take_profit=row.Close * (1 + TP),
                        n_shares=n_shares,
                        type="LONG",
                    )
                )

        # --- enter SHORT if signal ---
        if row.sell_signal:
            # you get cash immediately when shorting
            cash += row.Close * n_shares * (1 - COM)
            active_short_positions.append(
                Operation(
                    time=row.Datetime,
                    price=row.Close,
                    stop_loss=row.Close * (1 + SL), 
                    take_profit=row.Close * (1 - TP),
                    n_shares=n_shares,
                    type="SHORT",
                )
            )

        # --- update portfolio value ---
        portfolio_value.append(
            get_portfolio_value(
                cash,
                active_long_positions,
                active_short_positions,
                row.Close,
                n_shares,
                COM
            )
        )

    # Final return (after loop)
    return (portfolio_value[-1] / 1_000_000) - 1


    