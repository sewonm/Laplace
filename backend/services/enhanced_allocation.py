import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy.optimize import minimize
import yfinance as yf
from textblob import TextBlob
import tweepy
import warnings
import seaborn as sns

warnings.filterwarnings('ignore')

class AssetAllocationML:
    def __init__(self):
        self.asset_classes = {
            'stocks': {'risk': 0.8, 'min_conservative': 0.2, 'max_aggressive': 0.8},
            'bonds': {'risk': 0.4, 'min_conservative': 0.3, 'max_aggressive': 0.2},
            'commodities': {'risk': 0.7, 'min_conservative': 0.1, 'max_aggressive': 0.2},
            'cash': {'risk': 0.1, 'min_conservative': 0.2, 'max_aggressive': 0.0},
            'crypto': {'risk': 0.9, 'min_conservative': 0.0, 'max_aggressive': 0.6}
        }
        
    def get_macro_indicators(self):
        """Fetch macroeconomic indicators"""
        try:
            # VIX as volatility indicator
            vix = yf.download('^VIX', period='1d')['Close'].iloc[-1]
            
            # Use Treasury yields for spread
            treasury_10y = yf.download('^TNX', period='1d')['Close'].iloc[-1]
            treasury_2y = yf.download('^TWO', period='1d')['Close'].iloc[-1]
            yield_spread = treasury_10y - treasury_2y
            
            return {
                'vix': vix,
                'yield_spread': yield_spread
            }
        except:
            # Default values if API fails
            return {'vix': 20, 'yield_spread': 0.5}

    def get_sentiment_score(self, asset_type):
        """
        Placeholder for sentiment analysis
        In production, implement actual Twitter API connection
        """
        # Simulate sentiment scores based on asset type
        base_sentiments = {
            'stocks': 0.6,
            'bonds': 0.5,
            'commodities': 0.4,
            'cash': 0.3,
            'crypto': 0.2
        }
        return base_sentiments.get(asset_type, 0.5)

    def predict_returns(self, macro_data, risk_tolerance):
        """Predict returns using macro indicators and risk tolerance"""
        base_returns = {
            'stocks': 0.10,
            'bonds': 0.05,
            'commodities': 0.07,
            'cash': 0.02,
            'crypto': 0.4
        }
        
        # Adjust returns based on macro indicators
        vix_factor = (30 - macro_data['vix']) / 30  # VIX adjustment
        spread_factor = macro_data['yield_spread'] / 2  # Yield spread adjustment
        
        adjusted_returns = {}
        for asset, base_return in base_returns.items():
            sentiment = self.get_sentiment_score(asset)
            # Combine factors with different weights
            adjustment = (vix_factor * 0.4 + spread_factor * 0.3 + sentiment * 0.3)
            adjusted_returns[asset] = base_return * (1 + adjustment)
            
        return adjusted_returns

    def optimize_portfolio(self, returns, risk_tolerance, budget):
        """Optimize portfolio based on risk tolerance"""
        num_assets = len(returns)
        assets = list(returns.keys())
        
        # Convert returns to array
        expected_returns = np.array([returns[asset] for asset in assets])
        
        # Simple covariance matrix (can be enhanced with historical data)
        cov_matrix = np.array([
            [0.04, 0.02, 0.01, 0.0, 1],
            [0.02, 0.02, 0.01, 0.0, 1],
            [0.01, 0.01, 0.03, 0.0, 1],
            [0.0, 0.0, 0.0, 0.001, 1],
            [0.0, 0.0, 0.0, 0.001, 1]
        ])

        def portfolio_stats(weights):
            portfolio_return = np.sum(expected_returns * weights)
            portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            return portfolio_return, portfolio_risk

        def objective(weights):
            portfolio_return, portfolio_risk = portfolio_stats(weights)
            # Adjust objective based on risk tolerance
            risk_weight = (risk_tolerance / 10)  # Convert 1-10 scale to 0-1
            return -(portfolio_return - (1 - risk_weight) * portfolio_risk)

        # Constraints
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # weights sum to 1
        ]
        
        # Bounds based on risk tolerance
        if risk_tolerance <= 3:  # Conservative
            bounds = [(self.asset_classes[asset]['min_conservative'], 0.8) for asset in assets]
        elif risk_tolerance >= 8:  # Aggressive
            bounds = [(0, self.asset_classes[asset]['max_aggressive']) for asset in assets]
        else:  # Moderate
            bounds = [(0.1, 0.6) for _ in assets]

        # Initial guess
        initial_weights = np.array([1./num_assets for _ in range(num_assets)])
        
        # Optimize
        result = minimize(objective, initial_weights, method='SLSQP',
                        bounds=bounds, constraints=constraints)
        
        # Convert to monetary allocation
        allocation = {asset: weight * budget 
                     for asset, weight in zip(assets, result.x)}
        
        return allocation

def calculate_allocation(budget, risk_tolerance):
    """Main function to calculate asset allocation"""
    allocator = AssetAllocationML()
    
    # Get market data
    macro_data = allocator.get_macro_indicators()
    
    # Predict returns
    predicted_returns = allocator.predict_returns(macro_data, risk_tolerance)
    
    # Optimize portfolio
    allocation = allocator.optimize_portfolio(predicted_returns, risk_tolerance, budget)
    
    return allocation, predicted_returns

if __name__ == "__main__":
    # Example usage
    budget = 10000
    risk_tolerance = 2 # Scale of 1-10
    
    allocation, predicted_returns = calculate_allocation(budget, risk_tolerance)
    
    print("\nPredicted Annual Returns:")
    for asset, return_rate in predicted_returns.items():
        print(f"{asset}: {return_rate*100:.1f}%")
        
    print("\nRecommended Allocation:")
    for asset, amount in allocation.items():
        print(f"{asset}: ${amount:.2f}")
    
    
