import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler

# Streamlit setup
st.title("Portfolio Optimization")
st.write("This app simulates different portfolio allocations to find the best return for the amount of risk taken.")

# User inputs for the tickers and number of simulations
symbols = st.text_input("Enter stock tickers separated by commas (e.g., AAPL, MSFT, NVDA, AMZN):", "AAPL, MSFT, NVDA, AMZN")
symbols = [symbol.strip().upper() for symbol in symbols.split(',')]
number_of_symbols = len(symbols)

num_of_simulations = st.slider("Number of Simulations:", min_value=100, max_value=10000, value=1000)

# Retrieve stock data
price_data = pd.DataFrame()

for symbol in symbols:
    stock_data = yf.Ticker(symbol)
    history = stock_data.history(period="2y")
    history = history[['Close']].rename(columns={'Close': symbol})
    if price_data.empty:
        price_data = history
    else:
        price_data = price_data.join(history, how='outer')

# Setting up arrays for simulation data
all_weights = np.zeros((num_of_simulations, number_of_symbols))
ret_arr = np.zeros(num_of_simulations)
vol_arr = np.zeros(num_of_simulations)
sharpe_arr = np.zeros(num_of_simulations)

# Run the simulation
log_return = np.log(1 + price_data.pct_change())

for ind in range(num_of_simulations):
    random_weights = np.array(np.random.random(number_of_symbols))
    rebalance_weights = random_weights / np.sum(random_weights)
    all_weights[ind, :] = rebalance_weights

    exp_ret = np.sum((log_return.mean() * rebalance_weights) * 252)
    ret_arr[ind] = exp_ret

    exp_vol = np.sqrt(
        np.dot(
            rebalance_weights.T,
            np.dot(
                log_return.cov() * 252,
                rebalance_weights
            )
        )
    )
    vol_arr[ind] = exp_vol

    sharpe_ratio = (exp_ret - 0.039) / exp_vol
    sharpe_arr[ind] = sharpe_ratio

# Store the results in a DataFrame
simulation_data = [ret_arr, vol_arr, sharpe_arr, all_weights]
simulation_df = pd.DataFrame(data=simulation_data).T
simulation_df.columns = ['Returns', 'Volatility', 'Sharpe Ratio', 'Portfolio Weights']

# Identify the max Sharpe ratio and min Volatility
max_sharpe_ratio = simulation_df.loc[simulation_df['Sharpe Ratio'].idxmax()]
min_volatility = simulation_df.loc[simulation_df['Volatility'].idxmin()]

# Convert np.float64 to standard Python float for display
max_sharpe_weights = {symbols[i]: float(max_sharpe_ratio['Portfolio Weights'][i]) for i in range(number_of_symbols)}
min_vol_weights = {symbols[i]: float(min_volatility['Portfolio Weights'][i]) for i in range(number_of_symbols)}

# Display the results
st.write('### Max Sharpe Ratio Portfolio:')
st.write(max_sharpe_ratio.drop('Portfolio Weights'))
st.write(f"Weights: {max_sharpe_weights}")

st.write('### Min Volatility Portfolio:')
st.write(min_volatility.drop('Portfolio Weights'))
st.write(f"Weights: {min_vol_weights}")

# Plot the results
plt.figure(figsize=(10, 6))
plt.scatter(
    y=simulation_df['Returns'],
    x=simulation_df['Volatility'],
    c=simulation_df['Sharpe Ratio'],
    cmap='RdYlBu'
)
plt.title('Portfolio Returns Vs. Risk')
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('Standard Deviation (Volatility)')
plt.ylabel('Returns')

plt.scatter(
    max_sharpe_ratio['Volatility'],
    max_sharpe_ratio['Returns'],
    marker=(5, 1, 0),
    color='r',
    s=600,
    label='Max Sharpe Ratio'
)

plt.scatter(
    min_volatility['Volatility'],
    min_volatility['Returns'],
    marker=(5, 1, 0),
    color='b',
    s=600,
    label='Min Volatility'
)

plt.legend()
st.pyplot(plt)