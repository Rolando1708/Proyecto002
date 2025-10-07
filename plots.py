import matplotlib.pyplot as plt

def plot_portfolio_value(portfolio_value_train):
    """
    Grafica el valor del portafolio a lo largo del tiempo.
    Args:
        portfolio_value_train (pd.Series | list | np.ndarray): Valores del portafolio durante la fase de entrenamiento.
    Returns:
        None: Muestra una gráfica del valor del portafolio.
    """

    plt.figure(figsize=(12, 6))
    plt.plot(portfolio_value_train, label='Portfolio Value Train')
    plt.title('Portfolio Value Over Time')
    plt.xlabel('Time')
    plt.ylabel('Portfolio Value ($)')
    plt.legend()
    plt.grid(True)
    plt.show()



def plot_test_validation(portfolio_value_test, portfolio_value_validation):
    """
    Grafica la evolución del valor del portafolio durante las fases de prueba (test) y validación (validation).
    Args:
        portfolio_value_test (pd.Series | list | np.ndarray): Valores del portafolio durante la fase de prueba.
        portfolio_value_validation (pd.Series | list | np.ndarray): Valores del portafolio durante la fase de validación.
    Returns:
        None: Muestra una gráfica comparativa del valor del portafolio en ambas fases.
    """

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