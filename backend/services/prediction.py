import kagglehub
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

# Download dataset
path = kagglehub.dataset_download("paultimothymooney/stock-market-data")
print("Path to dataset files:", path)
sp500_csv_dir = os.path.join(path, "stock_market_data", "sp500", "csv")

stocks_file = os.path.join(sp500_csv_dir, "BMY.csv")
df = pd.read_csv(stocks_file)
print("Loaded dataset from:", stocks_file)
print(df.head())

print(df.describe())

print(df.shape)

print(df.info())

# plt.figure(figsize=(15,5))
# plt.plot(df['Close'])
# plt.title('BMY Close price.', fontsize=15)
# plt.ylabel('Price in dollars.')
# plt.show()

df = df.drop(['Adjusted Close'], axis=1)
df.isnull().sum()

features = ['Open', 'High', 'Low', 'Close', 'Volume']
plt.subplots(figsize=(20,10))

# df[df['Close'] == df['Adjusted Close']].shape

# for i, col in enumerate(features):
#     plt.subplot(2,3, i+1)
#     sb.distplot(df[col])
# plt.show()

# plt.subplots(figsize=(10,8))
# for i, col in enumerate(features):
#   plt.subplot(2,3,i+1)
#   sb.boxplot(df[col])
# plt.show()

splitted = df['Date'].str.split('/', expand=True)

df['day'] = splitted[1].astype('int')
df['month'] = splitted[0].astype('int')
df['year'] = splitted[2].astype('int')

df.head()



# Define the correct subdirectory where the CSV files are located
# sp500_csv_dir = os.path.join(path, "stock_market_data", "sp500", "csv")

# # Check if the directory exists
# if os.path.exists(sp500_csv_dir):
#     # Look for Tesla's stock file (TSLA.csv)
#     tsla_file = os.path.join(sp500_csv_dir, "BMY.csv")

#     if os.path.exists(tsla_file):
#         df = pd.read_csv(tsla_file)
#         print("Loaded dataset from:", tsla_file)
#         print(df.head())
#     else:
#         print("Tesla (BMY.csv) file not found in the dataset.")
# else:
#     print("S&P 500 CSV directory not found.")