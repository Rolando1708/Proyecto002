import ta

from models import Operation
from portfolio_value import get_portfolio_value


def backtest(data, trail) -> float:
    data = data.copy()

    rsi_window = trail.suggest_int('rsi_window', 5, 50)
    rsi_lower = trail.suggest_int('rsi_lower', 5, 35)
    rsi_upper = trail.suggest_int('rsi_upper', 65, 95)
    stop_loss = trail.suggest_float('stop_loss', 0.01, 0.15)
    take_profit = trail.suggest_float('take_profit', 0.01, 0.15)
    n_shares = trail.suggest_int('n_shares', 50, 500)

    rsi_indicator = ta.momentum.RSIIndicator(data.Close, window=rsi_window)
    data['RSI'] = rsi_indicator.rsi()

    historic = data.dropna()
    historic['buy_signal'] = historic.RSI < rsi_lower
    historic['sell_signal'] = historic.RSI > rsi_upper

    COM = 0.125 / 100
    SL = stop_loss
    TP = take_profit

    cash = 1_000_000

    active_long_positions: list[Operation] = []

    portfolio_value = [cash]

    for i, row in historic.iterrows():

        # this only works for long positions...
    
        # close positions
        for position in active_long_positions.copy():

            if row.Close > position.take_profit or row.Close < position.stop_loss:
                cash += row.Close * position.n_shares * (1 - COM)
                active_long_positions.remove(position)

    # check signal

        if not row.buy_signal:
            portfolio_value.append(get_portfolio_value(cash, active_long_positions, [], row.Close, n_shares, COM))
            continue
    
        #check if you have enough cash

        if cash < row.Close * n_shares * (1 + COM):
            portfolio_value.append(get_portfolio_value(cash, active_long_positions, [], row.Close, n_shares, COM))
            continue

        #discount the cost

        cash -= row.Close * n_shares * (1 + COM)
        # save the operation as active position

        active_long_positions.append(
            Operation(
                time=row.Datetime,
                price=row.Close,
                stop_loss=row.Close * (1 - SL),
                take_profit=row.Close * (1 + TP),
                n_shares=n_shares,
                type='LONG'
            )
        )

        portfolio_value.append(get_portfolio_value(cash, active_long_positions, [], row.Close, n_shares, COM))

        cash += row.Close * len(active_long_positions) * n_shares * (1 - COM)
        active_long_positions = []

        return (cash / 1_000_000) - 1 
    