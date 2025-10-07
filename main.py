
import optuna
import pandas as pd
from backtest import backtest
from metrics import metrics
from optimize import optimization
from plots import plot_portfolio_value, plot_test_validation
from signals import get_signals
from tables import returns
from utils import dataset_split, modified_data



def main():
    """
    Funcion principal que ejecuta el proceso de optimizacion, backtesting y evaluacion de una estrategia de trading.
    Returns:
        None: Imprime los resultados de la optimizacion y el backtesting.
    """
    data = pd.read_csv('Binance_BTCUSDT_1h.csv').dropna()
    data = modified_data(data)
    train_split, test_split, validation_split  = dataset_split(data)
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: optimization(trial, train_split), n_trials = 50)


    print("\n Best params:")
    print(study.best_params)
    print(f"\n Best value: {study.best_value:.4f}\n")

    print ("--- Train Results ---")

    data_train = get_signals(train_split.copy(), study.best_params)
    portfolio_value_train, cash_train, win_rate_train = backtest(data_train, cash=1_000_000, params=study.best_params)
    
    print(f"Portfolio Final Value: {portfolio_value_train.iloc[-1]:,.2f}")
    print(f"Final Cash: {cash_train:,.2f}")
    print(f"Win Rate: {win_rate_train:.2f}%")
    print(metrics(portfolio_value_train))

    print ("--- Test Results ---")

    data_test = get_signals(test_split.copy(), study.best_params)
    portfolio_value_test, cash_test, win_rate_test = backtest(data_test, cash=1_000_000, params=study.best_params)
    
    print(f"Portfolio Final Value: {portfolio_value_test.iloc[-1]:,.2f}")
    print(f"Final Cash: {cash_test:,.2f}")
    print(f"Win Rate: {win_rate_test:.2f}%")
    print(metrics(portfolio_value_test))

    print ("--- Validation Results ---")

    data_validation = get_signals(validation_split.copy(), study.best_params)
    portfolio_value_validation, cash_validation , win_rate_validation = backtest(data_validation, cash_test, params=study.best_params)
    
    print(f"Portfolio Final Value: {portfolio_value_validation.iloc[-1]:,.2f}")
    print(f"Final Cash: {cash_validation:,.2f}")
    print(f"Win Rate: {win_rate_validation:.2f}%")
    print(metrics(portfolio_value_validation))

    print("-- Test + Validation Results --")
    
    portfolio_total, portfolio_through_time = returns(portfolio_value_test, portfolio_value_validation, test_split, validation_split)

    print("Metrics:")
    print(metrics(portfolio_total))

    print("Returns:")
    print(portfolio_through_time)

    plot_portfolio_value(portfolio_value_train)
    plot_test_validation(portfolio_value_test, portfolio_value_validation)

if __name__ == '__main__':
    main()