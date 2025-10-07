import pandas as pd


def returns(portfolio_value_test, portfolio_value_validation, test_split, validation_split) -> tuple[pd.Series, pd.DataFrame]:
    test_validation = pd.concat([test_split, validation_split]).reset_index(drop=True)
    portfolio_value_test = portfolio_value_test.to_list()
    portfolio_value_validation = portfolio_value_validation.to_list()
    portfolio_total = portfolio_value_test + portfolio_value_validation
    portfolio_total = pd.Series(portfolio_total)

    portfolio_validation_index_dates = pd.DataFrame({
        'Portfolio Value': portfolio_total,
        'Datetime': test_validation['Datetime']
    })

    portfolio_validation_index_dates['Datetime'] = pd.to_datetime(portfolio_validation_index_dates['Datetime'])
    portfolio_validation_index_dates = portfolio_validation_index_dates.set_index('Datetime')
   
    portfolio_validation_index_dates['Returns'] = portfolio_validation_index_dates['Portfolio Value'].pct_change()

    monthly_returns = portfolio_validation_index_dates['Returns'].resample('ME').apply(lambda x: (1 + x).prod() - 1)
    quarterly_returns = portfolio_validation_index_dates['Returns'].resample('QE').apply(lambda x: (1 + x).prod() - 1)
    annual_returns = portfolio_validation_index_dates['Returns'].resample('YE').apply(lambda x: (1 + x).prod() - 1)

    portfolio_validation_through_time = pd.DataFrame({
        "Monthly Returns": monthly_returns,
        "Quarterly Returns": quarterly_returns,
        "Annual Returns": annual_returns
    })

    portfolio_validation_through_time = portfolio_validation_through_time.fillna(0)    

    return portfolio_total, portfolio_validation_through_time 