import kagglehub
import os
import pandas as pd

# Download dataset
path = kagglehub.dataset_download("paultimothymooney/stock-market-data")
sp500_csv_dir = os.path.join(path, "stock_market_data", "sp500", "csv")

def get_market_confidence():
    """
    Computes a market confidence score based on historical stock market performance.
    Confidence >1 indicates a strong market; <1 indicates a weak market.
    """
    # Load Apple (AAPL) stock data
    aapl_file = os.path.join(sp500_csv_dir, "AAPL.csv")
    df = pd.read_csv(aapl_file)

    # Convert 'Date' column to datetime with correct format
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

    # Sort by date to ensure time order
    df = df.sort_values(by="Date")

    # Compute 30-day rolling average of daily returns using 'Adjusted Close'
    df['Return'] = df['Adjusted Close'].pct_change(fill_method=None)  # FIX: No auto-fill for missing values
    rolling_avg = df['Return'].rolling(window=30).mean().iloc[-1]

    # Normalize confidence score
    confidence = 1 + (rolling_avg * 10)
    return max(confidence, 0.5)  # Ensure it doesn't go too low

def get_top_stocks():
    """
    Retrieves the top 5 stocks based on recent performance.
    """
    # Iterate through multiple stock files in the dataset directory
    stock_files = [f for f in os.listdir(sp500_csv_dir) if f.endswith('.csv')]

    stock_performance = {}

    for file in stock_files:
        stock_path = os.path.join(sp500_csv_dir, file)
        df = pd.read_csv(stock_path)

        # Ensure 'Date' is parsed correctly with the correct format
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        df = df.sort_values(by="Date")

        # Calculate recent 30-day return if enough data exists
        if len(df) > 30 and 'Adjusted Close' in df.columns:
            df['Return'] = df['Adjusted Close'].pct_change(fill_method=None)  # FIX: No auto-fill for missing values
            last_30d_return = df['Return'].rolling(window=30).mean().iloc[-1]
            stock_performance[file.replace(".csv", "")] = last_30d_return

    # Get the top 5 performing stocks
    top_stocks = sorted(stock_performance, key=stock_performance.get, reverse=True)[:5]

    return top_stocks