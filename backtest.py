import ta

from models import Operation
from portfolio_value import get_portfolio_value


def backtest(data, stop_loss, take_profit, n_shares) -> float:
    data = data.copy()

 

  
    COM = 0.125 / 100
    SL = stop_loss
    TP = take_profit

    cash = 1_000_000
    active_long_positions: list[Operation] = []
    active_short_positions: list[Operation] = []

    portfolio_value = [cash]

    
    for i, row in data.iterrows():

        # Close Positions
        
        # LONG
        for position in active_long_positions.copy():
            if row.Close > position.take_profit or row.Close < position.stop_loss:
                cash += row.Close * position.n_shares * (1 - COM)
                active_long_positions.remove(position)

        # SHORT
        for position in active_short_positions.copy():
            if row.Close < position.take_profit or row.Close > position.stop_loss:
                pnl = ((position.price - row.Close) * position.n_shares) * (1- COM)
                cash += (row.Close * position.n_shares ) + pnl
                active_short_positions.remove(position)

        # LONG Signal
        if row.buy_signal:
            cost = row.Close * n_shares * (1 + COM)
            if cash >= cost:
                cash -= cost
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

       # SHORT Signal
        if row.sell_signal:
            cost = row.Close * n_shares * (1 + COM)
            if cash >= cost:
                cash -= cost
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

        
        portfolio_value.append(
            get_portfolio_value(
                cash,
                active_long_positions,
                active_short_positions,
                row.Close,
                n_shares
            )
        )

    # Final return (after loop)
    return (portfolio_value[-1] / 1_000_000) - 1


    