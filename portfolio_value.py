from models import Operation


def get_portfolio_value(cash: float, long_ops: list[Operation], short_ops: list[Operation], current_price: float,
                        n_shares: int, COM: float) -> float:
    val = cash

    # Add long positions value
    val += len(long_ops) * current_price * n_shares

    # Add short positions equity (margin_account + margin_requirement - cost to cover)
    for pos in short_ops:
        pnl = (pos.price - current_price) * pos.n_shares * (1-COM)
        val +=  pnl

    return val