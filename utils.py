import pandas as pd

def modified_data(data: str) -> pd.DataFrame:
    """
    Modifica el DataFrame de datos para preparar el análisis.
    Args:
        data (pd.DataFrame): DataFrame que contiene los datos históricos del activo, incluyendo la columna 'Date'.
    Returns:
        pd.DataFrame: DataFrame modificado con la columna 'Datetime' y ordenado cronológicamente.
    """
    data = data.copy()
    data = data.rename(columns={'Date': 'Datetime'})
    data['Datetime'] = pd.to_datetime(data['Datetime'], errors='coerce', dayfirst=True)
    data = data.iloc[::-1].reset_index(drop=True)

    return data


def dataset_split(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Divide el DataFrame de datos en conjuntos de entrenamiento, prueba y validación.
    Args:
        data (pd.DataFrame): DataFrame que contiene los datos históricos del activo.
    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Tres DataFrames correspondientes a los conjuntos de entrenamiento, prueba y validación.
    """
    train_size = int(len(data) * 0.6)
    test_size = int(len(data) * 0.2)
    train_data = data[:train_size]
    test_data = data[train_size:train_size + test_size]
    validation_data = data[train_size + test_size:]

    return train_data, test_data, validation_data