import matplotlib.pyplot as plt

def plot_portfolio_value(portfolio_value_train):
    plt.figure(figsize=(12, 6))
    plt.plot(portfolio_value_train, label='Portfolio Value Train')
    plt.title('Portfolio Value Over Time')
    plt.xlabel('Time')
    plt.ylabel('Portfolio Value ($)')
    plt.legend()
    plt.grid(True)
    plt.show()



def plot_test_validation(portfolio_value_test, portfolio_value_validation):

    plt.figure(figsize=(12, 6))

    test = range(len(portfolio_value_test))
    validation = range(len(portfolio_value_test), len(
        portfolio_value_test) + len(portfolio_value_validation))

    plt.plot(test, portfolio_value_test,
            linewidth=2, label="Test Portfolio Value")
    plt.plot(validation, portfolio_value_validation,
            linewidth=2, label="Validation Portfolio Value")

    plt.title("Evolución del valor del portafolio (Test + Validation)")
    plt.xlabel("Time")
    plt.ylabel("Portfolio Value")
    plt.legend()
    plt.grid(True)
    plt.show()