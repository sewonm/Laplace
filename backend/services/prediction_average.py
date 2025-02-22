import kagglehub
import os
import pandas as pd

def get_market_data():
    """ Fetch market data from Kaggle and calculate return statistics. """
    path = kagglehub.dataset_download("paultimothymooney/stock-market-data")
    sp500_csv_dir = os.path.join(path, "stock_market_data", "sp500", "csv")

    # Load data for different assets
    stocks_df = pd.read_csv(os.path.join(sp500_csv_dir, "AAPL.csv"))
    bonds_df = pd.read_csv(os.path.join(sp500_csv_dir, "BND.csv"))
    cash_df = pd.read_csv(os.path.join(sp500_csv_dir, "CASH.csv"))  # Cash proxy (e.g., treasury yields)
    real_estate_df = pd.read_csv(os.path.join(sp500_csv_dir, "VNQ.csv"))

    # Convert to datetime and sort
    for df in [stocks_df, bonds_df, cash_df, real_estate_df]:
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        df.sort_values(by="Date", inplace=True)

    # Compute historical returns
    assets = [stocks_df, bonds_df, cash_df, real_estate_df]
    returns = [df['Adjusted Close'].pct_change().dropna() for df in assets]
    
    # Compute statistics
    expected_returns = [ret.mean() * 252 for ret in returns]  # Annualized return
    cov_matrix = np.cov([ret.values for ret in returns])

    return {"returns": np.array(expected_returns), "cov_matrix": cov_matrix}