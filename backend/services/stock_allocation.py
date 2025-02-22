import numpy as np
import pandas as pd
import os
import kagglehub
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

class StockReturnPredictor:
    def __init__(self, stock_symbol='AAPL'):
        self.stock_symbol = stock_symbol
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.dataset_path = self.download_kaggle_data()

    def download_kaggle_data(self):
        """Download stock market data from Kaggle"""
        path = kagglehub.dataset_download("paultimothymooney/stock-market-data")
        return os.path.join(path, "stock_market_data", "sp500", "csv")

    def get_stock_data(self):
        """Load stock data from Kaggle dataset"""
        stock_file = os.path.join(self.dataset_path, f"{self.stock_symbol}.csv")
        df = pd.read_csv(stock_file)

        # Convert Date column to datetime with explicit format
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')

        # Drop any rows where date conversion failed
        df.dropna(subset=['Date'], inplace=True)

        df.sort_values('Date', inplace=True)

        # Ensure only necessary columns
        df = df[['Date', 'Close', 'Volume']]
        df.set_index('Date', inplace=True)

        # Compute daily returns
        df['Return'] = df['Close'].pct_change().fillna(0)

        return df

    def prepare_features(self, df):
        """Create lagged features for predicting future returns"""
        df['SMA_5'] = df['Close'].rolling(window=5).mean().fillna(0)  # 5-day moving average
        df['SMA_10'] = df['Close'].rolling(window=10).mean().fillna(0)  # 10-day moving average
        df['Volatility'] = df['Return'].rolling(window=5).std().fillna(0)  # 5-day volatility

        # Target variable: next day's return
        df['Next_Return'] = df['Return'].shift(-1)

        # Drop NaN rows
        df.dropna(inplace=True)

        # Define features (X) and target variable (y)
        X = df[['SMA_5', 'SMA_10', 'Volatility']]
        y = df['Next_Return']

        return X, y

    def train_model(self, X, y):
        """Train the Random Forest model"""
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        
        # Evaluate model performance
        error = mean_absolute_error(y_test, predictions)
        print(f"Model Mean Absolute Error: {error:.5f}")

    def predict_next_return(self, df):
        """Predict the next stock return using the trained model"""
        X_latest = df[['SMA_5', 'SMA_10', 'Volatility']].iloc[-1].values.reshape(1, -1)
        predicted_return = self.model.predict(X_latest)[0]
        return predicted_return

if __name__ == "__main__":
    predictor = StockReturnPredictor(stock_symbol="AAPL")

    # Fetch and process stock data
    df = predictor.get_stock_data()
    X, y = predictor.prepare_features(df)

    # Train model
    predictor.train_model(X, y)

    # Predict next return
    predicted_return = predictor.predict_next_return(df)
    print(f"Predicted Next Day Return for {predictor.stock_symbol}: {predicted_return:.5f}")