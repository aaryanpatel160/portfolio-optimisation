# portfolio-optimisation

To run this file "python -m streamlit run portfolio-optimization-app.py"

Portfolio Optimization and Risk Management Tool

Developed a portfolio optimization tool using Python, leveraging Monte Carlo simulations to identify optimal stock allocations based on Sharpe Ratio and Volatility.
Utilized yFinance API to retrieve historical stock data for symbols like AAPL, MSFT, NVDA, and AMZN, analyzing two years of data to calculate expected returns and risk.
Implemented log returns and portfolio variance calculations to estimate expected portfolio performance across 1000 simulations.
Visualized results using Matplotlib, plotting risk-return profiles with color-coded Sharpe Ratios, and highlighted optimal portfolios.
Integrated the tool into a Streamlit web app, allowing users to input custom stock tickers and simulation parameters, providing an interactive platform for portfolio analysis.

## explaining the maths

### log returns
To convert from log returns (r) to simple returns (R):
𝑅=exp(𝑟)−1
Here, exp(r) represents the exponential function of r.

To convert from simple returns (R) to log returns (r):
𝑟=log(1+𝑅)r=log(1+R)

we are using log returns instead of normal returns as log returns can be easily aggregated over time, which is useful for multi-period analyses.
to explain this further:

Say you have returns of +25% one year followed by -20% the next year. This gets you back to initial value: $100 becomes $125, then $100. In other words, 0% total return.

Often we are tempted to describe things in terms of averages, but notice what happens if you take the average annual return:
(0.25 + -0.2) / 2 = 0.025

It is simply incorrect to say you should expect 2.5% from an asset that returns either +25% or -20% annually with equal likelihood.

Instead, you want to average the continuous growth, to capture the idea that they compound. This is what the logarithm provides: a measure of continuous growth rate. If you average log returns, you get:
(0.22314 + -0.22314) / 2 = 0

This website helps explain it better
https://robotwealth.com/the-intuition-of-log-returns/

The resaon we log the the returns and not the risk free rate is because if you log the risk-free rate, you’re assuming continuous compounding, which is not typically how the risk-free rate (like the yield on a government bond) is presented.



The expected returns per year = average daily return * 252 trading days

i calculate the expected volatility per year by using portfolio variance formula (search up if unfamiliar)
![image](https://github.com/user-attachments/assets/40679989-4bd0-4db8-bf74-0b007b19dc3b)
the key part of this formula is that is the covariance between assets. if the covariance is high then the correlation between the assets is high. for example they could all be tech stocks. this is bad as if all the tech stocks are down our portfolio takes a massive hit. it is good to spread out what you invest in.


and finally the sharpe ratio
the sharpe ratio is the (expected returns - the risk free rate) / volatility
