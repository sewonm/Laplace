import matplotlib.pyplot as plt
import json
from prediction import get_market_confidence, get_top_stocks

# Load user risk level (retrieved from some other file)
# with open("user_data.json", "r") as f:
#     user_data = json.load(f)
# risk = user_data.get("risk", "low")  # Default to low risk if not found
risk = "low"

budget = 1000


# Categories of investment
categories = ['stocks', 'bonds', 'cash', 'real_estate']

# Get market confidence score (should be >1 if confidence is high)
market_confidence = get_market_confidence()
# market_confidence = 1
print(market_confidence)


# # Get the top-performing stocks from a dataset
stocks_categories = get_top_stocks()
# stocks_categories = ["TSLA", "APPL", "MCST", "INTL"]
print(stocks_categories)


# Allocate portfolio based on risk level
allocation = {}

if risk == "low":
    allocation['stocks'] = 0.2 * market_confidence *10
    allocation['bonds'] = 0.5 * market_confidence * 100
    allocation['cash'] = 0.2 * market_confidence * 100
    allocation['real_estate'] = 0.1 * market_confidence * 10
elif risk == "medium":
    allocation['stocks'] = 0.5 * market_confidence
    allocation['bonds'] = 0.3 * market_confidence
    allocation['cash'] = 0.1 * market_confidence
    allocation['real_estate'] = 0.1 * market_confidence
elif risk == "high":
    allocation['stocks'] = 0.7 * market_confidence
    allocation['bonds'] = 0.1 * market_confidence
    allocation['cash'] = 0.1 * market_confidence
    allocation['real_estate'] = 0.1 * market_confidence

# Normalize allocation so the total sum equals 1
total_weight = sum(allocation.values())
allocation = {key: (value / total_weight) * budget for key, value in allocation.items()}

# Assign stocks to the stocks category
stock_allocation = {stock: allocation['stocks'] / len(stocks_categories) for stock in stocks_categories}

# Print allocation breakdown
print("\n### Portfolio Allocation ###")
for category, amount in allocation.items():
    print(f"{category.capitalize()}: ${amount:.2f}")

print("\n### Stock Allocation ###")
for stock, amount in stock_allocation.items():
    print(f"{stock}: ${amount:.2f}")

# Plot pie chart
labels = list(allocation.keys())
sizes = list(allocation.values())

plt.figure(figsize=(7, 7))
plt.pie(sizes, labels=labels, autopct=lambda p: f'${(p*budget/100):.2f}', startangle=140)
plt.title(f"Portfolio Allocation (Risk: {risk.capitalize()}, Budget: ${budget})")
plt.show()  # Prevents MacOS hanging