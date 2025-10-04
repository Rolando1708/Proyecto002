import matplotlib.pyplot as plt
import pandas as pd

def plot_portfolio_value(portfolio_value_train):

    plt.figure(figsize=(12, 6))
    plt.plot(portfolio_value_train, label='Portfolio Value Train', color='blue')
    plt.title('Portfolio Value Over Time')
    plt.xlabel('Time')
    plt.ylabel('Portfolio Value ($)')
    plt.legend()
    plt.grid(True)
    plt.show()



def plot_test_validation(portfolio_value_test, portfolio_value_validation, test, validation):

    test_data = pd.DataFrame({
        'Datetime': test['Datetime'].reset_index(drop=True),
        'Portfolio Value': portfolio_value_test
    })

    validation_data = pd.DataFrame({
        'Datetime': validation['Datetime'].reset_index(drop=True),
        'Portfolio Value': portfolio_value_validation
    })

    plt.figure(figsize=(12, 6))
    plt.plot(test_data['Datetime'], test_data['Portfolio Value'], label='Portfolio Value Test', color='orange')
    plt.plot(validation_data['Datetime'], validation_data['Portfolio Value'], label='Portfolio Value Validation', color='green')
    plt.title('Portfolio Value Over Time (Test & Validation)')
    plt.xlabel('Time')
    plt.ylabel('Portfolio Value ($)')
    plt.legend()
    plt.grid(True)
    plt.show()