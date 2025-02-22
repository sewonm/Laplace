import numpy as np

# Budget
budget = 1000  

# Expected returns per category (adjust these values based on historical data)
r_stocks = 0.80  # Example: Worst-case drop of 5%
r_bonds = 1.08   # Example: Bonds gain 2%
r_cash = 1.00    # Cash stays constant
r_real_estate = 1.03  # Example: Real estate gains 3%

# Coefficient matrix (A)
A = np.array([
    [1, 1, 1, 1],       # Total budget equation
    [r_stocks, r_bonds, r_cash, r_real_estate]  # Expected return equation
])

# Result matrix (B)
B = np.array([budget, budget])  # We want our investment to remain $1000

# Solve for x1, x2, x3, x4
solution = np.linalg.lstsq(A, B, rcond=None)[0]

# Extract allocations
stocks_alloc, bonds_alloc, cash_alloc, real_estate_alloc = solution

# Display results
print("\n### Optimized Portfolio Allocation (Low-Risk Strategy) ###")
print(f"Stocks: ${stocks_alloc:.2f}")
print(f"Bonds: ${bonds_alloc:.2f}")
print(f"Cash: ${cash_alloc:.2f}")
print(f"Real Estate: ${real_estate_alloc:.2f}")

# Plot allocation
import matplotlib.pyplot as plt

labels = ["Stocks", "Bonds", "Cash", "Real Estate"]
values = [stocks_alloc, bonds_alloc, cash_alloc, real_estate_alloc]

plt.figure(figsize=(7, 7))
plt.pie(values, labels=labels, autopct=lambda p: f'${(p*budget/100):.2f}', startangle=140)
plt.title(f"Optimized Portfolio Allocation (Budget: ${budget})")
plt.show()