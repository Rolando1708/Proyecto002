from models import Operation



def get_portfolio_value(cash: float, long_ops: list, short_ops: list, current_price: float,
                        n_shares: float) -> float:
    val = cash

    # Longs: current market value of holdings
    for pos in long_ops:
        val += current_price * pos.n_shares

    # Shorts: mark-to-market profit (entry_price - current_price) * n_shares
    for pos in short_ops:
        val += (pos.price * pos.n_shares) + (pos.price - current_price) * pos.n_shares

    return val
