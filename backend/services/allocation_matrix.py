import numpy as np
import matplotlib.pyplot as plt
from enhanced_allocation import calculate_allocation

def visualize_allocation(allocation, budget, risk_tolerance):
    """Create visualization for the allocation"""
    labels = list(allocation.keys())
    values = list(allocation.values())
    
    # Create pie chart
    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)
    plt.pie(values, labels=labels, autopct=lambda p: f'${(p*budget/100):.2f}', startangle=140)
    plt.title(f"Portfolio Allocation (Risk Tolerance: {risk_tolerance}/10)")
    
    # Create bar chart
    plt.subplot(1, 2, 2)
    plt.bar(labels, [v/budget*100 for v in values])
    plt.title("Allocation Percentages")
    plt.ylabel("Percentage (%)")
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()

def get_allocation(budget, risk_tolerance):
    """Get and visualize optimal allocation"""
    # Get allocation and predicted returns
    allocation, predicted_returns = calculate_allocation(budget, risk_tolerance)
    
    # Display results
    print("\n### Portfolio Allocation Summary ###")
    print(f"Budget: ${budget:.2f}")
    print(f"Risk Tolerance: {risk_tolerance}/10")
    
    print("\nPredicted Annual Returns:")
    for asset, return_rate in predicted_returns.items():
        print(f"{asset}: {return_rate*100:.1f}%")
    
    print("\nRecommended Allocation:")
    for asset, amount in allocation.items():
        print(f"{asset}: ${amount:.2f} ({amount/budget*100:.1f}%)")
    
    # Visualize the allocation
    visualize_allocation(allocation, budget, risk_tolerance)
    
    return allocation, predicted_returns

if __name__ == "__main__":
    # Example usage
    budget = 10000
    risk_tolerance = 2 # Scale of 1-10
    allocation, _ = get_allocation(budget, risk_tolerance)