# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 13:26:06 2021

@author: Leon aka Gitt Gott aka PP Koryphäe
"""

from base import load_obj

from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
from datetime import datetime


START_DATE = "2017-01-01"
END_DATE = datetime.now().strftime("%Y-%m-%d")

def get_yahoo_data(ticker, start_date, end_date):
    try:
        stock_data = data.DataReader(ticker, "yahoo", start_date, end_date)
        return stock_data
    except RemoteDataError:
        print(RemoteDataError)
        return None


if __name__ == "__main__":
    spCompanies = load_obj("SandP_Tickers")
    returns = {}
    for ticker in spCompanies:
        try:
            stock_history =  get_yahoo_data(ticker, START_DATE,END_DATE)
            stock_history.to_csv(f"{ticker}.csv")
        except:
            pass
