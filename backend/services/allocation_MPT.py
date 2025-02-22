import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from prediction_average import get_market_data

# Fetch real market data (expected returns & covariance matrix)
data = get_market_data()
expected_returns = data["returns"]
cov_matrix = data["cov_matrix"]

# Number of assets
num_assets = len(expected_returns)
budget = 1000

# Generate random portfolios (Monte Carlo simulation)
num_portfolios = 10000
weights_array = np.random.dirichlet(np.ones(num_assets), num_portfolios)
returns = weights_array @ expected_returns  # Expected portfolio return
volatilities = np.sqrt(np.einsum("ij,jk,ik->i", weights_array, cov_matrix, weights_array))  # Portfolio risk

# Efficient Frontier Optimization (MPT)
def portfolio_volatility(weights):
    """ Calculate portfolio standard deviation (risk). """
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

def objective(weights):
    """ Minimize risk for a given return. """
    return portfolio_volatility(weights)

# Constraints: Weights sum to 1
constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

# Bounds: Each weight is between 0 and 1
bounds = tuple((0, 1) for asset in range(num_assets))

# Optimize for minimum risk (efficient frontier)
optimized = minimize(objective, np.ones(num_assets) / num_assets, method='SLSQP', bounds=bounds, constraints=constraints)

# Get optimal portfolio
optimal_weights = optimized.x
optimal_return = np.dot(optimal_weights, expected_returns)
optimal_volatility = portfolio_volatility(optimal_weights)

# Plot Efficient Frontier
plt.figure(figsize=(10, 6))
plt.scatter(volatilities, returns, c=returns / volatilities, cmap="viridis", alpha=0.5, label="Random Portfolios")
plt.scatter(optimal_volatility, optimal_return, c="red", marker="*", s=200, label="Optimized Portfolio")
plt.colorbar(label="Sharpe Ratio (Return/Risk)")
plt.xlabel("Portfolio Risk (Volatility)")
plt.ylabel("Expected Return")
plt.title("Efficient Frontier with Optimal Portfolio")
plt.legend()
plt.grid()
plt.show()

# Print optimal allocation
asset_names = ["Stocks", "Bonds", "Cash", "Real Estate"]
allocations = optimal_weights * budget

print("\n### MPT Optimized Portfolio Allocation ###")
for name, amount in zip(asset_names, allocations):
    print(f"{name}: ${amount:.2f}")