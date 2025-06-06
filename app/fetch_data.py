import pandas as pd
import yfinance as yf

def fetch_data(ticker, start_date, end_date):
    
    data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)
    data.reset_index(inplace=True)
    return data

