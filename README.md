# Dynamic Asset Allocation System

## Overview
This project implements a **hybrid asset allocation strategy** that leverages **machine learning** for stock selection while using **linear algebra** and **macroeconomic/sentiment data** for broader asset class allocation.

## Key Components
1. **Stock Selection (ML-Based)**
   - Predicts future returns using an ML model (Random Forest, XGBoost, etc.)
   - Adjusts risk profile based on user selection (e.g., high risk prefers high return stocks)
   - Allocates stock weights dynamically based on ML predictions

2. **Category Allocation (Linear Algebra-Based)**
   - Stocks, bonds, cash, commodities have static base weights
   - Adjustments based on macroeconomic or sentiment indicators
   - Linear algebra method optimizes the category-level distribution

3. **Risk-Based Adjustments**
   - **High Risk** → More aggressive stocks, above the efficient frontier
   - **Medium/Low Risk** → Balanced mix with more stable assets

## Mathematical Formulation
### Stock Weights Calculation (ML-Based)
Let:
- \( X \) be a feature matrix of historical stock data
- \( Y \) be the target return vector
- \( f(X) \) be the trained ML model predicting expected return

The weight for each stock \( w_i \) is calculated as:
\[ w_i = \frac{f(X_i)}{\sum_{j} f(X_j)} \]

### Asset Category Allocation (Linear Algebra)
Given:
- **Risk tolerance factor** \( R \) (high = 1, medium = 0.5, low = 0.2)
- **Macroeconomic factor** \( M \) (scaled value from economic indicators)
- **Static base weights** \( W_0 \) for categories \( C \)

Final category weight adjustment:
\[ W_C = W_0 + (M \times R) \]

## Roadmap
1. **Train ML Model** for stock return prediction
2. **Develop Linear Algebra Model** for category allocation
3. **Integrate Macroeconomic Data** for dynamic category adjustments
4. **Build User Interface** for risk-based portfolio customization
5. **Backtest Strategy** on historical market data
6. **Optimize and Deploy**

## Installation
```bash
pip install -r requirements.txt
```

## Running the Model
```bash
python main.py
```

## Future Enhancements
- Improve ML model accuracy with additional financial indicators
- Implement real-time macroeconomic data integration
- Add reinforcement learning for adaptive portfolio rebalancing
