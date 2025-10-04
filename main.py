import pandas as pd



def main():
    data = pd.read_csv('Binance_BTCUSDT_1h.csv').dropna()


if __name__ == '__main__':
    main()