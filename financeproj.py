#SETUP
import pandas as pd
import numpy as np
import datetime as dt
import pandas_datareader as web
import matplotlib.pyplot as plt
from functions import return_portfolios, optimal_portfolio
print("Hello")
symbols = ['DAC', 'DDS', 'SPLP', 'IDT', 'JYNT']
start = dt.datetime(2021, 1, 1)
end = dt.datetime(2021, 7, 1)
stock_data = web.get_data_yahoo(symbols, start, end)

#CALCULATE FINANCIAL STATS
#adjusted closing prices over time
plt.plot(stock_data['Adj Close'], label = symbols)
plt.legend()
plt.xlabel('Date')
plt.ylabel('Adjusted Closing Prices Over Time')
plt.title('Stocks Adjusted Price')
plt.show()

#variance of simple rate of return over time
variance_srr = [stock_data['Adj Close']['DAC'].pct_change().var(),
                stock_data['Adj Close']['DDS'].pct_change().var(),
                stock_data['Adj Close']['SPLP'].pct_change().var(),
                stock_data['Adj Close']['IDT'].pct_change().var(),
                stock_data['Adj Close']['JYNT'].pct_change().var()]
plt.bar(range(len(symbols)), variance_srr, label = symbols)
plt.xticks(range(len(symbols)), symbols)
plt.xlabel('Stocks')
plt.ylabel('Variance of Simple Rate of Return')
plt.title('Variance of SRR for each Stock')
plt.show()

#mean of simple rate of return for each stock
expected_returns = stock_data['Adj Close'].pct_change().mean()
plt.bar(range(len(symbols)), expected_returns, label = symbols)
plt.xticks(range(len(symbols)), symbols)
plt.xlabel('Stocks')
plt.ylabel('Mean of SRR')
plt.title('Mean of SRR for each Stock')
plt.show()

#finding covariance
cov_quarterly = stock_data['Adj Close'].pct_change().cov()
print(cov_quarterly)

#OPTIMIZED PORTFOLIO
#random portfolios
random_portfolios = return_portfolios(expected_returns, cov_quarterly)
plt.scatter(random_portfolios.Volatility, random_portfolios.Returns)
#plt.show()

#efficient frontier
weights, returns, risks = optimal_portfolio(stock_data["Adj Close"].pct_change()[1:])
plt.plot(risks, returns, 'y-o')
plt.xlabel('Volatility(Standard Deviation)')
plt.ylabel('Expcted Returns')
plt.title('Efficient Frontier')
plt.show()
