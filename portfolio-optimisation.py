#### EXPLANATION IN README FILE ####
#### GETTING THE DATA ####


#want to get the best return for the amount of risk that we are taking
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


from sklearn.preprocessing import StandardScaler #to standardise data
import yfinance as yf

pd.set_option('display.max_colwidth', 0)
pd.set_option('expand_frame_repr', False)

#later on request user for symbols
symbols = ['AAPL','MSFT','NVDA','AMZN']

#no. of symbols
number_of_symbols = len(symbols)

price_data = pd.DataFrame()

# Loop through each symbol to retrieve data
for symbol in symbols:
    # Fetch the data for the current symbol
    stock_data = yf.Ticker(symbol)
    history = stock_data.history(period="2y")

    # Extract the 'Close' column and rename it to the symbol (rename is a pandas function)
    history = history[['Close']].rename(columns={'Close': symbol})

    # Merge this ticker's data with the main DataFrame
    if price_data.empty:
        price_data = history
    else:
        #join is a pandas method
        price_data = price_data.join(history, how='outer')


### setting up arrays to store simulation data

num_of_simulations = 1000

all_weights = np.zeros((num_of_simulations, number_of_symbols))

ret_arr = np.zeros(num_of_simulations)

vol_arr = np.zeros(num_of_simulations)

sharpe_arr = np.zeros(num_of_simulations)


#### RUNNING THE SIMULATION ####

log_return = np.log(1+ price_data.pct_change())


for ind in range(num_of_simulations):


    # generates an array of random numbers
    random_weights = np.array(np.random.random(number_of_symbols))

    # makes sure all weights add upto 1
    rebalance_weights = random_weights / np.sum(random_weights)

    all_weights[ind, :] = rebalance_weights

    # calculate the expected returns per year (average daily return * 252 trading days)
    exp_ret = np.sum((log_return.mean() * rebalance_weights) *252)
    ret_arr[ind] = exp_ret

    # calculate the expected volatility per year (using portfolio variance formula)

    exp_vol = np.sqrt(
        np.dot(
            rebalance_weights.T,
            np.dot(
                log_return.cov() *252,
                rebalance_weights
            )
        )
    )
    vol_arr[ind] = exp_vol

    # calculate the sharpe ratio (risk free rate = UK 10 year Gilt which as august 2024 is 3.9%)
    sharpe_ratio = (exp_ret - 0.039) / exp_vol
    sharpe_arr[ind] = sharpe_ratio


simulation_data = [ret_arr, vol_arr, sharpe_arr, all_weights]

simulation_df = pd.DataFrame(data=simulation_data).T

# Give the columns the Proper Names.
simulation_df.columns = [
    'Returns',
    'Volatility',
    'Sharpe Ratio',
    'Portfolio Weights'
]

# Print out the results.
print('')
print('='*80)
print('SIMULATIONS RESULT:')
print('-'*80)
print(simulation_df.head())
print('-'*80)

max_sharpe_ratio = simulation_df.loc[simulation_df['Sharpe Ratio'].idxmax()]

min_volatility = simulation_df.loc[simulation_df['Volatility'].idxmin()]

print('')
print('='*80)
print('MAX SHARPE RATIO:')
print('-'*80)
print(max_sharpe_ratio)
print('-'*80)

print('')
print('='*80)
print('MIN VOLATILITY:')
print('-'*80)
print(min_volatility)
print('-'*80)


# Plot the data on a Scatter plot.
plt.scatter(
    y=simulation_df['Returns'],
    x=simulation_df['Volatility'],
    c=simulation_df['Sharpe Ratio'],
    cmap='RdYlBu'
)

# Give the Plot some labels, and titles.
plt.title('Portfolio Returns Vs. Risk')
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('Standard Deviation')
plt.ylabel('Returns')

# Plot the Max Sharpe Ratio, using a `Red Star`.
plt.scatter(
    max_sharpe_ratio[1],
    max_sharpe_ratio[0],
    marker=(5, 1, 0),
    color='r',
    s=600
)

# Plot the Min Volatility, using a `Blue Star`.
plt.scatter(
    min_volatility[1],
    min_volatility[0],
    marker=(5, 1, 0),
    color='b',
    s=600
)

# Finally, show the plot.
plt.show()


