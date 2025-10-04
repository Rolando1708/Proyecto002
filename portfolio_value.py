from models import Operation


def get_portfolio_value(cash: float, long_ops: list[Operation], short_ops: list[Operation], current_price: float,
                        n_shares: int) -> float:
    val = cash

    for pos in long_ops:
        val += current_price * pos.n_shares

    for pos in short_ops:
        val += (pos.price - pos.n_shares) + (pos.price - current_price) * pos.n_shares

    return val