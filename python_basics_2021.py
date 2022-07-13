#Stock Screener

#from keys2 import ameritrade
import os

from matplotlib import pyplot as plt
import requests, time, re, os
import pandas as pd
import pickle as pkl
import datetime
import pandas_datareader.data as web
import plotly as px
import datetime as dt
import plotly.graph_objs as go
#data source
import yfinance as yf
#data visualization
import plotly.graph_objs as go
from datetime import datetime
import intrinio_sdk
import numpy as np
from pandas import read_json

url = 'https://api.tdameritrade.com/v1/instruments'

df = pd.read_excel('CompanyList.xlsx')
symbols = df["Ticker"].values.tolist()

start = 0
end = 500
files = []
filteredTickerVals = []
while start < len(symbols):
    tickers = symbols[start:end]
    payload = {'apikey': 'XTITDUJICQPUILWTZUIY89HZM5RVT31S',
               'symbol': tickers,
               'projection': 'fundamental'}

    results = requests.get(url, params=payload)
    data = results.json()
    f_name = time.asctime() + ".pkl"
    f_name = re.sub('[ :]', '_', f_name)
    files.append(f_name)
    with open(f_name, 'wb') as file:
        pkl.dump(data, file)
    start = end
    end += 500
    time.sleep(1)

data = []
peg_list = []
for file in files:
    with open(file, 'rb') as f:
        info = pkl.load(f)
    tickers = list(info)
    points = ['symbol', 'netProfitMarginMRQ', 'peRatio', 'pegRatio', 'high52']
    points_PEG = ['symbol', 'pegRatio']
    for ticker in tickers:
        tick = []
        tick2 = []
        for point in points:
            tick.append(info[ticker]['fundamental'][point])
        for point2 in points_PEG:
            tick2.append(info[ticker]['fundamental'][point2])
        data.append(tick)
        peg_list.append(tick2)
    os.remove(file)

points = ['Ticker', 'Margin', 'PE', 'PEG', '52 Week High']
PEG_list = ['Ticker', 'PEG']
df_results = pd.DataFrame(data, columns=points)
df_PEG = pd.DataFrame(peg_list, columns=PEG_list).sort_values('PEG')
df_PEG = df_PEG[(df_PEG['PEG'] < 1) & df_PEG['PEG'] > 0]

#contains all the tickers of undervalued companies
filteredTickerVals = list(df_PEG['Ticker'])
print(filteredTickerVals)

#TD Ameritrade Getting Hostorical Stock Data------------------------------------------------------------------------
start2 = dt.datetime(2021, 1, 1)
end2 = dt.datetime.now()
for filteredTick in filteredTickerVals:
    historical_stock_data_url = f'https://api.tdameritrade.com//v1/marketdata/{filteredTick}/pricehistory?apikey=XTITDUJICQPUILWTZUIY89HZM5RVT31S&periodType=day'
    response = requests.get(historical_stock_data_url)
    tmp = read_json(historical_stock_data_url)

    print(tmp)

